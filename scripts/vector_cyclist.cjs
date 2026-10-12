#!/usr/bin/env node
'use strict';
/** Original SVG artwork and constrained cycling rig. Node, sharp and FFmpeg.
 * All pose/world state is a pure function of t; no wall-clock animation.
 * This is a separate proof renderer, not an entry in the 137-preset atlas.
 */
const fs = require('node:fs');
const path = require('node:path');
const {spawn} = require('node:child_process');
const {once} = require('node:events');

const TAU = Math.PI * 2;
const DEFAULT = Object.freeze({duration:8, fps:60, width:1280, cadence:.82,
  gear:1.35, phase:.45, jersey:'#234c60', accent:'#dc8156', skyTop:'#426272',
  skyBottom:'#e8c4a0', seed:17, supersample:1.5});
const f = n => Number(n.toFixed(3));
const point = p => `${f(p.x)},${f(p.y)}`;
const polar = (c,r,a) => ({x:c.x+r*Math.cos(a),y:c.y+r*Math.sin(a)});
const dist = (a,b) => Math.hypot(a.x-b.x,a.y-b.y);
function rotate(p,a) { return {x:p.x*Math.cos(a)-p.y*Math.sin(a),y:p.x*Math.sin(a)+p.y*Math.cos(a)}; }
const mod = (a,b) => ((a % b) + b) % b;
function configuration(raw={}) {
  const c={...DEFAULT,...raw};
  for (const k of ['duration','fps','width','cadence','gear','phase','seed','supersample'])
    if (typeof c[k]!=='number' || !Number.isFinite(c[k])) throw Error(`${k} must be finite`);
  if (!(c.duration>0 && c.duration<=120)) throw Error('duration: 0..120 seconds');
  if (![24,30,60].includes(c.fps)) throw Error('fps: 24, 30 or 60');
  if (!Number.isInteger(c.width) || c.width<640 || c.width>2560 || c.width%32) throw Error('width: 640..2560, divisible by 32');
  if (!(c.cadence>=.25 && c.cadence<=1.8 && c.gear>=.5 && c.gear<=3)) throw Error('cadence: .25..1.8; gear: .5..3');
  if (!(c.supersample>=1 && c.supersample<=2)) throw Error('supersample: 1..2');
  for (const k of ['jersey','accent','skyTop','skyBottom']) if (!/^#[0-9a-f]{6}$/i.test(c[k])) throw Error(`${k}: #RRGGBB`);
  return c;
}

/** Circle-intersection IK. Refuse unreachable targets rather than stretch. */
function twoBone(root,target,a,b,side=-1) {
  const d=dist(root,target);
  if (d<Math.abs(a-b)+1e-8 || d>a+b-1e-8) throw Error('Unreachable IK target');
  const ux=(target.x-root.x)/d, uy=(target.y-root.y)/d;
  const along=(a*a-b*b+d*d)/(2*d), h=Math.sqrt(Math.max(0,a*a-along*along));
  return {x:root.x+ux*along-side*uy*h,y:root.y+uy*along+side*ux*h};
}

function state(t,c) {
  const theta=c.phase+TAU*c.cadence*t;
  const crank={x:605,y:473};
  const hip={x:558+.65*Math.sin(theta),y:332+.85*Math.sin(theta*2)};
  const shoulder={x:683+.55*Math.sin(theta*2+.4),y:260+.7*Math.sin(theta*2)};
  const armRoot={x:shoulder.x+8,y:shoulder.y+12};
  const hand={x:809,y:348};
  function leg(angle) {
    const pedal=polar(crank,40,angle);
    const footAngle=(-5+7*Math.sin(angle))*Math.PI/180;
    const local=rotate({x:-16,y:-19},footAngle);
    const ankle={x:pedal.x+local.x,y:pedal.y+local.y};
    const knee=twoBone(hip,ankle,102,103,-1);
    return {pedal,ankle,knee,footAngle};
  }
  const omega=TAU*c.cadence*c.gear, roadSpeed=omega*101;
  return {t,theta,crank,hip,shoulder,armRoot,hand,elbow:twoBone(armRoot,hand,78,84,1),
    near:leg(theta),far:leg(theta+Math.PI),wheel:omega*t,roadSpeed,
    // Head follows the shoulder, never the wheel or a global random wobble.
    head:{x:shoulder.x+45,y:shoulder.y-42}};
}

function line(a,b,color,width,extra='') {
  return `<path d="M${point(a)} L${point(b)}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" ${extra}/>`;
}
function terrain(t,base,amp,period,speed,phase,fill) {
  const pts=[];
  for(let x=-24;x<=1304;x+=16) {
    const w=(x+t*speed)/period*TAU+phase;
    const y=base+amp*(.60*Math.sin(w)+.26*Math.sin(w*3+.5)+.14*Math.sin(w*5-1));
    pts.push({x,y});
  }
  return `<path d="M-24,585 L${pts.map(point).join(' L')} L1304,585 Z" fill="${fill}"/>`;
}
function repeat(t,speed,spacing,draw) {
  const travel=t*speed,offset=mod(travel,spacing),cell=Math.floor(travel/spacing);
  let out='';
  for(let i=-2;i<=Math.ceil(1280/spacing)+2;i++) out+=draw(i*spacing-offset,i+cell);
  return out;
}

function environment(t,c,s) {
  let out=`<rect width="1280" height="720" fill="url(#sky)"/>
  <circle cx="232" cy="183" r="150" fill="url(#sunHalo)"/>
  <circle cx="232" cy="183" r="26" fill="#fff0c4"/>
  <path d="M75 222 Q174 207 330 222 Q240 232 75 222 M721 121 Q858 106 1058 120 Q919 135 721 121" fill="#ebd4b9" opacity=".09"/>`;
  out+=terrain(t,396,72,1660,s.roadSpeed*.022,.6,'#9caaae');
  out+=terrain(t,438,47,1190,s.roadSpeed*.053,2.3,'#7f989b');
  out+=terrain(t,477,35,950,s.roadSpeed*.10,-1,'#567d7e');
  out+=`<rect x="0" y="483" width="1280" height="92" fill="url(#meadow)"/>
  <path d="M0 495 Q317 473 680 496 Q1031 514 1280 491 L1280 506 Q940 530 533 506 Q270 496 0 510Z" fill="#b6b998" opacity=".65"/>`;
  out+=repeat(t,s.roadSpeed*.15,146,(x,i)=>{
    const y=481+5*Math.sin(i*1.9+c.seed), size=14+3*Math.sin(i*2.1);
    return `<g opacity=".75" fill="#496965"><path d="M${f(x)} ${f(y)} l${f(size*.43)} ${f(-size*1.9)} l${f(size*.43)} ${f(size*1.9)}Z"/><path d="M${f(x+17)} ${f(y+1)} l6 -23 l6 23Z"/></g>`;
  });
  out+=repeat(t,s.roadSpeed*.19,580,(x)=>`<g opacity=".62" stroke="#b9cdc5" fill="none" stroke-width="2"><path d="M${f(x)} 476V426"/><g transform="translate(${f(x)} 426) rotate(${f(t*21)})"><path d="M0 0L0 -21 M0 0L18 10 M0 0L-18 10"/></g></g>`);
  out+=repeat(t,s.roadSpeed*.38,91,(x)=>`<path d="M${f(x)} 542V569" stroke="#6a7d69" stroke-width="2" opacity=".5"/>`);
  out+=`<path d="M0 551H1280 M0 560H1280" stroke="#78866f" stroke-width="1.6" opacity=".53"/>`;
  out+=repeat(t,s.roadSpeed*.43,930,(x)=>`<g opacity=".52" stroke="#536965" fill="none"><path d="M${f(x)} 558V368" stroke-width="3"/><path d="M${f(x-22)} 382H${f(x+22)} M${f(x-15)} 375V385 M${f(x+15)} 375V385" stroke-width="2"/><path d="M${f(x)} 382Q${f(x+465)} 411 ${f(x+930)} 382" stroke-width="1.2"/></g>`);
  out+=`<rect x="0" y="570" width="1280" height="10" fill="#bdbea5"/>
  <rect x="0" y="580" width="1280" height="140" fill="url(#road)"/>
  <path d="M0 588H1280" stroke="#ddd5b8" stroke-width="3" opacity=".7"/>`;
  out+=repeat(t,s.roadSpeed,560,(x)=>`<path d="M${f(x)} 677H${f(x+235)}" stroke="#dddcc5" stroke-width="5" opacity=".85"/>`);
  return out;
}

function wheel(cx,angle) {
  const a=angle*180/Math.PI;
  return `<g transform="translate(${cx} 484)">
  <ellipse cy="104" rx="112" ry="9" fill="url(#contact)"/>
  <circle r="102" fill="#17292e"/><circle r="97" fill="url(#wheelDisc)" stroke="#b7c7bc" stroke-width="2.3"/>
  <circle r="92" fill="none" stroke="#617e7b" stroke-width="1" opacity=".7"/>
  <g transform="rotate(${f(a)})" opacity=".26"><path d="M0 0L-72 -51Q-12 -78 76 -47Z" fill="#667b7b"/>
  <path d="M0 0L-10 87Q40 63 75 39Z" fill="#0d252b"/>
  <path d="M13 -89A90 90 0 0 1 46 -77" fill="none" stroke="#d4dfce" stroke-width="2"/></g>
  <circle r="17" fill="none" stroke="#8ca4a0" stroke-width="1.5"/><circle r="10" fill="#8da6a0"/>
  <circle r="5" fill="#425f60"/></g>`;
}

function shoe(leg,near) {
  return `<g transform="translate(${point(leg.pedal)}) rotate(${f(leg.footAngle*180/Math.PI)})">
  <path d="M-25 -23L-12 -22L-8 -13Q7 -11 26 -5Q31 -2 28 2L-30 2Q-35 -5 -25 -23Z" fill="${near?'#f0eee0':'#bbcdc2'}"/>
  <path d="M-30 2H27" stroke="#859c91" stroke-width="3"/>
  <path d="M-5 -10L2 -5 M2 -9L9 -4 M9 -7L16 -3" stroke="#899e98" stroke-width="1.5"/>
  </g>`;
}
function legShape(s,leg,near) {
  const skin=near?'#d7aa83':'#ac8a70';
  return line(s.hip,leg.knee,skin,29)+
    line(leg.knee,leg.ankle,skin,21)+
    `<circle cx="${f(leg.knee.x)}" cy="${f(leg.knee.y)}" r="14" fill="${skin}"/>`+
    line({x:leg.knee.x+3,y:leg.knee.y+4},leg.ankle,near?'#e9bf98':'#c19c7f',8,'opacity=".48"')+
    line({x:leg.ankle.x+3,y:leg.ankle.y-12},leg.ankle,near?'#edeee1':'#bacabf',19)+shoe(leg,near);
}

function bicycle(s,c) {
  const A={x:439,y:484}, B={x:833,y:484}, C=s.crank, S={x:539,y:350}, H={x:788,y:351}, HB={x:797,y:390};
  let out=`<g stroke-linejoin="round">`;
  // Frame tubes have a dark edge and a narrow reflective centre.
  for(const [a,b] of [[A,S],[A,C],[S,C],[S,H],[HB,C],[H,HB],[HB,B]])
    out+=line(a,b,'#305963',9)+line(a,b,'#a9cbc1',5)+line({x:a.x,y:a.y-1},{x:b.x,y:b.y-1},'#deead9',1,'opacity=".75"');
  out+=line({x:539,y:351},{x:531,y:332},'#aecbc1',5)+
    `<path d="M511 332Q526 325 550 329Q562 330 562 335L523 339Z" fill="#253c40"/>
    <path d="M788 351L787 336L801 334Q826 338 826 352Q826 365 816 369" fill="none" stroke="#243a3e" stroke-width="6" stroke-linecap="round"/>
    <path d="M790 348Q745 367 787 418" fill="none" stroke="#506f70" stroke-width="1.2"/>
    <path d="M449 474L605 454M449 494L605 492" fill="none" stroke="#b5c1aa" stroke-width="2.5"/>
    <circle cx="605" cy="473" r="22" fill="#bdc7b4" stroke="#46645e" stroke-width="2"/>
    <g transform="translate(605 473) rotate(${f(s.theta*180/Math.PI)})">`;
  for(let i=0;i<5;i++) out+=`<path d="M6 -3L17 -9L17 -2L8 4Z" transform="rotate(${i*72})" fill="#46615d"/>`;
  out+=`<circle r="5" fill="#2b484b"/></g>`;
  out+=line(s.far.pedal,C,'#698582',5)+line(C,s.near.pedal,'#d0d8be',5);
  for(const leg of [s.far,s.near]) out+=line({x:leg.pedal.x-13,y:leg.pedal.y+2},{x:leg.pedal.x+13,y:leg.pedal.y+2},'#273f41',5);
  out+=`<g transform="translate(670 417) rotate(31)"><rect x="-8" y="-26" width="16" height="44" rx="4" fill="#e5e8d8"/><rect x="-8" y="-7" width="16" height="9" fill="${c.accent}"/><rect x="-5" y="-31" width="10" height="7" rx="2" fill="#405e5d"/></g></g>`;
  return out;
}

function rider(s,c) {
  const dx=s.hip.x-558,dy=s.hip.y-332;
  // Clothing contours cover the upper thigh roots; limbs remain independently rigged.
  let out=line({x:s.shoulder.x+14,y:s.shoulder.y+6},{x:s.head.x-19,y:s.head.y+23},'#cba17e',17)+`<g transform="translate(${f(dx)} ${f(dy)})">
  <path d="M550 329Q558 303 607 278Q648 249 681 251Q696 252 706 267L687 288Q657 281 627 308L574 349Z" fill="url(#jersey)"/>
  <path d="M551 330Q559 304 607 278Q649 252 680 253" fill="none" stroke="#527784" stroke-width="2" opacity=".7"/>
  <path d="M556 329L583 340L598 367Q582 381 563 373L542 354Q531 340 540 332Z" fill="#243940"/>
  <path d="M567 367L592 359" stroke="${c.accent}" stroke-width="6"/>
  <path d="M661 261Q677 250 692 257L705 269L687 288L668 279Z" fill="${c.accent}"/>
  </g>`;
  out+=legShape(s,s.near,true);
  // Redraw the near short over the root of the thigh, ending at a physical cuff.
  const thighEnd={x:s.hip.x+(s.near.knee.x-s.hip.x)*.33,y:s.hip.y+(s.near.knee.y-s.hip.y)*.33};
  out+=line(s.hip,thighEnd,'#233b42',38)+line({x:thighEnd.x-6,y:thighEnd.y-3},{x:thighEnd.x+9,y:thighEnd.y+1},c.accent,3);
  out+=line(s.armRoot,s.elbow,'#d2a581',22)+
    line(s.elbow,s.hand,'#dbb28d',17)+
    line({x:s.elbow.x+3,y:s.elbow.y-3},{x:s.hand.x-8,y:s.hand.y-4},'#eac39c',5,'opacity=".45"')+
    `<circle cx="${f(s.hand.x)}" cy="${f(s.hand.y)}" r="8.5" fill="${c.accent}"/>
    <path d="M${f(s.hand.x-5)} ${f(s.hand.y+3)}l11 3" stroke="#213b3f" stroke-width="5" stroke-linecap="round"/>`;
  const h=s.head;
  out+=`<g transform="translate(${point(h)}) rotate(16)">
  <path d="M-19 12L-26 34L-10 41L-1 23Z" fill="#c69b78"/>
  <path d="M-26 -7Q-30 9 -19 24Q-7 34 9 25L18 16L24 12L19 6Q19 -16 1 -23Q-17 -27 -26 -7Z" fill="url(#skin)"/>
  <path d="M-29 -8Q-29 -34 0 -34Q27 -33 32 -11L23 -5Q-3 -14 -29 -8Z" fill="#eae8d6"/>
  <path d="M-29 -9Q-4 -17 31 -10" stroke="#b6c7bc" stroke-width="3" fill="none"/>
  <path d="M-17 -12Q-14 -28 -3 -31 M-4 -14Q0 -28 8 -30 M10 -13Q15 -23 19 -26" stroke="#3c5557" stroke-width="4.5" fill="none" stroke-linecap="round"/>
  <path d="M-6 -1L22 0L18 9L2 8Z" fill="#203a46"/>
  <path d="M2 2L16 2" stroke="#789298" stroke-width="1.5"/>
  <ellipse cx="-10" cy="9" rx="4.2" ry="6" fill="#ddb28d"/>
  <path d="M-19 -6L-11 22L6 26L16 -3" fill="none" stroke="#677469" stroke-width="1.5"/>
  </g>`;
  return out;
}

function frameSvg(t,raw={}) {
  const c=configuration(raw),s=state(t,c);
  const defs=`<defs>
  <linearGradient id="sky" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="510"><stop stop-color="${c.skyTop}"/><stop offset=".5" stop-color="#9daba9"/><stop offset="1" stop-color="${c.skyBottom}"/></linearGradient>
  <radialGradient id="sunHalo"><stop stop-color="#ffeeae" stop-opacity=".31"/><stop offset=".34" stop-color="#f2deb0" stop-opacity=".17"/><stop offset="1" stop-color="#f2deb0" stop-opacity="0"/></radialGradient>
  <linearGradient id="meadow" x2="0" y2="1"><stop stop-color="#a4ae90"/><stop offset="1" stop-color="#85997b"/></linearGradient>
  <linearGradient id="road" x2="0" y2="1"><stop stop-color="#3a5356"/><stop offset="1" stop-color="#203c43"/></linearGradient>
  <radialGradient id="wheelDisc" cx=".35" cy=".3" r=".8"><stop stop-color="#354c50"/><stop offset="1" stop-color="#192f36"/></radialGradient>
  <radialGradient id="contact"><stop stop-color="#112b2e" stop-opacity=".53"/><stop offset="1" stop-color="#112b2e" stop-opacity="0"/></radialGradient>
  <linearGradient id="jersey" x2=".8" y2="1"><stop stop-color="#477180"/><stop offset=".5" stop-color="${c.jersey}"/><stop offset="1" stop-color="#1c3e4d"/></linearGradient>
  <linearGradient id="skin" x2="1" y2="1"><stop stop-color="#eac19a"/><stop offset="1" stop-color="#cea37e"/></linearGradient>
  <radialGradient id="vignette" r=".72"><stop offset=".44" stop-color="#102c36" stop-opacity="0"/><stop offset="1" stop-color="#102c36" stop-opacity=".23"/></radialGradient>
  </defs>`;
  let body=environment(t,c,s)+wheel(439,s.wheel)+wheel(833,s.wheel)+legShape(s,s.far,false)+bicycle(s,c)+rider(s,c);
  body+=`<rect width="1280" height="720" fill="url(#vignette)" pointer-events="none"/>`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">${defs}${body}</svg>`;
}

/** Geometry QA reports mechanisms, not an aesthetic score. */
function audit(raw={}) {
  const c=configuration(raw),n=Math.round(c.duration*c.fps);
  let maxBoneError=0,maxContactError=0,minKneeAngle=180,maxKneeAngle=0,maxJointStep=0;
  let previous;
  for(let i=0;i<n;i++) {
    const s=state(i/c.fps,c);
    maxBoneError=Math.max(maxBoneError,Math.abs(dist(s.armRoot,s.elbow)-78),Math.abs(dist(s.elbow,s.hand)-84));
    for(const l of [s.near,s.far]) {
      maxBoneError=Math.max(maxBoneError,Math.abs(dist(s.hip,l.knee)-102),Math.abs(dist(l.knee,l.ankle)-103));
      const sock=rotate({x:-16,y:-19},l.footAngle);
      maxContactError=Math.max(maxContactError,Math.hypot(l.ankle.x-l.pedal.x-sock.x,l.ankle.y-l.pedal.y-sock.y));
      const angle=Math.acos(Math.max(-1,Math.min(1,(102**2+103**2-dist(s.hip,l.ankle)**2)/(2*102*103))))*180/Math.PI;
      minKneeAngle=Math.min(minKneeAngle,angle);maxKneeAngle=Math.max(maxKneeAngle,angle);
    }
    if(previous) maxJointStep=Math.max(maxJointStep,dist(previous.near.knee,s.near.knee),dist(previous.near.ankle,s.near.ankle));
    previous=s;
  }
  const s0=state(0,c),s1=state(c.duration,c);
  const cyclePeriod=1/c.cadence,p0=state(0,c),p1=state(cyclePeriod,c);
  return {frames:n,fps:c.fps,source:'original SVG, continuous-time rig',maxBoneErrorPx:maxBoneError,
    maxShoePedalContactErrorPx:maxContactError,maxJointStepPx:maxJointStep,kneeAngleRangeDeg:[minKneeAngle,maxKneeAngle],
    wheelRoadResidualPx:Math.abs((s1.wheel-s0.wheel)*101-s1.roadSpeed*c.duration),
    poseCycleResidualPx:dist(p0.near.ankle,p1.near.ankle),
    geometryPass:maxBoneError<1e-6&&maxContactError<1e-6,
    note:'60 fps is independently evaluated per frame; normal-speed visual playback still required.'};
}

async function sharpModule() {
  try {return require('sharp');} catch(e) {
    const root=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
    if(!root) throw Error('sharp unavailable; install in the project or set CODEX_PRIMARY_RUNTIME_NODE_MODULES');
    return require(require.resolve('sharp',{paths:[root]}));
  }
}
async function render(raw,output) {
  const c=configuration(raw),sharp=await sharpModule(),height=c.width*9/16,n=Math.round(c.duration*c.fps);
  fs.mkdirSync(path.dirname(output),{recursive:true});
  const proc=spawn('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',`${c.width}x${height}`,'-r',String(c.fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart',output],{stdio:['pipe','inherit','inherit']});
  const completed=new Promise((resolve,reject)=>{proc.on('error',reject);proc.on('close',code=>code===0?resolve():reject(Error(`FFmpeg exited ${code}`)));});
  // Mark rejection handled while frames are rendering; await it below.
  completed.catch(()=>{});
  proc.stdin.on('error',()=>{});
  try {
    for(let i=0;i<n;i++) {
      const buf=await sharp(Buffer.from(frameSvg(i/c.fps,c)),{density:72*c.supersample}).resize(c.width,height).flatten({background:'#203c43'}).removeAlpha().raw().toBuffer();
      if(!proc.stdin.write(buf)) await Promise.race([once(proc.stdin,'drain'),completed.then(()=>{throw Error('FFmpeg ended before frames');})]);
      if(i%(c.fps*2)===0) console.error(`frame ${i}/${n}`);
    }
    proc.stdin.end();await completed;
  }catch(e){proc.kill();throw e;}
  const report={configuration:c,...audit(c)};
  fs.writeFileSync(output.replace(/\.[^.]+$/,'')+'.qa.json',JSON.stringify(report,null,2));
  console.log(JSON.stringify({output,frames:n,duration:n/c.fps,...audit(c)}));
}
async function main() {
  const args=process.argv.slice(2);let raw={},output='vector-cyclist.mp4',at=null,isAudit=false;
  for(let i=0;i<args.length;i++) {
    const a=args[i];
    if(a==='--config') raw={...raw,...JSON.parse(fs.readFileSync(args[++i],'utf8'))};
    else if(a==='--output') output=args[++i];
    else if(a==='--frame') at=Number(args[++i]);
    else if(a==='--audit') isAudit=true;
    else if(a==='--help'){console.log('node vector_cyclist.cjs --config config.json --output proof.mp4 [--frame SECONDS | --audit]');return;}
    else if(['--duration','--fps','--width'].includes(a)) raw[a.slice(2)]=Number(args[++i]);
    else throw Error('Unknown argument '+a);
  }
  const c=configuration(raw);
  if(isAudit){console.log(JSON.stringify(audit(c),null,2));return;}
  if(at!==null) {
    if(!Number.isFinite(at)||at<0||at>c.duration) throw Error('frame time out of range');
    fs.mkdirSync(path.dirname(output),{recursive:true});
    const svg=frameSvg(at,c);
    if(path.extname(output).toLowerCase()==='.svg') fs.writeFileSync(output,svg);
    else {const sharp=await sharpModule();await sharp(Buffer.from(svg),{density:72*c.supersample}).resize(c.width,c.width*9/16).png().toFile(output);}
    return;
  }
  if(path.extname(output).toLowerCase()!=='.mp4') throw Error('video output must be .mp4');
  await render(c,path.resolve(output));
}
module.exports={configuration,state,twoBone,frameSvg,audit,render};
if(require.main===module) main().catch(e=>{console.error(e.message);process.exitCode=1;});
