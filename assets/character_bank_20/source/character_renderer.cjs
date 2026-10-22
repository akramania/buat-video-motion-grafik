/** Original code-drawn editorial character artwork. No remote assets or bitmap tracing.
 * Static layered artwork and joint metadata: not an automatic deformation/action rig.
 */
'use strict';

const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const color=(s,f)=>/^#[0-9a-f]{6}$/i.test(s||'')?s:f;
function tint(hex,k){hex=color(hex,'#98735c');let v=hex.slice(1).match(/../g).map(x=>parseInt(x,16));return '#'+v.map(x=>Math.round(k>=0?x+(255-x)*k:x*(1+k)).toString(16).padStart(2,'0')).join('');}
function parameters(c,opts={}) {
  const age=Number(c.age)||30, child=age<13, young=age<8, teen=age>=13&&age<20, elder=age>=65;
  const sex=c.sex==='female'?'female':'male';
  const rawView=opts.view||'front';
  const view=(rawView==='side_right'||rawView==='side_left')?'side':(rawView==='three_quarter_right'||rawView==='three_quarter_left')?'three_quarter':(['front','three_quarter','side','back'].includes(rawView)?rawView:'front');
  const flipX=(rawView==='side_left'||rawView==='three_quarter_left');
  const build=c.body?.build||'average', headH=young?189:child?174:teen?145:elder?143:135;
  const headW=({oval:91,round:99,square:97,long:85,heart:94}[c.body?.head_shape]||91)*(young?1.49:child?1.44:1);
  const topY=56, faceY=topY+headH*.53, shoulderY=topY+headH+43;
  const width=({slender:90,average:105,broad:121,stocky:124}[build]||105)*(child?.88:1);
  const hem=sex==='female'?({baju_kurung:664,tunic_trousers:664,cardigan_skirt:595,dress:887}[c.style?.outfit]||664):({kurta:643,shirt:562,baju_melayu:629,polo:568,cardigan:579}[c.style?.outfit]||615);
  return {age,child,young,teen,elder,sex,view,headH,headW,topY,faceY,shoulderY,width,hem,
    skin:color(c.body?.skin,'#bb8567'),top:color(c.style?.top,'#547c81'),bottom:color(c.style?.bottom,'#334b55'),accent:color(c.style?.accent,'#b99864'),shoes:color(c.style?.shoes,'#453b38'),
    hair:color(c.head?.hair_color,'#292a2b'),hijab:color(c.head?.hijab_color,'#8b7278'),headShape:c.body?.head_shape||'oval',hairStyle:c.head?.hair||'sidepart',hijabStyle:c.head?.hijab||'none',
    glasses:c.head?.glasses||'none',facialHair:c.head?.facial_hair||'none',outfit:c.style?.outfit|| (sex==='female'?'baju_kurung':'kurta'), rawView,flipX, expression:opts.expression||'neutral',pose:opts.pose||'relaxed'};
}
function geometryCanonical(c,opts={}) {
  const p=parameters(c,opts), {shoulderY:s,width:w,view}=p;
  let L=view==='side'?{shoulder:[286,s],elbow:[280,457],wrist:[293,609],fingers:[299,651]}:{shoulder:[300-w*.79,s+8],elbow:[300-w-17,447],wrist:[300-w-8,610],fingers:[300-w-3,653]};
  let R=view==='side'?{shoulder:[310,s+2],elbow:[333,450],wrist:[342,607],fingers:[342,652]}:{shoulder:[300+w*.79,s+8],elbow:[300+w+13,443],wrist:[300+w+4,602],fingers:[300+w-3,648]};
  if(p.pose==='wave') R={shoulder:R.shoulder,elbow:[438,402],wrist:[451,265],fingers:[449,211]};
  if(view==='three_quarter'&&p.pose!=='wave'){R={shoulder:[300+w*.63,s+3],elbow:[300+w*.78,445],wrist:[300+w*.73,605],fingers:[300+w*.70,651]};}
  const hipY=568, ankleY=911;
  return {schema_version:1,id:c.id,name:c.name,view:p.view,units:'SVG user units',viewBox:[0,0,600,1000],height_cm:c.height_cm,
    rig_status:'Static layered artwork with landmarks; action deformation, IK and contacts require animation implementation.',
    bounds:{top:p.topY,bottom:947,left:Math.min(L.fingers[0]-25,300-w-31),right:Math.max(R.fingers[0]+25,300+w+31)},
    landmarks:{head:[300,p.faceY],neck:[300,s-17],shoulder_left:L.shoulder,elbow_left:L.elbow,wrist_left:L.wrist,fingers_left:L.fingers,shoulder_right:R.shoulder,elbow_right:R.elbow,wrist_right:R.wrist,fingers_right:R.fingers,pelvis:[300,hipY],hip_left:[269,hipY],hip_right:[333,hipY],knee_left:[265,752],knee_right:[338,755],ankle_left:[259,ankleY],ankle_right:[340,ankleY],heel_left:[241,936],toe_left:[279,940],heel_right:[328,937],toe_right:[377,940]},
    segments:{upper_arm_left:Math.hypot(L.elbow[0]-L.shoulder[0],L.elbow[1]-L.shoulder[1]),forearm_left:Math.hypot(L.wrist[0]-L.elbow[0],L.wrist[1]-L.elbow[1]),upper_arm_right:Math.hypot(R.elbow[0]-R.shoulder[0],R.elbow[1]-R.shoulder[1]),forearm_right:Math.hypot(R.wrist[0]-R.elbow[0],R.wrist[1]-R.elbow[1]),head_height:p.headH},
    garments:{outfit:p.outfit,shoulder_y:s,hem_y:p.hem,ankle_y:ankleY},
    layers:['shadow','leg_left','leg_right','shoe_left','shoe_right','arm_left_upper','arm_left_lower','hand_left','torso','arm_right_upper','arm_right_lower','hand_right','neck','hair_back','head','ears','eyes','brows','nose','mouth','hair_front','hijab_back','hijab_front','accessories']};
}
function geometry(c,opts={}) {
  const g=geometryCanonical(c,opts),raw=opts.view||'front';
  if(raw==='side_left'||raw==='three_quarter_left'){
    g.landmarks=Object.fromEntries(Object.entries(g.landmarks).map(([k,p])=>[k,[600-p[0],p[1]]]));
    const l=g.bounds.left;g.bounds.left=600-g.bounds.right;g.bounds.right=600-l;
  }
  g.view=raw;return g;
}
function characterSvg(c,opts={}) {
  const p=parameters(c,opts), g=geometryCanonical(c,{...opts,view:p.view}), id=String(c.id||'character').replace(/[^a-zA-Z0-9_-]/g,'_')+'_'+p.view;
  const gid=(name,body,attr='')=>`<g id="${id}_${name}" ${attr}>${body}</g>`;
  const path=(d,fill,stroke='none',sw=1,attrs='')=>`<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round" ${attrs}/>`;
  const ellipse=(x,y,rx,ry,fill,attrs='')=>`<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${fill}" ${attrs}/>`;
  const line=(d,stroke,sw=2,attrs='')=>path(d,'none',stroke,sw,attrs);
  const grad=n=>`url(#${id}_${n})`;
  const ink=tint(p.skin,-.47),clothInk=tint(p.top,-.32), hairLight=tint(p.hair,.19);
  const defs=`<defs>
    <linearGradient id="${id}_skin" x1="0" y1="0" x2="1" y2=".3"><stop stop-color="${tint(p.skin,.16)}"/><stop offset=".55" stop-color="${p.skin}"/><stop offset="1" stop-color="${tint(p.skin,-.10)}"/></linearGradient>
    <linearGradient id="${id}_cloth" x1="0" y1="0" x2="1" y2=".3"><stop stop-color="${tint(p.top,.12)}"/><stop offset=".56" stop-color="${p.top}"/><stop offset="1" stop-color="${tint(p.top,-.13)}"/></linearGradient>
    <linearGradient id="${id}_trouser" x1="0" x2="1"><stop stop-color="${tint(p.bottom,.13)}"/><stop offset="1" stop-color="${tint(p.bottom,-.08)}"/></linearGradient>
    <linearGradient id="${id}_hair" x1="0" x2="1"><stop stop-color="${hairLight}"/><stop offset=".6" stop-color="${p.hair}"/><stop offset="1" stop-color="${tint(p.hair,-.2)}"/></linearGradient>
    <linearGradient id="${id}_scarf" x1="0" x2="1"><stop stop-color="${tint(p.hijab,.17)}"/><stop offset=".5" stop-color="${p.hijab}"/><stop offset="1" stop-color="${tint(p.hijab,-.12)}"/></linearGradient>
  </defs>`;
  let parts=[];
  if(opts.transparent===false)parts.push(`<rect width="600" height="1000" fill="#f5f0e7"/>`);
  parts.push(gid('shadow',ellipse(308,949,p.view==='side'?77:112,10,'#1e2728','opacity=".09"')));
  const s=p.shoulderY,w=p.width,h=p.headH,fx=300,fy=p.faceY,rx=p.headW/2,ry=h/2;
  const slim=p.view==='side'?.62:p.view==='three_quarter'?.84:1,tw=w*slim;
  const skirt=p.sex==='female'&&p.outfit!=='tunic_trousers';
  const shoes = p.view==='side' ? [{x:280,y:915,r:false},{x:314,y:916,r:true}]:[{x:258,y:915,r:false},{x:341,y:916,r:true}];
  if(skirt){
    parts.push(gid('leg_left',path(`M ${300-tw*.72} 522 Q 300 506 ${300+tw*.71} 528 L ${300+tw*.94} 915 Q 305 935 ${300-tw*.94} 916 Z`,grad('trouser'),tint(p.bottom,-.28),1.8)+line(`M 275 649 Q 259 794 270 915 M 316 641 Q 326 793 322 919 M ${300+tw*.55} 670 L ${300+tw*.73} 914`,tint(p.bottom,.20),2.3,'opacity=".65"')));
    parts.push(gid('leg_right',''));
  }else{
    const lx=p.view==='side'?281:258,rr=p.view==='side'?316:341;
    parts.push(gid('leg_left',path(`M ${300-tw*.68} 507 Q ${300-tw*.85} 672 ${lx-24} 795 L ${lx-22} 918 Q ${lx} 925 ${lx+23} 917 L ${lx+27} 774 Q 292 657 303 544 Z`,grad('trouser'),tint(p.bottom,-.28),1.8)+line(`M ${lx+3} 604 Q ${lx-6} 762 ${lx+3} 898`,tint(p.bottom,.20),2,'opacity=".7"')));
    parts.push(gid('leg_right',path(`M 297 525 Q ${300+tw*.35} 503 ${300+tw*.67} 518 Q ${rr+22} 678 ${rr+24} 790 L ${rr+20} 921 Q ${rr} 927 ${rr-23} 919 L ${rr-24} 794 Q 315 659 297 525 Z`,grad('trouser'),tint(p.bottom,-.28),1.8)+line(`M ${rr-4} 600 Q ${rr+7} 766 ${rr-1} 899`,tint(p.bottom,.20),2,'opacity=".7"')));
  }
  shoes.forEach((sh,i)=>{let x=sh.x,y=sh.y;parts.push(gid('shoe_'+(i?'right':'left'),path(`M ${x-22} ${y} Q ${x} ${y+5} ${x+21} ${y} L ${x+25} ${y+12} Q ${x+47} ${y+14} ${x+49} ${y+26} Q ${x+15} ${y+34} ${x-25} ${y+27} L ${x-25} ${y+12} Z`,p.shoes,tint(p.shoes,-.25),1.7)+line(`M ${x-22} ${y+25} Q ${x+17} ${y+30} ${x+45} ${y+25}`,tint(p.shoes,.32),2)+line(`M ${x+8} ${y+10} l 13 5 M ${x+4} ${y+15} l 13 5`,tint(p.shoes,.28),1.5)));});
  // Arms are separate upper/lower groups and the seam is covered by the elbow overlap.
  function arm(side){const a=side==='left'?{S:g.landmarks.shoulder_left,E:g.landmarks.elbow_left,W:g.landmarks.wrist_left}:{S:g.landmarks.shoulder_right,E:g.landmarks.elbow_right,W:g.landmarks.wrist_right};let {S,E,W}=a;
    const seg=(A,B,wa,wb)=>{const dx=B[0]-A[0],dy=B[1]-A[1],len=Math.hypot(dx,dy),nx=-dy/len,ny=dx/len;return `M ${A[0]+nx*wa} ${A[1]+ny*wa} Q ${(A[0]+B[0])/2+nx*(wa+wb)*.58} ${(A[1]+B[1])/2+ny*(wa+wb)*.58} ${B[0]+nx*wb} ${B[1]+ny*wb} Q ${B[0]+dx/len*11} ${B[1]+dy/len*11} ${B[0]-nx*wb} ${B[1]-ny*wb} L ${A[0]-nx*wa} ${A[1]-ny*wa} Q ${A[0]-dx/len*wa*.85} ${A[1]-dy/len*wa*.85} ${A[0]+nx*wa} ${A[1]+ny*wa} Z`;};
    const far=p.view==='three_quarter'&&side==='right';
    let b=gid('arm_'+side+'_upper',path(seg(S,E,far?24:29,far?22:25),grad('cloth'),clothInk,1.8));
    b+=gid('arm_'+side+'_lower',path(seg(E,W,far?22:25,far?16:18),grad('cloth'),clothInk,1.8)+line(`M ${E[0]-13} ${E[1]+(p.pose==='wave'&&side==='right'?-9:13)} Q ${E[0]+2} ${E[1]+(p.pose==='wave'&&side==='right'?-1:21)} ${E[0]+13} ${E[1]+(p.pose==='wave'&&side==='right'?-9:13)}`,tint(p.top,-.20),1.8)+line(`M ${W[0]-16} ${W[1]-5} L ${W[0]+16} ${W[1]-5}`,tint(p.top,-.25),2));
    const wave=side==='right'&&p.pose==='wave', x=W[0],y=W[1];
    let d=wave?`M ${x-14} ${y+3} L ${x-17} ${y-28} Q ${x-30} ${y-42} ${x-25} ${y-47} Q ${x-21} ${y-51} ${x-11} ${y-38} L ${x-12} ${y-68} Q ${x-11} ${y-76} ${x-7} ${y-72} L ${x-3} ${y-46} L ${x-2} ${y-79} Q ${x} ${y-85} ${x+4} ${y-79} L ${x+6} ${y-46} L ${x+10} ${y-74} Q ${x+13} ${y-79} ${x+16} ${y-71} L ${x+15} ${y-42} L ${x+19} ${y-60} Q ${x+23} ${y-64} ${x+25} ${y-57} L ${x+22} ${y-25} Q ${x+22} ${y-12} ${x+14} ${y+2} Z`:
      `M ${x-15} ${y-1} Q ${x-18} ${y+12} ${x-14} ${y+24} L ${x-12} ${y+39} Q ${x-9} ${y+45} ${x-7} ${y+39} L ${x-8} ${y+26} L ${x-4} ${y+46} Q ${x-1} ${y+51} ${x+1} ${y+46} L ${x-1} ${y+28} L ${x+5} ${y+48} Q ${x+8} ${y+52} ${x+10} ${y+47} L ${x+5} ${y+26} L ${x+13} ${y+43} Q ${x+16} ${y+46} ${x+18} ${y+40} L ${x+10} ${y+23} Q ${x+24} ${y+10} ${x+19} ${y+6} Q ${x+15} ${y+4} ${x+8} ${y+18} L ${x+13} ${y} Z`;
    b+=gid('hand_'+side,path(d,grad('skin'),tint(p.skin,-.27),1.4));return b;}
  parts.push(arm(p.view==='three_quarter'?'right':'left'));
  // Neck is drawn before the garment neckline.
  parts.push(gid('neck',path(`M 278 ${fy+ry-22} L 277 ${s+21} Q 300 ${s+42} 326 ${s+20} L 322 ${fy+ry-24} Z`,grad('skin'),'none')+path(`M 280 ${fy+ry-13} Q 302 ${fy+ry+1} 323 ${fy+ry-17} L 324 ${fy+ry+2} Q 301 ${fy+ry+18} 279 ${fy+ry+4} Z`,tint(p.skin,-.12))));
  let torso=path(`M ${300-tw*.77} ${s-1} Q ${300-tw*.4} ${s-20} 278 ${s-13} Q 300 ${s+7} 325 ${s-13} Q ${300+tw*.55} ${s-12} ${300+tw*.78} ${s+6} Q ${300+tw*.89} ${s+65} ${300+tw*.68} 454 Q ${300+tw*.68} ${p.hem-80} ${300+tw*.89} ${p.hem} Q 300 ${p.hem+13} ${300-tw*.87} ${p.hem} Q ${300-tw*.64} 472 ${300-tw*.76} ${s+95} Z`,grad('cloth'),clothInk,1.8);
  torso+=line(`M ${300-tw*.56} ${s+61} Q ${300-tw*.70} 424 ${300-tw*.54} ${p.hem-24} M ${300+tw*.51} ${s+74} Q ${300+tw*.63} 436 ${300+tw*.57} ${p.hem-25}`,tint(p.top,-.19),1.8,'opacity=".7"');
  torso+=line(`M ${300-tw*.68} ${p.hem-14} Q 300 ${p.hem-4} ${300+tw*.70} ${p.hem-15}`,tint(p.top,.20),2.2);
  if(p.sex==='male'){
    if(p.outfit==='baju_melayu'||p.outfit==='kurta'){
      torso+=path(`M 278 ${s-13} Q 300 ${s-1} 325 ${s-13} L 324 ${s+6} Q 300 ${s+19} 279 ${s+5} Z`,tint(p.top,-.08),clothInk,1.4)+path(`M 294 ${s+11} L 309 ${s+11} L 309 ${s+101} Q 301 ${s+107} 294 ${s+101} Z`,tint(p.top,.05),clothInk,1);
      for(let j=0;j<4;j++)torso+=ellipse(301,s+26+j*20,2.2,2.2,p.accent);
    }else{
      torso+=path(`M 278 ${s-13} L 300 ${s+20} L 285 ${s+42} L 265 ${s+3} Z`,tint(p.top,.16),clothInk,1.3)+path(`M 325 ${s-13} L 300 ${s+20} L 315 ${s+41} L 336 ${s+3} Z`,tint(p.top,.09),clothInk,1.3)+line(`M 301 ${s+27} L 301 ${p.hem-9}`,tint(p.top,-.24),1.3);
      for(let j=0;j<4;j++)torso+=ellipse(305,s+60+j*52,2,2,p.accent);
      torso+=path(`M ${300+tw*.23} ${s+78} h 33 v 40 q -16 10 -33 0 z`,tint(p.top,.03),tint(p.top,-.21),1.3);
    }
    if(p.outfit==='baju_melayu')torso+=path(`M ${300-tw*.80} 551 Q 300 562 ${300+tw*.80} 551 L ${300+tw*.79} 714 Q 300 731 ${300-tw*.79} 714 Z`,p.accent,tint(p.accent,-.26),1.5)+line(`M ${300-tw*.78} 568 Q 300 582 ${300+tw*.78} 568 M 284 568 L 284 721`,tint(p.accent,-.2),2.5)+path(`M ${300-tw*.72} 684 Q 300 699 ${300+tw*.72} 684 L ${300+tw*.72} 696 Q 300 713 ${300-tw*.72} 696 Z`,tint(p.accent,.17));
  }else{
    torso+=path(`M 278 ${s-13} Q 300 ${s+29} 325 ${s-13} Q 324 ${s+26} 301 ${s+32} Q 278 ${s+25} 278 ${s-13} Z`,tint(p.top,-.1),clothInk,1.3);
    if(p.outfit==='baju_kurung')torso+=line(`M 300 ${s+32} v 34`,tint(p.top,-.3),1.5)+ellipse(300,s+47,3,3,p.accent);
    if(p.outfit==='dress')torso+=path(`M ${300-tw*.67} 498 Q 300 511 ${300+tw*.68} 498 L ${300+tw*.69} 513 Q 300 526 ${300-tw*.67} 513 Z`,p.accent);
  }
  if(p.outfit==='cardigan'||p.outfit==='cardigan_skirt')torso+=path(`M 279 ${s-11} Q 283 360 281 ${p.hem-2} L 320 ${p.hem-2} Q 317 370 324 ${s-11} Q 302 ${s+17} 279 ${s-11} Z`,tint(p.accent,.25),tint(p.top,-.2),1.5)+line(`M 276 ${s+9} L 270 ${p.hem-4} M 327 ${s+9} L 330 ${p.hem-4}`,tint(p.top,.22),3);
  parts.push(gid('torso',torso));parts.push(arm(p.view==='three_quarter'?'left':'right'));
  // Head silhouette: genuine profile has a projecting brow, nose, lips and chin.
  let face, ear='',hairBack='',hairFront='',scarfBack='',scarfFront='';
  const q=p.view==='three_quarter', side=p.view==='side',cx=side?302:q?304:300;
  if(side){
    face=`M ${cx-30} ${fy-ry+15} Q ${cx+13} ${fy-ry-10} ${cx+33} ${fy-ry+24} Q ${cx+43} ${fy-17} ${cx+39} ${fy-7} L ${cx+(p.young?48:54)} ${fy+9} Q ${cx+(p.young?52:59)} ${fy+16} ${cx+43} ${fy+19} L ${cx+44} ${fy+29} Q ${cx+50} ${fy+33} ${cx+41} ${fy+38} L ${cx+41} ${fy+47} Q ${cx+37} ${fy+ry+5} ${cx+10} ${fy+ry-1} Q ${cx-11} ${fy+ry-5} ${cx-15} ${fy+26} Q ${cx-48} ${fy+7} ${cx-42} ${fy-25} Z`;
    ear=ellipse(cx-6,fy+8,10,16,grad('skin'))+line(`M ${cx-8} ${fy+1} q 12 -9 11 9 q -8 -3 -8 4`,tint(p.skin,-.27),1.4);
  }else{
    const shape={round:{jaw:.98,chin:.34,cheek:1.02,bottom:.96},square:{jaw:.97,chin:.58,cheek:1,bottom:.96},heart:{jaw:.60,chin:.16,cheek:1.02,bottom:1},long:{jaw:.78,chin:.27,cheek:.94,bottom:1.05},oval:{jaw:.80,chin:.28,cheek:.98,bottom:1}}[p.headShape]||{jaw:.8,chin:.28,cheek:.98,bottom:1};
    const jaw=p.child?Math.max(.90,shape.jaw):shape.jaw, chin=p.child?Math.max(.30,shape.chin):shape.chin;
    face=`M ${cx-rx*.86} ${fy-ry*.57} Q ${cx-rx*.67} ${fy-ry-5} ${cx} ${fy-ry} Q ${cx+rx*.89} ${fy-ry+1} ${cx+rx*(q?.85:.99)} ${fy-ry*.42} L ${cx+rx*(q?.85:shape.cheek)} ${fy+ry*.28} Q ${cx+rx*jaw} ${fy+ry*.80} ${cx+rx*chin} ${fy+ry*shape.bottom} Q ${cx+4} ${fy+ry*(shape.bottom+.055)} ${cx-rx*chin} ${fy+ry*shape.bottom} Q ${cx-rx*jaw} ${fy+ry*.80} ${cx-rx*shape.cheek} ${fy+ry*.08} Z`;
    ear=(q?'':ellipse(cx-rx*.94,fy+5,9,15,grad('skin')))+ellipse(cx+rx*.95,fy+6,8,14,grad('skin'));
    ear+=line(`M ${cx+rx*.94} ${fy} q 6 -1 3 10`,tint(p.skin,-.27),1.3);
  }
  const hasScarf=p.sex==='female'&&p.hijabStyle!=='none';
  if(hasScarf){
    ear=''; // Ears stay covered in every hijab view.
    const long=p.hijabStyle==='long',reach=long?478:p.hijabStyle==='shawl'?399:365;
    scarfBack=path(`M ${cx-rx-14} ${fy-ry*.65} Q ${cx-rx*.87} ${fy-ry-25} ${cx+8} ${fy-ry-21} Q ${cx+rx+17} ${fy-ry-17} ${cx+rx+22} ${fy-ry*.38} Q ${cx+rx+16} ${fy+ry*.95} ${cx+tw*.93} ${reach-25} Q ${cx+19} ${reach+33} ${cx-tw*.97} ${reach-8} Q ${cx-rx-26} ${fy+ry} ${cx-rx-14} ${fy-ry*.65} Z`,grad('scarf'),tint(p.hijab,-.26),1.7);
    scarfFront=path(`M ${cx-rx-9} ${fy-ry*.34} Q ${cx-rx*.7} ${fy-ry-14} ${cx+8} ${fy-ry-11} Q ${cx+rx*.87} ${fy-ry-4} ${cx+rx+6} ${fy-ry*.34} Q ${cx+rx*.58} ${fy-ry*.76} ${cx+4} ${fy-ry*.77} Q ${cx-rx*.62} ${fy-ry*.78} ${cx-rx*.90} ${fy-ry*.15} Q ${cx-rx*.95} ${fy+ry*.65} ${cx+4} ${fy+ry+5} Q ${cx+rx*.86} ${fy+ry*.68} ${cx+rx*.91} ${fy+9} Q ${cx+rx+18} ${fy+ry+17} ${cx+tw*.82} ${reach-17} Q ${cx+tw*.27} ${reach+4} ${cx-tw*.68} ${reach-7} Q ${cx-29} ${fy+ry+46} ${cx-13} ${fy+ry+21} Q ${cx-rx-24} ${fy+ry*.52} ${cx-rx-9} ${fy-ry*.34} Z`,grad('scarf'),tint(p.hijab,-.23),1.5);
    scarfFront+=line(`M ${cx-12} ${fy+ry+18} Q ${cx+5} ${fy+ry+58} ${cx+tw*.63} ${reach-18} M ${cx-28} ${fy+ry+35} Q ${cx-36} ${reach-25} ${cx-tw*.44} ${reach-9}`,tint(p.hijab,-.18),2)+line(`M ${cx-rx-6} ${fy-ry*.4} Q ${cx-rx*.3} ${fy-ry-25} ${cx+rx*.64} ${fy-ry*.70}`,tint(p.hijab,.25),2);
    if(p.hijabStyle==='bawal')scarfFront+=path(`M ${cx-12} ${fy+ry+21} L ${cx+5} ${reach+30} L ${cx+tw*.70} ${reach-15} Z`,tint(p.hijab,-.02),tint(p.hijab,-.18),1.2);
    if(side)scarfFront=path(`M ${cx-42} ${fy-ry*.71} Q ${cx+2} ${fy-ry-29} ${cx+33} ${fy-ry*.38} Q ${cx+20} ${fy-ry*.70} ${cx-4} ${fy-ry*.74} Q ${cx-14} ${fy-ry*.57} ${cx+2} ${fy+6} Q ${cx+3} ${fy+ry*.70} ${cx+18} ${fy+ry+4} Q ${cx-1} ${fy+ry+26} ${cx+22} ${reach-11} Q ${cx-4} ${reach+9} ${cx-43} ${reach+3} Q ${cx-76} ${fy+ry+44} ${cx-58} ${fy-ry*.18} Z`,grad('scarf'),tint(p.hijab,-.22),1.5)+line(`M ${cx-35} ${fy+ry*.47} Q ${cx-24} ${fy+ry+27} ${cx+10} ${reach-11} M ${cx-50} ${fy-ry*.51} Q ${cx-24} ${fy-ry-18} ${cx+17} ${fy-ry*.68}`,tint(p.hijab,-.17),2);
  } else {
    const female=p.sex==='female', hs=p.hairStyle;
    if(female){
      const long=['long','wavy','braid'].includes(hs),end=long?s+116:fy+ry+22;
      hairBack=path(`M ${cx-rx-6} ${fy-ry*.52} Q ${cx-rx*.9} ${fy-ry-23} ${cx+4} ${fy-ry-18} Q ${cx+rx+13} ${fy-ry-16} ${cx+rx+10} ${fy+6} Q ${cx+rx+15} ${end-30} ${cx+rx*.78} ${end} Q ${cx+rx*.43} ${end+11} ${cx+rx*.24} ${end-6} L ${cx+rx*.43} ${fy+ry*.74} L ${cx-rx*.36} ${fy+ry*.74} Q ${cx-rx*.19} ${end-13} ${cx-rx*.48} ${end+3} Q ${cx-rx-15} ${end+6} ${cx-rx-11} ${end-1} Q ${cx-rx-22} ${fy+11} ${cx-rx-6} ${fy-ry*.52} Z`,grad('hair'));
      if(hs==='bun')hairBack=ellipse(cx-rx*.78,fy-ry*.63,24,28,grad('hair'))+hairBack;
      if(hs==='braid')for(let n=0;n<5;n++)hairBack+=ellipse(cx-rx*.85,fy+ry+10+n*18,11-n,15,p.hair);
      hairFront=path(`M ${cx-rx-3} ${fy-ry*.35} Q ${cx-rx-5} ${fy-ry-17} ${cx+3} ${fy-ry-14} Q ${cx+rx+10} ${fy-ry-15} ${cx+rx+3} ${fy-ry*.17} Q ${cx+rx*.63} ${fy-ry*.34} ${cx+rx*.25} ${fy-ry*.89} Q ${cx-rx*.20} ${fy-ry*.51} ${cx-rx*.86} ${fy-ry*.29} L ${cx-rx*.95} ${fy+22} Q ${cx-rx-12} ${fy-4} ${cx-rx-3} ${fy-ry*.35} Z`,grad('hair'));
      hairFront+=line(`M ${cx+5} ${fy-ry-8} Q ${cx-rx*.39} ${fy-ry*.49} ${cx-rx*.80} ${fy-ry*.38}`,hairLight,2.5,'opacity=".75"');
      if(hs==='wavy')hairFront+=line(`M ${cx+rx*.80} ${fy-ry*.16} Q ${cx+rx+10} ${fy+23} ${cx+rx*.82} ${fy+ry+18}`,hairLight,2.8,'opacity=".65"');
    }else if(hs==='bald'){
      hairFront=path(`M ${cx-rx*.99} ${fy-ry*.28} Q ${cx-rx*.85} ${fy-ry*.66} ${cx-rx*.70} ${fy-ry*.64} L ${cx-rx*.85} ${fy+10} L ${cx-rx} ${fy+5} Z M ${cx+rx*.70} ${fy-ry*.68} Q ${cx+rx*.94} ${fy-ry*.51} ${cx+rx} ${fy-ry*.13} L ${cx+rx*.9} ${fy+7} L ${cx+rx*.82} ${fy-ry*.3} Z`,grad('hair'));
    }else{
      const curly=hs==='curly';
      hairFront=path(`M ${cx-rx} ${fy+2} L ${cx-rx-2} ${fy-ry*.45} Q ${cx-rx-4} ${fy-ry-15} ${cx-5} ${fy-ry-15} Q ${cx+rx*.38} ${fy-ry-22} ${cx+rx*.83} ${fy-ry*.72} Q ${cx+rx+8} ${fy-ry*.60} ${cx+rx} ${fy+3} L ${cx+rx*.83} ${fy+12} L ${cx+rx*.76} ${fy-ry*.42} Q ${cx+rx*.31} ${fy-ry*.61} ${cx+6} ${fy-ry*.80} Q ${cx-rx*.35} ${fy-ry*.45} ${cx-rx*.76} ${fy-ry*.49} L ${cx-rx*.84} ${fy+12} Z`,grad('hair'));
      if(curly){for(let n=0;n<7;n++)hairFront+=ellipse(cx-rx*.8+n*rx*.27,fy-ry*.78-Math.sin(n*.5)*9,13,12,grad('hair'));}
      else if(hs==='crop'){hairFront=path(`M ${cx-rx} ${fy+3} L ${cx-rx*.98} ${fy-ry*.48} Q ${cx-rx*.82} ${fy-ry-5} ${cx} ${fy-ry-5} Q ${cx+rx*.83} ${fy-ry-5} ${cx+rx*.99} ${fy-ry*.45} L ${cx+rx*.89} ${fy+9} L ${cx+rx*.77} ${fy-ry*.45} Q ${cx} ${fy-ry*.64} ${cx-rx*.78} ${fy-ry*.46} L ${cx-rx*.86} ${fy+11} Z`,grad('hair'))+line(`M ${cx-rx*.65} ${fy-ry*.73} Q ${cx} ${fy-ry*.88} ${cx+rx*.64} ${fy-ry*.72}`,hairLight,2);}
      else {hairFront+=line(`M ${cx-rx*.65} ${fy-ry*.65} Q ${cx-rx*.1} ${fy-ry-13} ${cx+rx*.56} ${fy-ry*.76} M ${cx-rx*.63} ${fy-ry*.52} Q ${cx-rx*.12} ${fy-ry*.86} ${cx+rx*.32} ${fy-ry*.77}`,hairLight,2.2,'opacity=".7"');if(hs==='wavy')hairFront+=path(`M ${cx-rx*.93} ${fy-ry*.43} Q ${cx-rx*.7} ${fy-ry-25} ${cx-rx*.15} ${fy-ry-17} Q ${cx+rx*.15} ${fy-ry-25} ${cx+rx*.62} ${fy-ry*.8} Q ${cx+rx*.1} ${fy-ry*.61} ${cx-rx*.15} ${fy-ry*.67} Q ${cx-rx*.6} ${fy-ry*.42} ${cx-rx*.93} ${fy-ry*.43} Z`,grad('hair'));}
    }
  }
  if(side&&!hasScarf){
    const hs=p.hairStyle, short=p.sex==='male', crown=hs==='crop'?5:hs==='curly'?16:15;
    hairFront=path(`M ${cx-38} ${fy+19} Q ${cx-47} ${fy-13} ${cx-42} ${fy-ry*.48} Q ${cx-38} ${fy-ry-crown} ${cx+1} ${fy-ry-12} Q ${cx+27} ${fy-ry-13} ${cx+33} ${fy-ry*.36} Q ${cx+21} ${fy-ry*.42} ${cx+14} ${fy-ry*.76} Q ${cx-1} ${fy-ry*.45} ${cx-26} ${fy-ry*.40} L ${cx-28} ${fy+7} Z`,grad('hair'))+line(`M ${cx-35} ${fy-ry*.62} Q ${cx-6} ${fy-ry-13} ${cx+22} ${fy-ry*.73}`,hairLight,2.3,'opacity=".7"');
    if(hs==='bald')hairFront=path(`M ${cx-41} ${fy-ry*.15} Q ${cx-38} ${fy-ry*.53} ${cx-25} ${fy-ry*.51} L ${cx-29} ${fy+13} L ${cx-39} ${fy+16} Z`,grad('hair'));
    if(hs==='curly')for(let n=0;n<5;n++)hairFront+=ellipse(cx-32+n*13,fy-ry*.80-Math.sin(n*.8)*10,11,10,grad('hair'));
    if(!short){
      const len=['long','wavy','braid'].includes(hs)?s+104:fy+ry+18;
      hairBack=path(`M ${cx-37} ${fy-ry*.48} Q ${cx-52} ${fy-ry-14} ${cx-1} ${fy-ry-18} Q ${cx+23} ${fy-ry-13} ${cx+29} ${fy-ry*.48} Q ${cx-10} ${fy-ry*.52} ${cx-29} ${fy+5} Q ${cx-16} ${fy+ry+7} ${cx-14} ${len-14} Q ${cx-23} ${len+10} ${cx-51} ${len-1} Q ${cx-61} ${fy+21} ${cx-37} ${fy-ry*.48} Z`,grad('hair'));
      if(hs==='bun')hairBack=ellipse(cx-48,fy-ry*.49,22,25,grad('hair'))+hairBack;
      if(hs==='braid')for(let n=0;n<5;n++)hairBack+=ellipse(cx-42,fy+ry+6+n*17,10-n,14,p.hair);
    }
  }
  if(scarfBack)parts.push(gid('hijab_back',scarfBack));
  if(hairBack)parts.push(gid('hair_back',hairBack));
  parts.push(gid('head',path(face,grad('skin'),tint(p.skin,-.20),1.3)));
  parts.push(gid('ears',ear));
  if(!side)parts.push(gid('cheek_shading',ellipse(cx-rx*.57,fy+20,rx*.19,6,tint(p.skin,.18),'opacity=".30"')+ellipse(cx+rx*.59,fy+20,rx*.16,5,tint(p.skin,.13),'opacity=".25"')));
  const spacing={round:23,square:23,oval:21,long:19,heart:22}[p.headShape]||21;
  const ey=fy+(p.child?12:-3), ex=side?[cx+30]:q?[cx-13,cx+25]:[cx-spacing,cx+spacing];
  const eyeWidth=p.child?10.5:9, eyeRy=p.expression==='surprised'?5:(p.young?4.9:3.8);
  let eyes='',brows='';
  ex.forEach((x,i)=>{const ww=q&&i===1?eyeWidth*.73:side?7.5:eyeWidth;
    eyes+=path(`M ${x-ww} ${ey} Q ${x} ${ey-eyeRy*1.75} ${x+ww} ${ey} Q ${x} ${ey+eyeRy} ${x-ww} ${ey} Z`,'#fff9f1',ink,1.4);
    eyes+=ellipse(x+(side?2:q?1:0),ey-.2,p.child?2.7:2.35,p.child?3.1:2.7,tint(p.hair,-.1))+ellipse(x+.6,ey-1.4,.8,.8,'#fff');
    const concern=p.expression==='concerned',by=ey-(p.child?13:13.5),lift=concern?(i===0?-3:3):p.expression==='surprised'?-4:0;
    brows+=line(`M ${x-ww} ${by+2-lift} Q ${x} ${by-2} ${x+ww} ${by+1+lift}`,p.hair,p.sex==='female'?2.6:3.4);
  });
  parts.push(gid('eyes',eyes));parts.push(gid('brows',brows));
  let nose=side?line(`M ${cx+38} ${fy-1} L ${cx+47} ${fy+13} M ${cx+41} ${fy+19} l -7 -1`,tint(p.skin,-.32),1.6):line(`M ${cx+(q?10:2)} ${fy+1} q -3 12 -3 18 q 5 4 11 0`,tint(p.skin,-.31),1.5)+ellipse(cx+(q?9:3),fy+21,4,1.2,tint(p.skin,-.23));
  parts.push(gid('nose',nose));
  const mx=side?cx+41:q?cx+11:cx,my=fy+(p.child?48:36),mw=p.child?12:12;
  let mouth=p.expression==='happy'?path(`M ${mx-mw} ${my-1} Q ${mx} ${my+4} ${mx+mw} ${my-1} Q ${mx} ${my+17} ${mx-mw} ${my-1} Z`,tint(p.skin,-.48))+path(`M ${mx-mw+3} ${my+1} Q ${mx} ${my+4} ${mx+mw-3} ${my+1} L ${mx+mw-5} ${my+5} Q ${mx} ${my+7} ${mx-mw+5} ${my+5} Z`,'#fff8eb'):
    p.expression==='surprised'?ellipse(mx,my+2,4.5,7,tint(p.skin,-.48)):
    line(`M ${mx-mw*.8} ${my+(p.expression==='concerned'?4:0)} Q ${mx} ${my+(p.expression==='concerned'?-1:3)} ${mx+mw*.8} ${my+(p.expression==='concerned'?4:0)}`,tint(p.skin,-.50),1.8);
  if(!side)mouth+=line(`M ${mx-5} ${my+7} q 5 2 10 0`,tint(p.skin,-.17),1.3);
  parts.push(gid('mouth',mouth));
  if(p.elder){parts.push(gid('age_details',line(`M ${cx-21} ${fy-ry*.46} Q ${cx} ${fy-ry*.52} ${cx+20} ${fy-ry*.44} M ${cx-19} ${fy-ry*.35} Q ${cx} ${fy-ry*.40} ${cx+18} ${fy-ry*.34}`,tint(p.skin,-.22),1.2)+ex.map(x=>line(`M ${x-8} ${ey+8} q 8 3 16 0 M ${x-11} ${ey+1} l -4 3`,tint(p.skin,-.25),1.1)).join('')+line(`M ${mx-18} ${my-7} q -6 9 -3 18 M ${mx+18} ${my-7} q 6 9 3 18`,tint(p.skin,-.24),1.1)));}
  if(p.sex==='male'&&p.facialHair!=='none'){
    let fh=p.facialHair==='moustache'?path(`M ${mx} ${my-8} Q ${mx-8} ${my-12} ${mx-16} ${my-4} Q ${mx-8} ${my-1} ${mx} ${my-5} Q ${mx+9} ${my-1} ${mx+16} ${my-4} Q ${mx+8} ${my-12} ${mx} ${my-8}`,grad('hair')):
      p.facialHair==='goatee'?path(`M ${mx-9} ${my+8} Q ${mx} ${my+12} ${mx+10} ${my+7} L ${mx+7} ${my+22} Q ${mx} ${my+28} ${mx-8} ${my+22} Z`,grad('hair')):
      path(`M ${cx-rx*.83} ${fy+14} Q ${cx-rx*.53} ${fy+45} ${mx-13} ${my+3} Q ${mx} ${my+15} ${mx+15} ${my+3} Q ${cx+rx*.65} ${fy+41} ${cx+rx*.87} ${fy+13} Q ${cx+rx*.83} ${fy+ry*.76} ${cx+6} ${fy+ry+7} Q ${cx-rx*.65} ${fy+ry*.83} ${cx-rx*.83} ${fy+14} Z`,grad('hair'));
    parts.push(gid('facial_hair',fh));
  }
  if(hairFront)parts.push(gid('hair_front',hairFront));if(scarfFront)parts.push(gid('hijab_front',scarfFront));
  let accessory='';
  if(p.glasses!=='none'){
    ex.forEach((x,i)=>{const ww=side?11:q&&i===1?11:15;accessory+=p.glasses==='round'?ellipse(x,ey,ww,12,'#e8f1ee','fill-opacity=".15" stroke="#444b4d" stroke-width="2"'):`<rect x="${x-ww}" y="${ey-10}" width="${ww*2}" height="21" rx="4" fill="#e8f1ee" fill-opacity=".15" stroke="#444b4d" stroke-width="2"/>`;});
    if(ex.length===2)accessory+=line(`M ${ex[0]+13} ${ey-2} Q ${cx} ${ey-7} ${ex[1]-12} ${ey-2}`,'#444b4d',2);
    accessory+=line(`M ${ex[ex.length-1]+12} ${ey-4} L ${cx+rx+1} ${fy-3}`,'#444b4d',2);
  }
  parts.push(gid('accessories',accessory));
  if(p.view==='back'){
    const replace=(name,body)=>{const i=parts.findIndex(x=>x.startsWith(`<g id="${id}_${name}"`));if(i>=0)parts[i]=gid(name,body);else parts.push(gid(name,body));};
    const remove=new Set(['head','ears','eyes','brows','nose','mouth','cheek_shading','age_details','facial_hair','hair_front','hair_back','hijab_front','hijab_back','accessories']);
    parts=parts.filter(x=>!Array.from(remove).some(k=>x.startsWith(`<g id="${id}_${k}"`)));
    let bt=path(`M ${300-w*.78} ${s+3} Q 300 ${s-31} ${300+w*.78} ${s+3} Q ${300+w*.85} 430 ${300+w*.87} ${p.hem} Q 300 ${p.hem+13} ${300-w*.87} ${p.hem} Q ${300-w*.83} 430 ${300-w*.78} ${s+3} Z`,grad('cloth'),clothInk,1.8);
    bt+=line(`M ${300-w*.73} ${s+36} Q 300 ${s+54} ${300+w*.73} ${s+36} M 300 ${s+52} L 300 ${p.hem-17}`,tint(p.top,-.16),1.4);
    bt+=path(`M 277 ${s-8} Q 300 ${s+7} 326 ${s-8} L 326 ${s+7} Q 300 ${s+22} 277 ${s+7} Z`,tint(p.top,-.08),clothInk,1.3);
    if(p.outfit==='baju_melayu')bt+=path(`M ${300-w*.80} 551 Q 300 562 ${300+w*.80} 551 L ${300+w*.79} 714 Q 300 731 ${300-w*.79} 714 Z`,p.accent,tint(p.accent,-.26),1.5);
    replace('torso',bt);
    replace('neck',path(`M 278 ${fy+ry-18} L 278 ${s+2} Q 300 ${s+19} 324 ${s+2} L 322 ${fy+ry-18} Z`,grad('skin')));
    if(hasScarf){
      parts.push(gid('hijab_back',path(`M ${300-rx-16} ${fy-ry*.56} Q ${300-rx-9} ${fy-ry-24} 300 ${fy-ry-22} Q ${300+rx+22} ${fy-ry-18} ${300+rx+17} ${fy-ry*.39} L ${300+w*.89} ${p.hijabStyle==='long'?480:405} Q 300 ${p.hijabStyle==='long'?503:430} ${300-w*.91} ${p.hijabStyle==='long'?480:405} Z`,grad('scarf'),tint(p.hijab,-.24),1.7)+line(`M 300 ${fy-ry+2} Q 289 ${fy+ry} 305 ${p.hijabStyle==='long'?480:405}`,tint(p.hijab,-.15),1.7)));
    }else{
      parts.push(gid('ears',ellipse(300-rx*.94,fy+5,8,14,grad('skin'))+ellipse(300+rx*.94,fy+5,8,14,grad('skin'))));
      parts.push(gid('head',ellipse(300,fy,rx,ry,grad('skin'))));
      const longHair=p.sex==='female'&&['wavy','long','braid'].includes(p.hairStyle),end=longHair?s+100:fy+ry*.73;
      const hair= p.hairStyle==='bald'?path(`M ${300-rx} ${fy-ry*.14} Q 300 ${fy+ry*.91} ${300+rx} ${fy-ry*.14} L ${300+rx*.94} ${fy+ry*.51} Q 300 ${fy+ry*.98} ${300-rx*.94} ${fy+ry*.51} Z`,grad('hair')):path(`M ${300-rx-5} ${fy-ry*.42} Q ${300-rx} ${fy-ry-20} 300 ${fy-ry-15} Q ${300+rx+9} ${fy-ry-17} ${300+rx+6} ${fy-ry*.36} L ${300+rx*.92} ${end} Q 300 ${end+17} ${300-rx*.92} ${end} Z`,grad('hair'));
      parts.push(gid('hair_back',hair+(p.hairStyle==='bun'?ellipse(300,fy+ry*.57,25,27,grad('hair')):'')));
    }
    for(const [name,x]of [['left',258],['right',341]])replace('shoe_'+name,path(`M ${x-24} 916 Q ${x} 909 ${x+24} 916 L ${x+25} 941 Q ${x} 949 ${x-25} 941 Z`,p.shoes,tint(p.shoes,-.25),1.6)+line(`M ${x-21} 937 Q ${x} 943 ${x+21} 937`,tint(p.shoes,.3),2));
  }
  if(opts.guides)parts.push(gid('guides',Object.entries(g.landmarks).map(([key,xy])=>ellipse(xy[0],xy[1],3.2,3.2,'#db4760')+`<text x="${xy[0]+5}" y="${xy[1]-4}" font-family="sans-serif" font-size="8" fill="#9b2840">${esc(key)}</text>`).join(''),'opacity=".85"'));
  const vb=opts.headOnly?`180 25 245 ${Math.ceil(s+90)}`:'0 0 600 1000';
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${Number(opts.width)||600}" height="${Number(opts.height)||1000}" viewBox="${vb}" role="img" aria-labelledby="${id}_title"><title id="${id}_title">${esc(c.name)} · ${esc(p.view)} · ${esc(p.expression)}</title><metadata>${esc(JSON.stringify({creator:'Original code-drawn character bank',character_id:c.id,view:p.view,version:'1.0',asset_type:'static layered SVG',external_assets:false}))}</metadata>${defs}${p.flipX?'<g transform="translate(600 0) scale(-1 1)">':''}${parts.join('')}${p.flipX?'</g>':''}</svg>`;
}
module.exports={characterSvg,geometry};
