/**
 * Original articulated companion for character_renderer.cjs.
 * All limb controls are GLOBAL degrees from down: 0 down, +90 screen-right.
 * bodyLean/headTilt are clockwise SVG degrees: positive leans an upright head right.
 * rootX/rootY are translations in the 600 x 1000 authored SVG coordinate system.
 * This is a deterministic two-bone drawing rig, not a physics or collision solver.
 */
'use strict';
const {characterSvg,geometry:baseGeometry}=require('./character_renderer.cjs');
const R=Math.PI/180, clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
const n=x=>Math.round((Number(x)||0)*1000)/1000;
const xy=p=>`${n(p[0])} ${n(p[1])}`;
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const safe=x=>String(x||'character').replace(/[^A-Za-z0-9_-]/g,'_');
const validColor=(s,f)=>/^#[0-9a-f]{6}$/i.test(s||'')?s:f;
function tint(hex,k){hex=validColor(hex,'#98735c');return '#'+hex.slice(1).match(/../g).map(x=>{const v=parseInt(x,16);return Math.round(k>=0?v+(255-v)*k:v*(1+k)).toString(16).padStart(2,'0');}).join('');}
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]];
const mid=(a,b)=>[(a[0]+b[0])/2,(a[1]+b[1])/2];
const dist=(a,b)=>Math.hypot(a[0]-b[0],a[1]-b[1]);
const angle=(a,b)=>Math.atan2(b[0]-a[0],b[1]-a[1])/R;
const endpoint=(a,length,degrees)=>[a[0]+Math.sin(degrees*R)*length,a[1]+Math.cos(degrees*R)*length];
/** Optional deterministic analytical IK helper. bend selects either elbow solution. */
function solveTwoBone(origin,target,length1,length2,bend=1){
  const dx=target[0]-origin[0],dy=target[1]-origin[1],raw=Math.hypot(dx,dy),d=clamp(raw,Math.abs(length1-length2)+.001,length1+length2-.001);
  const bearing=Math.atan2(dy,dx),offset=Math.acos(clamp((length1*length1+d*d-length2*length2)/(2*length1*d),-1,1));
  const elbow=[origin[0]+Math.cos(bearing+(bend>=0?1:-1)*offset)*length1,origin[1]+Math.sin(bearing+(bend>=0?1:-1)*offset)*length1];
  const wrist=[origin[0]+Math.cos(bearing)*d,origin[1]+Math.sin(bearing)*d];
  return {upper:angle(origin,elbow),lower:angle(elbow,wrist),elbow,wrist,reachable:raw>=Math.abs(length1-length2)&&raw<=length1+length2};
}
function rotate(p,origin,degrees){const co=Math.cos(degrees*R),si=Math.sin(degrees*R),x=p[0]-origin[0],y=p[1]-origin[1];return [origin[0]+co*x-si*y,origin[1]+si*x+co*y];}
function normalized(c,state={},opts={}){
  const rawView=opts.view||state.orientation||state.view||'front';
  const view=(rawView==='side_right'||rawView==='side_left')?'side':(rawView==='three_quarter_right'||rawView==='three_quarter_left')?'three_quarter':(['front','three_quarter','side','back'].includes(rawView)?rawView:'front');
  const g=baseGeometry(c,{view}),j=g.landmarks;
  const defaults={rootX:0,rootY:0,bodyLean:0,headTilt:0,
    leftUpperArm:angle(j.shoulder_left,j.elbow_left),rightUpperArm:angle(j.shoulder_right,j.elbow_right),
    leftUpperArmScale:1,rightUpperArmScale:1,
    leftForearm:angle(j.elbow_left,j.wrist_left),rightForearm:angle(j.elbow_right,j.wrist_right),
    leftThigh:angle(j.hip_left,j.knee_left),rightThigh:angle(j.hip_right,j.knee_right),
    leftShin:angle(j.knee_left,j.ankle_left),rightShin:angle(j.knee_right,j.ankle_right),
    footLeft:0,footRight:0,handLeft:'relaxed',handRight:'relaxed',expression:'neutral',blink:0,mouthOpen:0,
    breath:0,headYaw:0,gazeX:0,shoulderLift:0,fingerTapLeft:0,fingerTapRight:0,prop:null,propAttachment:null,secondaryProp:null};
  const s={...defaults,...state,view,orientation:rawView,flipX:rawView==='side_left'||rawView==='three_quarter_left'};
  for(const key of Object.keys(defaults))if(typeof defaults[key]==='number')s[key]=Number.isFinite(Number(s[key]))?Number(s[key]):defaults[key];
  s.bodyLean=clamp(s.bodyLean,-55,55);s.headTilt=clamp(s.headTilt,-45,45);
  s.blink=clamp(s.blink,0,1);s.mouthOpen=clamp(s.mouthOpen,0,1);
  s.breath=clamp(s.breath,-2,2);s.headYaw=clamp(s.headYaw,-30,30);s.gazeX=clamp(s.gazeX,-12,12);s.shoulderLift=clamp(s.shoulderLift,-12,18);
  s.fingerTapLeft=clamp(s.fingerTapLeft,0,1);s.fingerTapRight=clamp(s.fingerTapRight,0,1);
  s.leftUpperArmScale=clamp(s.leftUpperArmScale,.45,1.25);s.rightUpperArmScale=clamp(s.rightUpperArmScale,.45,1.25);
  if(!['neutral','happy','concerned','surprised'].includes(s.expression))s.expression='neutral';
  for(const key of ['handLeft','handRight'])if(!['relaxed','open','point','grip'].includes(s[key]))s[key]='relaxed';
  return {s,g};
}
function defaultState(c,opts={}){return normalized(c,{},opts).s;}
function rigGeometry(c,state={},opts={}){
  const {s,g}=normalized(c,state,opts),j=g.landmarks,root=[s.rootX,s.rootY],pelvis=j.pelvis;
  const lift=s.shoulderLift+s.breath*1.8;
  const out={};
  for(const side of ['left','right']){
    const title=side==='left'?'Left':'Right',prefix=side==='left'?'left':'right';
    const shoulder=rotate(add(j['shoulder_'+side],[0,-lift]),pelvis,s.bodyLean);
    const upper=dist(j['shoulder_'+side],j['elbow_'+side])*s[prefix+'UpperArmScale'],fore=dist(j['elbow_'+side],j['wrist_'+side]);
    const elbow=endpoint(shoulder,upper,s[prefix+'UpperArm']),wrist=endpoint(elbow,fore,s[prefix+'Forearm']);
    const hip=j['hip_'+side],thigh=184,shin=159;
    const knee=endpoint(hip,thigh,s[prefix+'Thigh']),ankle=endpoint(knee,shin,s[prefix+'Shin']);
    out['shoulder_'+side]=add(shoulder,root);out['elbow_'+side]=add(elbow,root);out['wrist_'+side]=add(wrist,root);
    out['fingers_'+side]=add(endpoint(wrist,s['hand'+title]==='point'?65:49,s['handAngle'+title]??s[prefix+'Forearm']),root);
    out['hip_'+side]=add(hip,root);out['knee_'+side]=add(knee,root);out['ankle_'+side]=add(ankle,root);
    out['heel_'+side]=add(rotate([ankle[0]-23,ankle[1]+26],ankle,s['foot'+title]),root);
    out['toe_'+side]=add(rotate([ankle[0]+46,ankle[1]+28],ankle,s['foot'+title]),root);
  }
  out.pelvis=add(pelvis,root);out.neck=add(rotate(add(j.neck,[0,-lift]),pelvis,s.bodyLean),root);
  out.head=add(rotate(add(rotate(j.head,j.neck,s.headTilt),[0,-lift]),pelvis,s.bodyLean),root);
  const authoredWidth=({slender:90,average:105,broad:121,stocky:124}[c.body?.build]||105)*(c.age<13?.88:1)*(s.view==='side'?.62:s.view==='three_quarter'?.84:1);
  const edgePad=Math.max(110,authoredWidth*1.08+28),allPoints=Object.values(out);
  const bounds={left:Math.min(...allPoints.map(p=>p[0]))-edgePad,right:Math.max(...allPoints.map(p=>p[0]))+edgePad,
    top:Math.min(out.head[1]-g.segments.head_height*.65-25,...allPoints.map(p=>p[1]))-22,
    bottom:Math.max(...allPoints.map(p=>p[1]))+45};
  // These are conservative draw bounds, including opaque cloth cages and props.
  // A consumer should union them across a clip and keep one camera/viewBox.
  if(s.prop==='chair'||s.secondaryProp==='chair'){
    const chairX=['sit_down','stand_up'].includes(s.motion)?116:300+s.rootX;
    bounds.left=Math.min(bounds.left,chairX-80);bounds.right=Math.max(bounds.right,chairX+142);bounds.top=Math.min(bounds.top,550);bounds.bottom=Math.max(bounds.bottom,949);
  }
  if(s.prop==='laptop'&&s.propAttachment==='desk'){bounds.left=Math.min(bounds.left,365);bounds.right=Math.max(bounds.right,665);bounds.top=Math.min(bounds.top,660);bounds.bottom=Math.max(bounds.bottom,949);}
  if(s.prop&&s.prop!=='chair'){
    const C=mid(out.wrist_left,out.wrist_right),W=s.handRight==='grip'?out.wrist_right:out.wrist_left;
    const candidates=s.prop==='phone'?[W]:[C];
    for(const P of candidates){bounds.left=Math.min(bounds.left,P[0]-115);bounds.right=Math.max(bounds.right,P[0]+115);bounds.top=Math.min(bounds.top,P[1]-90);bounds.bottom=Math.max(bounds.bottom,P[1]+125);}
  }
  if(s.turnScaleX&&!opts.internal){for(const P of Object.values(out))P[0]=300+(P[0]-300)*s.turnScaleX;}
  if(s.flipX&&!opts.internal){for(const P of Object.values(out))P[0]=600-P[0];const l=bounds.left;bounds.left=600-bounds.right;bounds.right=600-l;}
  bounds.minX=bounds.left;bounds.minY=bounds.top;bounds.maxX=bounds.right;bounds.maxY=bounds.bottom;
  return {...g,view:s.orientation,schema_version:3,rig_status:'Articulated deterministic two-bone vector rig; evaluated joint positions, original face/style, deforming modest garments. No physics or automatic IK.',
    state:s,landmarks:out,segments:{...g.segments,
      upper_arm_left:g.segments.upper_arm_left*s.leftUpperArmScale,upper_arm_right:g.segments.upper_arm_right*s.rightUpperArmScale,
      thigh_left:184,shin_left:159,thigh_right:184,shin_right:159},
    bounds};
}
function extract(svg){
  const defs=svg.match(/<defs>[\s\S]*?<\/defs>/)?.[0]||'',groups={};
  const body=svg.slice(svg.indexOf('</defs>')+7),rx=/<g\b[^>]*>|<\/g>/g;let depth=0,start=-1,name='';
  for(let m;(m=rx.exec(body));){if(m[0].startsWith('</')){depth--;if(depth===0&&start>=0){groups[name]=body.slice(start,rx.lastIndex);start=-1;}}else{if(depth===0){start=m.index;name=m[0].match(/\bid="[^"]+?_(front|three_quarter|side|back)_(.+?)"/)?.[2]||'';}depth++;}}
  return {defs,groups};
}
const artCache=new Map();
function originalArt(c,s){
  const key=JSON.stringify(c)+'|'+s.view+'|'+s.expression;
  if(!artCache.has(key)){
    if(artCache.size>255)artCache.delete(artCache.keys().next().value);
    artCache.set(key,extract(characterSvg(c,{view:s.view,expression:s.expression,transparent:true})));
  }
  const art=artCache.get(key);return {defs:art.defs,groups:{...art.groups}};
}
function rigSvg(c,state={},opts={}){
  const {s,g:base}=normalized(c,state,opts),g=rigGeometry(c,s,{...opts,internal:true}),j=g.landmarks;
  const prefix=`${safe(opts.instanceId||c.id)}_${safe(s.orientation)}_rig`,oldPrefix=`${safe(c.id)}_${s.view}`;
  let {defs,groups}=originalArt(c,s);
  const rep=x=>(x||'').split(oldPrefix).join(prefix);
  defs=rep(defs);for(const key of Object.keys(groups))groups[key]=rep(groups[key]);
  const group=(name,body,attrs='')=>`<g id="${prefix}_${name}" ${attrs}>${body}</g>`;
  const path=(d,fill,stroke='none',sw=1,attrs='')=>`<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round" ${attrs}/>`;
  const line=(d,stroke,sw=2,attrs='')=>path(d,'none',stroke,sw,attrs);
  const ell=(x,y,rx,ry,fill,attrs='')=>`<ellipse cx="${n(x)}" cy="${n(y)}" rx="${n(rx)}" ry="${n(ry)}" fill="${fill}" ${attrs}/>`;
  const rect=(x,y,w,h,fill,rx=0,attrs='')=>`<rect x="${n(x)}" y="${n(y)}" width="${n(w)}" height="${n(h)}" rx="${rx}" fill="${fill}" ${attrs}/>`;
  const grad=name=>`url(#${prefix}_${name})`;
  const top=validColor(c.style?.top,'#547c81'),bottom=validColor(c.style?.bottom,'#334b55'),skin=validColor(c.body?.skin,'#bb8567'),shoes=validColor(c.style?.shoes,'#453b38'),accent=validColor(c.style?.accent,'#b99864');
  const outline=tint(top,-.32),legInk=tint(bottom,-.28),skinInk=tint(skin,-.28);
  const local=p=>[p[0]-s.rootX,p[1]-s.rootY];
  const p={};for(const key of Object.keys(j))p[key]=local(j[key]);
  const width=({slender:90,average:105,broad:121,stocky:124}[c.body?.build]||105)*(c.age<13?.88:1)*(s.view==='side'?.62:s.view==='three_quarter'?.84:1);
  const skirt=c.sex==='female'&&c.style?.outfit!=='tunic_trousers',hem=base.garments.hem_y;
  const isDress=c.style?.outfit==='dress',isSamping=c.style?.outfit==='baju_melayu';
  function capsule(A,B,wa,wb,fill,stroke,sw=1.8){
    const len=dist(A,B)||1,dx=(B[0]-A[0])/len,dy=(B[1]-A[1])/len,N=[dy,-dx];
    return path(`M ${xy(add(A,[N[0]*wa,N[1]*wa]))} Q ${xy(add(mid(A,B),[N[0]*(wa+wb)*.56,N[1]*(wa+wb)*.56]))} ${xy(add(B,[N[0]*wb,N[1]*wb]))} Q ${xy(add(B,[dx*9,dy*9]))} ${xy(add(B,[-N[0]*wb,-N[1]*wb]))} L ${xy(add(A,[-N[0]*wa,-N[1]*wa]))} Q ${xy(add(A,[-dx*wa*.7,-dy*wa*.7]))} ${xy(add(A,[N[0]*wa,N[1]*wa]))} Z`,fill,stroke,sw);
  }
  function leg(side){
    const H=p['hip_'+side],K=p['knee_'+side],A=p['ankle_'+side],far=s.view==='three_quarter'&&side==='right',lw=far?24:28;
    // A long skirt is the opaque leg silhouette. Hidden trouser capsules must not
    // protrude through it as angular spikes during a stride.
    let x=skirt?'':group('leg_'+side+'_thigh',capsule(H,K,lw+5,lw,grad('trouser'),legInk));
    if(!skirt)x+=group('leg_'+side+'_shin',capsule(K,A,lw,lw-5,grad('trouser'),legInk)+line(`M ${xy(add(K,[2,15]))} Q ${xy(add(mid(K,A),[7,0]))} ${xy(add(A,[2,-16]))}`,tint(bottom,.21),2,'opacity=".6"'));
    const footAngle=side==='left'?s.footLeft:s.footRight,ax=A[0],ay=A[1];
    let shoe=path(`M ${n(ax-22)} ${n(ay)} Q ${n(ax)} ${n(ay+5)} ${n(ax+21)} ${n(ay)} L ${n(ax+25)} ${n(ay+12)} Q ${n(ax+47)} ${n(ay+14)} ${n(ax+49)} ${n(ay+26)} Q ${n(ax+15)} ${n(ay+34)} ${n(ax-25)} ${n(ay+27)} L ${n(ax-25)} ${n(ay+12)} Z`,shoes,tint(shoes,-.25),1.7)+line(`M ${n(ax-22)} ${n(ay+25)} Q ${n(ax+17)} ${n(ay+30)} ${n(ax+45)} ${n(ay+25)} M ${n(ax+8)} ${n(ay+10)} l 13 5 M ${n(ax+4)} ${n(ay+15)} l 13 5`,tint(shoes,.3),1.8);
    if(s.view==='back')shoe=rect(ax-24,ay,48,31,shoes,10)+line(`M ${n(ax-21)} ${n(ay+25)} Q ${n(ax)} ${n(ay+33)} ${n(ax+21)} ${n(ay+25)}`,tint(shoes,.3),2);
    return x+group('shoe_'+side,shoe,`transform="rotate(${n(footAngle)} ${xy(A)})"`);
  }
  function hand(side){
    const W=p['wrist_'+side],style=side==='left'?s.handLeft:s.handRight,a=side==='left'?(s.handAngleLeft??s.leftForearm):(s.handAngleRight??s.rightForearm);
    let d;
    if(style==='open')d='M -15 -2 L -17 23 Q -28 34 -24 41 Q -20 46 -11 33 L -12 59 Q -11 67 -7 64 L -3 39 L -2 70 Q 1 76 5 69 L 6 39 L 10 65 Q 14 70 17 63 L 15 36 L 20 53 Q 24 58 27 51 L 23 21 Q 22 8 14 -1 Z';
    else if(style==='point')d='M -15 -2 L -17 26 Q -24 36 -18 43 Q -13 48 -8 42 L -6 27 L -3 65 Q -1 72 4 66 L 5 25 Q 15 20 20 29 Q 25 41 19 48 Q 12 57 2 47 L -9 43 L 14 -1 Z';
    else if(style==='grip')d='M -15 -1 Q -20 15 -16 31 Q -6 44 11 37 Q 23 31 21 13 L 10 10 Q 6 2 -3 9 L -5 25 Q 2 28 10 23 Q 15 15 11 7 L 14 -1 Z';
    else d='M -15 -1 Q -18 12 -14 24 L -12 39 Q -9 45 -7 39 L -8 26 L -4 46 Q -1 51 1 46 L -1 28 L 5 48 Q 8 52 10 47 L 5 26 L 13 43 Q 16 46 18 40 L 10 23 Q 24 10 19 6 Q 15 4 8 18 L 13 0 Z';
    const tap=side==='left'?s.fingerTapLeft:s.fingerTapRight;
    return group('hand_'+side,path(d,grad('skin'),skinInk,1.4),`transform="translate(${xy(W)}) rotate(${n(-a)}) scale(1 ${n(1-.14*tap)})"`);
  }
  function arm(side,part='both'){
    const S=p['shoulder_'+side],E=p['elbow_'+side],W=p['wrist_'+side],far=s.view==='three_quarter'&&side==='right';
    const f=side==='left'?s.leftForearm:s.rightForearm;
    const cuff=group('cuff_'+side,line('M -16 -5 L 16 -5',tint(top,-.25),2),`transform="translate(${xy(W)}) rotate(${n(-f)})"`);
    const upper=group('arm_'+side+'_upper',ell(E[0],E[1],far?21:24,far?21:24,grad('cloth'))+capsule(S,E,far?24:29,far?22:25,grad('cloth'),outline));
    const lower=group('arm_'+side+'_lower',capsule(E,W,far?22:25,far?16:18,grad('cloth'),outline))+cuff;
    return part==='upper'?upper:part==='lower'?lower:upper+lower;
  }
  // A connected cloth cage follows both knee/ankle chains; gaps never expose skin.
  function clothCage(endY,colorFill,stroke,name,topY=558,wide=1){
    const q=clamp((endY-568)/(911-568),0,1),shape=side=>{
      const H=p['hip_'+side],K=p['knee_'+side],A=p['ankle_'+side];
      return q<.54?[H[0]+(K[0]-H[0])*q/.54,H[1]+(K[1]-H[1])*q/.54]:[K[0]+(A[0]-K[0])*(q-.54)/.46,K[1]+(A[1]-K[1])*(q-.54)/.46];};
    const H=[300-width*.78,topY],J=[300+width*.78,topY],A=shape('left'),B=shape('right');
    const spread=width*(.63+q*.27)*wide;
    let lowLeft=[Math.min(A[0],B[0])-spread,Math.max(A[1],B[1])+7],lowRight=[Math.max(A[0],B[0])+spread,Math.max(A[1],B[1])+7];
    // Keep a convex, continuous side curve between waist and hem. An unrelated
    // knee must not pull a short tunic edge into a triangular bulge.
    const sideL=[Math.min(H[0],lowLeft[0]),topY+(lowLeft[1]-topY)*.55];
    const sideR=[Math.max(J[0],lowRight[0]),topY+(lowRight[1]-topY)*.55];
    const baseCenter=mid(lowLeft,lowRight);
    const d=`M ${xy(H)} Q 300 ${n(topY+8)} ${xy(J)} Q ${xy(sideR)} ${xy(lowRight)} Q ${n(baseCenter[0])} ${n(baseCenter[1]+14)} ${xy(lowLeft)} Q ${xy(sideL)} ${xy(H)} Z`;
    const seam1=[(H[0]+baseCenter[0])/2,(topY+baseCenter[1])/2],seam2=[(J[0]+baseCenter[0])/2,(topY+baseCenter[1])/2];
    return group(name,path(d,colorFill,stroke,1.7)+line(`M ${n(H[0]+25)} ${n(topY+20)} Q ${xy(seam1)} ${n(lowLeft[0]+35)} ${n(lowLeft[1]-12)} M ${n(J[0]-25)} ${n(topY+20)} Q ${xy(seam2)} ${n(lowRight[0]-35)} ${n(lowRight[1]-12)}`,tint(name==='skirt'?bottom:top,.19),2,'opacity=".7"')+line(`M ${n(lowLeft[0]+12)} ${n(lowLeft[1]-10)} Q ${n(baseCenter[0])} ${n(baseCenter[1]+3)} ${n(lowRight[0]-12)} ${n(lowRight[1]-10)}`,tint(name==='skirt'?bottom:top,.2),2));
  }
  const torsoMatrix=`rotate(${n(s.bodyLean)} 300 568) translate(0 ${n(-s.shoulderLift-s.breath*1.8)})`;
  // Keep upper clothing/collars/buttons from the original artwork, clip at pelvis,
  // then rebuild only its lower loose cloth as a joint-following opaque cage.
  const torsoClip=prefix+'_torso_upper_clip';
  defs=defs.replace('</defs>',`<clipPath id="${torsoClip}"><rect x="-600" y="-600" width="1800" height="1169"/></clipPath></defs>`);
  let upper=group('torso_upper_art',groups.torso||'',`clip-path="url(#${torsoClip})"`);
  const headNames=s.view==='back'?['head','ears','hair_back','hijab_back']:['hijab_back','hair_back','head','ears','cheek_shading','eyes','brows','nose','mouth','age_details','facial_hair','hair_front','hijab_front','accessories'];
  // Blink closes the original eye shapes around their local eye line, maintaining likeness.
  const age=Number(c.age)||30,faceY=56+(age<8?189:age<13?174:age<20?145:age>=65?143:135)*.53,ey=faceY+(age<13?12:-3);
  if(s.blink>0&&groups.eyes){groups.eyes=group('blink',groups.eyes,`transform="translate(0 ${n(ey)}) scale(1 ${n(Math.max(.06,1-s.blink))}) translate(0 ${n(-ey)})"`);}
  if(s.gazeX&&groups.eyes)groups.eyes=groups.eyes.replace(/<ellipse /g,`<ellipse transform="translate(${n(s.gazeX*.3)} 0)" `);
  if(s.mouthOpen>0){const cx=s.view==='side'?343:s.view==='three_quarter'?315:300,my=faceY+(age<13?48:36);
    groups.mouth=group('mouth',ell(cx,my+2,5+s.mouthOpen*4,2+s.mouthOpen*11,tint(skin,-.56))+ell(cx,my+4+s.mouthOpen*4,3+s.mouthOpen*3,1+s.mouthOpen*2,tint(skin,-.13)));}
  if(s.tear&&s.view!=='back'){const ex=s.view==='side'?337:326;groups.eyes=(groups.eyes||'')+group('tears',ell(ex,ey+14+Math.sin((s.progress||0)*Math.PI)*12,3,7,'#75bfd2',`opacity="${n(s.tear)}"`));}
  const N=base.landmarks.neck;
  const facialFeatures=new Set(['eyes','brows','nose','mouth','age_details','facial_hair','accessories']);
  let head=group('head_art',headNames.map(k=>s.headYaw&&facialFeatures.has(k)?group('yaw_'+k,groups[k]||'',`transform="translate(${n(s.headYaw*.23)} 0)"`):groups[k]||'').join(''),`transform="rotate(${n(s.headTilt)} ${xy(N)}) translate(300 0) scale(${n(1-Math.abs(s.headYaw)/190)} 1) translate(-300 0)"`);
  let elements=[];
  const vb=Array.isArray(opts.viewBox)&&opts.viewBox.length===4?opts.viewBox.map(n):[0,0,600,1000];
  if(opts.transparent===false)elements.push(rect(vb[0],vb[1],vb[2],vb[3],validColor(opts.background,'#f5f0e7')));
  // Ground shadow stays on the world ground, while its center follows the feet.
  elements.push(group('shadow',ell((j.ankle_left[0]+j.ankle_right[0])/2,949,Math.max(55,Math.abs(j.ankle_right[0]-j.ankle_left[0])/2+65),10,'#1e2728','opacity=".08"')));
  let body=[];
  if(s.prop==='chair'||s.secondaryProp==='chair'){
    const cx=['sit_down','stand_up'].includes(s.motion)?116:300+s.rootX,yy=760;
    elements.push(group('prop_chair',rect(cx-50,yy-203,165,199,'#8c6952',12)+rect(cx-64,yy,195,19,'#a17e61',7)+path(`M ${n(cx-45)} ${yy+15} L ${n(cx-52)} 941 M ${n(cx+105)} ${yy+15} L ${n(cx+119)} 941`,'none','#76583f',13)));
  }
  if(s.prop==='motorcycle'){
    const wheels=[200,600],wy=882,rr=65,phase=s.wheelPhase||0;
    let bike='';for(const x of wheels){bike+=ell(x,wy,rr,rr,'#29353d')+ell(x,wy,rr-12,rr-12,'#a6bbc0')+ell(x,wy,9,9,'#354b55');for(let k=0;k<6;k++){const a=phase+k*Math.PI/3;bike+=line(`M ${x} ${wy} l ${n(Math.cos(a)*47)} ${n(Math.sin(a)*47)}`,'#526873',3)}}
    bike+=path('M 200 882 L 315 752 L 440 867 L 600 882 L 520 731 L 490 578','none','#657f88',13)+path('M 290 748 Q 390 714 491 738 L 442 831 Q 365 838 309 787 Z','#57878a','#345b62',3)+rect(273,692,126,24,'#3d4b53',9)+line('M 470 570 H 535 M 470 853 H 539','#394f58',8)+ell(526,665,24,32,'#f1d395','stroke="#59737b" stroke-width="5"');
    elements.push(group('prop_motorcycle',bike));
  }
  if(s.prop==='meal')elements.push(group('prop_meal_table',rect(400,655,265,16,'#b18b63',5)+line('M 415 671 V 943 M 649 671 V 943','#7e6a54',10)+ell(488,642,49,10,'#f4ede0','stroke="#738e8c" stroke-width="2"')+ell(488,638,31,6,'#b6c790')+rect(574,609,32,39,'#f4eee1',5)));
  body.push(leg('right'),leg('left'));
  if(skirt)body.push(clothCage(916,grad('trouser'),legInk,'skirt',528));
  const far=s.view==='three_quarter'?'right':'left',near=far==='left'?'right':'left';
  body.push(arm(far,'upper'));
  body.push(group('neck_art',groups.neck||'',`transform="${torsoMatrix}"`));
  if(hem>570)body.push(clothCage(hem,grad('cloth'),outline,'top_lower',555,isDress?1.07:1));
  if(isSamping)body.push(clothCage(714,accent,tint(accent,-.26),'samping',552,.87));
  body.push(group('body_upper',upper,`transform="${torsoMatrix}"`));
  body.push(arm(near,'upper'));
  // Head follows torso; upper arms do not inherit body rotation because their angles are global.
  body.push(group('head_follow',head,`transform="${torsoMatrix}"`));
  body.push(arm(far,'lower'),arm(near,'lower'));
  // Simple original props use wrist anchors and do not introduce external artwork.
  const W1=p.wrist_left,W2=p.wrist_right,C=mid(W1,W2);
  if(s.prop==='phone'){
    const right=s.propAttachment==='right_hand'||s.handRight==='grip',low=s.propAttachment==='scene_low';
    const W=low?[Number.isFinite(s.propX)?s.propX-s.rootX:550-s.rootX,Number.isFinite(s.propY)?s.propY-s.rootY:635-s.rootY]:right?W2:W1,A=Number.isFinite(s.propAngle)?s.propAngle:low?0:right?s.rightForearm:s.leftForearm;
    body.push(group('prop_phone',rect(-21,0,42,75,'#303a40',7,'stroke="#17252c" stroke-width="2"')+rect(-16,8,32,53,'#b8d4d4',3)+ell(0,68,2.5,2.5,'#9eafaf'),`transform="translate(${xy(W)}) rotate(${n(-A)})"`));
  }else if(s.prop==='book'){
    const lx=Math.min(W1[0],W2[0])-8,rx=Math.max(W1[0],W2[0])+8,yy=Math.min(W1[1],W2[1])-8,mx=(lx+rx)/2,h=clamp((rx-lx)*.44,65,112);
    body.push(group('prop_book',path(`M ${n(lx)} ${n(yy)} Q ${n((lx+mx)/2)} ${n(yy-14)} ${n(mx)} ${n(yy+6)} Q ${n((mx+rx)/2)} ${n(yy-14)} ${n(rx)} ${n(yy)} L ${n(rx-3)} ${n(yy+h)} Q ${n((mx+rx)/2)} ${n(yy+h-18)} ${n(mx)} ${n(yy+h+5)} Q ${n((lx+mx)/2)} ${n(yy+h-18)} ${n(lx+3)} ${n(yy+h)} Z`,'#fcf3dd','#6b837d',2)+line(`M ${n(mx)} ${n(yy+6)} L ${n(mx)} ${n(yy+h+5)}`,'#9d9a85',2)));
  }else if(s.prop==='box'){
    const low=s.propAttachment==='scene_low',cx=low?(Number.isFinite(s.propX)?s.propX-s.rootX:300-s.rootX):C[0],yy=low?(Number.isFinite(s.propY)?s.propY-s.rootY:615-s.rootY):Math.min(W1[1],W2[1])-6;
    const w=low?170:Math.max(170,Math.abs(W1[0]-W2[0])+16),hh=clamp(w*.62,90,150);
    body.push(group('prop_box',rect(cx-w/2,yy,w,hh,'#b8956d',3,'stroke="#8e704e" stroke-width="2"')+rect(cx-11,yy,22,hh,'#d7c2a1')+line(`M ${n(cx-w/2)} ${n(yy+22)} H ${n(cx+w/2)}`,'#95734c',2)));
  }else if(s.prop==='laptop'){
    const fixedDesk=s.propAttachment==='desk',anchorX=Number.isFinite(s.propX)?s.propX:460,anchorY=Number.isFinite(s.propY)?s.propY:650;
    const left=fixedDesk?anchorX-45-s.rootX:Math.min(W1[0],W2[0])-12,yy=fixedDesk?anchorY+12-s.rootY:Math.max(W1[1],W2[1])+12,right=fixedDesk?anchorX+170-s.rootX:Math.max(W1[0],W2[0])+160;
    const deskY=yy+18,deskLeft=left-35,deskRight=right+25;
    if(s.propAttachment==='desk')elements.push(group('prop_desk',rect(deskLeft+s.rootX,deskY+s.rootY,deskRight-deskLeft,16,'#aa8b65',5)+path(`M ${n(deskLeft+s.rootX+13)} ${n(deskY+s.rootY+14)} V 943 M ${n(deskRight+s.rootX-13)} ${n(deskY+s.rootY+14)} V 943`,'none','#7e7262',11)));
    body.push(group('prop_laptop',path(`M ${n(left)} ${n(yy)} H ${n(right)} l 6 10 H ${n(left-9)} Z`,'#7a8e99','#354d5c',1.5)+path(`M ${n(right-10)} ${n(yy)} L ${n(right-31)} ${n(yy-104)} Q ${n(right-28)} ${n(yy-111)} ${n(right-22)} ${n(yy-108)} L ${n(right+2)} ${n(yy-1)} Z`,'#526674','#354d5c',2)+line(`M ${n(left+12)} ${n(yy+3)} H ${n(right-23)}`,'#c5d9dc',2)));
  }
  if(s.prop==='meal'){
    const W=W2,angle=s.rightForearm;
    body.push(group('prop_utensil',s.mealUtensil==='cup'?rect(-18,-25,36,45,'#f5eee1',6)+path('M 18 -15 Q 41 -18 36 6 Q 31 18 18 12','none','#d5c9ae',5):line('M 0 0 L 0 53','#b6c4ca',5)+ell(0,59,9,13,'#cbd5d7'),`transform="translate(${xy(W)}) rotate(${n(-angle)})"`));
  }
  if(s.lanyard)body.push(group('lanyard',line('M 278 246 L 300 410 L 326 246','#536d75',5)+rect(277,407,47,64,'#f8efdc',5,'stroke="#536d75" stroke-width="2"')+rect(283,432,35,4,'#a1b4b4',2)));
  body.push(hand(far),hand(near));
  if(opts.guides)body.push(group('guides',Object.entries(p).map(([key,P])=>ell(P[0],P[1],3.3,3.3,'#dc4970')+`<text x="${n(P[0]+5)}" y="${n(P[1]-4)}" font-family="sans-serif" font-size="8" fill="#9b2840">${esc(key)}</text>`).join('')));
  elements.push(group('rig_root',body.join(''),`transform="translate(${n(s.rootX)} ${n(s.rootY)})"`));
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${n(opts.width||600)}" height="${n(opts.height||1000)}" viewBox="${vb.join(' ')}" role="img" aria-labelledby="${prefix}_title"><title id="${prefix}_title">${esc(c.name)} · articulated ${esc(s.view)}</title><metadata>${esc(JSON.stringify({character_id:c.id,rig_version:'3.0',external_assets:false,state:s}))}</metadata>${defs}${s.turnScaleX?'<g transform="translate(300 0) scale('+n(s.turnScaleX)+' 1) translate(-300 0)">':''}${s.flipX?'<g transform="translate(600 0) scale(-1 1)">':''}${elements.join('')}${s.flipX?'</g>':''}${s.turnScaleX?'</g>':''}</svg>`;
}
module.exports={rigSvg,rigGeometry,defaultState,solveTwoBone};
