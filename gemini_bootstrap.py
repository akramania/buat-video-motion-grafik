#!/usr/bin/env python3
"""Download selected verified Drive packs, or use already downloaded ZIPs offline."""
import argparse
import hashlib
import http.cookiejar
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import urllib.parse
import urllib.request
import zipfile

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for data in iter(lambda:f.read(1024*1024),b''):h.update(data)
    return h.hexdigest()

def fetch(url, dest):
    parsed=urllib.parse.urlparse(url)
    if parsed.scheme!='https':raise ValueError('Download requires HTTPS')
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    req=urllib.request.Request(url,headers={'User-Agent':'Gemini-Atlas-Toolkit/1.0'})
    with opener.open(req,timeout=60) as response:
        first=response.read(4096)
        content_type=response.headers.get('Content-Type','')
        if 'text/html' in content_type or first.lstrip().lower().startswith((b'<!doctype html',b'<html')):
            raise RuntimeError('Drive returned a login/HTML page. Use the authorized Drive connector/browser to download the named file, then rerun with --local-dir. Do not save this page as ZIP.')
        with dest.open('wb') as f:
            f.write(first);shutil.copyfileobj(response,f)

def safe_destination(root,name):
    p=PurePosixPath(name)
    if not name or p.is_absolute() or '\\' in name or '\0' in name or any(v in ('','..','.') for v in name.split('/')):
        raise ValueError('Unsafe archive path')
    dest=root.joinpath(*p.parts)
    current=root
    for part in p.parts:
        current=current/part
        if current.is_symlink():raise ValueError('Symlink destination rejected')
    if not dest.resolve().is_relative_to(root.resolve()):raise ValueError('Path escapes toolkit')
    return dest

def install(zip_path,root,pack):
    if Path(zip_path).stat().st_size!=pack['size_bytes'] or sha(zip_path)!=pack['sha256']:
        raise ValueError('Pack size/checksum mismatch: '+pack['name'])
    expected={v['path']:v for v in pack['files']}
    with zipfile.ZipFile(zip_path) as z:
        if len(z.infolist())!=len(expected):raise ValueError('Unexpected ZIP entries')
        staged=[];seen=set()
        with tempfile.TemporaryDirectory(prefix='.gemini-unpack-',dir=root) as td:
            for info in z.infolist():
                row=expected.get(info.filename)
                if row is None or info.filename in seen or info.is_dir() or (info.external_attr>>16)&0o170000==0o120000:
                    raise ValueError('Unexpected/unsafe ZIP member')
                if info.file_size!=row['size_bytes']:raise ValueError('Member size mismatch')
                dest=safe_destination(root,info.filename)
                temp=safe_destination(Path(td),info.filename);temp.parent.mkdir(parents=True,exist_ok=True)
                with z.open(info) as src,temp.open('wb') as out:shutil.copyfileobj(src,out)
                if sha(temp)!=row['sha256']:raise ValueError('Member checksum mismatch')
                if dest.exists() and (not dest.is_file() or sha(dest)!=row['sha256']):
                    raise ValueError('Existing edited file preserved; use a new toolkit root: '+str(dest))
                staged.append((temp,dest));seen.add(info.filename)
            for temp,dest in staged:
                dest.parent.mkdir(parents=True,exist_ok=True)
                if not dest.exists():os.replace(temp,dest)
    return len(seen)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',required=True,help='Local JSON or HTTPS manifest URL')
    p.add_argument('--manifest-sha256')
    p.add_argument('--root',type=Path,default=Path('gemini_motion_toolkit'))
    p.add_argument('--packs',nargs='+',default=['all'])
    p.add_argument('--local-dir',type=Path,help='Directory of connector/browser-downloaded packs; network is skipped')
    p.add_argument('--list',action='store_true')
    a=p.parse_args();a.root.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='gemini-bootstrap-') as td:
        manifest=Path(a.manifest)
        if a.manifest.startswith('https://'):
            manifest=Path(td)/'manifest.json';fetch(a.manifest,manifest)
        if a.manifest_sha256 and sha(manifest)!=a.manifest_sha256:raise ValueError('Manifest checksum mismatch')
        data=json.loads(manifest.read_text())
        if data.get('schema')!='gemini-motion-packs-v1':raise ValueError('Unsupported manifest')
        packs=data['packs']
        if a.list:
            print(json.dumps([{'key':v['key'],'name':v['name'],'size_bytes':v['size_bytes'],'url':v['view_url']} for v in packs],indent=2));return
        requested=set(a.packs)
        if 'all' not in requested and requested-set(v['key'] for v in packs):raise ValueError('Unknown pack key')
        selected=[v for v in packs if 'all' in requested or v['key'] in requested]
        for pack in selected:
            name=pack['name']
            if Path(name).name!=name:raise ValueError('Unsafe pack name')
            source=a.local_dir/name if a.local_dir else Path(td)/name
            if not a.local_dir:fetch(pack['download_url'],source)
            count=install(source,a.root,pack)
            print(json.dumps({'pack':pack['key'],'files_verified':count,'root':str(a.root.resolve())}))

if __name__=='__main__':main()
