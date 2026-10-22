#!/usr/bin/env node
'use strict';
// Trusted LOCAL CommonJS scene -> @napi-rs/canvas -> sequential PNG pipe -> MP4.
// Required: renderFrame(ctx, tSeconds, width, height), optionally async.
// Optional: prepare({canvas,ctx,width,height,fps,duration,sceneDirectory}), dispose().
// Motion is an absolute-time function; prepare may load assets, not start timers.
const fs = require('node:fs/promises');
const path = require('node:path');
const { spawn } = require('node:child_process');
const { parseArgs } = require('./render_canvas.cjs');

function parseNativeArgs(argv) {
  const args = parseArgs(argv.map(arg => arg === '--scene' ? '--html' : arg));
  args.scene = args.html; delete args.html;
  return args;
}

async function renderNative(options) {
  const { createCanvas } = require('@napi-rs/canvas');
  const scenePath = await fs.realpath(options.scene);
  if (!(await fs.stat(scenePath)).isFile()) throw new Error('scene must be a local CommonJS file');
  const output = path.resolve(options.output);
  await fs.mkdir(path.dirname(output), { recursive: true });
  if (!options.overwrite) {
    try { await fs.lstat(output); throw new Error(`Output exists; use --overwrite: ${output}`); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  const scene = require(scenePath);
  if (typeof scene.renderFrame !== 'function') throw new Error('Scene must export renderFrame(ctx,t,width,height)');
  const canvas = createCanvas(options.width, options.height);
  const ctx = canvas.getContext('2d');
  const frames = Math.round(options.duration * options.fps);
  let encoder, done, result, temporaryDir, stderr = '', interrupted;
  const onSignal = () => { interrupted = new Error('Render interrupted'); if (encoder) encoder.kill('SIGTERM'); };
  process.once('SIGINT', onSignal); process.once('SIGTERM', onSignal);
  try {
    if (scene.prepare) await scene.prepare({ canvas, ctx, width: options.width, height: options.height,
      fps: options.fps, duration: frames / options.fps, sceneDirectory: path.dirname(scenePath) });
    if (interrupted) throw interrupted;
    temporaryDir = await fs.mkdtemp(path.join(path.dirname(output), '.native-canvas-render-'));
    const temporary = path.join(temporaryDir, 'render.mp4');
    const args = ['-hide_banner', '-loglevel', 'error', '-n', '-f', 'image2pipe', '-vcodec', 'png',
      '-framerate', String(options.fps), '-i', 'pipe:0', '-an', '-c:v', 'libx264', '-preset', 'medium',
      '-crf', '18', '-pix_fmt', 'yuv420p', '-vf', 'setsar=1', '-frames:v', String(frames), '-movflags', '+faststart', temporary];
    encoder = spawn('ffmpeg', args, { stdio: ['pipe', 'ignore', 'pipe'], shell: false });
    encoder.stdin.on('error', () => {});
    encoder.stderr.on('data', chunk => { stderr = (stderr + chunk).slice(-8000); });
    done = new Promise(resolve => {
      encoder.once('error', error => { result = { error }; resolve(result); });
      encoder.once('close', (code, signal) => { result = { code, signal }; resolve(result); });
    });
    for (let i = 0; i < frames; i++) {
      if (interrupted) throw interrupted;
      if (result) throw new Error(`FFmpeg stopped: ${result.error || stderr || result.code}`);
      // Reset the full drawing state for each independently rendered frame.
      canvas.width = options.width; canvas.height = options.height;
      await scene.renderFrame(ctx, i / options.fps, options.width, options.height);
      const png = canvas.toBuffer('image/png');
      await new Promise((resolve, reject) => encoder.stdin.write(png, error => error ? reject(error) : resolve()));
    }
    encoder.stdin.end();
    result = await done;
    if (result.error || result.code !== 0) throw new Error(`FFmpeg failed: ${result.error || stderr || result.signal || result.code}`);
    if (options.overwrite) await fs.rename(temporary, output);
    else { await fs.link(temporary, output); await fs.unlink(temporary); }
    return { output, frames, fps: options.fps, duration: frames / options.fps, width: options.width,
      height: options.height, backend: '@napi-rs/canvas', audio: false };
  } finally {
    process.removeListener('SIGINT', onSignal); process.removeListener('SIGTERM', onSignal);
    if (encoder && !result) {
      encoder.kill('SIGTERM');
      const force = setTimeout(() => encoder.kill('SIGKILL'), 2000);
      await done; clearTimeout(force);
    }
    if (temporaryDir) await fs.rm(temporaryDir, { recursive: true, force: true });
    if (scene.dispose) await scene.dispose();
  }
}

module.exports = { parseNativeArgs, renderNative };
if (require.main === module) {
  (async () => {
    const args = parseNativeArgs(process.argv.slice(2));
    if (args.help) {
      console.log('node render_native_canvas.cjs --scene scene.cjs --output video.mp4 [--width 1920 --height 1080 --fps 30 --duration 5 --overwrite]');
      return;
    }
    console.log(JSON.stringify(await renderNative(args)));
  })().catch(error => { console.error(`Render failed: ${error.message}`); process.exitCode = 1; });
}
