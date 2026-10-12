#!/usr/bin/env node
/** Motion Atlas: render original editable vector components or multi-layer scenes. */
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const req=createRequire(import.meta.url);
let sharp;
for(const candidate of ['sharp',process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES&&path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'sharp'),'/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp']){if(!candidate)continue;try{sharp=req(candidate);break;}catch{}}
if(!sharp)throw Error('Install sharp with npm install sharp, then rerun. FFmpeg is also required.');
sharp.cache(false);sharp.concurrency(1);
const args={};for(let i=2;i<process.argv.length;i++){let a=process.argv[i];if(!a.startsWith('--'))throw Error('Expected --option');args[a.slice(2)]=process.argv[i+1]?.startsWith('--')?true:process.argv[++i]??true;}
const library=args.library||here;
const {records,render,compose,customize}=await import(path.join(library,'motion_engine.mjs'));
const rows=records();
const w=Number(args.width||1920),h=Number(args.height||1080),fps=Number(args.fps||30);
if(!Number.isInteger(w)||!Number.isInteger(h)||w<32||h<32||w>4096||h>4096||!Number.isInteger(fps)||fps<1||fps>60)throw Error('Invalid dimensions/fps.');
const scene=args.scene?JSON.parse(fs.readFileSync(args.scene,'utf8')):null;
const given=args.recipe?JSON.parse(fs.readFileSync(args.recipe,'utf8')):null;
const row=given?customize(given.id,given.parameters||{}):args.id?rows.find(x=>x.id===args.id):null;
if(!row&&!scene)throw Error('Use --id MA0001, --recipe component.json or --scene scene.json.');
const duration=Number(args.duration||scene?.duration||row?.duration||3);if(!(duration>0&&duration<=1800))throw Error('Invalid duration.');
const output=path.resolve(args.output||`${row?.id||'scene'}.${args.alpha?'mov':'mp4'}`);fs.mkdirSync(path.dirname(output),{recursive:true});
const frames=Math.round(duration*fps);
const inputAlpha=Boolean(args.alpha||args['png-sequence']);
if(args['png-sequence'])fs.mkdirSync(output,{recursive:true});
const enc=args['png-sequence']?null:spawn('ffmpeg',['-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt',inputAlpha?'rgba':'rgb24','-s',`${w}x${h}`,'-r',`${fps}`,'-i','pipe:0','-an',...(inputAlpha?['-c:v','prores_ks','-profile:v','4','-pix_fmt','yuva444p10le']:['-c:v','libx264','-preset','veryfast','-crf',String(args.crf||20),'-pix_fmt','yuv420p','-movflags','+faststart']),'-frames:v',String(frames),output],{stdio:['pipe','ignore','pipe']});
let errors='';let exitPromise;if(enc){enc.stderr.on('data',x=>errors+=x);enc.stdin.on('error',()=>{});exitPromise=once(enc,'close');}
for(let i=0;i<frames;i++){
 const t=i/fps,svg=scene?compose(scene,t,{width:w,height:h,transparent:inputAlpha}):render(row,t*row.duration/duration,{width:w,height:h,transparent:inputAlpha});
 const img=sharp(Buffer.from(svg)).resize(w,h);
 if(args['png-sequence'])await img.png().toFile(path.join(output,`${String(i).padStart(6,'0')}.png`));
 else{const raw=await (inputAlpha?img.ensureAlpha():img.flatten({background:'#08131c'}).removeAlpha()).raw().toBuffer();if(!enc.stdin.write(raw))await once(enc.stdin,'drain');}
}
if(enc){enc.stdin.end();const[code]=await exitPromise;if(code!==0)throw Error(errors||`FFmpeg exit ${code}`);}
fs.writeFileSync(output+'.manifest.json',JSON.stringify({schema:1,collection:'Motion Atlas MA original adaptations',id:row?.id||null,scene,frames,fps,width:w,height:h,duration,alpha:inputAlpha,source_observations:row?.observation_ids||[...new Set(scene.layers.flatMap(l=>rows.find(r=>r.id===l.id)?.observation_ids||[]))],component_ids:row?[row.id]:[...new Set(scene.layers.map(l=>l.id))],parameters:row?.parameters||null,output:path.basename(output)},null,2));
console.log(JSON.stringify({output,frames,width:w,height:h,fps,duration}));
