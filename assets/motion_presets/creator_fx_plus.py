"""CFX21-CFX80. Original recipes from browser-sampled edited reference panels.

No source footage, third-party branding, matting model or tracker is bundled.
All frame state is seekable on the normalized 0..5 clock used by render.py.
"""
import math
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
from core import *
from creator_fx import cover, demo_person, room, footage_layer, subject_layer, zoom, draw_card, image_asset

REFS={
 'R01':('DeznKe6zYWd','0.24-7.66s','Three portrait video cards fan above a laptop; nested moving graphics.'),
 'R02':('DdtsGzhT2oP','~1.86-32.62s','AFTER/right only: text at different depths, building insert, fast spatial transitions.'),
 'R03':('DeHNxX-JEMZ','~5.87-20.01s','Four edited panels: UI, graph, text, inset media and changing focus.'),
 'R04':('DeRaKpNJ4ET','~3.02-13.00s','Edited panels: incoming-call UI, checklist, phone gauge, orange emphasis strips.'),
 'R05':('Db7qHm7B5Z6','~0.73-10.08s','Two edited examples: floating orbs, circular subject backdrop, perspective typography.'),
 'R06':('DdM89KRMPBJ','~3-23.77s','AFTER/right: note pinboard, dotted connector, glowing bulb, word emphasis.'),
 'R07':('DeXmN1Apj2c','~5.80-20.07s','AFTER/right: stock cluster, highlighted phrases, background placard and growth graphic.'),
 'R08':('DedfPaKPlnT','~2.75-49.43s','AFTER/right: price accent, food inserts, macro cutaways, reframing and captions.'),
 'R09':('DedavsYxYkh','~1.6-24.30s','AFTER/right: hero product macro, ingredient/media insert and comment CTA.'),
 'R13':('DePNgrmToh9','~1.8-9.5s','Finished collage examples: map, stamps, archival portrait, dated photo frames and tiled scenes.'),
 'R14':('DebyJVyTLOf','~1.6-35s','AFTER/right only: cream editorial sheets, palettes, layout grid, exploded layers, line stack.'),
}
# Each entry has a separate lead mechanism, not a palette/direction-only variant.
SPECS=[
 ('Triple Reel Fan','R01','three hinged portrait panels converge then fan'),
 ('Nested Screen Dock','R01','child panels dock into a parent monitor'),
 ('Card Flip Handoff','R01','two-sided planar flip with midpoint content handoff'),
 ('Split Panel Lift','R01','vertical slit masks reveal independently lifted panels'),
 ('Corner Halo Disc','R05','radial disc grows behind an alpha subject'),
 ('Parallax Orb Field','R05','seeded depth planes of orbs counter-pan behind subject'),
 ('Perspective Type Plane','R05','one text plane rotates through a projective quadrilateral'),
 ('Silhouette Halo Pulse','R05','dilated alpha contour rings expand behind subject'),
 ('Headline Occlusion Slide','R02','headline crosses from behind subject to a clear foreground hold'),
 ('Location Diorama Pop','R02','building layers rise at independent depths behind subject'),
 ('Whip Stretch Cut','R02','directional strip stretching hands off two scenes'),
 ('Roll-and-Land Caption','R02','word chips roll on circular paths and settle on a baseline'),
 ('Opposing Word Pair','R02','two phrase blocks converge on perpendicular masked tracks'),
 ('Floating Product Insert','R09','product cutout springs upward with an attached content tag'),
 ('Product Hero Cutaway','R09','macro product aperture replaces the presenter stage'),
 ('Ingredient Card Cascade','R09','ingredient cards stack by depth then spread around hero'),
 ('Price Tag Swing','R08','hinged tag swings with a damped pendulum'),
 ('Plate Tilt Showcase','R08','circular product composition tilts with orbiting detail pins'),
 ('Macro Crop Match Cut','R08','registered circular crop carries focus across a content cut'),
 ('Speed Ramp Push','R08','explicit nonlinear source-time remap drives a moving demo'),
 ('Quad Video Ensemble','R03','four independently animated panels share a stable grid'),
 ('Focus Rack Grid','R03','sharp focus transfers between four depth-separated panels'),
 ('Caption Depth Plane','R03','large caption plane passes behind a protected head region'),
 ('Glass Chat Stack','R03','messages reflow the existing stack when a new bubble arrives'),
 ('Live Chart Overlay','R03','chart path and moving data point build above footage'),
 ('Branch Card Flow','R03','one node branches into child cards as connectors reach them'),
 ('Incoming Call Panel','R04','call card enters, pulses, then changes to connected state'),
 ('Checklist Tap Reveal','R04','cursor visits checkboxes and reveals completed row states'),
 ('Gauge Sweep Phone','R04','needle and numeric readout share the same measured progress'),
 ('Highlight Strip Chase','R04','independent highlight bands chase successive phrase blocks'),
 ('Pinboard Notes Draw','R06','pinned notes arrive before drawn connecting paths'),
 ('Lightbulb Bloom','R06','bulb filament lights before a radial glow and ray burst'),
 ('Dotted Route Courier','R06','courier travels along a progressive dotted path'),
 ('Underline Word Sweep','R06','underline follows completed words while layout stays fixed'),
 ('Inventory Cluster Bloom','R07','items clone outward from one hero into a packed inventory'),
 ('Marker Box Emphasis','R07','hand-like marker rectangle draws around active wording'),
 ('Growth Curve Tracker','R07','point, label and reveal mask follow actual demo curve values'),
 ('Placard Tilt Replace','R07','a background placard turns around a hinge behind subject'),
 ('Blueprint Photo Collage','R13','photos assemble on a ruled blueprint with corner marks'),
 ('Archive Stamp Route','R13','date stamps land at route nodes with ink impressions'),
 ('Polaroid Deal','R13','photo cards slide from a deck with offset rotations'),
 ('Torn Portrait Aperture','R13','irregular radial paper aperture reveals a portrait'),
 ('Postcard Route Journey','R13','schematic paper route draws as an aircraft advances'),
 ('Date Card Flip','R13','top and bottom number flaps exchange at a hinge'),
 ('Archive Mosaic Zoom','R13','camera traverses a mosaic and resolves to one photo'),
 ('Museum Frame Parallax','R13','frame, artwork and foreground trim move at different depths'),
 ('Editorial Spec Sheet','R14','video header shrinks to make room for a design specification'),
 ('Palette Swatch Morph','R14','swatches change geometry and transfer their colors to a panel'),
 ('Typography Scale Ladder','R14','type specimen grows through measured size rungs'),
 ('Layout Grid Build','R14','grid lines draw before cells populate in reading order'),
 ('Exploded Layer Timeline','R14','flat layers separate in depth to reveal their order'),
 ('Timeline Track Assemble','R14','clips snap to time tracks while a playhead traverses them'),
 ('Paragraph Line Reveal','R14','line-specific masks reveal a paragraph without reflow'),
 ('Modular Panel Reflow','R14','panel rectangles interpolate between two layout topologies'),
 ('Flipbook Strip Cut','R14','image strips rotate independently to reveal the next panel'),
 ('B-roll Tile Pour','R08','small media tiles fall into fitted collage slots'),
 ('Continuous Caption Rail','R02','horizontal word rail moves beneath a stationary reading window'),
 ('Callout Magnifier Lens','R07','circular magnified crop follows a point with a leader label'),
 ('Isometric Window Fold','R14','three panels hinge into an isometric triptych'),
 ('Mosaic-to-Hero Resolve','R03','four tiles converge into one continuous hero image'),
]
assert len(SPECS)==60
PRESETS={}
for i,(name,ref,mechanism) in enumerate(SPECS,21):
 code,ts,finding=REFS[ref];pid=f'CFX{i:02d}'
 PRESETS[pid]=dict(name=name,description=mechanism[0].upper()+mechanism[1:]+'.',genre='education' if i>=59 and i<=75 else 'creator',
  family='creator-fx',category='creator-fx',text='IDEA DALAM GERAK',subtitle='Creator FX 80',duration=6,
  source_url='https://www.instagram.com/reel/'+code+'/',source_product='Instagram · '+ref+' · edited examples',source_ref=ref,
  observed_timestamp=ts,source_finding=finding,mechanism=mechanism,variant_basis='adapted',
  observation_basis='browser-sampled-edited-panel',adaptation_status='original-variant',
  limitations='Original demonstrator derived from observed principles; not an exact source template. Generic artwork/data. Real video needs prepared layers and verified cue/track inputs.',
  use_cases=['creator reel','explainer','editorial','product'],parameters=['image_path','image_paths','subject_path','background_path','items','values','text','subtitle','presentation'],
  items=['IDEA','KONTEKS','VISUAL','HASIL'],values=[18,37,55,78])

