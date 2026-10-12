#!/usr/bin/env python3
"""Restore the original VL asset files from verified lossless bundle parts.

The .cube codec stores the *existing* seven-decimal table as exact integers
with second differences. It does not resample, round, or change a LUT value.
Python's standard library is sufficient; every restored file is checked
against the SHA-256 of its original bytes before atomic installation.
"""
from __future__ import annotations

import argparse
from array import array
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import struct
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parent.parent / "assets" / "vlog_montage"
MAGIC = b"VLCUBE01"
CODEC = "cube-decimal-delta2-v1"


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def safe_name(name):
    if not isinstance(name, str) or not name or "\\" in name or "\0" in name:
        raise ValueError("Invalid bundle path")
    p = PurePosixPath(name)
    if p.is_absolute() or any(x in ("", ".", "..") for x in name.split("/")):
        raise ValueError("Invalid bundle path: " + name)
    return p


def safe_destination(root, name):
    current = root
    parts = safe_name(name).parts
    for i, part in enumerate(parts):
        current = current / part
        if current.is_symlink():
            raise ValueError("Symlink components are not allowed in VL asset paths: " + name)
        if i < len(parts) - 1 and current.exists() and not current.is_dir():
            raise ValueError("VL asset parent is not a directory: " + name)
    if not current.resolve().is_relative_to(root):
        raise ValueError("VL asset path escapes its collection")
    return current


def encode_cube(data):
    """Losslessly precondition this collection's fixed seven-decimal .cube."""
    lines = data.splitlines(keepends=True)
    first = next(i for i, line in enumerate(lines) if re.match(rb"[0-9]", line))
    header = b"".join(lines[:first])
    rows = lines[first:]
    if len(rows) != 33 ** 3 or b"LUT_3D_SIZE 33\n" not in header:
        raise ValueError("Expected an original 33-cube")
    previous = [0, 0, 0]
    differences = [0, 0, 0]
    codes = array("i")
    if codes.itemsize != 4:
        raise RuntimeError("32-bit integer arrays are required")
    for row in rows:
        if not re.fullmatch(rb"[01]\.[0-9]{7} [01]\.[0-9]{7} [01]\.[0-9]{7}\n", row):
            raise ValueError("Cube is not in the exact original decimal format")
        for channel, token in enumerate(row.split()):
            q = int(token.replace(b".", b""))
            if not 0 <= q <= 10_000_000:
                raise ValueError("LUT value outside the normalized domain")
            difference = q - previous[channel]
            codes.append(difference - differences[channel])
            previous[channel] = q
            differences[channel] = difference
    if sys.byteorder != "little":
        codes.byteswap()
    return MAGIC + struct.pack("<II", len(header), len(rows)) + header + codes.tobytes()


def decode_cube(data):
    if len(data) < 16 or data[:8] != MAGIC:
        raise ValueError("Unknown LUT bundle codec")
    header_size, rows = struct.unpack("<II", data[8:16])
    if not 0 < header_size <= 65536 or rows != 33 ** 3:
        raise ValueError("Invalid LUT bundle dimensions")
    if len(data) != 16 + header_size + rows * 3 * 4:
        raise ValueError("Truncated LUT bundle table")
    header = data[16:16 + header_size]
    if b"LUT_3D_SIZE 33\n" not in header:
        raise ValueError("Wrong LUT header size")
    codes = array("i")
    if codes.itemsize != 4:
        raise RuntimeError("32-bit integer arrays are required")
    codes.frombytes(data[16 + header_size:])
    if sys.byteorder != "little":
        codes.byteswap()
    values = [0, 0, 0]
    differences = [0, 0, 0]
    lines = []
    for offset in range(0, len(codes), 3):
        tokens = []
        for channel in range(3):
            differences[channel] += codes[offset + channel]
            values[channel] += differences[channel]
            q = values[channel]
            if not 0 <= q <= 10_000_000:
                raise ValueError("Decoded LUT value outside the normalized domain")
            tokens.append(f"{q // 10_000_000}.{q % 10_000_000:07d}")
        lines.append(" ".join(tokens) + "\n")
    return header + "".join(lines).encode("ascii")


def validate_manifest(manifest):
    if manifest.get("version") != 1 or manifest.get("archive_format") != "tar.xz":
        raise ValueError("Unsupported VL bundle manifest")
    entries = {}
    names = set()
    for row in manifest.get("files", []):
        name = str(safe_name(row["file"]))
        entry = str(safe_name(row["entry"]))
        if name in names or entry in entries:
            raise ValueError("Duplicate VL bundle path")
        if row.get("codec") not in ("raw", CODEC):
            raise ValueError("Unsupported VL file codec")
        if not isinstance(row["size"], int) or not 0 <= row["size"] <= 16 * 1024 * 1024:
            raise ValueError("Invalid VL file size")
        if not re.fullmatch(r"[a-f0-9]{64}", row["sha256"]):
            raise ValueError("Invalid VL file checksum")
        names.add(name)
        entries[entry] = row
    if len(entries) != manifest.get("file_count") or not entries:
        raise ValueError("Invalid VL bundle file count")
    for part in manifest.get("parts", []):
        safe_name(part["file"])
        if not re.fullmatch(r"[a-f0-9]{64}", part["sha256"]):
            raise ValueError("Invalid VL part checksum")
    return entries


