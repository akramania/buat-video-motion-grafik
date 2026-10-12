"""100 original premium map, route-camera and data infographic recipes.
Envato public listings informed categories only. Artwork and animation are original.
Maps, anatomy and telemetry are illustrative schematics; sample data is fictional.
Each render uses the normalized 0..5 clock and a 1280×720 canvas.
"""
from core import *
import math

SOURCES=[
 'https://elements.envato.com/map-route-animations-YBD3UMX',
 'https://elements.envato.com/canada-map-toolkit-3GXT9YP',
 'https://elements.envato.com/vox-map-documentary-45MRMKM',
 'https://elements.envato.com/panama-map-republic-of-panama-travel-map-UFDZHW7',
 'https://elements.envato.com/world-map-pro-travels-4TD6XUX',
 'https://elements.envato.com/norway-map-kingdom-of-norway-travel-map-RASHKVH',
 'https://elements.envato.com/speedometer-pack-K2VWGVL',
 'https://elements.envato.com/infographics-vertical-bars-TXJ9KM3',
 'https://elements.envato.com/ui-infographic-6SV9XWN',
 'https://elements.envato.com/infographics-W7P7MQJ',
 'https://elements.envato.com/modern-infographic-widgets-pack-clean-ui-kit-CVNA2KE',
 'https://elements.envato.com/process-flow-infographic-W3798EF',
 'https://elements.envato.com/heatmap-infographic-template-2DYTMWT',
 'https://elements.envato.com/infographic-pack-9X55V7T',
 'https://elements.envato.com/scientific-infographics-VP7UDFR',
 'https://elements.envato.com/hud-info-medical-panel-1-MJUYDDH',
 'https://elements.envato.com/hud-molecular-dna-KTTS2NV',
 'https://elements.envato.com/comparisson-infographic-powerpoint-template-J659HXN',
 'https://elements.envato.com/modern-infographics-U663PUY',
 'https://elements.envato.com/process-flowchart-infographic-ppt-JRGHNG8',
 'https://elements.envato.com/organizational-chart-presentation-infographic-9SQKVHL',
 'https://elements.envato.com/circle-arrows-icon-3d-abstract-EBAYPD5',
 'https://elements.envato.com/animated-hud-infographic-element-stock-market-cand-QNBY975',
 'https://elements.envato.com/process-flow-infographic-google-slides-S3L994M',
 'https://elements.envato.com/video-info-kit-V2CPYXS'
]
NAMES=[
 ['Rail Camera / Overhead Pursuit','Rail Camera / Banked Chase','Rail Camera / Horizon Corridor','Rail Camera / Descent to Destination'],
 ['Metro / Transfer Pulse','Network / Hub Dispatch','Metro / Interchange Weave','Rail / Branch Selection'],
 ['Coverage / Hex Field Sweep','Regions / Lifted Choropleth','Coverage / Radar Reach','Coverage / Contour Arrival'],
 ['Journey / Platform Milestones','Journey / Waypoint Flyby','Journey / Elevation Rail','Journey / ETA Ribbon'],
 ['Globe / Meridian Dispatch','Globe / Arc Constellation','Globe / Projection Unfold','Globe / Journey Inset'],
 ['Logistics / Parcel Convoy','Logistics / Last Mile Grid','Logistics / Ocean Corridor','Logistics / Drone Altitude'],
 ['Race / Lap Camera','Race / Sector Timeline','Race / Speed Heat Track','Race / Ghost Duel'],
 ['Bars / Ranked Ladder','Bars / Diverging Balance','Bars / Grouped Comparison','Bars / Composition Stacks'],
 ['Trend / Scanline Reveal','Trend / Multi Series Chase','Trend / Confidence Envelope','Trend / Ridgeline Layers'],
 ['Radial / Donut Assembly','Radial / Concentric Progress','Radial / Hierarchy Sunburst','Radial / Polar Columns'],
 ['KPI / Odometer Vault','KPI / Split Flap Ledger','KPI / Mechanical Dial','KPI / Perimeter Progress'],
 ['Flow / Ribbon Allocation','Flow / Conversion Funnel','Flow / Waterfall Bridge','Flow / Decision Branches'],
 ['Matrix / Heatmap Sweep','Matrix / Waffle Fill','Matrix / Calendar Intensity','Matrix / Correlation Focus'],
 ['Scatter / Bubble Trails','Scatter / Strategic Quadrants','Scatter / Population Swarm','Scatter / Ranked Dot Plot'],
 ['Science / Molecular Bond Build','Science / DNA Ribbon Scan','Science / Orbital Capture','Science / Harmonic Interference'],
 ['Engineering / Layer Cutaway','Engineering / Sensor Network','Engineering / Plant Pipeline','Engineering / Gauge Manifold'],
 ['Biology / Cell Callouts','Biology / Synaptic Relay','Biology / Specimen Carousel','Biology / Energy Cycle'],
 ['Compare / Delta Bridge','Compare / Before After Lens','Compare / Bullet Targets','Compare / Benchmark Ladder'],
 ['Dashboard / Bento Analytics','Dashboard / Command Deck','Dashboard / Scoreboard Stack','Dashboard / Newsroom Data'],
 ['Timeline / Cascade Chapters','Timeline / Milestone Ribbon','Timeline / Gantt Activation','Timeline / Clock Chronology'],
 ['Organisation / Reporting Tree','Organisation / Responsibility Matrix','Organisation / Hierarchy Pyramid','Organisation / Stakeholder Orbit'],
 ['Cycle / Flywheel Momentum','Cycle / Process Ring','Cycle / Feedback Circuit','Cycle / Lifecycle Stages'],
 ['Finance / Candlestick Scan','Finance / Orderbook Balance','Finance / Portfolio Weights','Finance / Compound Growth'],
 ['Systems / Architecture Packets','Systems / Layered Stack','Systems / Swimlane Handoff','Systems / Service Waterfall'],
 ['Editorial / Hero Statistic','Editorial / Pictogram Cascade','Editorial / Staircase Story','Editorial / Evidence Cards']
]
MECHANISMS=[
 ['World translates around a moving train with an overhead pursuit camera and route draw-on.','Oblique ground projection banks with heading while a train remains camera-centred.','Vanishing-point railway corridor advances toward camera with station gates and moving sleepers.','A wide schematic route descends through a smooth camera zoom to the destination marker.'],
 ['Two route lines draw independently and a transfer node emits timed rings.','A central interchange dispatches travelling packets along curved spokes.','Three intersecting metro lines weave under a central highlighted connection.','A train reaches a junction, pauses, then selects a highlighted branch.'],
 ['Staggered hexagonal cells gain data intensity under a travelling sweep.','Irregular schematic region slabs lift sequentially with quantitative callouts.','Concentric reach rings expand and a rotating radar wedge locates site markers.','Nested isochrone polygons expand outward with timed arrival labels.'],
 ['Platform stops advance through a connected milestone rail with a train shuttle.','Waypoint panels rise near a moving route marker with gated active-state focus.','An elevation area chart draws along a railway route with animated ascent marker.','An ETA ribbon counter advances concurrently with route progress and station handoffs.'],
 ['Rotating schematic meridians carry a route point around a globe silhouette.','A globe disk adds intercity arcs and rotating destination beacons.','A circular globe stretches into a wide cylindrical projection while a route transfers.','An inset globe overview hands off to a magnified curved journey path.'],
 ['A convoy of parcel nodes moves through a curved delivery route into endpoint stacks.','Orthogonal delivery streets animate a last-mile vehicle and staggered customer stops.','A vessel glides along a long ocean arc with wave parallax and port markers.','Drone altitude rises in a side profile then descends at a location grid.'],
 ['A track pursuit camera centres on a moving car while a lap rail progresses.','Track sectors reveal sequentially with a corresponding split-time timeline.','A racetrack gains speed-coloured segments while a telemetry needle follows the lap.','Two cars travel with different eased progress while a live gap readout changes.'],
 ['Ranked bars expand sequentially in descending order and settle exact values.','Positive and negative bars emerge from a common centreline with balance readout.','Paired bars grow together by group with labelled values and comparison markers.','Stacked category columns assemble segment by segment with total labels.'],
 ['An axis scan reveals a polyline and tracks the current value at the reveal head.','Three line series chase across a shared axis with independent end labels.','A line grows inside a translucent uncertainty envelope and resolves a final value.','Four filled ridgelines sweep in from back to front with separated row labels.'],
 ['Donut wedges assemble angularly and a centre total counts to the exact sum.','Independent concentric progress arcs sweep to separate exact target values.','Parent arcs and nested child arcs reveal as a hierarchy rather than one ring.','Radial columns extend from a circular baseline with aligned outside values.'],
 ['Staggered counters accumulate through a row of vault tiles and resolve exact digits.','A split-flap styled ledger sweeps a moving highlight above numeral seams before settling labelled targets.','A mechanical needle sweeps through a calibrated dial and resolves a value.','A card perimeter traces in four edge stages alongside its numeric counter.'],
 ['Width-weighted ribbons split from a source into proportional destinations.','Funnel trapezoids narrow by stage and consecutive conversion counts appear.','Positive and negative incremental columns connect into a final waterfall total.','A decision node grows into two branches then into four labelled leaves.'],
 ['A row-major scan fills matrix cells with scaled quantitative intensity.','A 10×10 waffle grid lights by exact percentage with a live counter.','A seven-column calendar staggers activity cells by week with legends.','A symmetric correlation matrix builds mirrored cells and highlights a chosen pair.'],
 ['Bubble points grow then travel on curved trails before reaching target coordinates.','Quadrant zones unfold and labelled strategy points settle into their positions.','A deterministic point swarm separates into four column populations.','Ranked dot rows connect to a baseline with lollipop stems and exact values.'],
 ['Molecular nodes appear in a staggered scaffold and bonds draw between them.','A rotating double helix slides behind a scanning bracket and readout cards.','Nested orbital tracks rotate particles around a central body with capture pulses.','Two wave signals propagate and an interference sum is built in a separate lane.'],
 ['A machine stack separates vertically to expose layers with leader-line callouts.','Sensor nodes connect in a topology and send moving readings to a central monitor.','A pipeline fills through tanks, a pump and a valve with phased flow packets.','Four calibrated gauges share a manifold and animate independent readings.'],
 ['A schematic cell membrane forms, organelles populate and callouts extend.','A neuron-shaped node relays a pulse to receptor branches through synaptic gaps.','Three specimen cards slide into a research carousel with active scan focus.','Four biological energy stages connect in a loop with circulating packets.'],
 ['Two headline values form a bridge and a signed delta expands between them.','A central comparison seam divides paired before-and-after bar scenes.','Bullet bars expand against background bands and explicit target markers.','Four benchmark rails build with sample markers against a common ruler.'],
 ['A bento dashboard staggers KPI, line, donut and ranked-bar modules.','A command deck sweeps through a signal plot, gauges and a timeline.','A tall scoreboard highlights rows in turn and counts their final metrics.','A newsroom layout assembles a hero value, map inset and three supporting bars.'],
 ['Offset chapter cards cascade down a zigzag route with matching connectors.','A timeline ribbon extends through four milestones and unveils anchored cards.','Staggered Gantt rows grow at different start positions under a moving cursor.','A circular clock chronology places events on fixed hour positions sequentially.'],
 ['A reporting tree grows from one leader to teams then to role nodes.','A responsibility grid reveals R,A,C,I cells per team and task.','Hierarchy trapezoids stack bottom-up and show levels in separated lanes.','Stakeholder nodes settle on two orbital rings with relationship links.'],
 ['A flywheel rotates with a changing speed and four inputs pointing toward its centre.','Four process arcs reveal clockwise then circulate a stage marker.','A forward chain is followed by a curved return circuit carrying feedback.','A lifecycle expands four differently sized stages around a loop.'],
 ['Candlestick bodies grow against a price grid and resolve to the supplied end-price tag.','Buy and sell volumes grow from a central orderbook seam with balance counts.','A portfolio ring and proportional allocation rows grow from supplied values.','Compound growth bars rise exponentially with a cumulative principal comparison.'],
 ['Architecture layers connect with routed packets and active endpoint focus.','Five stack cards fan in depth into a vertically layered service tower.','Three swimlanes pass an active job across lanes through timed connectors.','A service-waterfall timing chart staggers request bars by dependency start time.'],
 ['A huge statistic counts upward as supporting evidence lines reveal below it.','A pictogram array appears by cohort with an explicit highlighted share.','Four numbered steps build as a stair silhouette with rising captions.','Three evidence cards slide inward and link to a shared conclusion panel.']
]
PRESETS={}
for g in range(25):
 for v in range(4):
  pid=f'PX{101+g*4+v:03d}'
  schematic=g<7 or g in (14,15,16)
  PRESETS[pid]={
   'name':NAMES[g][v],'description':MECHANISMS[g][v]+(' Illustrative schematic, not surveyed geography or clinical illustration.' if schematic else ' Fictional demo data; replace with verified values.'),
   'genre':['corporate','saas','education','documentary'][g%4], 'text':NAMES[g][v].replace(' / ',' · '),'subtitle':'ILLUSTRATIVE SCHEMATIC' if schematic else 'CONFIGURABLE DATA · ORIGINAL DEMO',
   'family':'premium-map-data','duration':6,'source_url':SOURCES[g], 'observation_basis':'listing-description','mechanism':MECHANISMS[g][v],
   'variant_basis':'adapted','asset_types':['vector diagram','data values','labels']+(['normalised route coordinates'] if g<7 else []),
   'use_cases':(['rail and travel explainer','logistics','sports telemetry'] if g<7 else ['corporate report','education','data storytelling']),
   'parameters':{'values':'finite numeric array; exact endpoints; nonnegative for proportional charts','labels':'array of short names','route':'array of [x,y] pairs in 0..1 for map families','text':'headline','subtitle':'supporting line','unit':'counter suffix'},
   'adaptation_status':'original-demo','values':[64,86,73,92],'labels':['ALPHA','BETA','GAMMA','DELTA'],
   'recipe_group':g,'recipe_variant':v,'schematic':schematic,
   **({'price_series':[55,62,58,70,66,76,83,79,92,87,97,102]} if g==22 and v==0 else {}),
  }

