"""53 original geometric motion studies adapted from the guide names.
Camera/3D studies use projected 2.5D illustrations, not a 3D engine.
Each entry has its own temporal and visual mechanism. No source videos copied.
"""
from core import *
import json
INDEX=json.load(open(Path(__file__).with_name('guide_index.json')))
MECHANISMS=[
'Projected cube rotates in a grounded scene; 2.5D interpretation',
'Rapid camera scale punch followed by spring recovery',
'Cursor flies across perspective tiles with hover state changes',
'Three independently translated and scaled depth planes',
'Close camera traces across faces of a projected product box; 2.5D interpretation',
'Top down camera orbit over connected workspace tiles',
'Camera travels through a field of projected stars and panels',
'Perspective camera tilt decreases during a diagonal glide',
'Slow camera approach with accelerating tremor and release',
'Perspective terminal rotates as commands type; 2.5D interpretation',
'Avatar grid builds by radial distance then changes color',
'Draggable comparison divider scrubs two interface states',
'Line chart grows live with a tracking readout',
'Counter eases to its target then emits ballistic confetti',
'Gauge needle rotates to target with numerical readout',
'Diagonal hatch progressively reveals extruded bars',
'Clipped odometer reels roll independently into alignment',
'Particles burst at sequential target collisions',
'Discrete sand grains settle to form a filled vessel',
'Scrolling list decelerates and locks to a selected row',
'Camera tracks an expanding horizontal timeline',
'Card assembles from four quadrants before typing starts',
'Blended aurora fields bloom while central face flips',
'Four frame corners snap inward and lock onto content',
'Dashboard focus pill traverses three metrics with glow',
'Rotating HUD arcs acquire a moving target',
'Bright packet traverses bent communication paths',
'Performance icon morphs from idle bars into active tick',
'Button impact compresses surface and emits feedback ring',
'Moving light streak crosses beveled card and edge highlights',
'Hand drawn outlines redraw with frame dependent jitter',
'Phone emits delayed radial rings and floating chips',
'Offset spot color print layers stamp into registration',
'Brackets close around object while horizontal scan sweeps',
'Scan line finds three areas then annotations unfurl',
'Alternating scan strips fly from opposite sides to assemble',
'Heavy slab drops with squash and rebound debris',
'Spotlight traverses dark surface revealing concealed content',
'User prompt precedes streaming response with blinking caret',
'Gap control changes spacing across a live layout',
'Canvas strokes draw sequentially and become solid cards',
'One chip is selected while other grid entries black out',
'Topic chip lifts from grid into a user identity pill',
'Three collaborator cursors independently manipulate geometry',
'Command palette scales up and filters highlighted command',
'Dictation waveform converts into typed glass pill text',
'Hashtag text resolves into a rounded topic pill',
'Input completes, cursor triggers submit and results appear',
'Carousel slides through features and enlarges selected card',
'Segmented thumb slides between tabs with hero content change',
'Theme toggle moves and crossfades background and surfaces',
'Search query types while unmatched rows collapse',
'Voice waveform uses phase offset live amplitudes and playhead',
]
PRESETS={}
for i,m in enumerate(MECHANISMS,1):
 pid=f'PV{i:03d}'; z=INDEX[pid]
 PRESETS[pid]={**z,'genre':'saas','text':z['name'].replace('-',' ').title(),'subtitle':'Original guide adaptation','family':'guide','duration':6,'adaptation_status':'original-demo','mechanism':m,'category':('Camera and depth' if i<=10 else 'Data and comparison' if i<=21 else 'Visual effects' if i<=38 else 'UI interaction')}

def txt(im,s,x,y,p,size=26,color=None,anchor='center',opacity=1):
 text(im,s,x,y,fit_size(s,1000,size),color or p['text'],anchor=anchor,opacity=opacity)
def card(p,w=400,h=230,title='WORKSPACE',value='Ready',seed=0):
 im=layer(w,h);rr(im,(2,2,w-2,h-2),p['panel'],24,p['muted'],2)
 txt(im,title,28,36,p,20,anchor='left');line(im,[(24,67),(w-24,67)],rgba(p['muted'],65),2)
 txt(im,value,28,110,p,34,p['accent'],anchor='left')
 for j in range(3):rr(im,(28,150+j*19,28+(w-65)*(0.85-j*.17),158+j*19),rgba(p['muted'],90),4)
 return im

