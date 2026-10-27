#!/usr/bin/env python3
"""Maintenance: lock Atlas code/fonts/defaults and sample native-frame baselines.

Rebuild only after reviewing a deliberate backend change. Runtime never rebuilds
this file automatically. Published MP4 parity is a separate verify --reference step.
"""
import argparse
import ast
import base64
from concurrent.futures import ProcessPoolExecutor
import hashlib
import importlib
import json
import zlib
from pathlib import Path

from atlas_preset import (AtlasLibrary, LOCK, RENDERER, allowed_parameters, digest, canonical,
                          environment, source_hashes, write_json, read_contract)


def requirements(module, pid):
    if not pid.startswith('CFX'):
        return [], False
    tree = ast.parse((RENDERER / (module + '.py')).read_text())
    compose = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'compose')
    index = int(pid[3:])
    branch = None
    for node in ast.walk(compose):
        if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
            continue
        test = node.test
        if not isinstance(test.left, ast.Name) or test.left.id != 'k' or len(test.comparators) != 1:
            continue
        if not isinstance(test.ops[0], (ast.Eq, ast.In)):
            continue
        value = test.comparators[0]
        values = [value.value] if isinstance(value, ast.Constant) else [x.value for x in value.elts] if isinstance(value, (ast.Tuple, ast.List)) else []
        if index in values:
            branch = ast.Module(body=node.body, type_ignores=[])
            break
    if branch is None:
        return [], False
    names = {n.id for n in ast.walk(branch) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
    layers = []
    if 'person' in names:
        layers.append('subject')
    if 'backdrop' in names:
        layers.append('backdrop')
    if pid == 'CFX15':
        layers = []  # its demo-only room branch is skipped when footage is supplied
    return layers, bool(names & {'card_at', 'thumb', 'media', 'asset'})


def samples(pid):
    lib = AtlasLibrary(verify=False)
    cfg = lib.render.configuration(pid)
    duration = cfg['duration']
    result = []
    for fraction in (.13, .47, .83):
        seconds = duration * fraction
        im = lib.render.frame(pid, seconds, cfg, False)
        result.append({'seconds': seconds, 'mode': im.mode, 'sha256': hashlib.sha256(im.tobytes()).hexdigest()})
    return pid, result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--goldens', choices=['all', 'none'], default='all')
    ap.add_argument('--jobs', type=int, default=2)
    ap.add_argument('--reuse-goldens', action='store_true', help='Reuse native baselines only when all backend bytes, registry and environment are unchanged')
    args = ap.parse_args()
    if not 1 <= args.jobs <= 8:
        ap.error('--jobs must be 1..8')
    lib = AtlasLibrary(verify=False)
    files = source_hashes()
    presets = {}
    for pid, meta in lib.registry.items():
        module = lib.dispatch[pid].__module__
        layers, images = requirements(module, pid)
        presets[pid] = {'module': module, 'defaults_sha256': digest(meta),
                        'allowed_params': allowed_parameters(pid, meta, module),
                        'required_layers': layers, 'requires_image_assets': images,
                        'native_canvas': [1280, 720], 'time_mode': meta.get('time_mode', 'normalized'),
                        'default_duration': meta.get('duration',5)}
    contract = {'schema_version': 1, 'package_sha256': digest(files), 'files': files,
                'registry_sha256': digest(lib.registry), 'environment': environment(),
                'preset_count': len(presets), 'presets': presets, 'goldens': {},
                'baseline_scope': 'original Python clean native frames; not a certification of published Atlas MP4 files'}
    if args.reuse_goldens:
        previous = read_contract()
        if previous['files'] != files or previous['registry_sha256'] != contract['registry_sha256'] or previous['environment'] != environment():
            raise RuntimeError('Cannot reuse baselines after a backend/default/environment change')
        if set(previous['goldens']) != set(presets):
            raise RuntimeError('Existing baselines are incomplete')
        contract['goldens'] = previous['goldens']
    elif args.goldens == 'all':
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            for i, (pid, rows) in enumerate(pool.map(samples, sorted(presets), chunksize=6), 1):
                contract['goldens'][pid] = rows
                if i % 50 == 0 or i == len(presets):
                    print(f'Baseline {i}/{len(presets)}', flush=True)
    if source_hashes() != files:
        raise RuntimeError('Backend changed during baseline generation; review and rebuild')
    # Deduplicate parameter schemas and store only the three raw pixel hashes.
    # Runtime expands this losslessly before exposing the public contract API.
    compact = dict(contract, storage_format='compact-v1', parameter_sets=[], sample_fractions=[.13,.47,.83])
    compact['presets'] = {}
    compact['goldens'] = {}
    for pid, item in presets.items():
        fields = item['allowed_params']
        if fields not in compact['parameter_sets']:
            compact['parameter_sets'].append(fields)
        entry = dict(item, parameter_schema=compact['parameter_sets'].index(fields))
        del entry['allowed_params']
        compact['presets'][pid] = entry
        compact['goldens'][pid] = [row['sha256'] for row in contract['goldens'].get(pid, [])]
    raw = canonical(compact)
    envelope = {'schema_version': 1, 'storage_format': 'zlib-base64-v1',
                'package_sha256': contract['package_sha256'], 'preset_count': len(presets),
                'payload_sha256': hashlib.sha256(raw).hexdigest(),
                'payload': base64.b64encode(zlib.compress(raw, 9)).decode('ascii')}
    write_json(LOCK, envelope, compact=True)
    print(json.dumps({'contract': str(LOCK), 'presets': len(presets), 'goldens': len(contract['goldens']), 'package_sha256': contract['package_sha256']}))


if __name__ == '__main__':
    main()
