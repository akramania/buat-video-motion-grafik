#!/usr/bin/env python3
"""Rebuild lossless VL source bundle parts after editing original assets.

Materialize the existing bundle before rebuilding. Production artwork,
preview media, recipes and indices remain byte-exact; .cube text is
losslessly preconditioned for smaller storage and restored by SHA-256.
"""
from pathlib import Path
import argparse
import hashlib
import io
import json
import lzma
import os
import tarfile
import tempfile
from prepare_vlog_assets import CODEC, ROOT, decode_cube, digest, encode_cube


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--part-size', type=int, default=8_000_000)
    parser.add_argument('--exclude-previews', action='store_true', help='Keep preview media on the existing Motion Atlas')
    args = parser.parse_args()
    root = args.root.resolve()
    if not 1_000_000 <= args.part_size <= 8_000_000:
        parser.error('part-size must be 1..8 MB')
    excluded = {'payload', '__pycache__'}
    excluded_names = {'bundle_manifest.json', 'bundle_qa.json', '.gitignore', '.bundle-ready.json', '.bundle-extract.lock'}
    paths = sorted(p for p in root.rglob('*') if p.is_file() and not any(x in excluded for x in p.relative_to(root).parts) and p.name not in excluded_names)
    if args.exclude_previews:
        paths = [p for p in paths if not p.is_relative_to(root/'previews')]
    if len(list(root.glob('luts/*.cube'))) != 100:
        parser.error('Prepare all 100 original LUT files before rebuilding')
    records = []
    with tempfile.TemporaryDirectory(prefix='vl-bundle-build-') as temp:
        archive = Path(temp) / 'vlog600.tar.xz'
        with lzma.open(archive, 'wb', preset=6) as stream:
            with tarfile.open(fileobj=stream, mode='w|') as tar:
                for path in paths:
                    name = path.relative_to(root).as_posix()
                    original = path.read_bytes()
                    if path.suffix == '.cube':
                        stored = encode_cube(original)
                        if decode_cube(stored) != original:
                            raise RuntimeError('LUT byte-exact reconstruction failed: '+name)
                        codec = CODEC; entry = name + '.vlcube'
                    else:
                        stored = original; codec = 'raw'; entry = name
                    info = tarfile.TarInfo(entry); info.size = len(stored); info.mode = 0o644; info.mtime = 0
                    tar.addfile(info, io.BytesIO(stored))
                    records.append({'file': name, 'entry': entry, 'codec': codec, 'size': len(original), 'sha256': hashlib.sha256(original).hexdigest(), 'stored_sha256': hashlib.sha256(stored).hexdigest()})
        payload = root / 'payload'; payload.mkdir(exist_ok=True)
        archive_sha = digest(archive)
        parts = []
        with archive.open('rb') as f:
            i = 1
            while block := f.read(args.part_size):
                name = f'payload/vlog600-{archive_sha[:16]}-{args.part_size}.tar.xz.part{i:02d}'
                with tempfile.NamedTemporaryFile(dir=payload, prefix='.vlog-part-', suffix='.tmp', delete=False) as pending:
                    temporary = Path(pending.name)
                    pending.write(block); pending.flush(); os.fsync(pending.fileno())
                try:
                    if digest(temporary) != hashlib.sha256(block).hexdigest():
                        raise RuntimeError('VL bundle part write checksum mismatch')
                    os.replace(temporary,root/name)
                finally:
                    temporary.unlink(missing_ok=True)
                parts.append({'file': name, 'size': len(block), 'sha256': hashlib.sha256(block).hexdigest()}); i += 1
        manifest = {'version':1,'archive_format':'tar.xz','archive_size':archive.stat().st_size,'archive_sha256':archive_sha,'file_count':len(records),'asset_count':600,'production_file_count':800,'derived_preview_file_count':0 if args.exclude_previews else 700,'lut_encoding':'Exact original seven-decimal integers, second differences; no resampling or rounding','lut_count':100,'lut_dimension':33,'parts':parts,'files':records}
        with tempfile.NamedTemporaryFile(dir=root,prefix='.bundle-manifest-',suffix='.tmp',delete=False,mode='w',encoding='utf-8') as pending:
            temporary=Path(pending.name)
            pending.write(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');pending.flush();os.fsync(pending.fileno())
        try:
            os.replace(temporary,root/'bundle_manifest.json')
        finally:
            temporary.unlink(missing_ok=True)
        referenced={row['file'] for row in parts}
        for path in payload.glob('vlog600*.tar.xz.part*'):
            if path.relative_to(root).as_posix() not in referenced:path.unlink()
        print(json.dumps({'archive_size':manifest['archive_size'],'file_count':len(records),'parts':len(parts),'archive_sha256':manifest['archive_sha256'],'100_luts_byte_exact':True}))


if __name__ == '__main__':
    main()
