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

    def test_high_ratio_member_is_suspicious(self) -> None:
        payload = b"0" * MODULE.MIN_RATIO_CHECK_BYTES
        result = MODULE.inspect(self.make_zip({"expanded.bin": payload}))
        self.assertEqual(["expanded.bin"], result["archive"]["suspicious_members"])


if __name__ == "__main__":
    unittest.main()
