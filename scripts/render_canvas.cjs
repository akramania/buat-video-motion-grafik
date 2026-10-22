#!/usr/bin/env node
'use strict';
// Offline, deterministic HTML/SVG/Canvas -> PNG frames -> FFmpeg MP4.
// Page contract: renderFrame(tSeconds) redraws from absolute time, optionally
// returns a Promise, and must not depend on a preceding frame, timers, or a CDN.
const fs = require('node:fs/promises');
const path = require('node:path');
const http = require('node:http');
const { spawn } = require('node:child_process');

function parseArgs(argv) {
  const out = { width: 1920, height: 1080, fps: 30, duration: 5, overwrite: false };
  const known = new Set(['html', 'output', 'width', 'height', 'fps', 'duration']);
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--overwrite') { out.overwrite = true; continue; }
    if (arg === '--help') { out.help = true; continue; }
    const key = arg.slice(2);
    if (!arg.startsWith('--') || !known.has(key) || !argv[i + 1] || argv[i + 1].startsWith('--'))
      throw new Error(`Unknown option or missing value: ${arg}`);
    out[key] = ['html', 'output'].includes(key) ? argv[++i] : Number(argv[++i]);
  }
  if (out.help) return out;
  if (!out.html || !out.output) throw new Error('--html and --output are required');
  for (const key of ['width', 'height'])
    if (!Number.isInteger(out[key]) || out[key] < 2 || out[key] > 8192 || out[key] % 2)
      throw new Error(`${key} must be an even integer from 2 to 8192 (yuv420p)`);
  if (!Number.isInteger(out.fps) || out.fps < 1 || out.fps > 120)
    throw new Error('fps must be an integer from 1 to 120');
  if (!Number.isFinite(out.duration) || out.duration <= 0 || Math.round(out.duration * out.fps) < 1)
    throw new Error('duration must be positive and produce at least one frame');
  if (path.extname(out.output).toLowerCase() !== '.mp4') throw new Error('output must end in .mp4');
  return out;
}

async function scopedServer(html) {
  const realHtml = await fs.realpath(html);
  if (!(await fs.stat(realHtml)).isFile()) throw new Error('html must be a file');
  const root = path.dirname(realHtml);
  const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.cjs': 'text/javascript',
    '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.woff': 'font/woff', '.woff2': 'font/woff2',
    '.ttf': 'font/ttf', '.json': 'application/json', '.wasm': 'application/wasm' };
  const server = http.createServer(async (req, res) => {
    try {
      if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405); res.end(); return; }
      const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
      const candidate = path.resolve(root, `.${pathname}`);
      if (candidate !== root && !candidate.startsWith(root + path.sep)) { res.writeHead(403); res.end(); return; }
      const actual = await fs.realpath(candidate);
      if (!actual.startsWith(root + path.sep) || !(await fs.stat(actual)).isFile()) {
        res.writeHead(403); res.end(); return;
      }
      res.writeHead(200, {
        'Content-Type': mime[path.extname(actual).toLowerCase()] || 'application/octet-stream',
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff',
        'Content-Security-Policy': "default-src 'self' data: blob:; script-src 'self' 'unsafe-inline' 'unsafe-eval' data: blob:; style-src 'self' 'unsafe-inline'; connect-src 'self'; worker-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'"
      });
      res.end(req.method === 'HEAD' ? undefined : await fs.readFile(actual));
    } catch { if (!res.headersSent) res.writeHead(404); res.end(); }
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  const origin = `http://127.0.0.1:${server.address().port}`;
  return { server, origin, url: `${origin}/${encodeURIComponent(path.basename(realHtml))}` };
}

async function preparePage(browser, options, host) {
  const context = await browser.newContext({ viewport: { width: options.width, height: options.height },
    deviceScaleFactor: 1, reducedMotion: 'reduce', serviceWorkers: 'block', acceptDownloads: false });
  const blocked = [];
  await context.route('**/*', route => {
    const url = route.request().url();
    const allowed = url.startsWith('data:') || url.startsWith('blob:') || new URL(url).origin === host.origin;
    if (allowed) return route.continue();
    blocked.push(url);
    return route.abort('blockedbyclient');
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  // Pause browser timers; only explicit renderFrame(t) calls drive the scene.
  await page.clock.install({ time: new Date('2000-01-01T00:00:00Z') });
  await page.goto(host.url, { waitUntil: 'load' });
  await page.clock.pauseAt(new Date('2000-01-01T01:00:00Z'));
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(img => img.decode()));
    if (typeof window.renderFrame !== 'function') throw new Error('HTML must expose window.renderFrame(tSeconds)');
  });
  const check = () => {
    if (blocked.length) throw new Error(`Nonlocal requests blocked: ${blocked.join(', ')}`);
    if (errors.length) throw new Error(`Page error: ${errors.join('; ')}`);
  };
  check();
  return { page, context, check };
}

