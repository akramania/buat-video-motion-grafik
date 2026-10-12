"""Original long-hold motion scenes. Every cue is in seconds, not scene percentage.

The stage stays anchored while short local actions build the story.  Artwork is
drawn here from geometry; it does not include the reference character or assets.
"""
from core import *
from long_scene_tools import cue, progress
from functools import lru_cache


PRESETS = {
 'L01': dict(name='Hero Orbit Ensemble', genre='saas',
  genres=['saas','corporate','education','promo','creator'],
  description='Satu pentas kekal, tajuk tebal, drone geometri asli, orbit berlapis dan ciri muncul mengikut beat.',
  text='IDEA BESAR.\nGERAK PANTAS.', subtitle='Susun idea menjadi sesuatu yang jelas.',
  eyebrow='RUANG UNTUK IDEA', items=['FOKUS','SUSUN','HASIL'],
  summary='SEMUA ELEMEN SEIRAMA', trail_label='IDEA  /  STRUKTUR  /  TINDAKAN',
  time_mode='seconds', duration=16, min_duration=16, end_behavior='hold',
  cue_defaults={'title':0.25,'underline':1.2,'features':2.4,'orbit':4.6,'detail':7.1,'focus':10.4,'resolve':13.2}),
 'L02': dict(name='Task Conveyor', genre='saas',
  genres=['saas','corporate','education','promo'],
  description='Aliran jubin pada pentas tetap, paket bergerak sepanjang laluan dan dashboard berubah dalam beberapa beat.',
  text='BANYAK TUGAS. SATU ALIRAN.', subtitle='Lihat setiap langkah bergerak ke hadapan.',
  items=['RINGKAS','SUSUN','SEMAK','VISUAL','SIAP'],
  summary='ALIRAN LENGKAP', stage_labels=['SUSUN INPUT','PROSES BERMULA','BATCH SETERUSNYA'],
  time_mode='seconds', duration=16, min_duration=16, end_behavior='hold',
  cue_defaults={'title':0.2,'stage':0.7,'tiles':2.0,'process':3.4,'batch':6.8,'accelerate':9.5,'resolve':12.8}),
 'L03': dict(name='Benchmark Race', genre='corporate',
  genres=['corporate','education','saas','promo'],
  description='Bar data demo kekal pada tempatnya; nilai pertama, kemas kini kedua dan bukti muncul sebagai beat berasingan.',
  text='LIHAT PERUBAHANNYA.', subtitle='Dua set nilai. Satu pandangan yang jelas.',
  summary='4 METRIK • SATU CERITA',
  items=['KUALITI','KELAJUAN','KONSISTENSI','LIPUTAN'],
  initial_values=[42,58,36,51], values=[79,86,68,91], value_suffix='%', max_value=100,
  time_mode='seconds', duration=16, min_duration=16, end_behavior='hold',
  cue_defaults={'title':0.2,'rows':1.0,'first':2.0,'marker':5.3,'second':7.1,'evidence':10.5,'resolve':13.2}),
}


def _pr(t,cfg,key,default,length=.65):
 return progress(t,cue(cfg,key,default),length,cfg)


def _words(cfg,key,defaults,count):
 value=cfg.get(key,defaults)
 if not isinstance(value,(tuple,list)): value=defaults
 values=[str(x).replace('\n',' ')[:40] for x in value]
 return (values+list(defaults))[:count]


def _rows(value,n=2):
 rows=[s.strip() for s in str(value).splitlines() if s.strip()]
 if not rows:return ['']
 if len(rows)>1:return rows[:n]
 words=rows[0].split()
 if len(words)<3:return rows
 mid=(len(words)+1)//2
 return [' '.join(words[:mid]),' '.join(words[mid:])]


def _text_left(im,s,x,y,width,size,color,opacity=1,face='bold'):
 text(im,s,x,y,fit_size(s,width,size,face),color,face,opacity=opacity,anchor='left')


def _stroke(im,pts,fraction,color,width=2):
 if len(pts)<2 or fraction<=0:return
 k=clamp(fraction)*(len(pts)-1);i=int(k);out=pts[:i+1]
 if i<len(pts)-1:out=out+[(mix(pts[i][0],pts[i+1][0],k-i),mix(pts[i][1],pts[i+1][1],k-i))]
 if len(out)>1:line(im,out,color,width)


