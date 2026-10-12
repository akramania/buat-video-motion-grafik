"""Original guide adaptations. 2.5D perspective, never advertised as true 3D.
Deterministic normalized five-second timeline; independent configurable components.
"""
from core import *
import json
INDEX=json.loads((Path(__file__).parent/'guide_index.json').read_text())
PRESETS={}
for i in range(101,153):
 pid=f'PV{i:03d}'; meta=INDEX[pid]
 PRESETS[pid]=dict(name=meta['name'],description=meta['description'],genre='creator' if i<126 else 'saas',text='MAKE IDEAS MOVE' if i<126 else 'PROJECT ATLAS',subtitle='Original motion study',family='guide',duration=6,source_url=meta['source_url'],adaptation_status='original-demo',category=meta['category'],mechanism=meta['name']+(' (2.5D projection)' if i in (129,130,148) else ''))

def heading(im,cfg,p):
 tag(im,'ORIGINAL DEMO',80,78,p)
 text(im,cfg.get('subtitle','Motion study'),80,640,22,p['muted'],anchor='left')

def title(cfg): return str(cfg.get('text','MAKE IDEAS MOVE'))[:40]
def words(s): return s.split() or ['MOVE']
def glyph_positions(s,size):
 total=measure(s,size); x=640-total/2
 out=[]
 for ch in s:
  w=measure(ch,size);out.append((ch,x+w/2,w));x+=w
 return out

def card(p,caption='Project Atlas',w=340,h=240):
 im=layer(w,h);rr(im,(1,1,w-2,h-2),p['panel'],20,p['muted'])
 circle(im,32,35,7,p['accent']);text(im,caption,52,35,19,p['text'],anchor='left')
 rr(im,(24,66,w-24,h-68),rgba(p['accent'],20),12)
 for j in range(4):rr(im,(42+j*(w-90)/4,h-96-17*j,64+j*(w-90)/4,h-78),p['accent'],4)
 line(im,[(26,h-40),(w-80,h-40)],p['muted'],6)
 rr(im,(w-66,h-53,w-24,h-27),p['accent'],10)
 return im

def bez(a,b,c,d,u):
 v=1-u;return (v**3*a[0]+3*v*v*u*b[0]+3*v*u*u*c[0]+u**3*d[0],v**3*a[1]+3*v*v*u*b[1]+3*v*u*u*c[1]+u**3*d[1])
def path_trace(im,pts,q,col,width=4):
 n=clamp(q)*(len(pts)-1);count=int(n)
 segment=pts[:count+1]
 if count<len(pts)-1:segment.append((mix(pts[count][0],pts[count+1][0],n-count),mix(pts[count][1],pts[count+1][1],n-count)))
 if len(segment)>1:line(im,segment,col,width)
def pill(p,s,w=230,h=64):
 im=layer(w,h);rr(im,(0,0,w-1,h-1),p['panel'],h/2,p['accent'],2);text(im,s,w/2,h/2,24,p['text']);return im

