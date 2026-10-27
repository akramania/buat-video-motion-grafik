"""Creator FX 20: original, seekable compositing recipes, not source templates.

Call compose(pid, t, cfg, footage=RGBA, subject=RGBA, backdrop=RGBA) with
already prepared per-frame layers. This module does not run matting/tracking,
invent depth, generate speech or infer word timestamps. Preview art is original.
Clock is normalized 0..5; render.frame converts actual output seconds for CLI.
"""
from functools import lru_cache
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
from core import *

SOURCE='https://www.instagram.com/reel/De25fKeTRl7/'
NAMES=[
 ('Digital Punch Zoom','Zoom pada fokus tanpa mengubah kedudukan anchor.','anchor crop + eased scale'),
 ('Vertigo Layers','Subjek kekal; skala latar berubah untuk simulasi dolly zoom.','independent subject/background scale'),
 ('Background Swap','Reveal latar baharu di belakang cutout beralpha.','prepared alpha subject + background wipe'),
 ('Frame Break','Subjek melangkaui sempadan kad yang sedang bergerak.','clipped card + unbounded foreground composite'),
 ('Sticky Text','Label mengikut anchor objek yang bergerak.','shared analytic anchor + leader line'),
 ('Headline Wall','Kad tajuk membina dinding di belakang subjek.','staggered headlines + occluded cutout'),
 ('Doodle Boil','Kontur dan garisan lukisan hidup dalam gelung diskret.','three deterministic contour states + draw-on'),
 ('Pull-back Reveal','Kamera berundur untuk mendedahkan papan komposisi.','nested scene + perspective scale reveal'),
 ('Depth Scatter','Perkataan berpisah pada skala dan kedalaman berlainan.','independent glyph groups + blur depth planes'),
 ('UI World','Panel aplikasi asli membina ruang di sekeliling subjek.','staggered UI cards + parallax'),
 ('Phone Mockup','Footage melekat pada skrin telefon berperspektif.','screen clipping + homography + bezel'),
 ('Freeze and Label','Aksi berhenti pada cue dan label dilukis ke subjek.','time clamp + leader reveal'),
 ('Spotlight Focus','Sorotan mengikuti fokus sambil kawasan lain dimalapkan.','animated luminance mask'),
 ('Before After Wipe','Dua keadaan dibandingkan pada crop yang sama.','registered split wipe + divider'),
 ('Spotify-style Scroll','Senarai bergulir dengan item aktif pada pusat; pilihan mod lirik.','cue-driven vertical list + active line + cards'),
 ('Paper Cut Reveal','Jalur kertas bergerigi membuka lapisan seterusnya.','deterministic torn polygon matte'),
 ('Zoom-through Cut','Kamera masuk melalui portal ke komposisi berikutnya.','expanding portal + scale handoff'),
 ('Orbit Cards','Kad mengorbit di hadapan dan belakang subjek.','ellipse path + depth sort + scale'),
 ('Comment Bubble','Gelembung pertanyaan diikuti balasan berturutan.','spring bubble + connector + reply cue'),
 ('Motion Echo Trail','Salinan masa lampau tertinggal di belakang gerakan.','time-offset samples + decaying opacity'),
]

