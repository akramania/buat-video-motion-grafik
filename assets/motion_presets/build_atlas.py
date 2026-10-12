#!/usr/bin/env python3
"""Build catalogue, previews, configs and optional self-contained HTML.

--skip-render reuses existing video/poster files and renders missing assets.
Preset default durations are respected: legacy samples are 5s; persistent
scenes retain their longer dwell instead of being squeezed into five seconds.
"""
import argparse,base64,concurrent.futures,json,shutil,subprocess
from pathlib import Path
from render import registry,configuration,render_video,frame
HERE=Path(__file__).resolve().parent
METADATA={'name','description','genres','family','source_url','source_product','observed_timestamp','mechanism','variant_basis','render_mode','time_mode','min_duration','cue_defaults','supported_end_behaviors','adaptation_status','category','assets','use','demo_kind','limitations','components','observation_basis','asset_types','use_cases','parameters'}


def exported_config(pid,metadata):
    """Keep all render controls, including mechanism-specific parameters."""
    cfg={k:v for k,v in metadata.items() if k not in METADATA and not k.startswith('_')}
    cfg.update(preset=pid,duration=metadata.get('duration',5),fps=60,width=1280)
    if metadata.get('time_mode')=='seconds':
        cfg.setdefault('tempo',1)
        cfg.setdefault('cues',dict(metadata.get('cue_defaults',{})))
    return cfg


def catalogue_html(template,rows):
    # A user-supplied title containing </script> must remain data in HTML.
    encoded=json.dumps(rows,ensure_ascii=False).replace('</','<\\/').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    return template.replace('__DATA__',encoded)


def one(args):
    pid,out,reuse=args; out=Path(out); cfg=configuration(pid)
    duration=cfg['duration']; video=out/'previews'/f'{pid}.mp4'; poster=out/'posters'/f'{pid}.jpg'
    if not (reuse and video.exists() and video.stat().st_size):
        render_video(pid,cfg,video,duration=duration)
    if not (reuse and poster.exists() and poster.stat().st_size):
        frame(pid,duration*.52,cfg).save(poster,quality=92)
    return pid


def build(out,skip_render=False,jobs=4,standalone=False,reel=False):
    out=Path(out).resolve(); presets,_=registry()
    for d in ['previews','posters','configs']: (out/d).mkdir(parents=True,exist_ok=True)
    pending=[]
    for pid in presets:
        complete=all((out/d/f'{pid}.{ext}').is_file() and (out/d/f'{pid}.{ext}').stat().st_size for d,ext in [('previews','mp4'),('posters','jpg')])
        if skip_render and complete: print('Reused '+pid,flush=True)
        else: pending.append((pid,str(out),skip_render))
    if pending:
        with concurrent.futures.ProcessPoolExecutor(max_workers=jobs) as ex:
            for pid in ex.map(one,pending): print('Rendered '+pid,flush=True)
    rows=[]
    for pid,m in presets.items():
        cfg=exported_config(pid,m)
        (out/'configs'/f'{pid}.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf-8')
        rows.append(dict(m,id=pid,duration=m.get('duration',5),video=f'previews/{pid}.mp4',poster=f'posters/{pid}.jpg'))
    (out/'presets.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
    template=(HERE/'catalogue_template.html').read_text(encoding='utf-8')
    (out/'index.html').write_text(catalogue_html(template,rows),encoding='utf-8')
    dest=out/'renderer'
    if dest!=HERE: shutil.copytree(HERE,dest,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    if standalone:
        embed=[]
        for row in rows:
            r=dict(row)
            for field,mime in [('video','video/mp4'),('poster','image/jpeg')]:
                r[field]='data:'+mime+';base64,'+base64.b64encode((out/row[field]).read_bytes()).decode('ascii')
            embed.append(r)
        path=out.parent/(out.name+'.html'); path.write_text(catalogue_html(template,embed),encoding='utf-8'); print(path)
    if reel:
        listing=out/'reel-list.txt'; listing.write_text(''.join("file 'previews/"+pid+".mp4'\n" for pid in presets))
        try: subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-movflags','+faststart',str(out.parent/'Motion-Preset-Reel.mp4')],check=True)
        finally: listing.unlink(missing_ok=True)
    print(out/'index.html')


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True); ap.add_argument('--jobs',type=int,default=4)
    ap.add_argument('--skip-render',action='store_true',help='Reuse existing previews/posters, render missing files only')
    ap.add_argument('--standalone',action='store_true'); ap.add_argument('--reel',action='store_true'); a=ap.parse_args()
    if not 1<=a.jobs<=16: ap.error('--jobs must be 1..16')
    build(a.output,a.skip_render,a.jobs,a.standalone,a.reel)
