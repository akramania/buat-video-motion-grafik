"""Original demonstrations of MS packs, PL launch shots and AD flows.
Pack demos are representative examples, not complete implementations of 53 upstream skills.
Silent geometric artwork. 2.5D mockups do not claim physical 3D.
"""
import json,math,importlib
from pathlib import Path
from core import *
INDEX=json.loads((Path(__file__).parent/'guide_index.json').read_text())
MS={
 'MS01':[('H01','STOP SCROLLING'),('C01','MEET YOUR NEXT IDEA'),('X02','TRY IT TODAY')],
 'MS02':[('N03','Can we simplify this?'),('N01','Yes. One step at a time.'),('N04','Message delivered')],
 'MS03':[('T04','THE BIG QUESTION'),('C04','EXPLORE THE DETAILS'),('H02','ONE USEFUL TAKEAWAY')],
 'MS04':[('A05','NEW COLLECTION'),('C03','SEE EVERY DETAIL'),('B04','RM 50')],
 'MS05':[('H03','MAKE IT SIMPLE'),('U01','MEET THE SOLUTION'),('X02','GET STARTED')],
 'MS06':[('L03','COMPARE THE RESULTS'),('MP17','FOLLOW THE TREND'),('B04','MEASURE THE CHANGE')],
 'MS07':[('L06','BEFORE AND AFTER'),('L02','HOW IT WORKS'),('T04','ONE CLEAR IDEA')],
 'MS08':[('MP15','A JOURNEY BEGINS'),('MP17','LOOK AT THE DATA'),('T01','SEE THE CONNECTION')],
 'MS09':[('U01','OPEN THE WORKSPACE'),('U02','SEE THE UPDATE'),('U04','EXPLORE THE VIEW')],
 'MS10':[('X03','MOTION'),('A07','FORM AND RHYTHM'),('B02','IDENTITY IN MOTION')],
 'MS11':[('K01','WORDS IN MOTION'),('K16','A NEW PERSPECTIVE'),('K31','MAKE IT MEMORABLE')],
 'MS12':[('T04','BRIEF / DESIGN / REVIEW'),('L04','SHARE YOUR FEEDBACK'),('T01','READY TO DELIVER')],
 'MS13':[('U04','LAYERED SPACE'),('MP06','LIGHT AND DEPTH'),('C02','ORBIT THE VIEW')],
 'MS14':[('MP17','GRAPH THE RELATIONSHIP'),('T04','CAUSE / EFFECT'),('L03','COMPARE THE VALUES')],
 'MS15':[('MP08','SHAPE AND COLOUR'),('MP19','GENERATIVE PATTERNS'),('MP22','A NEW ARRANGEMENT')],
 'MS16':[('U01','BUILD THE SCENE'),('L02','MOVE THE OBJECTS'),('X01','TELL THE STORY')],
}
# Existing renderer components are explicitly named in metadata, not passed off as new upstream engines.
OLD_MODULES=['ui','typography','carousels','new_a','new_b','long_a','long_b','kinetic_a','kinetic_b','kinetic_c','motionprompt']
DISPATCH={}; META={}
for mn in OLD_MODULES:
 mod=importlib.import_module(mn)
 for k,v in mod.PRESETS.items():DISPATCH[k]=mod.render;META[k]=v
PLNAMES={
'PL01':'Kinetic type beats','PL02':'Crowding problem','PL03':'Held thesis','PL04':'Prompt composer','PL05':'Results surface','PL06':'Two-pane workspace','PL07':'Pipeline status tracker','PL08':'Hero stat count-up','PL09':'Feature grid','PL10':'Comparison columns','PL11':'End card CTA','PL12':'Hardware hero','PL13':'Terminal dev-tool','PL14':'Map and chart reveal'}
PRESETS={}
for pid,v in INDEX.items():
 if pid[:2] not in ('MS','PL','AD'):continue
 family=pid[:2];duration=15 if family=='AD' else 12 if family=='MS' else 6
 PRESETS[pid]={**v,'family':'guide','genre':'saas' if family!='AD' else 'promo','text':'MAKE IT SIMPLE','subtitle':'Original motion demonstration','duration':duration,'adaptation_status':'original-demo','mechanism':v['description'],'demo_kind':'representative-pack' if family=='MS' else 'flow' if family=='AD' else 'shot','limitations':'Original adaptation from bundled index; silent demo; illustrative data. 2.5D, not physical 3D.'}
 if family=='MS':PRESETS[pid]['components']=[x[0] for x in MS[pid]]