for code,fields in {'CFX37':['price'],'CFX63':['route_points'],'CFX64':['from_year','to_year'],'CFX73':['lines']}.items():
 PRESETS[code]['parameters']+=fields

def clock_remap(t):
 """CFX40 normalized source clock: slow hold, rapid travel, readable settle."""
 t=clamp(t,0,5)
 if t<1.5:return t*.28
 if t<2.8:return .42+(t-1.5)*2.65
 return min(5,3.865+(t-2.8)*.5159)

def validate_config(cfg):
 items=cfg.get('items',[])
 if not isinstance(items,list) or not items or not all(isinstance(x,str) and len(x)<=160 for x in items):raise ValueError('items must be a nonempty list of short text labels')
 if cfg.get('preset') in ('CFX45','CFX57'):
  values=cfg.get('values')
  if not isinstance(values,list) or not 2<=len(values)<=10 or not all(isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x) for x in values):raise ValueError('values must contain 2-10 finite numbers')
 if cfg.get('route_points') is not None:
  pts=cfg['route_points']
  if not isinstance(pts,list) or len(pts)<2 or not all(isinstance(z,(list,tuple)) and len(z)==2 and all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in z) for z in pts):raise ValueError('route_points must contain at least two finite (x,y) coordinates')
 return cfg

