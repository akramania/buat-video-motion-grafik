#!/usr/bin/env python3
"""Safely materialize original full font binaries from a bundled lossless archive."""
from __future__ import annotations
import argparse, hashlib, json, os, re, tarfile, tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def _sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def _catalogue():
 xs=json.loads((ROOT/'font_index.json').read_text())
 assert len(xs)==100 and len({x['id'] for x in xs})==100,'Invalid font catalogue'
 return xs

def _inside(path):
 p=(ROOT/path).resolve()
 if not p.is_relative_to(ROOT.resolve()):raise ValueError('Font path escapes bundle directory')
 return p

def _choose(query):
 xs=_catalogue();q=query.casefold()
 found=[x for x in xs if x['id'].casefold()==q or x['family'].casefold()==q or x['slug'].casefold()==q]
 if len(found)!=1:raise ValueError(f'Unknown or ambiguous font: {query}')
 return found[0]

def _atomic_bytes(dest,data,expected_sha):
 if hashlib.sha256(data).hexdigest()!=expected_sha:raise ValueError('Extracted font or license checksum mismatch')
 dest=_inside(str(dest.relative_to(ROOT)))
 dest.parent.mkdir(parents=True,exist_ok=True)
 if not dest.parent.resolve().is_relative_to(ROOT.resolve()):raise ValueError('Unsafe cache directory')
 fd,tmp=tempfile.mkstemp(prefix='.font-',suffix='.tmp',dir=dest.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(data)
  os.replace(tmp,dest)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)

def _prepare_records(records):
 manifest=json.loads((ROOT/'bundle_manifest.json').read_text())
 archive=_inside(manifest['archive'])
 if archive.stat().st_size!=manifest['bytes'] or _sha(archive)!=manifest['sha256']:raise ValueError('Font bundle archive checksum mismatch')
 needs={}
 for r in records:
  for member,key,hashkey in [(r['archive_member'],'file','sha256'),(r['license_archive_member'],'license_file','license_sha256')]:
   if member.startswith('/') or '..' in Path(member).parts:raise ValueError('Unsafe archive member in catalogue')
   output=_inside(r[key])
   if not output.is_file() or _sha(output)!=r[hashkey]:needs[member]=(output,r[hashkey])
 if needs:
  # Stream only declared regular files; never call extractall or follow links.
  with tarfile.open(archive,'r|xz') as tar:
   for item in tar:
    if item.name not in needs:continue
    if not item.isfile() or item.issym() or item.islnk():raise ValueError('Unsafe archive font member')
    if item.size>3*1024*1024:raise ValueError('Font member exceeds expected size')
    stream=tar.extractfile(item)
    if stream is None:raise ValueError('Could not read archive font')
    data=stream.read();dest,expected=needs.pop(item.name)
    _atomic_bytes(dest,data,expected)
    if not needs:break
  if needs:raise ValueError('Declared font or license missing from archive')
 return [_inside(r['file']) for r in records]

def prepare_font(query):
 """Return path to a selected original TTF, with its original OFL next to it."""
 return _prepare_records([_choose(query)])[0]

def prepare_all():return _prepare_records(_catalogue())

if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('font',nargs='?',help='Font ID, canonical family, or slug')
 parser.add_argument('--all',action='store_true',help='Materialize all 100 original fonts')
 parser.add_argument('--list',action='store_true',help='List the 100 families')
 parser.add_argument('--search',default='',help='Case-insensitive family/script/category filter for --list')
 args=parser.parse_args()
 if args.list:
  for r in _catalogue():
   if args.search.casefold() in (r['id']+' '+r['family']+' '+r['script']+' '+r['category']).casefold():print(r['id']+'\t'+r['family']+'\t'+r['script']+'\t'+r['category'])
 elif args.all:
  for p in prepare_all():print(p)
 elif args.font:print(prepare_font(args.font))
 else:parser.error('Supply a font ID/family, --all or --list')
