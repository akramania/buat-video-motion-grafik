#!/usr/bin/env node
// Explicit setup only. Default preflight never downloads or changes the project.
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import zlib from 'node:zlib';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {spawnSync} from 'node:child_process';
const args=process.argv.slice(2), value=(key,fall)=>{const i=args.indexOf(key);return i<0?fall:args[i+1]};
if(args.includes('--help')){console.log('Usage: node setup_hyperframes.mjs [--project DIR] [--runtime CACHE] [--browser EXECUTABLE] [--online | --install-offline]\nDefault: read-only preflight with actual Chrome launch. --online permits npm/browser downloads; --install-offline uses npm cache only.');process.exit(0);}
const skillRoot=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const project=path.resolve(value('--project',path.join(skillRoot,'assets/hyperframes')));
const runtime=path.resolve(value('--runtime',process.env.KM_HYPERFRAMES_RUNTIME||path.join(os.homedir(),'.cache/km-video-hyperframes/0.8.185')));
const online=args.includes('--online'), offline=args.includes('--install-offline');
const run=(cmd,a,opts={})=>spawnSync(cmd,a,{encoding:'utf8',...opts});
const exists=p=>!!p&&fs.existsSync(p);
const [nodeMajor,nodeMinor]=process.versions.node.split('.').map(Number);
if(nodeMajor<22 || (nodeMajor===22 && nodeMinor<12)) throw Error('Node.js >=22.12 required by the locked browser tooling');
if(online&&offline) throw Error('Choose --online OR --install-offline');
if(online||offline){
 fs.mkdirSync(runtime,{recursive:true});
 for(const file of ['package.json','package-lock.json']) fs.copyFileSync(path.join(project,file),path.join(runtime,file));
 const r=run('npm',['ci','--no-audit','--no-fund',...(offline?['--offline']:[])],{cwd:runtime,stdio:'inherit'});
 if(r.status!==0) throw Error('npm ci failed; source and existing assets preserved');
}
const moduleFile=path.join(runtime,'node_modules/hyperframes/bin/hyperframes.mjs');
let browser=value('--browser',process.env.HYPERFRAMES_BROWSER_PATH);
const savedBrowser=path.join(runtime,'browser-path.txt');
if(!browser&&exists(savedBrowser)) browser=fs.readFileSync(savedBrowser,'utf8').trim();
if(browser) browser=path.resolve(browser);
if(!exists(browser)) browser=['/usr/bin/google-chrome','/usr/bin/chromium','/usr/bin/chromium-browser'].find(exists);
if(!exists(browser)&&online&&exists(moduleFile)){
 const r=run(process.execPath,[moduleFile,'browser','ensure'],{cwd:runtime,env:{...process.env,HYPERFRAMES_NO_UPDATE_CHECK:'1'},timeout:120000});
 const p=run(process.execPath,[moduleFile,'browser','path'],{cwd:runtime,env:{...process.env,HYPERFRAMES_NO_UPDATE_CHECK:'1'},timeout:15000});
 if(p.status===0){const candidate=p.stdout.trim().split('\n').at(-1);if(exists(candidate)) browser=candidate;}
 if(!browser) console.error('Browser provider unavailable; trying the pinned npm Chromium fallback.');
}
// Offline-capable fallback after npm ci: unpack without chown, which managed filesystems can reject.
if(!exists(browser)&&(online||offline)){
 const bin=path.join(runtime,'node_modules/@sparticuz/chromium/bin'), out=path.join(runtime,'browser');
 if(exists(path.join(bin,'chromium.br'))){
  fs.mkdirSync(out,{recursive:true});
  browser=path.join(out,'chromium');
  fs.writeFileSync(browser,zlib.brotliDecompressSync(fs.readFileSync(path.join(bin,'chromium.br')))); fs.chmodSync(browser,0o755);
  for(const name of ['fonts','swiftshader','al2023']){
   const source=path.join(bin,name+'.tar.br'); if(!exists(source))continue;
   const tar=path.join(out,name+'.tar');fs.writeFileSync(tar,zlib.brotliDecompressSync(fs.readFileSync(source)));
   const r=run('tar',['--no-same-owner','-xf',tar,'-C',out]);if(r.status!==0)throw Error(r.stderr);fs.unlinkSync(tar);
  }
 }
}
const installedVersion=(name)=>{try{return JSON.parse(fs.readFileSync(path.join(runtime,'node_modules',name,'package.json'),'utf8')).version}catch{return null}};
const checks={node:{version:process.version,ready:true},ffmpeg:{ready:run('ffmpeg',['-version']).status===0},ffprobe:{ready:run('ffprobe',['-version']).status===0},hyperframes:{ready:exists(moduleFile),version:installedVersion('hyperframes')},gsap:{ready:exists(path.join(runtime,'node_modules/gsap/dist/gsap.min.js')),version:installedVersion('gsap')},plugins:{},browser:{path:browser||null,ready:false},runtime,project,networkUsed:online};
for(const p of ['DrawSVGPlugin','MorphSVGPlugin','MotionPathPlugin','SplitText']) checks.plugins[p]=exists(path.join(runtime,'node_modules/gsap/dist',p+'.min.js'));
if(exists(browser)){
 const version=run(browser,['--version'],{timeout:15000});checks.browser.version=(version.stdout||version.stderr||'').trim();
 try{
  const {default:puppeteer}=await import(pathToFileURL(path.join(runtime,'node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js')));
  const instance=await puppeteer.launch({executablePath:browser,headless:true,args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu'],timeout:20000});
  const page=await instance.newPage();await page.setContent('<p id="probe">ready</p>');checks.browser.ready=await page.$eval('#probe',e=>e.textContent==='ready');await instance.close();
 }catch(err){checks.browser.error=String(err)}
 if(checks.browser.ready&&(online||offline)){fs.mkdirSync(runtime,{recursive:true});fs.writeFileSync(savedBrowser,browser+'\n');}
}
const expected=JSON.parse(fs.readFileSync(path.join(project,'package.json'),'utf8')).dependencies;
checks.lockMatch={hyperframes:checks.hyperframes.version===expected.hyperframes,gsap:checks.gsap.version===expected.gsap};
checks.ready=Object.values(checks.lockMatch).every(Boolean)&&checks.node.ready&&checks.ffmpeg.ready&&checks.ffprobe.ready&&checks.hyperframes.ready&&checks.gsap.ready&&Object.values(checks.plugins).every(Boolean)&&checks.browser.ready;
console.log(JSON.stringify(checks,null,2));
if(!checks.ready) process.exitCode=1;