def prepare(root=ROOT, verify=False):
    """Prepare missing assets; keep existing edited files instead of clobbering."""
    root = Path(root).resolve()
    manifest_path = root / "bundle_manifest.json"
    if not manifest_path.is_file():
        # Atlas toolkit users may have already extracted the regular asset ZIPs.
        raise ValueError("VL bundle manifest is missing; extract the matching Atlas asset packs")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entries = validate_manifest(manifest)
    complete = True
    for row in entries.values():
        p = safe_destination(root, row["file"])
        if p.is_file() and verify and digest(p) != row["sha256"]:
            raise ValueError("Existing VL file differs from its original checksum: " + row["file"])
        if not p.is_file():
            complete = False
    if complete:
        return {"prepared": False, "files": len(entries), "verified": verify, "archive_sha256": manifest["archive_sha256"]}
    # Linux flock serializes simultaneous CLI calls; the lock never stores data.
    import fcntl
    root.mkdir(parents=True, exist_ok=True)
    with (root / ".bundle-extract.lock").open("a+b") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        if verify:
            for row in entries.values():
                p = safe_destination(root, row["file"])
                if p.is_file() and digest(p) != row["sha256"]:
                    raise ValueError("Existing VL file differs from its original checksum: " + row["file"])
        with tempfile.TemporaryDirectory(prefix=".vlog-prepare-", dir=root.parent) as temp:
            temp = Path(temp)
            archive = temp / "bundle.tar.xz"
            combined = hashlib.sha256()
            total = 0
            with archive.open("wb") as out:
                for part in manifest["parts"]:
                    p = safe_destination(root, part["file"])
                    if not p.is_file():
                        raise ValueError("VL bundle part is missing")
                    part_hash = hashlib.sha256()
                    part_size = 0
                    with p.open("rb") as f:
                        for block in iter(lambda: f.read(1024 * 1024), b""):
                            part_hash.update(block); combined.update(block)
                            out.write(block); part_size += len(block)
                    if part_hash.hexdigest() != part["sha256"] or part_size != part["size"]:
                        raise ValueError("VL bundle part checksum mismatch")
                    total += part_size
            if total != manifest["archive_size"] or combined.hexdigest() != manifest["archive_sha256"]:
                raise ValueError("VL archive checksum mismatch")
            staged = temp / "files"
            staged.mkdir()
            seen = set()
            with tarfile.open(archive, "r:xz") as tar:
                for member in tar:
                    entry = str(safe_name(member.name))
                    if not member.isfile() or entry not in entries or entry in seen:
                        raise ValueError("Unsafe or unexpected VL archive entry")
                    row = entries[entry]
                    limit = 16 * 1024 * 1024
                    if not 0 <= member.size <= limit:
                        raise ValueError("Oversized VL archive entry")
                    stream = tar.extractfile(member)
                    if stream is None:
                        raise ValueError("Missing VL archive data")
                    data = stream.read(limit + 1)
                    if len(data) != member.size or hashlib.sha256(data).hexdigest() != row["stored_sha256"]:
                        raise ValueError("VL stored entry checksum mismatch")
                    if row["codec"] == CODEC:
                        data = decode_cube(data)
                    if len(data) != row["size"] or hashlib.sha256(data).hexdigest() != row["sha256"]:
                        raise ValueError("VL restored asset checksum mismatch")
                    dest = staged.joinpath(*safe_name(row["file"]).parts)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    dest.write_bytes(data)
                    seen.add(entry)
            if seen != set(entries):
                raise ValueError("Incomplete VL asset archive")
            installed = preserved = 0
            for row in entries.values():
                relative = safe_name(row["file"])
                dest = safe_destination(root, row["file"])
                if dest.is_file():
                    if digest(dest) != row["sha256"]:
                        if verify:
                            raise ValueError("Existing VL file differs from its original checksum: " + row["file"])
                        preserved += 1
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                os.replace(staged.joinpath(*relative.parts), dest)
                installed += 1
            marker = temp / "ready.json"
            marker.write_text(json.dumps({"archive_sha256": manifest["archive_sha256"], "files": len(entries)}) + "\n")
            os.replace(marker, root / ".bundle-ready.json")
            return {"prepared": True, "files": len(entries), "installed": installed, "preserved_edited_files": preserved, "archive_sha256": manifest["archive_sha256"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--verify", action="store_true", help="Check all restored original SHA-256 values")
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args.root, args.verify), indent=2))
    except (ValueError, OSError, tarfile.TarError) as e:
        parser.error(str(e))


if __name__ == "__main__":
    main()