PRESETS={}
for n,(name,description,mechanism) in enumerate(NAMES,1):
 pid=f'CFX{n:02d}'
 PRESETS[pid]=dict(name=name,description=description,genre='creator',genres=['creator','education','promo'],
  family='creator-fx',category='creator-fx',text='IDEA JADI GERAK',subtitle='Creator FX 20',duration=6,
  source_url='' if n==20 else SOURCE if n not in (12,13,15) else ('https://www.instagram.com/reel/DemwQgyTKQu/' if n==15 else 'https://www.instagram.com/reel/DeXE2T0z7QW/'),
  source_product='Instagram · Creator FX references' if n!=20 else 'Creator FX 20 · Original extension',
  mechanism=mechanism,variant_basis='adapted',adaptation_status='original-implementation',
  observation_basis='browser-sampled' if n in (6,8,9,15,19) else 'original-extension' if n==20 else 'visible-label-or-metadata',
  observed_timestamp='Reel 23.67s: samples ~2.3s, 16.7s, 18.7s, 22.9s; label list visible throughout' if n in (6,8,9,19) else 'No exact movement match asserted; see creator-fx-20.md',
  use_cases=['reel','talking head','explainer','layered compositing'],
  limitations='Original vector demo; real subjects require prepared alpha/mask. 2.5D simulation, not reconstructed 3D. No automatic tracking or audio alignment.',
  parameters=['image_path','subject_path','background_path','focus_x','focus_y','amount','freeze_at','lines','line_cues','scroll_mode','freeze_image_path'],
  focus_x=.5,focus_y=.48,amount=1.,freeze_at=1.8,
  lines=['Satu idea dahulu','Kemudian beri konteks','Gerakkan fokus utama','Biar mesej mudah dibaca'],
  line_cues=[0.,1.25,2.5,3.75],scroll_mode='list')

PRESETS['CFX15'].update(observed_timestamp='Browser samples ~12.4, 24.4 and 36.5s of 46.04s reel; scrolling list/inset UI observed', source_product='Instagram · Scrolling list / perspective inset')
PRESETS['CFX20'].update(source_product='Creator FX 20 · Original extension', observed_timestamp='Original extension; not claimed as an observed source effect')

def cover(src,size):
 return ImageOps.fit(src.convert('RGBA'),tuple(map(int,size)),method=Image.Resampling.BICUBIC)

@lru_cache(maxsize=12)
def image_asset(path):
 with Image.open(Path(path).expanduser()) as im:return im.convert('RGBA')

@lru_cache(maxsize=1)
def demo_person():
 im=layer(440,540);d=ImageDraw.Draw(im)
 # Connected head/neck/shoulder silhouette. No third-party likeness/assets.
 d.rounded_rectangle((83,272,357,552),70,fill='#2F8E8A')
 d.polygon([(95,290),(22,438),(72,468),(142,329)],fill='#2F8E8A')
 d.polygon([(343,290),(420,438),(366,470),(298,330)],fill='#2F8E8A')
 d.rounded_rectangle((188,215,253,306),22,fill='#D88F6E')
 d.ellipse((127,65,313,254),fill='#E7AB88')
 d.polygon([(131,155),(122,95),(146,45),(202,26),(271,44),(314,99),(306,155),(286,112),(258,88),(195,100),(155,96)],fill='#23283D')
 d.ellipse((118,141,144,185),fill='#E7AB88');d.ellipse((298,141,324,185),fill='#E7AB88')
 d.arc((154,128,189,148),185,350,fill='#2A2D3D',width=5);d.arc((249,128,284,148),185,350,fill='#2A2D3D',width=5)
 d.ellipse((166,153,176,166),fill='#272C3E');d.ellipse((262,153,272,166),fill='#272C3E')
 d.line((219,160,211,188,225,190),fill='#BC775B',width=4)
 d.arc((189,190,253,224),10,165,fill='#914E48',width=4)
 d.polygon([(173,280),(220,322),(269,280),(257,267),(220,293),(186,265)],fill='#E6D7C3')
 d.line((220,323,220,490),fill='#237C79',width=4)
 d.ellipse((205,348,213,356),fill='#D4F2DC')
 return im

@lru_cache(maxsize=3)
def room(alternate=False):
 im=layer();d=ImageDraw.Draw(im);d.rectangle((0,0,W,H),fill='#193443' if alternate else '#EBE6DD')
 for x in range(0,W,160):d.line((x,0,x,H),fill='#315263' if alternate else '#D9D2C8',width=2)
 d.rectangle((820,105,1140,390),fill='#7EB6BF' if alternate else '#C0D2D3')
 for x in (820,980,1140):d.line((x,105,x,390),fill='#42647A',width=9)
 d.line((820,245,1140,245),fill='#42647A',width=9)
 d.rounded_rectangle((95,365,465,660),34,fill='#D7A16E' if alternate else '#9EABA2')
 d.rectangle((80,550,1220,690),fill='#284E5D' if alternate else '#BBAA92')
 d.rectangle((75,175,345,190),fill='#406578')
 for x,h,c in [(110,78,'#DE8F70'),(152,103,'#D2BE90'),(196,88,'#7BABA1')]:d.rectangle((x,175-h,x+32,175),fill=c)
 return im

