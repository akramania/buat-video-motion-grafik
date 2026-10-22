// Original deterministic vector scene. Shared by Node Canvas and a local browser.
(function(root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.CanvasScene = factory();
})(typeof window === 'object' ? window : globalThis, function() {
'use strict';
function renderFrame(ctx, t, w, h) {
const ease = x => { x=Math.max(0,Math.min(1,x)); return 1-Math.pow(1-x,3); };
function pill(x,y,w,h,r,fill){ctx.fillStyle=fill;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();}
function joint(x,y,angle,length,colour,width,child){
  ctx.save();ctx.translate(x,y);ctx.rotate(angle);ctx.strokeStyle=colour;ctx.lineWidth=width;
  ctx.lineCap='round';ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,length);ctx.stroke();
  if(child) child(0,length);ctx.restore();
}

  if(!Number.isFinite(t)) throw new Error('Finite seconds required');
  ctx.save();
  ctx.setTransform(w/960,0,0,h/540,0,0);
  const g=ctx.createLinearGradient(0,0,960,540);g.addColorStop(0,'#091e32');g.addColorStop(1,'#173f53');
  ctx.fillStyle=g;ctx.fillRect(0,0,960,540);
  // Two independent depth layers; the far layer travels more slowly.
  for(let layer=0;layer<2;layer++){
    ctx.fillStyle=layer?'#1e5666':'#123949';
    for(let i=-1;i<9;i++){
      const x=i*150+Math.sin(t*.35+layer)*22*(layer+1);
      ctx.beginPath();ctx.arc(x,480+layer*60,150+layer*25,Math.PI,0);ctx.fill();
    }
  }
  ctx.save();ctx.translate(650+Math.sin(t*.6)*6,260+Math.sin(t*1.5)*5);
  ctx.fillStyle='#07192766';ctx.beginPath();ctx.ellipse(0,204,104,17,0,0,Math.PI*2);ctx.fill();
  // Body rig: limbs inherit shoulder transforms; hand inherits elbow transform.
  joint(-31,105,-.08,83,'#b8dce3',27);joint(31,105,.08,83,'#b8dce3',27);
  pill(-65,-6,130,143,38,'#55c9b9');pill(-45,123,35,18,8,'#edf8ef');pill(10,123,35,18,8,'#edf8ef');
  joint(-62,20,-.12,73,'#55c9b9',26,(x,y)=>joint(x,y,-.2,52,'#ffd1a6',23));
  const shoulder=-2.1+Math.sin(t*4.5)*.12, elbow=.65+Math.sin(t*6)*.4;
  joint(62,20,shoulder,68,'#55c9b9',26,(x,y)=>joint(x,y,elbow,58,'#ffd1a6',23,(hx,hy)=>{
    ctx.save();ctx.translate(hx,hy);ctx.rotate(Math.sin(t*6)*.28);
    pill(-16,-7,32,36,14,'#ffd1a6');
    for(let i=0;i<4;i++) pill(-14+i*8,18,6,22-i%2*4,3,'#ffd1a6');ctx.restore();
  }));
  pill(-23,-29,46,45,14,'#ffd1a6');
  ctx.fillStyle='#ffd1a6';ctx.beginPath();ctx.ellipse(0,-68,58,64,0,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#173345';ctx.beginPath();ctx.ellipse(-1,-101,59,35,-.1,Math.PI,Math.PI*2);ctx.fill();
  pill(-54,-115,108,24,12,'#173345');
  const blink=Math.cos(t*2.1)>.995?.12:1;
  ctx.fillStyle='#173345';for(const x of [-20,20]){ctx.beginPath();ctx.ellipse(x,-69,4,6*blink,0,0,Math.PI*2);ctx.fill();}
  ctx.strokeStyle='#a25446';ctx.lineWidth=3;ctx.beginPath();ctx.arc(0,-55,13,.15,Math.PI-.15);ctx.stroke();
  ctx.restore();
  // Kinetic label: offset shadow + bright foreground, both inside a reveal mask.
  const reveal=ease(t/.65), lift=(1-reveal)*32;
  ctx.save();ctx.beginPath();ctx.rect(66,107,450*reveal,220);ctx.clip();
  ctx.font='800 54px sans-serif';ctx.fillStyle='#071724';ctx.fillText('VECTOR',78,180+lift);
  ctx.fillStyle='#f5f6e7';ctx.fillText('VECTOR',74,176+lift);
  ctx.fillStyle='#071724';ctx.fillText('IN MOTION',78,242+lift);
  ctx.fillStyle='#ffd36e';ctx.fillText('IN MOTION',74,238+lift);
  ctx.restore();
  pill(75,272,310*ease((t-.15)/.65),5,2,'#55c9b9');
  ctx.font='20px sans-serif';ctx.fillStyle='#c1d9e1';ctx.fillText('Rig • parallax • masked type',75,320);
  ctx.font='14px sans-serif';ctx.fillStyle='#98bdc8';ctx.fillText('LOCAL CANVAS → FFMPEG → MP4',75,463);

  ctx.restore();
}
return { renderFrame };
});
