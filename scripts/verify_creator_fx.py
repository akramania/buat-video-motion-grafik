#!/usr/bin/env python3
"""Verify CFX previews against their renderer, deterministic seek and full decode."""
import argparse, concurrent.futures, hashlib, json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

SKILL=Path(__file__).resolve().parents[1]
RENDERER=SKILL/'assets/motion_presets'
if not RENDERER.is_dir():RENDERER=SKILL/'renderer'
sys.path.insert(0,str(RENDERER))
import render

def verify(pid,media):
 cfg=render.configuration(pid);path=media/(pid+'.mp4')
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames:format=duration','-of','json',str(path)]))
 s=info['streams'][0]
 assert (s['width'],s['height'],s['r_frame_rate'])==(960,540,'30/1'),pid
 assert int(s['nb_frames'])==180 and abs(float(info['format']['duration'])-6)<.04,pid
 result=subprocess.run(['ffmpeg','-v','error','-threads','1','-i',str(path),'-f','null','-'],capture_output=True,check=True)
 assert not result.stderr,(pid,result.stderr.decode())
 times=[.4,1.3,2.9,4.6];hashes={}
 for t in times:hashes[t]=hashlib.sha256(render.frame(pid,t,cfg,False).tobytes()).hexdigest()
 for t in reversed(times):assert hashes[t]==hashlib.sha256(render.frame(pid,t,cfg,False).tobytes()).hexdigest(),(pid,'seek mismatch')
 assert len(set(hashes.values()))>1,(pid,'no visual change across samples')
 raw=subprocess.check_output(['ffmpeg','-v','error','-threads','1','-ss','3','-i',str(path),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'])
 actual=np.frombuffer(raw,dtype=np.uint8).reshape(540,960,3).astype(np.int16)
 expected=np.asarray(render.frame(pid,3,cfg,False).resize((960,540),Image.Resampling.LANCZOS)).astype(np.int16)
 error=float(np.abs(actual-expected).mean());assert error<5,(pid,'stale render',error)
 with Image.open(path.with_suffix('.webp')) as poster:assert poster.size==(640,360)
 return dict(id=pid,decode='pass',deterministic_seek='pass',frames=180,duration=6,mean_frame_error=round(error,3),sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--media',type=Path,required=True);ap.add_argument('--report',type=Path,required=True);ap.add_argument('--jobs',type=int,default=4);a=ap.parse_args()
 ids=sorted(pid for pid in render.registry()[0] if pid.startswith('CFX'))
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:rows=list(ex.map(lambda p:verify(p,a.media),ids))
 report=dict(count=len(ids),all_decoded=True,all_seek_deterministic=True,encoded_frames_match_renderer=True,visual_review='separate editorial pass required',audio='silent by design',items=rows)
 a.report.parent.mkdir(parents=True,exist_ok=True);a.report.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='items'}))
if __name__=='__main__':main()