def subject_layer(t,cfg,subject=None,move=True):
 im=subject or (image_asset(cfg['subject_path']) if cfg.get('subject_path') else demo_person())
 x=640+90*math.sin(t*1.3) if move else 640
 s=min(440/im.width,465/im.height)
 return im,x,s

def footage_layer(t,cfg,footage=None,subject=None,backdrop=None,alternate=False,move=True):
 if footage is not None:return cover(footage,(W,H))
 if cfg.get('image_path'):return cover(image_asset(cfg['image_path']),(W,H))
 bg=backdrop or (image_asset(cfg['background_path']) if cfg.get('background_path') else room(alternate))
 im=cover(bg,(W,H));person,x,s=subject_layer(t,cfg,subject,move)
 paste(im,person,x,465,scale=s)
 return im

def zoom(src,scale,fx=.5,fy=.48):
 # Crop around a stable normalized focus without revealing empty edges.
 scale=max(1.,scale);ww=src.width/scale;hh=src.height/scale
 left=clamp(fx*src.width-ww/2,0,src.width-ww);top=clamp(fy*src.height-hh/2,0,src.height-hh)
 return src.crop((left,top,left+ww,top+hh)).resize(src.size,Image.Resampling.BICUBIC)

def caption(im,value,p,y=575,size=42):
 size=fit_size(value,990,size);tile=text_img(value,size,p['text'])
 rr(im,(640-tile.width/2-24,y-tile.height/2-16,640+tile.width/2+24,y+tile.height/2+16),rgba('#172232',230),17)
 paste(im,tile,640,y)

def draw_card(title,body,p,w=280,h=150):
 im=layer(w,h);rr(im,(0,0,w-1,h-1),p['panel'],20,p['secondary'],2)
 text(im,title,22,36,fit_size(title,w-44,24),p['accent'],anchor='left')
 for i in range(3):rr(im,(23,71+i*19,w-23-i*22,78+i*19),rgba(p['muted'],100),3)
 if body:text(im,body,22,h-25,15,p['text'],anchor='left')
 return im