def _star(im,x,y,r,color,angle=0):
 pts=[]
 for j in range(8):
  a=angle+j*math.pi/4;d=r if j%2==0 else r*.29
  pts.append((x+d*math.cos(a),y+d*math.sin(a)))
 ImageDraw.Draw(im).polygon(pts,fill=color)


def _ink(color):
 vals=[v/255 for v in rgb(color)]
 vals=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in vals]
 luminance=.2126*vals[0]+.7152*vals[1]+.0722*vals[2]
 return '#102039' if luminance>.21 else '#FFFFFF'


@lru_cache(maxsize=16)
def _halo(color,size=380):
 im=layer(size,size);circle(im,size/2,size/2,size*.25,rgba(color,29))
 return im.filter(ImageFilter.GaussianBlur(size*.11))


@lru_cache(maxsize=48)
def _chip(s,fill,ink,accent,w=172,h=50):
 im=layer(w+60,h+60);paste(im,panel(w,h,fill,15,accent),im.width/2,im.height/2)
 text(im,s,im.width/2+7,im.height/2,fit_size(s,w-48,17),ink)
 circle(im,47,im.height/2,4,accent)
 return im


@lru_cache(maxsize=16)
def _drone_shell(panel_color,accent,secondary):
 """Original friendly survey drone: rounded cuboid, side pods and aerial."""
 im=layer(300,285)
 # Ambient shadow, rear geometry, body bevel, face glass, specular edge.
 shadow=layer(300,285);rr(shadow,(52,82,247,246),(0,0,0,115),49)
 im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16)))
 d=ImageDraw.Draw(im)
 d.polygon([(61,105),(27,92),(21,169),(58,181)],fill=secondary)
 d.polygon([(237,105),(271,92),(278,168),(240,181)],fill=secondary)
 line(im,[(31,105),(30,158)],rgba('#FFFFFF',100),3)
 line(im,[(267,105),(270,158)],rgba('#FFFFFF',100),3)
 rr(im,(57,55,241,225),accent,45)
 rr(im,(63,61,236,217),secondary,41)
 rr(im,(70,68,229,207),panel_color,35)
 rr(im,(82,93,218,173),'#10182B',28,'#53617B',2)
 line(im,[(84,79),(201,79)],rgba('#FFFFFF',130),3)
 line(im,[(151,34),(151,58)],secondary,5)
 circle(im,151,28,8,accent)
 rr(im,(109,196,191,202),rgba(accent,90),3)
 return im


def _drone(im,x,y,t,p,opacity=1,scale=1):
 bot=_drone_shell(p['panel'],p['accent'],p['secondary']).copy()
 blink_phase=t%4.7
 blink=1-.9*math.exp(-((blink_phase-3.72)/.085)**2)
 gaze=3*math.sin(t*.71)
 for xx in [120,181]:
  rr(bot,(xx-9+gaze,124-13*blink,xx+9+gaze,124+13*blink),p['accent'],7)
  if blink>.6:circle(bot,xx+gaze+3,119,2,'#FFFFFF')
 # A calm smile and a local activity LED are independently animated.
 arc=[(143+14*math.cos(a),148+7*math.sin(a)) for a in np.linspace(0,math.pi,24)]
 line(bot,arc,p['secondary'],2)
 circle(bot,208,193,3,rgba(p['accent'],160+75*math.sin(t*2.6)))
 paste(im,bot,x,y,opacity,scale,math.sin(t*.8)*1.8)


