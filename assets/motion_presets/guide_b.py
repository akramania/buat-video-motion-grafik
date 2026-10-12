"""47 original, reusable guide demonstrations. 3D wording uses projected 2.5D."""
from core import *
import json
from functools import lru_cache
_INDEX=json.load(open(Path(__file__).with_name('guide_index.json')))
PRESETS={}
for n in range(54,101):
 pid=f'PV{n:03}'; d=_INDEX[pid]
 PRESETS[pid]=dict(name=d['name'],description=d['description']+'; demonstrasi asal daripada indeks panduan.',genre='saas',text='MOTION ATLAS',subtitle='Build your next idea',family='guide',duration=6,source_url=d['source_url'],adaptation_status='original-demo',category=d['category'],mechanism=d['name']+(' (projected 2.5D)' if n in (55,60,84,85,88,92) else ''))
def title(im,cfg,p,y=360,size=80,alpha=1,scale=1):
 s=cfg.get('text','MOTION ATLAS');text(im,s,640,y,fit_size(s,1000,size),p['text'],opacity=alpha,scale=scale)
def badge(im,x,y,p,s='M',scale=1):
 q=layer(160,160);rr(q,(5,5,155,155),p['accent'],32);text(q,s,80,80,68,p['bg']);paste(im,q,x,y,scale=scale)
def card(p,w=480,h=280,title_s='Workspace'):
 im=layer(w,h);rr(im,(0,0,w-1,h-1),p['panel'],24,p['muted']);text(im,title_s,30,40,25,p['text'],anchor='left');
 for i in range(3):rr(im,(30,90+i*48,w-30,114+i*48),p['accent'] if i==0 else rgba(p['muted'],80),8)
 return im
def footer(im,cfg,p):text(im,cfg.get('subtitle','Build your next idea'),640,590,28,p['muted'])
@lru_cache(maxsize=32)
def scenes(key):
 genre,bg,accent,keytext=key;p=palette(dict(genre=genre,bg=bg,accent=accent));a=base(dict(genre=genre,bg=bg,accent=accent));b=Image.new('RGBA',(W,H),p['accent'])
 text(a,'01 / EXPLORE',110,110,26,p['accent'],anchor='left');text(a,'Ideas in motion',110,210,52,p['text'],anchor='left');
 for i in range(3):paste(a,card(p,285,230,['Research','Design','Create'][i]),245+i*390,445)
 circle(b,970,280,170,p['bg']);text(b,'02 / MAKE IT REAL',110,110,26,p['bg'],anchor='left');text(b,keytext,110,210,fit_size(keytext,850,62),p['bg'],anchor='left');
 for i,v in enumerate([.35,.6,.9]):rr(b,(120+i*250,590-v*300,270+i*250,590),p['panel'],16)
 text(b,'A new perspective',1000,280,22,p['accent']);return a,b