def render(pid,t,cfg):
 p=palette(cfg);im=base(cfg);heading(im,cfg,p);n=int(pid[2:]);s=title(cfg);sz=fit_size(s,1050,82);q=enter(t,.15,1.3);out=1-leave(t,4.35,5)
 scene=layer()
 if n>=126:text(scene,s,80,126,fit_size(s,1100,32),p['text'],anchor='left')
 if n==101:
  a=text_img(s,sz,p['text']);blur=(1-q)*22
  a=a.filter(ImageFilter.GaussianBlur(blur));paste(scene,a,640+360*(1-q),340,q)
 elif n==102:
  text(scene,s,640,350,sz,p['text'],opacity=q)
  for sign,ch in [(-1,'{'),(1,'}')]:text(scene,ch,640+sign*(measure(s,sz)/2+55)*q,350,110,p['accent'])
 elif n==103:
  beat=prog(t,.6,1.25);scale=1+.65*math.exp(-max(0,t-.65)*8) if t>.65 else .18
  if .65<t<.78:rr(scene,(80,165,1200,535),p['accent'],0)
  text(scene,s,640,355+18*math.sin(t*45)*math.exp(-max(0,t-.65)*8),sz,p['text'],scale=scale,opacity=beat)
  if t>.65:
   for j in range(12):
    a=j*math.tau/12;r=180+120*prog(t,.65,1.4);line(scene,[(640+math.cos(a)*r,355+math.sin(a)*r*.65),(640+math.cos(a)*(r+40),355+math.sin(a)*(r+40)*.65)],rgba(p['accent'],120*(1-prog(t,.65,1.4))),4)
 elif n==104:
  phase=min(2,int(t/1.05));num=str(3-phase) if t<3.15 else 'GO'
  pts=[(640+math.cos(-math.pi/2+a*math.tau)*150,345+math.sin(-math.pi/2+a*math.tau)*150) for a in [j/100 for j in range(101)]]
  path_trace(scene,pts,(t%1.05)/1.05 if t<3.15 else 1,p['accent'],8);text(scene,num,640,345,100,p['text'])
  if t>3.15:
   for j in range(18):a=j*math.tau/18;r=200+120*prog(t,3.15,4);circle(scene,640+math.cos(a)*r,345+math.sin(a)*r*.55,6,p['secondary'])
 elif n==105:
  rr(scene,(230,155,1050,555),p['panel'],18)
  lines=[s,'A clear idea starts here.','Build the story, one line at a time.'];amount=int(prog(t,.45,3.35)*sum(map(len,lines)))
  for j,st in enumerate(lines):
   k=min(len(st),max(0,amount));text(scene,st[:k],275,240+j*93,fit_size(st,720,36),p['text'],anchor='left');amount-=len(st)
 elif n==106:
  ws=words(s);size=fit_size(s,1020,74);x=640-measure(s,size)/2
  for j,w in enumerate(ws):
   ww=measure(w,size);a=enter(t,.15+j*.3,1.5+j*.3)
   text(scene,w,x+ww/2+(1-a)*(-600 if j%2==0 else 600),345+(1-a)*(200 if j%2 else -220),size,p['text'],angle=(1-a)*(60 if j%2 else -60));x+=ww+measure(' ',size)
 elif n==107:
  original=text_img(s,sz,p['text']);paste(scene,original,640,350)
  if t<2.3 and int(t*12)%3==0:
   for j in range(6):
    y=int(original.height*j/6);strip=original.crop((0,y,original.width,min(original.height,y+original.height//6)))
    paste(scene,strip,640+math.sin(t*33+j)*27,350-original.height/2+y,anchor='left')
   text(scene,s,648,350,sz,p['accent'],opacity=.4)
 elif n==108:
  tx=text_img(s,sz,p['text']);paste(scene,tx,640,350)
  ac=text_img(s,sz,p['accent']);mask=layer(ac.width,ac.height);d=ImageDraw.Draw(mask);cx=int((t/4.5)* (ac.width+200)-100);d.rectangle((cx-90,0,cx+90,ac.height),fill='white');ac.putalpha(Image.composite(ac.getchannel('A'),Image.new('L',ac.size),mask.getchannel('A')));paste(scene,ac,640,350)
 elif n==109:
  text(scene,s,640,330,sz,p['text'],opacity=q);ww=measure(s,sz)
  pts=[(640-ww/2+j*ww/50,399+math.sin(j*.5)*3) for j in range(51)];path_trace(scene,pts,prog(t,.7,2),p['accent'],15)
  xx=640-ww/2+ww*prog(t,.7,2);line(scene,[(xx,395),(xx+25,367)],p['secondary'],7)
 elif n==110:
  text(scene,s,640,350,sz,p['bg'],stroke=2,stroke_color=p['accent']);a=text_img(s,sz,p['text']);paste(scene,crop_reveal(a,prog(t,.7,2.5),'left'),640,350)
 elif n==111:
  sheet=layer(1040,280);d=ImageDraw.Draw(sheet);d.polygon([(0,15),(1000,0),(1040,260),(20,280)],fill='#EFE8DA');text(sheet,s,520,140,sz,'#222D3B')
  paste(scene,sheet,640,350+260*(1-q),angle=-5*(1-q))
 elif n==112:
  rr(scene,(360,280,920,420),p['panel'],35,p['accent'],2)
  text(scene,'MOVE',450,350,36,p['text']);cycle=['FAST','CLEAR','BOLD'];u=max(0,t-.5);idx=min(2,int(u));f=u%1 if idx<2 else 1
  slot=layer(250,80);text(slot,cycle[idx],125,40+(1-ease(f))*75,36,p['accent'],opacity=1-prog(t,2.3,3.3));paste(scene,slot,740,350)
  # Handled chip travel visibly docks into slot.
  pp=enter(t,2.3,3.3);paste(scene,pill(p,'READY',160),mix(1060,760,pp),mix(200,350,pp),opacity=prog(t,2.2,2.5))
 elif n==113:
  text(scene,'CREATE',365,350,54,p['text']);rr(scene,(570,298,985,402),p['accent'],52)
  slot=layer(395,90);u=max(0,t-.4);idx=min(2,int(u/1.1));f=(u%1.1)/1.1 if idx<2 else 1
  text(slot,['IDEAS','MOTION','IMPACT'][idx],197,45+90*(1-ease(f)),45,p['bg']);paste(scene,slot,777,350)
 elif n==114:
  chars='ABCDEFGHJKLMNPQRSTUVWXYZ0123456789';arr=''
  for j,ch in enumerate(s):arr+=ch if t> .3+j*.055 else (chars[(int(t*19)+j*7)%len(chars)] if ch!=' ' else ' ')
  text(scene,arr,640,350,sz,p['text'],'mono')
 elif n==115:
  ss=s[:18];size=fit_size(ss,1020,65);ww=measure('M',size,'mono')+14;x=640-len(ss)*ww/2
  for j,ch in enumerate(ss):
   a=prog(t,.2+j*.08,1+j*.08);rr(scene,(x+j*ww,287,x+(j+1)*ww-5,416),p['panel'],7)
   if ch!=' ':
    old=chr(65+(j+int(t*9))%26);tx=text_img(ch if a>.7 else old,size,p['text'],'mono');paste(scene,tx,x+(j+.5)*ww-2,350,scale=1)
    line(scene,[(x+j*ww,350),(x+(j+1)*ww-5,350)],p['bg'],3)
    if 0<a<1:rr(scene,(x+j*ww,350,x+(j+1)*ww-5,350+55*math.sin(a*math.pi)),rgba(p['accent'],60),2)
 elif n==116:
  ws=words(s);size=52
  for j,w in enumerate(ws):a=enter(t,.2+j*.16,1.7+j*.16);text(scene,w,mix(150+j*450/max(1,len(ws)-1),640,a),mix(210+j*130,250+j*90,a),size,p['text'])
 elif n==117:
  a=prog(t,1.5,2.6);a=ease(a);text(scene,s,mix(640,300,a),mix(335,205,a),sz,p['text'],scale=mix(1,.4,a))
  paste(scene,card(p,'Workspace',720,270),640,390,opacity=a)
 elif n==118:
  for j,(ch,x,w) in enumerate(glyph_positions(s,sz)):
   a=enter(t,.15+j*.025,1.6+j*.025);angle=(1-a)*(90 if j%2 else -90)
   text(scene,ch,x,350+(1-a)*(250 if j%2 else -250),sz,p['text'],angle=angle,opacity=a)
 elif n==119:
  tx=text_img(s,sz,p['text']);a=crop_reveal(tx,q);paste(scene,a,640,350+45*(1-q));line(scene,[(150,410),(1130,410)],rgba(p['accent'],160*(1-q)),3)
 elif n==120:
  ws=words(s)
  for j,w in enumerate(ws):a=enter(t,.25+j*.55,.5+j*.55);beat=max(0,math.sin((t-j*.55)*math.pi*2))*math.exp(-max(0,t-j*.55)*1.5);text(scene,w,640,240+j*100,fit_size(w,1000,70),p['text'],scale=(.9+.1*a+.12*beat),opacity=a)
 elif n==121:
  count=int(prog(t,.3,2.8)*len(s));part=s[:count];size=sz;left=640-measure(s,size)/2;text(scene,part,left,350,size,p['text'],'mono',anchor='left')
  if int(t*3)%2==0:rr(scene,(left+measure(part,size,'mono')+8,310,left+measure(part,size,'mono')+13,390),p['accent'],0)
 elif n==122:
  rr(scene,(220,170,1060,535),p['panel'],20)
  for j,c in enumerate([p['accent'],p['secondary'],p['muted']]):circle(scene,255+j*25,200,6,c)
  code=['const scene = createMotion();','scene.title = "MOVE";','scene.duration = 6;','render(scene);'];total=sum(map(len,code));num=int(prog(t,.3,3.5)*total)
  for j,st in enumerate(code):count=min(len(st),max(0,num));text(scene,f'{j+1:02}',257,270+j*59,23,p['muted'],'mono',anchor='left');text(scene,st[:count],310,270+j*59,27,p['accent'] if j==3 else p['text'],'mono',anchor='left');num-=len(st)
 elif n==123:
  rr(scene,(210,278,1070,422),p['panel'],12);slot=layer(840,130);u=max(0,t-.3);idx=min(2,int(u/1.1));f=(u%1.1)/1.1 if idx<2 else 1
  tx=text_img(['IMAGINE','CREATE','MOVE'][idx],84,p['text']);tx=tx.filter(ImageFilter.GaussianBlur((1-f)*6));paste(slot,tx,420,65+140*(1-ease(f)));paste(scene,slot,640,350)
 elif n==124:
  ws=words(s);a=prog(t,.2,3);x=640-a*max(0,len(ws)-1)*520
  film=layer()
  for j,w in enumerate(ws):rr(film,(x+j*520-230,250,x+j*520+230,445),p['panel'],5,p['accent']);text(film,w,x+j*520,347,fit_size(w,420,66),p['text'])
  paste(scene,film,640,360)
  for xh in range(80,1220,45):rr(scene,(xh,218,xh+18,232),p['muted'],2);rr(scene,(xh,463,xh+18,477),p['muted'],2)
 elif n==125:
  ws=words(s);idx=min(len(ws)-1,int(t/.95));shape=(idx%3);d=ImageDraw.Draw(scene)
  if shape==0:circle(scene,640,350,180,rgba(p['accent'],30),p['accent'],3)
  elif shape==1:rr(scene,(420,210,860,490),rgba(p['accent'],30),25,p['accent'],3)
  else:d.polygon([(640,170),(875,465),(405,465)],fill=rgba(p['accent'],30),outline=p['accent'])
  text(scene,ws[idx],640,350,fit_size(ws[idx],480,77),p['text'],scale=.9+.1*ease((t% .95)/.95))
 elif n==126:
  for j in range(5):
   angle=(j-2)*.65-(t*.3);x=640+math.sin(angle)*380;y=345+math.cos(angle)*35;r=42*(.7+.3*math.cos(angle));circle(scene,x,y,r,p['panel'],p['accent'],2);text(scene,chr(65+j),x,y,30,p['text'])
  for x,sign in [(505,1),(775,-1)]:line(scene,[(x+sign*18,275),(x,275),(x,425),(x+sign*18,425)],p['accent'],4)
 elif n==127:
  for j in range(5):
   start=(160,170+j*90);curve=[bez(start,(500,start[1]),(480,350),(800,350),k/60) for k in range(61)];path_trace(scene,curve,prog(t,.2+j*.15,2.6),rgba(p['accent'],100),3)
   a=ease(prog(t,.2+j*.15,2.6));x,y=bez(start,(500,start[1]),(480,350),(800,350),a);circle(scene,x,y,20,p['accent'])
  paste(scene,card(p,'Unified',300,240),880,350,opacity=prog(t,2,2.8))
 elif n==128:
  for j in reversed(range(4)):
   a=enter(t,.15+j*.18,1.4+j*.18);paste(scene,card(p,f'Card {j+1}'),640+j*20,350+j*17+430*(1-a),angle=(j-1.5)*4)
 elif n==129:
  cards=[]
  for j in range(5):a=t*.5+j*math.tau/5;z=math.cos(a);cards.append((z,j,a))
  for z,j,a in sorted(cards):
   x=640+math.sin(a)*370;sc=.55+.35*(z+1)/2;asset=card(p,f'Page {j+1}',280,230);asset=asset.resize((max(1,int(asset.width*(.55+.45*abs(z)))),asset.height));paste(scene,asset,x,345,scale=sc,opacity=.4+.6*(z+1)/2)
  label(scene,'2.5D PROJECTION',80,600,p)
 elif n==130:
  for j in reversed(range(7)):
   a=enter(t,.15+j*.1,1.2+j*.1);paste(scene,card(p,'Echo',370,230),640+(j-3)*35*a,350-j*19*a,opacity=1-j*.1,scale=1-j*.075)
  label(scene,'2.5D DEPTH',80,600,p)
 elif n==131:
  for j in range(4):
   a=enter(t,.2+j*.3,1.15+j*.3);paste(scene,card(p,f'Feature {j+1}',230,270),mix(160,280+j*240,a),mix(610,350,a),angle=(1-a)*(-120+j*18),opacity=a)
 elif n==132:
  a=enter(t,.2,1.4);paste(scene,card(p,'Document',420,330),mix(640,340,a),350,scale=mix(1,.85,a))
  for j,st in enumerate(['SUMMARY','ACTION','RESULT']):b=enter(t,1+j*.25,2.2+j*.25);paste(scene,pill(p,st,290),mix(360,900,b),mix(350,250+j*100,b),opacity=b)
 elif n==133:
  pts=[(390,245),(890,245),(890,455),(390,455),(390,245)];path_trace(scene,pts,prog(t,.2,2.3),p['accent'],5)
  c=[(450,385),(530,325),(610,365),(710,285),(815,325)];path_trace(scene,c,prog(t,1.6,3.2),p['secondary'],7)
 elif n==134:
  # Container arrives, then bodies settle with separate spring phases.
  a=enter(t,.1,1);rr(scene,(280,170+400*(1-a),1000,550+400*(1-a)),p['panel'],24)
  for j in range(3):b=pop(prog(t,.8+j*.18,1.6+j*.18));rr(scene,(330,235+j*90+70*(1-b),950,290+j*90+70*(1-b)),rgba(p['accent'],40),12);text(scene,f'COMPONENT {j+1}',360,262+j*90+70*(1-b),25,p['text'],anchor='left')
 elif n==135:
  for j,st in enumerate(['SMART','QUICK','CLEAR','READY']):
   a=enter(t,.2+j*.2,1.2+j*.2);asset=pill(p,st,280,82);rr(asset,(30,8,250,20),rgba('#FFFFFF',70),8);paste(scene,asset,420+(j%2)*430,270+(j//2)*160+math.sin(t*1.8+j)*14,scale=.75+.25*a,opacity=a,angle=math.sin(t+j)*3)
 elif n==136:
  circle(scene,640,350,65,p['panel'],p['accent'],4);text(scene,'HUB',640,350,30,p['text'])
  for j in range(6):a=j*math.tau/6;x=640+math.cos(a)*310;y=350+math.sin(a)*180;qj=prog(t,.2+j*.12,1.7+j*.12);path_trace(scene,[(640,350),(x,y)],qj,p['muted'],3);circle(scene,x,y,35*qj,p['accent']);text(scene,str(j+1),x,y,25,p['bg'],opacity=qj)
 elif n==137:
  for j in range(4):a=enter(t,.3+j*.35,1+j*.35);rr(scene,(270+160*(1-a),190+j*92,1010+160*(1-a),262+j*92),p['panel'],14);circle(scene,310+160*(1-a),226+j*92,10,p['accent']);text(scene,f'WORKFLOW STEP {j+1}',350+160*(1-a),226+j*92,27,p['text'],opacity=a,anchor='left')
 elif n==138:
  a=prog(t,1.4,2.7)
  for j in reversed(range(5)):
   y=mix(185+j*77,325+j*12,ease(a));paste(scene,pill(p,f'TASK {j+1}',580,65),640,y,scale=mix(1,1-j*.03,a))
  if t>2.7:circle(scene,955,350,24,p['accent']);text(scene,'✓',955,350,25,p['bg'])
 elif n==139:
  a=ease(prog(t,.3,2));ww=mix(100,720,a);hh=mix(100,340,a);rr(scene,(640-ww/2,350-hh/2,640+ww/2,350+hh/2),p['panel'],mix(50,22,a),p['accent'],3);paste(scene,card(p,'New workspace',680,300),640,350,opacity=prog(t,1.5,2.5))
 elif n==140:
  # Frame leads, card follows only after outline completion.
  pts=[(260,185),(1020,185),(1020,535),(260,535),(260,185)];path_trace(scene,pts,prog(t,.15,1.6),p['accent'],6);paste(scene,card(p,'Frame first',700,290),640,360+80*(1-enter(t,1.25,2.3)),opacity=prog(t,1.25,2.3))
 elif n==141:
  a=enter(t,.2,2.2);frame=layer(590,325);rr(frame,(3,3,585,320),None,25,p['accent'],5);paste(scene,frame,640+math.cos(t*5)*(1-a)*300,350-230*(1-a),angle=360*(1-a),scale=.5+.5*a);paste(scene,card(p,'Orbit / dock',535,265),640,350,opacity=prog(t,2,2.6))
 elif n==142:
  for col in range(4):
   for row in range(2):a=enter(t,.15+col*.2+row*.35,1.4+col*.2+row*.35);paste(scene,card(p,f'Page {col+row*4+1}',245,185),250+col*260,265+row*210-650*(1-a),opacity=a)
 elif n==143:
  a=enter(t,.2,2);sheet=card(p,'Fold / reveal',690,330);ww=max(2,round(sheet.width*a));sheet=sheet.resize((ww,sheet.height));paste(scene,sheet,640,350);line(scene,[(640-ww/2,185),(640-ww/2,515)],p['secondary'],5)
  if a<1:ImageDraw.Draw(scene).polygon([(640-ww/2,185),(640-ww/2+100*(1-a),220),(640-ww/2,515)],fill=p['accent'])
 elif n==144:
  rr(scene,(350,150,930,570),p['panel'],25, p['muted']);rr(scene,(390,190,890,355),rgba(p['accent'],25),15)
  circle(scene,640,270,55*enter(t,.15,1),p['accent']);text(scene,'ATLAS',640,400,40,p['text'],opacity=prog(t,.8,1.5));text(scene,'Build a clearer workflow',640,455,25,p['muted'],opacity=prog(t,1.5,2.1));paste(scene,pill(p,'EXPLORE',240),640,520,opacity=prog(t,2.1,2.8))
 elif n==145:
  for j in range(16):a=j*math.tau/16;r=180;d=(j%4)*.18;qj=pop(prog(t,.2+d,1.5+d));circle(scene,640+math.cos(a)*r*qj,350+math.sin(a)*r*qj,20,p['accent'])
  for r in [70,130,190]:circle(scene,640,350,r*prog(t,.15,2),None,rgba(p['secondary'],70),2)
 elif n==146:
  # Scroll window clips article cards and brings successive results to foreground.
  viewport=layer(740,400);u=ease(prog(t,.5,3.5))*360
  for j in range(5):
   y=50+j*145-u;rr(viewport,(20,y,720,y+126),p['panel'],15,p['muted']);text(viewport,f'RESEARCH NOTE {j+1}',55,y+35,25,p['text'],anchor='left');line(viewport,[(55,y+75),(650,y+75)],p['accent'],5)
  paste(scene,viewport,640,350);rr(scene,(1025,150,1032,550),p['panel'],3);rr(scene,(1025,150+u*.55,1032,240+u*.55),p['accent'],3)
 elif n==147:
  rr(scene,(200,240,1080,470),p['panel'],22);line(scene,[(245,290),(490,290)],p['muted'],7);line(scene,[(245,340),(490,340)],p['muted'],5)
  a=enter(t,.4,2);paste(scene,card(p,'Embedded view',440,190),mix(1050,805,a),355,scale=mix(.3,1,a));line(scene,[(550,270),(550,440)],rgba(p['muted'],100),2)
 elif n==148:
  # Ground plane + perspective growth, explicitly 2.5D.
  for j in range(8):line(scene,[(640,195),(100+j*155,580)],rgba(p['muted'],60),2)
  for j in range(6):y=210+j*j*12;line(scene,[(100,y),(1180,y)],rgba(p['muted'],60),2)
  a=enter(t,.25,2.6);paste(scene,card(p,'Arrival',660,320),640,mix(240,365,a),scale=mix(.08,1,a));label(scene,'2.5D GROUND PLANE',80,600,p)
 elif n==149:
  rr(scene,(280,155,1000,565),p['panel'],24);a=prog(t,1.7,2.6)
  sk=layer();rr(sk,(320,205,530,395),p['muted'],12)
  for j in range(4):rr(sk,(570,215+j*54,950-j*25,238+j*54),p['muted'],10)
  shimmer=layer();rr(shimmer,(int(200+t*220),160,int(270+t*220),560),rgba('#FFFFFF',50),4);sk.alpha_composite(shimmer);paste(scene,sk,640,360,opacity=1-a)
  paste(scene,card(p,'Loaded content',650,335),640,360,opacity=a)
 elif n==150:
  a=prog(t,.3,2.8);d=ImageDraw.Draw(scene);pts=[]
  for j in range(60):theta=j*math.tau/60;circle_pt=(640+math.cos(theta)*145,350+math.sin(theta)*145);square_pt=(640+math.copysign(170,math.cos(theta))*min(1,abs(math.cos(theta))*1.414),350+math.copysign(140,math.sin(theta))*min(1,abs(math.sin(theta))*1.414));pts.append((mix(circle_pt[0],square_pt[0],smooth(a)),mix(circle_pt[1],square_pt[1],smooth(a))))
  d.polygon(pts,fill=p['accent']);text(scene,'MORPH',640,350,40,p['bg'],opacity=prog(t,2.3,3))
 elif n==151:
  values=['CLEAR','FAST','FOCUSED'];colors=[p['accent'],p['secondary'],p['text']]
  for j,st in enumerate(values):a=enter(t,.2+j*.55,1+j*.55);rr(scene,(220+j*280,265+130*(1-a),470+j*280,435+130*(1-a)),colors[j],22);text(scene,st,345+j*280,350+130*(1-a),32,p['bg'],opacity=a)
 elif n==152:
  for j in range(12):row=j//4;col=j%4;a=prog(t,.2+row*.25+col*.15,1.3+row*.25+col*.15);asset=card(p,f'{j+1:02}',235,140);reveal=crop_reveal(asset,ease(a),'left');paste(scene,reveal,250+col*260,230+row*155)
 im.alpha_composite(scene if out>=.999 else fade(scene,out));return im

def fade(im,a):
 im=im.copy();im.putalpha(im.getchannel('A').point(lambda v:round(v*a)));return im
