from __future__ import annotations

import importlib.util
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "verify-artifact-delivery"
    / "scripts"
    / "inspect_artifact.py"
)
SPEC = importlib.util.spec_from_file_location("inspect_artifact", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class InspectArtifactTests(unittest.TestCase):
    def make_zip(self, members: dict[str, bytes]) -> Path:
        directory = Path(tempfile.mkdtemp())
        archive = directory / "artifact.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
            for name, payload in members.items():
                handle.writestr(name, payload)
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        return archive

    def test_safe_archive_passes(self) -> None:
        result = MODULE.inspect(self.make_zip({"release/app.txt": b"ready"}))
        archive = result["archive"]
        self.assertEqual([], archive["unsafe_members"])
        self.assertEqual([], archive["link_members"])
        self.assertEqual([], archive["suspicious_members"])
        self.assertFalse(archive["oversized_archive"])

    def test_parent_and_windows_drive_paths_are_unsafe(self) -> None:
        result = MODULE.inspect(
            self.make_zip({"../escape.txt": b"x", "C:\\temp\\secret.txt": b"y"})
        )
        self.assertEqual(
            ["../escape.txt", "C:\\temp\\secret.txt"],
            result["archive"]["unsafe_members"],
        )

    def test_windows_devices_and_alternate_streams_are_unsafe(self) -> None:
        result = MODULE.inspect(
            self.make_zip(
                {
                    "release/NUL.txt": b"device",
                    "release/report.txt:secret": b"stream",
                }
            )
        )
        self.assertEqual(
            ["release/NUL.txt", "release/report.txt:secret"],
            result["archive"]["unsafe_members"],
        )

    def test_symlink_member_is_rejected(self) -> None:
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        archive = directory / "link.zip"
        info = zipfile.ZipInfo("current")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr(info, "release-v2")
        result = MODULE.inspect(archive)
        self.assertEqual(["current"], result["archive"]["link_members"])

    def test_fifo_and_device_members_are_rejected(self) -> None:
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        archive = directory / "special-files.zip"
        fifo = zipfile.ZipInfo("release/events")
        fifo.create_system = 3
        fifo.external_attr = (stat.S_IFIFO | 0o600) << 16
        device = zipfile.ZipInfo("release/device")
        device.create_system = 3
        device.external_attr = (stat.S_IFCHR | 0o600) << 16
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr(fifo, b"")
            handle.writestr(device, b"")
        result = MODULE.inspect(archive)
        self.assertEqual(
            ["release/events", "release/device"],
            result["archive"]["special_file_members"],
        )

    def test_excessive_member_count_is_rejected(self) -> None:
        original_limit = MODULE.MAX_ARCHIVE_MEMBERS
        MODULE.MAX_ARCHIVE_MEMBERS = 1
        self.addCleanup(setattr, MODULE, "MAX_ARCHIVE_MEMBERS", original_limit)
        result = MODULE.inspect(self.make_zip({"one": b"", "two": b""}))
        self.assertTrue(result["archive"]["too_many_members"])

    def test_high_ratio_member_is_suspicious(self) -> None:
        payload = b"0" * MODULE.MIN_RATIO_CHECK_BYTES
        result = MODULE.inspect(self.make_zip({"expanded.bin": payload}))
        self.assertEqual(["expanded.bin"], result["archive"]["suspicious_members"])

    def test_duplicate_and_portable_path_aliases_are_rejected(self) -> None:
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        archive = directory / "aliases.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("release/app.txt", "first")
            handle.writestr("release/app.txt", "second")
            handle.writestr("Release\\README.md", "windows")
            handle.writestr("release/readme.md", "posix")
        result = MODULE.inspect(archive)
        self.assertEqual(
            [
                "release/app.txt",
                "release/app.txt",
                "Release\\README.md",
                "release/readme.md",
            ],
            result["archive"]["ambiguous_members"],
        )

    def test_unicode_and_windows_trim_aliases_are_rejected(self) -> None:
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(directory))
        archive = directory / "portable-aliases.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            handle.writestr("release/caf\N{LATIN SMALL LETTER E WITH ACUTE}.txt", "nfc")
            handle.writestr("release/cafe\N{COMBINING ACUTE ACCENT}.txt", "nfd")
            handle.writestr("release/report.txt", "plain")
            handle.writestr("release/report.txt. ", "trimmed")
        result = MODULE.inspect(archive)
        self.assertEqual(
            [
                "release/caf\N{LATIN SMALL LETTER E WITH ACUTE}.txt",
                "release/cafe\N{COMBINING ACUTE ACCENT}.txt",
                "release/report.txt",
                "release/report.txt. ",
            ],
            result["archive"]["ambiguous_members"],
        )


if __name__ == "__main__":
    unittest.main()
