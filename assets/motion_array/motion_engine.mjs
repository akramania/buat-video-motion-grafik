// Original vector adaptations inspired by observed public Motion Array previews.
import * as shapes from './shapes/engine.mjs';
import * as hud from './hud/engine.mjs';
import * as transitions from './transitions/engine.mjs';
import * as particles from './particles/engine.mjs';
const engines={shapes,hud,transitions,particles};
const data=Object.values(engines).flatMap(e=>e.records());
const byId=new Map(data.map(r=>[r.id,r]));
export const records=()=>data.map(r=>structuredClone(r));
export function render(recipe,t,options={}){const r=typeof recipe==='string'?byId.get(recipe):recipe;if(!r||!engines[r.group])throw Error('Unknown MA component');return engines[r.group].render(r,t,options);}
export function customize(id,parameters={}){
 const base=byId.get(id);if(!base)throw Error('Unknown MA component');
 function value(input,original,key){if(typeof original==='number'){if(typeof input!=='number'||!Number.isFinite(input)||Math.abs(input)>1e7)throw Error('Invalid numeric parameter '+key);if(/count|population|rows|columns|lobes|arms|layers|segments/i.test(key)&&(!Number.isInteger(input)||input<1||input>256))throw Error('Invalid component population');if(/variant|adaptation_index/.test(key)&&(!Number.isInteger(input)||input<0||input>19))throw Error('Invalid variation');if(key==='recipe'&&(!Number.isInteger(input)||input<1||input>20))throw Error('Invalid recipe');if(key==='mechanism_index'&&input!==original)throw Error('Mechanism index must match ID');return input;}
 if(Array.isArray(original)){if(!Array.isArray(input)||input.length<1||input.length>32)throw Error('Invalid parameter array');return input.map((x,i)=>value(x,original[Math.min(i,original.length-1)],key));}
 if(typeof original==='string'){const allowed=new Set(data.filter(r=>r.group===base.group).map(r=>r.parameters[key]));if(typeof input!=='string'||!allowed.has(input))throw Error('Invalid layout');return input;}throw Error('Unsupported parameter');}
 const out={...base,parameters:structuredClone(base.parameters)};for(const[k,v]of Object.entries(parameters)){if(!(k in base.parameters))throw Error('Unknown parameter '+k);out.parameters[k]=value(v,base.parameters[k],k);}return out;
}
function body(svg,prefix){const m=svg.match(/^\s*<svg\b[^>]*>([\s\S]*)<\/svg>\s*$/);if(!m)throw Error('Renderer returned malformed SVG');return m[1].replace(/\bid="([^"]+)"/g,(_,id)=>`id="${prefix}${id}"`).replace(/url\(#([^)]+)\)/g,(_,id)=>`url(#${prefix}${id})`).replace(/\b(?:href|xlink:href)="#([^"]+)"/g,(_,id)=>`href="#${prefix}${id}"`);}
const number=(x,d)=>Number.isFinite(Number(x))?Number(x):d;
export function compose(scene,t,{width=1920,height=1080,transparent=false}={}){
 if(!Array.isArray(scene.layers)||scene.layers.length>100)throw Error('Scene requires up to100 layers');
 const bg=transparent?'':`<rect width="640" height="360" fill="#08131c"/>`;
 const layers=scene.layers.map((l,i)=>{const r=l.parameters?customize(l.id,l.parameters):byId.get(l.id);if(!r)throw Error('Unknown layer '+l.id);const start=number(l.start,0),duration=number(l.duration,r.duration);if(t<start||t>=start+duration)return '';
 const local=(t-start)*r.duration/duration,x=number(l.x,0),y=number(l.y,0),scale=number(l.scale,1),opacity=Math.max(0,Math.min(1,number(l.opacity,1)));if(scale<=0||scale>10||duration<=0)throw Error('Invalid layer size/duration');
 const svg=render(r,local,{width:640,height:360,transparent:true});return `<g opacity="${opacity}" transform="translate(${x} ${y}) scale(${scale})">${body(svg,`L${i}_`)}</g>`;}).join('');
 return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 640 360">${bg}${layers}</svg>`;
}
