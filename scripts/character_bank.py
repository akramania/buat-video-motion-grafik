#!/usr/bin/env python3
"""Discover and use the bundled 20-character bank without absolute host paths."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys

BANK = Path(__file__).resolve().parents[1] / 'assets' / 'character_bank_20'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    ls = sub.add_parser('list', help='List characters, poses or motions as JSON')
    ls.add_argument('--kind', choices=['characters', 'poses', 'motions'], default='characters')
    ls.add_argument('--sex', choices=['male', 'female'])
    ls.add_argument('--age-group', choices=['kanak-kanak', 'remaja', 'dewasa', 'warga emas'])
    ls.add_argument('--hijab', choices=['yes', 'no'])
    render = sub.add_parser('render', help='Pass remaining options to the character renderer')
    render.add_argument('options', nargs=argparse.REMAINDER)
    cp = sub.add_parser('copy', help='Copy an existing generated asset into a project')
    cp.add_argument('--character', required=True)
    cp.add_argument('--kind', choices=['pose', 'motion'], required=True)
    cp.add_argument('--id', required=True)
    cp.add_argument('--format', choices=['svg', 'png', 'mp4', 'json'])
    cp.add_argument('--output', required=True, type=Path)
    args, unknown = parser.parse_known_args()
    if unknown and args.command != 'render':
        parser.error('unrecognized options: ' + ' '.join(unknown))
    roster = json.loads((BANK / 'source' / 'characters.json').read_text())
    if args.command == 'list':
        if args.kind == 'characters':
            values = [c for c in roster if (not args.sex or c['sex'] == args.sex)
                      and (not args.age_group or c['age_group'] == args.age_group)
                      and (not args.hijab or (c['sex'] == 'female' and
                          (c['head']['hijab'] != 'none') == (args.hijab == 'yes')))]
        else:
            registry = json.loads((BANK / 'source' / 'motion_catalog.json').read_text())
            values = registry[args.kind]
        print(json.dumps(values, ensure_ascii=False, indent=2))
    elif args.command == 'render':
        node = shutil.which('node')
        if not node:
            parser.error('Node.js is needed; MP4 also requires sharp and FFmpeg')
        # Retain original argument order; argparse.REMAINDER can reorder unknown flags.
        options = sys.argv[sys.argv.index('render') + 1:]
        if options[:1] == ['--']:
            options = options[1:]
        subprocess.run([node, str(BANK / 'source' / 'render_character.cjs'), *options], check=True)
    else:
        if args.character not in {c['id'] for c in roster}:
            parser.error('Unknown character ID')
        if not args.id or any(ch not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-' for ch in args.id):
            parser.error('Invalid asset ID')
        ext = args.format or ('svg' if args.kind == 'pose' else 'mp4')
        if args.kind == 'pose' and ext not in ('svg', 'png'):
            parser.error('Pose assets support svg/png')
        if args.kind == 'motion' and ext not in ('mp4', 'json'):
            parser.error('Motion assets support mp4/json')
        folder = 'poses' if args.kind == 'pose' else ('clips' if ext == 'mp4' else 'motions')
        source = BANK / folder / args.character / (args.id + '.' + ext)
        if args.output.resolve() == source.resolve():
            parser.error('Choose a project output path outside the source asset')
        if not source.is_file():
            if ext == 'json':
                parser.error('Materialize the full bank package for precomputed JSON recipes; see references/character-bank-20.md')
            node = shutil.which('node')
            if not node:
                parser.error('This asset is not cached. Use Node.js to render it, or materialize the full bank package.')
            if args.output.suffix.lower() != '.' + ext:
                parser.error('Output filename must end in .' + ext)
            subprocess.run([node, str(BANK / 'source' / 'render_character.cjs'),
                            '--character', args.character,
                            '--pose' if args.kind == 'pose' else '--motion', args.id,
                            '--output', str(args.output)], check=True)
            return
        args.output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, args.output)
        print(args.output.resolve())


if __name__ == '__main__':
    main()
