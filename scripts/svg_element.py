#!/usr/bin/env python3
"""Search or export original Motion Atlas SVG elements, preserving alpha."""
import argparse,json,shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent/'assets'/'svg_elements'

def index():
    rows=[]
    for path in sorted(ROOT.glob('svg_*_index.json')):
        data=json.loads(path.read_text(encoding='utf-8'))
        batch=data.get('items',[]) if isinstance(data,dict) else data
        for row in batch:
            row.setdefault('collection','icons' if path.name=='svg_icons_index.json' else 'motion' if path.name=='svg_motion_index.json' else 'explainer')
        rows.extend(batch)
    ids=[row['id'] for row in rows]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate SVG IDs in indices')
    return sorted(rows,key=lambda row:row['id'])

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--search',default='');ap.add_argument('--id');ap.add_argument('--output',type=Path)
    ap.add_argument('--collection',choices=['all','icons','motion','explainer','promotion'],default='all')
    ap.add_argument('--limit',type=int,default=20,help='Maximum search results; 0 returns all matches')
    ap.add_argument('--width',type=int,default=1024)
    args=ap.parse_args(); rows=index()
    if args.limit<0:ap.error('limit must be non-negative')
    if not args.id:
        q=args.search.casefold()
        matches=[r for r in rows if (args.collection=='all' or r['collection']==args.collection) and q in ' '.join([r['id'],r['title'],r['category'],*r.get('tags',[]),*r.get('use_cases',[])]).casefold()]
        print(json.dumps(matches[:args.limit] if args.limit else matches,ensure_ascii=False,indent=2));return
    row=next((r for r in rows if r['id']==args.id),None)
    if row is None:ap.error('Unknown SVG ID')
    source=ROOT/'files'/(row['id']+'.svg')
    if args.output is None:print(str(source));return
    out=args.output.resolve();out.parent.mkdir(parents=True,exist_ok=True)
    if out.suffix.lower()=='.svg':shutil.copyfile(source,out)
    elif out.suffix.lower()=='.png':
        if not 32<=args.width<=8192:ap.error('width must be 32..8192')
        try:import cairosvg
        except ImportError:ap.error('PNG export needs cairosvg; SVG copying has no extra dependency')
        cairosvg.svg2png(url=str(source),write_to=str(out),output_width=args.width)
    else:ap.error('output must end with .svg or .png')
    print(str(out))

if __name__=='__main__':main()