async function captureFrame(prepared, seconds) {
  prepared.check();
  await prepared.page.evaluate(async t => { await window.renderFrame(t); }, seconds);
  prepared.check();
  return prepared.page.screenshot({ type: 'png', fullPage: false, caret: 'hide' });
}

async function render(options) {
  const output = path.resolve(options.output);
  await fs.mkdir(path.dirname(output), { recursive: true });
  if (!options.overwrite) {
    try { await fs.lstat(output); throw new Error(`Output exists; use --overwrite: ${output}`); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  const frames = Math.round(options.duration * options.fps);
  let host, browser, encoder, encoderDone, temporaryDir;
  let encoderResult, stderr = '', interrupted;
  const stop = signal => {
    interrupted = new Error(`Interrupted by ${signal}`);
    if (browser) browser.close().catch(() => {});
    if (encoder) encoder.kill('SIGTERM');
  };
  const onInt = () => stop('SIGINT'), onTerm = () => stop('SIGTERM');
  process.once('SIGINT', onInt); process.once('SIGTERM', onTerm);
  try {
    host = await scopedServer(options.html);
    const { chromium } = require('playwright');
    const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
    browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}),
      args: ['--disable-background-networking'] });
    const prepared = await preparePage(browser, options, host);
    if (interrupted) throw interrupted;
    temporaryDir = await fs.mkdtemp(path.join(path.dirname(output), '.canvas-render-'));
    const temporary = path.join(temporaryDir, 'render.mp4');
    const args = ['-hide_banner', '-loglevel', 'error', '-n', '-f', 'image2pipe', '-vcodec', 'png',
      '-framerate', String(options.fps), '-i', 'pipe:0', '-an', '-c:v', 'libx264', '-preset', 'medium',
      '-crf', '18', '-pix_fmt', 'yuv420p', '-vf', 'setsar=1', '-frames:v', String(frames), '-movflags', '+faststart', temporary];
    encoder = spawn('ffmpeg', args, { stdio: ['pipe', 'ignore', 'pipe'], shell: false });
    encoder.stdin.on('error', () => {}); // write callbacks propagate EPIPE without an uncaught event.
    encoder.stderr.on('data', chunk => { stderr = (stderr + chunk).slice(-8000); });
    encoderDone = new Promise(resolve => {
      encoder.once('error', error => { encoderResult = { error }; resolve(encoderResult); });
      encoder.once('close', (code, signal) => { encoderResult = { code, signal }; resolve(encoderResult); });
    });
    for (let i = 0; i < frames; i++) {
      if (interrupted) throw interrupted;
      if (encoderResult) throw new Error(`FFmpeg stopped: ${encoderResult.error || stderr || encoderResult.code}`);
      const png = await captureFrame(prepared, i / options.fps);
      // One awaited write callback per frame bounds buffering and honors pipe backpressure.
      await new Promise((resolve, reject) => encoder.stdin.write(png, error => error ? reject(error) : resolve()));
    }
    encoder.stdin.end();
    const result = await encoderDone;
    if (result.error || result.code !== 0) throw new Error(`FFmpeg failed: ${result.error || stderr || result.signal || result.code}`);
    if (options.overwrite) await fs.rename(temporary, output);
    else { await fs.link(temporary, output); await fs.unlink(temporary); } // Atomic no-clobber publication.
    return { output, frames, fps: options.fps, duration: frames / options.fps, width: options.width, height: options.height };
  } finally {
    process.removeListener('SIGINT', onInt); process.removeListener('SIGTERM', onTerm);
    if (encoder && !encoderResult) {
      encoder.kill('SIGTERM');
      const force = setTimeout(() => encoder.kill('SIGKILL'), 2000);
      await encoderDone; clearTimeout(force);
    }
    if (browser) await browser.close().catch(() => {});
    if (host) {
      host.server.closeAllConnections();
      await new Promise(resolve => host.server.close(resolve));
    }
    if (temporaryDir) await fs.rm(temporaryDir, { recursive: true, force: true });
  }
}

module.exports = { parseArgs, scopedServer, preparePage, captureFrame, render };
if (require.main === module) {
  (async () => {
    const options = parseArgs(process.argv.slice(2));
    if (options.help) {
      console.log('node render_canvas.cjs --html scene.html --output video.mp4 [--width 1920 --height 1080 --fps 30 --duration 5 --overwrite]');
      return;
    }
    console.log(JSON.stringify(await render(options)));
  })().catch(error => { console.error(`Render failed: ${error.message}`); process.exitCode = 1; });
}