def card(im,x,y,w,h,title,p,accent=None):
 rr(im,(x,y,x+w,y+h),p['panel'],22,rgba(p['muted'],90),2)
 circle(im,x+32,y+34,7,accent or p['accent'])
 text(im,title,x+53,y+35,fit_size(title,w-78,22),p['text'],anchor='left')
 for j in range(3):line(im,[(x+25,y+77+j*18),(x+w-35-j*28,y+77+j*18)],rgba(p['muted'],90),4)

def headline(im,cfg,p,y=184):
 s=cfg.get('text','MAKE IT SIMPLE');text(im,s,640,y,fit_size(s,1070,55),p['text'])

def cursor(im,x,y,p):
 ImageDraw.Draw(im).polygon([(x,y),(x+6,y+34),(x+14,y+23),(x+28,y+22)],fill=p['text'])

def render_pl(pid,t,cfg):
 im=base(cfg);p=palette(cfg);e=enter(t,.2,1.1);a=life(t); headline(im,cfg,p)
 if pid=='PL01':
  words=cfg.get('items',['LESS','FRICTION','MORE','MOMENTUM']);i=min(len(words)-1,int(max(0,t-.3)/1.0));q=prog(t,.3+i,.7+i)
  text(im,words[i],640,390,fit_size(words[i],1000,118),p['accent'],scale=.6+.4*pop(q),opacity=e)
  text(im,'A CLEAR BEAT FOR EVERY IDEA',640,565,22,p['muted'])
 elif pid=='PL02':
  for i in range(13):
   q=enter(t,.2+i*.14,.7+i*.14);x=210+(i%5)*185;y=265+(i//5)*86
   card(im,x+math.sin(i)*22*q,y+math.cos(i)*20*q,210,140,['TABS','TASKS','FILES','NOTES','MESSAGES'][i%5],p)
  if t>2.8:
   z=enter(t,2.8,3.3);rr(im,(405,318,875,443),p['accent'],26);text(im,'TOO MUCH TO MANAGE',640,380,30,p['bg'],opacity=z)
 elif pid=='PL03':
  rr(im,(150,290,1130,530),p['panel'],30)
  text(im,cfg.get('thesis','ONE WORKSPACE. A CLEARER DAY.'),640,385,fit_size(cfg.get('thesis','ONE WORKSPACE. A CLEARER DAY.'),880,50),p['text'],opacity=e)
  line(im,[(310,465),(310+660*enter(t,.8,1.4),465)],p['accent'],6)
 elif pid in ('PL04','PL13'):
  rr(im,(180,270,1100,560),p['panel'],25)
  text(im,'WORKSPACE' if pid=='PL04' else 'TERMINAL',215,305,17,p['muted'],'mono',anchor='left')
  s=cfg.get('prompt','Create a clear launch plan') if pid=='PL04' else cfg.get('code','> build --preview\n> assets ready\n> render complete')
  n=round(len(s)*prog(t,.5,2.7));lines=s[:n].split('\n')
  for j,ss in enumerate(lines):text(im,ss,225,370+j*45,26,p['accent'],'mono',anchor='left')
  if pid=='PL04':
   rr(im,(875,450,1065,512),p['accent'],16);text(im,'GENERATE',970,481,22,p['bg']);cursor(im,mix(600,1020,enter(t,2.3,2.8)),mix(610,492,enter(t,2.3,2.8)),p)
   if t>3.1:text(im,'Plan ready',640,607,25,p['text'],opacity=enter(t,3.1,3.5))
 elif pid=='PL05':
  for i,name in enumerate(cfg.get('items',['OVERVIEW','ACTIONS','TIMELINE'])):
   q=enter(t,.45+i*.38,1.2+i*.38);card(im,145+i*335,290+110*(1-q),310,225,name,p)
   circle(im,300+i*335,458,22*q,p['accent']);text(im,str(i+1),300+i*335,458,22,p['bg'],opacity=q)
 elif pid=='PL06':
  card(im,120,275,455,285,'YOUR INPUT',p);card(im,705,275,455,285,'YOUR RESULT',p)
  for i in range(5):
   q=enter(t,.4+i*.3,.8+i*.3);line(im,[(157,447+i*17),(157+345*q,447+i*17)],rgba(p['muted'],170),4)
  arrow(im,640,415,p['accent'],1.6)
  for i in range(4):
   q=enter(t,2.2+i*.23,2.7+i*.23);rr(im,(740,433+i*22,740+365*q,445+i*22),p['accent'],4)
 elif pid=='PL07':
  items=cfg.get('items',['INPUT','PROCESS','REVIEW','READY']);active=min(3,int(max(0,t-.6)/.8))
  for i,s in enumerate(items[:4]):
   x=210+i*285;circle(im,x,380,54,p['accent'] if i<=active else p['panel'],p['muted'],2);text(im,str(i+1),x,380,30,p['bg'] if i<=active else p['muted']);text(im,s,x,465,22,p['text'])
   if i<3:line(im,[(x+65,380),(x+220,380)],p['accent'] if i<active else p['muted'],4)
  text(im,'PROCESS COMPLETE' if active==3 else 'WORKING...',640,570,22,p['accent'])
 elif pid=='PL08':
  val=cfg.get('to_value',100);n=val*ease(prog(t,.4,3.4));s=f"{cfg.get('prefix','')}{n:,.0f}{cfg.get('suffix','%')}"
  text(im,s,640,385,115,p['accent']);text(im,'ILLUSTRATIVE DEMO VALUE',640,525,23,p['muted'])
 elif pid=='PL09':
  for i,s in enumerate(cfg.get('items',['PLAN','CREATE','REVIEW','EXPORT','SHARE','REPEAT'])[:6]):
   q=enter(t,.3+i*.23,.9+i*.23);x=160+(i%3)*335;y=265+(i//3)*162
   rr(im,(x,y+50*(1-q),x+290,y+140+50*(1-q)),p['panel'],22);text(im,s,x+145,y+70+50*(1-q),30,p['accent'],opacity=q)
 elif pid=='PL10':
  for i,(title,items) in enumerate([('BEFORE',['Scattered tasks','Repeated work','Hard to track']),('AFTER',['One workspace','Reusable steps','Clear progress'])]):
   x=155+i*515;q=enter(t,.3+i*.6,1.2+i*.6);rr(im,(x,270,x+455,585),p['panel'],25);text(im,title,x+227,325,35,p['muted'] if i==0 else p['accent'])
   for j,s in enumerate(items):text(im,s,x+227,405+j*55,25,p['text'],opacity=q)
 elif pid=='PL11':
  q=enter(t,.4,1.2);circle(im,640,315,55*q,p['accent']);text(im,'M',640,315,55,p['bg'],opacity=q)
  text(im,cfg.get('brand','MOTION ATLAS'),640,420,48,p['text'],opacity=q)
  rr(im,(425,500,855,580),p['accent'],24);text(im,cfg.get('cta','EXPLORE THE POSSIBILITIES'),640,540,25,p['bg'],opacity=q)
 elif pid=='PL12':
  product=layer(460,345);rr(product,(20,15,440,278),p['panel'],18,p['accent'],3);rr(product,(45,40,415,245),p['bg'],8)
  text(product,'MOTION',230,132,46,p['text']);text(product,'WORKSPACE',230,182,22,p['accent']);ImageDraw.Draw(product).polygon([(20,288),(440,288),(458,322),(2,322)],fill=p['muted'])
  paste(im,product,640,425,opacity=e,scale=.72+.28*e,angle=-5+10*math.sin(t*.5))
  text(im,'ORIGINAL 2.5D PRODUCT MOCKUP',640,630,19,p['muted'])
 elif pid=='PL14':
  # Abstract network, deliberately not a geographic map.
  points=[(245,370),(420,300),(525,440),(750,345),(1000,420)]
  q=prog(t,.5,2.5)
  for i in range(4):
   u=clamp(q*4-i);a0,b=points[i],points[i+1];line(im,[a0,(mix(a0[0],b[0],u),mix(a0[1],b[1],u))],p['accent'],5)
  for i,(x,y) in enumerate(points):circle(im,x,y,12*enter(t,.4+i*.3,.9+i*.3),p['accent']);text(im,str(i+1),x,y+40,20,p['text'])
  for i,v in enumerate(cfg.get('values',[.45,.65,.85])[:3]):
   x=470+i*125;h=100*v*enter(t,2.7+i*.2,3.4+i*.2);rr(im,(x,610-h,x+70,610),p['secondary'],6)
  text(im,'ABSTRACT NETWORK / DEMO DATA',640,655,17,p['muted'])
 return im

def component(pid,t,cfg,s):
 c={**META[pid],**{k:v for k,v in cfg.items() if k in ('genre','bg','accent','text_color','panel','muted','secondary')}}
 c['text']=s;c['_labels']=False;c['_duration']=META[pid].get('duration',5)
 clock=t/5*c['_duration'] if META[pid].get('time_mode')=='seconds' else t
 c['_seconds']=clock
 return DISPATCH[pid](pid,clock,c)

def render(pid,t,cfg):
 if pid.startswith('PL'):return render_pl(pid,t,cfg)
 if pid.startswith('MS'):
  n=min(2,int(t/5*3));local=(t/5*3-n)*5
  if t==5:local=5
  # Mathematical and map packs get custom representative diagram scenes.
  if pid=='MS14':
   im=base(cfg);p=palette(cfg);headline(im,{'text':'A RELATIONSHIP YOU CAN SEE'},p)
   line(im,[(240,560),(1050,560)],p['muted'],3);line(im,[(240,560),(240,260)],p['muted'],3)
   q=prog(t,.3,3.6);pts=[(240+x*740,560-240*x*x) for x in np.linspace(0,q,80)];line(im,pts,p['accent'],5)
   text(im,'y = x²',930,285,40,p['text']);text(im,'x',1100,560,25,p['text']);text(im,'y',240,230,25,p['text']);return im
  if pid=='MS08':return render_pl('PL14',t,{**cfg,'text':'FOLLOW THE CONNECTION'})
  im=component(*[MS[pid][n][0],local,cfg,MS[pid][n][1]])
  p=palette(cfg);rr(im,(30,25,330,80),rgba(p['bg'],230),12);text(im,'REPRESENTATIVE PACK DEMO',180,53,16,p['muted'])
  return im
 # Silent multi-beat ads with explicitly synthetic testimonial copy.
 im=base(cfg);p=palette(cfg);beat=min(4,int(t));local=(t-beat)*5
 if t==5:local=5
 if pid=='AD01':
  seq=[('PL01',{'items':['TOO MANY TABS?']}),('PL01',{'items':['NEED A CLEARER DAY?']}),('PL06',{}),('PL09',{}),('PL11',{'cta':'EXPLORE THE WORKSPACE'})]
 elif pid=='AD02':
  seq=[('PL03',{'thesis':'A NEW WAY TO CREATE'}),('PL12',{}),('PL05',{}),('PL09',{}),('PL11',{})]
 else:
  if beat in (0,1,2,3):
   rr(im,(180,215,1100,585),p['panel'],32);circle(im,295,350,52,p['accent']);text(im,'A',295,350,48,p['bg'])
   quote=['"One clear workspace."','"I can see the next step."','"A calmer way to plan."','SAMPLE TESTIMONIAL'][beat]
   text(im,quote,735,350,fit_size(quote,650,43),p['text'],opacity=enter(local,.2,.8));text(im,'FICTIONAL DEMO / NOT A CUSTOMER REVIEW',640,510,20,p['muted']);return im
  seq=[None,None,None,None,('PL11',{})]
 target,over=seq[beat]
 return render_pl(target,local,{**cfg,**over,'text':'MOTION WORKSPACE'})
