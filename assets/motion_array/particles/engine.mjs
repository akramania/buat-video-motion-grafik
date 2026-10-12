/* Original vector particle, optical and weather components.
   Motion mechanisms were studied in 5 public Motion Array previews.
   See observations.json for exact source sections; no stock media is bundled. */
const TAU=Math.PI*2;
const MECHANISMS=[
 ['dust_depth','Habuk berlapis','Habuk','MAS017'],['dust_eddy','Pusaran habuk','Habuk','MAS017'],
 ['bokeh_micro','Cahaya mikro','Bokeh','MAPS041'],['bokeh_bloom','Bokeh mengembang','Bokeh','MAPS041'],
 ['bokeh_dual','Bokeh dua kedalaman','Bokeh','MAPS041'],['bokeh_streak','Tabir cahaya','Bokeh','MAPS041'],
 ['bokeh_wide','Bokeh lensa luas','Bokeh','MAPS041'],['bokeh_small','Debu optik halus','Bokeh','MAPS041'],
 ['bokeh_floor','Bokeh dari bawah','Bokeh','MAPS041'],['bokeh_column','Bokeh lajur sisi','Bokeh','MAPS041'],
 ['bokeh_front','Bokeh latar depan','Bokeh','MAPS041'],['bokeh_dense','Bokeh keemasan','Bokeh','MAPS041'],
 ['spark_flow','Aliran bara serong','Bara','MAS020'],['spark_burst','Kipas bara','Bara','MAS020'],
 ['spark_vertical','Bara naik tegak','Bara','MAS020'],['spark_plume','Kepulan bara','Bara','MAS020'],
 ['spark_arc','Bara mengikut lengkung','Bara','MAS020'],['spark_scatter','Serakan bara','Bara','MAS020'],
 ['leak_edge','Cahaya tepi lembut','Light leak','MAS025'],['leak_column','Cahaya sisi ambar','Light leak','MAS025'],
 ['leak_corner','Cahaya penjuru','Light leak','MAS025'],['leak_flash','Kilatan cahaya','Light leak','MAS025'],
 ['rain_splash','Percikan hujan','Hujan','MAS034'],['rain_mist','Hujan berkabus','Hujan','MAS034'],
 ['rain_front','Hujan latar depan','Hujan','MAS034']
];
const STRUCTURES=[
 ['islands','Pulau cahaya','Three separated emitters and unequal cluster footprints'],
 ['diagonal','Laluan serong','Diagonal depth corridor with staggered cluster spacing'],
 ['triptych','Tiga zon','Three vertical windows with interleaved emission phases'],
 ['clear_center','Ruang tengah','Two side fields surrounding a clear center for titles'],
 ['depth','Terowong dalam','Near/mid/far populations with perspective-scaled positions'],
 ['bands','Jalur berselang','Four horizontal bands with alternating local wave paths'],
 ['corner','Penjuru bertingkat','Asymmetric corner cluster with a smaller counterweight'],
 ['halo','Halo terbuka','Broken elliptical belt with a deliberate central aperture'],
 ['fan','Kipas berlapis','Five radial emitter lanes with different opening angles'],
 ['dual','Dua arus','Two interleaved streams with different origin paths'],
 ['floor_edge','Tepi dan bawah','Bottom arc field plus an independent vertical edge'],
 ['orbit','Orbit terpisah','Two offset elliptical orbital fields of different radii'],
 ['weave','Laluan anyaman','S-shaped alternating depth paths and separated crossing points'],
 ['tunnel','Kedalaman bertingkat','Four nested perspective rectangles with near-edge emphasis'],
 ['pockets','Kelompok berselang','Five isolated pockets with asynchronous local motion'],
 ['arch','Lengkung terbuka','Semicircular emitter arch leaving a lower center aperture'],
 ['lattice','Petak perspektif','Staggered modular grid with perspective density changes'],
 ['spiral','Lingkaran beransur','Open spiral cluster with increasing local radius'],
 ['wave','Gelombang lapis','Three broad sinusoidal bands with unequal amplitudes'],
 ['staggered','Siri kelompok','Alternating left/right pockets with independent emission phases']
];
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,Number.isFinite(x)?x:a));
const smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
const mix=(a,b,t)=>a+(b-a)*t;
const frac=x=>x-Math.floor(x);
const f=x=>(Number.isFinite(x)?x:0).toFixed(3).replace(/\.?0+$/,'');
const h=(n,seed)=>frac(Math.sin((n+1)*127.1+seed*311.7)*43758.5453123);
const C=(x,y,r,color,o=1)=>`<circle cx="${f(x)}" cy="${f(y)}" r="${f(Math.max(0,r))}" fill="${color}" opacity="${f(clamp(o))}"/>`;
const E=(x,y,rx,ry,color,o=1,rot=0)=>`<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(Math.max(0,rx))}" ry="${f(Math.max(0,ry))}" fill="${color}" opacity="${f(clamp(o))}" transform="rotate(${f(rot)} ${f(x)} ${f(y)})"/>`;
const L=(x,y,xx,yy,color,w=1,o=1)=>`<path d="M${f(x)} ${f(y)}L${f(xx)} ${f(yy)}" fill="none" stroke="${color}" stroke-width="${f(w)}" stroke-linecap="round" opacity="${f(clamp(o))}"/>`;
const PALETTES=[['#ffce86','#fa8763','#fff3da'],['#c8edff','#70bfda','#f4fbff'],['#e6b6fb','#a67cdd','#f8e6ff'],['#ffbd65','#e37942','#ffeac7']];
function makeRecords(){
 const out=[];
 MECHANISMS.forEach(([mechanism,title,category,source],m)=>STRUCTURES.forEach(([layout,label,basis],v)=>{
  const id=`MA${String(1501+m*20+v).padStart(4,'0')}`;
  out.push({id,title:`${title} — ${label}`,category,mechanism,variant_basis:basis,tags:['motion-array-preview-adaptation','original-vector',mechanism,layout,category.toLowerCase()],use_cases:['video promosi','video montaj','video vlogging','video explainer'],duration:3,group:'particles',parameters:{mechanism_index:m,adaptation_index:v,layout,population:42+(v%7)*7,cluster_count:2+v%4,depth_layers:2+v%3,path_bend:.28+(v%5)*.12,emitter_count:1+v%5,phase_segments:2+v%4,seed:1807+m*1009+v*283},source_ids:[source],observation_ids:[`MAPO${String(m+1).padStart(3,'0')}`],blend_mode:category==='Hujan'?'normal':'screen',alpha:true,adaptation:'Authored SVG geometry and 3-second choreography based on the recorded public-preview observation; no source footage.'});
 }));
 return out;
}
const CATALOG=makeRecords();
export function records(){return CATALOG.map(r=>({...r,parameters:{...r.parameters},tags:[...r.tags],source_ids:[...r.source_ids],observation_ids:[...r.observation_ids]}));}
function resolve(recipe){
 const id=typeof recipe==='string'?recipe:recipe?.id;
 const r=CATALOG.find(q=>q.id===id);
 if(!r)throw new RangeError('Unknown particles recipe ID');
 if(typeof recipe!=='object'||!recipe.parameters)return r;
 const p={...r.parameters},q=recipe.parameters;
 for(const [key,lo,hi,integer] of [['adaptation_index',0,19,true],['population',10,180,true],['cluster_count',1,8,true],['depth_layers',1,4,true],['path_bend',0,2,false],['emitter_count',1,8,true],['phase_segments',1,8,true],['seed',1,2147483647,true]])if(Number.isFinite(Number(q[key]))){const value=clamp(Number(q[key]),lo,hi);p[key]=integer?Math.round(value):value;}
 p.layout=STRUCTURES[p.adaptation_index][0];
 return {...r,parameters:p};
}
/* Structural layouts intentionally change emitter topology, empty space and paths. */
function layoutPoint(v,u,w,i,time=0){
 const cx=320,cy=180;
 switch(v){
 case 0:{const k=i%3;const a=[[-145,-52],[104,-35],[-14,84]][k];return[cx+a[0]+(u-.5)*166,cy+a[1]+(w-.5)*106];}
 case 1:return[40+u*560,302-u*237+(w-.5)*94];
 case 2:return[65+(i%3)*215+(u-.5)*92,32+w*298];
 case 3:return[i%2?436+u*188:16+u*188,22+w*316];
 case 4:{const z=i%3,s=[.48,.75,1.11][z];return[cx+(u-.5)*580*s,cy+(w-.5)*320*s];}
 case 5:return[20+u*600,44+(i%4)*91+Math.sin(u*TAU+(i%4)*.9+time*.45)*16];
 case 6:return[i%4?cx-176+(u-.5)*236:cx+211+(u-.5)*89,i%4?cy+69+(w-.5)*148:cy-108+(w-.5)*68];
 case 7:{const a=u*TAU+.42,r=.68+w*.28;return[cx+Math.cos(a)*258*r,cy+Math.sin(a)*138*r];}
 case 8:{const lane=i%5,a=-.8+lane*.4,r=45+u*286;return[57+r*Math.cos(a),180+r*Math.sin(a)+(w-.5)*30];}
 case 9:{const k=i%2;return[22+u*598, k?70+u*187+(w-.5)*61:278-u*183+(w-.5)*61];}
 case 10:return[i%3?16+u*608:592+(u-.5)*53,i%3?288+Math.sin(u*Math.PI)*38+(w-.5)*43:30+w*300];
 case 11:{const k=i%2,a=u*TAU,r=.75+w*.25;return[(k?425:206)+Math.cos(a)*(k?150:122)*r,cy+Math.sin(a)*(k?94:137)*r];}
 case 12:return[22+u*596,cy+Math.sin(u*TAU*1.25+(i%2)*Math.PI)*111+(w-.5)*36];
 case 13:{const z=i%4,sz=.43+z*.19;const edge=i%4;return edge%2?[cx+(u-.5)*618*sz,cy+(edge===1?-1:1)*160*sz]:[cx+(edge===0?-1:1)*300*sz,cy+(w-.5)*328*sz];}
 case 14:{const k=i%5,a=k*TAU/5-.4;return[cx+Math.cos(a)*203+(u-.5)*85,cy+Math.sin(a)*97+(w-.5)*68];}
 case 15:{const a=Math.PI+(u*Math.PI);return[cx+Math.cos(a)*(210+w*59),cy+50+Math.sin(a)*(111+w*40)];}
 case 16:{const c=i%7,r=Math.floor(i/7)%4;return[49+c*90+(u-.5)*53,44+r*87+(w-.5)*53];}
 case 17:{const a=u*TAU*2.2,r=24+u*267;return[cx+Math.cos(a)*r+(w-.5)*31,cy+Math.sin(a)*r*.51+(w-.5)*25];}
 case 18:return[14+u*612,51+(i%3)*125+Math.sin(u*TAU*.8+(i%3)*1.4)*31+(w-.5)*36];
 default:{const k=i%6;return[k%2?415+(u-.5)*168:174+(u-.5)*168,44+Math.floor(k/2)*134+(w-.5)*72];}
 }
}
function glowDefs(prefix,palette){
 return `<defs><radialGradient id="${prefix}g"><stop offset="0" stop-color="${palette[2]}" stop-opacity=".85"/><stop offset=".22" stop-color="${palette[0]}" stop-opacity=".54"/><stop offset=".68" stop-color="${palette[1]}" stop-opacity=".16"/><stop offset="1" stop-color="${palette[1]}" stop-opacity="0"/></radialGradient><radialGradient id="${prefix}d"><stop offset="0" stop-color="${palette[0]}" stop-opacity=".5"/><stop offset=".8" stop-color="${palette[0]}" stop-opacity=".38"/><stop offset="1" stop-color="${palette[0]}" stop-opacity="0"/></radialGradient><radialGradient id="${prefix}h"><stop offset="0" stop-color="${palette[0]}" stop-opacity=".38"/><stop offset=".58" stop-color="${palette[1]}" stop-opacity=".2"/><stop offset="1" stop-color="${palette[1]}" stop-opacity="0"/></radialGradient><linearGradient id="${prefix}s" x1="0" y1="1" x2="1" y2="0"><stop stop-color="${palette[1]}" stop-opacity="0"/><stop offset=".6" stop-color="${palette[0]}" stop-opacity=".72"/><stop offset="1" stop-color="${palette[2]}"/></linearGradient></defs>`;
}
function dust(r,t,prefix,palette){
 const p=r.parameters,v=p.adaptation_index,seed=p.seed,b=[];
 const fog=r.mechanism==='dust_eddy';
 if(fog)for(let i=0;i<6+p.cluster_count;i++){
  const u=h(i,seed),w=h(i+70,seed),pt=layoutPoint(v,u,w,i,t),dx=Math.sin(t*.5+i*.91)*42,dy=Math.cos(t*.39+i)*18;
  b.push(E(pt[0]+dx,pt[1]+dy,66+h(i+8,seed)*114,28+h(i+5,seed)*67,`url(#${prefix}h)`,.25+h(i+20,seed)*.25,12+Math.sin(t*.7+i)*25));
 }
 const n=p.population+38;
 for(let i=0;i<n;i++){
  const u=h(i,seed),w=h(i+151,seed),pt=layoutPoint(v,u,w,i,t),depth=.3+(i%p.depth_layers)/p.depth_layers*.72+h(i+66,seed)*.19;
  const dx=Math.sin(t*.62+i*.7)*13*depth+t*3*depth,dy=-t*6*depth+Math.sin(t*.41+i)*7;
  const rr=.5+h(i+21,seed)*1.85*depth,op=.18+h(i+89,seed)*.57;
  if(i%11===0)b.push(C(pt[0]+dx,pt[1]+dy,rr*3.8,`url(#${prefix}g)`,op*.48));
  b.push(C(pt[0]+dx,pt[1]+dy,rr,palette[i%11===0?2:0],op*(.7+.3*Math.sin(t*.9+i))));
 }
 return b.join('');
}
function bokeh(r,t,prefix,palette){
 const p=r.parameters,v=p.adaptation_index,s=p.seed,m=r.mechanism,b=[];
 const big=['bokeh_wide','bokeh_column','bokeh_front','bokeh_dense','bokeh_dual','bokeh_floor','bokeh_bloom'].includes(m);
 const count=m==='bokeh_dense'?p.population:m==='bokeh_small'?p.population+22:m==='bokeh_micro'?p.population+20:m==='bokeh_streak'?p.cluster_count*3:16+p.cluster_count*3;
 if(m==='bokeh_streak'){
  for(let k=0;k<p.cluster_count+2;k++){
   const pt=layoutPoint(v,h(k,s),h(k+19,s),k,t);
   b.push(E(pt[0]+Math.sin(t*.6+k)*45,pt[1]+Math.cos(t*.42+k)*18,144+h(k+20,s)*105,17+h(k+14,s)*33,`url(#${prefix}h)`,.65,Math.sin(k*1.7)*16));
  }
 }
 for(let i=0;i<count;i++){
  const u=h(i,s),w=h(i+117,s),pt=layoutPoint(v,u,w,i,t),depth=.42+(i%p.depth_layers)/p.depth_layers*.64+h(i+92,s)*.19;
  let x=pt[0]+Math.sin(t*.42+i*.63)*13*depth,y=pt[1]+Math.cos(t*.51+i)*11*depth;
  let rr=big?12+h(i+27,s)*31:1.4+h(i+27,s)*5.8;
  if(m==='bokeh_micro')rr=.8+h(i+28,s)*2.6;
  if(m==='bokeh_floor')y=262+Math.abs(pt[1]-180)*.58-t*(7+depth*5);
  if(m==='bokeh_column'){
   const lane=(v%4)+1;x=(i%lane)/(Math.max(1,lane-1))*120+(v%2?462:54)+Math.sin(t*.5+i)*11;
   y=20+u*342+Math.cos(t*.36+i)*14;
  }
  if(m==='bokeh_front'){rr=20+h(i+27,s)*41;y=178+(pt[1]-180)*.81;}
  if(m==='bokeh_wide')rr=23+h(i+27,s)*29;
  if(m==='bokeh_dense')rr=9+h(i+27,s)*27;
  if(m==='bokeh_bloom')rr=(18+h(i+27,s)*38)*(1+.48*Math.sin(clamp(t/3)*Math.PI));
  let o=.34+h(i+81,s)*.47;
  if(i%3===0)o*=.52;
  b.push(C(x,y,rr,`url(#${prefix}${m==='bokeh_micro'?'g':'d'})`,o));
  if(big&&i%4===0)b.push(`<circle cx="${f(x)}" cy="${f(y)}" r="${f(rr*.91)}" fill="none" stroke="${palette[0]}" stroke-width=".65" opacity="${f(o*.19)}"/>`);
  if((m==='bokeh_dual'||m==='bokeh_small'||m==='bokeh_micro')&&i%2===0)b.push(C(x+13,y-19,.7+h(i+99,s)*1.1,palette[2],.5+h(i+133,s)*.4));
 }
 if(m==='bokeh_dual'||m==='bokeh_small'||m==='bokeh_micro')for(let i=0;i<36;i++){
  const pt=layoutPoint(v,h(i+600,s),h(i+701,s),i,t);
  b.push(C(pt[0]+Math.sin(t*.58+i)*9,pt[1]-t*7+Math.sin(t*.6+i)*5,.5+h(i+900,s)*1.15,palette[2],.21+h(i+802,s)*.6));
 }
 if(m==='bokeh_bloom'){
  const pulse=Math.pow(Math.sin(clamp(t/3)*Math.PI),3);
  b.push(E(320,180,440*pulse,280*pulse,`url(#${prefix}g)`,.55*pulse));
 }
 return b.join('');
}
function sparks(r,t,prefix,palette){
 const p=r.parameters,v=p.adaptation_index,s=p.seed,m=r.mechanism,b=[];
 const n=p.population+17;
 for(let i=0;i<n;i++){
  const u=h(i,s),w=h(i+117,s),depth=.38+h(i+132,s),life=frac(t*.31+h(i+78,s)+(i%p.phase_segments)/p.phase_segments),fade=Math.sin(life*Math.PI),pt=layoutPoint(v,u,w,i,t),origin=layoutPoint(v,h(i%p.emitter_count,s+1),h(i%p.emitter_count+30,s+1),i%p.emitter_count,t);
  let x,y,dx,dy;
  if(m==='spark_flow'){
   x=pt[0]-220+life*440;y=pt[1]+110-life*220+Math.sin(life*Math.PI)*p.path_bend*42;dx=9+depth*9;dy=-dx*.47;
  }else if(m==='spark_burst'){
   const angle=-1.18+(u-.5)*1.32;
   const radius=life*(108+depth*174);
   x=origin[0]+Math.cos(angle)*radius;y=origin[1]+Math.sin(angle)*radius;dx=Math.cos(angle)*(8+depth*9);dy=Math.sin(angle)*(8+depth*9);
  }else if(m==='spark_vertical'){
   x=pt[0]+Math.sin(life*3.1+i)*16*depth;y=380-life*460+(pt[1]-180)*.46;dx=Math.cos(life*3+i)*1.7;dy=-7-depth*11;
  }else if(m==='spark_plume'){
   x=origin[0]+(u-.5)*74+Math.sin(life*3.8+i)*life*45;y=350-life*(286+depth*70)+(origin[1]-180)*.36;dx=Math.cos(life*3.8+i)*3.5;dy=-10-depth*15;
  }else if(m==='spark_arc'){
   x=origin[0]-145+life*290;y=origin[1]+56-Math.sin(life*Math.PI)*(74+p.path_bend*56);dx=8+depth*10;dy=-Math.cos(life*Math.PI)*9;
  }else{
   const a=u*TAU,radius=life*(52+depth*158);
   x=pt[0]+Math.cos(a)*radius;y=pt[1]+Math.sin(a)*radius*.7;dx=Math.cos(a)*(7+depth*9);dy=Math.sin(a)*(7+depth*9)*.7;
  }
  const op=fade*(.54+h(i+98,s)*.46),size=.65+depth*1.75;
  if(i%5===0)b.push(C(x,y,7+depth*3,`url(#${prefix}g)`,op*.59));
  b.push(L(x-dx,y-dy,x,y,`url(#${prefix}s)`,size,op));
  if(i%3===0)b.push(C(x,y,size*.54,palette[2],op*.9));
 }
 return b.join('');
}
function lightLeaks(r,t,prefix,palette){
 const p=r.parameters,v=p.adaptation_index,s=p.seed,m=r.mechanism,b=[];
 const progress=clamp(t/3),pulse=Math.pow(Math.sin(progress*Math.PI),m==='leak_flash'?3:1.25);
 for(let i=0;i<p.cluster_count+2;i++){
  const u=h(i,s),w=h(i+29,s),pt=layoutPoint(v,u,w,i,t);
  let x=pt[0],y=pt[1],rx=124+u*122,ry=124+w*117;
  if(m==='leak_edge'){x=(v%2?632:8)+(i%2?28:-28)+Math.sin(t*.8+i)*37;y=32+i/(p.cluster_count+1)*298;rx=145+u*113;ry=93+w*95;}
  if(m==='leak_column'){x=(v%2?512:128)+(i%2?28:-28)+Math.sin(t*.57+i)*24;y=14+i/(p.cluster_count+1)*330;rx=67+u*82;ry=113+w*155;}
  if(m==='leak_corner'){x=(v%2?601:39)+(i%2?-30:30);y=(v%3?310:36)+(i%2?-39:25);rx=140+u*124;ry=109+w*135;}
  if(m==='leak_flash'){x=320+(pt[0]-320)*.5;y=180+(pt[1]-180)*.5;rx=133+u*174+pulse*160;ry=123+w*138+pulse*117;}
  const spread=1+.13*Math.sin(t*.76+i*.74);
  b.push(E(x,y,rx*spread,ry/spread,`url(#${prefix}g)`,(.48+u*.38)*pulse,Math.sin(i+t*.3)*22));
 }
 // Every structural adaptation also changes the secondary emitter arrangement.
 for(let i=0;i<2+p.emitter_count;i++){
  const pt=layoutPoint(v,h(i+290,s),h(i+390,s),i,t);
  b.push(E(pt[0]+Math.sin(t*.5+i)*21,pt[1],65+h(i+393,s)*105,19+h(i+690,s)*55,`url(#${prefix}h)`,pulse*.4,12+Math.sin(i*2)*30));
 }
 if(m==='leak_flash')b.push(`<rect x="0" y="0" width="640" height="360" fill="${palette[2]}" opacity="${f(pulse*.61)}"/>`);
 return b.join('');
}
function rain(r,t,prefix,palette){
 const p=r.parameters,v=p.adaptation_index,s=p.seed,m=r.mechanism,b=[];
 if(m==='rain_mist')for(let i=0;i<6+p.cluster_count;i++){
  const pt=layoutPoint(v,h(i,s),h(i+37,s),i,t),shift=Math.sin(t*.32+i*.6)*39;
  b.push(E(pt[0]+shift,pt[1]+40,93+h(i+41,s)*90,35+h(i+81,s)*59,`url(#${prefix}h)`,.3,Math.sin(t*.4+i)*9));
 }
 if(m!=='rain_splash'){
  const n=m==='rain_front'?p.population+54:p.population;
  for(let i=0;i<n;i++){
   const u=h(i,s),w=h(i+301,s),depth=.35+h(i+41,s)*.85,pt=layoutPoint(v,u,w,i,t),life=frac(t*(.62+depth*.25)+h(i+401,s));
   const x=pt[0]+(life-.5)*(v%3-1)*20,y=-40+life*440;
   const len=(m==='rain_front'?13:5)+depth*(m==='rain_front'?23:10),angle=(v%4-1.5)*.12;
   b.push(L(x,y,x+len*angle,y+len,palette[2],m==='rain_front'?.65+depth:.6+depth*.3,.16+depth*.37));
  }
 }
 // Perspective splash crowns are explicit vector arcs, independent of copied imagery.
 const splashN=m==='rain_splash'?26+p.cluster_count*5:12+p.cluster_count*3;
 for(let i=0;i<splashN;i++){
  const u=h(i+700,s),z=.18+h(i+831,s)*.82,life=frac(t*.78+h(i+800,s)),fade=Math.sin(life*Math.PI),pt=layoutPoint(v,u,h(i+612,s),i,t);
  const x=pt[0],y=205+z*139,rx=(2+z*13)*life,ry=(1+z*2.2)*life;
  if(life<.72){
   b.push(`<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(ry)}" fill="none" stroke="${palette[1]}" stroke-width="${f(.5+z*.5)}" opacity="${f(fade*.47)}"/>`);
   for(let k=0;k<3+(v%3);k++){
    const a=(k/(3+v%3))*Math.PI+.14,hgt=Math.sin(life*Math.PI)*(.8+z*11),dx=Math.cos(a)*rx;
    b.push(L(x+dx*.3,y-hgt*.3,x+dx,y-hgt,palette[2],.55+z*.46,fade*.51));
    b.push(C(x+dx,y-hgt,.42+z*.65,palette[2],fade*.58));
   }
  }
 }
 return b.join('');
}
export function render(recipe,t,{width=640,height=360,transparent=true}={}){
 const r=resolve(recipe),m=r.mechanism,index=r.parameters.mechanism_index,prefix=r.id.toLowerCase(),time=clamp(Number(t),0,3),w=Math.round(clamp(Number(width),1,8192)),hh=Math.round(clamp(Number(height),1,8192));
 const palette=index<2?PALETTES[1]:index>=22?PALETTES[1]:index===20?PALETTES[2]:index>=12&&index<=19?PALETTES[3]:PALETTES[0];
 const envelope=smooth(time/.32)*smooth((3-time)/.4);
 let body='';
 if(envelope>0){
  if(m.startsWith('dust_'))body=dust(r,time,prefix,palette);
  else if(m.startsWith('bokeh_'))body=bokeh(r,time,prefix,palette);
  else if(m.startsWith('spark_'))body=sparks(r,time,prefix,palette);
  else if(m.startsWith('leak_'))body=lightLeaks(r,time,prefix,palette);
  else body=rain(r,time,prefix,palette);
 }
 return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${hh}" viewBox="0 0 640 360">${glowDefs(prefix,palette)}${transparent?'':'<rect width="640" height="360" fill="#07111d"/>'}<g opacity="${f(envelope)}">${body}</g></svg>`;
}
export default {records,render};
