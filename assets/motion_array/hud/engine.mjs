/** Original vector HUD artwork. Source previews are inspiration, never embedded media. */
const TAU = Math.PI * 2;
const COLORS = { a: '#65e6ed', b: '#f4fcff', c: '#7599b5', warn: '#ffc86c' };
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const smooth = x => { x = clamp(x); return x * x * (3 - 2 * x); };
const n = x => Number(x.toFixed(3));
const point = (cx, cy, r, a) => [n(cx + r * Math.cos(a)), n(cy + r * Math.sin(a))];
const esc = x => String(x).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const attrs = x => Object.entries(x).filter(([,v]) => v !== undefined && v !== null).map(([k,v]) => `${k}="${esc(v)}"`).join(' ');
const el = (tag, a = {}, inside = '') => `<${tag} ${attrs(a)}>${inside}</${tag}>`;
const line = (x1,y1,x2,y2,c=COLORS.a,w=1.5,o=1) => el('line',{x1:n(x1),y1:n(y1),x2:n(x2),y2:n(y2),stroke:c,'stroke-width':w,opacity:n(o),'stroke-linecap':'round'});
const path = (d,c=COLORS.a,w=1.5,o=1,fill='none',extra={}) => el('path',{d,fill,stroke:c,'stroke-width':w,opacity:n(o),'stroke-linecap':'round','stroke-linejoin':'round',...extra});
const circle = (x,y,r,c=COLORS.a,w=1.5,o=1,fill='none',extra={}) => el('circle',{cx:n(x),cy:n(y),r:n(r),stroke:c,'stroke-width':w,opacity:n(o),fill,...extra});
const rect = (x,y,w,h,c=COLORS.a,sw=1.5,o=1,fill='none',rx=0) => el('rect',{x:n(x),y:n(y),width:n(w),height:n(h),rx,fill,stroke:c,'stroke-width':sw,opacity:n(o)});
const group = (content, extra={}) => el('g',extra,content);
const arc = (cx,cy,r,a,b,c=COLORS.a,w=2,o=1) => {
  if (b-a >= TAU-.001) return circle(cx,cy,r,c,w,o);
  const p=point(cx,cy,r,a),q=point(cx,cy,r,b);
  return path(`M${p[0]} ${p[1]} A${n(r)} ${n(r)} 0 ${b-a>Math.PI?1:0} 1 ${q[0]} ${q[1]}`,c,w,o);
};
const poly = (pts,c=COLORS.a,w=1.5,o=1,fill='none',close=false) => path(pts.map((p,i)=>`${i?'L':'M'}${n(p[0])} ${n(p[1])}`).join(' ')+(close?' Z':''),c,w,o,fill);
const rng = seed => () => { seed = (Math.imul(seed,1664525)+1013904223) >>> 0; return seed/4294967296; };
const digitBits = [0b1111110,0b0110000,0b1101101,0b1111001,0b0110011,0b1011011,0b1011111,0b1110000,0b1111111,0b1111011];
const variants = [
  ['single hub','one hub with asymmetric auxiliary geometry'],
  ['paired scopes','two linked scopes with unequal proportions'],
  ['triple constellation','three coordinated groups in a triangular layout'],
  ['four quadrant','four coordinated groups around the center'],
  ['wide instrument','a wide field with distributed subordinate modules'],
  ['offset ladder','staggered modules with an offset connection ladder'],
  ['nested instrument','three levels of nested and offset geometry'],
  ['diagonal array','a diagonal cluster with an independent satellite'],
  ['split hierarchy','a dominant instrument beside two smaller satellites'],
  ['radial constellation','multiple local instruments around a circular field'],
  ['compact cluster','a compact dense cluster with different member sizes'],
  ['panoramic band','a horizontal band of modules with one central hub'],
  ['vertical stack','a stacked composition with linking side rails'],
  ['stepped matrix','a stepped matrix with unequal rows'],
  ['orbit satellites','one central hub with staggered orbital satellites'],
  ['triangular hierarchy','a wide upper module and two narrow lower modules'],
  ['dual columns','two opposed columns of independently sequenced modules'],
  ['perimeter network','a perimeter layout surrounding an open central field'],
  ['interlocking cluster','interlocking modules with overlapping local fields'],
  ['modular dashboard','a large central module, side stacks, and lower strip']
];

