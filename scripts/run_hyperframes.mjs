#!/usr/bin/env node
// Invoke the pinned local CLI. Never use npx or download at render time.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
const runtime = path.resolve(process.env.KM_HYPERFRAMES_RUNTIME || path.join(os.homedir(), '.cache/km-video-hyperframes/0.9.4'));
const cli = path.join(runtime, 'node_modules/hyperframes/bin/hyperframes.mjs');
if (!fs.existsSync(cli)) throw Error('Run setup_hyperframes.mjs during setup; pinned local runtime is missing.');
const browserFile = path.join(runtime, 'browser-path.txt');
const browser = process.env.HYPERFRAMES_BROWSER_PATH || (fs.existsSync(browserFile) ? fs.readFileSync(browserFile, 'utf8').trim() : '');
if (process.argv[2] === 'render' && (!browser || !fs.existsSync(browser))) throw Error('Run HTML preflight; local browser is missing.');
const environmentFile=path.join(runtime,'runtime-env.json');
const savedEnvironment=fs.existsSync(environmentFile)?JSON.parse(fs.readFileSync(environmentFile,'utf8')):{};
const result = spawnSync(savedEnvironment.nodeExecutable||process.execPath, [cli, ...process.argv.slice(2)], {
  stdio: 'inherit',
  env: {...process.env, ...(savedEnvironment.binDirs?{PATH:[...savedEnvironment.binDirs,process.env.PATH].join(path.delimiter)}:{}), HYPERFRAMES_NO_UPDATE_CHECK: '1', HYPERFRAMES_NO_TELEMETRY: '1', ...(browser ? {HYPERFRAMES_BROWSER_PATH: browser} : {})}
});
if (result.error) throw result.error;
process.exitCode = result.status ?? 1;
