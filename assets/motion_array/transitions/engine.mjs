// Original, editable vector choreography. Public preview provenance is attached
// after visual observation; no Motion Array source media is included.
const W=640,H=360,TAU=Math.PI*2;
const PALETTES=[['#18c9be','#b3f2e9','#13798a'],['#52a8ff','#c0dcff','#245f9e'],['#a885ea','#e2d3ff','#655097'],['#edba60','#ffedc6','#a57c35']];
const clamp=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const smooth=x=>{x=clamp(x);return x*x*(3-2*x);};
const ease=x=>1-Math.pow(1-clamp(x),3);
const n=x=>Number(x.toFixed(3));
const pts=a=>a.map(p=>p.map(n).join(',')).join(' ');
const poly=(a,c,extra='')=>`<polygon points="${pts(a)}" fill="${c}" ${extra}/>`;
const circle=(x,y,r,c,extra='')=>`<circle cx="${n(x)}" cy="${n(y)}" r="${n(Math.max(0,r))}" fill="${c}" ${extra}/>`;
const path=(d,c,extra='')=>`<path d="${d}" fill="${c}" ${extra}/>`;
const line=(d,c,width,extra='')=>path(d,'none',`stroke="${c}" stroke-width="${n(width)}" stroke-linecap="round" stroke-linejoin="round" ${extra}`);
const rect=(x,y,w,h,c,extra='')=>`<rect x="${n(x)}" y="${n(y)}" width="${n(Math.max(0,w))}" height="${n(Math.max(0,h))}" fill="${c}" ${extra}/>`;
const esc=s=>String(s).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[m]));
const envelope=t=>{t=clamp(t/3);return t<.38?ease(t/.38):t>.59?1-smooth((t-.59)/.41):1;};
const local=(t,delay=0)=>envelope(t-delay);
const axisPoint=(cx,cy,r,a)=>[cx+r*Math.cos(a),cy+r*Math.sin(a)];
function scallop(cx,cy,r,lobes,depth,phase=0){
 const a=[];for(let j=0;j<=lobes*12;j++){const th=j/(lobes*12)*TAU;const rr=r*(1-depth*.5+depth*.5*Math.cos(th*lobes+phase));a.push(axisPoint(cx,cy,rr,th));}return a;
}
function ribbon(y,amp,waves,phase,thickness=60){
 const top=[],bottom=[];for(let j=0;j<=40;j++){const x=-100+j*21;const yy=y+amp*Math.sin(j/40*TAU*waves+phase);top.push([x,yy-thickness/2]);bottom.unshift([x,yy+thickness/2]);}return [...top,...bottom];
}
const TILE_PAIRS=[['circle','circle'],['circle','hexagon'],['circle','square'],['circle','triangle'],['hexagon','hexagon'],['hexagon','square'],['square','square'],['square','triangle'],['triangle','circle'],['triangle','triangle']];
const MECHANISMS=[
 ...TILE_PAIRS.map(([a,b])=>[`tile_${a}_${b}`,`${a[0].toUpperCase()+a.slice(1)} → ${b} tile wipe`,'geometric']),
 ['liquid_petal_burst','Petal splash burst','liquid'],
 ['liquid_concave_square_iris','Concave square iris','liquid'],
 ['liquid_drip_curtain','Scalloped liquid curtain','liquid'],
 ['liquid_spiral_curl','Liquid spiral curl','liquid'],
 ['liquid_scallop_sidewipe','Scalloped liquid sidewipe','liquid'],
 ['liquid_diagonal_strips','Diagonal liquid strips','liquid'],
 ['liquid_spiky_bloom','Irregular splash bloom','liquid'],
 ['liquid_vertical_ribbons','Wavering vertical ribbons','liquid'],
 ['smoke_fragment_ring','Fragmented smoke ring','smoke'],
 ['smoke_cluster_cover','Clustered smoke cover','smoke'],
 ['smoke_arc_puff_sweep','Curved puff sweep','smoke'],
 ['smoke_horizontal_streaks','Horizontal smoke streaks','smoke'],
 ['smoke_curling_puff','Curling smoke puff','smoke'],
 ['smoke_vertical_plume','Vertical smoke plume','smoke'],
 ['smoke_ground_roll','Ground smoke roll','smoke']
];
let PROVENANCE=Object.fromEntries(MECHANISMS.map(([m],i)=>[m,{source_ids:[i<10?'MAS006':i<18?'MAS004':'MAS005'],observation_ids:[`MAOBS-TR${String(i+1).padStart(2,'0')}`],scope:'Actual public video preview geometry observed; recipe is an original structural adaptation.'}]));
export function withProvenance(mapping={}){PROVENANCE={...PROVENANCE,...mapping};return records();}
export function records(){return MECHANISMS.flatMap(([mechanism,title,category],mi)=>Array.from({length:20},(_,v)=>{
 const id=`MA${String(1001+mi*20+v).padStart(4,'0')}`;
 const p={variant:v,count:3+v%5,lobes:3+(v*2)%7,bend:.18+.045*Math.floor(v/4),spacing:.75+.09*(v%4),offset:(v%5-2)*.085,phase:(v%4)*Math.PI/8,stagger:(v%5)*.035,rows:3+Math.floor(v/4),columns:6+v%4,center_x:320+(v%5-2)*34,center_y:180+(Math.floor(v/5)-1.5)*20,aspect:.65+(v%4)*.18};
 const proof=PROVENANCE[mechanism]||{};
 return {id,title:`${title} · ${String(v+1).padStart(2,'0')}`,category,mechanism,variant_basis:`Topology ${p.count}, ${p.lobes} lobes, ${p.rows}×${p.columns} spacing, offset ${p.offset}, bend ${p.bend.toFixed(3)}; staggered layer choreography`,tags:['motion-array-inspired','original-vector',category,'transition','transparent'],use_cases:['scene transition','multi-layer motion graphic','explainer','promotion','montage'],duration:3,poster_time:mi<10?.14:mi<18?.32:.85,group:'transitions',parameters:p,source_ids:proof.source_ids||[],observation_ids:proof.observation_ids||[],observation_scope:proof.scope||'pending visual provenance; original choreography only'};
}));}