def transition(n,t,cfg,p):
 a,b=scenes((cfg.get('genre','saas'),cfg.get('bg',''),cfg.get('accent',''),cfg.get('text','MOTION ATLAS')));q=smooth(prog(t,1.8,3.5));im=a.copy();d=ImageDraw.Draw(im)
 if n==82:
  # Two stacked panels rise from bottom, then yield scene B.
  y=round(720*(1-q));im.paste(b.crop((0,0,W,720-y)),(0,y));rr(im,(0,y-22,W,y),p['secondary'],0)
 elif n==83:
  mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask)
  for i in range(36):
   x=(i*347)%W;y=(i*197)%H;r=q*(220+(i%5)*30);md.ellipse((x-r,y-r,x+r,y+r),fill=255)
  if q>.97:mask=Image.new('L',(W,H),255)
  im=Image.composite(b,a,mask)
 elif n==84:
  if q<.5:src=a;ww=max(1,round(W*(1-q*2)))
  else:src=b;ww=max(1,round(W*((q-.5)*2)))
  im=Image.new('RGBA',(W,H),p['bg']);im.paste(src.resize((ww,H)),((W-ww)//2,0))
 elif n==85:
  im=b.copy()
  for j in range(3):
   for i in range(5):
    z=clamp(q*1.5-(i+j)*.055);tile=a.crop((i*256,j*240,(i+1)*256,(j+1)*240));paste(im,tile,128+i*256+z*450,120+j*240-z*850,scale=max(.01,1-z),angle=z*160)
 elif n==86:
  mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask);r=q*850;md.ellipse((640-r,360-r,640+r,360+r),fill=255);im=Image.composite(b,a,mask)
 elif n==87:
  for j in range(6):
   z=clamp(q*1.8-j*.14);x=round(W*z);im.paste(b.crop((0,j*120,x,(j+1)*120)),(0,j*120))
 elif n==88:
  # A and B occupy two projected faces of a rotating 2.5D cube.
  im=Image.new('RGBA',(W,H),p['bg']);split=mix(W,0,q);inset=100*math.sin(q*math.pi)
  if q<.999:im.alpha_composite(warp_quad(a,[(0,inset),(split,0),(split,H),(0,H-inset)]))
  if q>.001:im.alpha_composite(warp_quad(b,[(split,0),(W,inset),(W,H-inset),(split,H)]))
 elif n==89:
  xx=np.arange(W)[None,:];m=np.clip((q*1.5-xx/W)*510,0,255);mask=Image.fromarray(np.uint8(np.tile(m,(H,1))));im=Image.composite(b,a,mask)
  if q>=1:im=b.copy()
 elif n==90:
  x=round(W*q);im.paste(b.crop((0,0,x,H)),(0,0));line(im,[(x,0),(x,H)],p['secondary'],16);circle(im,x,360,27,p['text'])
 elif n==91:
  for j in range(6):
   for i in range(10):
    z=clamp(q*2-(i+j)*.07);box=(i*128,j*120,(i+1)*128,(j+1)*120)
    if z>0:paste(im,b.crop(box),i*128+64,j*120+60,scale=z)
  if q>=1:im=b.copy()
 elif n==92:
  im=b.copy();edge=round(W*(1-q));
  if edge>0:im.paste(a.crop((0,0,edge,H)),(0,0))
  fold=round(180*math.sin(math.pi*q));ImageDraw.Draw(im).polygon([(edge,0),(edge+fold,60),(edge+fold,H-60),(edge,H)],fill=rgba(p['secondary'],255));line(im,[(edge,0),(edge,H)],p['muted'],3)
 elif n==93:
  # A paper plane crosses; its expanding message card opens scene B.
  if q>.48:
   z=clamp((q-.48)/.52);mask=Image.new('L',(W,H));ImageDraw.Draw(mask).rectangle((640-640*z,360-360*z,640+640*z,360+360*z),fill=255);im=Image.composite(b,a,mask)
  x=mix(-140,1420,q);y=360-180*math.sin(q*math.pi);ImageDraw.Draw(im).polygon([(x-85,y-35),(x+65,y),(x-60,y+55),(x-35,y+5)],fill=p['text']);line(im,[(x-35,y+5),(x+65,y)],p['muted'],3)
 elif n==94:
  # deterministic halftone printing, expanding ink dots reveal B.
  mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask)
  for y in range(0,H+32,32):
   for x in range(0,W+32,32):
    r=clamp(q*1.6-x/W*.5)*24;md.ellipse((x-r,y-r,x+r,y+r),fill=255)
  if q>=1:mask=Image.new('L',(W,H),255)
  im=Image.composite(b,a,mask)
 elif n==95:
  # hard shot cut, with a brief whip smear around the splice.
  im=(a if q<.5 else b).copy()
  if abs(q-.5)<.13:
   im=im.filter(ImageFilter.GaussianBlur(10*(1-abs(q-.5)/.13)))
   for j in range(10):line(im,[(0,50+j*70),(W,25+j*70)],rgba(p['text'],35),8)
 elif n==96:
  mask=Image.new('L',(W,H));md=ImageDraw.Draw(mask);edge=W*q
  points=[(0,0),(edge,0)]+[(edge+math.sin(y*.08)*28,y) for y in range(0,H+1,12)]+[(0,H)];md.polygon(points,fill=255);im=Image.composite(b,a,mask)
  line(im,[(edge+math.sin(y*.08)*28,y) for y in range(0,H+1,12)],p['text'],10)
  if q>=1:im=b.copy()
 elif n==97:
  # foreground block occludes frame completely at the hidden A/B cut.
  im=(a if q<.5 else b).copy();x=mix(-W,W,q);rr(im,(x,0,x+W,H),p['panel'],0)
 elif n==98:
  # travel camera pushes A left while B enters from the right.
  im=Image.new('RGBA',(W,H),p['bg']);im.paste(a,(-round(q*W),0));im.paste(b,(round((1-q)*W),0))
 elif n==99:
  im=(a if q<.5 else b).copy();flash=max(0,1-abs(q-.5)/.22);white=Image.new('RGBA',(W,H),'white');im=Image.blend(im,white,flash)
  if q>.72:badge(im,1010,450,p,scale=.65)
 elif n==100:
  # angled geometric wipe, with real outgoing and incoming scenes.
  mask=Image.new('L',(W,H));x=mix(-500,W+500,q);ImageDraw.Draw(mask).polygon([(0,0),(x+220,0),(x-220,H),(0,H)],fill=255);im=Image.composite(b,a,mask)
 return im