def compose(pid,t,cfg,footage=None,subject=None,backdrop=None):
 """Return the full design canvas. Inputs are current-frame prepared layers.

 For CFX12 feed the cached freeze frame after freeze_at (or freeze_image_path).
 For CFX20 supply cfg['_echo_subjects'] as [(past_rgba,x,y,scale), ...]
 for genuine footage echoes; otherwise the original analytic demo is sampled.
 CFX05 can use cfg['_anchor']=(x,y) from an externally verified track.
 """
 p=palette(cfg);im=base(cfg);k=int(pid[3:]);amount=clamp(float(cfg.get('amount',1)),0,2)
 a=enter(t,.1,.7);end=1-leave(t,4.55,5)
 fx=float(cfg.get('focus_x',.5));fy=float(cfg.get('focus_y',.48))
 src=footage_layer(t,cfg,footage,subject,backdrop)
 person,x,ps=subject_layer(t,cfg,subject)
 scene=src.copy()
 if k==1:
  z=1+.32*amount*ease(prog(t,.7,1.2))-.16*amount*ease(prog(t,2.6,3.2))
  scene=zoom(src,z,fx,fy)
 elif k==2:
  bg=cover(backdrop or room(),(W,H));scene=zoom(bg,1+.65*amount*smooth(prog(t,.7,3.7)),fx,fy)
  paste(scene,person,640,465,scale=ps)
 elif k==3:
  scene=footage_layer(t,cfg,None,subject,room(False));other=footage_layer(t,cfg,None,subject,backdrop or room(True))
  edge=round(W*smooth(prog(t,.6,2.7)));scene.paste(other.crop((0,0,edge,H)),(0,0))
  line(scene,[(edge,140),(edge,615)],p['accent'],5)
 elif k==4:
  scene=base(cfg);q=enter(t,.3,1.5);card=cover(room(),(580,310));paste(scene,card,640,390,angle=-5*q)
  rr(scene,(346,230,934,550),None,25,p['secondary'],5)
  paste(scene,person,640,425-35*q,scale=ps*(.65+.48*q))
 elif k==5:
  anchor=cfg.get('_anchor',(x+65,291));ax,ay=anchor
  line(scene,[(ax,ay),(ax+118,ay-68),(ax+310,ay-68)],p['accent'],4)
  circle(scene,ax,ay,8,p['accent']);text(scene,cfg['text'],ax+130,ay-95,fit_size(cfg['text'],270,28),p['text'],anchor='left',stroke=2,stroke_color='#172232')
 elif k==6:
  scene=base(cfg)
  for i in range(8):
   q=enter(t,.1+i*.13,.6+i*.13);col=i%4;row=i//4
   card=draw_card(['IDEA','CERITA','VISUAL','FOKUS'][col],cfg['text'],p,290,160)
   paste(scene,card,150+col*325,270+row*195+70*(1-q),opacity=q,angle=(-1)**i*4)
  paste(scene,person,x,465,scale=ps)
 elif k==7:
  scene=src.copy();state=int(t*8)%3
  mask=person.getchannel('A').resize((round(person.width*ps),round(person.height*ps)))
  mask=mask.filter(ImageFilter.MaxFilter(15+state*2));outline=Image.new('RGBA',mask.size,p['accent']);outline.putalpha(mask)
  paste(scene,outline,x+(state-1)*2,465)
  paste(scene,person,x,465,scale=ps)
  pts=[(350+i*17,560+8*math.sin(i*.8+state)) for i in range(round(34*enter(t,.4,1.5)))]
  if len(pts)>1:line(scene,pts,p['secondary'],6)
 elif k==8:
  scene=base(cfg);z=1-.56*smooth(prog(t,.6,2.6));tile=src.resize((720,405))
  # Render the board first; the hero tile recedes to reveal its context.
  for i in range(4):paste(scene,draw_card(['SKRIP','ASET','CUE','HASIL'][i],'',p,220,155),200+290*i,420,opacity=1-z)
  paste(scene,tile,640,360,scale=z*1.8,angle=-5*(1-z))
 elif k==9:
  scene=src.copy();words=cfg['text'].split()[:7];q=smooth(prog(t,.7,2.8))
  for i,w in enumerate(words):
   depth=i/max(1,len(words)-1);tx=640+(i-(len(words)-1)/2)*240*q
   ty=380+math.sin(i*2.1)*125*q;sz=int(54+(depth-.4)*75*q)
   tile=text_img(w,max(24,sz),p['accent'] if i%2 else p['text'])
   if depth<.3:tile=tile.filter(ImageFilter.GaussianBlur(3*q))
   paste(scene,tile,tx,ty,scale=.65+.55*q)
 elif k==10:
  scene=base(cfg)
  for i in range(5):
   q=enter(t,.15+i*.18,.8+i*.18);angle=(-1)**i*(8+2*math.sin(t+i));xx=[260,1030,210,1035,640][i];yy=[250,260,475,490,195][i]
   paste(scene,draw_card(['IDEA','TIMELINE','CAPTION','EXPORT','PROJEK'][i],'',p,255,145),xx,yy+80*(1-q),opacity=q,angle=angle)
  paste(scene,person,640,475,scale=ps)
 elif k==11:
  scene=base(cfg);phone=layer(300,500);rr(phone,(0,0,299,499),'#0D1422',36,'#C2D7D9',5)
  screen=cover(src,(268,438));mask=Image.new('L',screen.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,267,437),22,fill=255);screen.putalpha(mask);phone.alpha_composite(screen,(16,38))
  rr(phone,(110,12,190,23),'#8295A4',6)
  q=smooth(prog(t,.2,2));dx=45*math.sin(t*.7)
  quad=[(460+dx,170),(775+dx,145+30*q),(810+dx,615),(490+dx,595)]
  scene.alpha_composite(warp_quad(phone,quad))
 elif k==12:
  frozen=float(cfg.get('freeze_at',1.8));held=t>=frozen
  scene=footage_layer(min(t,frozen),cfg,footage,subject,backdrop)
  if held and cfg.get('freeze_image_path'):scene=cover(image_asset(cfg['freeze_image_path']),(W,H))
  q=enter(t,frozen,frozen+.65);px=640+90*math.sin(frozen*1.3)
  line(scene,[(px+55,300),(px+190*q,240),(px+380*q,240)],rgba(p['accent'],255*q),4)
  text(scene,'FREEZE',px+205,203,32,p['accent'],opacity=q,anchor='left')
  text(scene,cfg['text'],640,570,fit_size(cfg['text'],900,40),p['text'],opacity=q,stroke=2,stroke_color='#162235')
 elif k==13:
  scene=src.copy();mask=Image.new('L',(W,H),185);d=ImageDraw.Draw(mask);cx=640+190*math.sin(t*1.4);cy=340+65*math.cos(t)
  d.ellipse((cx-150,cy-170,cx+150,cy+170),fill=0);mask=mask.filter(ImageFilter.GaussianBlur(28))
  dark=layer();dark.putalpha(mask);scene.alpha_composite(dark)
  ImageDraw.Draw(scene).ellipse((cx-152,cy-172,cx+152,cy+172),outline=p['accent'],width=3)
 elif k==14:
  before=ImageOps.grayscale(src).convert('RGBA');after=footage_layer(t,cfg,None,subject,room(True));scene=before
  edge=round(W*(.18+.64*smooth(prog(t,.5,3.7))));scene.paste(after.crop((0,0,edge,H)),(0,0));line(scene,[(edge,145),(edge,610)],p['accent'],5)
  rr(scene,(edge-23,350,edge+23,395),p['accent'],18);text(scene,'< >',edge,373,17,'#132236')
  text(scene,'SELEPAS',120,190,24,p['accent']);text(scene,'SEBELUM',1110,190,24,'#25314B')
 elif k==15:
  scene=src.copy() if cfg.get('scroll_mode','list')=='list' else base(cfg);lines=cfg.get('lines',PRESETS[pid]['lines']);cues=cfg.get('line_cues',PRESETS[pid]['line_cues'])
  if cfg.get('scroll_mode','list')=='list' and footage is None and not cfg.get('image_path'):
   scene=cover(backdrop or room(),(W,H));paste(scene,person,x-260,465,scale=ps)
  if len(lines)!=len(cues) or not lines:raise ValueError('lines and line_cues must have equal nonzero length')
  idx=max([i for i,c in enumerate(cues) if t>=c] or [0]);frac=smooth(prog(t,cues[idx],cues[idx]+.38));scroll=max(0,idx-1)+frac if idx else 0
  is_list=cfg.get('scroll_mode','list')=='list';clip=layer();left,right=(605,1120) if is_list else (210,1070);center=(left+right)/2
  rr(clip,(left,150,right,610),rgba(p['panel'],235),30)
  for i,s in enumerate(lines):
   yy=335+(i-scroll)*100;tile=text_img(s,fit_size(s,350 if is_list else 750,30 if is_list else 48),p['text'] if i==idx else p['muted'])
   if i==idx:rr(clip,(left+15,yy-39,right-15,yy+39),rgba(p['accent'],30),18)
   if is_list:
    rr(clip,(left+26,yy-25,left+76,yy+25),p['accent'] if i==idx else p['secondary'],9)
    text(clip,str(i+1),left+51,yy,22,'#172232')
   paste(clip,tile,center+25 if is_list else center,yy,opacity=1 if i==idx else .45)
  mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rounded_rectangle((left,150,right,610),30,fill=255);clip.putalpha(ImageChops.multiply(clip.getchannel('A'),mask));scene.alpha_composite(clip)
 elif k==16:
  scene=base(cfg);q=smooth(prog(t,.3,3));edge=int(1280*q);pts=[(0,0),(edge,0)]+[(edge+(-1)**i*(13+(i*17)%23),i*30) for i in range(25)]+[(0,H)]
  matte=Image.new('L',(W,H));ImageDraw.Draw(matte).polygon(pts,fill=255)
  paper=src.copy();paper.putalpha(matte);scene.alpha_composite(paper)
  line(scene,pts[1:-1],'#F6EAD5',12)
 elif k==17:
  scene=src.copy();q=smooth(prog(t,.6,2.8));r=int(25+1250*q*q);mask=Image.new('L',(W,H));ImageDraw.Draw(mask).ellipse((640-r,360-r,640+r,360+r),fill=255)
  other=zoom(footage_layer(t,cfg,None,subject,room(True)),max(1,1.7-.7*q));other.putalpha(mask);scene.alpha_composite(other)
  ImageDraw.Draw(scene).ellipse((640-r,360-r,640+r,360+r),outline=p['accent'],width=8)
 elif k==18:
  scene=base(cfg);objects=[]
  for i in range(5):
   phase=t*1.2+i*math.tau/5;z=math.sin(phase);objects.append((z,210*math.cos(phase),75*z,i))
  for z,xx,yy,i in sorted(objects):
   if z<0:paste(scene,draw_card(['IDEA','TEKS','ASET','CUE','FX'][i],'',p,200,110),640+xx*1.8,375+yy,scale=.65+.2*(z+1),opacity=.7)
  paste(scene,person,640,475,scale=ps)
  for z,xx,yy,i in sorted(objects):
   if z>=0:paste(scene,draw_card(['IDEA','TEKS','ASET','CUE','FX'][i],'',p,200,110),640+xx*1.8,485+15*z,scale=.65+.2*(z+1))
 elif k==19:
  scene=src.copy();q=pop(prog(t,.3,1));r=pop(prog(t,1.8,2.5))
  bubble=layer(490,110);rr(bubble,(0,0,489,109),'#F4F0E7',45);circle(bubble,50,55,26,'#B9C8CD');text(bubble,'Boleh buat macam ini?',290,54,27,'#233847')
  paste(scene,bubble,590,380,scale=q,opacity=min(1,q))
  if r>0:
   reply=layer(390,115);rr(reply,(0,0,389,114),p['panel'],28,p['accent'],2);text(reply,cfg['text'],195,56,fit_size(cfg['text'],340,29),p['accent'])
   paste(scene,reply,760,515,scale=r,opacity=min(1,r));line(scene,[(400,425),(400,505),(555,505)],p['secondary'],3)
 elif k==20:
  scene=cover(backdrop or room(True),(W,H));echoes=cfg.get('_echo_subjects')
  if echoes is None:echoes=[(person,640+200*math.sin((t-j*.22)*1.35),465,ps) for j in range(5,0,-1)]
  for j,(art,xx,yy,ss) in enumerate(echoes):paste(scene,art,xx,yy,opacity=.08+.07*j,scale=ss)
  paste(scene,person,640+200*math.sin(t*1.35),465,scale=ps)
 else:raise ValueError('Unknown Creator FX preset '+pid)
 if k not in (5,6,9,12,15,19):caption(scene,cfg['text'],p)
 if cfg.get('presentation')=='full':return scene
 # Preserve full scene; clip it into a stage rather than crop a landscape master.
 stage=cover(scene,(1060,460));rr(im,(100,143,1180,623),p['secondary'],24)
 mask=Image.new('L',stage.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,1059,459),18,fill=255);stage.putalpha(mask)
 paste(im,stage,640,383,opacity=end)
 return im

def render(pid,t,cfg):return compose(pid,t,cfg)