const specs = [
 ['segmented-ring','Segmented orbital ring','Radial HUD','Rotating arcs with gaps and small tick accents','modular-ring'],
 ['globe-grid','Rotating globe grid','Radial HUD','Orthogonal elliptical meridians inside an orbital rim','modular-globe'],
 ['radial-ticks','Radial tick dial','Radial HUD','Dense tick divisions grouped into major and minor intervals','modular-ring'],
 ['radial-scan','Orbiting marker spokes','Radial HUD','A rotating spoke cluster carries perimeter marker accents','modular-ring'],
 ['ring-stack','Concentric ring stack','Radial HUD','Nested rings with staggered counter motion','modular-ring'],
 ['branch-nodes','Branching node strokes','Networks','Polyline branches grow from hubs into connected endpoints','modular-nodes'],
 ['node-mesh','Connected node mesh','Networks','An evolving network connects neighboring node clusters','modular-nodes'],
 ['elbow-circuit','Elbow connector circuit','Networks','Right-angle routing reveals between outlined terminal nodes','modular-nodes'],
 ['scan-frame','Subject scan frame','Scanning','Horizontal scan travels through an outlined subject frame','modular-frame'],
 ['corner-brackets','Corner bracket frame','Scanning','Separate bracket corners enter around a tracking field','modular-corners'],
 ['wave-strip','Waveform strip','Signals','A thin waveform oscillates through a horizontal instrument strip','modular-wave'],
 ['wave-channels','Stacked waveform channels','Signals','Several waveform channels run in coordinated narrow rows','modular-wave'],
 ['scan-lines','Stacked scan lines','Scanning','A scanning sweep activates groups of parallel raster lines','modular-lines'],
 ['segment-timer','Segment timer','Readouts','Geometric seven-segment readouts advance in a modular panel','modular-timer'],
 ['warning-panel','Warning geometry panel','Readouts','A framed panel reveals an abstract geometric alert and bars','modular-warning'],
 ['bar-meter','Broad sector rotor','Radial HUD','Broad annular wedges rotate and exchange scale','crt-sector'],
 ['arc-meter','Building arc progress','Radial HUD','An open broad ring fills and rotates around an empty core','crt-arc'],
 ['scope-grid','Assembling rectangular frame','Scanning','Disconnected rectangular edges assemble into instrument frames','crt-frame'],
 ['target-boxes','Orbital dot loader','Radial HUD','A circular dot constellation chases with a fading tail','crt-dots'],
 ['data-stacks','Thin orbital rings','Radial HUD','Thin interrupted rings exchange diameter with an inner rotary rim','crt-thinrings'],
 ['pulse-trace','Animated pie sectors','Data','A circular chart reveals differently proportioned pie sectors','corporate-pie'],
 ['radar-blips','Concentric target rings','Data','Concentric rings form a target with an offset geometric pointer','corporate-target'],
 ['micro-tile','Curved process arrows','Networks','An arc-shaped process connector grows into an arrow head','corporate-arrow'],
 ['bevel-panel','Dotted orbit connector','Networks','A dashed orbit connects modular badge nodes around a central field','corporate-orbit'],
 ['coordinate-rail','Circular icon containers','Readouts','Circular badge containers scale in with original neutral geometric symbols','corporate-badges']
];

