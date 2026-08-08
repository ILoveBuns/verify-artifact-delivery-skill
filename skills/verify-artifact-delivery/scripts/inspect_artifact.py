#!/usr/bin/env python3
"""Produce a safe structural inventory for a local artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import stat
from pathlib import Path, PurePosixPath
import zipfile


MAX_COMPRESSION_RATIO = 1_000
MIN_RATIO_CHECK_BYTES = 1024 * 1024
MAX_MEMBER_BYTES = 1024 * 1024 * 1024
MAX_ARCHIVE_BYTES = 4 * 1024 * 1024 * 1024
WINDOWS_DRIVE_RE = re.compile(r"^[A-Za-z]:/")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def unsafe_member(name: str) -> bool:
    normalized = name.replace("\\", "/")
    path = PurePosixPath(normalized)
    return (
        path.is_absolute()
        or bool(WINDOWS_DRIVE_RE.match(normalized))
        or ".." in path.parts
    )


def is_link(member: zipfile.ZipInfo) -> bool:
    mode = (member.external_attr >> 16) & 0xFFFF
    return stat.S_ISLNK(mode)


def compression_ratio(member: zipfile.ZipInfo) -> float:
    if member.file_size == 0:
        return 0.0
    if member.compress_size == 0:
        return float("inf")
    return member.file_size / member.compress_size


def suspicious_member(member: zipfile.ZipInfo) -> bool:
    return (
        member.file_size > MAX_MEMBER_BYTES
        or (
            member.file_size >= MIN_RATIO_CHECK_BYTES
            and compression_ratio(member) > MAX_COMPRESSION_RATIO
        )
    )


def inspect(path: Path) -> dict:
    result: dict = {
        "path": str(path.resolve()),
        "exists": path.exists(),
        "kind": "missing",
    }
    if not path.exists():
        return result
    if path.is_dir():
        entries = sorted(
            str(item.relative_to(path)) for item in path.rglob("*") if item.is_file()
        )
        result.update(
            kind="directory",
            file_count=len(entries),
            files=entries[:200],
            truncated=len(entries) > 200,
        )
        return result
    result.update(
        kind="file",
        size_bytes=path.stat().st_size,
        extension=path.suffix.lower(),
        mime_type=mimetypes.guess_type(path.name)[0] or "application/octet-stream",
        sha256=sha256(path),
    )
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            members = archive.infolist()
            unsafe = [member.filename for member in members if unsafe_member(member.filename)]
            links = [member.filename for member in members if is_link(member)]
            encrypted = [member.filename for member in members if member.flag_bits & 0x1]
            suspicious = [
                member.filename for member in members if suspicious_member(member)
            ]
            uncompressed_bytes = sum(member.file_size for member in members)
            result["archive"] = {
                "member_count": len(members),
                "uncompressed_bytes": uncompressed_bytes,
                "members": [member.filename for member in members[:200]],
                "truncated": len(members) > 200,
                "unsafe_members": unsafe,
                "link_members": links,
                "encrypted_members": encrypted,
                "suspicious_members": suspicious,
                "oversized_archive": uncompressed_bytes > MAX_ARCHIVE_BYTES,
                "crc_check": archive.testzip(),
            }
    return result


def human(result: dict) -> str:
    lines = [f"path: {result['path']}", f"exists: {str(result['exists']).lower()}"]
    if not result["exists"]:
        return "\n".join(lines)
    lines.append(f"kind: {result['kind']}")
    if result["kind"] == "directory":
        lines.append(f"file_count: {result['file_count']}")
        return "\n".join(lines)
    lines.extend(
        [
            f"size_bytes: {result['size_bytes']}",
            f"mime_type: {result['mime_type']}",
            f"sha256: {result['sha256']}",
        ]
    )
    archive = result.get("archive")
    if archive:
        lines.extend(
            [
                f"archive_member_count: {archive['member_count']}",
                f"archive_crc_check: {archive['crc_check'] or 'ok'}",
                f"unsafe_archive_members: {len(archive['unsafe_members'])}",
                f"archive_link_members: {len(archive['link_members'])}",
                f"archive_encrypted_members: {len(archive['encrypted_members'])}",
                f"archive_suspicious_members: {len(archive['suspicious_members'])}",
                f"archive_oversized: {str(archive['oversized_archive']).lower()}",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = inspect(args.path)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else human(result))
    if not result["exists"]:
        return 2
    if result["kind"] == "file" and result["size_bytes"] == 0:
        return 3
    archive = result.get("archive")
    if archive and (
        archive["unsafe_members"]
        or archive["link_members"]
        or archive["encrypted_members"]
        or archive["suspicious_members"]
        or archive["oversized_archive"]
        or archive["crc_check"]
    ):
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
