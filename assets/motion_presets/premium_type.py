"""100 original typography recipes informed by public Envato listing descriptions.

PX001-PX100; deterministic Pillow frame rendering on the normalized 0..5 clock.
No Envato source files, preview frames, fonts, audio, or artwork are embedded.
"""
from core import *
from PIL import ImageChops
import json

SOURCES = [
 'https://elements.envato.com/kinetic-titles-2-0-mogrt-3J4F4XF',
 'https://elements.envato.com/typography-titles-2-0-fcpx-apple-motion-HNPH9TN',
 'https://elements.envato.com/kinetic-typography-titles-mogrt-PK2EQEF',
 'https://elements.envato.com/kinetic-titles-22SGMK4',
 'https://elements.envato.com/kinetic-titles-3-0-fcpx-6G8GZKV',
 'https://elements.envato.com/bold-editorial-titles-and-lower-thirds-for-after-e-3E4YZGP',
 'https://elements.envato.com/hook-captions-for-social-media-JZE2XRQ',
 'https://elements.envato.com/typography-titles-EW3U4ZW',
 'https://elements.envato.com/lower-thirds-DFWHQ27',
 'https://elements.envato.com/subtitle-caption-text-animations-DS7CPVF',
 'https://elements.envato.com/social-hook-titles-for-premiere-pro-RGLNV6M',
 'https://elements.envato.com/kinetic-hook-titles-B8T9WR2',
]

def E(t,a=.15,b=1.2): return ease(prog(t,a,b))
def O(t): return 1-smooth(prog(t,4.18,4.95))
def chunks(s,n=3):
 w=s.split() or ['']; n=min(n,len(w)); return [' '.join(w[round(i*len(w)/n):round((i+1)*len(w)/n)]) for i in range(n)]
def title(cfg,p,size=88,width=1000,face='bold',color=None):
 s=cfg.get('text','MAKE IT MATTER'); return text_img(s,fit_size(s,width,size,face),color or p['text'],face)
def sub(dst,cfg,p,x=640,y=528,opacity=1,anchor='center',width=960):
 s=cfg.get('subtitle','Designed to tell your story'); text(dst,s,x,y,fit_size(s,width,26,'sans'),p['muted'],'sans',opacity=opacity,anchor=anchor)
def mask(src,draw):
 m=Image.new('L',src.size,0); draw(ImageDraw.Draw(m),src.width,src.height); out=src.copy();out.putalpha(ImageChops.multiply(src.getchannel('A'),m));return out

def stage(dst,p,v,y=370):
 # Small geometric details occupy margins, leaving headlines unobstructed.
 line(dst,[(120,y-96),(174,y-96)],rgba(p['accent'],150),3)
 line(dst,[(1106,y+98),(1160,y+98)],rgba(p['accent'],150),3)
 if v%2: circle(dst,1138,y-92,5,p['secondary'])

def letters(dst,s,p,t,mode,x=640,y=366,size=88):
 size=fit_size(s,1000,size); widths=[measure(c,size) for c in s];total=sum(widths);left=x-total/2
 for i,(c,ww) in enumerate(zip(s,widths)):
  q=E(t,.12+i*.028,.76+i*.028); px=left+ww/2;py=y;sc=1.;angle=0
  if mode==0: py+=85*(1-q)+math.sin(i*.62+t*4)*12*(1-q);sc=.85+.15*q
  elif mode==1:
   ang=math.pi*2*i/max(1,len(s));px=mix(x+math.cos(ang)*460,px,q);py=mix(y+math.sin(ang)*175,y,q);angle=(1-q)*(-ang*180/math.pi)
  elif mode==2: py-=150*(1-q);angle=(1-q)*(70 if i%2 else -70);sc=.45+.55*pop(prog(t,.12+i*.025,.95+i*.025))
  else: sc=max(.02,abs(math.cos((1-q)*math.pi/2)));py+=42*(1-q);angle=(1-q)*(18 if i%2 else -18)
  if c.strip(): text(dst,c,px,py,size,p['text'],opacity=q,scale=sc,angle=angle)
  left+=ww