let observedMap = {"segmented-ring":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD001"]},"globe-grid":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD002"]},"radial-ticks":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD003"]},"radial-scan":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD004"]},"ring-stack":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD005"]},"branch-nodes":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD006"]},"node-mesh":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD007"]},"elbow-circuit":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD008"]},"scan-frame":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD009"]},"corner-brackets":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD010"]},"wave-strip":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD011"]},"wave-channels":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD012"]},"scan-lines":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD013"]},"segment-timer":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD014"]},"warning-panel":{"source_ids":["MAS014"],"observation_ids":["MAOBS_HUD015"]},"bar-meter":{"source_ids":["MAS011"],"observation_ids":["MAOBS_HUD016"]},"arc-meter":{"source_ids":["MAS011"],"observation_ids":["MAOBS_HUD017"]},"scope-grid":{"source_ids":["MAS011"],"observation_ids":["MAOBS_HUD018"]},"target-boxes":{"source_ids":["MAS011"],"observation_ids":["MAOBS_HUD019"]},"data-stacks":{"source_ids":["MAS011"],"observation_ids":["MAOBS_HUD020"]},"pulse-trace":{"source_ids":["MAS007"],"observation_ids":["MAOBS_HUD021"]},"radar-blips":{"source_ids":["MAS007"],"observation_ids":["MAOBS_HUD022"]},"micro-tile":{"source_ids":["MAS007"],"observation_ids":["MAOBS_HUD023"]},"bevel-panel":{"source_ids":["MAS007"],"observation_ids":["MAOBS_HUD024"]},"coordinate-rail":{"source_ids":["MAS007"],"observation_ids":["MAOBS_HUD025"]}};
export function setObservations(map = {}) { observedMap = {...map}; }
export const mechanisms = specs.map((s,i)=>({index:i,key:s[0],title:s[1],category:s[2],description:s[3],observation_key:s[4]}));

export function records() {
  return specs.flatMap((s,mi)=>variants.map(([label,basis],v)=>{
    const id=`MA${String(501+mi*20+v).padStart(4,'0')}`;
    const evidence=observedMap[s[0]] || observedMap[s[4]] || {};
    return {id,title:`${s[1]} — ${label}`,category:s[2],mechanism:s[0],mechanism_description:s[3],variant_basis:basis,tags:['HUD','technology','transparent',s[2].toLowerCase(),label],use_cases:['video explainer','technology promotion','motion graphic layering','data visualisation'],duration:3,group:'hud',parameters:{variant:v,mechanism_index:mi,seed:mi*997+v*59+719,layout:label},source_ids:evidence.source_ids||[],observation_ids:evidence.observation_ids||[],source_status:evidence.observation_ids?.length?'observed-preview-original-adaptation':'awaiting-preview-mapping'};
  }));
}

function layouts(v) {
  const a= [
   [[320,180,1]], [[225,180,.82],[440,190,.56]], [[320,104,.56],[226,241,.53],[425,238,.62]],
   [[215,112,.5],[425,112,.54],[215,248,.56],[425,248,.5]], [[180,178,.76],[381,129,.4],[467,228,.43]],
   [[186,108,.46],[285,179,.63],[458,250,.47]], [[320,180,1],[320,180,.66],[320,180,.33]],
   [[185,245,.47],[315,172,.7],[464,92,.45]], [[259,180,.85],[460,106,.4],[467,251,.4]],
   [[320,180,.59],[196,97,.36],[447,96,.4],[440,264,.39],[195,264,.36]],
   [[264,179,.65],[390,118,.5],[423,241,.45]], [[148,184,.39],[261,184,.49],[389,184,.56],[504,184,.38]],
   [[320,83,.4],[320,180,.64],[320,283,.39]], [[203,106,.43],[358,105,.48],[456,179,.42],[288,242,.51],[150,253,.34]],
   [[320,180,.69],[157,177,.29],[454,81,.3],[467,266,.35]], [[320,117,.74],[219,266,.43],[431,265,.46]],
   [[198,88,.35],[198,179,.42],[198,273,.35],[441,96,.38],[441,183,.45],[441,277,.33]],
   [[148,95,.3],[318,70,.34],[495,99,.3],[513,251,.36],[321,292,.33],[130,258,.33]],
   [[245,170,.72],[381,202,.62],[458,99,.31]], [[321,150,.67],[132,100,.3],[133,195,.34],[494,107,.33],[496,207,.3],[321,286,.34]]
  ];
  return a[v % 20];
}

