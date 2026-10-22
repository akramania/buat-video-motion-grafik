#!/usr/bin/env node
'use strict';
// Export real per-character pose assets, motion recipes, and encoded MP4 samples.
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {engine,roster,dimensions,durationFor,frameBox,svgFor,pngFor,renderClip}=require('./render_character.cjs');
const DEFAULT_ROOT=path.resolve(__dirname,'..');
function parse(argv) {
  const result={};
  const flags=new Set(['help','skip-clips']);
  const values=new Set(['character','jobs','clip-width','clip-height','pose-width','fps','output-root','manifest','ffmpeg','crf']);
  for(let i=0;i<argv.length;i++) {
    const key=argv[i].replace(/^--/,'');
    if(!argv[i].startsWith('--')) throw new Error('Unexpected argument '+argv[i]);
    if(flags.has(key)) result[key]=true;
    else if(values.has(key)) {
      if(argv[i+1]===undefined||argv[i+1].startsWith('--')) throw new Error('Missing value for --'+key);
      result[key]=argv[++i];
    } else throw new Error('Unknown option --'+key);
  }
  return result;
}
function number(value,name,min,max,integer=false) {
  const n=Number(value);
  if(!Number.isFinite(n)||n<min||n>max||(integer&&!Number.isInteger(n))) throw new Error(name+' must be '+(integer?'an integer ':'a number ')+'between '+min+' and '+max+'.');
  return n;
}
function writeJson(file,value) {
  fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,JSON.stringify(value,null,2)+'\n');
}
function sha(file) {return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}
function relative(root,file) {return path.relative(root,file).split(path.sep).join('/');}
async function main(argv=process.argv.slice(2)) {
  const args=parse(argv);
  if(args.help) {
    console.log(`Export Bank Watak 20 poses and motions (offline)

node source/export_motion_bank.cjs
node source/export_motion_bank.cjs --character P05,L01 --jobs 4
node source/export_motion_bank.cjs --skip-clips

Default: all 20 characters, all 42 poses (SVG + PNG), all 34 motion recipes,
and all 680 actual H.264 MP4 clips. Recipes describe callable deterministic
motion code and sampled states; they are not frame sequences.

--character IDS     Optional comma-separated subset
--jobs N            1..4 simultaneous clip jobs; default 4
--clip-width N      Default 288; height defaults to 5/3 width, rounded to even
--clip-height N     Default 480; MP4 dimensions must be even
--pose-width N      PNG pose width; default 320; SVG retains scalable viewBox
--fps N             Clip fps; default 24
--skip-clips        Export poses + recipes only; records zero generated clips
--output-root DIR   Collection root; default parent of source directory
--manifest FILE     Optional manifest path relative to output root
--ffmpeg PATH       Optional FFmpeg executable
--crf N             H.264 quality 0..51; default 27
`);return;
  }
  const e=engine(), all=roster(), root=path.resolve(args['output-root']??DEFAULT_ROOT);
  const ids=args.character?new Set(args.character.split(',').filter(Boolean)):null;
  if(ids) for(const id of ids) if(!all.some(c=>c.id===id)) throw new Error('Unknown character '+id);
  const chars=ids?all.filter(c=>ids.has(c.id)):all;
  if(!chars.length) throw new Error('No characters selected.');
  const jobs=number(args.jobs??4,'jobs',1,4,true);
  const clipWidth=number(args['clip-width']??288,'clip-width',2,4096,true);
  const clipHeight=number(args['clip-height']??Math.round(clipWidth*5/6)*2,'clip-height',2,4096,true);
  if(clipWidth%2||clipHeight%2) throw new Error('Clip width and height must be even for yuv420p.');
  const poseWidth=number(args['pose-width']??320,'pose-width',2,4096,true);
  const poseHeight=Math.round(poseWidth*5/3);
  const fps=number(args.fps??24,'fps',1,120);
  const crf=number(args.crf??27,'crf',0,51);
  dimensions({width:poseWidth,height:poseHeight});
  if(e.POSES.length!==42||e.MOTIONS.length!==34) throw new Error('Expected 42 poses and 34 motions.');
  const manifest={
    collection:'Bank Watak 20 — Pose dan Gerakan',version:'3.0',generated_at:new Date().toISOString(),
    artwork:'original code-native layered SVG',fictional:true,
    status:'Articulated 2D vector rig, deterministic motion recipes, pose assets, and actual encoded MP4 samples. No audio or automatic lip sync.',
    source_api:{rig:'source/character_rig.cjs: rigSvg(character, state, options), rigGeometry(character, state, options)',
      poses:'source/motion_library.cjs: POSES, poseState(poseId, character)',
      motions:'source/motion_library.cjs: MOTIONS, sampleMotion(motionId, seconds, character, options), durationForCharacter(motionId, character)',
      renderer:'node source/render_character.cjs --help'},
    output:{pose_png:{width:poseWidth,height:poseHeight,alpha:true},
      clip:{asset_role:'clips_preview; reusable MP4 action samples',width:clipWidth,height:clipHeight,fps,codec:'h264',pixel_format:'yuv420p',background:'#f6f1e7',audio:false,
        production_export:'Use source/render_character.cjs to render from the vector rig at the master resolution or export transparent PNG frames.'}},
    summary:{character_count:chars.length,poses_per_character:e.POSES.length,motions_per_character:e.MOTIONS.length,
      pose_svg_count:0,pose_png_count:0,motion_recipe_count:0,motion_clip_count:0},
    catalog:{poses:e.POSES,motions:e.MOTIONS},source_sha256:{},characters:[]
  };
  for(const file of ['characters.json','character_renderer.cjs','character_rig.cjs','motion_library.cjs','render_character.cjs','export_motion_bank.cjs']) {
    const full=path.join(__dirname,file);if(fs.existsSync(full))manifest.source_sha256['source/'+file]=sha(full);
  }
  const tasks=[];
  for(const c of chars) {
    const entry={id:c.id,name:c.name,age:c.age,age_group:c.age_group,poses:[],motions:[]};
    const poseDir=path.join(root,'poses',c.id);fs.mkdirSync(poseDir,{recursive:true});
    for(const definition of e.POSES) {
      const state=e.poseState(definition.id,c), view=definition.view??state.view??'front';
      const viewBox=frameBox(c,[state],{width:poseWidth,height:poseHeight,view});
      const svg=svgFor(c,state,{width:poseWidth,height:poseHeight,view,viewBox});
      const svgPath=path.join(poseDir,definition.id+'.svg'),pngPath=path.join(poseDir,definition.id+'.png');
      fs.writeFileSync(svgPath,svg);
      fs.writeFileSync(pngPath,await pngFor(svg,{width:poseWidth,height:poseHeight}));
      entry.poses.push({id:definition.id,label:definition.label,view,view_box:viewBox,
        svg:relative(root,svgPath),png:relative(root,pngPath),svg_sha256:sha(svgPath),png_sha256:sha(pngPath)});
      manifest.summary.pose_svg_count++;manifest.summary.pose_png_count++;
    }
    for(const definition of e.MOTIONS) {
      const duration=durationFor(definition.id,c), frameCount=Math.ceil(duration*fps);
      const recipePath=path.join(root,'motions',c.id,definition.id+'.json');
      const clipPath=path.join(root,'clips',c.id,definition.id+'.mp4');
      const recipe={character_id:c.id,motion_id:definition.id,label:definition.label,
        asset_type:'deterministic motion recipe, not pre-rendered frame data',
        view:definition.view??'front',loop:Boolean(definition.loop),duration_seconds:duration,
        callable:{module:'source/motion_library.cjs',export:'sampleMotion',arguments:[definition.id,'time_seconds','character_object',{loop:Boolean(definition.loop)}],
          character_reference:{file:'source/characters.json',id:c.id},
          note:'Load the matching character object from the roster before calling sampleMotion.'},
        timing:'Evaluate state at time_seconds = frame_index / fps. Character-specific action duration is already applied by sampleMotion.',
        state_samples:[0,.25,.5,.75,1-1e-6].map(f=>({time_seconds:duration*f,state:e.sampleMotion(definition.id,duration*f,c,{loop:Boolean(definition.loop)})})),
        clip:args['skip-clips']?null:{path:relative(root,clipPath),status:'pending',asset_role:'clips_preview',width:clipWidth,height:clipHeight,fps,frame_count:frameCount,
          encoded_duration:frameCount/fps,codec:'h264',pixel_format:'yuv420p',alpha:false,audio:false}
      };
      writeJson(recipePath,recipe);
      const item={id:definition.id,label:definition.label,recipe:relative(root,recipePath),duration_seconds:duration,loop:Boolean(definition.loop),clip:null};
      entry.motions.push(item);manifest.summary.motion_recipe_count++;
      if(!args['skip-clips']) tasks.push({c,definition,recipe,recipePath,clipPath,item});
    }
    manifest.characters.push(entry);
    console.log(c.id+' pose assets and motion recipes exported.');
  }
  let next=0,completed=0,aborted=false;
  async function worker() {
    while(!aborted&&next<tasks.length) {
      const task=tasks[next++];
      try {
        const result=await renderClip(task.c,task.definition.id,task.clipPath,{width:clipWidth,height:clipHeight,fps,crf,ffmpeg:args.ffmpeg});
        const bytes=fs.statSync(task.clipPath).size;
        task.recipe.clip={...task.recipe.clip,status:'rendered',frame_count:result.frame_count,encoded_duration:result.encoded_duration,
          view_box:result.view_box,bytes,sha256:sha(task.clipPath)};
        writeJson(task.recipePath,task.recipe);
        task.item.clip={...task.recipe.clip};
        manifest.summary.motion_clip_count++;completed++;
        if(completed%12===0||completed===tasks.length) console.log('MP4 '+completed+'/'+tasks.length+' complete.');
      } catch(error) { aborted=true;throw new Error(task.c.id+'/'+task.definition.id+': '+error.message); }
    }
  }
  const outcomes=await Promise.allSettled(Array.from({length:Math.min(jobs,tasks.length)},()=>worker()));
  const failure=outcomes.find(result=>result.status==='rejected');
  if(failure) throw failure.reason;
  const filename=args.manifest??(ids?'motion_bank_manifest_'+chars.map(c=>c.id).join('_')+'.json':'motion_bank_manifest.json');
  const manifestPath=path.resolve(root,filename);
  writeJson(manifestPath,manifest);
  console.log(JSON.stringify({manifest:manifestPath,...manifest.summary},null,2));
  return manifest;
}
module.exports={main,parse};
if(require.main===module) main().catch(error=>{console.error('Export error: '+error.message);process.exitCode=1;});
