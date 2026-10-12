#!/usr/bin/env python3
"""Find, copy and render original MA motion components or multi-layer scenes."""
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ASSETS=ROOT/'assets/motion_array'

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--search',default='');p.add_argument('--group',choices=['shapes','hud','transitions','particles']);p.add_argument('--id');p.add_argument('--copy',type=Path);p.add_argument('--output',type=Path);p.add_argument('--scene',type=Path);p.add_argument('--recipe',type=Path);p.add_argument('--width',type=int,default=1920);p.add_argument('--height',type=int,default=1080);p.add_argument('--fps',type=int,default=30);p.add_argument('--alpha',action='store_true');p.add_argument('--png-sequence',action='store_true')
 a=p.parse_args();rows=json.loads((ASSETS/'index.json').read_text())['items']
 if a.id:
  matches=[r for r in rows if r['id'].casefold()==a.id.casefold()]
  if len(matches)!=1:p.error('Unknown MA component ID')
  selected=matches[0]
  if a.copy:
   a.copy.parent.mkdir(parents=True,exist_ok=True);a.copy.write_text(json.dumps(selected,ensure_ascii=False,indent=2));print(a.copy.resolve())
 if a.output:
  if not (a.id or a.scene or a.recipe):p.error('Rendering requires --id, --recipe or --scene')
  cmd=['node',str(ASSETS/'render_motion.mjs'),'--output',str(a.output),'--width',str(a.width),'--height',str(a.height),'--fps',str(a.fps)]
  if a.scene:cmd+=['--scene',str(a.scene)]
  elif a.recipe:cmd+=['--recipe',str(a.recipe)]
  else:cmd+=['--id',selected['id']]
  if a.alpha:cmd+=['--alpha']
  if a.png_sequence:cmd+=['--png-sequence']
  subprocess.run(cmd,check=True)
 elif not a.copy:
  q=a.search.casefold()
  for r in rows:
   if a.id and r['id']!=selected['id']:continue
   if a.group and r['group']!=a.group:continue
   if q not in ' '.join([r['id'],r['title'],r['mechanism'],*r['tags']]).casefold():continue
   print(r['id']+'\t'+r['group']+'\t'+r['title']+'\t'+','.join(r['observation_ids']))
if __name__=='__main__':main()
