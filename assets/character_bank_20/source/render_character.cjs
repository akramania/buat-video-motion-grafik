#!/usr/bin/env node
'use strict';
// Offline, deterministic renderer for the original Bank Watak 20 rigs.
const fs = require('node:fs');
const path = require('node:path');
const {spawn} = require('node:child_process');

function loadSharp() {
  try { return require('sharp'); } catch (first) {
    for (const base of [process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,
      '/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules'].filter(Boolean)) {
      try { return require(path.join(base, 'sharp')); } catch (_) {}
    }
    throw new Error('sharp is required. Install it locally with npm install sharp. ' + first.message);
  }
}
let sharp;
let renderSequence=0;
function rasterizer() {
  if (!sharp) { sharp = loadSharp(); sharp.concurrency(1); sharp.cache({memory:32, files:0, items:32}); }
  return sharp;
}
function engine() {
  return {...require('./character_rig.cjs'), ...require('./motion_library.cjs')};
}
function roster() { return JSON.parse(fs.readFileSync(path.join(__dirname,'characters.json'),'utf8')); }
function characterById(id) {
  const c=roster().find(c=>c.id===id);
  if (!c) throw new Error('Unknown character: '+id+'. Use --list.');
  return c;
}
function positive(value,name,{integer=false,min=0,max=Infinity}={}) {
  const n=Number(value);
  if (!Number.isFinite(n)||n<=min||n>max||(integer&&!Number.isInteger(n))) {
    throw new Error(name+' must be '+(integer?'an integer ':'a number ')+'greater than '+min+' and at most '+max+'.');
  }
  return n;
}
function dimensions(options={}) {
  const width=positive(options.width??360,'width',{integer:true,max:4096});
  const height=positive(options.height??Math.round(width*5/3),'height',{integer:true,max:4096});
  return {width,height};
}
function validView(view) {
  if(view!==undefined&&!['front','back','side','three_quarter','side_right','side_left','three_quarter_right','three_quarter_left'].includes(view)) throw new Error('view must be front, back, side_right, side_left, three_quarter_right or three_quarter_left (legacy side/three_quarter supported).');
  return view;
}
function validBackground(value) {
  if(value!==undefined&&!/^#[0-9a-fA-F]{6}$/.test(value)) throw new Error('background must be a six-digit hex colour, e.g. #f6f1e7.');
  return value;
}
function selectedDefinition(list,id,type) {
  const entry=list.find(d=>d.id===id);
  if(!entry) throw new Error('Unknown '+type+': '+id+'. Use --list.');
  return entry;
}
function durationFor(id,c,override) {
  const e=engine(), d=selectedDefinition(e.MOTIONS,id,'motion');
  const duration=override??(typeof e.durationForCharacter==='function'?e.durationForCharacter(id,c):d.duration);
  return positive(duration,'duration',{max:1800});
}
function frameBox(c,states,options={}) {
  // One fixed camera for the whole action: no frame-to-frame auto-zoom.
  const {width,height}=dimensions(options),e=engine();
  let left=0,top=0,right=600,bottom=1000;
  for(const state of states) {
    const g=e.rigGeometry(c,state,{view:options.view??state.view??'front'}),b=g.bounds;
    if(!b) throw new Error('The rig must expose geometry bounds for safe framing.');
    const l=b.minX??b.left,t=b.minY??b.top,r=b.maxX??b.right,d=b.maxY??b.bottom;
    if(![l,t,r,d].every(Number.isFinite)) throw new Error('The rig returned non-finite geometry bounds.');
    left=Math.min(left,l-12);top=Math.min(top,t-12);right=Math.max(right,r+12);bottom=Math.max(bottom,d+12);
  }
  const cx=(left+right)/2,cy=(top+bottom)/2,aspect=width/height;
  let w=right-left,h=bottom-top;
  if(w/h>aspect)h=w/aspect;else w=h*aspect;
  return [cx-w/2,cy-h/2,w,h].map(v=>Math.round(v*1000)/1000);
}
function svgFor(c,state,options={}) {
  const size=dimensions(options), view=validView(options.view??state.view??'front');
  const background=validBackground(options.background);
  return engine().rigSvg(c,state,{...size,view,transparent:!background,background,
    viewBox:options.viewBox, guides:Boolean(options.guides)});
}
async function pngFor(svg,size,background) {
  let pipeline=rasterizer()(Buffer.from(svg)).resize(size.width,size.height,{fit:'fill'}).ensureAlpha();
  if(background) pipeline=pipeline.flatten({background});
  return pipeline.png().toBuffer();
}
async function renderStatic(c,poseId,output,options={}) {
  const e=engine(); selectedDefinition(e.POSES,poseId,'pose');
  const size=dimensions(options), state=e.poseState(poseId,c);
  const viewBox=options.viewBox??frameBox(c,[state],options);
  const svg=svgFor(c,state,{...options,viewBox}), ext=path.extname(output).toLowerCase();
  if(!['.svg','.png'].includes(ext)) throw new Error('Pose output must end in .svg or .png.');
  fs.mkdirSync(path.dirname(path.resolve(output)),{recursive:true});
  if(ext==='.svg') fs.writeFileSync(output,svg);
  else fs.writeFileSync(output,await pngFor(svg,size,validBackground(options.background)));
  return {character_id:c.id,pose:poseId,...size,view:options.view??state.view??'front',view_box:viewBox,output:path.resolve(output)};
}
async function writePipe(stream,buffer) {
  await new Promise((resolve,reject)=>stream.write(buffer,error=>error?reject(error):resolve()));
}
async function renderClip(c,motionId,output,options={}) {
  const e=engine(), definition=selectedDefinition(e.MOTIONS,motionId,'motion');
  const {width,height}=dimensions(options);
  const fps=positive(options.fps??30,'fps',{max:120});
  const actionDuration=durationFor(motionId,c),duration=durationFor(motionId,c,options.duration), frameCount=Math.ceil(duration*fps);
  const view=validView(options.view), background=validBackground(options.background)??'#f6f1e7';
  const framingStates=Array.from({length:25},(_,i)=>e.sampleMotion(motionId,duration*i/24,c,{loop:options.loop??definition.loop}));
  const viewBox=options.viewBox??frameBox(c,framingStates,{width,height,view});
  const frames=options.frames?path.resolve(options.frames):null;
  if(!output&&!frames) throw new Error('Motion rendering requires --output file.mp4 or --frames directory.');
  if(output&&path.extname(output).toLowerCase()!=='.mp4') throw new Error('Motion output must end in .mp4.');
  if(output&&(width%2||height%2)) throw new Error('MP4 width and height must be even for yuv420p.');
  if(frames) fs.mkdirSync(frames,{recursive:true});
  let encoder, completion, stderr='', spawnError,encoderOutput;
  if(output) {
    fs.mkdirSync(path.dirname(path.resolve(output)),{recursive:true});
    // Publish only a finished MP4. Consumers never see an in-progress file.
    encoderOutput=path.join(path.dirname(path.resolve(output)),'.'+path.basename(output,'.mp4')+'.render-'+process.pid+'-'+(++renderSequence)+'.mp4');
    encoder=spawn(options.ffmpeg??'ffmpeg',[
      '-y','-hide_banner','-loglevel','error', '-f','rawvideo','-pixel_format','rgba',
      '-video_size',width+'x'+height,'-framerate',String(fps),'-i','pipe:0','-an',
      '-c:v','libx264','-preset','veryfast','-threads','1','-crf',String(options.crf??27),
      '-pix_fmt','yuv420p','-r',String(fps),'-movflags','+faststart',encoderOutput
    ],{stdio:['pipe','ignore','pipe']});
    encoder.stderr.on('data',chunk=>{stderr=(stderr+chunk.toString()).slice(-16000);});
    // Attach handlers immediately so a missing encoder / broken pipe is a normal error.
    encoder.stdin.on('error',error=>{spawnError??=error;});
    completion=new Promise(resolve=>{
      encoder.on('error',error=>{spawnError=error;resolve({code:null,signal:null});});
      encoder.on('close',(code,signal)=>resolve({code,signal}));
    });
  }
  try {
    for(let i=0;i<frameCount;i++) {
      const time=i/fps;
      const state=e.sampleMotion(motionId,time,c,{loop:options.loop??definition.loop});
      const svg=svgFor(c,state,{width,height,view,viewBox,guides:options.guides});
      if(frames) fs.writeFileSync(path.join(frames,'frame_'+String(i).padStart(6,'0')+'.png'),await pngFor(svg,{width,height},options.framesBackground));
      if(encoder) {
        if(spawnError) throw spawnError;
        // Flatten against a deliberate solid colour; H.264 MP4 does not retain alpha.
        const rgba=await rasterizer()(Buffer.from(svg)).resize(width,height,{fit:'fill'})
          .flatten({background}).ensureAlpha().raw().toBuffer();
        await writePipe(encoder.stdin,rgba);
      }
      if(options.onProgress) options.onProgress({frame:i+1,frameCount,time});
    }
    if(encoder) {
      encoder.stdin.end();
      const result=await completion;
      if(spawnError||result.code!==0) throw new Error('FFmpeg failed: '+(spawnError?.message??('exit '+result.code+(result.signal?' '+result.signal:'')))+'\n'+stderr.trim());
      fs.renameSync(encoderOutput,path.resolve(output));
    }
  } catch(error) {
    if(encoder) { encoder.stdin.destroy(); encoder.kill('SIGTERM'); await completion; }
    if(encoderOutput) { try {fs.unlinkSync(encoderOutput);} catch(_){} }
    if(spawnError) throw new Error('FFmpeg failed: '+spawnError.message+(stderr.trim()?'\n'+stderr.trim():''));
    throw error;
  }
  return {character_id:c.id,motion:motionId,width,height,fps,frame_count:frameCount,
    requested_duration:duration,action_duration:actionDuration,encoded_duration:frameCount/fps,loop:Boolean(options.loop??definition.loop),
    view:view??definition.view??'front',view_box:viewBox,background:output?background:null,
    output:output?path.resolve(output):null,frames_directory:frames,
    frames_alpha:frames&&!options.framesBackground?true:undefined,
    format:output?'H.264 MP4 / yuv420p': 'PNG sequence / RGBA'};
}
function parseArgs(argv) {
  const flags=new Set(['list','help','loop','no-loop','guides']);
  const values=new Set(['character','pose','motion','output','frames','fps','width','height','duration','view','background','ffmpeg','crf']);
  const out={};
  for(let i=0;i<argv.length;i++) {
    const token=argv[i];
    if(!token.startsWith('--')) throw new Error('Unexpected argument '+token+'. Use --help.');
    const key=token.slice(2);
    if(flags.has(key)) out[key]=true;
    else if(values.has(key)) {
      if(argv[i+1]===undefined||argv[i+1].startsWith('--')) throw new Error('Missing value for '+token);
      out[key]=argv[++i];
    } else throw new Error('Unknown option '+token+'. Use --help.');
  }
  if(out['no-loop']&&out.loop) throw new Error('Use only one of --loop and --no-loop.');
  if(out['no-loop']) out.loop=false;
  if(out.crf!==undefined) {
    const crf=Number(out.crf); if(!Number.isFinite(crf)||crf<0||crf>51) throw new Error('crf must be 0..51.'); out.crf=crf;
  }
  return out;
}
const HELP=`Bank Watak 20 — deterministic SVG / PNG / FFmpeg renderer

node source/render_character.cjs --list
node source/render_character.cjs --character P05 --pose wave_hello --output P05.svg
node source/render_character.cjs --character L01 --motion wave_hello --output L01.mp4 --fps 30 --width 360 --height 600
node source/render_character.cjs --character P10 --motion walk_across --frames transparent_frames --fps 24

--character ID       One character ID from --list
--pose ID            One static pose; output .svg or .png
--motion ID          One motion; output .mp4 and/or transparent --frames DIR
--duration SECONDS   Rendered time window; does not retime the action. Default is its full character-specific duration.
--width N --height N Default 360 × 600; MP4 requires even dimensions
--fps N              Default 30 (motion only)
--view VIEW          front/back/side_right/side_left/three_quarter_right/three_quarter_left
--background #RRGGBB MP4 background; default #f6f1e7. Explicitly colours static assets.
--loop / --no-loop   Override motion looping
--crf N              H.264 quality 0..51; default 27
--ffmpeg PATH        Encoder executable; default ffmpeg in PATH
--guides             Include rig reference guides

SVG / PNG assets and PNG motion frames retain alpha by default.
MP4 is H.264 yuv420p with faststart; no audio. Times are evaluated at frame_index / fps.
The viewBox is fixed once per pose or whole motion from sampled rig bounds and the original canvas.
Requirements: Node.js, sharp (npm install sharp), FFmpeg with libx264. No network at render time.
`;
async function main(argv=process.argv.slice(2)) {
  const args=parseArgs(argv);
  if(args.help||!argv.length) { console.log(HELP); return; }
  if(args.list) {
    const e=engine();
    console.log(JSON.stringify({characters:roster().map(({id,name,age,age_group})=>({id,name,age,age_group})),poses:e.POSES,motions:e.MOTIONS},null,2));
    return;
  }
  if(!args.character) throw new Error('--character is required.');
  if(Boolean(args.pose)===Boolean(args.motion)) throw new Error('Select exactly one --pose or --motion.');
  const c=characterById(args.character);
  if(args.pose) {
    if(!args.output) throw new Error('--output file.svg or file.png is required for a pose.');
    if(args.frames) throw new Error('--frames is supported for motions only.');
    console.log(JSON.stringify(await renderStatic(c,args.pose,args.output,args),null,2));
  } else console.log(JSON.stringify(await renderClip(c,args.motion,args.output,args),null,2));
}
module.exports={loadSharp,rasterizer,engine,roster,characterById,dimensions,durationFor,frameBox,svgFor,pngFor,renderStatic,renderClip,parseArgs,main};
if(require.main===module) main().catch(error=>{console.error('Render error: '+error.message);process.exitCode=1;});