def data_points(values,left=240,right=1040,top=210,bottom=550):
 lo=min(0,min(values));hi=max(1,max(values));span=hi-lo
 return [(left+i*(right-left)/(len(values)-1),bottom-(v-lo)/span*(bottom-top)) for i,v in enumerate(values)],lo,hi

def asset(cfg,i=0):
 paths=cfg.get('image_paths') or ([cfg['image_path']] if cfg.get('image_path') else [])
 return image_asset(paths[i%len(paths)]) if paths else None

@lru_cache(maxsize=32)
def poster(i=0):
 im=layer(400,500);d=ImageDraw.Draw(im);colors=['#E6A26E','#8BBEC1','#B8A4D2','#D5C27B'];d.rectangle((0,0,400,500),fill=colors[i%4])
 for j in range(5):d.ellipse((40+j*24,70+j*25,340-j*20,390-j*5),outline='#F9EFE0',width=3)
 d.polygon([(20,480),(160,210),(250,380),(310,270),(400,480)],fill='#284951')
 text(im,['CERITA','FOKUS','IDEA','GERAK'][i%4],200,60,40,'#24394B');return im

def media(cfg,i=0):return asset(cfg,i) or poster(i)

def thumb(cfg,i,size=(240,310)):
 art=cover(media(cfg,i),size);mask=Image.new('L',size);ImageDraw.Draw(mask).rounded_rectangle((0,0,size[0]-1,size[1]-1),18,fill=255);art.putalpha(mask);return art

def icon(im,x,y,p,kind=0,s=1):
 if kind%4==0:
  rr(im,(x-44*s,y-60*s,x+44*s,y+60*s),p['accent'],14*s,p['text'],2);rr(im,(x-27*s,y-40*s,x+27*s,y+10*s),p['panel'],5)
 elif kind%4==1:
  circle(im,x,y,53*s,p['accent']);line(im,[(x-25*s,y),(x-3*s,y+22*s),(x+29*s,y-24*s)],p['bg'],8*s)
 elif kind%4==2:
  d=ImageDraw.Draw(im);d.polygon([(x,y-65*s),(x+58*s,y-25*s),(x+58*s,y+35*s),(x,y+70*s),(x-58*s,y+35*s),(x-58*s,y-25*s)],fill=p['secondary'],outline=p['text']);line(im,[(x-58*s,y-25*s),(x,y+10*s),(x+58*s,y-25*s)],p['text'],3);line(im,[(x,y+10*s),(x,y+70*s)],p['text'],3)
 else:
  rr(im,(x-65*s,y-42*s,x+65*s,y+42*s),p['panel'],17*s,p['accent'],3);circle(im,x-24*s,y,10*s,p['accent']);line(im,[(x-4*s,y-11*s),(x+43*s,y-11*s)],p['text'],4)

def person_at(im,person,x=640,y=460,scale=.82):paste(im,person,x,y,scale=scale)

def text_block(s,p,w=660,h=110,size=56):
 im=layer(w,h);rr(im,(0,0,w-1,h-1),p['panel'],22,p['accent'],2);text(im,s,w/2,h/2,fit_size(s,w-42,size),p['text']);return im

def caption(im,value,p,y=575,size=42):
 tile=text_img(value,fit_size(value,990,size),p['text']);rr(im,(640-tile.width/2-24,y-tile.height/2-16,640+tile.width/2+24,y+tile.height/2+16),rgba(p['panel'],245),17);paste(im,tile,640,y)

def card_at(im,cfg,i,x,y,w=240,h=300,angle=0,scale=1,opacity=1):paste(im,thumb(cfg,i,(w,h)),x,y,angle=angle,scale=scale,opacity=opacity)

def line_part(im,points,q,color,width=4):
 lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])];remaining=sum(lengths)*clamp(q);out=[points[0]]
 for a,b,distance in zip(points,points[1:],lengths):
  if remaining>=distance:out.append(b);remaining-=distance
  else:
   f=remaining/max(.001,distance);out.append((mix(a[0],b[0],f),mix(a[1],b[1],f)));break
 if q>0:line(im,out,color,width)
 return out[-1]

def path_heading(points,q):
 lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])];remaining=sum(lengths)*clamp(q);heading=0
 for a,b,distance in zip(points,points[1:],lengths):
  if distance>0:
   heading=math.atan2(b[1]-a[1],b[0]-a[0])
   if remaining<=distance:return heading
   remaining-=distance
 return heading

def schematic():
 im=layer();d=ImageDraw.Draw(im);d.rectangle((0,0,W,H),fill='#E8DFCC')
 for x in range(0,W,80):d.line((x,0,x,H),fill='#D3C9B6')
 for y in range(0,H,80):d.line((0,y,W,y),fill='#D3C9B6')
 d.polygon([(180,340),(310,180),(480,210),(500,375),(730,470),(1040,330),(1100,530),(700,600),(390,510)],fill='#C4C5AF',outline='#858F85')
 text(im,'LALUAN DEMO',1000,610,18,'#5D6D63','mono');return im