def family_mask(dst,t,cfg,p,v):
 im=title(cfg,p);q=E(t);w,h=im.size;cx,cy=640,365
 if v==0:
  r=mask(im,lambda d,w,h:d.rectangle((0,h*(1-q)/2,w,h*(1+q)/2),fill=255));paste(dst,r,cx,cy)
  line(dst,[(cx-w/2,cy-h*q/2-16),(cx+w/2,cy-h*q/2-16)],p['accent'],3);line(dst,[(cx-w/2,cy+h*q/2+16),(cx+w/2,cy+h*q/2+16)],p['secondary'],3)
 elif v==1:
  r=layer(w,h)
  for k in range(6):
   a=k*h//6;b=(k+1)*h//6;z=E(t,.13+k*.09,.86+k*.09);piece=im.crop((0,a,w,b));piece=mask(piece,lambda d,w,h:d.rectangle((0,0,w*z,h),fill=255));r.alpha_composite(piece,(0,a))
  paste(dst,r,cx,cy);rr(dst,(cx-w/2-18,cy+h/2+26,cx-w/2-18+max(1,w*q),cy+h/2+32),p['accent'],3)
 elif v==2:
  def checker(d,w,h):
   cell=36
   for x in range(0,w,cell):
    for y in range(0,h,cell):
     z=clamp(q*2.3-((x//cell+y//cell)%3)*.55);d.rectangle((x,y,x+cell*z,y+cell*z),fill=255)
  paste(dst,mask(im,checker),cx,cy);line(dst,[(130,cy),(180,cy)],p['accent'],4);line(dst,[(1100,cy),(1150,cy)],p['accent'],4)
 else:
  r=layer(w,h)
  for k in range(8):
   a=k*w//8;b=(k+1)*w//8;z=E(t,.10+k*.055,.92+k*.055);piece=im.crop((a,0,b,h));piece=mask(piece,lambda d,w,h:d.rectangle((0,h*(1-z),w,h),fill=255));r.alpha_composite(piece,(a,0))
  paste(dst,r,cx,cy);line(dst,[(cx-w/2,cy+h/2+24),(cx+w/2,cy+h/2+24)],rgba(p['muted'],100),2)
 sub(dst,cfg,p,opacity=E(t,.65,1.35));stage(dst,p,v)

def family_split(dst,t,cfg,p,v):
 im=title(cfg,p);w,h=im.size;q=E(t,.12,1.3);cx,cy=640,365
 if v==0:
  for k in range(2):
   crop=im.crop((0,k*h//2,w,(k+1)*h//2));paste(dst,crop,cx+(-1 if k==0 else 1)*230*(1-q),cy-h/4+k*h/2,opacity=q)
  line(dst,[(cx-70*q,cy+92),(cx+70*q,cy+92)],p['accent'],4)
 elif v==1:
  for k in range(4):
   xx=k%2;yy=k//2;a=xx*w//2;b=yy*h//2;crop=im.crop((a,b,(xx+1)*w//2,(yy+1)*h//2));paste(dst,crop,cx-w/4+xx*w/2+(xx*2-1)*160*(1-q),cy-h/4+yy*h/2+(yy*2-1)*76*(1-q),q)
  for x in (cx-w/2-24,cx+w/2+24):line(dst,[(x,cy-50),(x,cy+50)],rgba(p['accent'],150),3)
 elif v==2:
  for k in range(5):
   a=k*h//5;b=(k+1)*h//5;crop=im.crop((0,a,w,b));z=E(t,.12+k*.09,.85+k*.09);paste(dst,crop,cx+(k%2*2-1)*320*(1-z),cy-h/2+(a+b)/2,z)
  rr(dst,(cx-90,cy+86,cx+90,cy+92),p['secondary'],3)
 else:
  for k in range(2):
   cut=mask(im,lambda d,w,h:d.polygon([(0,0),(w,0),(0,h)] if k==0 else [(w,0),(w,h),(0,h)],fill=255));paste(dst,cut,cx+(k*2-1)*180*(1-q),cy+(k*2-1)*60*(1-q),q)
  line(dst,[(cx-140*q,cy+90),(cx+140*q,cy+55)],p['accent'],4)
 sub(dst,cfg,p,opacity=E(t,.75,1.5));stage(dst,p,v)

def family_letter(dst,t,cfg,p,v):
 letters(dst,cfg['text'],p,t,v);sub(dst,cfg,p,opacity=E(t,.8,1.6))
 if v==0:
  pts=[(160+i*16,450+math.sin(i*.28+t*2)*6) for i in range(61)];line(dst,pts[:max(2,int(len(pts)*E(t)))],rgba(p['accent'],145),3)
 elif v==1:
  ImageDraw.Draw(dst).arc((150,186,1130,558),0,180,fill=rgba(p['accent'],65),width=2)
 elif v==2:
  for i in range(7): circle(dst,290+i*116,458,3,p['accent'])
 else:
  line(dst,[(220,440),(1060,440)],rgba(p['muted'],60),2);circle(dst,640,440,7,p['accent'])

def family_outline(dst,t,cfg,p,v):
 s=cfg['text'];size=fit_size(s,990,90);im=text_img(s,size,p['text']);out=text_img(s,size,(0,0,0,0),'bold',2,p['accent']);q=E(t,.15,1.4);w,h=im.size
 if v==0:
  paste(dst,out,640,365);paste(dst,mask(im,lambda d,w,h:d.rectangle((0,0,w*q,h),fill=255)),640,365);line(dst,[(640-w/2+w*q,290),(640-w/2+w*q,440)],rgba(p['secondary'],180),2)
 elif v==1:
  for k in range(5,0,-1):paste(dst,out,640+(1-q)*k*34,365-(1-q)*k*19,.2+k*.07,1+(1-q)*k*.035)
  paste(dst,im,640,365,q);rr(dst,(535,450,745,455),p['accent'],3)
 elif v==2:
  for k in range(3):paste(dst,out,640,280+k*88,.2 if k!=1 else 1)
  paste(dst,mask(im,lambda d,w,h:d.rectangle((0,h*(1-q),w,h),fill=255)),640,368)
  rr(dst,(174,348,184,388),p['accent'],3);rr(dst,(1096,348,1106,388),p['accent'],3)
 else:
  for k in range(8):
   a=k*w//8;b=(k+1)*w//8;z=E(t,.15+k*.055,1.02+k*.055);piece=im.crop((a,0,b,h));paste(dst,piece,640-w/2+(a+b)/2,365+(1-z)*65,z)
  paste(dst,out,640,365,1-q);ImageDraw.Draw(dst).arc((480,428,800,486),0,180,fill=p['accent'],width=3)
 sub(dst,cfg,p,y=550,opacity=E(t,.8,1.7))

def family_writer(dst,t,cfg,p,v):
 s=cfg['text'];size=fit_size(s,960,77,'mono');q=prog(t,.18,1.72);count=int(len(s)*q);left=640-measure(s,size,'mono')/2
 if v==0:
  text(dst,s[:count],left,360,size,p['text'],'mono',anchor='left');xx=left+measure(s[:count],size,'mono');rr(dst,(xx+8,322,xx+18,402),p['accent'],2)
  line(dst,[(left,445),(left+measure(s,size,'mono'),445)],rgba(p['muted'],70),2)
 elif v==1:
  paper=panel(980,200,p['panel'],10,'');paste(dst,paper,640,372)
  text(dst,s[:count],left,352,size,p['text'],'mono',anchor='left');text(dst,'PRINT / STORY',left,423,17,p['accent'],'mono',anchor='left')
  for i in range(30):line(dst,[(163+i*33,268),(175+i*33,268)],rgba(p['muted'],100),2)
 elif v==2:
  alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';ss=''.join(c if i<count else alphabet[(i*7+int(t*13))%len(alphabet)] if c!=' ' else ' ' for i,c in enumerate(s))
  rr(dst,(130,255,1150,465),p['panel'],22,rgba(p['accent'],70));text(dst,'> '+ss,640,357,fit_size('> '+ss,940,77,'mono'),p['text'],'mono');line(dst,[(165,420),(165+900*q,420)],p['accent'],3)
 else:
  text(dst,s,left,355,size,p['text'],'mono',anchor='left',opacity=.2+.8*E(t));old=cfg['subtitle'];ww=measure(old,30,'mono');text(dst,old,640,442,fit_size(old,800,30,'mono'),p['muted'],'mono');line(dst,[(640-ww/2,445),(640-ww/2+ww*E(t,.65,1.4),445)],p['accent'],4)
  text(dst,'REWRITE THE STORY',640,500,27,p['accent'],'mono',opacity=E(t,1.25,2.0))
 if v!=3:sub(dst,cfg,p,y=534,opacity=E(t,1.2,2.0))

def family_cards(dst,t,cfg,p,v):
 ww=chunks(cfg['text'],3);n=len(ww)
 if v==0:
  gap=18;cw=min(325,960/n);left=640-(n*cw+(n-1)*gap)/2
  for k,s in enumerate(ww):
   q=E(t,.12+k*.14,1+k*.14);x=left+k*(cw+gap)+cw/2;im=panel(cw,148,p['panel'],18,p['accent']);paste(dst,im,x,370,q,scale=max(.03,q));text(dst,s,x,370,fit_size(s,cw-30,52),p['text'],opacity=q)
 elif v==1:
  for k,s in enumerate(ww):
   q=E(t,.15+k*.16,1+k*.16);x=640+(k-(n-1)/2)*275*q;y=365+abs(k-(n-1)/2)*20;im=layer(300,180);rr(im,(5,5,295,175),p['panel'],18,p['secondary'],2);text(im,s,150,90,fit_size(s,260,56),p['text']);paste(dst,im,x,y,q,angle=(k-(n-1)/2)*8*q)
 elif v==2:
  for k,s in enumerate(ww):
   q=E(t,.12+k*.23,.9+k*.23);im=layer(880,86);rr(im,(0,0,879,85),p['panel'],12,p['accent'] if k==n-1 else rgba(p['muted'],80));text(im,s,440,43,fit_size(s,780,55),p['text']);paste(dst,im,640+(-1 if k%2 else 1)*140*(1-q),275+k*102,q)
 else:
  for k,s in enumerate(ww):
   q=E(t,.14+k*.17,1.05+k*.17);cw=940/n;x=170+(k+.5)*cw;im=layer(cw-18,190);rr(im,(0,0,im.width-1,189),p['panel'],14,p['secondary']);text(im,s,im.width/2,95,fit_size(s,im.width-24,58),p['text']);scale=max(.025,abs(math.cos((1-q)*math.pi/2)));im=im.resize((im.width,max(1,int(im.height*scale))),Image.Resampling.BICUBIC);paste(dst,im,x,365,q)
 sub(dst,cfg,p,y=574,opacity=E(t,.9,1.65))

def family_scale(dst,t,cfg,p,v):
 s=cfg['text'];q=E(t,.12,1.25);im=title(cfg,p,size=88,width=900)
 if v==0:
  size=fit_size(s,830,85);sp=21*(1-q);widths=[measure(c,size) for c in s];left=640-(sum(widths)+(len(s)-1)*sp)/2
  for c,w in zip(s,widths):
   text(dst,c,left+w/2,365,size,p['text'],opacity=q);left+=w+sp
  line(dst,[(290,456),(990,456)],p['accent'],3)
 elif v==1:
  w,h=im.size;im=im.resize((max(1,int(w*(.23+.77*q))),max(1,int(h*(1.8-.8*q)))),Image.Resampling.BICUBIC);paste(dst,im,640,360,q);rr(dst,(240,452,1040,458),p['accent'],3)
 elif v==2:
  scale=2.2-1.2*q;paste(dst,im,640,365,q,scale=scale);r=54+180*q;circle(dst,640,366,r,None,rgba(p['accent'],55),2);sub(dst,cfg,p,y=571,opacity=E(t,.85,1.65));return
 else:
  z=prog(t,.13,1.4);scale=1-.30*math.exp(-z*7)*math.cos(z*math.pi*6);paste(dst,im,640,365,q,scale);circle(dst,640,365,70+220*q,None,rgba(p['accent'],max(0,85*(1-q))),3);rr(dst,(535,459,745,463),p['secondary'],2)
 sub(dst,cfg,p,opacity=E(t,.7,1.45))

def family_glitch(dst,t,cfg,p,v):
 im=title(cfg,p,width=920);w,h=im.size;q=E(t,.13,1.45);cx,cy=640,365
 if v==0:
  for k in range(9):
   a=k*h//9;b=(k+1)*h//9;sh=math.sin(k*13+t*25)*90*(1-q);paste(dst,im.crop((0,a,w,b)),cx+sh,cy-h/2+(a+b)/2,q)
  line(dst,[(220,456),(1060,456)],p['accent'],2)
 elif v==1:
  s=cfg['text'];size=fit_size(s,920,88)
  for k,c in enumerate((p['accent'],p['secondary'],p['text'])):paste(dst,text_img(s,size,c),cx+(k-1)*35*(1-q),cy+(k-1)*11*(1-q),.8 if k!=2 else q)
  for k in range(6):line(dst,[(230+k*130,461),(300+k*130,461)],rgba(p['accent'],120),3)
 elif v==2:
  def scan(d,w,h):
   step=5
   for y in range(0,h,step):d.rectangle((0,y,w,y+max(1,round(step*q))),fill=255)
  paste(dst,mask(im,scan),cx,cy,q);line(dst,[(cx-w/2-25,cy-h/2-16),(cx+w/2+25,cy-h/2-16)],p['accent'],2)
 else:
  sz=max(1,int(24*(1-q))+1);small=im.resize((max(1,w//sz),max(1,h//sz)),Image.Resampling.BILINEAR).resize((w,h),Image.Resampling.NEAREST);paste(dst,small,cx,cy,q)
  for k in range(8):rr(dst,(280+k*96,455,306+k*96,459),p['accent'],2)
 sub(dst,cfg,p,opacity=E(t,.95,1.8))

def family_lower(dst,t,cfg,p,v):
 q=E(t,.12,1.22);s=cfg['text'];size=fit_size(s,790,58);y=405
 if v==0:
  x=190;line(dst,[(x,295),(x,295+180*q)],p['accent'],5);text(dst,s,x+28+80*(1-q),y-18,size,p['text'],opacity=q,anchor='left');sub(dst,cfg,p,x=x+28,y=y+48,opacity=E(t,.5,1.4),anchor='left',width=850)
  line(dst,[(x+28,475),(x+28+780*q,475)],rgba(p['muted'],80),2)
 elif v==1:
  rr(dst,(185,290,185+900*q,495),p['panel'],90);circle(dst,275,393,61,p['accent']);text(dst,''.join(w[0] for w in s.split()[:2]),275,393,38,p['bg']);text(dst,s,367,365,size,p['text'],opacity=q,anchor='left');sub(dst,cfg,p,x=367,y=432,opacity=E(t,.4,1.2),anchor='left',width=650)
 elif v==2:
  line(dst,[(180,290),(180+920*q,290)],p['accent'],4);line(dst,[(1100,494),(1100-920*E(t,.4,1.4),494)],p['secondary'],4);text(dst,s,640,367,size,p['text'],opacity=q);sub(dst,cfg,p,y=436,opacity=E(t,.5,1.4));rr(dst,(170,280,183,301),p['accent'],2);rr(dst,(1097,484,1110,505),p['secondary'],2)
 else:
  for xx,sign in ((180,1),(1100,-1)):
   line(dst,[(xx+30*sign,285),(xx,285),(xx,490),(xx+30*sign,490)],p['accent'],4)
  text(dst,s,640,365,size,p['text'],opacity=q);sub(dst,cfg,p,y=440,opacity=E(t,.55,1.4));line(dst,[(1090,283),(1150,217),(1180,217)],rgba(p['muted'],110),2);circle(dst,1180,217,5,p['secondary'])

def family_editorial(dst,t,cfg,p,v):
 q=E(t,.15,1.3);s=cfg['text'];ww=chunks(s,2)
 if v==0:
  first=s[:1];rest=s[1:];text(dst,first,280,376,220,p['accent'],'serif',opacity=q);text(dst,rest,425,366,fit_size(rest,665,69,'serif'),p['text'],'serif',opacity=E(t,.3,1.2),anchor='left');line(dst,[(200,508),(1080,508)],rgba(p['muted'],80),2);sub(dst,cfg,p,y=558,opacity=q)
 elif v==1:
  line(dst,[(640,235),(640,496)],rgba(p['muted'],110),2)
  for k,phrase in enumerate(ww):text(dst,phrase,405+k*475,345,fit_size(phrase,410,75,'serif'),p['text'],'serif',opacity=E(t,.2+k*.3,1+k*.3))
  text(dst,'01',215,225,24,p['accent'],'mono',opacity=q);text(dst,'02',690,225,24,p['accent'],'mono',opacity=q);sub(dst,cfg,p,y=554,opacity=q)
 elif v==2:
  text(dst,s,172,322,fit_size(s,950,76,'serif'),p['text'],'serif',opacity=q,anchor='left');line(dst,[(172,393),(172+930*q,393)],p['accent'],3);sub(dst,cfg,p,x=174,y=455,opacity=E(t,.7,1.4),anchor='left');text(dst,'EDIT / STORY',1100,211,17,p['muted'],'mono',anchor='right',opacity=q)
 else:
  text(dst,'01',265,347,140,p['accent'],'serif',opacity=q);line(dst,[(395,239),(395,497)],rgba(p['muted'],110),2);text(dst,s,444,332,fit_size(s,650,64),p['text'],anchor='left',opacity=E(t,.5,1.3));sub(dst,cfg,p,x=444,y=425,opacity=E(t,.8,1.6),anchor='left',width=650);text(dst,'CHAPTER',265,471,19,p['muted'],'mono',opacity=q)

def family_caption(dst,t,cfg,p,v):
 ws=cfg['text'].split() or [''];size=fit_size(cfg['text'],900,76);widths=[measure(s,size)+28 for s in ws];left=640-sum(widths)/2;active=min(len(ws)-1,max(0,int(prog(t,.8,3.7)*len(ws))))
 for k,(s,w) in enumerate(zip(ws,widths)):
  q=E(t,.13+k*.09,.84+k*.09);x=left+w/2
  if v==0:
   if k==active:rr(dst,(left-3,314,left+w-7,407),p['accent'],13)
   text(dst,s,x,362,size,p['bg'] if k==active else p['text'],opacity=q)
  elif v==1:
   z=1+.08*max(0,1-abs(t-(1+k*.45))/.3);text(dst,s,x,358,size,p['accent'] if k<=active else p['muted'],opacity=q,scale=z)
   if k==active:circle(dst,x,438,5,p['accent'])
  elif v==2:
   text(dst,s,x,355,size,p['text'],opacity=q);a=prog(t,.9+k*.45,1.35+k*.45);line(dst,[(left+9,418),(left+9+(w-19)*a,418)],p['accent'],6)
  else:
   rr(dst,(left,309+(1-q)*44,left+w-14,411+(1-q)*44),p['panel'] if k>active else p['accent'],23);text(dst,s,x-7,357+(1-q)*44,size,p['text'] if k>active else p['bg'],opacity=q)
  left+=w
 sub(dst,cfg,p,y=540,opacity=E(t,.8,1.6));stage(dst,p,v)

def family_quote(dst,t,cfg,p,v):
 q=E(t,.15,1.3);ss=chunks(cfg['text'],2)
 if v==0:
  text(dst,'“',226,273,178,p['accent'],'serif',opacity=q);text(dst,cfg['text'],640,358,fit_size(cfg['text'],820,74,'serif'),p['text'],'serif',opacity=E(t,.5,1.4));text(dst,'”',1050,444,150,p['accent'],'serif',opacity=E(t,.65,1.55));sub(dst,cfg,p,y=550,opacity=q)
 elif v==1:
  line(dst,[(180,248),(180,248+252*q)],p['accent'],8)
  for k,s in enumerate(ss):text(dst,s,235,303+k*92,fit_size(s,850,64,'serif'),p['text'],'serif',anchor='left',opacity=E(t,.2+k*.22,1+k*.22))
  sub(dst,cfg,p,x=235,y=536,opacity=q,anchor='left')
 elif v==2:
  for k,s in enumerate(ss):
   z=E(t,.15+k*.2,1.1+k*.2);w=min(940,measure(s,63)+62);rr(dst,(640-w/2,268+k*108,640-w/2+w*z,350+k*108),p['accent'] if k==0 else p['panel'],7);text(dst,s,640,309+k*108,fit_size(s,w-40,63),p['bg'] if k==0 else p['text'],opacity=z)
  sub(dst,cfg,p,y=553,opacity=E(t,.8,1.55))
 else:
  line(dst,[(410,244),(410+460*q,244)],p['accent'],2);text(dst,cfg['text'],640,353,fit_size(cfg['text'],950,80,'serif'),p['text'],'serif',opacity=q);line(dst,[(870,455),(870-460*q,455)],p['accent'],2);text(dst,'•',640,455,26,p['accent'],opacity=q);sub(dst,cfg,p,y=540,opacity=q)

def family_stamp(dst,t,cfg,p,v):
 q=E(t,.15,1.15);s=cfg['text']
 if v==0:
  circle(dst,640,362,151,None,p['accent'],5);circle(dst,640,362,134,None,rgba(p['accent'],150),2);text(dst,s,640,361,fit_size(s,700,74),p['text'],opacity=q,scale=.7+.3*pop(prog(t,.2,1.1)));text(dst,'ORIGINAL / MOTION',640,258,20,p['accent'],'mono',opacity=q);sub(dst,cfg,p,y=557,opacity=q)
 elif v==1:
  rr(dst,(168,288,1112,442),p['panel'],5,p['accent'],2);im=title(cfg,p,size=67,width=820);paste(dst,crop_reveal(im,q,'left'),640,365);line(dst,[(184+914*q,285),(184+914*q,446)],p['accent'],4);text(dst,'LABEL / 001',186,482,18,p['muted'],'mono',anchor='left');sub(dst,cfg,p,y=551,opacity=q)
 elif v==2:
  card=layer(964,220);rr(card,(12,12,952,208),p['panel'],3,p['accent'],2)
  for x in range(12,953,27):circle(card,x,12,7,p['bg']);circle(card,x,208,7,p['bg'])
  for y in range(12,209,27):circle(card,12,y,7,p['bg']);circle(card,952,y,7,p['bg'])
  text(card,s,482,93,fit_size(s,855,73,'serif'),p['text'],'serif');text(card,cfg['subtitle'],482,161,fit_size(cfg['subtitle'],860,22,'sans'),p['muted'],'sans');paste(dst,card,640,373,q,angle=-3*(1-q),scale=.9+.1*q)
 else:
  for k in range(18):
   ang=k*math.pi*2/18;circle(dst,640+math.cos(ang)*142,355+math.sin(ang)*142,26,p['accent'])
  circle(dst,640,355,141,p['accent']);circle(dst,640,355,120,None,p['bg'],3);
  for k,phrase in enumerate(chunks(s,2)):
   text(dst,phrase,640,331+k*52,fit_size(phrase,220,44,'serif'),p['bg'],'serif',opacity=q)
  sub(dst,cfg,p,y=563,opacity=q)

def family_neon(dst,t,cfg,p,v):
 im=title(cfg,p,width=920);q=E(t,.12,1.3);w,h=im.size;cx,cy=640,365
 if v==0:
  tube=text_img(cfg['text'],fit_size(cfg['text'],920,88),(0,0,0,0),'bold',2,p['accent']);glow=tube.filter(ImageFilter.GaussianBlur(9));paste(dst,glow,cx,cy,q);paste(dst,crop_reveal(tube,q,'left'),cx,cy);paste(dst,im,cx,cy,E(t,.95,1.6)*.65)
 elif v==1:
  paste(dst,im.filter(ImageFilter.GaussianBlur(16)),cx,cy,.24*q);paste(dst,im,cx,cy,q);x=cx-w/2+(w+60)*prog(t,.2,2.7);circle(dst,x,cy+h/2+26,9,p['accent']);line(dst,[(cx-w/2,cy+h/2+26),(min(cx+w/2,x),cy+h/2+26)],p['accent'],3)
 elif v==2:
  for k in range(6,0,-1):paste(dst,im,cx-k*25*(1-q),cy+k*13*(1-q),.06*k,scale=1-k*.012*(1-q))
  paste(dst,im,cx,cy,q);line(dst,[(320,453),(960,453)],rgba(p['accent'],130),3)
 else:
  paste(dst,im,cx,cy,q)
  for k in range(16):
   z=prog(t,.15+k*.035,.6+k*.035);ang=k*math.pi*2/16;radius=125+90*z;x=cx+math.cos(ang)*radius*2.3;y=cy+math.sin(ang)*radius*.62;line(dst,[(x,y),(x+math.cos(ang)*18*(1-z),y+math.sin(ang)*18*(1-z))],rgba(p['accent'],220*(1-z)),3)
  rr(dst,(465,455,815,459),p['secondary'],2)
 sub(dst,cfg,p,y=542,opacity=E(t,.8,1.7))

def family_burst(dst,t,cfg,p,v):
 q=E(t,.12,1.15);cx,cy=640,358;d=ImageDraw.Draw(dst)
 if v==0:
  for k in range(24):
   ang=k*math.pi*2/24;r1=190+(1-q)*65;r2=250+(1-q)*125;line(dst,[(cx+math.cos(ang)*r1*1.85,cy+math.sin(ang)*r1*.58),(cx+math.cos(ang)*r2*1.85,cy+math.sin(ang)*r2*.58)],rgba(p['accent'],110*q),3)
 elif v==1:
  for k in range(3):d.ellipse((230-k*25,243-k*15,1050+k*25,473+k*15),outline=rgba(p['accent'],70+k*25),width=2)
  rr(dst,(250,280,1030,432),p['panel'],60)
 elif v==2:
  for k in range(10):
   ang=k*math.pi*2/10;pts=[(cx+math.cos(ang-.08)*220,cy+math.sin(ang-.08)*115),(cx+math.cos(ang)*490*q,cy+math.sin(ang)*195*q),(cx+math.cos(ang+.08)*220,cy+math.sin(ang+.08)*115)];d.polygon(pts,fill=rgba(p['accent'],70))
 else:
  sticker=layer(940,220);rr(sticker,(8,8,932,212),p['accent'],40);text(sticker,cfg['text'],470,110,fit_size(cfg['text'],850,81),p['bg']);paste(dst,sticker,cx,cy,q,scale=.7+.3*pop(prog(t,.1,1)),angle=-4+4*q);sub(dst,cfg,p,y=556,opacity=q);return
 text(dst,cfg['text'],cx,cy,fit_size(cfg['text'],820,81),p['text'],opacity=q,scale=.8+.2*pop(prog(t,.1,1.1)));sub(dst,cfg,p,y=565,opacity=q)

def family_frame(dst,t,cfg,p,v):
 q=E(t,.13,1.28);box=(178,258,1102,466);x0,y0,x1,y1=box
 if v==0:
  pts=[(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)];total=2*((x1-x0)+(y1-y0));remaining=total*q
  for a,b in zip(pts,pts[1:]):
   dist=math.dist(a,b);z=min(1,max(0,remaining/dist));line(dst,[a,(mix(a[0],b[0],z),mix(a[1],b[1],z))],p['accent'],3);remaining-=dist
 elif v==1:
  line(dst,[(x0,250),(mix(x0,x1,q),250)],p['accent'],3);line(dst,[(x1,474),(mix(x1,x0,q),474)],p['secondary'],3);line(dst,[(x0-18,250),(x0-18,mix(250,474,q))],rgba(p['muted'],160),2);line(dst,[(x1+18,474),(x1+18,mix(474,250,q))],rgba(p['muted'],160),2)
 elif v==2:
  for x,y,dx,dy in [(x0,y0,1,1),(x1,y0,-1,1),(x1,y1,-1,-1),(x0,y1,1,-1)]:line(dst,[(x+50*dx*q,y),(x,y),(x,y+50*dy*q)],p['accent'],4)
 else:
  for x in [x0-12,x1+12]:line(dst,[(x,223),(x,497)],rgba(p['muted'],100),1)
  for y in [y0-12,y1+12]:line(dst,[(140,y),(1140,y)],rgba(p['muted'],100),1)
  for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]:rr(dst,(x-7,y-7,x+7,y+7),p['accent'],2)
  line(dst,[(x0,216),(x0+(x1-x0)*q,216)],p['secondary'],2)
 im=title(cfg,p,width=830,size=82);paste(dst,im,640,360,E(t,.45,1.4));sub(dst,cfg,p,y=550,opacity=E(t,.8,1.6))

def family_ribbon(dst,t,cfg,p,v):
 q=E(t,.13,1.25);s=cfg['text'];card=layer(980,160)
 if v==0:
  rr(card,(10,10,970,150),p['accent'],4);text(card,s,490,80,fit_size(s,870,75),p['bg']);paste(dst,card,640,360,q,angle=-7*q,scale=.85+.15*q);sub(dst,cfg,p,y=560,opacity=q)
 elif v==1:
  d=ImageDraw.Draw(dst);d.polygon([(180,310),(290,310),(290,434),(180,434),(207,372)],fill=p['secondary']);d.polygon([(1100,310),(990,310),(990,434),(1100,434),(1073,372)],fill=p['secondary']);rr(dst,(245,288,1035,417),p['accent'],3);d.polygon([(245,417),(290,417),(290,443)],fill=p['muted']);d.polygon([(1035,417),(990,417),(990,443)],fill=p['muted']);text(dst,s,640,353,fit_size(s,710,69),p['bg'],opacity=q);sub(dst,cfg,p,y=545,opacity=q)
 elif v==2:
  rr(dst,(155,293,1125,432),p['panel'],0);im=title(cfg,p,size=78,width=830);paste(dst,im,640+80*(1-q),363,q)
  for k in range(9):line(dst,[(178+k*116,452),(217+k*116,452)],rgba(p['accent'],140),4)
  text(dst,'MESSAGE / ON AIR',176,263,18,p['accent'],'mono',anchor='left',opacity=q);sub(dst,cfg,p,y=548,opacity=q)
 else:
  ss=chunks(s,3);cw=920/len(ss)
  for k,phrase in enumerate(ss):
   z=E(t,.12+k*.2,.95+k*.2);x=180+k*cw;rr(dst,(x,294+(1-z)*60,x+cw-12,430+(1-z)*60),p['accent'] if k==1 else p['panel'],7);text(dst,phrase,x+(cw-12)/2,362+(1-z)*60,fit_size(phrase,cw-34,63),p['bg'] if k==1 else p['text'],opacity=z)
  sub(dst,cfg,p,y=544,opacity=E(t,.8,1.6))

def family_rotate(dst,t,cfg,p,v):
 q=E(t,.14,1.35);ss=chunks(cfg['text'],3);n=len(ss)
 if v==0:
  for k,s in enumerate(ss):
   y=282+k*80;im=text_img(s,fit_size(s,920,70),p['text']);z=E(t,.13+k*.17,1+k*.17);im=im.resize((im.width,max(1,round(im.height*(.08+.92*z)))),Image.Resampling.BICUBIC);paste(dst,im,640,y+(1-z)*35,z)
  for x in (175,1105):line(dst,[(x,237),(x,490)],p['accent'],2)
 elif v==1:
  for k,s in enumerate(ss):
   z=E(t,.16+k*.13,1.15+k*.13);angle=(1-z)*90;im=text_img(s,fit_size(s,650,70),p['text']);paste(dst,im,640,285+k*82,z,angle=angle)
  ImageDraw.Draw(dst).polygon([(175,365),(208,336),(239,365),(208,394)],outline=p['accent'],width=3);ImageDraw.Draw(dst).polygon([(1041,365),(1072,336),(1105,365),(1072,394)],outline=p['accent'],width=3)
 elif v==2:
  phrase=cfg['text'];size=max(13,min(48,int(920/max(1,len(phrase)))));radius=172
  for k,c in enumerate(phrase):
   z=E(t,.12+k*.025,.9+k*.025);angle=k*math.pi*2/max(1,len(phrase))-math.pi/2+(1-q)*1.8;r=radius*(.6+.4*q);x=640+math.cos(angle)*r;y=365+math.sin(angle)*r
   if c.strip():text(dst,c,x,y,size,p['text'],opacity=z,angle=-angle*180/math.pi-90)
  circle(dst,640,365,135,None,rgba(p['accent'],70),2);text(dst,''.join(w[0] for w in phrase.split()[:4]),640,365,52,p['accent'],opacity=q);ImageDraw.Draw(dst).arc((505,230,775,500),int(t*45),int(t*45)+40,fill=p['accent'],width=5)
 else:
  im=layer(1000,192);rr(im,(0,0,999,191),p['panel'],22,p['accent'],2);text(im,cfg['text'],500,96,fit_size(cfg['text'],905,80),p['text']);angle=math.sin(prog(t,.12,1.8)*math.pi*5)*14*(1-E(t,.12,1.8));paste(dst,im,640,365,q,angle=angle);line(dst,[(640,208),(640,268)],rgba(p['muted'],120),3);circle(dst,640,208,7,p['accent'])
 sub(dst,cfg,p,y=579,opacity=E(t,.95,1.8))

def family_paper(dst,t,cfg,p,v):
 q=E(t,.13,1.3);s=cfg['text'];d=ImageDraw.Draw(dst)
 if v==0:
  pts=[(155,282),(1125,282)]+[(1125-i*24,447+(i%3-1)*6) for i in range(41)]+[(155,282)];d.polygon(pts,fill=p['panel']);im=title(cfg,p,size=76,width=860);paste(dst,crop_reveal(im,q,'left'),640,362);sub(dst,cfg,p,y=548,opacity=q)
 elif v==1:
  rr(dst,(188,271,1092,445),p['panel'],6)
  for x,a in ((190,-12),(1090,12)):
   tape=layer(146,42);rr(tape,(0,0,145,41),rgba(p['secondary'],140),1);paste(dst,tape,x,272,q,angle=a)
  text(dst,s,640,357,fit_size(s,820,76),p['text'],opacity=E(t,.4,1.4));sub(dst,cfg,p,y=550,opacity=q)
 elif v==2:
  rr(dst,(165,274,1115,445),p['panel'],3);fold=110*(1-q);d.polygon([(1115-fold,274),(1115,274+fold),(1115-fold,274+fold)],fill=p['secondary']);im=title(cfg,p,size=75,width=850);paste(dst,mask(im,lambda dd,w,h:dd.rectangle((0,0,w*q,h),fill=255)),640,360);sub(dst,cfg,p,y=550,opacity=q)
 else:
  ss=chunks(s,3)
  for k,phrase in enumerate(ss):
   z=E(t,.14+k*.2,1+k*.2);x=255+k*355;rr(dst,(x-115,260+30*k+(1-z)*70,x+145,417+30*k+(1-z)*70),p['panel'],8,p['secondary'],2);rr(dst,(x-115,247+30*k+(1-z)*70,x-25,270+30*k+(1-z)*70),p['accent'],4);text(dst,phrase,x+15,338+30*k+(1-z)*70,fit_size(phrase,235,59),p['text'],opacity=z)
  sub(dst,cfg,p,y=558,opacity=E(t,.95,1.8))

def family_cinema(dst,t,cfg,p,v):
 q=E(t,.14,1.5);im=title(cfg,p,size=87,width=970);w,h=im.size
 if v==0:
  paste(dst,im,640,365,q);rr(dst,(120,228,1160,365-80*q),p['bg'],0);rr(dst,(120,365+80*q,1160,502),p['bg'],0);line(dst,[(180,228),(1100,228)],rgba(p['accent'],90),2);line(dst,[(180,502),(1100,502)],rgba(p['accent'],90),2)
 elif v==1:
  r=mask(im,lambda d,w,h:d.rectangle((w*(1-q)/2,0,w*(1+q)/2,h),fill=255));paste(dst,r,640,365);beam=layer(1080,8);rr(beam,(0,0,1079,7),rgba(p['accent'],150),3);paste(dst,beam,640,450,q);paste(dst,beam.filter(ImageFilter.GaussianBlur(10)),640,450,q)
 elif v==2:
  for k in range(10,0,-1):paste(dst,title(cfg,p,size=87,width=970,color=p['accent']),640+k*3,365+k*3,.08*q)
  paste(dst,im,640,365,q,scale=1.1-.1*q);line(dst,[(435,462),(845,462)],p['secondary'],2)
 else:
  blur=14*(1-q);paste(dst,im.filter(ImageFilter.GaussianBlur(blur)),640,365,q,scale=1.18-.18*q);line(dst,[(150,260),(200,260),(200,294)],rgba(p['accent'],130),2);line(dst,[(1130,470),(1080,470),(1080,436)],rgba(p['accent'],130),2)
 sub(dst,cfg,p,y=566,opacity=E(t,1,1.9))

def family_shape(dst,t,cfg,p,v):
 q=E(t,.13,1.4);im=title(cfg,p,size=81,width=910);w,h=im.size
 if v==0:
  radius=max(w,h)*.6*q;r=mask(im,lambda d,w,h:d.ellipse((w/2-radius,h/2-radius,w/2+radius,h/2+radius),fill=255));paste(dst,r,640,364);circle(dst,640,364,126,None,rgba(p['accent'],95),2)
 elif v==1:
  a=w*q*.62;b=max(h,w*.4)*q;r=mask(im,lambda d,w,h:d.polygon([(w/2-a,h/2),(w/2,h/2-b),(w/2+a,h/2),(w/2,h/2+b)],fill=255));paste(dst,r,640,364);ImageDraw.Draw(dst).polygon([(210,364),(640,230),(1070,364),(640,498)],outline=rgba(p['accent'],90),width=2)
 elif v==2:
  ss=chunks(cfg['text'],3)
  for k,s in enumerate(ss):
   z=E(t,.14+k*.18,1+k*.18);x=310+k*330;d=ImageDraw.Draw(dst);d.polygon([(x-140,290),(x+130,290),(x+150,425),(x-120,425)],fill=p['panel']);text(dst,s,x,357,fit_size(s,235,55),p['text'],opacity=z);line(dst,[(x-120,442),(x-120+245*z,442)],p['accent'],3)
 else:
  def wave(d,w,h):
   points=[(0,h),(w,h)]+[(x,h*(1-q)+math.sin(x*.025+t*4)*12*(1-q)) for x in range(w,-1,-8)];d.polygon(points,fill=255)
  paste(dst,mask(im,wave),640,364);pts=[(180+i*16,457+math.sin(i*.18+t*1.2)*5) for i in range(58)];line(dst,pts,p['accent'],3)
 sub(dst,cfg,p,y=568,opacity=E(t,.9,1.7))

def family_score(dst,t,cfg,p,v):
 q=E(t,.15,1.3);s=cfg['text']
 if v==0:
  text(dst,'01',265,352,144,p['accent'],'mono',opacity=q);line(dst,[(404,254),(404,457)],rgba(p['muted'],100),2);text(dst,s,454,322,fit_size(s,635,68),p['text'],anchor='left',opacity=E(t,.4,1.3));sub(dst,cfg,p,x=454,y=407,opacity=q,anchor='left',width=635);rr(dst,(454,466,454+630*q,474),p['accent'],3)
 elif v==1:
  for k,w in enumerate(chunks(s,3)):
   z=E(t,.15+k*.18,1+k*.18);y=282+k*103;rr(dst,(182,y-34,1098,y+43),p['panel'],12);text(dst,'0'+str(k+1),225,y+3,28,p['accent'],'mono',opacity=z);text(dst,w,300,y+2,fit_size(w,740,49),p['text'],anchor='left',opacity=z)
  sub(dst,cfg,p,y=593,opacity=q)
 elif v==2:
  rr(dst,(180,248,1100,482),p['panel'],15,rgba(p['muted'],100));line(dst,[(380,248),(380,482)],rgba(p['muted'],100),2);text(dst,'TITLE',280,309,20,p['accent'],'mono',opacity=q);text(dst,'KEY',280,415,20,p['accent'],'mono',opacity=q);line(dst,[(180,362),(1100,362)],rgba(p['muted'],80),2);text(dst,s,420,307,fit_size(s,640,62),p['text'],anchor='left',opacity=q);sub(dst,cfg,p,x=420,y=417,opacity=E(t,.6,1.5),anchor='left',width=640)
 else:
  elapsed=min(60,int(prog(t,.18,1.5)*60));text(dst,f'{elapsed//60:02}:{elapsed%60:02}',640,271,57,p['accent'],'mono',opacity=q);text(dst,s,640,375,fit_size(s,960,79),p['text'],opacity=q);rr(dst,(340,455,940,462),rgba(p['muted'],100),3);rr(dst,(340,455,340+600*prog(t,.2,3.8),462),p['accent'],3);sub(dst,cfg,p,y=550,opacity=q)

def family_space(dst,t,cfg,p,v):
 q=E(t,.14,1.35);ss=chunks(cfg['text'],3);n=len(ss)
 if v==0:
  for k,s in enumerate(ss):text(dst,s,320+k*220,282+k*84,fit_size(s,570,67),p['text'],opacity=E(t,.15+k*.2,1+k*.2));line(dst,[(200,450),(1030,514)],rgba(p['accent'],90),3)
 elif v==1:
  ss=chunks(cfg['text'],2);line(dst,[(640,232),(640,484)],p['accent'],3)
  for k,s in enumerate(ss):text(dst,s,405+k*475,359,fit_size(s,420,76),p['text'],opacity=E(t,.2+k*.3,1.1+k*.3));circle(dst,640,358,10,p['accent'])
 elif v==2:
  for k,s in enumerate(ss):
   z=E(t,.13+k*.16,1.1+k*.16);h=126+k*24;x=188+k*310;rr(dst,(x,445-h*z,x+285,445),p['panel'],3,p['secondary'],2);text(dst,s,x+142,405-h/2+35*(1-z),fit_size(s,248,56),p['text'],opacity=z)
  line(dst,[(160,467),(1120,467)],p['accent'],3)
 else:
  positions=[(335,279),(925,352),(465,439)]
  for k,(s,(x,y)) in enumerate(zip(ss,positions)):
   z=E(t,.16+k*.18,1+k*.18);text(dst,s,x+(1-z)*35,y,fit_size(s,520,65),p['text'],opacity=z);line(dst,[(x-155,y+51),(x+155,y+51)],rgba(p['accent'],110),2);text(dst,f'X/{k+1:02}',x-155,y-55,16,p['muted'],'mono',anchor='left',opacity=z)
 sub(dst,cfg,p,y=581,opacity=E(t,.95,1.8))

def family_callout(dst,t,cfg,p,v):
 q=E(t,.13,1.3);s=cfg['text']
 if v==0:
  circle(dst,270,358,13,p['accent']);circle(dst,270,358,35,None,rgba(p['accent'],90),2);line(dst,[(270,358),(360,294),(1055,294)],p['accent'],3);text(dst,s,411,358,fit_size(s,660,69),p['text'],anchor='left',opacity=q);sub(dst,cfg,p,x=411,y=450,opacity=E(t,.6,1.5),anchor='left',width=660)
 elif v==1:
  circle(dst,330,345,89,p['panel'],p['accent'],3);line(dst,[(394,409),(447,462)],p['accent'],12);text(dst,s[:1],330,345,100,p['accent'],'serif',opacity=q);text(dst,s,500,332,fit_size(s,605,68),p['text'],anchor='left',opacity=q);sub(dst,cfg,p,x=500,y=430,opacity=q,anchor='left',width=605)
 elif v==2:
  ss=chunks(s,3);cx,cy=640,362;circle(dst,cx,cy,23,p['accent'])
  pos=[(365,244),(921,312),(365,467)]
  for k,(w,(x,y)) in enumerate(zip(ss,pos)):
   z=E(t,.2+k*.2,1.1+k*.2);line(dst,[(cx,cy),(mix(cx,x,z),mix(cy,y,z))],rgba(p['accent'],140),2);rr(dst,(x-210,y-37,x+210,y+37),p['panel'],12);text(dst,w,x,y,fit_size(w,380,52),p['text'],opacity=z)
  sub(dst,cfg,p,y=568,opacity=q)
 else:
  rr(dst,(173,288,1107,438),p['panel'],17,p['accent'],2);rr(dst,(173,288,190,438),p['accent'],6);d=ImageDraw.Draw(dst);d.polygon([(265,318),(233,393),(297,393)],outline=p['accent'],width=3);text(dst,'!',265,369,35,p['accent']);text(dst,s,330,355,fit_size(s,720,71),p['text'],anchor='left',opacity=q);sub(dst,cfg,p,y=546,opacity=q)

def family_cadence(dst,t,cfg,p,v):
 q=E(t,.13,1.25);s=cfg['text']
 if v==0:
  text(dst,'WHY?',640,251,52,p['accent'],opacity=q);line(dst,[(555,307),(725,307)],p['accent'],3);text(dst,s,640,387,fit_size(s,930,82),p['text'],opacity=E(t,.8,1.7));sub(dst,cfg,p,y=561,opacity=E(t,1.2,2.0))
 elif v==1:
  text(dst,'BEFORE',325,252,20,p['muted'],'mono',opacity=q);text(dst,'AFTER',955,252,20,p['accent'],'mono',opacity=E(t,.65,1.5));text(dst,cfg['subtitle'],325,359,fit_size(cfg['subtitle'],410,41),p['muted'],opacity=q);text(dst,s,955,359,fit_size(s,410,65),p['text'],opacity=E(t,.7,1.55));arrow(dst,640,360,p['accent'],2);line(dst,[(180,447),(510,447)],rgba(p['muted'],90),2);line(dst,[(770,447),(1100,447)],p['accent'],3)
 elif v==2:
  ss=chunks(s,3)
  for k,w in enumerate(ss):
   z=E(t,.15+k*.3,1+k*.3);y=282+k*100;circle(dst,226,y,17,p['accent']);line(dst,[(219,y),(225,y+6),(235,y-7)],p['bg'],3);text(dst,w,285,y,fit_size(w,770,62),p['text'],anchor='left',opacity=z)
  sub(dst,cfg,p,y=591,opacity=E(t,1,1.9))
 else:
  im=layer(950,176);rr(im,(0,0,949,175),p['accent'],28);text(im,s,440,88,fit_size(s,750,79),p['bg']);arrow(im,867,88,p['bg'],2);paste(dst,im,640,361,q,scale=.84+.16*pop(prog(t,.1,1.1)));line(dst,[(525,482),(755,482)],rgba(p['muted'],100),2);sub(dst,cfg,p,y=548,opacity=q)

FAMILIES=[family_mask,family_split,family_letter,family_outline,family_writer,
 family_cards,family_scale,family_glitch,family_lower,family_editorial,
 family_caption,family_quote,family_stamp,family_neon,family_burst,
 family_frame,family_ribbon,family_rotate,family_paper,family_cinema,
 family_shape,family_score,family_space,family_callout,family_cadence]

def render(pid,t,cfg):
 if pid not in PRESETS:raise ValueError('Unknown premium typography preset '+pid)
 n=int(pid[2:])-1;g,v=divmod(n,4);p=palette(cfg);dst=base(cfg);content=layer()
 # Tempo changes choreography pace while exit remains synchronized to the scene clock.
 tempo=float(cfg.get('tempo',1));clock=t*tempo
 FAMILIES[g](content,clock,cfg,p,v)
 paste(dst,content,0,0,opacity=O(t),anchor='top-left')
 return dst

PRESETS=json.loads((Path(__file__).parent/'premium_type_index.json').read_text())
