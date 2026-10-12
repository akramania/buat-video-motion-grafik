const fs = require('fs');
const path = require('path');
process.env.XDG_CACHE_HOME ||= path.join(require('os').tmpdir(),'codex-vector-small-steps-cache');
fs.mkdirSync(process.env.XDG_CACHE_HOME,{recursive:true});
const sharp = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES
 ? require(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES, 'sharp')) : require('sharp');
sharp.concurrency(1);
const TAU=Math.PI*2;
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const mix=(a,b,p)=>a+(b-a)*p;
const smooth=v=>{v=clamp(v);return v*v*(3-2*v)};
const ease=v=>1-(1-clamp(v))**3;
const prog=(t,a,b)=>clamp((t-a)/(b-a));
const f=v=>Number(v.toFixed(3));
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const P={ink:'#285256',cream:'#F2EADA',cream2:'#E2D7BF',teal:'#467A78',dark:'#254F56',sage:'#9DB598',ochre:'#DDBF83',orange:'#D58C68',skin:'#C98B62',skinLight:'#E3AD82',pants:'#776C52',night:'#19353F',navy:'#2B424C'};
const g=(s,tr='',opacity=1)=>`<g${tr?` transform="${tr}"`:''}${opacity<1?` opacity="${f(clamp(opacity))}"`:''}>${s}</g>`;
const rect=(x,y,w,h,col,rx=0,attrs='')=>`<rect x="${f(x)}" y="${f(y)}" width="${f(Math.max(0,w))}" height="${f(Math.max(0,h))}" rx="${rx}" fill="${col}" ${attrs}/>`;
const ell=(x,y,rx,ry,col,attrs='')=>`<ellipse cx="${f(x)}" cy="${f(y)}" rx="${f(rx)}" ry="${f(ry)}" fill="${col}" ${attrs}/>`;
const circle=(x,y,r,col,attrs='')=>ell(x,y,r,r,col,attrs);
const line=(x,y,x2,y2,col,w=2,attrs='')=>`<path d="M ${f(x)} ${f(y)} L ${f(x2)} ${f(y2)}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" ${attrs}/>`;
const shape=(d,col,stroke='',w=2,attrs='')=>`<path d="${d}" fill="${col}"${stroke?` stroke="${stroke}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`:''} ${attrs}/>`;
const txt=(s,x,y,size,col,attrs='')=>`<text x="${x}" y="${y}" font-family="DejaVu Sans" font-size="${size}" fill="${col}" ${attrs}>${esc(s)}</text>`;
const defs=`<defs>
 <linearGradient id="day" x2="0" y2="1"><stop stop-color="#AFCDC3"/><stop offset=".65" stop-color="#F1E9D5"/><stop offset="1" stop-color="#EDDDBF"/></linearGradient>
 <linearGradient id="dawn" x2="0" y2="1"><stop stop-color="#718F9B"/><stop offset=".48" stop-color="#DDBEB0"/><stop offset="1" stop-color="#F5DEAC"/></linearGradient>
 <linearGradient id="night" x2="0" y2="1"><stop stop-color="#142C38"/><stop offset="1" stop-color="#355961"/></linearGradient>
 <linearGradient id="wall" x2="1" y2="1"><stop stop-color="#F7EDDB"/><stop offset="1" stop-color="#D5DCC8"/></linearGradient>
 <linearGradient id="bedwall" x2="1" y2="1"><stop stop-color="#274951"/><stop offset="1" stop-color="#18323D"/></linearGradient>
 <linearGradient id="shirt" x2="1" y2="1"><stop stop-color="#65938B"/><stop offset="1" stop-color="#3E706E"/></linearGradient>
 <linearGradient id="glass" x2="0" y2="1"><stop stop-color="#CEE7E0"/><stop offset="1" stop-color="#8FB4AC"/></linearGradient>
 <radialGradient id="sun"><stop stop-color="#F9E3AE" stop-opacity=".55"/><stop offset="1" stop-color="#F9E3AE" stop-opacity="0"/></radialGradient>
 <radialGradient id="warm"><stop stop-color="#FFCF83" stop-opacity=".38"/><stop offset="1" stop-color="#FFCF83" stop-opacity="0"/></radialGradient>
 <linearGradient id="water" x2="0" y2="1"><stop stop-color="#B2DDD4"/><stop offset="1" stop-color="#619D9B"/></linearGradient>
 <linearGradient id="shoe" x2="0" y2="1"><stop stop-color="#53666A"/><stop offset="1" stop-color="#354C54"/></linearGradient>
 <linearGradient id="fire" x2="0" y2="1"><stop stop-color="#FFE7A0"/><stop offset=".55" stop-color="#F8B567"/><stop offset="1" stop-color="#C77652"/></linearGradient>
 </defs>`;