export function render(recipe,t,{width=640,height=360,transparent=true}={}){
 const rr=typeof recipe==='string'?records().find(r=>r.id===recipe):recipe;
 if(!rr||!MECHANISMS.some(m=>m[0]===rr.mechanism))throw new Error('Unknown transition recipe');
 t=clamp(Number.isFinite(t)?t:0,0,3); const p=rr.parameters,v=p.variant,m=rr.mechanism,e=envelope(t),cx=p.center_x,cy=p.center_y;
 const palette=m.startsWith('smoke_')?['#f3f6fa','#c7d2db','#8697a7']:PALETTES[v%PALETTES.length]; const col=i=>palette[((i%palette.length)+palette.length)%palette.length];let s='';
 if(e>0.00001){
 if(m.startsWith('tile_')){
   const [,a,b]=m.split('_'), entering=t<1.45, shape=entering?a:b;
   const cols=p.columns,rows=p.rows,w=640/cols,h=360/rows,layout=v%4;
   for(let y=-1;y<=rows;y++)for(let x=-1;x<=cols;x++){
     let xx=x*w+w/2,yy=y*h+h/2;
     if(layout===1)xx+=(y%2)*w*.45;
     if(layout===2){const q=(x+cols+y*2)*.13;xx+=Math.sin(q)*w*.22;yy+=Math.cos(q)*h*.2;}
     if(layout===3){xx+=(y-rows/2)*w*.15;yy+=(x-cols/2)*h*.09;}
     const distance=layout===0?(x+y)/Math.max(1,cols+rows):layout===1?Math.hypot(x-cols/2,y-rows/2)/Math.hypot(cols/2,rows/2):layout===2?(y+1)/(rows+2):(x+1)/(cols+2);
     const delay=distance*p.stagger*2;const ee=local(t,delay),r=Math.hypot(w,h)*.92*ee;
     const rot=(v%3)*.09+(1-ee)*p.bend;
     if(shape==='circle')s+=circle(xx,yy,r,col(0));
     else if(shape==='square')s+=rect(xx-r*.8,yy-r*.8,r*1.6,r*1.6,col(0),`transform="rotate(${n(rot*180/Math.PI)} ${n(xx)} ${n(yy)})"`);
     else s+=poly(Array.from({length:shape==='hexagon'?6:3},(_,k)=>axisPoint(xx,yy,r,k*TAU/(shape==='hexagon'?6:3)-Math.PI/2+rot)),col(0));
   }
 }else if(m==='liquid_concave_square_iris'){
   for(let i=2;i>=0;i--){const ee=local(t,i*.06),hw=ee*(420+i*26),hh=ee*(260+i*14),dent=(1-ee*.6)*hw*p.bend; s+=path(`M${n(cx-hw)},${n(cy-hh)} Q${cx},${n(cy-hh+dent)} ${n(cx+hw)},${n(cy-hh)} Q${n(cx+hw-dent)},${cy} ${n(cx+hw)},${n(cy+hh)} Q${cx},${n(cy+hh-dent)} ${n(cx-hw)},${n(cy+hh)} Q${n(cx-hw+dent)},${cy} ${n(cx-hw)},${n(cy-hh)}Z`,col(i));}
 }else if(m==='liquid_vertical_ribbons'){
   const pitch=640/p.columns;for(let i=0;i<p.columns+1;i++){const ee=local(t,(i%3)*p.stagger),a=[],b=[];for(let j=0;j<=36;j++){const yy=-60+j*480/36,xx=i*pitch+Math.sin(j/36*TAU*(1+v%3)+p.phase+i*.7)*(18+p.bend*40),hw=ee*pitch*.64;a.push([xx-hw,yy]);b.unshift([xx+hw,yy]);}s+=poly([...a,...b],col(i));}
 }else if(m==='smoke_fragment_ring'){
   const rad=e*(70+v%4*25),count=p.lobes+8;for(let i=0;i<count;i++){const a=TAU*i/count+p.phase+t*.25,rr=rad+Math.sin(a*3)*e*8;const size=e*(18+(i%3)*7)*(t>1.8?1-clamp((t-1.8)/1.2)*.5:1);s+=poly(scallop(cx+Math.cos(a)*rr,cy+Math.sin(a)*rr,size,5+i%3,.23,a),col(0));}
 }else if(m==='smoke_arc_puff_sweep'){
   const count=p.count+5;for(let i=0;i<count;i++){const q=i/(count-1),ee=local(t,i*.025),a=-Math.PI*.75+q*Math.PI*1.18+p.phase*.4,x=cx+Math.cos(a)*(80+v%4*18),y=cy+Math.sin(a)*(65+v%3*18);s+=poly(scallop(x,y,ee*(22+q*48),4+(i%4),.17+p.bend*.2,i*.6),col(0));}
 }else if(m==='smoke_horizontal_streaks'){
   for(let i=0;i<p.count;i++){const ee=local(t,i*.06),yy=cy+(i-(p.count-1)/2)*(16+v%4*6),x=cx-ee*(140+i*12),len=ee*(240+i*15),tail=ee*(10+p.lobes*2);s+=line(`M${n(x)},${n(yy)} C${n(x+len*.25)},${n(yy-20*p.bend)} ${n(x+len*.6)},${n(yy+16*p.bend)} ${n(x+len)},${n(yy)}`,col(0),tail);s+=poly(scallop(x+len,yy,ee*(15+i%3*4),4+i%3,.23,i),col(0));}
 }else if(m==='smoke_curling_puff'){
   for(let k=0;k<2+(v%3);k++){const ee=local(t,k*.07),a=[];for(let j=0;j<=50;j++){const q=j/50,th=-Math.PI/2+q*TAU*(.8+p.bend),rad=ee*(85+v%4*12)*(1-q*.72);a.push([cx-80+k*24+Math.cos(th)*rad,cy+35+k*8+Math.sin(th)*rad]);}s+=line(`M${a.map(q=>q.map(n).join(',')).join(' L')}`,col(0),ee*(14+p.lobes*2));}s+=path(`M${n(cx-140*e)},${n(cy+80*e)} Q${n(cx-55*e)},${n(cy+30*e)} ${n(cx+30*e)},${n(cy+80*e)}Z`,col(0));
 }else if(m==='smoke_vertical_plume'){
   const count=p.rows+4;for(let i=0;i<count;i++){const q=i/(count-1),ee=local(t,i*.055),x=cx+Math.sin(q*TAU*(1+v%3)+p.phase)*ee*(18+p.bend*25),y=300-q*ee*235,r=ee*(14+q*(22+v%4*8));s+=poly(scallop(x,y,r,4+(i%4),.2,i),col(0));}
 }else if(m==='smoke_ground_roll'){
   const count=p.count+4;for(let i=0;i<count;i++){const q=i/(count-1),ee=local(t,i*.045),x=cx-105+q*ee*220,y=cy+65-Math.sin(q*Math.PI)*ee*(25+p.bend*35),r=ee*(12+Math.sin(q*Math.PI)*(38+v%4*10));s+=poly(scallop(x,y,r,4+i%3,.2,i),col(0));}s+=line(`M${n(cx-150*e)},${cy+82} L${n(cx+150*e)},${cy+82}`,col(0),e*(8+p.lobes));
 }else if(m==='liquid_wave_curtain'){
   for(let i=p.count-1;i>=0;i--){const ee=local(t,i*.028),y=-145+ee*690-i*26; const edge=[];for(let j=0;j<=40;j++){let x=j*16;edge.push([x,y+(24+p.bend*90)*Math.sin(j/40*TAU*(1+v%3)+p.phase+i*.52)]);}s+=poly([[0,-150],[640,-150],...edge.reverse()],col(i));}
 }else if(m==='liquid_drip_curtain'){
   for(let layer=2;layer>=0;layer--){const ee=local(t,layer*.06),base=-110+ee*560-layer*18;const d=[];for(let j=0;j<=p.columns*12;j++){const x=j/(p.columns*12)*640;const yy=base+Math.sin(j/12*Math.PI)*(30+p.lobes*6)+Math.cos(j/(p.columns*12)*TAU+p.phase)*20;d.push([x,yy]);}s+=poly([[0,-180],[640,-180],...d.reverse()],col(layer));}
 }else if(m==='smoke_cluster_cover'){
   for(let i=p.count-1;i>=0;i--){const angle=TAU*i/p.count+p.phase;const dist=55+v%4*24;const x=cx+Math.cos(angle)*dist,y=cy+Math.sin(angle)*dist;const ee=local(t,i*p.stagger);s+=poly(scallop(x,y,ee*(420+v%3*45),p.lobes,.14+p.bend*.24,i),col(i));}
 }else if(m==='liquid_branch_splash'){
   s+=circle(cx,cy,e*155,col(0));for(let i=0;i<p.count+3;i++){const a=TAU*i/(p.count+3)+p.phase,ee=local(t,i*.018);const x=cx+Math.cos(a)*ee*310,y=cy+Math.sin(a)*ee*310;const a2=a+p.bend;const ctl=axisPoint(cx,cy,ee*180,a2);s+=line(`M${cx},${cy} Q${n(ctl[0])},${n(ctl[1])} ${n(x)},${n(y)}`,col(i),ee*(45+v%4*12));s+=circle(x,y,ee*(42+v%3*11),col(i));}
 }else if(m==='smoke_ring_bloom'){
   for(let band=2;band>=0;band--){const ee=local(t,band*.065);for(let i=0;i<p.lobes+4;i++){const a=TAU*i/(p.lobes+4)+p.phase;const dist=ee*(160+band*34);s+=poly(scallop(cx+Math.cos(a)*dist,cy+Math.sin(a)*dist,ee*(112+v%4*16),5+v%3,.17,a),col(band));}}s+=circle(cx,cy,e*160,col(0));
 }else if(m==='smoke_puff_sweep'){
   for(let j=0;j<p.rows;j++)for(let i=0;i<p.columns;i++){const ee=local(t,(i+j)*p.stagger),x=-90+ee*920+(i-p.columns/2)*55,y=70+j*90+Math.sin(i*.8+p.phase)*28;const radius=(60+i%3*18)*Math.pow(ee,.45);s+=poly(scallop(x,y,radius,4+i%3,.21+p.bend*.1,i),col(j));}
 }else if(m==='liquid_spiky_bloom'){
   for(let i=2;i>=0;i--){const ee=local(t,i*.07);s+=poly(scallop(cx,cy,ee*(520-i*55),p.lobes+i,.2+p.bend*.35,p.phase+t*.1),col(i));}
 }else if(m==='liquid_scallop_sidewipe'){
   for(let i=p.count-1;i>=0;i--){const ee=local(t,i*.025),x=-610+ee*1300-i*32; s+=path(`M${n(x)},-100 C${n(x+500*p.bend)},40 ${n(x-130*p.bend)},320 ${n(x+180)},460 L${n(x-620)},460 L${n(x-620)},-100 Z`,col(i));}
 }else if(m==='liquid_spiral_curl'){
   for(let i=0;i<p.count;i++){const a=[];const r=e*(400+i*16),base=TAU*i/p.count+p.phase;for(let j=0;j<=50;j++){const q=j/50,th=base+q*TAU*(.65+p.bend)+t*.6;const rr=r*q;a.push(axisPoint(cx,cy,rr,th));}s+=line(`M${a.map(x=>x.map(n).join(',')).join(' L')}`,col(i),e*(42+p.lobes*8));}s+=circle(cx,cy,e*44,col(0));
 }else if(m==='staggered_strip_shutter'){
   const bw=640/p.columns;for(let i=0;i<p.columns;i++){const ee=local(t,(i%p.count)*p.stagger),yy=i%2?360-ee*440:-80;s+=rect(i*bw-2,yy,bw+4,ee*440,col(i));}
 }else if(m==='liquid_diagonal_strips'){
   const bw=900/p.count;for(let i=p.count-1;i>=0;i--){const ee=local(t,i*p.stagger),x=-700+ee*1100+(i-(p.count-1)/2)*bw*.65;const slant=110+p.bend*220;s+=poly([[x-slant,-100],[x+bw,-100],[x+bw+slant,460],[x,460]],col(i));}
 }else if(m==='square_grid_pop'){
   const w=640/p.columns,h=360/p.rows;for(let y=0;y<p.rows;y++)for(let x=0;x<p.columns;x++){const ee=local(t,((x+y)%p.count)*p.stagger),sz=ee*1.06;const rot=(1-ee)*(v%4+1)*22;s+=rect(x*w+w/2-w*sz/2,y*h+h/2-h*sz/2,w*sz,h*sz,col((x+2*y)%3),`transform="rotate(${n(rot)} ${n(x*w+w/2)} ${n(y*h+h/2)})"`);}
 }else if(m==='interlocking_triangle_teeth'){
   const bw=640/p.columns;for(let i=0;i<p.columns;i++){const ee=local(t,(i%3)*p.stagger),reach=ee*(460+v%3*40);s+=poly([[i*bw-20,-80],[(i+1)*bw+20,-80],[i*bw+bw*(.3+p.bend),reach]],col(i));s+=poly([[i*bw-20,440],[(i+1)*bw+20,440],[i*bw+bw*(.7-p.bend*.5),360-reach]],col(i+1));}
 }else if(m==='hexagon_cell_wave'){
   const r=48+v%4*5,step=r*1.7;for(let y=-1;y<p.rows+3;y++)for(let x=-1;x<p.columns+5;x++){const xx=x*step+(y%2)*step/2,yy=y*r*1.5;const ee=local(t,((x+y+p.columns)%p.count)*p.stagger);s+=poly(Array.from({length:6},(_,k)=>axisPoint(xx,yy,r*1.1*ee,k*TAU/6)),col((x+2*y+30)%3));}
 }else if(m==='rotating_shutter_blades'){
   for(let i=0;i<p.count+2;i++){const a=TAU*i/(p.count+2)+p.phase+(1-e)*.7;const off=(1-e)*380;const origin=axisPoint(cx,cy,off,a);const q=[origin,axisPoint(origin[0],origin[1],e*650,a-.28-p.bend*.2),axisPoint(origin[0],origin[1],e*650,a+.85)];s+=poly(q,col(i));}
 }else if(m==='disc_iris_pulse'){
   for(let i=p.count-1;i>=0;i--){const ee=local(t,i*p.stagger);s+=circle(cx+(i%2?1:-1)*i*7*p.aspect,cy+i*5*p.offset,ee*(475-i*23),col(i));}
 }else if(m==='radial_wedge_fan'){
   for(let i=0;i<p.lobes+2;i++){const a=TAU*i/(p.lobes+2)+p.phase,ee=local(t,i*p.stagger*.45),r=ee*720,q=[ [cx,cy],axisPoint(cx,cy,r,a),axisPoint(cx,cy,r,a+TAU/(p.lobes+2)*1.1)];s+=poly(q,col(i));}
 }else if(m==='center_split_planks'){
   const bh=360/p.rows;for(let i=0;i<p.rows;i++){const ee=local(t,(i%p.count)*p.stagger),w=ee*360;s+=rect(cx-w,i*bh,w+1,bh+2,col(i));s+=rect(cx,i*bh,w+1,bh+2,col(i+1));}
 }else if(m==='quadrilateral_flip_tiles'){
   const w=640/p.columns,h=360/p.rows;for(let y=0;y<p.rows;y++)for(let x=0;x<p.columns;x++){const ee=local(t,((x*2+y)%p.count)*p.stagger),off=(1-ee)*h*p.bend,xx=x*w,yy=y*h,sw=w*ee;s+=poly([[xx+w/2-sw/2,yy-off],[xx+w/2+sw/2,yy+off],[xx+w/2+sw/2,yy+h-off],[xx+w/2-sw/2,yy+h+off]],col(x+y));}
 }else if(m==='broken_angle_sweep'){
   for(let i=p.count-1;i>=0;i--){const ee=local(t,i*p.stagger),x=-760+ee*1600-i*35;const d=80+p.bend*200;s+=poly([[x-800,-100],[x,-100],[x+d,75],[x-d/2,190],[x+d,300],[x,460],[x-800,460]],col(i));}
 }else if(m==='flying_sine_line_train'){
   for(let i=0;i<p.count;i++){const ee=local(t,i*.06),x=-190+ee*1000,len=380+v%5*40,a=[];for(let j=0;j<=40;j++){const xx=x-len+j/40*len,yy=cy+(i-(p.count-1)/2)*(22+v%3*10)+Math.sin(j/40*TAU*(1+v%3)+p.phase+i*.3)*(20+p.bend*50);a.push([xx,yy]);}s+=line(`M${a.map(q=>q.map(n).join(',')).join(' L')}`,col(i),e*(8+p.lobes));}
 }else if(m==='elastic_s_ribbon'){
   for(let i=p.count-1;i>=0;i--){const ee=local(t,i*.045),x=-700+ee*1450-i*27;s+=path(`M${n(x)},-100 C${n(x+640*p.bend)},30 ${n(x-540*p.bend)},300 ${n(x+210)},460 L${n(x-95)},460 C${n(x-520*p.bend)},300 ${n(x+440*p.bend)},20 ${n(x-230)},-100 Z`,col(i));}
 }else if(m==='liquid_petal_burst'){
   s+=circle(cx,cy,e*160,col(0));for(let i=0;i<p.lobes+3;i++){const a=TAU*i/(p.lobes+3)+p.phase,ee=local(t,i*.018),dist=ee*(310+v%4*30),point=axisPoint(cx,cy,dist,a),r=ee*(45+v%3*11),base=axisPoint(cx,cy,dist-r*1.8,a),left=axisPoint(point[0],point[1],r,a+Math.PI/2),right=axisPoint(point[0],point[1],r,a-Math.PI/2);s+=path(`M${n(base[0])},${n(base[1])} Q${n(left[0])},${n(left[1])} ${n(point[0]+Math.cos(a)*r)},${n(point[1]+Math.sin(a)*r)} Q${n(right[0])},${n(right[1])} ${n(base[0])},${n(base[1])}Z`,col(i));}
 }else if(m==='zigzag_stroke_growth'){
   for(let i=0;i<p.count;i++){const ee=local(t,i*.04),a=[];for(let j=0;j<=p.columns+2;j++){const x=-100+j*840/(p.columns+2),yy=cy+(j%2?1:-1)*(40+p.bend*160)+(i-(p.count-1)/2)*30;a.push([x,yy]);}const plen=1300;s+=line(`M${a.map(q=>q.map(n).join(',')).join(' L')}`,col(i),e*(20+v%3*10),`stroke-dasharray="${n(plen*ee)} ${plen}"`);}
 }else if(m==='opposing_cloud_banks'){
   for(let side=0;side<2;side++)for(let layer=2;layer>=0;layer--)for(let i=0;i<p.columns;i++){const ee=local(t,layer*.05+(i%3)*p.stagger),x=i*640/(p.columns-1),r=90+v%4*15,yy=side?440-ee*(280+layer*20):-80+ee*(280+layer*20);s+=poly(scallop(x,yy,r*ee,4+i%4,.2+p.bend*.1,p.phase+i),col(layer+side));}
 }
 }
 const bg=transparent?'':rect(0,0,W,H,'#071725');
 return `<svg xmlns="http://www.w3.org/2000/svg" width="${n(width)}" height="${n(height)}" viewBox="0 0 640 360" preserveAspectRatio="xMidYMid meet" role="img" aria-label="${esc(rr.title)}">${bg}${s}</svg>`;
}