def render(pid,t,cfg):
 n=int(pid[2:]);p=palette(cfg);im=base(cfg);e=enter(t,.15,1.8);s=cfg.get('text','MOTION ATLAS');sz=fit_size(s,1000,82)
 if n>=82:return transition(n,t,cfg,p)
 if n==54:
  pts=[(150+i*8,360+math.sin(i*.065)*45) for i in range(round(e*124))]
  if len(pts)>1:line(im,pts,p['accent'],70)
  title(im,cfg,p,alpha=prog(t,1.2,2.1));footer(im,cfg,p)
 elif n==55:
  # camera cranes up from projected foreground floor to hero.
  for i in range(7):line(im,[(100+i*180,720),(640+(i-3)*55,430-e*220)],rgba(p['muted'],100),2)
  paste(im,card(p,700,330,'A higher perspective'),640,650-e*310,scale=.65+.35*e);title(im,cfg,p,120,54,prog(t,1.4,2.3))
 elif n==56:
  for i in range(12):
   z=enter(t,.15+i*.05,1.7+i*.05);h=(80+(i*71)%245)*z;rr(im,(90+i*94,550-h,145+i*94,550),p['accent'] if i%2 else p['secondary'],6)
  line(im,[(90+i*94,500-(i*37)%180*e) for i in range(12)],p['text'],4);title(im,cfg,p,180,62,prog(t,1.3,2.2))
 elif n==57:
  ti=text_img(s,sz,p['text']);
  for i in range(12):
   x0=round(ti.width*i/12);x1=round(ti.width*(i+1)/12);piece=ti.crop((x0,0,x1,ti.height));paste(im,piece,640-ti.width/2+x0+piece.width/2+(1-e)*(i-6)*120,360+(1-e)*math.sin(i*2)*280,angle=(1-e)*(i-6)*20)
 elif n==58:
  for j in range(4):
   for i in range(9):
    z=prog(t,.15+(i+j)*.1,1+(i+j)*.1);x=180+i*115;y=190+j*100;circle(im,x,y,23,p['accent'] if z>.7 else p['muted']);text(im,['+','*','>'][i%3],x,y,23,p['bg'])
  title(im,cfg,p,590,58,prog(t,1.5,2.5))
 elif n==59:
  widths=[measure(c,sz) for c in s];total=sum(widths)+(len(s)-1)*(1-e)*35;x=640-total/2
  for c,w in zip(s,widths):text(im,c,x+w/2,360,sz,p['text'],opacity=e);x+=w+(1-e)*35
 elif n==60:
  for i in range(5):
   q=enter(t,.2+i*.08,1.8+i*.08);paste(im,card(p,240,300,'IDEA '+str(i+1)),640+mix((i-2)*200,(i-2)*75,q),360,angle=mix((i-2)*-75,(i-2)*12,q),scale=.55+.2*q)
  title(im,cfg,p,610,48,prog(t,1.8,2.8))
 elif n==61:
  dark=layer();ImageDraw.Draw(dark).polygon([(520,0),(760,0),(1130,660),(150,660)],fill=rgba(p['accent'],35));im.alpha_composite(dark);paste(im,card(p,700,350,'The spotlight is yours'),640,380,opacity=e,scale=.85+.15*e)
 elif n==62:
  # logo path builds segment by segment.
  pts=[(450,470),(450,230),(640,400),(830,230),(830,470)];q=prog(t,.2,2.5)*4
  for i in range(4):
   z=clamp(q-i)
   if z:line(im,[pts[i],(mix(pts[i][0],pts[i+1][0],z),mix(pts[i][1],pts[i+1][1],z))],p['accent'],22)
  title(im,cfg,p,595,54,prog(t,2,2.8))
 elif n==63:
  ti=text_img(s,sz,'white');content=layer(ti.width,ti.height)
  for i in range(14):rr(content,(i*100-200+t*70,0,i*100-150+t*70,ti.height),p['accent'] if i%2 else p['secondary'],0)
  content.putalpha(ti.getchannel('A'));paste(im,content,640,360);footer(im,cfg,p)
 elif n==64:
  # Editorial outro: three hook fragments cut to final call.
  stage=min(3,int(t/.95));words=['MAKE','YOUR','NEXT',s];text(im,words[stage],640,350,fit_size(words[stage],950,110),p['text']);line(im,[(170,470),(170+940*prog(t,2.8,3.8),470)],p['accent'],8)
 elif n==65:
  title(im,cfg,p);q=prog(t,2.2,4.8);noise=np.random.default_rng(65).random((90,160));mask=Image.fromarray(np.uint8((noise>q)*255)).resize((W,H),Image.Resampling.NEAREST);im.putalpha(mask);back=base(cfg);back.alpha_composite(im);im=back
 elif n==66:
  z=smooth(prog(t,1.2,3));badge(im,mix(640,340,z),360,p,scale=mix(1.8,.8,z));text(im,s,mix(800,780,z),360,fit_size(s,650,64),p['text'],opacity=z)
 elif n==67:
  for j in range(3):
   q=layer();text(q,s,640+math.sin(t*1.4+j)*90,230+j*130,sz,p['accent'] if j==1 else p['text'],stroke=1);glow=q.filter(ImageFilter.GaussianBlur(9));im.alpha_composite(glow);im.alpha_composite(q)
  for y in (165,425,555):line(im,[(80,y),(1200,y)],p['secondary'],2)
 elif n==68:
  # Original avatar group (no real photograph supplied) launches upward.
  for i in range(7):
   z=enter(t,.1+i*.11,1.3+i*.11);x=190+i*150;y=460+(1-z)*500-70*leave(t,3.4,4.6);circle(im,x,y,44,p['secondary']);circle(im,x,y+76,60,p['accent']);text(im,chr(65+i),x,y,30,p['bg'])
  title(im,cfg,p,170,62,prog(t,1.6,2.5))
 elif n==69:
  for i in range(5):
   z=leave(t,1+i*.3,2+i*.3);paste(im,card(p,700,70,'Layer '+str(i+1)),640+(1 if i%2 else -1)*z*1400,190+i*85)
  title(im,cfg,p,360,76,prog(t,2.6,3.6))
 elif n==70:
  z=smooth(prog(t,1.2,3.2));w=mix(720,150,z);h=mix(380,150,z);rr(im,(640-w/2,360-h/2,640+w/2,360+h/2),p['accent'],mix(22,42,z));
  if z<.85:
   for i in range(3):line(im,[(640-w*.35,310+i*55),(640+w*.35,310+i*55)],rgba(p['bg'],255*(1-z)),14)
  text(im,'M',640,360,80,p['bg'],opacity=z);title(im,cfg,p,565,54,z)
 elif n==71:
  beat=int(t*2)%4;layouts=[('CREATE',p['accent']),('CONNECT',p['secondary']),('BUILD',p['text']),(s,p['accent'])];word,c=layouts[beat];text(im,word,640,360,fit_size(word,1000,115),c);rr(im,(100,540,100+beat*250,565),c,0)
 elif n==72:
  step=min(3,int(t/1.2));colors=[p['accent'],p['secondary'],p['text'],p['accent']]
  for i,w in enumerate(['Discover','Explore','Create','Publish']):rr(im,(250,170+i*105,1030,250+i*105),colors[step] if i==step else p['panel'],16);text(im,w,640,210+i*105,40,p['bg'] if i==step else p['muted'])
 elif n==73:
  # editorial montage alternates wide composition, detail, title and graph.
  beat=int(t/.75)%4
  if beat==0:paste(im,card(p,700,380,'The workspace'),640,360)
  elif beat==1:paste(im,card(p,700,380,'Detail view'),640,360,scale=1.6)
  elif beat==2:title(im,cfg,p)
  else:
   for i in range(7):rr(im,(150+i*140,550-(i+1)*50,240+i*140,550),p['accent'],10)
 elif n==74:
  for j in range(2):
   for i in range(3):z=.8+.2*math.sin(t*2+i+j);paste(im,card(p,320,230,'Panel '+str(j*3+i+1)),260+i*380,220+j*280,scale=z)
 elif n==75:
  # Four simultaneous independent concepts, each safely clipped to quadrant.
  for i in range(4):
   sub=layer(600,310);rr(sub,(0,0,599,309),p['panel'],24)
   if i==0:circle(sub,300,155,50+30*math.sin(t*2),p['accent'])
   elif i==1:line(sub,[(40+k*50,155+70*math.sin(k*.7+t*3)) for k in range(11)],p['secondary'],9)
   elif i==2:text(sub,str(round(t*20))+'%',300,155,70,p['text'])
   else:rr(sub,(70,110,70+460*prog(t,0,5),200),p['accent'],15)
   paste(im,sub,330+(i%2)*620,185+(i//2)*350)
 elif n==76:
  # repeated smooth orbit interrupted by hard centered warning hold.
  if 2<t<3.2:text(im,'PAUSE',640,360,120,p['secondary']);rr(im,(540,500,740,520),p['secondary'],0)
  else:
   for i in range(5):a=t*2+i*math.pi*2/5;circle(im,640+260*math.cos(a),360+160*math.sin(a),44,p['accent'])
 elif n==77:
  # stepped anticipation, fast action, long settle (sakuga timing principles).
  if t<1.6:x=200+15*math.sin(t*8);sc=1
  elif t<2.05:q=prog(t,1.6,2.05);x=mix(200,990,q*q);sc=1+.6*math.sin(q*math.pi)
  else:x=990-40*math.exp(-(t-2.05)*4)*math.sin((t-2.05)*15);sc=1
  rr(im,(x-60*sc,300,x+60*sc,420),p['accent'],24);line(im,[(180,475),(1100,475)],p['muted'],3);text(im,'ANTICIPATE  /  STRIKE  /  HOLD',640,580,28,p['muted'])
 elif n==78:
  x=640+350*math.sin(t*2.2)
  for i in range(9,0,-1):past=640+350*math.sin((t-i*.04)*2.2);circle(im,past,360,60,rgba(p['accent'],18+i*9))
  circle(im,x,360,65,p['accent']);footer(im,cfg,p)
 elif n==79:
  z=prog(t,1,3.5)
  for i in range(20):
   h=mix(70+60*math.sin(i*.7+t*5),18,z);x=mix(140+i*50,240+(i//5)*210,z);y=mix(360-h/2,215+(i%5)*58,z);w=mix(30,165,z);rr(im,(x,y,x+w,y+h),p['accent'] if i%2 else p['secondary'],mix(15,5,z))
  title(im,cfg,p,590,50,z)
 elif n==80:
  # speed accelerates, stops sharply, resumes slowly.
  if t<2:q=(t/2)**3
  elif t<3.6:q=1
  else:q=1+(t-3.6)*.12
  x=180+720*min(q,1);paste(im,card(p,280,240,'Frozen detail'),x,360,angle=0 if t>=2 else -10+q*10);text(im,'FREEZE' if 2<=t<3.6 else 'SPEED RAMP',640,590,36,p['accent'])
 elif n==81:
  # trailer grammar: question / black pause / fast inserts / final release.
  if t<1.1:text(im,'What comes next?',640,360,80,p['text'])
  elif t<1.5:im=Image.new('RGBA',(W,H),p['bg'])
  elif t<3.1:
   k=int((t-1.5)*5);paste(im,card(p,500+(k%3)*140,280,'Glimpse '+str(k+1)),640,360,angle=(k%3-1)*8)
  else:title(im,cfg,p,360,80,prog(t,3.1,3.8));footer(im,cfg,p)
 return im