function brackets(x,y,w,h,size,c=COLORS.a,opacity=1) {
  return [[x,y,1,1],[x+w,y,-1,1],[x,y+h,1,-1],[x+w,y+h,-1,-1]].map(([a,b,sx,sy])=>poly([[a+sx*size,b],[a,b],[a,b+sy*size]],c,2,opacity)).join('');
}
function timer(x,y,count,v,t) {
  const w=17,h=31,gap=8,th=2.6;
  const segments=[[[3,0],[w-3,0]],[[w,3],[w,h/2-3]],[[w,h/2+3],[w,h-3]],[[3,h],[w-3,h]],[[0,h/2+3],[0,h-3]],[[0,3],[0,h/2-3]],[[3,h/2],[w-3,h/2]]];
  let out='';
  for(let i=0;i<count;i++){
    const d=(Math.floor(t*4)+v*3+i*7)%10,bits=digitBits[d];
    for(let k=0;k<7;k++){const [a,b]=segments[k];out+=line(x+i*(w+gap)+a[0],y+a[1],x+i*(w+gap)+b[0],y+b[1],COLORS.a,th,bits&(1<<(6-k))?.95:.12);}
  }
  return out;
}

function local(key,v,t,seed,phase) {
  const R=rng(seed), out=[];
  const a=t*.76+v*.11, count=5+v%7;
  const add=x=>out.push(x);
  const baseR=91+(v%4)*3;
  switch(key) {
    case 'segmented-ring': {
      const bands=2+v%3, segs=4+v%8;
      for(let band=0;band<bands;band++){
        const r=baseR-band*15, rot=(band%2?-1:1)*a*(.5+band*.25), gap=.12+(v%3)*.035;
        for(let j=0;j<segs;j++)add(arc(0,0,r,j*TAU/segs+rot,j*TAU/segs+rot+TAU/segs-gap,band===0?COLORS.a:COLORS.c,band===0?3.8:1.3,band===0?.95:.65));
      }
      add(circle(0,0,5,COLORS.b,1,.8));
      for(let j=0;j<segs*3;j++){const p=point(0,0,baseR+8,j*TAU/(segs*3)),q=point(0,0,baseR+12+(j%3===0?5:0),j*TAU/(segs*3));add(line(...p,...q,COLORS.b,1,.42));}
      break;
    }
    case 'globe-grid': {
      add(circle(0,0,baseR,COLORS.a,1.9,.9));
      const meridians=3+v%5;
      for(let j=0;j<meridians;j++){const z=Math.sin(a+j*Math.PI/meridians);add(el('ellipse',{cx:0,cy:0,rx:n(Math.max(1,Math.abs(z)*baseR)),ry:baseR,fill:'none',stroke:COLORS.a,'stroke-width':1,opacity:n(.3+.4*Math.abs(z))}));}
      for(let j=1;j<meridians;j++){const yy=-baseR+j*2*baseR/meridians,rr=Math.sqrt(Math.max(0,baseR**2-yy**2));add(el('ellipse',{cx:0,cy:n(yy),rx:n(rr),ry:n(rr*.15),fill:'none',stroke:COLORS.c,'stroke-width':1,opacity:.7}));}
      add(arc(0,0,baseR+11,a,a+Math.PI*.85,COLORS.b,3,.72));
      break;
    }
    case 'radial-ticks': {
      const ticks=24+(v%8)*6;
      for(let j=0;j<ticks;j++){const theta=TAU*j/ticks,r0=baseR-(j%4?8:19),p=point(0,0,r0,theta),q=point(0,0,baseR,theta);add(line(...p,...q,j%4?COLORS.c:COLORS.a,j%4?1:2.5,.8));}
      add(arc(0,0,baseR-28,a,a+Math.PI*(.7+v%3*.14),COLORS.b,2));
      const p=point(0,0,baseR-33,a),q=point(0,0,baseR+6,a);add(line(...p,...q,COLORS.a,3));add(circle(0,0,6,COLORS.a,2));
      break;
    }
    case 'radial-scan': {
      const spokes=6+v%9;
      for(let j=0;j<spokes;j++){const theta=TAU*j/spokes+a,p=point(0,0,baseR-7,theta),q=point(0,0,baseR+5,theta);add(line(...p,...q,COLORS.b,2,.82));const rr=point(0,0,baseR+15,theta+.03);add(circle(...rr,2,COLORS.a,1,.72));}
      add(arc(0,0,baseR-26,-a,-a+Math.PI*1.28,COLORS.a,2.4,.8));add(circle(0,0,baseR-39,COLORS.c,.8,.4));break;
    }
    case 'ring-stack': {
      const rings=3+v%6;
      for(let j=0;j<rings;j++){const r=baseR*(j+1)/(rings+1),ang=a*(j%2?-1:1)+j*.8;add(arc(0,0,r,ang,ang+Math.PI*(1.25+(j%3)*.14),j%2?COLORS.c:COLORS.a,1.5+j%2,.9));}
      add(circle(0,0,baseR,COLORS.c,1,.4));break;
    }
    case 'branch-nodes': {
      const branches=3+v%7;
      add(circle(0,0,11,COLORS.b,2));
      for(let j=0;j<branches;j++){
        const theta=TAU*j/branches+.4, p=point(0,0,38+R()*17,theta),q=point(0,0,82+R()*16,theta+.16*Math.sin(j+v));
        const bend=[p[0]+(q[0]-p[0])*.65,p[1]];
        add(poly([[0,0],p,bend,q],COLORS.a,1.5,.85));add(circle(...q,4+j%2,COLORS.a,1.4,.95));
        if(j%2===0){const s=[q[0]+(R()-.5)*36,q[1]-22];add(poly([q,s],COLORS.c,1,.5));add(rect(s[0]-3,s[1]-3,6,6,COLORS.b,1,.7));}
        const z=(t*.36+j/branches)%1,pp=z<.5?[p[0]*z*2,p[1]*z*2]:[p[0]+(q[0]-p[0])*(z-.5)*2,p[1]+(q[1]-p[1])*(z-.5)*2];add(circle(...pp,2,COLORS.b,1,.85,COLORS.b));
      }break;
    }
    case 'node-mesh': {
      const nodes=6+v%9, pts=Array.from({length:nodes},(_,j)=>point(0,0,42+R()*55,TAU*j/nodes+.13*Math.sin(t+j)));
      for(let j=0;j<nodes;j++){add(poly([pts[j],pts[(j+1)%nodes]],COLORS.c,1,.5));if(j%2===0)add(poly([pts[j],pts[(j+3)%nodes]],COLORS.a,1,.3));}
      pts.forEach((p,j)=>{add(circle(...p,3+j%3,COLORS.a,1.4,.9));add(circle(...p,7+j%3,COLORS.c,.7,.3));});break;
    }
    case 'elbow-circuit': {
      const branches=3+v%6;
      add(rect(-13,-13,26,26,COLORS.a,1.6,.9));
      for(let j=0;j<branches;j++){const q=point(0,0,70+R()*29,TAU*j/branches+.3),p=[q[0]*.45,q[1]*.35];add(poly([[0,0],[p[0],0],p,[q[0],p[1]],q],COLORS.c,1.6,.8));add(rect(q[0]-5,q[1]-5,10,10,COLORS.a,1.4,.9));add(line(q[0]-2,q[1],q[0]+2,q[1],COLORS.b,1.5));}break;
    }
    case 'scan-frame': {
      const w=160+v%4*11,h=114+v%5*8;add(brackets(-w/2,-h/2,w,h,14+v%4*3));add(rect(-w/2+5,-h/2+5,w-10,h-10,COLORS.c,.8,.35));
      const yy=-h/2+(t*.52+.1*v)%1*h;
      for(let j=0;j<5;j++)add(line(-w/2+9,yy-j*2,w/2-9,yy-j*2,COLORS.a,j===0?2:1,.65-j*.1));
      const silhouette=Array.from({length:8+v%5},(_,j)=>point(0,0,25+(j%2)*18,TAU*j/(8+v%5)));add(poly(silhouette,COLORS.c,1,.75,'none',true));break;
    }
    case 'corner-brackets': {
      const w=155+v%5*12,h=112+v%4*12,sz=14+v%6*3;add(brackets(-w/2,-h/2,w,h,sz));
      add(line(-11,0,11,0,COLORS.c,1,.55));add(line(0,-11,0,11,COLORS.c,1,.55));
      const pairs=1+v%3;for(let j=0;j<pairs;j++)add(brackets(-w/2-7-j*8,-h/2-7-j*8,w+14+j*16,h+14+j*16,sz/2,COLORS.c,.24));
      add(rect(w/2+5,-h/2+9,4,15+v%4*8,COLORS.b,0,.85,COLORS.b));break;
    }
    case 'wave-strip': {
      const w=190+v%4*8, ampl=16+v%6*4,samples=50+v%8;
      add(line(-w/2,0,w/2,0,COLORS.c,1,.38));add(brackets(-w/2-8,-ampl-13,w+16,ampl*2+26,8,COLORS.c,.65));
      const pts=Array.from({length:samples},(_,j)=>{const x=-w/2+w*j/(samples-1),z=j/(samples-1);return[x,Math.sin(z*TAU*(2+v%5)+t*3)*ampl*(.45+.55*Math.sin(Math.PI*z))+.25*ampl*Math.sin(z*TAU*11-t*2)];});add(poly(pts,COLORS.a,2.2));
      for(let j=0;j<4;j++)add(line(-w/2+j*w/3,ampl+18,-w/2+j*w/3,ampl+23,COLORS.c,1,.7));break;
    }
    case 'wave-channels': {
      const rows=2+v%5,w=204,height=106,spacing=height/rows;
      for(let row=0;row<rows;row++){const y=-height/2+(row+.5)*spacing;add(line(-w/2,y,w/2,y,COLORS.c,.7,.38));const pts=Array.from({length:58},(_,j)=>[-w/2+j*w/57,y+Math.sin(j*.25+t*(2+row*.2)+row)*spacing*.26*Math.sin(j*Math.PI/57)]);add(poly(pts,row%2?COLORS.b:COLORS.a,1.4,.86));add(rect(-w/2-9,y-4,4,8,COLORS.a,0,.7,COLORS.a));}
      add(brackets(-w/2-17,-height/2-8,w+34,height+16,9,COLORS.c,.6));break;
    }
    case 'scan-lines': {
      const lines=8+v%11,w=176+v%4*10,h=132,scan=(t*.43+v*.07)%1;
      for(let j=0;j<lines;j++){const yy=-h/2+j*h/(lines-1),distance=Math.abs(j/(lines-1)-scan),len=w*(.68+.32*Math.sin(j*.6+v)**2);add(line(-len/2,yy,len/2,yy,COLORS.a,distance<.08?2.2:1,distance<.14?.9:.24));}
      add(brackets(-w/2-9,-h/2-8,w+18,h+16,9,COLORS.c,.6));break;
    }
    case 'segment-timer': {
      const digits=3+v%6,w=digits*25-8,h=54;add(rect(-w/2-12,-h/2,w+24,h,COLORS.c,1,.6));add(timer(-w/2,-15.5,digits,v,t));
      for(let j=0;j<2+v%4;j++)add(line(-w/2+j*w/(2+v%4),h/2+8,-w/2+j*w/(2+v%4)+12,h/2+8,COLORS.a,2,.7));break;
    }
    case 'warning-panel': {
      const w=176+v%5*10,h=120+v%4*8;add(rect(-w/2,-h/2,w,h,COLORS.c,1,.7));add(poly([[-w/2,-h/2],[-w/2+31,-h/2],[-w/2+38,-h/2+8],[w/2,-h/2+8]],COLORS.warn,2,.9));
      const sides=3+v%3,pts=Array.from({length:sides},(_,j)=>point(-w*.25,0,23+v%4*3,TAU*j/sides-Math.PI/2));add(poly(pts,COLORS.warn,2,.9,'none',true));add(line(-w*.25,-9,-w*.25,5,COLORS.warn,3,.9));add(circle(-w*.25,12,1.8,COLORS.warn,1,1,COLORS.warn));
      for(let j=0;j<3+v%3;j++)add(line(-w*.03,-h*.28+j*13,w*.38-((j+v)%3)*13,-h*.28+j*13,COLORS.a,2,.5+.4*Math.sin(t*2+j)**2));break;
    }
    case 'bar-meter': {
      const sectors=3+v%6,bands=1+v%3;
      for(let band=0;band<bands;band++)for(let j=0;j<sectors;j++){const r=baseR-band*24,theta=j*TAU/sectors+a*(band%2?-1:1),span=TAU/sectors*.64;add(arc(0,0,r,theta,theta+span,COLORS.a,12+band*3,.82));}
      add(circle(0,0,baseR*.2,COLORS.c,1,.8));break;
    }
    case 'arc-meter': {
      const bands=1+v%3,theta=-Math.PI*.82+a,span=Math.PI*1.64;
      for(let j=0;j<bands;j++){const r=baseR-j*24;add(arc(0,0,r,theta,theta+span,COLORS.c,9,.15));add(arc(0,0,r,theta,theta+span*(.32+.6*(.5+.5*Math.sin(t*1.7+j+.2*v))),COLORS.a,11,.9));}
      for(let j=0;j<14+v%8;j++){const p=point(0,0,baseR+9,theta+span*j/(13+v%8)),q=point(0,0,baseR+14,theta+span*j/(13+v%8));add(line(...p,...q,COLORS.b,1,.65));}break;
    }
    case 'scope-grid': {
      const w=165+v%5*10,h=113+v%4*10,bands=1+v%3,progress=.15+.85*smooth((t+.2)%1.6/1.4);
      for(let j=0;j<bands;j++){const x=-w/2-j*9,y=-h/2-j*9,ww=w+j*18,hh=h+j*18;add(poly([[x,y+hh],[x,y+hh*(1-progress)],[x+ww*progress,y],[x+ww,y],[x+ww,y+hh*progress],[x+ww*(1-progress),y+hh]],j?COLORS.c:COLORS.a,j?1:4,j?.5:.9));}break;
    }
    case 'target-boxes': {
      const dots=5+v%10,r=baseR*.76,theta=t*2.2;
      for(let j=0;j<dots;j++){const th=TAU*j/dots,p=point(0,0,r,th),diff=(theta-th+TAU*20)%TAU,op=.15+.8*Math.exp(-diff*.8);add(circle(...p,5+j%3,COLORS.a,0,op,COLORS.a));}
      if(v%3) add(circle(0,0,r-16,COLORS.c,.8,.22));break;
    }
    case 'data-stacks': {
      const rings=2+v%5,expansion=.79+.2*Math.sin(t*2+v*.2);
      for(let j=0;j<rings;j++){const r=(baseR-j*8)*expansion,rot=a*(j%2?-1:1)+j*.7;add(arc(0,0,r,rot,rot+TAU*(.61+j*.025),j%2?COLORS.b:COLORS.a,.8+j%2*.6,.65));}
      add(circle(0,0,16+v%5,COLORS.a,2,.8));for(let j=0;j<20+v%7;j++){const p=point(0,0,22,TAU*j/(20+v%7)+a),q=point(0,0,27,TAU*j/(20+v%7)+a);add(line(...p,...q,COLORS.b,.8,.6));}break;
    }
    case 'pulse-trace': {
      const sectors=3+v%5,weights=Array.from({length:sectors},(_,j)=>1+((j*7+v*3)%5)),total=weights.reduce((a,b)=>a+b,0);let start=-Math.PI/2;
      weights.forEach((weight,j)=>{const end=start+TAU*weight/total-.035,rr=baseR*(.84+.1*Math.sin(t*1.4+j)**2),p=point(0,0,rr,start),q=point(0,0,rr,end);add(path(`M0 0 L${p[0]} ${p[1]} A${n(rr)} ${n(rr)} 0 ${end-start>Math.PI?1:0} 1 ${q[0]} ${q[1]} Z`,j%2?COLORS.c:COLORS.a,1,.42+.13*(j%3),j%2?COLORS.c:COLORS.a));start=end+.035;});add(circle(0,0,baseR+5,COLORS.b,1,.65));break;
    }
    case 'radar-blips': {
      const rings=3+v%4;for(let j=rings;j>0;j--)add(circle(0,0,baseR*j/rings,j%2?COLORS.a:COLORS.c,7+(v%3),.85));
      const theta=-.52+Math.sin(t*.8)*.1,p=point(0,0,baseR+28,theta),q=point(0,0,10,theta);add(line(...p,...q,COLORS.b,4,.9));add(circle(0,0,6,COLORS.a,1,.95,COLORS.a));break;
    }
    case 'micro-tile': {
      const arrows=1+v%3;
      for(let j=0;j<arrows;j++){const r=baseR-j*25,from=-2.7+j*.5,to=from+Math.PI*(1.1+(v%4)*.12)*(.7+.3*Math.sin(t*.9+j)**2);add(arc(0,0,r,from,to,j%2?COLORS.c:COLORS.a,5,.9));const end=point(0,0,r,to),tangent=to+Math.PI/2,tip=[end[0]+Math.cos(tangent)*12,end[1]+Math.sin(tangent)*12],left=[end[0]+Math.cos(tangent+2.4)*10,end[1]+Math.sin(tangent+2.4)*10],right=[end[0]+Math.cos(tangent-2.4)*10,end[1]+Math.sin(tangent-2.4)*10];add(poly([left,tip,right],j%2?COLORS.c:COLORS.a,3,.95));}break;
    }
    case 'bevel-panel': {
      add(circle(0,0,baseR,COLORS.c,1.2,.7,'none',{'stroke-dasharray':`${3+v%3} ${5+v%4}`}));add(arc(0,0,baseR-18,-a,-a+Math.PI*1.4,COLORS.a,1.6,.8));
      const nodes=2+v%6;for(let j=0;j<nodes;j++){const theta=j*TAU/nodes+.2*Math.sin(t*.5),p=point(0,0,baseR,theta);add(circle(...p,9+j%3,COLORS.a,1.5,.9));add(circle(...p,3,COLORS.b,.8,.7));}break;
    }
    case 'coordinate-rail': {
      const r=baseR*.78;add(circle(0,0,r,COLORS.a,2,.85));add(circle(0,0,r+8,COLORS.c,.8,.6));
      const sides=3+v%6,pts=Array.from({length:sides},(_,j)=>point(0,0,r*.38,TAU*j/sides-.5*Math.PI+.09*Math.sin(t)));add(poly(pts,COLORS.b,1.5,.8,'none',true));
      for(let j=0;j<1+v%4;j++){const yy=r*.58+j*4;add(line(-r*.32,yy,r*.32,yy,COLORS.c,1,.6));}break;
    }
  }
  return out.join('');
}