def cursor(im,x,y,p,label=None,color=None):
 c=color or p['accent'];ImageDraw.Draw(im).polygon([(x,y),(x+4,y+31),(x+12,y+20),(x+25,y+18)],fill=c)
 if label:rr(im,(x+15,y+29,x+110,y+60),c,8);txt(im,label,x+62,y+44,p,15,p['bg'])
def cube(im,cx,cy,size,a,p):
 # Orthographic projected 2.5D cube; rotate around vertical axis.
 v=[]
 for x,y,z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
  xx=x*math.cos(a)+z*math.sin(a); zz=-x*math.sin(a)+z*math.cos(a)
  v.append((cx+xx*size*.7,cy+y*size*.64+zz*size*.25,zz))
 faces=[([0,1,2,3],p['panel']),([4,5,6,7],p['accent']),([0,4,7,3],p['secondary']),([1,5,6,2],p['secondary']),([0,1,5,4],p['text'])]
 for ids,col in sorted(faces,key=lambda f:sum(v[k][2] for k in f[0])):
  pts=[v[k][:2] for k in ids];ImageDraw.Draw(im).polygon(pts,fill=col);line(im,pts+[pts[0]],p['bg'],3)

def chart(im,p,x=300,y=500,w=660,h=280,q=1):
 line(im,[(x,y-h),(x,y),(x+w,y)],p['muted'],2)
 vals=[.13,.26,.20,.47,.40,.73,.68,.92]
 pts=[(x+j*w/7,y-v*h) for j,v in enumerate(vals)]
 n=q*7;k=int(n);k=min(k,6);partial=pts[:k+1]+[(mix(pts[k][0],pts[k+1][0],n-k),mix(pts[k][1],pts[k+1][1],n-k))]
 line(im,partial,p['accent'],5);circle(im,*partial[-1],8,p['text']);return partial[-1]

