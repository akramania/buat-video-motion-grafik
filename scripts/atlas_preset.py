#!/usr/bin/env python3
"""Locked, cached access to the original Atlas Python renderers.

Run --help. Import AtlasPreset for prepared-frame compositing in an editor.
No browser, network, inference model, or reimplementation of a preset is used.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import importlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zlib
from fractions import Fraction

import numpy as np
from PIL import Image, __version__ as PILLOW_VERSION

SKILL = Path(__file__).resolve().parents[1]
RENDERER = SKILL / 'assets/motion_presets'
if not RENDERER.is_dir():
    RENDERER = SKILL / 'renderer'
LOCK = RENDERER / 'atlas_contract.json'
SCHEMA = 1
COLORS = {'bg', 'panel', 'text_color', 'muted', 'accent', 'secondary'}
COMMON = {'text', 'subtitle', 'genre'} | COLORS
CONTENT = {'asset', 'image_path', 'image_paths', 'subject_path', 'background_path',
           'freeze_image_path', 'items', 'lines', 'labels', 'values', 'prefix',
           'suffix', 'value', 'from_value', 'to_value', 'decimals', 'grouping',
           'eyebrow', 'summary', 'summary_text', 'trail_label', 'value_suffix',
           'before_label', 'after_label', 'ready_label', 'processing_label',
           'complete_label', 'progress_label', 'sample_text', 'label_text',
           'support_text', 'band_text', 'window_subtitle', 'brand', 'cta', 'code',
           'prompt', 'thesis', 'price', 'from_year', 'to_year', 'unit', 'route',
           'route_points', 'compare_values', 'price_series', 'opening_price',
           'growth_rate', 'changes', 'show_titles', 'draft', 'caret'}
PATH_KEYS = {'asset', 'image_path', 'subject_path', 'background_path', 'freeze_image_path'}
EXTRA = {
    'T03': {'draft', 'caret'}, 'H04': {'value', 'decimals', 'prefix', 'suffix'},
    'A05': {'image_path'}, 'B02': {'asset'}, 'K25': {'asset'},
    'B04': {'from_value', 'to_value', 'prefix', 'suffix', 'decimals', 'grouping'},
    'B07': {'from_value', 'to_value', 'prefix', 'suffix', 'decimals', 'grouping'},
    'CFX15': {'lines', 'scroll_mode'}, 'CFX37': {'price'},
    'CFX63': {'route_points', 'image_path'}, 'CFX64': {'from_year', 'to_year'},
    'CFX73': {'lines'},
}
IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tif', '.tiff'}


class AtlasError(ValueError):
    pass


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def source_files(root=RENDERER):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.name != LOCK.name
                  and p.suffix.lower() in {'.py', '.json', '.geojson', '.ttf', '.otf'})


def source_hashes(root=RENDERER):
    return {p.relative_to(root).as_posix(): file_hash(p) for p in source_files(root)}


def environment():
    return {'python': '.'.join(map(str, sys.version_info[:2])),
            'pillow': PILLOW_VERSION, 'numpy': np.__version__}


def finite(value, name, lo=None, hi=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise AtlasError(name + ' must be a finite number')
    if lo is not None and value < lo or hi is not None and value > hi:
        raise AtlasError(f'{name} must be within {lo}..{hi}')
    return float(value)


def keys_only(value, allowed, name):
    if not isinstance(value, dict):
        raise AtlasError(name + ' must be an object')
    unknown = set(value) - set(allowed)
    if unknown:
        raise AtlasError(name + ': unsupported fields ' + ', '.join(sorted(unknown)))


def write_json(path, data, compact=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + f'.{os.getpid()}.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=None if compact else 2,
                              separators=(',', ':') if compact else None, allow_nan=False) + '\n')
    os.replace(tmp, path)


def read_contract():
    data = json.loads(LOCK.read_text())
    if data.get('storage_format') == 'zlib-base64-v1':
        envelope = data
        try:
            raw = zlib.decompress(base64.b64decode(envelope['payload'], validate=True))
            if hashlib.sha256(raw).hexdigest() != envelope['payload_sha256']:
                raise AtlasError('Contract payload checksum differs')
            data = json.loads(raw)
            if data['package_sha256'] != envelope['package_sha256']:
                raise AtlasError('Contract envelope package differs')
        except (ValueError, zlib.error, KeyError) as error:
            raise AtlasError('Invalid compressed Atlas contract') from error
    if data.get('storage_format') == 'compact-v1':
        for pid, item in data['presets'].items():
            item['allowed_params'] = list(data['parameter_sets'][item['parameter_schema']])
            data['goldens'][pid] = [
                {'seconds': item['default_duration'] * fraction, 'mode': 'RGB', 'sha256': sha}
                for fraction, sha in zip(data['sample_fractions'], data['goldens'][pid])]
    return data


def backend():
    # Load from the verified directory rather than a module in a caller's cwd.
    if str(RENDERER) not in sys.path:
        sys.path.insert(0, str(RENDERER))
    mod = importlib.import_module('render')
    if Path(mod.__file__).resolve() != (RENDERER / 'render.py').resolve():
        raise AtlasError('Another render module is loaded; use an isolated Python process')
    return mod


def allowed_parameters(pid, metadata, module):
    # Deliberately conservative: animation internals remain at their source defaults.
    declared = metadata.get('parameters', [])
    fields = COMMON | (set(metadata) & CONTENT) | (set(declared) & CONTENT) | EXTRA.get(pid, set())
    if module == 'carousels':
        fields.add('image_paths')
    if module == 'motionprompt':
        fields |= {'asset', 'image_path', 'image_paths', 'items'}
    if pid in {'CFX01', 'CFX02', 'CFX13'}:
        fields |= {'focus_x', 'focus_y', 'amount'}
    if pid.startswith('CFX'):
        fields.add('presentation')
    return sorted(fields)


class AtlasLibrary:
    def __init__(self, verify=True):
        self.contract = read_contract() if LOCK.is_file() else None
        if verify:
            if not self.contract:
                raise AtlasError('Atlas contract is missing; restore the complete skill toolkit')
            actual = source_hashes()
            if actual != self.contract['files']:
                changed = sorted(k for k in set(actual) | set(self.contract['files'])
                                 if actual.get(k) != self.contract['files'].get(k))
                raise AtlasError('Renderer package changed; review and rebuild the contract: ' + ', '.join(changed[:8]))
            if digest(actual) != self.contract['package_sha256']:
                raise AtlasError('Invalid package fingerprint')
        self.render = backend()
        self.registry, self.dispatch = self.render.registry()  # exactly once per session
        if verify and digest(self.registry) != self.contract['registry_sha256']:
            raise AtlasError('Registry differs from the locked contract')
        self.environment = environment()
        self._verified_baselines = set()
        self._asset_fingerprints = {}

    def refresh_assets(self, paths):
        hashes = {str(p): file_hash(p) for p in paths}
        if any(self._asset_fingerprints.get(p) != h for p, h in hashes.items()):
            # Original loaders cache by path. A replaced image at the same path
            # must invalidate that loader as well as the rendered-video cache.
            for module_name, function_name in [('creator_fx', 'image_asset'), ('motionprompt', '_asset'),
                                                ('premium_ui_product', 'loaded_image'), ('premium_promo_fx', '_load'),
                                                ('new_a', '_image_asset')]:
                module = importlib.import_module(module_name)
                getattr(module, function_name).cache_clear()
        self._asset_fingerprints.update(hashes)

    def verify_baseline(self, pid):
        if pid in self._verified_baselines:
            return
        samples = self.contract.get('goldens', {}).get(pid, [])
        if not samples:
            raise AtlasError('No native-frame baseline for ' + pid + '; restore or certify the complete package')
        cfg = self.render.configuration(pid)
        for sample in samples:
            im = self.render.frame(pid, sample['seconds'], cfg, False)
            if hashlib.sha256(im.tobytes()).hexdigest() != sample['sha256']:
                raise AtlasError('Native baseline mismatch for ' + pid + '; check Pillow/NumPy/fonts before rendering')
        self._verified_baselines.add(pid)

    def describe(self, pid):
        if pid not in self.registry:
            raise AtlasError('Unknown Atlas preset: ' + pid)
        meta = self.registry[pid]
        contract = self.contract['presets'].get(pid, {}) if self.contract else {}
        return {'id': pid, 'name': meta['name'], 'mechanism': meta.get('mechanism', meta['description']),
                'renderer': self.dispatch[pid].__module__ + '.render',
                'native_canvas': [1280, 720], 'native_portrait': False,
                'time_mode': meta.get('time_mode', 'normalized'),
                'defaults': {k: meta[k] for k in contract.get('allowed_params', []) if k in meta},
                'allowed_params': contract.get('allowed_params', allowed_parameters(pid, meta, self.dispatch[pid].__module__)),
                'cue_seconds': ['line_cues'] if pid == 'CFX15' else ['freeze_at'] if pid == 'CFX12' else ['word_intervals'] if pid == 'B05'
                    else ['character_pauses'] if pid == 'B06' else sorted(meta.get('cue_defaults', {})),
                'footage_compose': pid.startswith('CFX'),
                'required_footage_layers': contract.get('required_layers', []),
                'requires_project_images': contract.get('requires_image_assets', False),
                'footage_restriction': 'reviewed before/after adapter required' if pid == 'CFX14'
                    else 'real echo history through the Python API required' if pid == 'CFX20' else None,
                'limitations': meta.get('limitations', 'Review changed content and placement on actual footage.')}

    def template(self, pid):
        info = self.describe(pid)
        meta = self.registry[pid]
        return {'schema_version': SCHEMA, 'preset': pid, 'mode': 'native',
                'params': {k: copy.deepcopy(meta[k]) for k in ('text', 'subtitle', 'genre')},
                'output': {'duration': meta.get('duration', 5), 'fps': 30, 'width': 960, 'transparent': False},
                'cue_seconds': {}, 'inputs': {},
                'reference': {'package_sha256': self.contract['package_sha256'],
                              'defaults_sha256': digest(meta)}}


class AtlasPreset:
    """One validated session; frame(seconds) always uses the original function.

    Prepared PIL RGBA frames can be passed to frame() in mode='footage'.
    Inputs remain caller-prepared: this API does not infer alpha or tracking.
    """
    def __init__(self, spec, library=None, base_dir=None):
        self.library = library or AtlasLibrary()
        self.spec = copy.deepcopy(spec)
        self.base_dir = Path(base_dir or Path.cwd()).resolve()
        keys_only(spec, {'schema_version', 'preset', 'mode', 'params', 'output', 'cue_seconds', 'inputs', 'reference'}, 'job')
        if type(spec.get('schema_version')) is not int or spec.get('schema_version') != SCHEMA:
            raise AtlasError('Unsupported schema_version')
        self.pid = spec.get('preset')
        if self.pid not in self.library.registry:
            raise AtlasError('Unknown Atlas preset: ' + str(self.pid))
        self.meta = self.library.registry[self.pid]
        self.contract = self.library.contract['presets'][self.pid]
        self.library.verify_baseline(self.pid)
        keys_only(spec.get('reference', {}), {'package_sha256', 'defaults_sha256'}, 'reference')
        if spec.get('reference') != {'package_sha256': self.library.contract['package_sha256'], 'defaults_sha256': digest(self.meta)}:
            raise AtlasError('Missing or stale reference; create the job using init for this package')
        self.mode = spec.get('mode', 'native')
        if self.mode not in ('native', 'footage'):
            raise AtlasError('mode must be native or footage')
        if self.mode == 'footage' and not self.pid.startswith('CFX'):
            raise AtlasError('Prepared footage compose is supported only by CFX; use native alpha layers for other presets')
        params = copy.deepcopy(spec.get('params', {}))
        if self.mode == 'footage':
            params.setdefault('presentation', 'full')
        keys_only(params, self.contract['allowed_params'], 'params')
        for k, v in params.items():
            self._validate_param(k, v)
        self.asset_paths = {}
        for k in PATH_KEYS:
            if params.get(k):
                params[k] = str(self._path(params[k]))
                self.asset_paths[k] = params[k]
        if params.get('image_paths'):
            params['image_paths'] = [str(self._path(p)) for p in params['image_paths']]
            for i, p in enumerate(params['image_paths']):
                self.asset_paths[f'image_paths/{i}'] = p
        for path in self.asset_paths.values():
            try:
                with Image.open(path) as image:
                    image.verify()
            except (OSError, ValueError) as error:
                raise AtlasError('Invalid image asset: ' + str(path)) from error
        self.library.refresh_assets(self.asset_paths.values())
        opts = spec.get('output', {})
        keys_only(opts, {'duration', 'fps', 'width', 'height', 'transparent', 'catalogue_labels'}, 'output')
        self.duration = finite(opts.get('duration', self.meta.get('duration', 5)), 'duration', self.meta.get('min_duration', .5), 120)
        self.fps = opts.get('fps', 30)
        if type(self.fps) is not int or self.fps not in (24, 25, 30, 50, 60):
            raise AtlasError('fps must be 24, 25, 30, 50 or 60')
        self.width = opts.get('width', 960)
        if type(self.width) is not int or not 320 <= self.width <= 3840 or self.width % 32:
            raise AtlasError('width must be 320..3840 and divisible by 32')
        self.height = self.width * 9 // 16
        if opts.get('height', self.height) != self.height:
            raise AtlasError('This preset has a locked 16:9 layout; a portrait layout requires a separately tested variant')
        self.transparent = opts.get('transparent', False)
        if type(self.transparent) is not bool:
            raise AtlasError('transparent must be boolean')
        self.labels = opts.get('catalogue_labels', False)
        if type(self.labels) is not bool or self.labels and (self.transparent or self.mode != 'native'):
            raise AtlasError('catalogue_labels requires opaque native mode')
        params['duration'] = self.duration
        params.update(self._convert_cues(spec.get('cue_seconds', {})))
        self.cfg = self.library.render.configuration(self.pid, params)
        self.cfg.update(_fps=self.fps, _duration=self.duration, _transparent=self.transparent, _labels=self.labels)
        if self.pid == 'CFX15':
            lines, cues = self.cfg['lines'], self.cfg['line_cues']
            if len(lines) != len(cues):
                raise AtlasError('Changed lines require matching cue_seconds.line_cues')
        if params.get('subject_path'):
            with Image.open(params['subject_path']) as subject:
                if 'A' not in subject.getbands() or subject.getchannel('A').getextrema()[0] == 255:
                    raise AtlasError('subject_path must contain genuine alpha transparency')
        self.fn = self.library.dispatch[self.pid]
        self.module = importlib.import_module(self.fn.__module__)
        self.inputs = copy.deepcopy(spec.get('inputs', {}))
        keys_only(self.inputs, {'footage', 'subject', 'backdrop', 'anchor_track'}, 'inputs')
        self.input_paths = {}
        for k, item in self.inputs.items():
            if k == 'anchor_track':
                if self.pid != 'CFX05':
                    raise AtlasError('anchor_track is supported by CFX05; do not infer tracking support for other presets')
                self._track(item)
                continue
            keys_only(item, {'path', 'start', 'fit'}, 'inputs.' + k)
            item['path'] = str(self._path(item.get('path')))
            finite(item.get('start', 0), k + '.start', 0)
            if item.get('fit', 'contain') != 'contain':
                raise AtlasError('Only contain is supported for prepared inputs; crop deliberately before using this wrapper')
            self.input_paths[k] = item['path']
        if self.mode == 'native' and self.inputs:
            raise AtlasError('inputs require mode=footage; native mode never silently ignores footage')
        self.sources = {}

    def _path(self, value):
        if not isinstance(value, str) or not value:
            raise AtlasError('Asset path must be a nonempty local path')
        p = Path(value).expanduser()
        p = (self.base_dir / p).resolve() if not p.is_absolute() else p.resolve()
        if not p.is_file():
            raise AtlasError('Missing asset: ' + str(p))
        return p

    def _validate_param(self, key, value):
        if key in COLORS:
            if not isinstance(value, str) or len(value) != 7 or not value.startswith('#'):
                raise AtlasError(key + ' must be #RRGGBB')
            try:
                int(value[1:], 16)
            except ValueError:
                raise AtlasError(key + ' must be #RRGGBB')
        elif key in PATH_KEYS:
            if not isinstance(value, str):
                raise AtlasError(key + ' must be a path string')
        elif key == 'image_paths':
            if not isinstance(value, list) or (not value and self.mode != 'native') or not all(isinstance(p, str) for p in value):
                raise AtlasError('image_paths must contain local paths (an empty list is allowed only for native demo defaults)')
        elif key in {'text', 'subtitle', 'draft', 'label_text', 'support_text', 'window_subtitle', 'band_text', 'price', 'prefix', 'suffix', 'unit', 'brand', 'cta', 'code', 'prompt', 'thesis'}:
            if not isinstance(value, str) or len(value) > 160:
                raise AtlasError(key + ' must be text of at most 160 characters')
        elif key in {'lines', 'items', 'labels'}:
            if not isinstance(value, list) or not value or not all(isinstance(x, str) and len(x) <= 160 for x in value):
                raise AtlasError(key + ' must be a nonempty list of short text')
        elif key in {'value', 'from_value', 'to_value', 'from_year', 'to_year', 'opening_price', 'growth_rate'}:
            finite(value, key)
        elif key in {'values', 'compare_values', 'price_series', 'changes'}:
            if not isinstance(value, list) or not value:
                raise AtlasError(key + ' must be a nonempty numeric list')
            for v in value:
                finite(v, key)
        elif key in {'focus_x', 'focus_y'}:
            finite(value, key, 0, 1)
        elif key == 'amount':
            finite(value, key, 0, 2)
        elif key == 'decimals':
            maximum = 3 if self.pid == 'H04' else 6
            if type(value) is not int or not 0 <= value <= maximum:
                raise AtlasError(f'decimals must be an integer 0..{maximum}')
        elif key in {'grouping', 'show_titles'} and type(value) is not bool:
            raise AtlasError(key + ' must be boolean')
        elif key == 'scroll_mode' and value not in {'list', 'lyrics'}:
            raise AtlasError('scroll_mode must be list or lyrics')
        elif key == 'presentation' and value not in {'full', 'preview'}:
            raise AtlasError('presentation must be full or preview')
        elif key == 'caret' and value not in {'vertical', 'underscore', 'bracket'}:
            raise AtlasError('caret must be vertical, underscore or bracket')
        # Reject NaN and non-JSON data even in structured source-supported fields.
        canonical(value)

    def _convert_cues(self, cues):
        if not isinstance(cues, dict):
            raise AtlasError('cue_seconds must be an object')
        if not cues:
            return {}
        factor = 1 if self.meta.get('time_mode') == 'seconds' else 5 / self.duration
        def second(v):
            return finite(v, 'cue seconds', 0, self.duration) * factor
        if self.pid == 'CFX12':
            keys_only(cues, {'freeze_at'}, 'cue_seconds')
            return {'freeze_at': second(cues.get('freeze_at'))}
        if self.pid == 'CFX15':
            keys_only(cues, {'line_cues'}, 'cue_seconds')
            values = cues.get('line_cues')
            if not isinstance(values, list) or not values:
                raise AtlasError('line_cues must be a nonempty list')
            result = [second(v) for v in values]
            if any(b <= a for a, b in zip(result, result[1:])):
                raise AtlasError('line_cues must increase strictly')
            lines = self.spec.get('params', {}).get('lines', self.meta['lines'])
            if len(result) != len(lines):
                raise AtlasError('line_cues and lines must have equal length')
            return {'line_cues': result}
        if self.pid == 'B05':
            keys_only(cues, {'word_intervals'}, 'cue_seconds')
            intervals = cues.get('word_intervals')
            words = self.spec.get('params', {}).get('text', self.meta['text']).split()
            if not isinstance(intervals, list) or len(intervals) != len(words):
                raise AtlasError('Provide one word interval per text word')
            result = []
            last = 0
            for item in intervals:
                keys_only(item, {'start', 'end'}, 'word interval')
                start, end = second(item.get('start')), second(item.get('end'))
                if not last <= start < end:
                    raise AtlasError('Word intervals must be ordered and non-overlapping')
                result.append({'start': start, 'end': end}); last = end
            return {'cues': result}
        if self.pid == 'B06':
            keys_only(cues, {'character_pauses'}, 'cue_seconds')
            pauses = cues.get('character_pauses')
            if not isinstance(pauses, list):
                raise AtlasError('character_pauses must be a list')
            result = []
            for item in pauses:
                keys_only(item, {'after_character', 'duration'}, 'character pause')
                pos = item.get('after_character')
                if type(pos) is not int or pos < 0:
                    raise AtlasError('after_character must be a nonnegative integer')
                result.append({'after_character': pos, 'duration': second(item.get('duration'))})
            if sum(p['duration'] for p in result) >= 2.95:
                raise AtlasError('Character pauses exceed the native timing budget')
            return {'pauses': result}
        allowed = self.meta.get('cue_defaults', {})
        keys_only(cues, allowed, 'cue_seconds')
        return {'cues': {k: second(v) for k, v in cues.items()}}

    def _track(self, track):
        if not isinstance(track, list) or not track:
            raise AtlasError('anchor_track must be a nonempty list of {time,x,y}')
        previous = -1
        for p in track:
            keys_only(p, {'time', 'x', 'y'}, 'anchor_track point')
            t = finite(p.get('time'), 'anchor time', 0, self.duration)
            finite(p.get('x'), 'anchor x', 0, 1280); finite(p.get('y'), 'anchor y', 0, 720)
            if t <= previous:
                raise AtlasError('Anchor times must increase strictly')
            previous = t

    def _anchor(self, seconds):
        track = self.inputs.get('anchor_track')
        if not track:
            return None
        if seconds <= track[0]['time']:
            return track[0]['x'], track[0]['y']
        for a, b in zip(track, track[1:]):
            if seconds <= b['time']:
                u = (seconds - a['time']) / (b['time'] - a['time'])
                return a['x'] + (b['x'] - a['x']) * u, a['y'] + (b['y'] - a['y']) * u
        return track[-1]['x'], track[-1]['y']

    def source_seconds(self, seconds):
        seconds = finite(seconds, 'frame seconds', 0, self.duration)
        if self.pid == 'CFX12':
            return min(seconds, float(self.cfg.get('freeze_at', 1.8)) / 5 * self.duration)
        if self.pid == 'CFX40':
            return self.module.clock_remap(seconds / self.duration * 5) / 5 * self.duration
        return seconds

    def frame(self, seconds, *, footage=None, subject=None, backdrop=None, anchor=None, echo_subjects=None, footage_seconds=None):
        seconds = finite(seconds, 'frame seconds', 0, self.duration)
        cfg = dict(self.cfg, _seconds=seconds)
        clock = seconds if self.meta.get('time_mode') == 'seconds' else seconds / self.duration * 5
        if self.mode == 'native':
            if any(x is not None for x in (footage, subject, backdrop, anchor, echo_subjects, footage_seconds)):
                raise AtlasError('Prepared layers require mode=footage')
            im = self.library.render.frame(self.pid, seconds, cfg, True) if self.labels else self.fn(self.pid, clock, cfg)
        else:
            if footage is None:
                raise AtlasError('mode=footage requires a current footage frame; no demo fallback')
            if self.pid in {'CFX12', 'CFX40'}:
                if footage_seconds is None or abs(finite(footage_seconds, 'footage_seconds', 0) - self.source_seconds(seconds)) > 1e-6:
                    raise AtlasError('Provide the frame at source_seconds(t) and declare footage_seconds; current-frame input would fake freeze/speed-ramp')
            for key, param in [('subject', 'subject_path'), ('backdrop', 'background_path')]:
                if (subject if key == 'subject' else backdrop) is None and cfg.get(param):
                    with Image.open(cfg[param]) as image:
                        prepared = image.convert('RGBA')
                    if key == 'subject':
                        subject = prepared
                    else:
                        backdrop = prepared
            for name, value in [('footage', footage), ('subject', subject), ('backdrop', backdrop)]:
                if value is not None and (not isinstance(value, Image.Image) or value.mode != 'RGBA'):
                    raise AtlasError(name + ' must be a prepared PIL RGBA image')
            if (subject is not None and subject.getchannel('A').getextrema()[0] == 255):
                raise AtlasError('Subject has no transparent pixels; prepare a genuine alpha matte')
            missing = [k for k in self.contract.get('required_layers', []) if {'subject': subject, 'backdrop': backdrop}.get(k) is None]
            if missing:
                raise AtlasError('Prepared layers required: ' + ', '.join(missing))
            if self.pid == 'CFX20':
                if not isinstance(echo_subjects, (list, tuple)) or not echo_subjects:
                    raise AtlasError('CFX20 requires nonempty real past-frame echo_subjects; analytic demo fallback is disabled')
                for echo in echo_subjects:
                    if not isinstance(echo, (list, tuple)) or len(echo) != 4 or not isinstance(echo[0], Image.Image) or echo[0].mode != 'RGBA':
                        raise AtlasError('Each echo must be (past_rgba,x,y,scale)')
                    for value in echo[1:]:
                        finite(value, 'echo transform')
                    if echo[3] <= 0:
                        raise AtlasError('Echo scale must be positive')
            if self.contract.get('requires_image_assets') and not (cfg.get('image_path') or cfg.get('image_paths')):
                raise AtlasError('This footage composition needs project image_path/image_paths; generic demo artwork is disabled')
            if self.pid == 'CFX14':
                raise AtlasError('CFX14 needs a reviewed before/after adapter; native demo remains available')
            if anchor is None:
                anchor = self._anchor(seconds)
            if anchor is not None and self.pid != 'CFX05':
                raise AtlasError('This preset does not consume a tracking anchor')
            if self.pid == 'CFX05' and anchor is None:
                raise AtlasError('CFX05 footage requires a verified anchor or anchor_track')
            if anchor is not None:
                if len(anchor) != 2:
                    raise AtlasError('anchor must contain x,y')
                cfg['_anchor'] = (finite(anchor[0], 'anchor x', 0, 1280), finite(anchor[1], 'anchor y', 0, 720))
            if echo_subjects is not None:
                cfg['_echo_subjects'] = echo_subjects
            im = self.module.compose(self.pid, clock, cfg, footage=footage, subject=subject, backdrop=backdrop)
        im = im.convert('RGBA')
        if im.size != (1280, 720):
            raise AtlasError('Original renderer returned a different canvas')
        if not self.transparent:
            im = im.convert('RGB')
        return im

    def output_frame(self, seconds):
        if self.mode == 'native':
            im = self.frame(seconds)
        else:
            if not self.sources:
                self.sources = {k: FrameSource(v, self.fps) for k, v in self.inputs.items() if k != 'anchor_track'}
            if 'footage' not in self.sources:
                raise AtlasError('CLI mode=footage requires inputs.footage')
            sample = self.source_seconds(seconds)
            layers = {k: source.get(sample if k == 'footage' else seconds) for k, source in self.sources.items()}
            im = self.frame(seconds, **layers, footage_seconds=sample)
        if im.size != (self.width, self.height):
            im = im.resize((self.width, self.height), Image.Resampling.LANCZOS)
        return im

    def close(self):
        for source in self.sources.values():
            source.close()

    def provenance(self):
        assets = {k: {'path': p, 'sha256': file_hash(p)} for k, p in {**self.asset_paths, **self.input_paths}.items()}
        return {'schema_version': SCHEMA, 'preset': self.pid, 'renderer': self.fn.__module__ + '.render',
                'package_sha256': self.library.contract['package_sha256'],
                'defaults_sha256': digest(self.meta), 'job_sha256': digest(self.spec),
                'environment': environment(), 'assets': assets,
                'wrapper_sha256': file_hash(__file__), 'mode': self.mode,
                'width': self.width, 'height': self.height, 'fps': self.fps,
                'duration': round(self.duration * self.fps) / self.fps,
                'frames': round(self.duration * self.fps), 'transparent': self.transparent,
                'catalogue_labels': self.labels, 'native_portrait': False}


class FrameSource:
    """Sequential FFmpeg decoder; exact indexed seek restarts only when needed."""
    def __init__(self, spec, fps):
        self.path = Path(spec['path']); self.fps = fps; self.start = spec.get('start', 0)
        self.proc = None; self.index = -1; self.last = None
        self.still = None
        if self.path.suffix.lower() in IMAGE_SUFFIXES:
            with Image.open(self.path) as im:
                self.still = im.convert('RGBA')

    def close(self):
        if self.proc:
            self.proc.stdout.close()
            if self.proc.poll() is None:
                self.proc.terminate()
            self.proc.wait(); self.proc = None

    def get(self, seconds):
        if self.still is not None:
            return self.still.copy()
        index = max(0, round(seconds * self.fps))
        if self.proc is None or index < self.index or index - self.index > 120:
            self.close()
            cmd = ['ffmpeg', '-v', 'error', '-threads', '1', '-ss', str(self.start), '-i', str(self.path),
                   '-vf', f'fps={self.fps},scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:color=black@0',
                   '-threads', '1', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-']
            self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            self.index = -1
        while self.index < index:
            need = 1280 * 720 * 4; chunks = bytearray()
            while len(chunks) < need:
                chunk = self.proc.stdout.read(need - len(chunks))
                if not chunk:
                    raise AtlasError('Source ended before requested frame: ' + str(self.path))
                chunks.extend(chunk)
            self.last = Image.frombytes('RGBA', (1280, 720), bytes(chunks))
            self.index += 1
        return self.last.copy()


def render_job(job, output, cache=None):
    output = Path(output).resolve(); output.parent.mkdir(parents=True, exist_ok=True)
    if job.transparent and output.suffix.lower() != '.mov':
        raise AtlasError('Transparent export requires .mov (ProRes 4444)')
    if not job.transparent and output.suffix.lower() != '.mp4':
        raise AtlasError('Opaque export requires .mp4')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise AtlasError('FFmpeg and ffprobe are required')
    if job.mode == 'footage':
        try:
            job.output_frame(0)  # fail before encoding if alpha/track/input is missing
        except BaseException:
            job.close()
            raise
    provenance = job.provenance()
    provenance['ffmpeg'] = subprocess.check_output(['ffmpeg', '-version'], text=True).splitlines()[0]
    cache_key = digest(provenance)
    cache_dir = Path(cache or os.environ.get('XDG_CACHE_HOME', str(Path.home() / '.cache'))) / 'motion-atlas-v1'
    cached = cache_dir / (cache_key + output.suffix)
    receipt = cached.with_suffix(cached.suffix + '.json')
    hit = cached.is_file() and receipt.is_file()
    if hit:
        hit = json.loads(receipt.read_text()).get('output_sha256') == file_hash(cached)
    if hit:
        shutil.copy2(cached, output)
        report = json.loads(receipt.read_text()); report.update(cache_hit=True, output=str(output))
        write_json(str(output) + '.atlas.json', report)
        job.close()
        return report
    fd, tempname = tempfile.mkstemp(prefix=output.stem + '.', suffix=output.suffix, dir=output.parent)
    os.close(fd); temp = Path(tempname)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba' if job.transparent else 'rgb24',
           '-s', f'{job.width}x{job.height}', '-r', str(job.fps), '-i', '-', '-an']
    cmd += ['-c:v', 'prores_ks', '-profile:v', '4', '-pix_fmt', 'yuva444p10le'] if job.transparent else ['-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-pix_fmt', 'yuv420p']
    cmd += ['-threads', '2', '-movflags', '+faststart', str(temp)]
    with tempfile.TemporaryFile() as err:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=err)
        try:
            for i in range(round(job.duration * job.fps)):
                proc.stdin.write(job.output_frame(i / job.fps).tobytes())
            proc.stdin.close()
            if proc.wait():
                err.seek(0); raise AtlasError('FFmpeg failed: ' + err.read().decode(errors='replace')[-1800:])
            subprocess.run(['ffmpeg', '-v', 'error', '-threads', '1', '-i', str(temp), '-f', 'null', '-'], check=True, capture_output=True)
            os.replace(temp, output)
        except BaseException:
            if proc.poll() is None:
                proc.kill(); proc.wait()
            temp.unlink(missing_ok=True)
            raise
        finally:
            job.close()
    report = dict(provenance, output=str(output), output_sha256=file_hash(output), cache_key=cache_key,
                  cache_hit=False, decode='pass', visual_review='required for changed content and footage', audio='silent layer; mix source audio in the editor')
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_temp = cached.with_name(cached.name + f'.{os.getpid()}.tmp')
    shutil.copy2(output, cache_temp); os.replace(cache_temp, cached)
    write_json(receipt, report); write_json(str(output) + '.atlas.json', report)
    return report


def verify_video(job, video, *, reference=False):
    """Compare actual encoded frames with their original Python source at exact indices."""
    video = Path(video)
    raw = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                   'stream=width,height,r_frame_rate,nb_frames:format=duration', '-of', 'json', str(video)])
    info = json.loads(raw); stream = info['streams'][0]
    if (stream['width'], stream['height']) != (job.width, job.height) or Fraction(stream['r_frame_rate']) != job.fps:
        raise AtlasError('Video dimensions/fps do not match this job; use the actual Atlas export configuration')
    frames = round(job.duration * job.fps)
    if abs(float(info['format']['duration']) - frames / job.fps) > 1 / job.fps + .002:
        raise AtlasError('Video duration differs from this job')
    subprocess.run(['ffmpeg', '-v', 'error', '-threads', '1', '-i', str(video), '-f', 'null', '-'], check=True, capture_output=True)
    indices = sorted({0, round((frames - 1) * .12), round((frames - 1) * .35), round((frames - 1) * .6), round((frames - 1) * .85), frames - 1})
    checks = []
    try:
        for i in indices:
            actual = subprocess.check_output(['ffmpeg', '-v', 'error', '-threads', '1', '-i', str(video), '-vf', f'select=eq(n\\,{i})',
                                              '-frames:v', '1', '-f', 'rawvideo', '-pix_fmt', 'rgba' if job.transparent else 'rgb24', '-'])
            channels = 4 if job.transparent else 3
            a = np.frombuffer(actual, np.uint8).reshape(job.height, job.width, channels).astype(np.int16)
            expected = np.asarray(job.output_frame(i / job.fps)).astype(np.int16)
            error = float(np.abs(a - expected).mean())
            if error > 5:
                raise AtlasError(f'Encoded frame {i} does not match this renderer/configuration (mean error {error:.3f})')
            checks.append({'frame': i, 'mean_pixel_error': round(error, 4)})
    finally:
        job.close()
    return {'preset': job.pid, 'decode': 'pass', 'sampled_frame_match': 'pass',
            'samples': checks, 'reference_video': str(video) if reference else None,
            'reference_sha256': file_hash(video), 'package_sha256': job.library.contract['package_sha256'],
            'claim_scope': 'sampled encoded frames and metadata; visual/temporal editorial review remains necessary'}


def load_job(path, library=None):
    path = Path(path).resolve()
    return AtlasPreset(json.loads(path.read_text()), library, path.parent)


def import_config(path, library):
    """Convert existing Atlas exports without silently accepting changed internals."""
    path = Path(path).resolve()
    raw = json.loads(path.read_text())
    if not isinstance(raw, dict) or raw.get('preset') not in library.registry:
        raise AtlasError('Legacy config must contain a known preset')
    pid = raw['preset']; meta = library.registry[pid]
    spec = library.template(pid)
    for key in ('duration', 'fps', 'width'):
        if key in raw:
            spec['output'][key] = raw[key]
    duration = finite(spec['output']['duration'], 'duration', .5, 120)
    allowed = library.contract['presets'][pid]['allowed_params']
    native_defaults = library.render.configuration(pid)
    for key, value in raw.items():
        if key in {'preset', 'duration', 'fps', 'width'}:
            continue
        if key == 'line_cues' and pid == 'CFX15':
            spec['cue_seconds']['line_cues'] = [v / 5 * duration for v in value]
        elif key == 'freeze_at' and pid == 'CFX12':
            spec['cue_seconds']['freeze_at'] = value / 5 * duration
        elif key == 'cues' and pid == 'B05':
            spec['cue_seconds']['word_intervals'] = [{'start': v['start'] / 5 * duration, 'end': v['end'] / 5 * duration} for v in value]
        elif key == 'pauses' and pid == 'B06':
            spec['cue_seconds']['character_pauses'] = [{'after_character': v['after_character'], 'duration': v['duration'] / 5 * duration} for v in value]
        elif key == 'cues' and meta.get('time_mode') == 'seconds':
            spec['cue_seconds'] = value
        elif key in allowed:
            if key in PATH_KEYS and value:
                value = str((path.parent / value).resolve())
            elif key == 'image_paths':
                value = [str((path.parent / p).resolve()) for p in value]
            spec['params'][key] = value
        elif key in native_defaults and value == native_defaults[key]:
            continue  # fixed metadata/animation defaults, never applied as overrides
        else:
            raise AtlasError('Unsupported or changed internal field in legacy config: ' + key)
    AtlasPreset(spec, library, path.parent)
    return spec


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    listing = sub.add_parser('list'); listing.add_argument('--search', default='')
    desc = sub.add_parser('describe'); desc.add_argument('preset')
    init = sub.add_parser('init'); init.add_argument('preset'); init.add_argument('--output', type=Path, required=True)
    convert = sub.add_parser('import-config'); convert.add_argument('config', type=Path); convert.add_argument('--output', type=Path, required=True)
    check = sub.add_parser('check'); check.add_argument('job', type=Path)
    render = sub.add_parser('render'); render.add_argument('job', type=Path); render.add_argument('--output', type=Path, required=True); render.add_argument('--cache', type=Path)
    frame = sub.add_parser('frame'); frame.add_argument('job', type=Path); frame.add_argument('--time', type=float, required=True); frame.add_argument('--output', type=Path, required=True)
    verify = sub.add_parser('verify'); verify.add_argument('job', type=Path); verify.add_argument('--video', type=Path, required=True); verify.add_argument('--reference', action='store_true'); verify.add_argument('--report', type=Path)
    args = ap.parse_args(argv)
    try:
        lib = AtlasLibrary()
        if args.command == 'list':
            query = args.search.casefold()
            result = [{'id': pid, 'name': m['name']} for pid, m in lib.registry.items() if query in (pid + ' ' + m['name'] + ' ' + m['description']).casefold()]
        elif args.command == 'describe':
            result = lib.describe(args.preset)
        elif args.command == 'init':
            result = lib.template(args.preset); write_json(args.output, result)
            result = {'job': str(args.output), 'preset': args.preset}
        elif args.command == 'import-config':
            result = import_config(args.config, lib); write_json(args.output, result)
            result = {'job': str(args.output), 'preset': result['preset'], 'imported': True}
        else:
            job = load_job(args.job, lib)
            if args.command == 'check':
                if job.mode == 'footage':
                    try:
                        job.output_frame(0)
                    finally:
                        job.close()
                result = {'valid': True, **job.provenance()}
            elif args.command == 'render':
                result = render_job(job, args.output, args.cache)
            elif args.command == 'frame':
                args.output.parent.mkdir(parents=True, exist_ok=True)
                try:
                    job.output_frame(args.time).save(args.output)
                finally:
                    job.close()
                result = {'frame': str(args.output), 'seconds': args.time, 'preset': job.pid}
            else:
                result = verify_video(job, args.video, reference=args.reference)
                if args.report:
                    write_json(args.report, result)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    except (AtlasError, ValueError, KeyError, FileNotFoundError, subprocess.CalledProcessError) as e:
        print('ATLAS ERROR: ' + str(e), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