def _l01(t,cfg):
 p=palette(cfg);im=base(cfg)
 title_start=cue(cfg,'title',.25)
 reveal=ease(progress(t,title_start,.6,cfg))
 paste(im,_halo(p['secondary'],490),953,333,reveal)
 # Fixed orbit stage forms a quieter back plane behind the drone.
 orbit_start=cue(cfg,'orbit',4.6)
 orbit_on=ease(progress(t,orbit_start,.65,cfg))
 cx,cy=942,341
 for j in range(3):
  pts=[(cx+(173+j*22)*math.cos(a),cy+(65+j*23)*math.sin(a)) for a in np.linspace(0,math.tau,121)]
  line(im,pts,rgba(p['secondary'],(19+j*4)*reveal),1)
 # Cards that are at the rear of the orbit are drawn before the character.
 for back in [True,False]:
  if not back:
   bob=5*math.sin(t*1.55)+2*math.sin(t*.4)
   _drone(im,cx,cy+bob,t,p,reveal,.94+.06*reveal)
  for j,label in enumerate(['+','Aa','✓']):
   a=(t-orbit_start)*.42+j*math.tau/3
   front=math.sin(a)>0
   if back==front:continue
   xx=cx+192*math.cos(a);yy=cy+94*math.sin(a)
   z=.82+.17*(math.sin(a)+1)/2
   tile=layer(95,95);paste(tile,panel(49,49,p['panel'],14,p['secondary']),47,47)
   text(tile,label,47,46,25,p['accent'])
   paste(im,tile,xx,yy,orbit_on,z,math.sin(a)*8)
 # One title with sequential lines, not a page replacement.
 eyebrow=str(cfg.get('eyebrow','RUANG UNTUK IDEA'))[:50]
 _text_left(im,eyebrow,72,181,580,17,p['accent'],reveal,'mono')
 rows=_rows(cfg.get('text','IDEA BESAR.\nGERAK PANTAS.'))
 size=min(fit_size(s,646,56) for s in rows)
 for j,s in enumerate(rows):
  q=ease(progress(t,title_start+.10+j*.19,.58,cfg))
  text(im,s,72,252+j*67+(1-q)*23,size,p['text'],opacity=q,anchor='left')
 underline=ease(_pr(t,cfg,'underline',1.2,.6))
 line(im,[(73,357),(73+min(600,max(measure(s,size) for s in rows))*underline,357)],p['accent'],5)
 _text_left(im,cfg.get('subtitle',''),74,392,614,21,p['muted'],ease(progress(t,1.5,.6,cfg)),'sans')
 items=_words(cfg,'items',['FOKUS','SUSUN','HASIL'],3)
 fs=cue(cfg,'features',2.4)
 for j,s in enumerate(items):
  q=ease(progress(t,fs+j*.28,.5,cfg));yy=466+(1-q)*19
  # Soft card shadow is cached; only the local card position moves.
  paste(im,_chip(s,p['panel'],p['text'],p['secondary'],184,51),169+j*204,yy,q)
  focus=cue(cfg,'focus',10.4)+j*.66
  pulse=math.sin(math.pi*progress(t,focus,.5,cfg)) if focus<=t<=focus+.5/max(.01,float(cfg.get('tempo',1))) else 0
  if pulse>0:rr(im,(77+j*204,yy-26,261+j*204,yy+26),None,15,rgba(p['accent'],220*pulse),2)
 # Supporting narrative beat with an independent left-to-right signal rail.
 ds=cue(cfg,'detail',7.1);detail=ease(progress(t,ds,.48,cfg))
 for j in range(5):
  xx=92+j*91
  line(im,[(xx,540),(xx+59,540)],rgba(p['secondary'],75*detail),2)
  q=ease(progress(t,ds+j*.22,.32,cfg))
  circle(im,xx,540,5,p['accent'] if q>.9 else rgba(p['muted'],100*detail))
  if q>0:line(im,[(xx,540),(xx+59*q,540)],rgba(p['accent'],180*detail),2)
 _text_left(im,str(cfg.get('trail_label','IDEA  /  STRUKTUR  /  TINDAKAN')),72,569,555,14,p['muted'],detail,'mono')
 resolve=ease(_pr(t,cfg,'resolve',13.2,.45))
 if resolve:
  rr(im,(795,542,1149,593),rgba(p['accent'],22*resolve),15,rgba(p['accent'],85*resolve),1)
  summary=str(cfg.get('summary','SEMUA ELEMEN SEIRAMA'))
  text(im,summary,972,566,fit_size(summary,322,17),p['accent'],opacity=resolve)
 for j in range(4):
  q=ease(progress(t,orbit_start+1+j*.3,.5,cfg))
  _star(im,770+j*119,217+18*math.sin(j*2+t*.3),5+j%2*2,rgba(p['secondary'],140*q),t*.1)
 return im


