#!/usr/bin/env python3
"""Install ALL downloaded packs into the persistent Gemini skill directory offline."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from gemini_bootstrap import install, sha, safe_destination

def preflight(root):
    checks={}
    for module in ('PIL','numpy','cairosvg'):
        checks[module]=importlib.util.find_spec(module) is not None
    for exe in ('ffmpeg','ffprobe','node'):
        checks[exe]=bool(shutil.which(exe))
    checks['libx264']=False
    if checks['ffmpeg']:
        result=subprocess.run(['ffmpeg','-hide_banner','-encoders'],capture_output=True,text=True,check=True)
        checks['libx264']='libx264' in result.stdout
    checks['sharp']=False
    if checks['node']:
        probe="const s=require(process.argv[1]).rasterizer();if(!s.versions?.vips)process.exit(2)"
        checks['sharp']=subprocess.run(['node','-e',probe,str(root/'assets/character_bank_20/source/render_character.cjs')],cwd=root,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
    checks['core_render_ready']=all(checks[k] for k in ('PIL','numpy','ffmpeg','ffprobe','libx264'))
    checks['svg_renderer_ready']=checks['cairosvg'] or (checks['node'] and checks['sharp'])
    checks['all_components_ready']=all(checks[k] for k in ('core_render_ready','svg_renderer_ready','node','sharp'))
    return checks

def prepare_upgrade(root,data):
    """Back up only unchanged installed files whose distributed versions changed."""
    previous=root/'Gemini_Motion_Manifest.json'
    if not previous.is_file():raise ValueError('--upgrade requires the previous installed Gemini_Motion_Manifest.json; otherwise install into a new skill root')
    old=json.loads(previous.read_text())
    if old.get('schema')!='gemini-motion-packs-v1':raise ValueError('Invalid previous manifest')
    old_files={row['path']:row for pack in old['packs'] for row in pack['files']}
    changed=[]
    for pack in data['packs']:
        for row in pack['files']:
            target=safe_destination(root,row['path'])
            if not target.exists():continue
            if not target.is_file():raise ValueError('File destination is not a file: '+row['path'])
            current=sha(target)
            if current==row['sha256']:continue
            prior=old_files.get(row['path'])
            if prior is None or current!=prior['sha256']:
                raise ValueError('Edited/untracked file preserved; merge it in a project or install into a new root: '+row['path'])
            changed.append((row['path'],target))
    if not changed:return None
    base=safe_destination(root,'.gemini-backups');base.mkdir(exist_ok=True)
    backup=Path(tempfile.mkdtemp(prefix='upgrade-',dir=base))
    shutil.copy2(previous,backup/'Gemini_Motion_Manifest.json')
    for name,target in changed:
        destination=safe_destination(backup,name);destination.parent.mkdir(parents=True,exist_ok=True)
        os.replace(target,destination)
    return str(backup)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--manifest',required=True,type=Path)
    p.add_argument('--packs-dir',type=Path)
    p.add_argument('--skill-root',required=True,type=Path)
    p.add_argument('--verify-only',action='store_true')
    p.add_argument('--self-test',action='store_true')
    p.add_argument('--upgrade',action='store_true',help='Back up and replace only files matching the previous installed manifest; preserve user edits')
    a=p.parse_args();root=a.skill_root.resolve();root.mkdir(parents=True,exist_ok=True)
    if a.upgrade and a.verify_only:p.error('--upgrade cannot be combined with --verify-only')
    data=json.loads(a.manifest.read_text())
    if data.get('schema')!='gemini-motion-packs-v1':raise ValueError('Wrong manifest')
    files=0;backup=None
    if not a.verify_only:
        if not a.packs_dir:p.error('--packs-dir required for installation')
        # Validate availability of EVERY pack before installing any files.
        for pack in data['packs']:
            source=a.packs_dir/pack['name']
            if not source.is_file():raise FileNotFoundError('Download missing pack before offline install: '+pack['name'])
            if source.stat().st_size!=pack['size_bytes'] or sha(source)!=pack['sha256']:raise ValueError('Corrupt pack: '+pack['name'])
        if a.upgrade:backup=prepare_upgrade(root,data)
        for pack in data['packs']:files+=install(a.packs_dir/pack['name'],root,pack)
    for pack in data['packs']:
        for row in pack['files']:
            target=safe_destination(root,row['path'])
            if not target.is_file() or target.stat().st_size!=row['size_bytes'] or sha(target)!=row['sha256']:
                raise ValueError('Incomplete installation: '+row['path'])
    if not (root/'SKILL.md').is_file():
        raise ValueError('Place the Gemini SKILL.md in --skill-root before installing. Do not use the old ChatGPT SKILL.md.')
    # Expand every losslessly packed VL asset now; rendering must not lazy-download.
    subprocess.run([sys.executable,str(root/'scripts/prepare_vlog_assets.py'),'--verify'],check=True)
    # All 100 fonts are expanded during installation, with their original licenses.
    subprocess.run([sys.executable,str(root/'assets/fonts_creative_100/prepare_fonts.py'),'--all'],check=True,stdout=subprocess.DEVNULL)
    bank=root/'assets/character_bank_20/source'
    catalog=json.loads((bank/'motion_catalog.json').read_text())
    characters=json.loads((bank/'characters.json').read_text())
    views={'front','back','side_right','side_left','three_quarter_right','three_quarter_left'}
    if len(characters)!=20 or len(catalog['poses'])!=42 or len(catalog['motions'])!=34 or not all(views.issubset(c.get('supported_views',[])) for c in characters):
        raise ValueError('Character V3 source is incomplete: expected20characters/42poses/34motions/6views')
    checks=preflight(root);checks['character_v3_catalog']=True
    if a.self_test and checks['core_render_ready']:
        output=root/'validation/offline-smoke.mp4'
        subprocess.run([sys.executable,str(root/'scripts/gemini_atlas.py'),'--preset','B01','--duration','1','--fps','30','--width','640','--proof',str(root/'validation/paper-fold'),'--output',str(output)],check=True)
        subprocess.run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'],check=True)
        checks['offline_smoke_passed']=True
    if a.self_test and checks['all_components_ready']:
        motion=root/'validation/character-v3.mp4';camera=root/'validation/vector-camera.mp4'
        subprocess.run(['node',str(bank/'render_character.cjs'),'--character','P04','--motion','walk_side_left','--duration','1','--width','180','--height','300','--fps','24','--output',str(motion)],check=True,stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable,str(root/'scripts/vector_character_camera.py'),'--demo','--duration','1','--width','640','--height','360','--fps','24','--output',str(camera)],check=True,stdout=subprocess.DEVNULL)
        for video in (motion,camera):subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(video),'-f','null','-'],check=True)
        checks['character_v3_smoke_passed']=True;checks['vector_camera_smoke_passed']=True
    smoke=all(checks.get(k,False) for k in ('offline_smoke_passed','character_v3_smoke_passed','vector_camera_smoke_passed'))
    report={'schema':2,'assets_installed':True,'all_packs':len(data['packs']),'files_verified':sum(len(v['files']) for v in data['packs']),'fonts_materialized':100,'network_used_by_installer':False,'skill_root':str(root),'upgrade_backup':backup,'character_bank':{'version':3,'characters':20,'poses':42,'motion_recipes':34,'views':6},'checks':checks,'ready':checks['all_components_ready'] and (not a.self_test or smoke)}
    (root/'gemini-offline-status.json').write_text(json.dumps(report,indent=2)+'\n')
    destination=root/'Gemini_Motion_Manifest.json'
    if a.manifest.resolve()!=destination.resolve():shutil.copy2(a.manifest,destination)
    print(json.dumps(report,indent=2))
    if not checks['all_components_ready']:
        print('Assets are local. Missing runtime tools must be provisioned in the setup environment before claiming every component works offline.',file=sys.stderr)
        sys.exit(2)

if __name__=='__main__':main()
