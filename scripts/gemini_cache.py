#!/usr/bin/env python3
"""Offline cache inspection and selective verified pack installation. No network."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import os
import stat
import tempfile
import zipfile

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''): h.update(b)
    return h.hexdigest()

def safe(root, name):
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or '\\' in name or not p.parts:
        raise ValueError('Unsafe archive path: '+name)
    out=root.joinpath(*p.parts)
    if not out.resolve().is_relative_to(root.resolve()): raise ValueError('Escaping symlink: '+name)
    return out

def valid(root, entry):
    p=safe(root,entry['path'])
    return p.is_file() and p.stat().st_size==entry['size_bytes'] and sha(p)==entry['sha256']

def selected(manifest, requested):
    packs=manifest['packs']
    if not requested: raise ValueError('Select required pack keys/categories explicitly')
    unknown=set(requested)-{'all'}-{p['key'] for p in packs}-{p['category'] for p in packs}
    if unknown: raise ValueError('Unknown packs: '+','.join(sorted(unknown)))
    return [p for p in packs if 'all' in requested or p['key'] in requested or p['category'] in requested]

def plan(manifest, requested, roots, staging):
    rows=[]
    for p in selected(manifest,requested):
        hit=next((r for r in roots if all(valid(r,e) for e in p['files'])),None)
        z=next((d/p['name'] for d in staging if (d/p['name']).is_file()
                and (d/p['name']).stat().st_size==p['size_bytes'] and sha(d/p['name'])==p['sha256']),None)
        rows.append({'key':p['key'],'status':'ready' if hit else 'install-local' if z else 'download-required',
                     'root':str(hit) if hit else None,'archive':str(z) if z else None,
                     'name':p['name'],'drive_url':p.get('drive_url'),'sha256':p['sha256']})
    return rows

def install(manifest, requested, root, roots, staging):
    root.mkdir(parents=True,exist_ok=True)
    receipt=root/'.gemini-cache-receipt.json'
    old=json.loads(receipt.read_text()) if receipt.is_file() else {'files':{}}
    known=old.get('files',{})
    plans=plan(manifest,requested,roots,staging)
    missing=[p['name'] for p in plans if p['status']=='download-required']
    if missing: raise ValueError('Download only missing packs before install: '+', '.join(missing))
    writes=[]
    # Prevalidate every selected payload and collision before changing any installed file.
    for p,decision in zip(selected(manifest,requested),plans):
        if decision['root']==str(root) and decision['status']=='ready': continue
        archive=zipfile.ZipFile(decision['archive']) if decision['status']!='ready' else None
        try:
            if archive:
                names=[i.filename for i in archive.infolist() if not i.is_dir()]
                if len(names)!=len(set(names)) or set(names)!={e['path'] for e in p['files']}:
                    raise ValueError('Archive membership mismatch: '+p['name'])
                for i in archive.infolist():
                    safe(root,i.filename)
                    if stat.S_ISLNK(i.external_attr>>16): raise ValueError('Archive symlink rejected')
            for e in p['files']:
                target=safe(root,e['path'])
                if valid(root,e): continue
                if target.exists() and (not target.is_file() or sha(target)!=known.get(e['path'])):
                    raise ValueError('Preserve modified/unmanaged file; select a fresh versioned root: '+e['path'])
                data=archive.read(e['path']) if archive else safe(Path(decision['root']),e['path']).read_bytes()
                if len(data)!=e['size_bytes'] or hashlib.sha256(data).hexdigest()!=e['sha256']:
                    raise ValueError('Payload checksum mismatch: '+e['path'])
                writes.append((target,data))
        finally:
            if archive: archive.close()
    for target,data in writes:
        target.parent.mkdir(parents=True,exist_ok=True)
        fd,name=tempfile.mkstemp(prefix='.cache-',dir=target.parent)
        try:
            with os.fdopen(fd,'wb') as f:f.write(data)
            os.replace(name,target)
        finally:
            if os.path.exists(name): os.unlink(name)
    for p in selected(manifest,requested):
        for e in p['files']:
            if not valid(root,e): raise ValueError('Installed file failed verification')
            known[e['path']]=e['sha256']
    receipt.write_text(json.dumps({'files':known,'release':manifest.get('release')},indent=2)+'\n')
    return {'ready_for_selected_packs':True,'installed_files':len(writes),'root':str(root),
            'packs':[p['key'] for p in selected(manifest,requested)],'runtime_preflight_required':True}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['plan','install','verify'])
    p.add_argument('--manifest',required=True,type=Path)
    p.add_argument('--need',required=True,nargs='+')
    p.add_argument('--root',required=True,type=Path)
    p.add_argument('--cache-root',action='append',default=[],type=Path)
    p.add_argument('--packs-dir',action='append',default=[],type=Path)
    a=p.parse_args();m=json.loads(a.manifest.read_text())
    roots=list(dict.fromkeys(p.resolve() for p in [a.root,*a.cache_root]))
    staging=[p.resolve() for p in a.packs_dir]
    if a.action=='install':result=install(m,a.need,roots[0],roots,staging)
    else:
        rows=plan(m,a.need,roots if a.action=='plan' else roots[:1],staging)
        result={'packs':rows,'ready_for_selected_packs':all(r['status']=='ready' for r in rows)}
    print(json.dumps(result,indent=2))
    if a.action=='verify' and not result['ready_for_selected_packs']:raise SystemExit(1)

if __name__=='__main__':main()