def vals(cfg,n=4):
 raw=cfg.get('values',[64,86,73,92]);raw=raw if isinstance(raw,(list,tuple)) else [raw]
 arr=[]
 for x in raw:
  try:
   x=float(x)
   if math.isfinite(x):arr.append(x)
  except (ValueError,TypeError):pass
 if not arr:arr=[64,86,73,92]
 return (arr*((n+len(arr)-1)//len(arr)))[:n]
def labs(cfg,n=4):
 a=cfg.get('labels',['ALPHA','BETA','GAMMA','DELTA']);a=a if isinstance(a,(list,tuple)) and a else ['ALPHA','BETA','GAMMA','DELTA']
 return [str(a[i%len(a)])[:13] for i in range(n)]
def fmt(v):return f'{v:,.0f}' if abs(v-round(v))<.005 else f'{v:,.1f}'
def phase(t,delay=0):return smooth(prog(t,.25+delay,2.6+delay))
def poly(im,points,c,outline=None):
 d=ImageDraw.Draw(im);d.polygon([(round(x),round(y)) for x,y in points],fill=c)
 if outline:line(im,points+[points[0]],outline,2)
def arc(im,cx,cy,r,start,end,color,w=8):
 if end<=start:return
 pts=[(cx+r*math.cos(math.radians(a)),cy+r*math.sin(math.radians(a))) for a in np.linspace(start,end,max(3,int(abs(end-start)/3)+1))]
 line(im,pts,color,w)
def card(im,x,y,w,h,p):
 rr(im,(x+3,y+7,x+w+3,y+h+7),rgba('#000000',45),20)
 rr(im,(x,y,x+w,y+h),p['panel'],20,rgba(p['muted'],50))
def txt(im,s,x,y,p,size=26,col=None,anchor='center'):
 text(im,s,x,y,size,col or p['text'],anchor=anchor)
def small(im,s,x,y,p,anchor='center'):text(im,s,x,y,17,p['muted'],'mono',anchor=anchor)
def palette_ext(cfg):
 p=palette(cfg);p['third']='#F4B969';p['fourth']='#CE9AF2';return p
def colors(p):return [p['accent'],p['secondary'],p['third'],p['fourth']]
def grid(im,p,x=190,y=265,w=930,h=290):
 for i in range(5):line(im,[(x,y+i*h/4),(x+w,y+i*h/4)],rgba(p['muted'],45),1)
 line(im,[(x,y),(x,y+h),(x+w,y+h)],rgba(p['muted'],100),2)
def partial(points,f):
 if not points:return []
 lengths=[math.hypot(b[0]-a[0],b[1]-a[1]) for a,b in zip(points,points[1:])];total=sum(lengths)*clamp(f);out=[points[0]]
 for a,b,l in zip(points,points[1:],lengths):
  if total>=l:out.append(b);total-=l
  else:
   q=total/max(l,.0001);out.append((mix(a[0],b[0],q),mix(a[1],b[1],q)));break
 return out
def at(points,f):return partial(points,f)[-1]
def route(cfg):
 r=cfg.get('route');
 if isinstance(r,(list,tuple)) and len(r)>=2:
  try:return [(clamp(float(a[0]))*980+150,clamp(float(a[1]))*310+260) for a in r]
  except (ValueError,TypeError,IndexError):pass
 return [(170,530),(300,440),(435,465),(555,310),(710,350),(845,275),(1080,385)]
def mapground(im,p,project=lambda x,y:(x,y)):
 # Abstract district blocks intentionally do not portray a named country.
 for i in range(14):
  x=125+(i%7)*153;y=250+(i//7)*164;pts=[project(x,y),project(x+126,y+14),project(x+113,y+135),project(x+7,y+122)]
  poly(im,pts,rgba(p['secondary'],17),rgba(p['muted'],27))
 for i in range(8):line(im,[project(110+i*145,235),project(115+i*145,620)],rgba(p['muted'],50),2)
 for i in range(5):line(im,[project(95,245+i*80),project(1175,245+i*80)],rgba(p['muted'],45),2)
def vehicle(im,x,y,p,heading=0,train=True,scale=1):
 q=layer(140,54);d=ImageDraw.Draw(q);d.rounded_rectangle((6,9,124,44),radius=12,fill=p['accent']);d.polygon([(124,9),(137,27),(124,44)],fill=p['accent'])
 for i in range(4):d.rounded_rectangle((16+i*25,17,34+i*25,35),radius=3,fill=p['bg'])
 paste(im,q,x,y,scale=scale,angle=-heading)
def dot(im,x,y,p,r=8):circle(im,x,y,r+5,rgba(p['accent'],45));circle(im,x,y,r,p['accent'])
def header(im,t,cfg,p):
 q=ease(prog(t,0,.7));txt(im,cfg.get('text','DATA STORY'),70,170+15*(1-q),p,fit_size(cfg.get('text','DATA STORY'),1130,36),anchor='left')
 text(im,cfg.get('subtitle',''),72,208,16,p['muted'],'mono',anchor='left')

def maps(im,t,cfg,p,v):
 pts=route(cfg);f=phase(t);pos=at(pts,f);n=at(pts,min(1,f+.01));heading=math.degrees(math.atan2(n[1]-pos[1],n[0]-pos[0]));
 if v==2:
  # Genuine perspective corridor recipe: depth projected to vanishing point.
  horizon=290;cx=640+55*math.sin(t*.9);d=ImageDraw.Draw(im)
  poly(im,[(cx-22,horizon),(cx+22,horizon),(1050,617),(230,617)],rgba(p['accent'],13))
  for offset in [-.42,-.26,.26,.42]:line(im,[(cx+offset*30,horizon),(640+offset*760,617)],p['secondary'],4)
  for j in range(22):
   z=((j/22+t*.19)%1)**2;yy=mix(horizon,615,z);half=mix(12,240,z);line(im,[(cx-half,yy),(cx+half,yy)],rgba(p['muted'],130),max(1,int(z*4)))
  gate=phase(t)*.75+.12;gy=mix(horizon,570,gate**2);gw=mix(90,610,gate**2)
  line(im,[(cx-gw/2,gy+55),(cx-gw/2,gy),(cx+gw/2,gy),(cx+gw/2,gy+55)],p['accent'],5)
  txt(im,labs(cfg)[3],cx,gy-20,p,26);card(im,70,480,220,115,p);txt(im,fmt(vals(cfg)[3]*f),180,520,p,42);small(im,'ROUTE PROGRESS',180,565,p)
 elif v==3:
  zoom=mix(.83,1.85,smooth(prog(t,.6,3.4)));target=pts[-1];cx=mix(640,target[0],f);cy=mix(430,target[1],f)
  project=lambda x,y:((x-cx)*zoom+760,(y-cy)*zoom+430)
  mp=layer();mapground(mp,p,project);pp=[project(x,y) for x,y in pts];line(mp,pp,rgba(p['muted'],80),8);line(mp,partial(pp,f),p['accent'],8);dot(mp,*project(*pos),p)
  crop=mp.crop((350,238,1210,620));im.alpha_composite(crop,(350,238));card(im,70,270,255,300,p);txt(im,'ARRIVAL',198,315,p,30);txt(im,labs(cfg)[-1],198,379,p,26);txt(im,f'{round(f*100)}%',198,455,p,52);small(im,'CAMERA DESCENT',198,529,p)
 else:
  if v==0:
   zoom=mix(1,1.5,phase(t));project=lambda x,y:((x-pos[0])*zoom+700,(y-pos[1])*zoom+415)
  else:
   yaw=math.radians(-heading*.25);c=math.cos(yaw);s=math.sin(yaw)
   def project(x,y):
    xx=x-pos[0];yy=y-pos[1];a=xx*c-yy*s;b=xx*s+yy*c;depth=1+max(-.3,min(.35,b/1500));return 700+a*1.4/depth,420+b*.64/depth
  mp=layer();mapground(mp,p,project);pp=[project(x,y) for x,y in pts];line(mp,pp,rgba(p['secondary'],100),13);line(mp,partial(pp,f),p['accent'],6)
  for j,a in enumerate(pts):
   x,y=project(*a);circle(mp,x,y,8,p['panel'],p['secondary'],2)
   if j in [0,3,6]:small(mp,labs(cfg)[j%4],x,y-24,p)
  vehicle(mp,700,415,p,heading if v==0 else 0,scale=.8)
  im.alpha_composite(mp.crop((360,237,1210,617)),(360,237));card(im,70,270,270,300,p);small(im,'SCHEMATIC CAMERA',205,312,p);txt(im,f'{round(f*100)}%',205,384,p,65);small(im,'OVERHEAD FOLLOW' if v==0 else 'OBLIQUE CHASE',205,450,p);txt(im,labs(cfg)[int(min(3,f*4))],205,527,p,25)

def networks(im,t,cfg,p,v):
 f=phase(t);cols=colors(p);ls=labs(cfg)
 if v==0:
  a=[(170,510),(350,510),(510,340),(760,340),(1050,480)];b=[(215,285),(510,340),(670,545),(1085,545)]
  for k,r in enumerate([a,b]):line(im,r,rgba(cols[k],45),12);line(im,partial(r,phase(t,k*.3)),cols[k],7)
  for i,(x,y) in enumerate(a):circle(im,x,y,12,p['panel'],cols[0],3);small(im,ls[i%4],x,y+37,p)
  for rad in range(4):circle(im,510,340,18+rad*16+((t*20)%16),None,rgba(cols[1],max(15,130-rad*32)),2)
 elif v==1:
  center=(640,425);dest=[(250,290),(1050,290),(270,565),(1030,565)];circle(im,*center,55,p['panel'],p['accent'],4);txt(im,'HUB',640,425,p,24)
  for i,d in enumerate(dest):
   r=[center,(mix(center[0],d[0],.4),d[1]),d];line(im,partial(r,phase(t,i*.13)),cols[i],5);dot(im,*at(r,clamp((t-.6-i*.17)/3)),p);circle(im,*d,28,p['panel'],cols[i],3);small(im,ls[i],d[0],d[1]+48,p)
 elif v==2:
  paths=[[(130,340),(1140,340)],[(170,560),(580,340),(1100,240)],[(620,595),(620,250)]]
  for i,path in enumerate(paths):line(im,path,rgba(cols[i],40),14);line(im,partial(path,phase(t,i*.35)),cols[i],7)
  circle(im,620,340,35,p['bg'],p['text'],4);txt(im,'X',620,340,p,29)
  for i,(x,y) in enumerate([(280,340),(870,340),(400,437),(620,540)]):circle(im,x,y,9,p['text']);small(im,ls[i],x,y+33,p)
 else:
  a=[(135,470),(440,470),(640,395)];b=[(640,395),(1000,270)];c=[(640,395),(1090,560)];line(im,a,rgba(p['accent'],50),9);line(im,b,rgba(p['secondary'],60),8);line(im,c,rgba(p['muted'],60),8);line(im,partial(a,min(1,f*1.8)),p['accent'],7)
  follow=clamp((f-.56)/.44);line(im,partial(b,follow),p['accent'],7);pt=at(a,min(1,f*1.8)) if f<.56 else at(b,follow);vehicle(im,*pt,p,scale=.7);txt(im,'BRANCH A',1040,247,p,24);small(im,'BRANCH B',1080,596,p);circle(im,640,395,16,p['panel'],p['accent'],4)

def coverage(im,t,cfg,p,v):
 f=phase(t);vs=vals(cfg);cols=colors(p)
 if v==0:
  d=ImageDraw.Draw(im)
  for row in range(5):
   for col in range(11):
    x=220+col*73+(row%2)*36;y=285+row*61;intensity=((row*13+col*7)%20+5)/25;q=phase(t,(row+col)*.045)
    points=[(x+37*math.cos(math.pi/3*i),y+37*math.sin(math.pi/3*i)) for i in range(6)];poly(im,points,rgba(p['accent'],20+int(180*intensity*q)),rgba(p['muted'],65))
  txt(im,'COVERAGE',1060,385,p,22);txt(im,f'{round(f*100)}%',1060,446,p,48)
 elif v==1:
  for i in range(4):
   x=170+i*255;y=470-120*phase(t,i*.25);points=[(x,y-90),(x+135,y-110),(x+213,y-30),(x+172,y+65),(x+35,y+90)]
   poly(im,[(a,b+20) for a,b in points],rgba(cols[i],65));poly(im,points,rgba(cols[i],140),cols[i]);txt(im,fmt(vs[i]*phase(t,i*.2)),x+105,y,p,34);small(im,labs(cfg)[i],x+105,590,p)
 elif v==2:
  cx=650;cy=435
  for i in range(1,5):circle(im,cx,cy,40*i,None,rgba(p['accent'],50),2)
  a=t*1.8;poly(im,[(cx,cy),(cx+170*math.cos(a-.32),cy+170*math.sin(a-.32)),(cx+170*math.cos(a),cy+170*math.sin(a))],rgba(p['accent'],55))
  for i in range(4):x=cx+145*math.cos(i*1.5+.3);y=cy+140*math.sin(i*1.5+.3);circle(im,x,y,9*phase(t,i*.2)+1,cols[i]);small(im,labs(cfg)[i],x+28,y,p,'left')
  txt(im,'REACH',230,360,p,26);txt(im,fmt(vs[0]*f),230,420,p,58);small(im,'DEMO UNITS',230,475,p)
 else:
  for i in reversed(range(4)):
   r=55+i*44;pts=[(680+r*1.7*math.cos(a)*(1+.13*math.sin(a*3)),440+r*.8*math.sin(a)) for a in np.linspace(0,2*math.pi,40)];poly(im,[(mix(680,x,f),mix(440,y,f)) for x,y in pts],rgba(cols[i],35),rgba(cols[i],110))
  for i in range(4):small(im,f'{(i+1)*10} MIN',930,310+i*63,p,'left');circle(im,905,310+i*63,6,cols[3-i])
  dot(im,680,440,p,12);txt(im,'ARRIVAL ZONES',270,402,p,26);small(im,'SCHEMATIC ISOCHRONES',270,452,p)

def itinerary(im,t,cfg,p,v):
 f=phase(t);ls=labs(cfg);vs=vals(cfg)
 if v==0:
  pts=[(220,470),(500,470),(780,470),(1060,470)];line(im,pts,rgba(p['muted'],80),8);line(im,partial(pts,f),p['accent'],8)
  for i,(x,y) in enumerate(pts):q=phase(t,i*.3);circle(im,x,y,20*q+1,p['panel'],p['accent'],3);card(im,x-105,270,210,110,p);txt(im,ls[i],x,310,p,23);small(im,f'STOP {i+1:02d}',x,347,p)
  vehicle(im,*at(pts,f),p,scale=.6)
 elif v==1:
  pts=route(cfg);line(im,pts,rgba(p['muted'],75),7);line(im,partial(pts,f),p['accent'],5);dot(im,*at(pts,f),p,11)
  for i in range(4):x=170+i*278;q=phase(t,i*.4);card(im,x,535-70*q,232,100,p);txt(im,ls[i],x+116,568-70*q,p,23);small(im,'WAYPOINT '+str(i+1),x+116,603-70*q,p)
 elif v==2:
  grid(im,p);pts=[(180+i*925/19,540-(.25+.6*math.sin(i*.18)**2)*265*phase(t)) for i in range(20)];poly(im,[(180,555)]+pts+[(1105,555)],rgba(p['accent'],40));line(im,partial(pts,f),p['accent'],5);dot(im,*at(pts,f),p,11)
  card(im,800,245,320,85,p);txt(im,'ELEVATION '+fmt(vs[0]*f),960,283,p,26);small(im,'ILLUSTRATIVE PROFILE',650,598,p)
 else:
  pts=[(160,400),(400,400),(610,325),(830,450),(1120,450)];line(im,pts,rgba(p['secondary'],65),10);line(im,partial(pts,f),p['accent'],6);vehicle(im,*at(pts,f),p,scale=.7)
  card(im,160,525,960,77,p);rr(im,(175,540,175+930*f,590),rgba(p['accent'],40),12);txt(im,'ETA '+fmt((1-f)*vs[0])+' MIN',640,565,p,31)

def globes(im,t,cfg,p,v):
 f=phase(t);cx=480 if v==3 else 640;cy=430;r=168;d=ImageDraw.Draw(im)
 if v==2:
  q=phase(t);rx=mix(r,440,q);ry=mix(r,150,q);d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),fill=rgba(p['accent'],18),outline=rgba(p['accent'],140),width=3)
  for j in range(-3,4):x=cx+j*rx/4;line(im,[(x,cy-ry*math.sqrt(max(0,1-(j/4)**2))),(x,cy+ry*math.sqrt(max(0,1-(j/4)**2)))],rgba(p['muted'],90),2)
  pts=[(cx-rx*.75,cy+ry*.45),(cx,cy-ry*.4),(cx+rx*.72,cy)];line(im,partial(pts,f),p['secondary'],5);dot(im,*at(pts,f),p)
 else:
  circle(im,cx,cy,r,rgba(p['accent'],18),rgba(p['accent'],170),3)
  for j in range(-3,4):
   yr=cy+j*42;xr=math.sqrt(max(0,r*r-(yr-cy)**2));line(im,[(cx-xr,yr),(cx+xr,yr)],rgba(p['muted'],70),1)
  for j in range(5):
   width=abs(math.cos(t*.25+j*math.pi/5))*r;d.ellipse((cx-width,cy-r,cx+width,cy+r),outline=rgba(p['muted'],65),width=2)
  if v==0:
   a=-2+f*3.4;x=cx+math.sin(a)*r*.86;y=cy+math.cos(a)*80;arc(im,cx,cy,120,-160,-160+f*240,p['secondary'],5);dot(im,x,y,p,11)
  elif v==1:
   for i in range(4):
    a=-2.5+i*1.45;end=(cx+math.cos(a)*r*.83,cy+math.sin(a)*r*.83);pts=[(cx-110,cy+80),(cx+20,cy-130),end];line(im,partial(pts,phase(t,i*.2)),colors(p)[i],3);circle(im,*end,7,colors(p)[i])
  else:
   line(im,[(cx+r,cy),(770,cy),(800,330)],rgba(p['secondary'],140),3);card(im,805,272,345,292,p);pts=[(835,490),(920,345),(1085,380)];line(im,partial(pts,f),p['accent'],5);vehicle(im,*at(pts,f),p,scale=.48);small(im,'ZOOMED JOURNEY',970,534,p)
 if v!=3:small(im,'SCHEMATIC GLOBE · NO GEOGRAPHIC CLAIM',640,610,p)

def logistics(im,t,cfg,p,v):
 f=phase(t);pts=route(cfg);cols=colors(p)
 if v==0:
  line(im,pts,rgba(p['muted'],65),8);line(im,partial(pts,f),p['accent'],5)
  for i in range(5):x,y=at(pts,clamp(f-i*.08));rr(im,(x-15,y-15,x+15,y+15),cols[i%4],5);line(im,[(x,y-15),(x,y+15)],p['bg'],2)
 elif v==1:
  for y in [295,430,560]:line(im,[(155,y),(1120,y)],rgba(p['muted'],70),4)
  for x in [250,500,770,1020]:line(im,[(x,265),(x,600)],rgba(p['muted'],70),4)
  r=[(170,560),(500,560),(500,430),(770,430),(770,295),(1050,295)];line(im,partial(r,f),p['accent'],7);vehicle(im,*at(r,f),p,scale=.55)
  for i,(x,y) in enumerate([(250,295),(500,560),(770,430),(1020,295)]):card(im,x-40,y-65,80,50,p);txt(im,str(i+1),x,y-40,p,23)
 elif v==2:
  for j in range(6):pts2=[(120+i*12,310+j*48+8*math.sin(i*.15+t*.8+j)) for i in range(90)];line(im,pts2,rgba(p['secondary'],55),2)
  r=[(180,520),(330,380),(560,290),(800,300),(1080,470)];line(im,r,rgba(p['accent'],80),3);x,y=at(r,f);poly(im,[(x-32,y),(x+32,y),(x+20,y+23),(x-24,y+23)],p['accent']);rr(im,(x-20,y-20,x+16,y),p['secondary'],3)
  for x,y in [r[0],r[-1]]:circle(im,x,y,15,p['panel'],p['accent'],3)
 else:
  grid(im,p,170,300,930,260);r=[(170,540),(400,305),(790,305),(1100,540)];line(im,partial(r,f),p['accent'],4);x,y=at(r,f)
  line(im,[(x-40,y),(x+40,y)],p['secondary'],4)
  for dx in [-40,40]:circle(im,x+dx,y,16,None,p['accent'],3)
  rr(im,(x-16,y-12,x+16,y+12),p['accent'],5);small(im,'ALTITUDE PROFILE',640,595,p)

def races(im,t,cfg,p,v):
 f=phase(t);track=[(300,390),(390,265),(690,280),(870,360),(970,530),(730,570),(580,470),(350,550),(300,390)];cols=colors(p)
 if v==0:
  pos=at(track,f);pr=lambda x,y:((x-pos[0])*1.3+715,(y-pos[1])*1.05+425);tr=[pr(x,y) for x,y in track];mp=layer();line(mp,tr,rgba(p['muted'],70),32);line(mp,partial(tr,f),p['accent'],6);vehicle(mp,715,425,p,train=False,scale=.5);im.alpha_composite(mp.crop((350,235,1195,620)),(350,235));card(im,80,290,250,240,p);txt(im,'LAP 01',205,335,p,34);txt(im,f'{round(f*100)}%',205,410,p,54);small(im,'TRACK CAMERA',205,484,p)
 elif v==1:
  line(im,track,rgba(p['muted'],80),20)
  for i in range(3):
   part=partial(track,(i+1)/3);prev=partial(track,i/3);seg=[prev[-1]]+part[len(prev):];line(im,partial(seg,phase(t,i*.3)),cols[i],6)
  vehicle(im,*at(track,f),p,scale=.45)
  for i in range(3):card(im,145+i*332,572,300,48,p);txt(im,f'S{i+1}  {fmt(vals(cfg)[i]*phase(t,i*.45))}',295+i*332,596,p,21)
 elif v==2:
  for i,(a,b) in enumerate(zip(track,track[1:])):line(im,[a,b],cols[i%4],14)
  pos=at(track,f);dot(im,*pos,p,12);card(im,925,255,275,165,p);txt(im,fmt(vals(cfg)[0]*f),1062,310,p,54);small(im,cfg.get('unit','DEMO SPEED'),1062,365,p)
  arc(im,1062,494,63,140,400,rgba(p['muted'],65),8);arc(im,1062,494,63,140,140+260*f,p['accent'],8)
 else:
  line(im,track,rgba(p['muted'],80),24);line(im,partial(track,f),p['accent'],4);x,y=at(track,f);vehicle(im,x,y,p,scale=.44);p2=dict(p);p2['accent']=p['secondary'];ghost=clamp(f*.91+.04);vehicle(im,*at(track,ghost),p2,scale=.38);card(im,865,255,300,120,p);txt(im,'GAP '+fmt(abs(f-ghost)*100),1015,305,p,36);small(im,'TWO VEHICLE DEMO',1015,351,p)

def bars(im,t,cfg,p,v):
 a=vals(cfg);ls=labs(cfg);mx=max(1,max(abs(x) for x in a));cols=colors(p)
 if v==0:
  order=sorted(range(4),key=lambda i:a[i],reverse=True)
  for rank,i in enumerate(order):q=phase(t,rank*.13);y=290+rank*80;small(im,ls[i],165,y+19,p,'right');rr(im,(205,y,205+800*max(0,a[i])/mx*q+1,y+39),cols[rank],10);txt(im,fmt(a[i]*q),1050,y+20,p,27)
 elif v==1:
  line(im,[(640,260),(640,585)],p['muted'],2)
  for i,x in enumerate(a):q=phase(t,i*.12);signed=x if i%2==0 else -x;w=abs(signed)/mx*380*q;y=285+i*79;rr(im,(640-w if signed<0 else 640,y,640 if signed<0 else 640+w,y+41),cols[i],8);small(im,ls[i],100,y+21,p,'left');txt(im,fmt(signed*q),1130,y+21,p,26)
 elif v==2:
  grid(im,p);b=vals({**cfg,'values':cfg.get('compare_values',[49,71,60,83])});mx=max(1,max(a+b))
  for i in range(4):x=260+i*232;q=phase(t,i*.15)
  for i in range(4):
   x=260+i*232;q=phase(t,i*.15)
   for j,val in enumerate([a[i],b[i]]):h=240*val/mx*q;rr(im,(x+j*62,555-h,x+49+j*62,555),cols[j],6);txt(im,fmt(val*q),x+24+j*62,540-h,p,20)
   small(im,ls[i],x+52,595,p)
 else:
  grid(im,p)
  for i,x in enumerate(a):
   cx=260+i*235;y=555;fractions=[.45,.32,.23]
   for j,r in enumerate(fractions):h=260*x/mx*r*phase(t,i*.1+j*.3);rr(im,(cx,y-h,cx+110,y),cols[j],4);y-=h
   txt(im,fmt(x*phase(t,i*.1+.6)),cx+55,y-23,p,24);small(im,ls[i],cx+55,595,p)

def lines(im,t,cfg,p,v):
 grid(im,p);f=phase(t);cols=colors(p);vs=vals(cfg,16);mx=max(1,max(abs(x) for x in vs));ls=labs(cfg)
 def points(series=0):return [(190+i*925/15,555-((vs[i]/mx)*.72+.08*math.sin(i*.8+series))*270) for i in range(16)]
 if v==0:
  pts=points();line(im,partial(pts,f),p['accent'],5);x,y=at(pts,f);line(im,[(x,265),(x,555)],rgba(p['secondary'],110),2);dot(im,x,y,p,8);card(im,850,270,240,70,p);txt(im,fmt(vs[min(15,int(f*15))]),970,305,p,30)
 elif v==1:
  for j in range(3):
   pts=[(x,y+j*35-25) for x,y in points(j)];line(im,partial(pts,phase(t,j*.3)),cols[j],4);x,y=pts[-1];txt(im,ls[j],x+30,y,p,18,cols[j],anchor='left')
 elif v==2:
  pts=points();qpts=partial(pts,f);poly(im,[(x,y-34) for x,y in qpts]+[(x,y+34) for x,y in reversed(qpts)],rgba(p['secondary'],40));line(im,qpts,p['accent'],5);dot(im,*qpts[-1],p,8);small(im,'DEMO UNCERTAINTY BAND',640,598,p)
 else:
  for j in range(4):
   yy=590-j*72;pts=[(190+i*925/30,yy-55*(.4+.6*math.sin(i*.18+j)**2)) for i in range(31)];qpts=partial(pts,phase(t,(3-j)*.2));poly(im,[(190,yy)]+qpts+[(qpts[-1][0],yy)],rgba(cols[j],65));line(im,qpts,cols[j],3);small(im,ls[j],165,yy-24,p,'right')

def radials(im,t,cfg,p,v):
 vs=[max(0,x) for x in vals(cfg)];total=max(1,sum(vs));cols=colors(p);f=phase(t);ls=labs(cfg)
 if v==0:
  start=-90
  for i,val in enumerate(vs):end=start+val/total*360;arc(im,450,425,145,start,mix(start,end,phase(t,i*.17)),cols[i],43);start=end
  txt(im,fmt(sum(vs)*f),450,415,p,55);small(im,'TOTAL',450,467,p)
 elif v==1:
  for i,val in enumerate(vs):r=155-i*31;arc(im,450,425,r,-90,270,rgba(p['muted'],35),18);arc(im,450,425,r,-90,-90+clamp(val/100)*360*phase(t,i*.2),cols[i],18)
  txt(im,'PROGRESS',450,422,p,23)
 elif v==2:
  start=-90
  for i,val in enumerate(vs):end=start+val/total*360;arc(im,450,425,104,start,mix(start,end,phase(t,i*.2)),cols[i],50);arc(im,450,425,158,start,mix(start,end-3,phase(t,i*.2+.3)),rgba(cols[i],140),42);start=end
  circle(im,450,425,57,p['panel']);txt(im,'ROOT',450,425,p,22)
 else:
  mx=max(1,max(vs));circle(im,450,425,74,None,rgba(p['muted'],80),2)
  for i in range(12):a=-math.pi/2+i*math.pi/6;value=vs[i%4];r=74+88*value/mx*phase(t,i*.04);line(im,[(450+74*math.cos(a),425+74*math.sin(a)),(450+r*math.cos(a),425+r*math.sin(a))],cols[i%4],20)
 for i in range(4):circle(im,810,295+i*85,7,cols[i]);small(im,ls[i],840,285+i*85,p,'left');txt(im,fmt(vs[i]*phase(t,i*.17)),840,318+i*85,p,32,anchor='left')

def kpis(im,t,cfg,p,v):
 vs=vals(cfg);ls=labs(cfg);f=phase(t);cols=colors(p)
 if v==0:
  for i in range(4):x=80+i*302;card(im,x,285,278,265,p);small(im,ls[i],x+139,330,p);value=vs[i]*phase(t,i*.22);num=fmt(value);txt(im,num,x+139,425,p,fit_size(num,245,65));small(im,cfg.get('unit','DEMO UNITS'),x+139,500,p)
 elif v==1:
  for i in range(4):x=110+i*285;q=phase(t,i*.2);card(im,x,310,250,185,p);txt(im,fmt(vs[i]*q),x+125,404,p,58);line(im,[(x+12,404),(x+238,404)],p['bg'],3);rr(im,(x+8,317,x+242,329+abs(math.sin(t*6+i))*25*(1-q)),rgba(p['secondary'],90),4);small(im,ls[i],x+125,543,p)
 elif v==2:
  cx=620;cy=480;r=176;arc(im,cx,cy,r,150,390,rgba(p['muted'],50),22)
  for i in range(11):a=math.radians(150+i*24);line(im,[(cx+(r-18)*math.cos(a),cy+(r-18)*math.sin(a)),(cx+(r+4)*math.cos(a),cy+(r+4)*math.sin(a))],p['secondary'],3)
  target=clamp(vs[0]/100);a=math.radians(150+240*target*f);line(im,[(cx,cy),(cx+142*math.cos(a),cy+142*math.sin(a))],p['accent'],6);circle(im,cx,cy,16,p['accent']);txt(im,fmt(vs[0]*f),620,552,p,46);small(im,ls[0],620,602,p)
 else:
  x=280;y=285;w=720;h=275;card(im,x,y,w,h,p);pts=[(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)];line(im,partial(pts,f),p['accent'],7);txt(im,fmt(vs[0]*f)+cfg.get('unit','%'),640,397,p,83);small(im,ls[0],640,484,p)

def flows(im,t,cfg,p,v):
 f=phase(t);vs=vals(cfg);ls=labs(cfg);cols=colors(p)
 if v==0:
  total=max(1,sum(max(0,z) for z in vs));card(im,95,325,225,195,p);txt(im,fmt(total*f),207,395,p,45);small(im,'INPUT',207,461,p)
  for i,val in enumerate(vs):y=285+i*88;r=[(320,420),(650,420),(850,y),(1000,y)];line(im,partial(r,phase(t,i*.13)),cols[i],max(8,round(50*max(0,val)/total)));rr(im,(1000,y-24,1190,y+24),rgba(cols[i],35),12);txt(im,ls[i],1095,y,p,21)
 elif v==1:
  mx=max(1,max(abs(x) for x in vs));
  for i,val in enumerate(vs):w=240+560*max(0,val)/mx;y=260+i*82;h=62*phase(t,i*.2);poly(im,[(640-w/2,y),(640+w/2,y),(640+w*.43,y+h),(640-w*.43,y+h)],rgba(cols[i],180));txt(im,ls[i]+'  '+fmt(val*phase(t,i*.2)),640,y+31,p,24)
 elif v==2:
  changes=cfg.get('changes',[60,24,-17,31]);changes=vals({'values':changes});total=0;mx=max(100,sum(abs(x) for x in changes));base=570
  grid(im,p)
  for i,val in enumerate(changes):prev=total;total+=val;x=235+i*180;q=phase(t,i*.3);y1=base-prev/mx*260;y2=base-(prev+val*q)/mx*260;rr(im,(x,min(y1,y2),x+95,max(y1,y2)+1),cols[i],5);line(im,[(x+95,base-total/mx*260),(x+180,base-total/mx*260)],rgba(p['muted'],90),2);txt(im,fmt(val*q),x+47,min(y1,y2)-23,p,22)
  rr(im,(1035,base-total/mx*260*f,1130,base),p['accent'],5);txt(im,fmt(total*f),1082,base-total/mx*260*f-25,p,26)
 else:
  root=(230,425);nodes=[(590,300),(590,550)];leaves=[(1040,255),(1040,365),(1040,480),(1040,590)];circle(im,*root,50,p['panel'],p['accent'],3);txt(im,'?',*root,p,34)
  for i,n in enumerate(nodes):line(im,partial([root,(420,425),(420,n[1]),n],phase(t,i*.2)),cols[i],4);circle(im,*n,35,p['panel'],cols[i],3);txt(im,'YES' if i==0 else 'NO',*n,p,19)
  for i,n in enumerate(leaves):start=nodes[i//2];line(im,partial([start,(810,start[1]),(810,n[1]),n],phase(t,.6+i*.1)),cols[i],3);rr(im,(n[0]-80,n[1]-23,n[0]+80,n[1]+23),p['panel'],10,cols[i]);txt(im,ls[i],*n,p,20)

def matrices(im,t,cfg,p,v):
 f=phase(t);cols=colors(p);vs=vals(cfg);d=ImageDraw.Draw(im)
 if v==1:
  for row in range(10):
   for col in range(10):idx=row*10+col;active=idx<round(clamp(vs[0]/100)*100*f);rr(im,(235+col*29,260+row*29,259+col*29,284+row*29),p['accent'] if active else rgba(p['muted'],40),4)
  txt(im,f'{round(clamp(vs[0]/100)*100*f)}%',860,390,p,82);small(im,'100 CELL SHARE',860,468,p)
 else:
  rows=5 if v==0 else (5 if v==2 else 6);ncols=7 if v==2 else 6
  for r in range(rows):
   for c in range(ncols):
    value=((min(r,c)*17+max(r,c)*11)%100)/100 if v==3 else ((r*23+c*17+14)%100)/100;q=phase(t,(r+c)*.045);x=270+c*105;y=265+r*62
    rr(im,(x,y,x+91,y+50),rgba(p['accent'],25+round(180*value*q)),7);txt(im,str(round(value*100)),x+45,y+25,p,18)
  if v==3:rr(im,(270+2*105,265+4*62,361+2*105,315+4*62),None,7,p['secondary'],4)
  for i in range(ncols):small(im,['M','T','W','T','F','S','S'][i] if v==2 else str(i+1),315+i*105,240,p)
  small(im,['INTENSITY SCAN','', 'ACTIVITY BY WEEK','SYMMETRIC CORRELATION'][v],640,610,p)

def scatters(im,t,cfg,p,v):
 f=phase(t);vs=vals(cfg);ls=labs(cfg);cols=colors(p)
 if v==3:
  for i,val in enumerate(vs):y=285+i*80;small(im,ls[i],190,y,p,'right');line(im,[(220,y),(1090,y)],rgba(p['muted'],40),2);x=220+clamp(val/100)*850*phase(t,i*.2);line(im,[(220,y),(x,y)],cols[i],5);circle(im,x,y,11,cols[i]);txt(im,fmt(val*phase(t,i*.2)),1140,y,p,26)
 elif v==2:
  for j in range(4):
   for i in range(28):x=230+j*270+((i*37)%95)-46;y=520-((i*19)%220);sx=640+(i%7)*10;sy=430+(i%5)*10;q=phase(t,j*.17);circle(im,mix(sx,x,q),mix(sy,y,q),6,cols[j])
   small(im,ls[j],230+j*270,590,p)
 else:
  grid(im,p);line(im,[(640,265),(640,555)],rgba(p['muted'],80),2);line(im,[(190,410),(1120,410)],rgba(p['muted'],80),2)
  if v==1:
   for i,(x,y) in enumerate([(195,270),(650,270),(195,415),(650,415)]):rr(im,(x,y,x+455,y+135),rgba(cols[i],15*phase(t,i*.15)),6)
  for i in range(12):
   xx=250+((i*137)%800);yy=290+((i*79)%230);q=phase(t,i*.035);x=mix(230,xx,q);y=mix(545,yy,q);r=10+(vs[i%4]/100)*15
   if v==0:line(im,[(230,545),(mix(230,xx,q*.6),mix(545,yy,q*.5)),(x,y)],rgba(cols[i%4],75),2)
   circle(im,x,y,max(2,r*q),rgba(cols[i%4],170))
  small(im,'SAMPLE POSITIONS · REPLACE WITH VERIFIED DATA',650,610,p)

def science(im,t,cfg,p,v):
 f=phase(t);cols=colors(p)
 if v==0:
  pts=[(390,360),(570,270),(755,375),(600,530),(865,530),(255,520)];edges=[(0,1),(1,2),(2,3),(3,0),(2,4),(0,5)]
  for i,(a,b) in enumerate(edges):line(im,partial([pts[a],pts[b]],phase(t,i*.08)),rgba(p['secondary'],170),10)
  for i,(x,y) in enumerate(pts):q=phase(t,i*.15);circle(im,x+4,y+9,39*q,rgba('#000000',70));circle(im,x,y,38*q+1,cols[i%4]);circle(im,x-10,y-12,11*q,rgba('#FFFFFF',80));small(im,['C','N','O','H','P','H'][i],x,y+61,p)
 elif v==1:
  left=[];right=[]
  for i in range(30):y=260+i*10;a=i*.38+t*.9;x=610+100*math.sin(a);x2=610-100*math.sin(a);left.append((x,y));right.append((x2,y));line(im,[(x,y),(x2,y)],rgba(p['muted'],90),3);circle(im,x,y,5,p['accent']);circle(im,x2,y,5,p['secondary'])
  line(im,left,p['accent'],4);line(im,right,p['secondary'],4);yy=265+300*f;line(im,[(460,yy),(760,yy)],p['third'],3);card(im,860,285,280,220,p);txt(im,'SCAN',1000,327,p,25);txt(im,f'{round(f*100)}%',1000,400,p,54);small(im,'DNA SCHEMATIC',1000,463,p)
 elif v==2:
  for i in range(3):
   rx=135+i*60;ry=45+i*30;pts=[(640+rx*math.cos(a),430+ry*math.sin(a)) for a in np.linspace(0,2*math.pi,90)];line(im,pts,rgba(cols[i],85),2);a=t*(.65+i*.25)+i*2;circle(im,640+rx*math.cos(a),430+ry*math.sin(a),12,cols[i])
  circle(im,640,430,48,p['panel'],p['accent'],4);txt(im,'CORE',640,430,p,20);arc(im,640,430,76,-90,-90+360*f,p['secondary'],3)
 else:
  for j in range(3):
   basey=300+j*122;points=[]
   for i in range(100):x=160+i*9.6;a=i*.16-t*2;value=math.sin(a) if j==0 else (.55*math.sin(a*1.3+1) if j==1 else math.sin(a)+.55*math.sin(a*1.3+1));points.append((x,basey-value*26*f))
   line(im,[(160,basey),(1120,basey)],rgba(p['muted'],55),1);line(im,points,cols[j],4);small(im,['SIGNAL A','SIGNAL B','SUM'][j],128,basey,p,'right')

def engineering(im,t,cfg,p,v):
 f=phase(t);cols=colors(p);vs=vals(cfg)
 if v==0:
  for i in reversed(range(4)):
   y=535-i*32-i*28*f;pts=[(370,y),(650,y-60),(910,y),(630,y+65)];poly(im,[(x,y+14) for x,y in pts],rgba(cols[i],65));poly(im,pts,rgba(cols[i],160),cols[i]);line(im,[(900,y),(1030,y),(1080,y)],cols[i],2);small(im,labs(cfg)[i],1090,y,p,'left')
 elif v==1:
  center=(650,430);nodes=[(245,290),(1040,290),(230,555),(1055,555)];rr(im,(570,370,730,490),p['panel'],15,p['accent'],3);txt(im,'MONITOR',650,430,p,22)
  for i,n in enumerate(nodes):path=[n,(n[0],430),center];line(im,path,rgba(cols[i],70),3);dot(im,*at(path,clamp((t*.35+i*.2)%1)),p);circle(im,*n,34,p['panel'],cols[i],3);txt(im,fmt(vs[i]*phase(t,i*.1)),*n,p,22);small(im,labs(cfg)[i],n[0],n[1]+53,p)
 elif v==2:
  pipe=[(180,430),(450,430),(450,530),(760,530),(760,340),(1080,340)];line(im,pipe,rgba(p['muted'],100),24);line(im,partial(pipe,f),p['accent'],12)
  for i,x in enumerate([180,620,1080]):rr(im,(x-48,275,x+48,460),p['panel'],17,p['secondary'],3);rr(im,(x-40,452-160*phase(t,i*.23),x+40,452),rgba(p['accent'],85),8);small(im,'TANK '+str(i+1),x,495,p)
  circle(im,450,430,35,p['panel'],p['third'],4);arrow(im,450,430,p['third']);small(im,'FLOW SCHEMATIC',660,603,p)
 else:
  line(im,[(170,505),(1120,505)],rgba(p['secondary'],90),14)
  for i,value in enumerate(vs):x=230+i*270;line(im,[(x,505),(x,375)],p['secondary'],5);circle(im,x,355,77,p['panel'],cols[i],3);a=math.radians(150+240*clamp(value/100)*phase(t,i*.14));line(im,[(x,355),(x+60*math.cos(a),355+60*math.sin(a))],cols[i],4);txt(im,fmt(value*phase(t,i*.14)),x,557,p,29);small(im,labs(cfg)[i],x,602,p)

def biology(im,t,cfg,p,v):
 f=phase(t);cols=colors(p)
 if v==0:
  pts=[(580+205*(1+.06*math.sin(a*5))*math.cos(a)*f,430+143*(1+.04*math.sin(a*7))*math.sin(a)*f) for a in np.linspace(0,2*math.pi,90)];poly(im,pts,rgba(p['accent'],22),p['accent']);circle(im,550,425,59*f,rgba(p['secondary'],70),p['secondary'],3)
  for i in range(5):a=i*1.3;x=580+135*math.cos(a);y=430+90*math.sin(a);circle(im,x,y,14*phase(t,i*.2)+1,cols[i%4]);line(im,[(x,y),(850,280+i*65),(930,280+i*65)],rgba(cols[i%4],170),2);small(im,'STRUCTURE '+str(i+1),945,280+i*65,p,'left')
 elif v==1:
  circle(im,320,430,48,p['panel'],p['accent'],4)
  for i in range(6):a=i*math.pi/3;line(im,[(320,430),(320+100*math.cos(a),430+100*math.sin(a))],p['accent'],4)
  path=[(370,430),(680,430),(735,380),(810,380)];line(im,path,p['secondary'],8);dot(im,*at(path,f),p,12)
  for i in range(4):y=280+i*93;line(im,partial([(850,380),(930,380),(1040,y)],phase(t,.55+i*.12)),cols[i],4);circle(im,1040,y,25,p['panel'],cols[i],3)
  small(im,'ILLUSTRATIVE SYNAPTIC RELAY',620,605,p)
 elif v==2:
  for i in range(3):x=100+i*380+30*(1-phase(t,i*.2));card(im,x,275,335,300,p);circle(im,x+167,387,68,rgba(cols[i],30),cols[i],3)
  for i in range(3):
   x=100+i*380+30*(1-phase(t,i*.2));yy=327+120*((t*.32+i*.18)%1);line(im,[(x+85,yy),(x+250,yy)],cols[i],2);txt(im,'SPECIMEN '+str(i+1),x+167,503,p,26);small(im,'SCHEMATIC SAMPLE',x+167,543,p)
 else:
  pts=[(390,290),(890,290),(890,560),(390,560),(390,290)];line(im,pts,rgba(p['muted'],70),5);line(im,partial(pts,f),p['accent'],5)
  for i,(x,y) in enumerate(pts[:-1]):circle(im,x,y,41,p['panel'],cols[i],4);txt(im,str(i+1),x,y,p,27);small(im,labs(cfg)[i],x,y+62,p)
  dot(im,*at(pts,clamp(t/4)),p,10)

def compares(im,t,cfg,p,v):
 f=phase(t);a=vals(cfg);ls=labs(cfg);cols=colors(p);b=vals({'values':cfg.get('compare_values',[45,68,60,79])})
 if v==0:
  card(im,100,290,330,230,p);card(im,850,290,330,230,p);txt(im,fmt(a[0]*f),265,373,p,70);txt(im,fmt(a[1]*f),1015,373,p,70);small(im,ls[0],265,464,p);small(im,ls[1],1015,464,p);line(im,[(430,405),(850,405)],p['accent'],5);txt(im,('+' if a[1]>=a[0] else '')+fmt((a[1]-a[0])*f),640,348,p,54);arrow(im,825,405,p['accent'])
 elif v==1:
  for i in range(4):y=290+i*75;small(im,ls[i],130,y+17,p,'left');rr(im,(315,y,315+clamp(b[i]/100)*310*f,y+33),p['secondary'],7);rr(im,(680,y,680+clamp(a[i]/100)*350*f,y+33),p['accent'],7);txt(im,fmt(b[i]*f),620,y+16,p,21);txt(im,fmt(a[i]*f),1100,y+16,p,21)
  line(im,[(660,265),(660,593)],p['third'],3);small(im,'BEFORE',440,610,p);small(im,'AFTER',885,610,p)
 elif v==2:
  for i in range(4):y=288+i*78;small(im,ls[i],120,y+18,p,'left');rr(im,(290,y,1100,y+35),rgba(p['muted'],45),4);rr(im,(290,y+5,290+810*clamp(a[i]/100)*phase(t,i*.15),y+30),cols[i],4);x=290+810*clamp(b[i]/100);line(im,[(x,y-8),(x,y+43)],p['text'],4)
  small(im,'VERTICAL MARK = COMPARISON TARGET',640,608,p)
 else:
  for i in range(4):y=286+i*82;small(im,ls[i],125,y,p,'left');line(im,[(300,y),(1120,y)],rgba(p['muted'],100),3)
  for i in range(4):
   y=286+i*82
   for j in range(11):x=300+j*82;line(im,[(x,y-5),(x,y+5)],rgba(p['muted'],70),1)
   x=300+820*clamp(a[i]/100)*phase(t,i*.1);circle(im,x,y,13,cols[i]);txt(im,fmt(a[i]*phase(t,i*.1)),x,y-27,p,22)

def dashboards(im,t,cfg,p,v):
 f=phase(t);vs=vals(cfg);cols=colors(p)
 if v==0:
  card(im,90,260,360,320,p);card(im,475,260,310,145,p);card(im,810,260,380,145,p);card(im,475,425,715,155,p)
  txt(im,fmt(vs[0]*f),270,328,p,58);small(im,'PRIMARY METRIC',270,385,p);arc(im,270,490,58,-90,-90+360*clamp(vs[0]/100)*f,p['accent'],12)
  for i,x in enumerate([630,1000]):txt(im,fmt(vs[i+1]*phase(t,.25)),x,318,p,48);small(im,labs(cfg)[i+1],x,370,p)
  pts=[(500+i*35,553-70*(.3+.7*math.sin(i*.22)**2)*f) for i in range(19)];line(im,partial(pts,f),p['accent'],4)
 elif v==1:
  card(im,95,270,770,245,p);card(im,890,270,300,245,p);card(im,95,535,1095,68,p)
  pts=[(125+i*7.1,395+math.sin(i*.38-t*2)*45*f) for i in range(100)];line(im,pts,p['accent'],4);line(im,[(125+710*f,285),(125+710*f,499)],rgba(p['secondary'],130),2);arc(im,1040,388,65,130,410,rgba(p['muted'],45),10);arc(im,1040,388,65,130,130+280*f,p['accent'],10);txt(im,fmt(vs[0]*f),1040,470,p,31);txt(im,'STATUS  '+('READY' if f>.99 else 'SCANNING'),643,569,p,26)
 elif v==2:
  for i in range(4):y=265+i*84;card(im,165,y,950,67,p);circle(im,203,y+33,15,cols[i]);txt(im,labs(cfg)[i],255,y+33,p,27,anchor='left');rr(im,(540,y+22,540+360*clamp(vs[i]/100)*phase(t,i*.16),y+46),cols[i],8);txt(im,fmt(vs[i]*phase(t,i*.16)),1040,y+33,p,30)
 else:
  card(im,90,260,425,315,p);txt(im,fmt(vs[0]*f),303,337,p,84);small(im,'DEMO HEADLINE STAT',303,415,p);txt(im,'DATA UPDATE',303,515,p,28)
  card(im,540,260,650,145,p);line(im,partial([(580,370),(740,285),(875,330),(1135,295)],f),p['accent'],5)
  for i in range(3):y=433+i*48;small(im,labs(cfg)[i+1],640,y+17,p,'right');rr(im,(660,y,660+390*clamp(vs[i+1]/100)*phase(t,i*.13),y+29),cols[i+1],6)

def timelines(im,t,cfg,p,v):
 f=phase(t);ls=labs(cfg);cols=colors(p)
 if v==0:
  pts=[]
  for i in range(4):x=215+i*273;y=305+i*63;pts.append((x,y));q=phase(t,i*.25);card(im,x-105,y-30-30*(1-q),230,100,p);txt(im,f'{i+1:02d} · '+ls[i],x+10,y+2-30*(1-q),p,22);small(im,'CHAPTER',x+10,y+39-30*(1-q),p)
  line(im,partial([(215,375),(488,438),(761,501),(1034,564)],f),p['accent'],3)
 elif v==1:
  pts=[(200,425),(493,425),(786,425),(1080,425)];line(im,pts,rgba(p['muted'],65),8);line(im,partial(pts,f),p['accent'],7)
  for i,(x,y) in enumerate(pts):circle(im,x,y,17,p['panel'],cols[i],3);y2=295 if i%2==0 else 520;line(im,[(x,y),(x,y2)],rgba(cols[i],130),2);card(im,x-100,y2-39,200,78,p);txt(im,ls[i],x,y2,p,24)
 elif v==2:
  for i in range(4):y=285+i*75;small(im,ls[i],180,y+17,p,'right');x=235+i*135;q=phase(t,i*.22);rr(im,(x,y,x+425*q+1,y+39),cols[i],8)
  x=235+865*f;line(im,[(x,259),(x,597)],p['text'],2)
 else:
  circle(im,640,431,145,None,rgba(p['muted'],80),4)
  for i in range(4):a=-math.pi/2+i*math.pi/2;x=640+145*math.cos(a);y=431+145*math.sin(a);circle(im,x,y,16*phase(t,i*.3)+1,cols[i]);small(im,ls[i],x+(120 if i==1 else -120 if i==3 else 0),y+(34 if i==2 else -35 if i==0 else 0),p)
  a=-math.pi/2+2*math.pi*f;line(im,[(640,431),(640+123*math.cos(a),431+123*math.sin(a))],p['accent'],5);circle(im,640,431,10,p['accent'])

def organisations(im,t,cfg,p,v):
 f=phase(t);cols=colors(p);ls=labs(cfg)
 if v==0:
  root=(640,285);teams=[(370,415),(910,415)];leaves=[(235,565),(505,565),(775,565),(1045,565)]
  for i,n in enumerate(teams):line(im,partial([root,(640,355),(n[0],355),n],phase(t,i*.17)),p['accent'],3)
  for i,n in enumerate(leaves):a=teams[i//2];line(im,partial([a,(a[0],500),(n[0],500),n],phase(t,.4+i*.1)),cols[i],3)
  for i,(x,y) in enumerate([root]+teams+leaves):rr(im,(x-82,y-25,x+82,y+25),p['panel'],11,cols[i%4],2);txt(im,'LEAD' if i==0 else 'TEAM '+str(i) if i<3 else ls[i-3],x,y,p,20)
 elif v==1:
  for i in range(4):small(im,ls[i],395+i*195,260,p)
  for r in range(4):
   small(im,'TASK '+str(r+1),170,320+r*75,p,'left')
   for c in range(4):x=315+c*195;y=286+r*75;rr(im,(x,y,x+160,y+61),rgba(cols[c],25+int(80*phase(t,(r+c)*.07))),10);txt(im,['R','A','C','I'][(r+c)%4],x+80,y+30,p,28)
 elif v==2:
  for i in reversed(range(4)):
   y=265+i*78;q=phase(t,(3-i)*.2);w=190+i*210;poly(im,[(640-w/2,y+70),(640+w/2,y+70),(640+(w-180)/2,y+70-66*q),(640-(w-180)/2,y+70-66*q)],rgba(cols[i],180));txt(im,ls[i],640,y+40,p,22)
 else:
  for r in [90,177]:circle(im,640,430,r,None,rgba(p['muted'],70),2)
  circle(im,640,430,42,p['panel'],p['accent'],3);txt(im,'CORE',640,430,p,20)
  for i in range(8):a=i*math.pi/4+.18;rrr=90 if i%2 else 177;x=640+rrr*math.cos(a);y=430+rrr*math.sin(a);line(im,partial([(640,430),(x,y)],phase(t,i*.06)),rgba(cols[i%4],130),2);circle(im,x,y,21,cols[i%4]);small(im,ls[i%4],x+40*(1 if x>=640 else -1),y,p,'left' if x>=640 else 'right')

def cycles(im,t,cfg,p,v):
 f=phase(t);cols=colors(p);ls=labs(cfg)
 if v==0:
  circle(im,640,430,140,None,rgba(p['muted'],70),26)
  for i in range(4):a=t*(1.5-f)+i*math.pi/2;x=640+140*math.cos(a);y=430+140*math.sin(a);circle(im,x,y,17,cols[i]);n=(-1 if i%2 else 1);line(im,[(640+n*300,300+i*63),(640+n*167,360+i*30)],rgba(cols[i],90),3)
  txt(im,'MOMENTUM',640,430,p,26)
 elif v==1:
  for i in range(4):a=-88+i*90;arc(im,640,430,143,a,a+82*phase(t,i*.22),cols[i],28);ang=math.radians(a+40);x=640+215*math.cos(ang);y=430+170*math.sin(ang);small(im,ls[i],x,y,p)
  a=-math.pi/2+t*1.2;dot(im,640+143*math.cos(a),430+143*math.sin(a),p,9);txt(im,'PROCESS',640,430,p,25)
 elif v==2:
  nodes=[(235,385),(580,385),(970,385)];line(im,partial(nodes,f),p['accent'],5);back=[nodes[-1],(970,565),(235,565),nodes[0]];line(im,partial(back,phase(t,.6)),p['secondary'],4)
  for i,(x,y) in enumerate(nodes):card(im,x-95,y-48,190,96,p);txt(im,['INPUT','ACTION','OUTPUT'][i],x,y,p,24)
  dot(im,*at(back,clamp((t-1)/3)),p,8);small(im,'FEEDBACK',595,591,p)
 else:
  pts=[(410,295),(890,320),(820,550),(350,530),(410,295)];line(im,partial(pts,f),rgba(p['accent'],150),5)
  for i,(x,y) in enumerate(pts[:-1]):q=phase(t,i*.22);circle(im,x,y,(34+i*9)*q+1,rgba(cols[i],65),cols[i],3);txt(im,ls[i],x,y,p,21)

def finance(im,t,cfg,p,v):
 f=phase(t);cols=colors(p);vs=vals(cfg);ls=labs(cfg)
 if v==0:
  grid(im,p);prices=vals({'values':cfg.get('price_series',cfg.get('values',[55,62,58,70,66,76,83,79,92,87,97,102]))},12);mx=max(1,max(abs(x) for x in prices)*1.14);prev=float(cfg.get('opening_price',prices[0]*.91))
  for i,close in enumerate(prices):x=230+i*75;q=phase(t,i*.06);yy=lambda value:555-value/mx*265;op=prev;line(im,[(x,yy(max(op,close)+8)),(x,yy(min(op,close)-6))],cols[0] if close>=op else cols[2],2);rr(im,(x-18,yy(max(op,close)*q),x+18,yy(min(op,close)*q)+1),cols[0] if close>=op else cols[2],3);prev=close
  small(im,'FICTIONAL PRICE SERIES',640,602,p);txt(im,'END '+fmt(prices[-1]*f),1040,250,p,24)
 elif v==1:
  line(im,[(640,265),(640,588)],p['muted'],2)
  for i in range(6):y=280+i*49;left=90+((i*41)%260);right=70+((i*73)%260);q=phase(t,i*.08);rr(im,(620-left*q,y,620,y+29),p['accent'],5);rr(im,(660,y,660+right*q,y+29),p['third'],5);txt(im,str(101+i),640,y+14,p,17);small(im,fmt(left*q),190,y+14,p,'right');small(im,fmt(right*q),1080,y+14,p,'left')
  small(im,'BUY VOLUME',355,610,p);small(im,'SELL VOLUME',924,610,p)
 elif v==2:
  total=max(1,sum(max(0,z) for z in vs));start=-90
  for i,z in enumerate(vs):end=start+max(0,z)/total*360;arc(im,380,425,134,start,mix(start,end,phase(t,i*.12)),cols[i],35);start=end
  txt(im,'ASSETS',380,425,p,28)
  for i,z in enumerate(vs):y=280+i*82;small(im,ls[i],680,y,p,'left');rr(im,(680,y+21,680+400*max(0,z)/total*phase(t,i*.12)+1,y+42),cols[i],5);txt(im,f'{max(0,z)/total*100:.1f}%',1130,y+22,p,24)
 else:
  grid(im,p);principal=max(1,abs(vs[0]));rate=float(cfg.get('growth_rate',.12));rate=max(-.8,min(1,rate));amounts=[principal*(1+rate)**i for i in range(8)];mx=max(amounts)*1.1
  for i,value in enumerate(amounts):x=235+i*108;h=value/mx*265*phase(t,i*.1);rr(im,(x,555-h,x+65,555),p['accent'],6);small(im,str(i),x+32,591,p)
  y=555-principal/mx*265;line(im,[(195,y),(1110,y)],p['secondary'],2);txt(im,'FINAL '+fmt(amounts[-1]*f),960,251,p,25)

def systems(im,t,cfg,p,v):
 f=phase(t);cols=colors(p);ls=labs(cfg)
 if v==0:
  boxes=[(230,415),(620,290),(620,550),(1040,415)];paths=[[(230,415),(440,415),(440,290),(620,290)],[(230,415),(440,415),(440,550),(620,550)],[(620,290),(850,290),(850,415),(1040,415)],[(620,550),(850,550),(850,415),(1040,415)]]
  for i,r in enumerate(paths):line(im,partial(r,phase(t,i*.12)),rgba(cols[i],140),3);dot(im,*at(r,clamp((t*.3+i*.21)%1)),p,6)
  for i,(x,y) in enumerate(boxes):card(im,x-80,y-38,160,76,p);txt(im,ls[i],x,y,p,22)
 elif v==1:
  for i in reversed(range(5)):
   q=phase(t,i*.12);x=340+i*25*f;y=535-i*57;card(im,x,y,570,49,p);txt(im,['INTERFACE','APPLICATION','SERVICES','DATA','INFRASTRUCTURE'][i],x+285,y+24,p,21)
 elif v==2:
  for i in range(3):y=270+i*115;rr(im,(160,y,1150,y+97),rgba(cols[i],20),10);small(im,'LANE '+str(i+1),185,y+48,p,'left')
  path=[(380,320),(650,320),(650,435),(880,435),(880,550),(1090,550)];line(im,partial(path,f),p['accent'],4);x,y=at(path,f);rr(im,(x-38,y-25,x+38,y+25),p['accent'],9);txt(im,'JOB',x,y,p,19,p['bg'])
 else:
  starts=[0,.2,.35,.57,.7];lengths=[.25,.42,.2,.3,.19]
  for i in range(5):y=270+i*62;small(im,'REQUEST '+str(i+1),165,y+16,p,'left');x=350+starts[i]*760;q=phase(t,i*.15);rr(im,(x,y,x+lengths[i]*760*q+1,y+35),cols[i%4],7)
  x=350+760*f;line(im,[(x,253),(x,598)],p['text'],2);small(im,'ILLUSTRATIVE DEPENDENCY TIMES',680,615,p)

def editorial(im,t,cfg,p,v):
 f=phase(t);vs=vals(cfg);ls=labs(cfg);cols=colors(p)
 if v==0:
  txt(im,fmt(vs[0]*f)+cfg.get('unit','%'),640,353,p,118,p['accent']);txt(im,ls[0],640,461,p,30)
  for i in range(3):q=phase(t,.5+i*.18);line(im,[(380,520+i*33),(380+520*q,520+i*33)],rgba(cols[i],120),3);small(im,['MEASURED VALUE','REPLACE SAMPLE DATA','CLEAR CONTEXT'][i],640,537+i*33,p)
 elif v==1:
  count=round(clamp(vs[0]/100)*40*f)
  for i in range(40):x=255+(i%10)*83;y=280+(i//10)*73;c=p['accent'] if i<count else rgba(p['muted'],55);circle(im,x,y,11,c);rr(im,(x-13,y+16,x+13,y+44),c,7)
  txt(im,f'{count}/40',1040,347,p,49);small(im,'HIGHLIGHTED SHARE',1040,408,p)
 elif v==2:
  for i in range(4):x=135+i*265;y=560-i*65;q=phase(t,i*.2);rr(im,(x,y-90*q,x+238,606),rgba(cols[i],45),10);txt(im,f'{i+1:02d}',x+119,y-42*q,p,45,cols[i]);txt(im,ls[i],x+119,y-118,p,24)
  line(im,partial([(155,470),(420,405),(685,340),(950,275)],f),p['accent'],4)
 else:
  for i in range(3):x=105+i*385;q=phase(t,i*.2);card(im,x+45*(1-q),275,340,225,p);small(im,'EVIDENCE '+str(i+1),x+170+45*(1-q),312,p);txt(im,fmt(vs[i]*q),x+170+45*(1-q),383,p,56);small(im,ls[i],x+170+45*(1-q),455,p);line(im,[(x+170,500),(x+170,549),(640,549)],rgba(cols[i],90),2)
  card(im,370,550,540,64,p);txt(im,'CONCLUSION',640,582,p,27)

HANDLERS=[maps,networks,coverage,itinerary,globes,logistics,races,bars,lines,radials,kpis,flows,matrices,scatters,science,engineering,biology,compares,dashboards,timelines,organisations,cycles,finance,systems,editorial]
def render(pid,t,cfg):
 if pid not in PRESETS:raise ValueError('Unknown preset '+pid)
 cfg={**PRESETS[pid],**cfg}
 for key in ('recipe_group','recipe_variant','schematic'):cfg[key]=PRESETS[pid][key]
 p=palette_ext(cfg);im=base(cfg);scene=layer();header(scene,t,cfg,p);HANDLERS[cfg['recipe_group']](scene,t,cfg,p,cfg['recipe_variant'])
 # All artwork is clipped to the atlas content region; ending values dwell before a short soft exit.
 scene=scene.crop((54,140,1226,635));opacity=1-smooth(prog(t,4.75,5));paste(im,scene,54,140,opacity=opacity,anchor='topleft');return im
