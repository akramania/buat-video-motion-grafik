#!/usr/bin/env node
// Module and CPU checks only; this does not validate a browser or video render.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';
const runtime=path.resolve(process.argv[2]);
const require=createRequire(path.join(runtime,'package.json'));
const React=require('react'), dom=require('react-dom/server');
if(dom.renderToStaticMarkup(React.createElement('h1',null,'Motion'))!=='<h1>Motion</h1>')throw Error('React server render failed');
const THREE=await import(pathToFileURL(path.join(runtime,'node_modules/three/build/three.module.js')));
const geometry=new THREE.BoxGeometry(), material=new THREE.MeshBasicMaterial();
const mesh=new THREE.Mesh(geometry,material);mesh.rotation.y=.5;mesh.updateMatrixWorld();
if(!mesh.matrixWorld.elements.every(Number.isFinite))throw Error('Three.js matrix check failed');
for(const name of ['remotion','@remotion/renderer','@remotion/bundler','gsap/dist/gsap','gsap/dist/DrawSVGPlugin','gsap/dist/MorphSVGPlugin','gsap/dist/MotionPathPlugin','gsap/dist/SplitText'])require(name);
geometry.dispose();material.dispose();
console.log(JSON.stringify({ready:true,react:React.version,three:THREE.REVISION,remotion:JSON.parse(fs.readFileSync(path.join(runtime,'node_modules/remotion/package.json'),'utf8')).version,checks:['module imports','React static markup','Three.js finite scene matrix'],browserRenderTested:false}));