export function render(recipe,t,{width=640,height=360,transparent=true}={}) {
  if(typeof recipe==='string') recipe=records().find(r=>r.id===recipe);
  if(!recipe || !specs.some(s=>s[0]===recipe.mechanism)) throw new Error('Unknown HUD recipe');
  if(!Number.isFinite(t)) throw new Error('Time must be finite');
  const v=recipe.parameters?.variant ?? ((Number(recipe.id.slice(2))-501)%20),seed=recipe.parameters?.seed??719+v*59;
  const time=clamp(t,0,3), entrance=smooth(time/.45),exit=1-smooth((time-2.55)/.45), opacity=entrance*exit;
  let artwork='';
  const elements=layouts(v);
  elements.forEach(([x,y,s],j)=>{
    const delay=Math.min(.16,j*.028),e=smooth((time-delay)/.38)*(1-smooth((time-2.6+j*.018)/.38)),slide=8*(1-smooth((time-delay)/.45));
    artwork+=group(local(recipe.mechanism,v,time+j*.11,seed+j*881,entrance),{transform:`translate(${x} ${n(y+slide)}) scale(${s})`,opacity:n(e)});
  });
  if([5,8,12,15,16,19].includes(v)){
    const pts=elements.map(([x,y])=>[x,y]);
    artwork=group(poly(pts,COLORS.c,.7,.25)+artwork);
  }
  const bg=transparent?'':rect(0,0,640,360,'none',0,1,'#081521');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${n(width)}" height="${n(height)}" viewBox="0 0 640 360">${bg}${group(artwork,{opacity:n(opacity)})}</svg>`;
}