function leaf(x,y,a,size,col){return g(shape(`M 0 0 C ${size*.9} ${-size*.4}, ${size} ${-size*1.3}, 0 ${-size*1.5} C ${-size*.65} ${-size}, ${-size*.6} ${-size*.3}, 0 0`,col),`translate(${f(x)} ${f(y)}) rotate(${f(a)})`)}
function plant(x,y,s,t,pot=P.orange){
 let z=ell(0,4,32,8,'#53665B','opacity=".18"')+shape('M -27 -36 L 27 -36 L 20 2 Q 0 15 -20 2 Z',pot)+rect(-30,-40,60,12,pot,5);
 for(let i=0;i<7;i++){let a=(i-3)*18+Math.sin(t*.75+i)*2.5;z+=line(0,-38,Math.sin(a*Math.PI/180)*54,-120+Math.abs(i-3)*10,P.teal,3)+leaf(Math.sin(a*Math.PI/180)*47,-92+Math.abs(i-3)*8,a+20,30,i%2?P.sage:P.teal)}
 return g(z,`translate(${x} ${y}) scale(${s})`);
}
function tree(x,y,s,t,col='#5F8B7C'){
 let sw=Math.sin(t*.38+x*.01)*1.1;
 return g(shape('M -12 8 L -8 -124 Q 0 -142 8 -125 L 15 8 Z','#777C63')+g(ell(0,-138,56,73,col)+ell(-32,-126,39,49,col)+ell(33,-153,36,54,col)+shape('M -29 -169 Q -3 -209 31 -172 Q 6 -184 -29 -169','#BDCEAB','',0,'opacity=".35"'),`rotate(${f(sw)} 0 0)`),`translate(${f(x)} ${f(y)}) scale(${s})`)
}
function clouds(t,night=false){
 let s='';for(let i=0;i<4;i++){let x=(i*370+t*4)%1660-170,y=100+(i%2)*68; s+=g(ell(x,y,80,19,'#FFFFFF')+ell(x-29,y-15,38,22,'#FFFFFF')+ell(x+21,y-12,49,24,'#FFFFFF'),'',night?.035:.22)}return s;
}
function cameraPan(t){return Math.sin(t*.16)*13;}
function layerPan(t,depth=1){return `translate(${f(-cameraPan(t)*depth)} 0)`;}
function hills(t,mode='day',moving=false,distance=null){
 const isDawn=mode==='dawn',world=distance===null?(moving?walkState(t).rootDistance:cameraPan(t)):distance;
 let s=rect(0,0,1280,720,`url(#${mode})`);
 s+=g(circle(isDawn?870:1050,isDawn?255:136,isDawn?270:220,'url(#sun)')+circle(isDawn?870:1050,isDawn?255:136,isDawn?60:39,'#F6D899','opacity=".9"'),`translate(${f(-world*.012)} 0)`);
 s+=g(clouds(t),`translate(${f(-world*.025)} 0)`);
 s+=g(shape('M -400 442 C -70 290 176 343 352 407 C 545 257 681 307 820 400 C 1000 229 1340 321 1800 454 L 1800 720 L -400 720Z','#A3BCAE'),`translate(${f(-world*.075)} 0)`);
 s+=g(shape('M -400 502 C -40 361 191 415 410 492 C 651 347 867 399 1030 462 C 1183 381 1430 435 1850 510 L 1850 720 L -400 720 Z','#80A492'),`translate(${f(-world*.18)} 0)`);
 s+=g(shape('M -400 550 Q 70 484 505 547 T 1030 548 Q 1420 506 1800 572 L 1800 720 L -400 720 Z','#719583'),`translate(${f(-world*.31)} 0)`);
 return s;
}
function outdoors(t,mode='day',moving=false){
 const world=moving?walkState(t).rootDistance:cameraPan(t);
 let s=hills(t,mode,moving,world);
 const treeDist=world*.67;
 for(let i=-1;i<6;i++){let idx=Math.floor((treeDist-140)/314)+i,screen=idx*314-treeDist;s+=tree(screen,545,.65+((idx%2+2)%2)*.12,t,idx%2?'#597F70':'#648D7C')}
 s+=shape('M -400 558 Q 630 529 1700 558 L 1700 720 L -400 720 Z','#BAAE91')+rect(0,584,1280,136,'#D6C7AA');
 for(let i=-1;i<9;i++){let idx=Math.floor(world/230)+i,x=idx*230-world;s+=line(x,605,x+96,605,'#F2E6CD',4,'opacity=".8"')}
 for(let i=-1;i<9;i++){let idx=Math.floor(world*.82/204)+i,x=idx*204-world*.82+34;s+=shape(`M ${f(x)} 575 l 4 -13 l 4 13 l 5 -8 l 3 10`,'none','#557B68',2);}
 return s;
}
function room(t,dark=false){
 let s=rect(0,0,1280,720,`url(#${dark?'bedwall':'wall'})`)+rect(0,512,1280,208,dark?'#44605D':'#BFB798')+line(0,512,1280,512,dark?'#5E7770':'#B5B197',5);
 let floor='';for(let i=-1;i<7;i++)floor+=line(i*330-230,720,i*190+30,513,dark?'#3A5351':'#AAA88C',1.5,'opacity=".5"');s+=g(floor,layerPan(t,.9));
 let window=rect(808,70,267,300,dark?'#BDAB7D':'#C3B395',12)+rect(823,83,237,268,dark?'url(#night)':'url(#day)',7);
 if(dark){window+=circle(1006,144,34,'#EEE2BB')+circle(1021,130,31,'#294652');for(let i=0;i<8;i++)window+=circle(843+(i*27)%209,104+(i*43)%200,1.5,'#D5DDCC')}
 else{window+=`<svg x="823" y="83" width="237" height="268" viewBox="823 83 237 268" overflow="hidden">`+g(shape('M 750 268 Q 918 204 1140 272 L 1140 380 L 750 380 Z','#9DB49E')+clouds(t),layerPan(t,.12))+`</svg>`;}
 window+=line(940,83,940,351,dark?'#B9A579':'#C3B395',10)+line(823,220,1060,220,dark?'#B9A579':'#C3B395',9);s+=g(window,layerPan(t,.28));
 let sw=Math.sin(t*.44)*2;
 let curtains=shape(`M 785 68 Q 796 183 ${800+sw} 249 Q 805 301 790 373 L 836 377 Q 825 278 844 70 Z`,dark?'#4F7774':'#91B2A1')+shape(`M 1068 70 Q ${1043-sw} 246 1052 376 L 1105 373 Q 1090 223 1114 68 Z`,dark?'#4F7774':'#91B2A1')+line(773,63,1120,63,dark?'#AD9670':'#A89B7A',7);s+=g(curtains,layerPan(t,.46));
 s+=g(plant(1186,590,1.05,t,dark?'#987557':P.orange),layerPan(t,1.08));
 return s;
}
function shoe(x,y,s,angle=0,scuff=true){
 let z=ell(7,8,82,11,'#263D40','opacity=".12"')+shape('M -63 -3 L -59 -37 Q -38 -39 -16 -23 Q -4 -16 15 -13 C 33 -12 55 -15 76 -2 Q 89 5 79 16 L -63 16 Q -72 11 -63 -3Z','url(#shoe)',P.ink,2.5);
 z+=shape('M -66 8 Q 0 15 81 5 L 80 17 Q 12 27 -62 19Z','#ACB8B2',P.ink,1.7)+shape('M -53 -30 Q -30 -25 -15 -16 L -20 -8 Q -40 -22 -56 -22Z','#778787');
 for(let i=0;i<4;i++)z+=line(-29+i*11,-23+i*3,-40+i*11,-14+i*3,'#DDD4BC',3);
 z+=shape('M -52 -7 Q -21 -14 1 -4 Q 37 9 67 0','none','#778A86',2);
 if(scuff)z+=line(51,4,72,5,'#B7C1B7',2.5)+line(48,8,67,9,'#8FA49C',1.5)+line(-56,15,-45,14,'#6D807B',2);
 return g(z,`translate(${f(x)} ${f(y)}) rotate(${f(angle)}) scale(${s})`);
}
function book(x,y,s,angle=0,open=false){
 let z='';if(open){z=shape('M 0 -53 Q -59 -79 -108 -55 L -108 20 Q -51 -3 0 19 Q 56 -2 107 19 L 107 -55 Q 54 -79 0 -53 Z','#F5ECD2',P.ink,2.4)+shape('M 0 -54 L 0 17','none','#B7B595',2)+shape('M -113 -54 L -113 26 Q -54 2 0 23 Q 52 1 112 25 L 112 -53','none',P.teal,5);
 for(let i=0;i<5;i++){z+=shape(`M -91 ${-45+i*11} Q -54 ${-56+i*11} -15 ${-41+i*11}`,'none','#B7B697',1.3)+shape(`M 16 ${-41+i*11} Q 53 ${-56+i*11} 92 ${-45+i*11}`,'none','#B7B697',1.3)}
 }else{z=rect(-50,-75,100,139,'#487D70',6,'stroke="#285256" stroke-width="3"')+rect(-44,-69,85,127,'none',3,'stroke="#CABC86" stroke-width="1.5"')+rect(-49,54,97,12,'#D6CDA8',3)+shape('M 0 -41 Q 24 -20 23 0 Q 16 28 0 36 Q -21 25 -23 0 Q -23 -21 0 -41Z','none','#CEBF87',2)+line(-40,-66,-40,54,'#285256',3)}
 return g(z,`translate(${x} ${y}) rotate(${angle}) scale(${s})`);
}
function ik(a,b,l1,l2,bend=-1){
 let dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy);if(d>l1+l2-.01||d<Math.abs(l1-l2)+.01)throw Error('IK unreachable '+d);
 let ang=Math.atan2(dy,dx),offset=Math.acos(clamp((l1*l1+d*d-l2*l2)/(2*l1*d),-1,1));
 return [a[0]+l1*Math.cos(ang+bend*offset),a[1]+l1*Math.sin(ang+bend*offset)];
}
function limb(a,b,width,col){
 let dx=b[0]-a[0],dy=b[1]-a[1],dd=Math.hypot(dx,dy),nx=-dy/dd,ny=dx/dd,w1=width*.52,w2=width*.39;
 return shape(`M ${f(a[0]+nx*w1)} ${f(a[1]+ny*w1)} Q ${f((a[0]+b[0])/2+nx*w1)} ${f((a[1]+b[1])/2+ny*w1)} ${f(b[0]+nx*w2)} ${f(b[1]+ny*w2)} Q ${f(b[0]+dx/dd*w2)} ${f(b[1]+dy/dd*w2)} ${f(b[0]-nx*w2)} ${f(b[1]-ny*w2)} L ${f(a[0]-nx*w1)} ${f(a[1]-ny*w1)} Q ${f(a[0]-dx/dd*w1)} ${f(a[1]-dy/dd*w1)} ${f(a[0]+nx*w1)} ${f(a[1]+ny*w1)}Z`,col,P.ink,1.2);
}
function walkState(t,speed=1){
 const period=1.6/speed,ph=(t/period)%1;
 const legs=[0,.5].map((off)=>{let p=(ph+off)%1,x,y,angle;
  if(p<.62){x=mix(32,-32,p/.62);y=0;angle=mix(-2,7,smooth(prog(p,.48,.62)))}
  else{let q=(p-.62)/.38,m=-64*.38/.62;
   x=(2*q*q*q-3*q*q+1)*-32+(q*q*q-2*q*q+q)*m+(-2*q*q*q+3*q*q)*32+(q*q*q-q*q)*m;
   y=-(Math.sin(Math.PI*q)**2)*25;angle=mix(7,-2,smooth(q))-18*Math.sin(Math.PI*q)**2;}
  return {p,foot:[x,0+y],angle};
 });return {legs,bodyY:4*Math.sin(ph*TAU*2)**2,phase:ph,rootDistance:t*(64/(.62*period))};
}
function bareFoot(x,y,s=1,angle=0){
 const z=shape('M -12 -9 Q -9 -16 -1 -14 L 4 -5 Q 11 -2 18 -1 Q 24 0 24 4 Q 22 7 15 7 L -10 7 Q -15 6 -12 -9 Z',P.skinLight,P.ink,1.15)+line(15,3,21,3,P.skin,1);
 return g(z,`translate(${f(x)} ${f(y)}) rotate(${f(angle)}) scale(${s})`);
}
function actorState(t,pose='stand',opts={}){
 const walking=pose==='walk'||pose==='run',gait=walkState(t,pose==='run'?1.7:1);
 const by=walking?gait.bodyY*.58:Math.sin(t*1.45)*.45;
 const seated=pose==='sit'||pose==='read';
 const hip=[0,seated?-119:(walking?-144:-148)+by];
 const torsoY=seated?23+by:by;
 const lean=pose==='tired'?6.5:pose==='read'?4:walking?2+Math.sin(gait.phase*TAU)*.65:pose==='dua'?-1:0;
 const feet=walking?gait.legs.map(l=>l.foot):seated?[[-5,0],[70,-10]]:[[-17,0],[22,0]];
 return {walking,gait,by,seated,hip,torsoY,lean,feet,barefoot:opts.barefoot||pose==='salah'||pose==='dua'};
}
function actor(x,y,s,t,pose='stand',opts={}){
 const st=actorState(t,pose,opts),{walking,gait,hip,torsoY,lean,feet,barefoot}=st;
 let z=ell(12,8,48,8,'#2C4443','opacity=".14"');
 function leg(i){let a=[hip[0]+(i===0?-11:9),hip[1]],b=[feet[i][0],feet[i][1]-6],mid=ik(a,b,73,72,-1),col=i===0?'#665E4D':P.pants;
  let trouser=limb(a,mid,26,col)+limb(mid,b,23,col);let foot=barefoot?bareFoot(b[0]+5,b[1]+2,.95,walking?gait.legs[i].angle:0):shoe(b[0]+9,b[1]+4,.28,walking?gait.legs[i].angle:0,false);return trouser+foot;}
 z+=leg(0)+leg(1);
 // One upper-body parent: every shoulder, neck and head shares the pelvis transform.
 const shoulder=[1,-240],neckPivot=[8,-265];
 function arm(target,front){let sh=[shoulder[0]+(front?12:-11),shoulder[1]+3],mid=ik(sh,target,48,49,(front||pose==='dua'||pose==='salah'||pose==='read')?1:-1);
  let hand=ell(target[0]+1,target[1]+1,8,11,P.skinLight,'stroke="#285256" stroke-width="1.2"');
  if(pose==='dua')hand=g(shape('M -9 4 Q -6 -3 1 -5 L 12 -6 Q 19 -4 16 1 L 7 6 Q -4 10 -9 4Z',P.skinLight,P.ink,1.2)+line(6,-2,14,-3,P.skin,1)+line(6,1,14,0,P.skin,1),`translate(${target[0]} ${target[1]})`);
  return limb(sh,mid,24,front?P.teal:'#3F6968')+limb(mid,target,18,front?P.teal:'#3F6968')+hand;}
 let back=[-29,-145],front=[26,-143];
 if(walking){back=[-20+Math.sin(gait.phase*TAU)*22,-151];front=[18-Math.sin(gait.phase*TAU)*22,-150]}
 if(pose==='dua'){back=[36,-202];front=[49,-198]}
 if(pose==='read'){back=[38,-167];front=[54,-163]}
 if(pose==='salah'){back=[22,-177];front=[32,-174]}
 if(pose==='tired')front=[34,-258];
 if(pose==='wave')front=[55,-249+Math.sin(t*2.2)*3.5];
 let upper=arm(back,false);
 // The skin neck extends underneath the collar; head pivots inside that overlap.
 upper+=shape('M -8 -281 Q 4 -282 16 -275 L 16 -229 Q 5 -224 -11 -231Z',P.skin,P.ink,1.1);
 upper+=shape('M -20 -248 Q -8 -256 0 -253 Q 12 -257 26 -247 Q 38 -218 34 -151 L 27 -126 Q 0 -117 -24 -128 L -29 -161 Q -34 -215 -20 -238Z','url(#shirt)',P.ink,2)+shape('M -13 -247 L 4 -238 L 20 -249','none','#A8C0AA',2)+line(6,-237,10,-132,'#2A595E',1.7)+rect(14,-213,14,17,'none',2,'stroke="#91B4A5" stroke-width="1.3"')+circle(9,-192,1.6,'#C3CBB1')+circle(9,-163,1.6,'#C3CBB1')+line(-20,-142,29,-139,'#2A595E',1.5);
 upper+=arm(front,true);
 if(pose==='read'&&!opts.noBook)upper+=book(49,-174,.30,-8,true);
 const headRot=pose==='tired'?9:pose==='read'?7:pose==='dua'?-3:pose==='salah'?7:walking?1:0;
 let face=shape('M -17 -306 Q -5 -332 19 -319 Q 31 -312 30 -298 L 37 -287 Q 41 -284 33 -280 L 30 -265 Q 17 -255 0 -262 Q -16 -270 -17 -290Z',P.skinLight,P.ink,1.7)+shape('M -17 -304 Q -21 -326 -2 -332 Q 19 -337 29 -318 L 29 -304 Q 14 -307 10 -318 Q -4 -307 -12 -299Z','#344D50')+ell(-12,-291,8,10,P.skinLight,'stroke="#285256" stroke-width="1.3"')+shape('M -14 -295 Q -5 -298 -8 -287','none',P.skin,1.4);
 let blink=pose==='salah'||((t+(opts.blinkOffset||0))%4.9)>4.72;
 if(blink)face+=line(21,-298,27,-298,P.ink,1.6);else face+=ell(24,-297,2.2,2.7,P.ink)+line(20,-306,28,-305,P.ink,1.8);
 face+=shape(pose==='tired'?'M 18 -273 Q 24 -277 29 -273':pose==='wave'?'M 16 -277 Q 23 -272 30 -278':'M 20 -274 Q 25 -272 29 -275','none',P.ink,1.4)+shape('M 1 -270 Q 7 -263 15 -262','none','#A77354',1.6);
 upper+=g(face,`rotate(${headRot} ${neckPivot[0]} ${neckPivot[1]}) translate(${neckPivot[0]} ${neckPivot[1]}) scale(.94) translate(${-neckPivot[0]} ${-neckPivot[1]})`);
 z+=g(upper,`translate(0 ${f(torsoY)}) rotate(${f(lean)} 0 -133)`);
 return g(z,`translate(${f(x)} ${f(y)}) scale(${s})`);
}
function lantern(x,y,s,t,on=true){
 let z=on?circle(0,0,150,'url(#warm)'):'';
 z+=shape('M -24 -34 L 24 -34 L 35 24 L -35 24Z','#254B4D',P.ink,2)+rect(-18,-30,36,48,on?'#EFCA86':'#687F70',3)+line(-10,-30,-10,18,'#4D6B5E',3)+line(10,-30,10,18,'#4D6B5E',3)+rect(-40,21,80,10,'#355654',5)+rect(-29,-41,58,9,'#355654',4)+shape('M -14 -41 Q -14 -65 0 -65 Q 14 -65 14 -41','none',P.ink,4);
 if(on)z+=shape(`M -6 10 Q -14 -2 ${Math.sin(t*3)*3} -16 Q 10 -3 6 10 Z`,'#FFF0B1');
 return g(z,`translate(${x} ${y}) scale(${s})`);
}
function shoeScene(t,d){
 let s=room(t),fg=rect(603,417,505,22,'#938667',6)+rect(620,437,18,164,'#918264',4)+rect(1068,437,19,164,'#918264',4)+rect(603,541,505,18,'#A09170',5)+rect(614,562,478,24,'#B4A17B',4);
 fg+=shoe(755,404,1.15,-6)+shoe(925,409,1.10,2)+shoe(741,529,.76,-3,false);
 fg+=rect(65,402,277,17,'#B4A17B',5)+rect(83,419,14,142,'#A59672')+rect(305,419,15,142,'#A59672')+plant(177,392,.62,t);
 s+=g(fg,layerPan(t,.76));
 for(let i=0;i<6;i++)s+=circle(730+Math.sin(t*.23+i)*130,170+(i*83+t*3)%270,1.5,'#F6EFDC','opacity=".55"');
 const vis=1-smooth(prog(t,2.2,3.2));s+=g(txt('Seni Langkah Kecil',95,127,46,P.ink,'font-weight="bold"'),'',vis);
 return s;
}
function walkScene(t,d){
 let s=outdoors(t,'day',true),travel=walkState(t).rootDistance;
 s+=ell(830-travel,582,86,10,'#86A9A1','opacity=".6"')+ell(828-travel,581,50,3,'#CFDDD0','opacity=".55"');
 s+=actor(924,600,1.0,t,'walk');
 for(let i=0;i<3;i++)s+=g(shape('M -14 0 Q 0 7 14 0','none','#4C756F',2),`translate(${700-i*22} ${170+Math.sin(t*.5+i)*8})`);
 return s;
}
function ambition(t,d){
 let s=room(t),fg=actor(961,600,1.04,t,'stand');
 // The Quran rests on a raised study table, never on the floor.
 fg+=rect(64,455,274,18,'#A39472',5)+rect(81,473,16,121,'#8F8465',4)+rect(303,473,16,121,'#8F8465',4)+line(92,548,309,548,'#A39472',7)+book(133,413,.6,-7)+lantern(239,436,.55,t,true);
 s+=g(fg,layerPan(t,.76));
 const icons=[{x:848,y:199,kind:'moon'},{x:1129,y:313,kind:'book'},{x:733,y:483,kind:'calendar'}];
 for(let i=0;i<icons.length;i++){let q=ease(prog(t,.4+i*1.1,1.3+i*1.1)),o=icons[i];s+=g(ell(0,0,68,65,'#F5E9CF','stroke="#B8B89A" stroke-width="2"')+(o.kind==='moon'?circle(0,-3,30,'#D3B574')+circle(13,-15,28,'#F5E9CF'):o.kind==='book'?book(0,1,.48,0,false):rect(-37,-36,74,76,'#7F9E8B',9)+rect(-30,-22,60,55,'#F4E6C8',5)+txt('7',0,19,36,P.teal,'text-anchor="middle" font-weight="bold"')),`translate(${o.x} ${f(o.y+Math.sin(t*.9+i)*5)}) scale(${f(q)})`,q)}
 return s;
}
function matchScene(t,d){
 let s=rect(0,0,1280,720,'url(#night)')+rect(0,562,1280,158,'#52695C')+ell(914,594,205,23,'#18353C','opacity=".33"');
 let ext=smooth(prog(t,d*.54,d*.72)),fire=1-ext;
 s+=circle(930,365,220,'url(#warm)',`opacity="${fire}"`)+g(rect(-11,-8,22,211,'#C4AA7D',5)+ell(0,-10,14,20,'#5E6455'),`translate(919 370) rotate(-17)`);
 let fw=43+Math.sin(t*7)*3,dx=Math.sin(t*4.4)*5;
 s+=g(shape(`M 914 367 C 854 329 ${875+dx} 272 ${927+dx} 220 C ${919+dx} 277 ${1000+dx} 295 962 359 Q 941 383 914 367 Z`,'url(#fire)')+shape(`M 922 366 Q 885 335 930 292 Q 970 347 944 368 Z`,'#FFF3B9'),'',fire);
 for(let i=0;i<4;i++){let p=prog(t,d*.58+i*.22,d*.86+i*.22);s+=g(shape(`M 922 352 C ${913-i*6} 306 ${982+i*8} 275 ${956+i*13} 223 C 938 185 997 178 1004 145`,'none','#A9B6A6',3,'stroke-dasharray="100 210" stroke-dashoffset="'+f(-p*205)+'"'),'',Math.sin(p*Math.PI)*.34)}
 s+=shape('M 75 209 C 231 185 247 240 387 219','none','#78958F',2,'opacity=".3"')+shape('M 40 274 C 210 252 300 284 460 255','none','#78958F',2,'opacity=".25"');
 return s;
}
function tiredScene(t,d){
 let s=room(t,true),fg=rect(680,430,450,130,'#756F65',12)+rect(679,422,434,57,'#B6B89D',12)+rect(821,434,285,107,'#6A928C',12)+shape('M 811 463 Q 952 454 1105 469 L 1105 553 L 813 553 Z','#719B93')+line(1073,458,1073,550,'#97B2A0',3);
 fg+=rect(701,551,24,49,'#52655C',4)+rect(1080,551,24,49,'#52655C',4)+actor(1002,600,1.04,t,'tired');
 fg+=book(113,378,.51,-8)+rect(62,412,182,18,'#8A8C74',4)+rect(65,430,13,167,'#7A7F6B')+rect(220,430,13,167,'#7A7F6B')+rect(76,512,142,13,'#8A8C74',4)+lantern(181,397,.48,t,true);
 return s+g(fg,layerPan(t,.76));
}
function hadithScene(t,d){
 let s=rect(0,0,1280,720,'url(#wall)')+circle(962,276,270,'url(#sun)'),arch=shape('M 725 613 L 725 223 Q 725 71 945 54 Q 1172 91 1172 223 L 1172 613Z','#CAD8BD')+shape('M 763 612 L 763 222 Q 763 110 945 87 Q 1134 116 1134 222 L 1134 612Z','#E9E3CB')+shape('M 811 611 L 811 227 Q 811 148 945 122 Q 1086 148 1086 227 L 1086 611Z','url(#dawn)');
 s+=g(arch,layerPan(t,.22))+rect(0,608,1280,112,'#D1C7AC');
 let fg=plant(117,597,1.18,t)+plant(1203,597,.77,t);
 fg+=rect(806,503,291,20,'#A49370',7,'stroke="#285256" stroke-width="2"')+rect(826,523,18,79,'#92815F',4)+rect(1060,523,18,79,'#92815F',4)+line(835,570,1068,570,'#A49370',8)+book(952,476,1.02,-2,true);
 s+=g(fg,layerPan(t,.82))+txt('Sahih al-Bukhari 6464  ·  Sahih Muslim 782b',80,602,21,P.ink);
 for(let i=0;i<10;i++)s+=circle(820+(i*47)%266,193+(i*73+t*8)%230,1.5,'#F5E7BE','opacity=".6"');
 return s;
}
function prayerScene(t,d){
 let s=room(t,true),fg=shape('M 779 551 L 1076 551 L 1112 613 L 747 613 Z','#789D8B',P.ink,2)+shape('M 790 560 L 1060 560 L 1085 603 L 769 603 Z','none','#C8C392',2)+shape('M 860 591 Q 916 560 975 591','none','#C8C392',2);
 fg+=actor(934,590,.94,t,'salah',{barefoot:true})+lantern(243,545,.7,t,true);
 // Shoes stay off the mat beside the wall.
 fg+=shoe(680,586,.29,-6,false)+shoe(715,589,.28,1,false);
 return s+g(fg,layerPan(t,.76));
}
function readingScene(t,d){
 let s=room(t),fg=rect(735,461,244,89,'#87795C',15)+rect(724,540,34,65,'#776F54',5)+rect(950,539,34,66,'#776F54',5)+rect(729,427,240,45,'#C5B68C',13)+actor(858,600,1.0,t,'read',{noBook:true});
 // Quran is physically supported by this raised reading table (cover bottom y459.5, table top y460).
 fg+=rect(874,460,110,12,'#A99770',4,'stroke="#285256" stroke-width="1.5"')+rect(955,472,13,117,'#8E8062',3)+shape('M 936 588 L 984 588 L 990 600 L 929 600 Z','#9B8B67')+book(920,450,.38,0,true);
 s+=g(fg,layerPan(t,.76));
 let shelf=rect(84,191,148,273,'#A3956C',7)+rect(96,204,124,247,'#6F8C79',4);
 for(let i=0;i<4;i++)shelf+=rect(108,216+i*48,13,39,['#D4B67F','#E0D3A7','#9AAE84','#D09C77'][i],2)+rect(128,223+i*48,76,12,'#B4B48B',2);
 shelf+=rect(85,466,148,13,'#8D835F',3);
 return s+g(shelf,layerPan(t,.42));
}
function charityScene(t,d){
 let s=outdoors(t,'day',false);
 s+=shape('M 853 342 L 985 342 L 995 520 Q 918 544 842 520Z','#94AE9C',P.ink,3)+ell(918,342,66,13,'#CED8BB','stroke="#285256" stroke-width="2"')+rect(889,336,59,9,P.dark,4)+txt('SEDEKAH',918,451,19,P.ink,'text-anchor="middle" font-weight="bold"');
 let q=prog(t,.5,2.8);let y=mix(168,336,ease(q));s+=g(circle(917,y,26,P.ochre,'stroke="#9A835B" stroke-width="3"')+txt('1',917,y+9,25,'#927951','text-anchor="middle" font-weight="bold"'),'',1-prog(q,.82,1));
 s+=g(actor(1099,598,.89,t,'wave')+actor(765,598,.78,t+.5,'stand'),layerPan(t,1));
 for(let i=0;i<3;i++){let p=prog(t,2+i*.7,3.5+i*.7);s+=g(shape('M 0 8 C -17 -3 -19 -14 -11 -19 Q -2 -24 0 -15 Q 8 -26 18 -17 C 25 -8 12 6 0 17 Z',P.orange),`translate(${f(840+i*73)} ${f(289-p*45)}) scale(.5)`,Math.sin(p*Math.PI))}
 return s;
}
function waterScene(t,d){
 let s=rect(0,0,1280,720,'url(#wall)')+rect(0,557,1280,163,'#C4B993'),fg='';
 fg+=rect(939,103,129,42,'#789897',12)+shape('M 1032 104 L 1032 215 Q 1032 232 1010 232 L 945 232 L 945 257 L 909 257 L 909 218 Q 909 200 929 200 L 995 200 L 995 103 Z','#789897',P.ink,2)+rect(882,83,201,30,'#597E7C',12)+line(953,83,953,59,P.ink,9)+rect(925,41,56,17,'#597E7C',7);
 fg+=shape('M 774 385 L 1078 385 L 1045 575 Q 930 609 810 575 Z','#91B5AA',P.ink,3)+shape('M 810 567 L 785 401 L 1065 401 L 1037 567 Q 927 595 810 567Z','#B3CCC0');
 const waterY=mix(569,416,smooth(prog(t,0,d*.86)));fg+=shape(`M 807 ${f(waterY)} Q 925 ${f(waterY-8+Math.sin(t*3)*3)} 1046 ${f(waterY)} L 1034 565 Q 927 592 816 565Z`,'url(#water)')+ell(928,waterY,117,9,'#C3E1D5','opacity=".65"');
 fg+=ell(926,384,151,18,'none','stroke="#285256" stroke-width="3"')+shape('M 779 405 Q 761 224 926 224 Q 1093 224 1073 405','none','#62877E',8);
 for(let i=0;i<2;i++){let ph=(t*1.35+i*.5)%1,y=mix(276,waterY,ease(ph));fg+=g(shape('M 0 -10 C -5 -3 -10 3 -8 8 Q 0 18 8 8 C 11 3 6 -3 0 -10Z','#85BEB3'),`translate(928 ${f(y)})`,1-prog(ph,.89,1));let rip=(t*1.35+i*.5+.08)%1;fg+=ell(928,waterY+2,20+rip*80,3+rip*6,'none',`stroke="#E4F0DD" stroke-width="1.6" opacity="${f((1-rip)*.5)}"`)}
 fg+=plant(130,595,1.4,t);
 return s+g(fg,layerPan(t,.72));
}
function pathScene(t,d,mode='day'){
 const local=t*.72,travel=walkState(local).rootDistance,cam=travel*.84;
 let s=hills(local,mode,true,cam);
 const ground=shape('M -900 601 Q 350 373 2400 608 L 2400 720 L -900 720Z','#668F7A')+shape('M 580 720 Q 574 572 715 516 Q 879 471 1006 400 L 1040 401 Q 941 502 794 542 Q 722 576 760 720Z','#D1BE96');
 s+=g(ground,`translate(${f(-cam)} 0)`);
 const treeDist=cam*.67;
 for(let i=-2;i<8;i++){let idx=Math.floor(treeDist/185)+i,x=idx*185-treeDist;s+=tree(x,557+(idx%2)*18,.63+((idx%3+3)%3)*.11,t,idx%2?'#557C69':'#698D78')}
 s+=actor(842+travel-cam,600,1.0,local,'walk');
 let stones='';for(let i=-1;i<7;i++){let idx=Math.floor(cam/230)+i,x=idx*230-cam;stones+=shape(`M ${f(x)} 597 q -18 -8 -32 2 q -9 8 16 15 q 25 5 34 -2Z`,'#BDAD84');}s+=stones;
 return s;
}
function gardenScene(t,d){
 let s=outdoors(t,'day',false);s+=rect(741,476,371,23,'#A4926E',8)+rect(763,495,18,105,'#8E8165',4)+rect(1057,495,18,105,'#8E8165',4)+rect(748,366,347,93,'#B1A078',8)+line(748,404,1095,404,'#917F5D',3)+actor(1140,598,.94,t,'stand');
 let gq=smooth(prog(t,.7,d*.72));s+=plant(903,520,.44+gq*.20,t);
 for(let i=0;i<5;i++){let ph=(t*.32+i*.23)%1;s+=leaf(841+ph*141,273+Math.sin(ph*TAU)*24,ph*250,12,'#90AE8B')}
 return s;
}
function sunriseScene(t,d){return pathScene(t,d,'dawn')+g(ell(970,187,193,72,'url(#sun)'),'');}
function stepsScene(t,d){
 const local=t*.83,travel=walkState(local).rootDistance,cam=travel*.84;
 // Use the tracking camera distance consistently for both character and contact marks.
 let s=hills(local,'dawn',true,cam)+shape('M -400 558 Q 630 529 1700 558 L 1700 720 L -400 720Z','#BAAE91')+rect(0,584,1280,136,'#D6C7AA');
 let treeDist=cam*.67;for(let i=-1;i<6;i++){let idx=Math.floor((treeDist-140)/314)+i;s+=tree(idx*314-treeDist,545,.7,t,idx%2?'#597F70':'#648D7C')}
 for(let i=0;i<12;i++){let vis=smooth(prog(travel,i*32+15,i*32+30));s+=g(ell(810+i*32-cam,602+(i%2)*7,13,4,'#94886C'),`rotate(-7 ${f(810+i*32-cam)} ${602+(i%2)*7})`,vis*.38)}
 s+=actor(830+travel-cam,598,1.0,local,'walk');
 return s;
}
function duaScene(t,d){
 let s=hills(t,'dawn',false)+g(tree(107,594,1.10,t,'#628773')+tree(1229,585,1.05,t,'#658975'),layerPan(t,.7));
 let fg=shape('M 775 556 L 1115 556 L 1160 614 L 731 614Z','#A6B69A',P.ink,1.8)+shape('M 791 565 L 1096 565 L 1124 604 L 763 604Z','none','#D7CEA4',2)+actor(955,591,1.10,t,'dua',{barefoot:true});
 fg+=shoe(688,591,.29,-4,false)+shoe(725,590,.28,2,false);
 s+=g(fg,layerPan(t,.92));
 const a=smooth(prog(t,d-3.4,d-2.5));s+=g(txt('Seni Langkah Kecil',72,551,30,P.ink,'font-weight="bold"')+txt('Sedikit pun tidak mengapa.',72,588,24,P.ink),'',a);
 return s;
}
const scenes={shoes:shoeScene,walk:walkScene,ambition,match:matchScene,tired:tiredScene,hadith:hadithScene,prayer:prayerScene,reading:readingScene,charity:charityScene,water:waterScene,path:pathScene,garden:gardenScene,sunrise:sunriseScene,steps:stepsScene,dua:duaScene};
function frameSvg(name,t,dur,width=1920){let s=scenes[name](t,dur);return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${width*9/16}" viewBox="0 0 1280 720">${defs}${s}</svg>`;}
async function render(){
 const args=process.argv.slice(2);const name=args[0];const dur=Number(args[1]);const fps=Number(args[2]||60);const width=Number(args[3]||1920);
 if(args[4]){const t=Number(args[5]||0);const svg=frameSvg(name,t,dur,width);if(args[4].endsWith('.svg'))fs.writeFileSync(args[4],svg);else await sharp(Buffer.from(svg)).png().toFile(args[4]);return;}
 const n=Math.round(dur*fps);
 for(let i=0;i<n;i++){const buf=await sharp(Buffer.from(frameSvg(name,i/fps,dur,width))).flatten({background:P.cream}).removeAlpha().raw().toBuffer();if(!process.stdout.write(buf))await new Promise(resolve=>process.stdout.once('drain',resolve));}
}
function audit(){
 let maxBone=0,maxSlip=0,poseSamples=0,minNeckOverlap=Infinity;
 const poses=['walk','run','stand','tired','read','salah','dua','wave','sit'];
 for(let i=0;i<=960;i++){let t=i/600,st=actorState(t,'walk');for(let [j,leg] of st.gait.legs.entries()){let a=[j===0?-11:9,st.hip[1]],b=[leg.foot[0],leg.foot[1]-6],m=ik(a,b,73,72,-1);maxBone=Math.max(maxBone,Math.abs(Math.hypot(m[0]-a[0],m[1]-a[1])-73),Math.abs(Math.hypot(m[0]-b[0],m[1]-b[1])-72));if(leg.p<.61){let next=walkState(t+.00001);maxSlip=Math.max(maxSlip,Math.abs(next.rootDistance+next.legs[j].foot[0]-st.gait.rootDistance-leg.foot[0]));}}}
 for(let pose of poses){for(let i=0;i<=320;i++){let t=i/20;actor(0,0,1,t,pose);poseSamples++;}
  // A point lying inside the head remains inside the neck skin polygon after relative head rotation.
  const headRot=pose==='tired'?9:pose==='read'?7:pose==='dua'?-3:pose==='salah'?7:(pose==='walk'||pose==='run')?1:0,r=headRot*Math.PI/180;
  const px=8+Math.sin(r)*4.7,py=-265-Math.cos(r)*4.7;
  minNeckOverlap=Math.min(minNeckOverlap,16-px,px+9,py+280,-239-py);
 }
 let boundaryJumps=[];for(let t of [1.6*.62,1.6]){let a=walkState(t-1e-7).legs[0],b=walkState(t+1e-7).legs[0];boundaryJumps.push({time:t,position_jump:Math.hypot(a.foot[0]-b.foot[0],a.foot[1]-b.foot[1]),angle_jump:Math.abs(a.angle-b.angle)});}
 return {bone_length_error:maxBone,stance_contact_error:maxSlip,walk_period:1.6,frames_tested:961,pose_samples_without_unreachable_joint:poseSamples,head_neck_overlap_min_design_px:minNeckOverlap,collar_neck_overlap_design_px:9,prayer_and_dua_barefoot:true,reading_book_cover_bottom_y:459.5,reading_table_top_y:460,subtitle_art_clearance_y:614,parallax_depth_rates:{sun:.012,clouds:.025,distant_hills:.075,middle_hills:.18,near_hills:.31,trees:.67,ground:1},boundaryJumps};
}
if(require.main===module){if(process.argv.includes('--audit'))console.log(JSON.stringify(audit()));else render().catch(e=>{console.error(e);process.exit(1)});}
module.exports={frameSvg,walkState,actorState,actor,ik,audit,defs,palette:P,hills,outdoors,room};