def render(pid,t,cfg=None):
 cfg=cfg or {};p=palette(cfg);im=base(cfg);i=int(pid[2:]);u=clamp(t/5);e=ease(prog(t,.3,1.3));
 # All guides share captions only; motion scene and temporal behavior are distinct.
 title=cfg.get('text',PRESETS[pid]['text']);txt(im,title,640,63,p,32)
 txt(im,cfg.get('subtitle',PRESETS[pid]['mechanism']),640,664,p,17,p['muted'])
 if i==1:
  ImageDraw.Draw(im).ellipse((360,486,920,566),fill=rgba(p['accent'],28));cube(im,640,345,145*e,.45+t*.40,p)
  for k in range(5):line(im,[(340+k*130,565),(470+k*80,485)],rgba(p['muted'],65),2)
 elif i==2:
  q=prog(t,.8,1.22);z=1+1.9*math.exp(-((t-1.25)/.24)**2)+.1*math.sin(t*8)*math.exp(-max(0,t-1.3)*2)
  scene=card(p,460,260,'LAUNCH','Impact');paste(im,scene,640+8*math.sin(t*14)*q,355,scale=z*.84)
  if 1<t<1.6:line(im,[(150,180),(420,285)],p['accent'],7);line(im,[(1100,540),(875,415)],p['accent'],7)
 elif i==3:
  for k in range(4):
   x=245+k*250;hover=abs(x-(220+840*u))<130
   c=card(p,205,180,'MODULE '+str(k+1),'Active' if hover else 'Ready');paste(im,c,x,360-(20 if hover else 0),scale=1+(0.08 if hover else 0),angle=-5)
  cursor(im,220+840*u,300+75*math.sin(u*math.pi*2),p,'Explore')
 elif i==4:
  for k in range(3):
   a=card(p,400,220,['BACKGROUND','MIDDLE','FOREGROUND'][k],str(k+1))
   paste(im,a,640+(k-1)*215+(k+1)*45*math.sin(t*.8),360+(k-1)*48,opacity=.55+.2*k,scale=.65+.19*k)
 elif i==5:
  scene=layer();cube(scene,640,340,180,.5+t*.19,p)
  crop=scene.crop((280,120,1000,610));paste(im,crop,640+95*math.sin(t*.9),352,scale=1.0+.32*math.sin(u*math.pi))
  tag(im,'FACE '+str(1+int(u*2.99)),100,570,p)
 elif i==6:
  for k in range(8):
   a=k*math.pi/4+t*.17;x=640+240*math.cos(a);y=350+170*math.sin(a)
   line(im,[(640,350),(x,y)],rgba(p['muted'],100),2);paste(im,card(p,145,110,str(k+1),'Tile'),x,y,angle=math.degrees(a)+90,scale=.8)
  circle(im,640,350,55,p['accent']);txt(im,'HUB',640,350,p,25,p['bg'])
 elif i==7:
  for k in range(56):
   ang=k*2.3999;dep=((k*.137+t*.22)%1);r=40+dep*480;x=640+math.cos(ang)*r;y=350+math.sin(ang)*r*.58
   circle(im,x,y,1+dep*3,rgba(p['text'],90+160*dep))
  for k in range(3):
   z=((k/3+t*.13)%1);paste(im,card(p,260,170,'NODE '+str(k),'Connected'),640+math.sin(k*2)*z*460,350+math.cos(k*2)*z*170,scale=.12+z,opacity=z)
 elif i==8:
  src=card(p,630,350,'PROJECTED CANVAS','Tilt glide');q=smooth(u);dx=mix(-110,100,q)
  quad=[(360+dx,210),(915+dx,160+100*q),(960+dx,505),(280+dx,510-50*q)]
  im.alpha_composite(warp_quad(src,quad))
 elif i==9:
  tension=prog(t,.7,3.5);shake=math.sin(t*39)*tension*9*(1-prog(t,3.5,4.0));z=.65+tension*.55
  paste(im,card(p,510,280,'SYSTEM CHECK','Released' if t>3.6 else 'Building tension'),640+shake,350+shake*.4,scale=z)
  for k in range(4):line(im,[(260+k*15,200),(260+k*15,510)],rgba(p['accent'],int(120*tension)),2)
 elif i==10:
  src=layer(680,350);rr(src,(2,2,678,348),p['panel'],15,p['accent']);commands=['$ initialize scene','$ load motion module','$ render --preview','> operation complete']
  for k,s in enumerate(commands):txt(src,s[:int(prog(t,k*.7+.3,k*.7+1.0)*len(s))],30,68+k*64,p,24,p['accent'],anchor='left')
  wob=math.sin(t*.65)*45;quad=[(310,185+wob),(970,145),(1010,515-wob),(275,555)];im.alpha_composite(warp_quad(src,quad))
 elif i==11:
  for r in range(5):
   for c in range(9):
    d=math.hypot(c-4,r-2);a=enter(t,.15+d*.14,.6+d*.14);col=p['secondary'] if t<2.1+d*.13 else p['accent']
    x=360+c*70;y=215+r*70;circle(im,x,y,23*a,rgba(col,220*a));circle(im,x,y-5,7*a,p['bg']);rr(im,(x-12*a,y+5*a,x+12*a,y+14*a),p['bg'],7)
 elif i==12:
  left=card(p,740,340,'BEFORE','Manual workflow');right=card(p,740,340,'AFTER','Automated workflow');divider=int(740*(.12+.76*(.5-.5*math.cos(t*1.05))))
  left.paste(right.crop((0,0,divider,340)),(0,0));paste(im,left,640,360);x=270+divider
  line(im,[(x,185),(x,540)],p['accent'],4);circle(im,x,360,24,p['accent']);txt(im,'<>',x,359,p,22,p['bg']);cursor(im,x+12,398,p)
 elif i==13:
  x,y=chart(im,p,q=prog(t,.3,4.2));tag(im,str(int(1200*prog(t,.3,4.2)))+' units',x-40,y-35,p)
  txt(im,'LIVE GROWTH',310,175,p,22,anchor='left')
 elif i==14:
  q=ease(prog(t,.2,2.8));txt(im,str(round(10000*q)),640,342,p,108,p['accent']);txt(im,'milestone reached',640,446,p,26)
  for k in range(65):
   a=k*2.3999;v=150+(k%7)*38;dt=max(0,t-2.8);x=640+math.cos(a)*v*dt;y=330+math.sin(a)*v*dt+100*dt*dt
   if dt:rr(im,(x,y,x+8,y+15),p['accent'] if k%2 else p['secondary'],1)
 elif i==15:
  d=ImageDraw.Draw(im);d.arc((410,155,870,615),180,360,fill=p['muted'],width=28);q=ease(prog(t,.3,3));ang=math.pi+q*math.pi*.83
  d.arc((410,155,870,615),180,180+q*150,fill=p['accent'],width=28);line(im,[(640,385),(640+180*math.cos(ang),385+180*math.sin(ang))],p['text'],7);circle(im,640,385,16,p['accent']);txt(im,str(round(83*q))+'%',640,485,p,54)
 elif i==16:
  for k,h in enumerate([95,180,260,340]):
   x=340+k*145;y=560;hh=h*ease(prog(t,.2+k*.25,1.8+k*.25));ImageDraw.Draw(im).polygon([(x,y),(x+85,y),(x+110,y-20),(x+110,y-hh-20),(x+85,y-hh),(x,y-hh)],fill=p['panel'])
   rr(im,(x,y-hh,x+85,y),p['secondary'],1)
   for j in range(0,math.ceil(hh),17):line(im,[(x,y-j),(x+85,min(y,y-j+55))],p['accent'],2)
   txt(im,str(h),x+45,y+32,p,21)
 elif i==17:
  target='12850';q=prog(t,.2,3.8)
  for k,ch in enumerate(target):
   reel=layer(115,160);rr(im,(337+k*121,267,452+k*121,437),p['panel'],14)
   z=(int(ch)+20)*(1-ease(clamp(q*1.3-k*.06)));num=int(ch)+int(z);off=(z%1)*140
   for j in [-1,0,1]:txt(reel,str((num+j)%10),57,80+off+j*140,p,83,p['accent'])
   paste(im,reel,394+k*121,352)
 elif i==18:
  for k in range(3):
   x=360+k*280;dt=t-.8-k*.8;circle(im,x,370,35,p['panel'],p['accent'],3)
   if dt>0:
    txt(im,'✓',x,370,p,30,p['accent'])
    for j in range(20):a=j*math.pi/10;r=max(0,dt)*110;circle(im,x+math.cos(a)*r,370+math.sin(a)*r+dt*dt*22,3,rgba(p['accent'],255*max(0,1-dt/2)))
   if -.7<dt<0:circle(im,x,370+dt*210,15,p['text'])
 elif i==19:
  rr(im,(470,190,810,555),None,14,p['muted'],4);q=prog(t,.2,4.0)
  for k in range(600):
   born=(k/600)*3.8+.2
   if t>=born:
    targety=546-(k//55)*12;targetx=480+(k*47%318);fall=clamp((t-born)/.55);y=mix(200,targety,fall*fall);circle(im,targetx,y,3,p['accent'] if k%3 else p['secondary'])
  txt(im,str(round(q*100))+'% filled',640,590,p,25)
 elif i==20:
  vp=layer(580,370);q=1-math.exp(-max(0,t-.25)*1.45);offset=600*q
  for k in range(12):
   y=60+k*90-offset;selected=k==7;rr(vp,(12,y-34,568,y+34),p['accent'] if selected else p['panel'],13);txt(vp,'Result '+str(k+1),45,y,p,25,p['bg'] if selected else p['text'],anchor='left')
  paste(im,vp,640,360);line(im,[(365,393),(915,393)],p['secondary'],2);tag(im,'BRAKE / LOCK',490,580,p)
 elif i==21:
  q=smooth(prog(t,.2,4.4));offset=800*q
  line(im,[(100,390),(1180,390)],p['muted'],4)
  for k in range(7):
   x=400+k*235-offset
   if 100<x<1180:circle(im,x,390,14,p['accent']);txt(im,str(2024+k),x,450,p,29);txt(im,['Idea','Build','Test','Launch','Grow','Scale','Next'][k],x,330,p,25)
  line(im,[(640,225),(640,525)],p['secondary'],2)
 elif i==22:
  src=card(p,620,320,'ASSEMBLED','');q=ease(prog(t,.2,1.5))
  for k,(a,b) in enumerate([(0,0),(310,0),(0,160),(310,160)]):
   tile=src.crop((a,b,a+310,b+160));paste(im,tile,330+a+155+(1-q)*(-250 if a==0 else 250),200+b+80+(1-q)*(-160 if b==0 else 160),opacity=q)
  s=cfg.get('sample_text','Build once. Reuse everywhere.');txt(im,s[:int(prog(t,1.65,3.8)*len(s))],360,349,p,29,p['accent'],anchor='left')
 elif i==23:
  glow=layer()
  for k in range(7):
   x=180+k*160+65*math.sin(t+k);y=340+100*math.sin(k+t*.7);circle(glow,x,y,130,p['accent'] if k%2 else p['secondary'])
  glow=glow.filter(ImageFilter.GaussianBlur(75));paste(im,glow,640,360,opacity=.42)
  a=(t*.7)%math.pi;scale=max(.025,abs(math.cos(a)));face=card(p,450,220,'AURORA', 'Reveal' if math.cos(a)>0 else 'Bloom');face=face.resize((max(1,int(face.width*scale)),face.height));paste(im,face,640,360)
 elif i==24:
  paste(im,card(p,500,270,'BRAND','Focused'),640,355,opacity=e)
  q=pop(prog(t,.1,1.25));w=mix(900,550,q);h=mix(440,320,q)
  for sx,sy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
   x=640+sx*w/2;y=355+sy*h/2;line(im,[(x-sx*55,y),(x,y),(x,y-sy*55)],p['accent'],8)
 elif i==25:
  centers=[360,640,920]
  for k,x in enumerate(centers):paste(im,card(p,240,220,['USERS','REVENUE','RETENTION'][k],['12.8K','RM50K','89%'][k]),x,360)
  q=clamp((t-.3)/3.8)*2;k=min(1,int(q));x=mix(centers[k],centers[k+1],smooth(q-k));gl=layer();rr(gl,(x-124,245,x+124,475),rgba(p['accent'],130),30);gl=gl.filter(ImageFilter.GaussianBlur(17));im.alpha_composite(gl);rr(im,(x-126,243,x+126,477),None,28,p['accent'],3)
 elif i==26:
  d=ImageDraw.Draw(im)
  for k,r in enumerate([100,155,220]):d.arc((640-r,350-r,640+r,350+r),t*45+k*75,t*45+k*75+235,fill=p['accent'] if k%2 else p['secondary'],width=3)
  x=640+math.sin(t*.8)*85;y=350+math.cos(t*.9)*60;line(im,[(x-35,y),(x+35,y)],p['text'],2);line(im,[(x,y-35),(x,y+35)],p['text'],2);txt(im,'TARGET '+str(round(100*e))+'%',640,595,p,24)
 elif i==27:
  paths=[[(240,260),(470,260),(620,360),(1000,360)],[(240,480),(520,480),(690,360),(1000,360)]]
  for k,pts in enumerate(paths):
   line(im,pts,p['muted'],3);phase=(t*.45+k*.5)%1;seg=phase*3;j=min(2,int(seg));x=mix(pts[j][0],pts[j+1][0],seg-j);y=mix(pts[j][1],pts[j+1][1],seg-j)
   for r in range(25,0,-4):circle(im,x,y,r,rgba(p['accent'],15))
   circle(im,x,y,6,p['text']);circle(im,*pts[0],16,p['secondary'])
  circle(im,1000,360,42,p['accent']);txt(im,'SYNC',1000,435,p,25)
 elif i==28:
  q=prog(t,1.7,2.8)
  for k in range(5):h=(80+45*math.sin(t*5+k))*(1-q);rr(im,(480+k*63,440-h,510+k*63,440),p['secondary'],14)
  check=[(500,360),(595,440),(785,240)];line(im,check[:2] if q<.5 else check,p['accent'],max(1,round(15*q)));txt(im,'Complete' if q>.8 else 'Processing',640,545,p,30)
 elif i==29:
  dt=t-1.7;squash=1-.22*math.exp(-dt*dt/.03);bt=card(p,390,140,'ACTION','Saved' if dt>0 else 'Save');paste(im,bt,640,360,scale=squash)
  cursor(im,690,410-40*ease(prog(t,.3,1.6)),p)
  if dt>0:circle(im,640,360,75+150*dt,None,rgba(p['accent'],max(0,255*(1-dt/1.1))),4)
 elif i==30:
  src=card(p,600,320,'LIGHT PLAY','Reflective surface');paste(im,src,640,360)
  shimmer=layer(600,320);x=-180+t*170;ImageDraw.Draw(shimmer).polygon([(x,0),(x+75,0),(x+230,320),(x+145,320)],fill=rgba(p['text'],80));paste(im,shimmer,640,360)
  line(im,[(345,202),(935,202)],rgba(p['accent'],150+80*math.sin(t*2)),3)
 elif i==31:
  f=int(t*12)
  for k in range(5):
   pts=[]
   for j in range(70):a=j*2*math.pi/69;r=95+k*29+3*math.sin(j*7+f*4+k);pts.append((640+math.cos(a)*r*1.5,350+math.sin(a)*r))
   line(im,pts,p['accent'] if k%2 else p['secondary'],2)
  txt(im,'DRAW / REDRAW',640,350,p,29)
 elif i==32:
  rr(im,(548,190,732,540),p['panel'],32,p['muted'],3);rr(im,(602,203,678,216),p['bg'],5)
  for k in range(4):
   phase=(t*.38-k*.23)%1;circle(im,640,365,40+phase*230,None,rgba(p['accent'],180*(1-phase)),3)
   a=k*math.pi/2+.4;x=640+math.cos(a)*270;y=365+math.sin(a)*155;rr(im,(x-78,y-22,x+78,y+22),p['panel'],22,p['accent']);txt(im,['Fast','Smart','Secure','Simple'][k],x,y,p,20)
 elif i==33:
  q=pop(prog(t,.15,1.0));offset=35*(1-ease(prog(t,1.2,2.5)))
  for k in range(3):
   col=[p['accent'],p['secondary'],p['text']][k];x=640+(k-1)*offset;y=350+(k-1)*offset*.6
   for j in range(120):
    dx=(j%20-9.5)*22;dy=(j//20-2.5)*24;circle(im,x+dx*q,y+dy*q,3,col)
   text(im,'PRINT',x,y,90,col,opacity=.5)
 elif i==34:
  paste(im,card(p,420,260,'OBJECT','Scan ready'),640,355)
  q=ease(prog(t,.3,1.5));half=mix(420,230,q)
  for sx,sy in [(-1,-1),(1,-1),(-1,1),(1,1)]:x=640+sx*half;y=355+sy*(half*.62);line(im,[(x-sx*32,y),(x,y),(x,y-sy*32)],p['accent'],5)
  sy=235+(t*.55%1)*240;line(im,[(415,sy),(865,sy)],p['accent'],4)
 elif i==35:
  paste(im,card(p,570,300,'ANALYSIS','Detecting elements'),590,345)
  sy=210+clamp(t/2.4)*270;line(im,[(300,sy),(900,sy)],p['accent'],3)
  for k,(x,y) in enumerate([(445,260),(540,350),(750,435)]):
   q=ease(prog(t,.5+k*.8,1+k*.8));circle(im,x,y,16*q,None,p['secondary'],3);line(im,[(x+18,y),(x+18+170*q,y)],p['secondary'],2)
   txt(im,['Header','Metric','Detail'][k],x+180,y-20,p,19,opacity=q)
 elif i==36:
  src=card(p,640,350,'SCAN ASSEMBLY','All strips connected')
  for k in range(14):
   piece=src.crop((0,k*25,640,(k+1)*25));q=ease(prog(t,k*.08,.65+k*.08));paste(im,piece,640+(1-q)*(700 if k%2 else -700),185+k*25+12,opacity=q)
 elif i==37:
  q=prog(t,.1,1.2);bounce=max(0,t-1.2);y=350 if q>=1 else mix(-180,350,q*q);y-=abs(math.sin(bounce*9))*35*math.exp(-bounce*2)
  paste(im,card(p,600,230,'IMPACT','Heavy entrance'),640,y)
  if bounce>0:
   for k in range(24):a=k*2.4;x=640+math.cos(a)*bounce*280;yy=490+math.sin(a)*bounce*65+bounce*bounce*65;rr(im,(x,yy,x+9,yy+5),rgba(p['accent'],255*max(0,1-bounce/1.4)),1)
 elif i==38:
  scene=card(p,780,350,'SPOTLIGHT','Reveal the hidden detail');dark=layer(780,350);rr(dark,(0,0,780,350),rgba(p['bg'],225),20)
  mask=Image.new('L',(780,350),255);d=ImageDraw.Draw(mask);x=-80+t*190;d.ellipse((x-110,-70,x+110,420),fill=0);mask=mask.filter(ImageFilter.GaussianBlur(35));dark.putalpha(mask.point(lambda z:int(z*.86)));scene.alpha_composite(dark);paste(im,scene,640,360)
 elif i==39:
  rr(im,(260,165,1020,565),p['panel'],24);rr(im,(510,195,980,270),rgba(p['secondary'],50),18);txt(im,'Explain this idea simply.',535,230,p,26,anchor='left')
  response='A clear explanation starts with one useful idea.\nShow the action. Then show the result.';n=int(prog(t,1.1,4.5)*len(response));visible=response[:n]
  for k,row in enumerate(visible.split('\n')):txt(im,row,305,335+k*55,p,24,anchor='left')
  if int(t*3)%2:rr(im,(305+measure(visible.split('\n')[-1],24),322+55*(visible.count('\n')),310+measure(visible.split('\n')[-1],24),349+55*(visible.count('\n'))),p['accent'],1)
 elif i==40:
  gap=20+65*(.5+.5*math.sin(t*1.1));w=155;total=4*w+3*gap
  for k in range(4):x=640-total/2+k*(w+gap);rr(im,(x,245,x+w,430),p['panel'],18,p['accent']);txt(im,str(k+1),x+w/2,335,p,35)
  line(im,[(410,530),(870,530)],p['muted'],6);knob=410+(gap-20)/65*460;circle(im,knob,530,16,p['accent']);txt(im,'Gap: '+str(round(gap))+' px',640,590,p,25)
 elif i==41:
  for k,(x,y,w,h) in enumerate([(330,215,620,70),(330,310,290,205),(660,310,290,205)]):
   q=prog(t,.2+k*.45,.8+k*.45);pts=[(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)];n=q*4;j=min(3,int(n));drawpts=pts[:j+1]+[(mix(pts[j][0],pts[j+1][0],n-j),mix(pts[j][1],pts[j+1][1],n-j))];line(im,drawpts,p['accent'],3)
   if q==1:rr(im,(x+2,y+2,x+w-2,y+h-2),rgba(p['panel'],int(255*prog(t,1.9,2.9))),14);txt(im,['CANVAS','Layout','Content'][k],x+w/2,y+h/2,p,27,opacity=prog(t,2,3))
 elif i==42:
  pick=4;selected=prog(t,1.1,2.0)
  for k in range(9):
   x=400+(k%3)*240;y=240+(k//3)*120;active=k==pick;col=p['accent'] if active and selected else p['panel'];alpha=1 if active else 1-.8*selected
   tile=layer(210,78);rr(tile,(1,1,209,77),col,39);txt(tile,['Design','Video','Data','Text','Motion','Audio','Map','Code','Learn'][k],105,39,p,24,p['bg'] if active and selected else p['text']);paste(im,tile,x,y,opacity=alpha,scale=1+.1*selected if active else 1)
  cursor(im,672,380,p)
 elif i==43:
  rr(im,(690,190,1020,280),p['panel'],45);circle(im,738,235,25,p['secondary']);txt(im,'User',790,235,p,25,anchor='left')
  for k in range(6):
   x=350+(k%3)*235;y=390+(k//3)*110
   if k!=1:rr(im,(x-90,y-30,x+90,y+30),p['panel'],30);txt(im,'Topic '+str(k+1),x,y,p,23)
  q=smooth(prog(t,.7,3.2));x=mix(585,895,q);y=mix(390,235,q)-85*math.sin(q*math.pi);rr(im,(x-90,y-30,x+90,y+30),p['accent'],30);txt(im,'Motion',x,y,p,23,p['bg'])
 elif i==44:
  rr(im,(275,180,1005,555),p['panel'],20)
  for k in range(3):
   x=420+k*205+math.sin(t*(.65+k*.2)+k)*55;y=320+math.cos(t*.8+k*2)*95;cursor(im,x,y,p,['Ali','Maya','Sam'][k], [p['accent'],p['secondary'],p['text']][k]);rr(im,(x-50,y-60,x+55,y-12),None,7,[p['accent'],p['secondary'],p['text']][k],2)
 elif i==45:
  q=pop(prog(t,.2,.9));pal=layer(650,350);rr(pal,(2,2,648,348),p['panel'],20,p['muted']);query='render preview';s=query[:int(prog(t,.9,2.4)*len(query))];txt(pal,'> '+s,30,48,p,27,anchor='left')
  for k,row in enumerate(['Render preview','Export MP4','Open settings']):rr(pal,(20,105+k*74,630,166+k*74),rgba(p['accent'],45) if k==0 and t>2 else rgba(p['muted'],15),8);txt(pal,row,40,135+k*74,p,24,anchor='left')
  paste(im,pal,640,365,opacity=clamp(q),scale=max(.01,q));
 elif i==46:
  rr(im,(275,270,1005,445),rgba(p['secondary'],25),60,rgba(p['text'],140),2)
  if t<2.7:
   for k in range(34):h=10+48*abs(math.sin(t*6+k*.7))*e;line(im,[(440+k*12,355-h),(440+k*12,355+h)],p['accent'],5)
  else:txt(im,'Your voice becomes text.'[:int(prog(t,2.7,4.7)*24)],640,355,p,36)
  circle(im,335,355,22,p['accent']);line(im,[(335,338),(335,368)],p['bg'],5)
 elif i==47:
  q=ease(prog(t,1.1,2.7));s='#motion';w=measure(s,56)+100
  rr(im,(640-w/2,350-60*q,640+w/2,350+60*q),rgba(p['accent'],int(255*q)),60*q)
  txt(im,s,640,350,p,56,p['bg'] if q>.5 else p['text']);tag(im,'TOPIC READY',535,530,p) if t>3 else None
 elif i==48:
  rr(im,(290,240,820,325),p['panel'],16,p['muted']);s='Create my preview';txt(im,s[:int(prog(t,.2,1.7)*len(s))],320,282,p,29,anchor='left');rr(im,(850,240,990,325),p['accent'],16);txt(im,'GO',920,282,p,29,p['bg']);cursor(im,1000-100*ease(prog(t,1.5,2.2)),355-60*ease(prog(t,1.5,2.2)),p)
  q=enter(t,2.4,3.2);paste(im,card(p,700,190,'RESULT','Preview is ready'),640,460+60*(1-q),opacity=q)
 elif i==49:
  phase=clamp((t-.3)/4)*3
  for k in range(6):
   x=640+(k-phase-1)*270;dist=abs(x-640);scale=max(.5,1-dist/1800)
   if 110<x<1170:paste(im,card(p,245,260,['Capture','Arrange','Animate','Preview','Export','Share'][k],str(k+1)),x,350,scale=scale,opacity=max(.15,1-dist/900))
  for k in range(4):circle(im,590+k*33,560,6,p['accent'] if k==round(phase) else p['muted'])
 elif i==50:
  rr(im,(340,160,940,225),p['panel'],32);q=clamp((t-.5)/4)*2;idx=min(2,int(q+.5));x=440+200*q;rr(im,(x-95,165,x+95,220),p['accent'],27)
  for k,s in enumerate(['Plan','Create','Share']):txt(im,s,440+k*200,193,p,24,p['bg'] if k==idx else p['text'])
  paste(im,card(p,610,300,['PLAN YOUR IDEA','CREATE YOUR STORY','SHARE YOUR RESULT'][idx],['Outline ready','Motion ready','Link ready'][idx]),640,410,scale=.97+.03*math.cos(t*5))
 elif i==51:
  q=smooth(prog(t,1.2,3.5));light={'bg':'#F1F5F9','panel':'#FFFFFF','text':'#152238','muted':'#6D7890','accent':p['accent'],'secondary':p['secondary']};dark=im.copy();lit=Image.new('RGBA',(1280,720),light['bg']);paste(lit,card(light,560,300,'APPEARANCE','Light mode'),640,365);paste(dark,card(p,560,300,'APPEARANCE','Dark mode'),640,365);im=Image.blend(dark,lit,q)
  rr(im,(560,545,720,605),p['muted'],30);circle(im,590+100*q,575,24,p['accent']);txt(im,title,640,63,light if q>.5 else p,32);txt(im,'Theme crossfade',640,664,light if q>.5 else p,17)
 elif i==52:
  query='motion';n=int(prog(t,.2,2.4)*len(query));rr(im,(325,170,955,245),p['panel'],20,p['accent']);txt(im,'Search: '+query[:n],350,208,p,27,anchor='left');rows=['Motion design','Colour palette','Motion presets','Voice narration','Motion studies']
  y=305
  for k,row in enumerate(rows):
   visible=1 if n==0 or query[:n].lower() in row.lower() else 1-prog(t,.8,2.1)
   if visible>0:rr(im,(325,y-28,955,y+35),rgba(p['panel'],255*visible),12);txt(im,row,350,y,p,25,anchor='left',opacity=visible);y+=76*visible
 elif i==53:
  rr(im,(225,205,1055,510),p['panel'],25)
  for k in range(80):
   x=265+k*9.5;h=12+95*abs(math.sin(k*.25+t*4)*math.cos(k*.07-t*.7));line(im,[(x,355-h),(x,355+h)],p['accent'] if x<265+750*u else p['muted'],5)
  x=265+750*u;line(im,[(x,225),(x,490)],p['text'],2);txt(im,f'{int(t):02d}:00 / 05:00',640,570,p,24)
 return im.convert('RGBA')
