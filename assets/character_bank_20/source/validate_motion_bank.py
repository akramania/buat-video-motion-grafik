#!/usr/bin/env python3
"""Check generated character assets and fully decode every motion preview."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json, subprocess, xml.etree.ElementTree as ET
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent

def run():
 cs=json.loads((ROOT/'source/characters.json').read_text()); cat=json.loads((ROOT/'source/motion_catalog.json').read_text())
 assert len(cs)==20 and len(cat['poses'])==42 and len(cat['motions'])==34
 assert sum(c['sex']=='male' for c in cs)==10 and sum(c['sex']=='female' for c in cs)==10
 assert sum(c['sex']=='female' and c['head']['hijab']!='none' for c in cs)==6
 posecount=0; clip_paths=[]; edge=[]
 for c in cs:
  for p in cat['poses']:
   path=ROOT/'poses'/c['id']/(p['id']+'.svg'); tree=ET.parse(path); assert tree.getroot().tag.endswith('svg')
   ids=[e.get('id') for e in tree.iter() if e.get('id')]; assert len(ids)==len(set(ids)),str(path)
   assert 'NaN' not in path.read_text() and 'Infinity' not in path.read_text()
   png=path.with_suffix('.png');im=Image.open(png);im.load();assert im.mode=='RGBA',str(png)
   bbox=im.getchannel('A').getbbox();assert bbox,str(png)
   if bbox[0]<=1 or bbox[1]<=1 or bbox[2]>=im.width-1 or bbox[3]>=im.height-1:edge.append(str(png.relative_to(ROOT)))
   posecount+=1
  for m in cat['motions']:
   meta=json.loads((ROOT/'motions'/c['id']/(m['id']+'.json')).read_text()); assert meta
   clip_paths.append(ROOT/'clips'/c['id']/(m['id']+'.mp4'))
 def check(p):
  assert p.stat().st_size>1000,str(p)
  data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
  s=[s for s in data['streams'] if s['codec_type']=='video'][0]
  assert s['codec_name']=='h264' and s['pix_fmt']=='yuv420p',str(p)
  assert s['width']%2==0 and s['height']%2==0
  assert float(data['format']['duration'])>0
  subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],check=True,capture_output=True)
  return {'path':str(p.relative_to(ROOT)),'width':s['width'],'height':s['height'],'fps':s['avg_frame_rate'],'frames':s.get('nb_frames'),'duration':data['format']['duration']}
 with ThreadPoolExecutor(max_workers=4)as pool:clips=list(pool.map(check,clip_paths))
 report={'status':'passed' if not edge else 'edge_review_required','characters':20,'poses':posecount,'clips_fully_decoded':len(clips),'png_near_edges':edge,'clip_checks':clips,'scope':'File/XML/alpha/framing-edge checks and full MP4 decoding; visual pose/prop checks performed separately. Not a motion-capture realism metric.'}
 out=ROOT/'output'/'QA_Pose_Gerakan_20.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='clip_checks'}))
 if edge:raise SystemExit(2)
if __name__=='__main__':run()
