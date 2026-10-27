#!/usr/bin/env python3
"""Maintainer: package existing toolkit into independently extractable small ZIPs."""
import argparse
from collections import defaultdict
import hashlib
import io
import json
from pathlib import Path
import zipfile

def digest(data):return hashlib.sha256(data).hexdigest()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--max-mib',type=int,default=8)
    a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    adapter=Path(__file__).resolve().parent.parent
    groups=defaultdict(list)
    for path in sorted(a.source.rglob('*')):
        rel=path.relative_to(a.source)
        if (not path.is_file() or any(part.startswith('.') or part in ('__pycache__','node_modules') for part in rel.parts)
                or path.suffix=='.pyc'):
            continue
        if rel.parts[0] in ('scripts','references'):group='core'
        elif rel.parts[0]=='assets':
            category=rel.parts[1]
            group={'motion_presets':'presets','motion_array':'motion_array','fonts_creative_100':'fonts','svg_elements':'svg','character_bank_20':'characters','local_video':'core'}.get(category,'core')
            if category=='vlog_montage':
                sub=rel.parts[2]
                # Original lossless payload expands ALL 600 VL assets at install time.
                # Avoid shipping the same raw LUTs/WAVs a second time.
                if sub in ('luts','transitions','overlays','sfx','graphics_vlog','graphics_montage') or sub.startswith('.'):continue
                group='vlog_payload' if sub=='payload' else 'previews' if sub=='previews' else 'core'
        else:continue
        content=path.read_bytes()
        if rel.parts[0]=='scripts' and path.suffix=='.py':
            content=content.replace(b'import cairosvg',b'import gemini_svg as cairosvg')
        # Portable Gemini copy: source artwork/recipes retained, preview background softened.
        if rel.parts[0]=='assets' and rel.parts[1]=='motion_array' and path.suffix in ('.mjs','.json'):
            for dark in (b'#08131c',b'#071725',b'#0b1728',b'#07111d',b'#081521'):
                content=content.replace(dark,b'#F8F3E8')
        groups[group].append((rel.as_posix(),content))
    for path in sorted((adapter/'scripts').iterdir()):
        if not path.is_file() or path.suffix not in ('.py','.mjs','.cjs','.js'):continue
        if path.name=='build_gemini_packs.py':continue
        groups['core'].append(('scripts/'+path.name,path.read_bytes()))
    for path in sorted((adapter/'references').glob('selective-cache.md')):
        shared=True
        groups['core'].append(('references/'+('' if shared else 'gemini-')+path.name,path.read_bytes()))
    groups['core'].append(('SKILL.md',(adapter/'SKILL.md').read_bytes()))
    groups['core'].append(('agents/openai.yaml',(adapter/'agents/openai.yaml').read_bytes()))
    # Snapshot original instructions as reference; Gemini SKILL.md has precedence.
    groups['core'].append(('references/source-skill-context.md',(a.source/'SKILL.md').read_bytes()))
    # Adapter files intentionally override common source resources without duplicate ZIP members.
    for key,entries in groups.items():
        merged={name:data for name,data in entries}
        groups[key]=sorted(merged.items())
    limit=a.max_mib*1024*1024
    packs=[]
    for group,entries in sorted(groups.items(),key=lambda v:({'core':0,'presets':1}.get(v[0],2),v[0])):
        segments=[];current=[];size=22
        # Compress one file to estimate its exact ZIP contribution. Keep each ZIP independent.
        for name,data in entries:
            buf=io.BytesIO()
            with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:z.writestr(name,data)
            entry_size=len(buf.getvalue())-22
            if entry_size+22>limit:raise ValueError('Single file exceeds requested pack limit: '+name)
            if current and size+entry_size>limit:
                segments.append(current);current=[];size=22
            current.append((name,data));size+=entry_size
        if current:segments.append(current)
        for i,segment in enumerate(segments,1):
            key=group if len(segments)==1 else f'{group}_{i:02d}'
            name=f'Gemini_Motion_{key}.zip';out=a.output/name
            files=[]
            with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
                for rel,data in segment:
                    info=zipfile.ZipInfo(rel,date_time=(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                    z.writestr(info,data,compresslevel=9)
                    files.append({'path':rel,'size_bytes':len(data),'sha256':digest(data)})
            assert out.stat().st_size<=limit
            packs.append({'key':key,'category':group,'name':name,'size_bytes':out.stat().st_size,'sha256':digest(out.read_bytes()),'files':files})
    manifest={'schema':'gemini-motion-packs-v1','created':'2026-10-27','release':'atlas-locked-cache-first-2026-10-27','html_extension':{'source_included':(a.source/'assets/hyperframes/package-lock.json').is_file(),'runtime_binaries_included':False,'requires':'Provision Node>=22.12, npm dependencies, Chrome and optional ASR/rembg models for target OS/CPU during setup; run HTML preflight separately.'},'source_folder_url':'https://drive.google.com/drive/folders/1Vd09--QnSxFxNTPejHsEmcjYsU1UnY6j','download_folder_url':'https://drive.google.com/drive/folders/1QF3fxMu5ruysNbw92Jii5aU3xyb-tiJF','extract_rule':'Extract selected independent ZIPs into the same toolkit root; preserve paths. Check cache first; install only selected missing packs with gemini_cache.py. Atlas needs core + presets.','packs':packs}
    (a.output/'Gemini_Motion_Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps([{'key':v['key'],'files':len(v['files']),'bytes':v['size_bytes']} for v in packs],indent=2))

if __name__=='__main__':main()
