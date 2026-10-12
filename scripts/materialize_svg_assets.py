#!/usr/bin/env python3
"""Restore the 1,500 original SVG files distributed in a verified archive."""
from pathlib import Path
import hashlib
import tarfile

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets' / 'svg_elements'
ARCHIVE = ASSETS / 'svg-originals-1500.tar.xz'
SHA256 = 'e304d54bec8e750b36358b86a74996a8c090be1594f629db56f23f825165e3cb'

def main():
    if hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() != SHA256:
        raise ValueError('SVG archive checksum mismatch')
    restored = 0
    with tarfile.open(ARCHIVE, 'r:xz') as archive:
        members = archive.getmembers()
        if len(members) != 1500:
            raise ValueError('Expected exactly 1,500 original SVG files')
        for member in members:
            path = Path(member.name)
            if not member.isfile() or len(path.parts) != 2 or path.parts[0] != 'files' or path.suffix != '.svg':
                raise ValueError('Unexpected archive path')
            data = archive.extractfile(member).read()
            target = ASSETS / path
            if target.exists() and target.read_bytes() == data:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            restored += 1
    print(f'1,500 original SVG assets verified; {restored} files restored.')

if __name__ == '__main__':
    main()
