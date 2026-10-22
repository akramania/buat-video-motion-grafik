/* Original deterministic adapters for selected Kelas Multimedia Python presets.
 * Caller owns GSAP, loading, composition registration and final timeline duration.
 * No timers, independent ticker, media control or network calls.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.KMMotion = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const finite = (v, label) => { if (!Number.isFinite(v)) throw Error(label + ' must be finite'); return v; };
  const clamp = (v, a=0, b=1) => Math.max(a, Math.min(b, v));
  const mix = (a,b,p) => a+(b-a)*p;
  const progress = (t,a,b) => b>a ? clamp((t-a)/(b-a)) : Number(t>=b);
  const cubicOut = p => 1-(1-clamp(p))**3;
  const smooth = p => { p=clamp(p); return p*p*(3-2*p); };
  const pop = p => { p=clamp(p); return 1-(1-p)**3*Math.cos(p*Math.PI*2.8); };
  const PORTS = Object.freeze({
    'JS:T01': {sourceId:'T01', source:'assets/motion_presets/typography.py:masked_words', mechanism:'fixed mask with staggered whole-word rise and exit'},
    'JS:B04': {sourceId:'B04', source:'assets/motion_presets/new_b.py:_b04', mechanism:'exact finite numeric counter with measured marker sweep'},
    'JS:X02': {sourceId:'X02', source:'assets/motion_presets/typography.py:bar_underline', mechanism:'text wipe leading bar compresses into underline'}
  });
  function timebase(config={}) {
    const start=finite(config.start ?? 0,'start'), duration=finite(config.duration ?? 5,'duration');
    if (start<0 || duration<=0) throw Error('start >= 0 and duration > 0 required');
    return {start,duration,at:v=>start+v*duration/5,span:v=>v*duration/5};
  }
  function nodes(value) {
    if (typeof value==='string') throw Error('Pass measured element(s), not selector text');
    if (!value) throw Error('Target required');
    return Array.isArray(value) ? value : typeof value.length==='number' && !value.nodeType ? Array.from(value) : [value];
  }
  function entranceHoldExit(tl, target, config={}) {
    const list=nodes(target), start=finite(config.start ?? 0,'start');
    const enterDuration=finite(config.enterDuration ?? .55,'enterDuration');
    const exitDuration=finite(config.exitDuration ?? .35,'exitDuration');
    const anticipation=finite(config.anticipation ?? .09,'anticipation');
    const follow=finite(config.followThrough ?? .12,'followThrough');
    const stagger=finite(config.stagger ?? .06,'stagger');
    const holdUntil=finite(config.holdUntil ?? 3,'holdUntil');
    const distance=finite(config.distance ?? 38,'distance');
    const mode=config.mode ?? 'up';
    if (!['up','left','pop'].includes(mode)) throw Error('Unknown entrance mode');
    if (start<0 || enterDuration<=0 || exitDuration<=0 || anticipation<0 || follow<0 || stagger<0) throw Error('Invalid finite motion timing');
    const entered=start+anticipation+enterDuration+follow+Math.max(0,list.length-1)*stagger;
    if (holdUntil<entered) throw Error('holdUntil overlaps entrance/follow-through');
    const axis=mode==='left'?'x':'y';
    list.forEach((el,i)=>{
      const s=start+i*stagger;
      const from={opacity:0, [axis]:distance, scale:mode==='pop'?.82:1};
      tl.set(el, from, s);
      if (anticipation>0) tl.fromTo(el,{[axis]:distance},{[axis]:distance*1.1,duration:anticipation,ease:'power2.in',immediateRender:false},s);
      tl.fromTo(el,{opacity:0,[axis]:distance*1.1,scale:mode==='pop'?.82:1},{opacity:1,[axis]:0,scale:1,duration:enterDuration,ease:config.ease ?? 'back.out(1.35)',immediateRender:false},s+anticipation);
      if (follow>0) tl.fromTo(el,{rotation:mode==='pop'?-1.2:0},{rotation:0,duration:follow,ease:'power2.out',immediateRender:false},s+anticipation+enterDuration);
      tl.fromTo(el,{opacity:1,[axis]:0,scale:1},{opacity:0,[axis]:-distance*.75,scale:mode==='pop'?.96:1,duration:exitDuration,ease:'power2.in',immediateRender:false},holdUntil+i*stagger);
    });
    return {start,entranceEnd:entered,holdUntil,end:holdUntil+(list.length-1)*stagger+exitDuration};
  }
  function sampleT01(t,index=0,count=1) {
    const n=Math.max(1,count), s=.17+index*Math.min(.085,.5/Math.max(1,n-1));
    const ex=4.15+index*Math.min(.025,.15/Math.max(1,n-1));
    const a=cubicOut(progress(t,s,s+.54)), q=smooth(progress(t,ex,ex+.53));
    return {yEm:(1-a)-q,opacity:a*(1-q),reveal:a};
  }
  function maskedWords(tl, target, config={}) {
    const list=nodes(target), {at,span,start,duration}=timebase(config), n=list.length;
    const step=Math.min(.085,.5/Math.max(1,n-1)), exStep=Math.min(.025,.15/Math.max(1,n-1));
    list.forEach((el,i)=>{
      tl.set(el,{yPercent:100,opacity:0},start);
      tl.fromTo(el,{yPercent:100,opacity:0},{yPercent:0,opacity:1,duration:span(.54),ease:cubicOut,immediateRender:false},at(.17+i*step));
      tl.fromTo(el,{yPercent:0,opacity:1},{yPercent:-100,opacity:0,duration:span(.53),ease:smooth,immediateRender:false},at(4.15+i*exStep));
    });
    return {start,end:start+duration,sourceId:'T01'};
  }
  function sampleB04(t, config={}) {
    const a=finite(config.from ?? 0,'from'), b=finite(config.to ?? 100,'to');
    const q=smooth(progress(t,4.15,4.85)), v=cubicOut(progress(t,.75,3.35));
    return {value:v>=1?b:v<=0?a:mix(a,b,v),marker:cubicOut(progress(t,1.1,2.7))*(1-q),opacity:cubicOut(progress(t,.15,.8))*(1-q),y:-25*q};
  }
  function formatCounter(value, config={}) {
    const decimals=config.decimals ?? 0;
    if (!Number.isInteger(decimals) || decimals<0 || decimals>6) throw Error('decimals must be integer 0..6');
    return new Intl.NumberFormat(config.locale ?? 'en-MY',{minimumFractionDigits:decimals,maximumFractionDigits:decimals,useGrouping:config.grouping ?? true}).format(Number(value));
  }
  function metricMarker(tl, target, config={}) {
    const {group,counter,marker}=target;
    if (!group || !counter || !marker) throw Error('B04 targets: group, counter, marker');
    const {at,span,start,duration}=timebase(config), a=finite(config.from ?? 0,'from'), b=finite(config.to ?? 100,'to');
    formatCounter(a,config);
    tl.set(group,{opacity:0,y:0},start);
    tl.set(marker,{scaleX:0,transformOrigin:'0% 50%'},start);
    tl.set(counter,{textContent:formatCounter(a,config)},start);
    tl.fromTo(group,{opacity:0},{opacity:1,duration:span(.65),ease:cubicOut,immediateRender:false},at(.15));
    // Modifier is a render-time property setter, not an onUpdate event. It also runs when seek suppresses callbacks.
    tl.fromTo(counter,{textContent:a},{textContent:b,duration:span(2.6),ease:cubicOut,modifiers:{textContent:v=>formatCounter(v,config)},immediateRender:false},at(.75));
    tl.fromTo(marker,{scaleX:0},{scaleX:1,duration:span(1.6),ease:cubicOut,immediateRender:false},at(1.1));
    tl.fromTo(marker,{scaleX:1},{scaleX:0,duration:span(.7),ease:smooth,immediateRender:false},at(4.15));
    tl.fromTo(group,{opacity:1,y:0},{opacity:0,y:-25,duration:span(.7),ease:smooth,immediateRender:false},at(4.15));
    return {start,end:start+duration,sourceId:'B04'};
  }
  function sampleX02(t,width=600,textHeight=80) {
    finite(width,'width');finite(textHeight,'textHeight');
    const a=cubicOut(progress(t,.16,.94)), q=smooth(progress(t,4.15,4.85));
    const compress=progress(t,.78,1.12), widen=progress(t,.94,1.12);
    return {reveal:a,barX:mix(-width/2+width*a,0,widen),barY:mix(0,59,compress),barWidth:mix(15,width,widen),barHeight:mix(textHeight+24,5,compress),ruleReveal:1-smooth(progress(t,4.07,4.57)),opacity:1-q,y:-32*q};
  }
  function barUnderline(tl,target,config={}) {
    const {group,text,bar}=target;
    if (!group || !text || !bar) throw Error('X02 targets: group, text, bar');
    const {at,span,start,duration}=timebase(config), width=finite(config.width,'measured width'), height=finite(config.height,'measured height');
    if (width<=0 || height<=0) throw Error('Measure text after loading fonts');
    tl.set(group,{opacity:1,y:0},start);
    tl.set(text,{clipPath:'inset(0% 100% 0% 0%)'},start);
    tl.set(bar,{opacity:0,x:-width/2,y:0,width:15,height:height+24},start);
    tl.fromTo(text,{clipPath:'inset(0% 100% 0% 0%)'},{clipPath:'inset(0% 0% 0% 0%)',duration:span(.78),ease:cubicOut,immediateRender:false},at(.16));
    tl.fromTo(bar,{opacity:0},{opacity:1,duration:span(.17),ease:cubicOut,immediateRender:false},at(.15));
    tl.fromTo(bar,{x:-width/2},{x:width/2,duration:span(.78),ease:cubicOut,immediateRender:false},at(.16));
    tl.fromTo(bar,{height:height+24,y:0},{height:5,y:59,duration:span(.34),ease:'none',immediateRender:false},at(.78));
    tl.fromTo(bar,{width:15,x:width/2},{width:width,x:0,duration:span(.18),ease:'none',immediateRender:false},at(.94));
    tl.fromTo(bar,{scaleX:1},{scaleX:0,transformOrigin:'0% 50%',duration:span(.5),ease:smooth,immediateRender:false},at(4.07));
    tl.fromTo(group,{opacity:1,y:0},{opacity:0,y:-32,duration:span(.7),ease:smooth,immediateRender:false},at(4.15));
    return {start,end:start+duration,sourceId:'X02'};
  }
  function applyPreset(tl,id,target,config={}) {
    if (!tl || typeof tl.fromTo!=='function' || typeof tl.set!=='function') throw Error('Caller must supply a GSAP timeline');
    if (id==='JS:T01') return maskedWords(tl,target,config);
    if (id==='JS:B04') return metricMarker(tl,target,config);
    if (id==='JS:X02') return barUnderline(tl,target,config);
    throw Error('Unsupported adapter '+id+'; do not infer support for other Atlas presets');
  }
  function solveTwoBone(root,target,l1,l2,bend=1) {
    [root.x,root.y,target.x,target.y,l1,l2,bend].forEach(v=>finite(v,'IK input'));
    if (l1<=0 || l2<=0 || (bend!==1 && bend!==-1)) throw Error('IK lengths > 0; bend must be +1/-1');
    let dx=target.x-root.x,dy=target.y-root.y,requested=Math.hypot(dx,dy);
    const min=Math.abs(l1-l2)+1e-8,max=l1+l2-1e-8,d=clamp(requested,min,max);
    const direction=requested>1e-10?Math.atan2(dy,dx):0;
    const alpha=Math.acos(clamp((l1*l1+d*d-l2*l2)/(2*l1*d),-1,1));
    const upper=direction+bend*alpha, elbow={x:root.x+l1*Math.cos(upper),y:root.y+l1*Math.sin(upper)};
    const end={x:root.x+d*Math.cos(direction),y:root.y+d*Math.sin(direction)};
    const lowerWorld=Math.atan2(end.y-elbow.y,end.x-elbow.x);
    return {elbow,end,upperDegrees:upper*180/Math.PI,lowerLocalDegrees:(lowerWorld-upper)*180/Math.PI,reachable:requested>=Math.abs(l1-l2)&&requested<=l1+l2,requestedDistance:requested};
  }
  function svgPivot(gsap,element,x,y) {
    finite(x,'pivot x');finite(y,'pivot y');
    if (!gsap || typeof gsap.set!=='function') throw Error('GSAP required');
    gsap.set(element,{svgOrigin:x+' '+y,smoothOrigin:false});
  }
  return Object.freeze({PORTS,clamp,mix,progress,cubicOut,smooth,pop,timebase,entranceHoldExit,sampleT01,sampleB04,sampleX02,formatCounter,applyPreset,solveTwoBone,svgPivot});
});