def compose(pid,t,cfg,footage=None,subject=None,backdrop=None):
 validate_config(dict(cfg,preset=pid))
 k=int(pid[3:]);p=palette(cfg);scene=base(cfg);q=smooth(prog(t,.45,3.5));e=enter(t,.1,.8);items=cfg.get('items',['IDEA','KONTEKS','VISUAL','HASIL']) or ['IDEA']
 src=footage_layer(t,cfg,footage,subject,backdrop);person=subject or (image_asset(cfg['subject_path']) if cfg.get('subject_path') else demo_person())
 if k==21:
  for i in (0,2,1):card_at(scene,cfg,i,640+(i-1)*250*e,385+abs(i-1)*45,w=250,h=350,angle=(i-1)*17*e,scale=.8+.2*e)
 elif k==22:
  rr(scene,(285,175,995,565),p['panel'],25,p['secondary'],4);paste(scene,cover(src,(660,335)),640,365)
  for i in range(3):
   a=enter(t,.2+i*.25,1.4+i*.25);card_at(scene,cfg,i,mix(220+420*i,470+170*i,a),mix(540,380,a),w=155,h=210,scale=1-.5*a)
  line(scene,[(640,565),(640,600),(530,600),(750,600)],p['secondary'],9)
 elif k==23:
  phase=prog(t,.3,3.8)*math.pi;ww=max(.015,abs(math.cos(phase)));card_at(scene,cfg,0 if phase<math.pi/2 else 1,640,380,w=380,h=420,scale=1)
  art=thumb(cfg,0 if phase<math.pi/2 else 1,(380,420)).resize((max(2,int(380*ww)),420));scene=base(cfg);paste(scene,art,640,380)
 elif k==24:
  for i in range(3):
   a=enter(t,.2+i*.32,1.2+i*.32);tile=thumb(cfg,i,(260,350));tile=crop_reveal(tile,a);paste(scene,tile,340+300*i,410-70*a)
 elif k==25:
  circle(scene,640,340,220*e,p['secondary']);circle(scene,640,340,185*e,p['accent']);person_at(scene,person)
 elif k==26:
  for i in range(16):
   depth=(i%4+1)/4;xx=(i*167+90*depth*math.sin(t))%1300;yy=170+(i*79)%400
   circle(scene,xx,yy,10+28*depth,rgba(p['secondary'],80+int(100*depth)))
  person_at(scene,person)
 elif k==27:
  plane=text_block(cfg['text'],p,850,170,82);tilt=math.sin(t*.8)*80
  scene.alpha_composite(warp_quad(plane,[(210,310-tilt),(1070,210+tilt),(1060,460+tilt),(220,520-tilt)]))
 elif k==28:
  a=person.resize((350,430));mask=a.getchannel('A')
  for radius in (31,21,11):
   outer=mask.filter(ImageFilter.MaxFilter(radius));ring=ImageChops.subtract(outer,mask);art=Image.new('RGBA',a.size,p['secondary']);art.putalpha(ring.point(lambda z:int(z*(.25+.2*math.sin(t*3+radius)))));paste(scene,art,640,410,scale=1+.03*math.sin(t*3))
  paste(scene,a,640,410)
 elif k==29:
  scene=cover(backdrop or room(True),(W,H));word=text_img(cfg['text'],fit_size(cfg['text'],1000,110),p['accent']);yy=mix(430,215,q)
  paste(scene,word,640,yy);person_at(scene,person);
  if t>3.2:paste(scene,word,640,215)
 elif k==30:
  for i in range(6):
   a=enter(t,.12+i*.14,.9+i*.14);x=220+i*145;h=120+((i*57)%170)
   rr(scene,(x,520-h*a,x+120,530),p['secondary'] if i%2 else p['panel'],9,p['accent'],2)
   for j in range(3):rr(scene,(x+20+j*30,540-h*a,x+35+j*30,555-h*a),p['accent'],2)
  person_at(scene,person,640,460,.77)
 elif k==31:
  edge=int(W*q);other=cover(media(cfg,1),(W,H));scene=src.copy();scene.paste(other.crop((0,0,edge,H)),(0,0))
  if 30<edge<W-30:
   strip=src.crop((int(clamp(edge,1,W-2)),0,int(clamp(edge,1,W-2))+1,H)).resize((180,H));paste(scene,strip,edge,360,opacity=.75)
 elif k==32:
  words=cfg['text'].split()[:5]
  for i,w in enumerate(words):
   a=enter(t,.1+i*.18,1.4+i*.18);theta=(1-a)*math.tau;tile=text_block(w,p,190,90,36);paste(scene,tile,250+195*i+45*math.sin(theta),390-85*(1-a)*math.cos(theta),angle=(1-a)*360)
 elif k==33:
  words=cfg['text'].split();left=' '.join(words[:max(1,len(words)//2)]);right=' '.join(words[max(1,len(words)//2):]) or 'GERAK'
  paste(scene,text_block(left,p,660,120),mix(-400,640,e),310);paste(scene,text_block(right,p,660,120),640,mix(900,465,enter(t,.5,1.4)))
 elif k==34:
  scene=src.copy();icon(scene,910,440-110*pop(prog(t,.3,1.4)),p,2,1.4);paste(scene,text_block(items[0],p,290,65,30),910,520)
 elif k==35:
  circle(scene,640,370,220*e,p['secondary']);icon(scene,640,350,p,2,2.4)
  for i in range(3):
   a=enter(t,.5+i*.22,1.4+i*.22);x=230+410*i;y=190 if i!=1 else 575;line(scene,[(640,350),(x,y)],rgba(p['accent'],255*a),3);text(scene,items[i%len(items)],x,y,28,p['text'],opacity=a)
 elif k==36:
  icon(scene,640,380,p,2,1.5)
  for i in range(4):
   a=enter(t,.3+i*.2,1.3+i*.2);ang=i*math.pi/2+.3;paste(scene,draw_card(items[i%len(items)],'',p,230,120),640+370*math.cos(ang)*a,380+160*math.sin(ang)*a,angle=(1-a)*25,opacity=a)
 elif k==37:
  line(scene,[(640,150),(640,250)],p['secondary'],4);theta=math.sin(t*5)*22*math.exp(-t*.9);tagim=text_block(cfg.get('price','RM 20 · DEMO'),p,430,220,48);paste(scene,tagim,640+80*math.sin(math.radians(theta)),385,angle=theta);circle(scene,640,160,10,p['accent'])
 elif k==38:
  plate=layer(420,420);circle(plate,210,210,205,'#F5E8D1',p['secondary'],7);paste(plate,cover(media(cfg,0),(290,290)),210,210)
  paste(scene,plate,640,380,angle=6*math.sin(t*.8))
  for i in range(3):
   a=t*.6+i*math.tau/3;circle(scene,640+250*math.cos(a),380+180*math.sin(a),14,p['accent'])
 elif k==39:
  art=cover(media(cfg,0 if t<2.5 else 1),(W,H));scene=base(cfg);r=190+55*math.sin(t*1.4);mask=Image.new('L',(W,H));ImageDraw.Draw(mask).ellipse((640-r,360-r,640+r,360+r),fill=255);art.putalpha(mask);scene.alpha_composite(art);circle(scene,640,360,r,None,p['accent'],5)
 elif k==40:
  tc=clock_remap(t);scene=footage_layer(tc,cfg,footage,subject,backdrop);x=190+180*tc;circle(scene,x,540,28,p['accent']);line(scene,[(190,580),(1090,580)],p['secondary'],3);text(scene,'SLOW  /  FAST  /  HOLD',640,185,28,p['text'])
 elif k in (41,42):
  active=int(t//1.05)%4
  for i in range(4):
   art=thumb(cfg,i,(390,205));
   if k==42 and i!=active:art=art.filter(ImageFilter.GaussianBlur(7))
   paste(scene,art,420+440*(i%2),270+245*(i//2),scale=1+.03*math.sin(t*1.4+i))
   rr(scene,(215+440*(i%2),160+245*(i//2),625+440*(i%2),380+245*(i//2)),None,20,p['accent'] if k==42 and i==active else p['secondary'],3)
 elif k==43:
  tile=text_img(cfg['text'],fit_size(cfg['text'],1100,130),p['secondary']);paste(scene,tile,640+160*math.sin(t),300);person_at(scene,person,640,470,.86);caption(scene,items[0],p)
 elif k==44:
  count=min(4,1+int(t/.8));shift=70*(count-1)
  for i in range(count):
   a=enter(t,i*.8,i*.8+.4);tile=text_block(items[i%len(items)],p,520,95,36);paste(scene,tile,640+(-1)**i*100,400+i*88-shift+50*(1-a),opacity=a)
 elif k==45:
  scene=src.copy()
  if footage is None and not cfg.get('image_path'):scene=cover(backdrop or room(),(W,H));person_at(scene,person,400)
  panelim=draw_card('DATA DEMO','',p,580,350);pts,lo,hi=data_points(cfg['values'],55,525,100,275);end=line_part(panelim,pts,q,p['accent'],7);paste(scene,panelim,900,400);circle(scene,900-290+end[0],400-175+end[1],10,p['text'])
 elif k==46:
  paste(scene,draw_card(items[0],'',p,230,120),290,365)
  for i in range(3):
   y=220+i*155;a=enter(t,.3+i*.25,1.5+i*.25);pts=[(410,365),(560,365),(560,y),(800,y)];line_part(scene,pts,a,p['secondary'],4);paste(scene,draw_card(items[(i+1)%len(items)],'',p,300,115),950,y,opacity=a)
 elif k==47:
  a=enter(t,.2,.8);connected=t>2.3;card=draw_card('CONNECTED' if connected else 'INCOMING CALL','',p,640,330);circle(card,320,125,47,p['secondary']);circle(card,235,260,28,'#DE7770');circle(card,405,260,28,p['accent']);paste(scene,card,640,380+100*(1-a),opacity=a)
  if not connected:circle(scene,640,340,50+15*math.sin(t*7),None,p['accent'],3)
 elif k==48:
  for i in range(4):
   yy=220+i*102;done=t>i*.75+.6;rr(scene,(300,yy-27,355,yy+28),p['accent'] if done else p['panel'],10,p['secondary'],2);text(scene,items[i%len(items)],400,yy,38,p['text'],anchor='left')
   if done:line(scene,[(310,yy),(322,yy+12),(345,yy-14)],p['bg'],5)
  cy=220+min(3,int(t/.75))*102;line(scene,[(345,cy+12),(365,cy+38),(353,cy+38),(350,cy+48)],p['text'],4)
 elif k==49:
  rr(scene,(425,140,855,620),p['panel'],38,p['secondary'],5);center=(640,380);d=ImageDraw.Draw(scene);d.arc((500,240,780,520),180,360,fill=p['secondary'],width=18);ang=math.pi+math.pi*q;line(scene,[(640,380),(640+130*math.cos(ang),380+130*math.sin(ang))],p['accent'],8);text(scene,str(round(q*100)),640,485,66,p['text']);text(scene,'DATA DEMO',640,555,20,p['muted'])
 elif k==50:
  for i in range(4):
   yy=220+i*105;active=min(3,int(t/.8))==i;ww=650*enter(t,i*.8,i*.8+.35)
   if active:rr(scene,(290,yy-34,290+ww,yy+34),p['accent'],8)
   text(scene,items[i%len(items)],640,yy,43,p['bg'] if active else p['text'])
 elif k==51:
  scene=schematic();coords=[(360,245),(900,235),(600,480)]
  for i,(x,y) in enumerate(coords):
   a=enter(t,.1+i*.3,.8+i*.3);paste(scene,draw_card(items[i%len(items)],'',p,280,170),x,y,opacity=a,angle=(-1)**i*5);circle(scene,x,y-75,10,'#BD715C')
  line_part(scene,[(360,260),(470,315),(600,480),(760,330),(900,250)],enter(t,1.1,3),p['accent'],5)
 elif k==52:
  glow=layer();circle(glow,640,330,145,p['accent']);glow=glow.filter(ImageFilter.GaussianBlur(65));paste(scene,glow,640,360,opacity=.2+.5*enter(t,.7,1.4));circle(scene,640,320,95,'#EAD273',p['text'],4);rr(scene,(600,395,680,455),p['secondary'],10);line(scene,[(610,320),(640,375),(670,320)],'#FFF3C6',7)
  for i in range(12):
   a=i*math.tau/12;z=enter(t,.8,1.5);line(scene,[(640+130*math.cos(a),320+130*math.sin(a)),(640+(130+50*z)*math.cos(a),320+(130+50*z)*math.sin(a))],p['accent'],5)
 elif k==53:
  points=[(200+i*12,390+110*math.sin(i/11)) for i in range(75)];limit=round(q*74)
  for i in range(0,limit,3):circle(scene,*points[i],4,p['secondary'])
  x,y=points[limit];icon(scene,x,y,p,0,.65)
 elif k==54:
  words=cfg['text'].split()[:6];sizes=[measure(w,54) for w in words];x=640-(sum(sizes)+25*(len(words)-1))/2
  for i,w in enumerate(words):
   text(scene,w,x,355,54,p['text'],anchor='left');a=enter(t,.2+i*.45,.6+i*.45);line(scene,[(x,405),(x+sizes[i]*a,405)],p['accent'],9);x+=sizes[i]+25
 elif k==55:
  for i in range(12):
   a=enter(t,.1+i*.1,.9+i*.1);x=260+(i%4)*250;y=230+(i//4)*160;icon(scene,mix(640,x,a),mix(380,y,a),p,2,.65)
 elif k==56:
  paste(scene,text_block(cfg['text'],p,850,150,70),640,370);pts=[(210,280),(1060,280),(1060,465),(210,465),(210,280)];a=prog(t,.5,2.8);line_part(scene,pts,a,p['accent'],11)
 elif k==57:
  pts,lo,hi=data_points(cfg['values'],bottom=500);line(scene,[(240,190),(240,500),(1100,500)],p['muted'],3)
  for value,yy in [(hi,210),(lo,500)]:
   line(scene,[(230,yy),(240,yy)],p['muted'],2);text(scene,f'{value:g}',217,yy,23,p['muted'],anchor='right')
  if lo<0<hi:
   zero=500-(0-lo)/(hi-lo)*290;line(scene,[(240,zero),(1100,zero)],p['muted'],1);text(scene,'0',217,zero,23,p['muted'],anchor='right')
  x,y=line_part(scene,pts,q,p['accent'],7);circle(scene,x,y,13,p['secondary']);text(scene,str(round(lo+(500-y)/290*(hi-lo))),x,y-40,35,p['text']);text(scene,'DATA DEMO',1030,545,19,p['muted'])
 elif k==58:
  board=cover(media(cfg,0),(900,420));scene.alpha_composite(warp_quad(board,[(180+180*q,180),(1100-180*q,180),(1100,590),(180,590)]));person_at(scene,person,640,470,.8)
 elif k==59:
  scene=schematic()
  for i in range(3):
   a=enter(t,.15+i*.25,.9+i*.25);card_at(scene,cfg,i,320+320*i,350+45*math.sin(i),w=250,h=285,angle=(-1)**i*8,opacity=a)
  for x,y in [(175,170),(1080,170),(175,565),(1080,565)]:line(scene,[(x,y+22),(x,y),(x+22,y)],'#7C8478',3)
 elif k==60:
  scene=schematic();nodes=[(270,420),(600,260),(1010,435)];line_part(scene,nodes,q,'#A45744',4)
  for i,(x,y) in enumerate(nodes):
   a=enter(t,.3+i*.7,.6+i*.7);stamp=layer(180,100);rr(stamp,(4,4,175,95),None,4,'#A45744',5);text(stamp,['01','02','03'][i],90,50,42,'#A45744');paste(scene,stamp,x,y,scale=1.5-.5*a,opacity=a,angle=(-1)**i*8)
 elif k==61:
  for i in range(4):
   a=enter(t,.2+i*.2,1.2+i*.2);art=layer(255,320);rr(art,(0,0,254,319),'#FBF1DD',3);paste(art,cover(media(cfg,i),(225,245)),127,138);paste(scene,art,mix(640,300+i*220,a),380,angle=mix(0,(i-1.5)*9,a),opacity=a)
 elif k==62:
  photo=cover(media(cfg,0),(W,H));pts=[]
  for i in range(48):
   a=i*math.tau/48;r=(220+18*math.sin(i*6.3))*e;pts.append((640+r*math.cos(a),360+r*math.sin(a)))
  mask=Image.new('L',(W,H));ImageDraw.Draw(mask).polygon(pts,fill=255);photo.putalpha(mask);scene.alpha_composite(photo);line(scene,pts+[pts[0]],p['secondary'],8)
 elif k==63:
  scene=cover(backdrop or asset(cfg,0),(W,H)) if (backdrop is not None or asset(cfg,0) is not None) else schematic();points=cfg.get('route_points') or [(220+i*12,450-130*math.sin(i/17)) for i in range(70)];x,y=line_part(scene,points,q,'#A45744',4);angle=path_heading(points,q);d=ImageDraw.Draw(scene);d.polygon([(x+xx*math.cos(angle)-yy*math.sin(angle),y+xx*math.sin(angle)+yy*math.cos(angle)) for xx,yy in [(25,0),(-25,-8),(-5,0),(-25,8)]],fill='#9D4C3A');circle(scene,*points[0],9,'#9D4C3A');circle(scene,*points[-1],9,'#9D4C3A')
 elif k==64:
  old=str(cfg.get('from_year','1952'));new=str(cfg.get('to_year','2026'));h=max(.025,abs(math.cos(math.pi*q)));word=new if q>.5 else old;tile=text_block(word,p,600,300,130);tile=tile.resize((600,max(2,int(300*h))));paste(scene,tile,640,380);line(scene,[(335,380),(945,380)],p['secondary'],3)
 elif k==65:
  board=layer(1000,500)
  for i in range(8):paste(board,cover(media(cfg,i),(230,230)),130+(i%4)*245,125+(i//4)*245)
  paste(scene,board,640-150*q,370+40*q,scale=1+q*1.25)
 elif k==66:
  art=cover(media(cfg,0),(570,360));paste(scene,art,640+25*math.sin(t),370);rr(scene,(335-15*math.sin(t),155,945-15*math.sin(t),585),None,6,'#A98350',27);rr(scene,(348,168,932,572),None,2,'#EBD39B',5)
 elif k==67:
  page=layer(650,480);rr(page,(0,0,649,479),'#EFE9DC',12);a=enter(t,.4,1.7);paste(page,cover(src,(570,round(mix(360,200,a)))),325,120+80*(1-a));text(page,'DESIGN SYSTEM',325,285,32,'#26353B',opacity=a)
  for i in range(3):icon(page,145+i*180,385,p,i,.5*a)
  paste(scene,page,640,380)
 elif k==68:
  colors=['#DA896B','#83A7B5','#B2A0CC','#D3BE7F'];a=enter(t,.2,1.4)
  for i,c in enumerate(colors):rr(scene,(250+i*205,230,390+i*205,230+140*a),c,70*(1-q))
  rr(scene,(250,440,390+615*q,535),colors[min(3,int(t*.8))],18)
 elif k==69:
  for i,size in enumerate([26,38,54,76]):
   a=enter(t,.2+i*.35,.8+i*.35);text(scene,cfg['text'],300,220+i*105,size,p['text'],opacity=a,anchor='left');line(scene,[(250,220+i*105),(280,220+i*105)],p['accent'],3)
 elif k==70:
  for x in range(250,1051,200):line_part(scene,[(x,170),(x,590)],q,p['muted'],2)
  for y in range(170,591,140):line_part(scene,[(250,y),(1050,y)],q,p['muted'],2)
  for i in range(6):
   a=enter(t,.8+i*.15,1.4+i*.15);paste(scene,cover(media(cfg,i),(180,115)),350+(i%4)*200,240+(i//4)*140,opacity=a)
 elif k==71:
  for i in range(5):
   z=(i-2)*q;tile=cover(media(cfg,i),(550,250));quad=[(350+z*90,290+z*40),(880+z*90,225+z*40),(980+z*90,390+z*40),(450+z*90,455+z*40)];scene.alpha_composite(warp_quad(tile,quad))
 elif k==72:
  for row in range(4):
   yy=220+row*100;line(scene,[(200,yy),(1100,yy)],p['muted'],2)
   for col in range(4):
    a=enter(t,.05*(row*4+col),.8+.05*(row*4+col));x=220+col*210;rr(scene,(x,yy-30-80*(1-a),x+175,yy+30-80*(1-a)),p['accent'] if row%2 else p['secondary'],8)
  line(scene,[(210+q*860,160),(210+q*860,590)],p['text'],4)
 elif k==73:
  lines=cfg.get('lines',['Satu idea yang jelas.','Susun lapisan mengikut makna.','Beri ruang untuk membaca.','Gerak menyokong cerita.'])
  for i,s in enumerate(lines[:5]):
   tile=text_img(s,fit_size(s,850,42),p['text']);tile=crop_reveal(tile,enter(t,.2+i*.6,.7+i*.6),'left');paste(scene,tile,270,225+i*92,anchor='left')
 elif k==74:
  before=[(420,265,350,180),(860,265,350,180),(420,485,350,180),(860,485,350,180)];after=[(370,380,280,410),(800,230,510,135),(800,395,510,135),(800,560,510,135)]
  for i,(a,b) in enumerate(zip(before,after)):
   x,y,w,h=[mix(v,z,q) for v,z in zip(a,b)];paste(scene,cover(media(cfg,i),(max(2,int(w)),max(2,int(h)))),x,y)
 elif k==75:
  a=prog(t,.5,3.6)
  for i in range(7):
   z=clamp(a*1.5-i*.08);ww=max(2,round(125*abs(math.cos(z*math.pi))));art=cover(media(cfg,0 if z<.5 else 1),(125,390)).resize((ww,390));paste(scene,art,265+i*125,380)
 elif k==76:
  for i in range(8):
   a=pop(prog(t,.1+i*.16,1.1+i*.16));card_at(scene,cfg,i,300+(i%4)*230,410+85*(i//4)-330*(1-a),w=200,h=170,angle=(1-a)*35,opacity=clamp(a))
 elif k==77:
  words=(' '+cfg['text']+'  /')*5;tile=text_img(words,72,p['text']);paste(scene,tile,640-((t*220)%(tile.width/5)),360);rr(scene,(450,270,830,445),None,15,p['accent'],6);rr(scene,(80,270,450,445),rgba(p['bg'],190),0);rr(scene,(830,270,1200,445),rgba(p['bg'],190),0)
 elif k==78:
  scene=src.copy();cx=440+350*q;cy=370+80*math.sin(t);magnified=zoom(src,2.4,cx/W,cy/H);mask=Image.new('L',(W,H));ImageDraw.Draw(mask).ellipse((cx-125,cy-125,cx+125,cy+125),fill=255);magnified.putalpha(mask);scene.alpha_composite(magnified);circle(scene,cx,cy,126,None,p['accent'],5);line(scene,[(cx+90,cy+90),(cx+210,cy+180)],p['secondary'],12)
 elif k==79:
  for i in range(3):
   shift=(i-1)*210;fold=(i-1)*q*65;tile=cover(media(cfg,i),(220,330));quad=[(530+shift,220+fold),(750+shift,220-fold),(750+shift,550-fold),(530+shift,550+fold)];scene.alpha_composite(warp_quad(tile,quad))
 elif k==80:
  other=cover(media(cfg,0),(W,H));positions=[(320,220),(960,220),(320,520),(960,520)]
  for i,(x,y) in enumerate(positions):
   box=((i%2)*640,(i//2)*360,(i%2+1)*640,(i//2+1)*360);piece=other.crop(box);piece=piece.resize((int(mix(450,640,q)),int(mix(250,360,q))));paste(scene,piece,mix(x,320+640*(i%2),q),mix(y,180+360*(i//2),q),angle=(1-q)*(-1)**i*8)
 else:raise ValueError('Unknown CFX extension '+pid)
 if k not in (29,32,33,37,43,50,54,56,64,69,73,77):caption(scene,cfg['text'],p,y=590 if k==57 else 575)
 if cfg.get('presentation')=='full':return scene
 im=base(cfg);stage=cover(scene,(1060,460));mask=Image.new('L',stage.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,1059,459),18,fill=255);stage.putalpha(mask);rr(im,(100,143,1180,623),p['secondary'],24);paste(im,stage,640,383,opacity=1-leave(t,4.6,5));return im

def render(pid,t,cfg):return compose(pid,t,cfg)