@lru_cache(maxsize=96)
def _task_tile(s,fill,ink,accent):
 im=layer(206,122);paste(im,panel(158,72,fill,18,accent),103,60)
 rr(im,(42,40,64,62),accent,7)
 line(im,[(48,47),(57,47)],ink,2);line(im,[(48,53),(57,53)],ink,2)
 text(im,s,124,51,fit_size(s,88,16),ink)
 text(im,'TUGAS DEMO',124,73,9,ink,'mono')
 return im


def _packet(im,pts,fraction,color):
 # Equidistant interpolation keeps speed constant around route corners.
 lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(pts,pts[1:])]
 dist=(fraction%1)*sum(lengths)
 for a,b,n in zip(pts,pts[1:],lengths):
  if dist<=n:
   q=dist/max(.001,n);x=mix(a[0],b[0],q);y=mix(a[1],b[1],q)
   circle(im,x,y,7,rgba(color,35));circle(im,x,y,3,color);return
  dist-=n


def _l02(t,cfg):
 p=palette(cfg);im=base(cfg);title=ease(_pr(t,cfg,'title',.2,.55))
 _text_left(im,cfg.get('text',''),68,171,1090,39,p['text'],title)
 _text_left(im,cfg.get('subtitle',''),71,214,1060,20,p['muted'],ease(progress(t,.6,.5,cfg)),'sans')
 stage=ease(_pr(t,cfg,'stage',.7,.6));process_start=cue(cfg,'process',3.4)
 # Connector layer stays fixed while packets travel along its paths.
 paths=[[(270,339),(336,339),(336,349),(404,349)],[(887,349),(947,349),(947,339),(1011,339)]]
 for j,pts in enumerate(paths):
  line(im,pts,rgba(p['secondary'],83*stage),2)
  if t>process_start:
   for k in range(3):_packet(im,pts,(t-process_start)*.32+k/3-j*.25,p['accent'])
 # Source and result are independent animated modules.
 for side,xx in enumerate([175,1102]):
  q=ease(progress(t,.8+side*.2,.48,cfg))
  paste(im,panel(183,161,p['panel'],23,p['secondary']),xx,347+(1-q)*20,q)
  text(im,'MASUK' if side==0 else 'SELESAI',xx,293,14,p['muted'],'mono',opacity=q)
  count=max(0,min(24,int(max(0,t-process_start)*1.2+max(0,t-cue(cfg,'accelerate',9.5)))))
  text(im,f'{count+3:02d}' if side==0 else f'{count:02d}',xx,347,50,p['text'] if side==0 else p['accent'],opacity=q)
  text(im,'TUGAS DEMO',xx,399,11,p['muted'],'mono',opacity=q)
 # Central dashboard, with header, surface glass and three live work rows.
 panel_layer=layer(538,296)
 paste(panel_layer,panel(478,236,p['panel'],26,p['secondary']),269,148)
 rr(panel_layer,(47,43,491,75),rgba(p['secondary'],22),9)
 for j,c in enumerate([p['accent'],p['secondary'],p['muted']]):circle(panel_layer,61+j*16,59,3,c)
 text(panel_layer,'WORKFLOW / LIVE',158,59,12,p['muted'],'mono',anchor='left')
 items=_words(cfg,'items',['RINGKAS','SUSUN','SEMAK','VISUAL','SIAP'],5)
 batch_start=cue(cfg,'batch',6.8)
 rowstarts=[process_start+j*.9 for j in range(3)]
 update=ease(progress(t,batch_start,.5,cfg))
 for j in range(3):
  yy=109+j*53
  row_batch=batch_start+j*.22
  text(panel_layer,items[j if t<row_batch+.25/max(.01,float(cfg.get('tempo',1))) else (j+2)%5],60,yy,15,p['text'],anchor='left')
  rr(panel_layer,(224,yy-7,445,yy+7),rgba(p['muted'],30),7)
  if t<row_batch:q=ease(progress(t,rowstarts[j],1.45,cfg))
  else:
   retract=1-smooth(progress(t,row_batch,.25,cfg))
   refill=ease(progress(t,row_batch+.3/max(.01,float(cfg.get('tempo',1))),1.65,cfg))
   q=max(retract,refill)
  rr(panel_layer,(224,yy-7,224+max(.1,221*q),yy+7),p['accent'] if j%2==0 else p['secondary'],7)
  text(panel_layer,f'{round(q*100):02d}',477,yy,13,p['accent'],'mono',anchor='right')
  if q>=.99:
   line(panel_layer,[(459,yy+7),(463,yy+11),(470,yy+3)],p['accent'],2)
 paste(im,panel_layer,646,358+(1-stage)*26,stage)
 # Four beats keep the composition but change its message.
 step=0 if t<process_start else 1 if t<batch_start else 2 if t<cue(cfg,'resolve',12.8) else 3
 labels=_words(cfg,'stage_labels',['SUSUN INPUT','PROSES BERMULA','BATCH SETERUSNYA'],3)+[str(cfg.get('summary','ALIRAN LENGKAP'))]
 q=ease(progress(t,[.8,process_start,batch_start,cue(cfg,'resolve',12.8)][step],.3,cfg))
 text(im,labels[step],643,489,fit_size(labels[step],550,14,'mono'),p['accent'],'mono',opacity=q)
 # Conveyor uses its own clipped layer. Local tiles remain swift in a 16s scene.
 band=layer(1144,125);draw=ImageDraw.Draw(band)
 line(band,[(0,62),(1143,62)],rgba(p['secondary'],65*stage),2)
 tile_start=cue(cfg,'tiles',2.0);q=ease(progress(t,tile_start,.55,cfg))
 elapsed=max(0,t-tile_start);accel=cue(cfg,'accelerate',9.5)
 # Continuous displacement at acceleration cue, with no position jump.
 displacement=elapsed*79+max(0,t-accel)*29
 for j in range(9):
  x=((j*194+displacement)%(194*9))-215
  colors=[p['accent'],p['secondary'],'#EFB58D']
  tile=_task_tile(items[j%5],colors[j%3],_ink(colors[j%3]),colors[(j+1)%3])
  paste(band,tile,x,65+math.sin(j+t*.7)*2,q,angle=math.sin(j+t*.43)*1.5)
 # Fade only within the conveyor lane, preserving labels and title.
 mask=Image.new('L',band.size,255);md=ImageDraw.Draw(mask)
 for x in range(75):
  md.line((x,0,x,124),fill=round(255*x/75))
  md.line((1143-x,0,1143-x,124),fill=round(255*x/75))
 band.putalpha(Image.fromarray(np.uint8(np.array(band.getchannel('A'),dtype=np.float32)*np.array(mask,dtype=np.float32)/255)))
 paste(im,band,640,568)
 return im


