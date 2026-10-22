'use strict';
const assert=require('node:assert/strict');
const path=require('node:path');
const bank=require('./motion-bank.js');
const gsapPath=process.env.KM_GSAP_PATH || require.resolve('gsap/dist/gsap.js',{paths:[process.cwd(),__dirname]});
const {gsap}=require(path.resolve(gsapPath));
const close=(a,b,tolerance=1e-5)=>assert.ok(Math.abs(a-b)<tolerance,`${a} != ${b}`);
// Exact easing from the Python source; never use frame deltas or wall-clock.
assert.equal(bank.cubicOut(0),0);assert.equal(bank.cubicOut(1),1);
assert.equal(bank.pop(1),1);assert.equal(bank.sampleB04(5,{to:37000}).value,37000);
assert.equal(bank.sampleB04(-1,{to:37000}).value,0);
assert.equal(bank.sampleT01(0).opacity,0);assert.equal(bank.sampleT01(2).opacity,1);assert.equal(bank.sampleT01(5).opacity,0);
assert.equal(bank.sampleX02(2,600,80).barHeight,5);
assert.equal(bank.formatCounter(37000,{locale:'en-MY'}),'37,000');
assert.throws(()=>bank.timebase({duration:Infinity}),/finite/);
assert.throws(()=>bank.applyPreset({fromTo(){},set(){}},'JS:B07',{},{}),/Unsupported/);
assert.throws(()=>bank.entranceHoldExit({},{x:0},{holdUntil:.2}),/overlaps/);
// Reachable, overextended, folded and mirrored bends all preserve segment lengths.
for(const bend of [-1,1])for(const target of [{x:4,y:3},{x:100,y:0},{x:0,y:0},{x:-3,y:5}]){
  const root={x:0,y:0},q=bank.solveTwoBone(root,target,5,4,bend);
  close(Math.hypot(q.elbow.x,q.elbow.y),5);
  close(Math.hypot(q.end.x-q.elbow.x,q.end.y-q.elbow.y),4);
  assert.ok(Number.isFinite(q.lowerLocalDegrees));
}
// Re-seek real GSAP plain-object targets, with callbacks suppressed (HyperFrames compatible).
const group={opacity:0,y:0},counter={textContent:'0'},marker={scaleX:0,transformOrigin:''};
const timeline=gsap.timeline({paused:true});
bank.applyPreset(timeline,'JS:B04',{group,counter,marker},{to:37000,duration:5});
for(const time of [0,.2,.75,2.05,3.35,4,4.8,2.05,0,3.35]){
  timeline.seek(time,true);
  const expected=bank.sampleB04(time,{to:37000});
  assert.equal(String(counter.textContent),bank.formatCounter(expected.value));
  close(group.opacity,expected.opacity);close(group.y,expected.y);close(marker.scaleX,expected.marker);
}
// Initial DOM/CSS state must match the start pose; seek(0) need not cross a zero-time set.
const words=[{yPercent:100,opacity:0},{yPercent:100,opacity:0},{yPercent:100,opacity:0}],wordTL=gsap.timeline({paused:true});
bank.applyPreset(wordTL,'JS:T01',words,{duration:5});
for(const time of [0,.4,2,4.3,5,2,.4]){
  wordTL.seek(time,true);
  words.forEach((word,i)=>{
    const expected=bank.sampleT01(time,i,words.length);
    close(word.opacity,expected.opacity,1e-4);close(word.yPercent,expected.yEm*100,1e-4);
  });
}
const item={opacity:1,y:0,scale:1,rotation:0},motionTL=gsap.timeline({paused:true});
const range=bank.entranceHoldExit(motionTL,item,{mode:'pop',start:0,holdUntil:2});
motionTL.seek(1,true);assert.equal(item.opacity,1);close(item.scale,1);close(item.y,0);
motionTL.seek(range.end,true);assert.equal(item.opacity,0);
console.log(JSON.stringify({ok:true,gsap:gsap.version,ports:Object.keys(bank.PORTS),checks:['Python easing endpoints','exact counter value','suppressed callback seek','nonmonotonic seek','T01 sampler parity','IK length/contact','finite timing guards']}));
gsap.globalTimeline.clear();gsap.ticker.sleep();