def _numbers(cfg,key,defaults,n):
 arr=cfg.get(key,defaults)
 if not isinstance(arr,(tuple,list)):arr=defaults
 out=[]
 for i in range(n):
  try:v=float(arr[i])
  except (IndexError,ValueError,TypeError):v=defaults[i]
  if not math.isfinite(v) or v<0:raise ValueError(key+' must contain finite nonnegative chart values')
  out.append(v)
 return out


def _num(v,suffix):
 return (f'{v:.1f}'.rstrip('0').rstrip('.') if abs(v-round(v))>.05 else str(round(v)))+suffix


def _l03(t,cfg):
 p=palette(cfg);im=base(cfg)
 a=ease(_pr(t,cfg,'title',.2,.55))
 _text_left(im,cfg.get('text',''),74,170,920,39,p['text'],a)
 _text_left(im,cfg.get('subtitle',''),76,211,1000,20,p['muted'],ease(progress(t,.6,.5,cfg)),'sans')
 # The visible badge explicitly prevents demo data from becoming a real claim.
 rr(im,(1090,152,1214,187),rgba(p['accent'],25*a),12,rgba(p['accent'],90*a))
 text(im,'DATA DEMO',1152,170,13,p['accent'],'mono',opacity=a)
 items=_words(cfg,'items',['KUALITI','KELAJUAN','KONSISTENSI','LIPUTAN'],4)
 initial=_numbers(cfg,'initial_values',[42,58,36,51],4)
 final=_numbers(cfg,'values',[79,86,68,91],4)
 maximum=float(cfg.get('max_value',100))
 if not math.isfinite(maximum) or maximum<=0:raise ValueError('max_value must be finite and positive')
 maximum=max(maximum,max(initial+final));suffix=str(cfg.get('value_suffix','%'))[:8]
 row_start=cue(cfg,'rows',1.0);first=cue(cfg,'first',2.0);second=cue(cfg,'second',7.1)
 update_on=t>=second
 plot_left=393;plot_width=655
 # Grid behind inset row panels establishes one continuous chart stage.
 for j in range(5):
  xx=plot_left+j*plot_width/4
  line(im,[(xx,244),(xx,539)],rgba(p['muted'],28*a),1)
  text(im,_num(maximum*j/4,''),xx,546,10,p['muted'],'mono',opacity=a)
 for j,label in enumerate(items):
  y=284+j*67;row_on=ease(progress(t,row_start+j*.12,.42,cfg))
  paste(im,panel(1117,53,p['panel'],13,None),640,y+(1-row_on)*12,row_on)
  _text_left(im,label,108,y,244,18,p['text'],row_on)
  rr(im,(plot_left,y-8,plot_left+plot_width,y+8),rgba(p['muted'],30*row_on),8)
  q=ease(progress(t,first+j*.22,.95,cfg));value=initial[j]*q
  if update_on:
   q2=ease(progress(t,second+j*.2,1.04,cfg));value=mix(initial[j],final[j],q2)
   # Initial-set marker remains anchored and establishes a visual comparison.
   oldx=plot_left+initial[j]/maximum*plot_width
   line(im,[(oldx,y-15),(oldx,y+15)],rgba(p['secondary'],180*row_on),2)
  width=plot_width*value/maximum
  if width>0:
   rr(im,(plot_left,y-8,plot_left+width,y+8),p['accent'] if update_on else p['secondary'],8)
   line(im,[(plot_left+7,y-5),(plot_left+max(7,width-7),y-5)],rgba('#FFFFFF',80),1)
  text(im,_num(value,suffix),1149,y,22,p['accent'] if update_on else p['text'],opacity=row_on,anchor='right')
  focus=cue(cfg,'evidence',10.5)+j*.48
  qf=progress(t,focus,.35,cfg)
  if t>=focus:
   # Small local evidence ticks enter quickly, then hold for reading.
   xx=1184;yy=y
   line(im,[(xx-6,yy),(xx-2,yy+5),(xx+7,yy-6)],rgba(p['accent'],255*ease(qf)),3)
 # A marker object supplies secondary motion without moving the chart itself.
 mark=cue(cfg,'marker',5.3);m=ease(progress(t,mark,.48,cfg))
 pointer_x=393+655*clamp(.2+.6*smooth(progress(t,mark,1.3,cfg)))
 if t<second:
  circle(im,pointer_x,241,8,rgba(p['secondary'],50*m))
  _star(im,pointer_x,241,5,rgba(p['secondary'],255*m),t*.4)
 else:
  pointer_x=393+655*(.25+.55*smooth(progress(t,second,1.5,cfg)))
  circle(im,pointer_x,241,8,rgba(p['accent'],50))
  _star(im,pointer_x,241,5,p['accent'],t*.4)
 # Status changes only in this small footer, never by replacing the whole scene.
 if t<second:status='SET 01  /  NILAI AWAL';sc=p['secondary']
 elif t<cue(cfg,'evidence',10.5):status='SET 02  /  NILAI DIKEMAS KINI';sc=p['accent']
 else:status='SET 01  →  SET 02  /  PERBANDINGAN';sc=p['accent']
 _text_left(im,status,86,592,720,16,sc,ease(progress(t,first,.4,cfg)),'mono')
 resolve=ease(_pr(t,cfg,'resolve',13.2,.42))
 if resolve:
  rr(im,(928,565,1210,614),rgba(p['accent'],22*resolve),15,rgba(p['accent'],85*resolve))
  summary=str(cfg.get('summary','4 METRIK • SATU CERITA'))
  text(im,summary,1069,589,fit_size(summary,252,15),p['accent'],opacity=resolve)
 return im


def render(pid,t,cfg):
 return {'L01':_l01,'L02':_l02,'L03':_l03}[pid](t,cfg)
