#!/usr/bin/env python3
"""Regression tests for native Atlas parity, rejected jobs, cues and real media IO."""
import argparse
import copy
from concurrent.futures import ProcessPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

import numpy as np
from PIL import Image, ImageDraw
import atlas_preset as atlas

LIB = None


def worker_init():
    global LIB
    LIB = atlas.AtlasLibrary()


def parity(pid):
    spec = LIB.template(pid)
    job = atlas.AtlasPreset(spec, LIB)
    t = job.duration * .39
    actual = job.frame(t)
    expected = LIB.render.frame(pid, t, LIB.render.configuration(pid), False)
    if actual.tobytes() != expected.tobytes():
        raise AssertionError(pid + ' differs from the original renderer')
    # Out-of-order sampling must restore exactly the same frame.
    job.frame(job.duration * .81)
    if actual.tobytes() != job.frame(t).tobytes():
        raise AssertionError(pid + ' is not seek-deterministic')
    from build_atlas import exported_config
    with tempfile.TemporaryDirectory() as temp:
        path = Path(temp) / 'legacy.json'
        atlas.write_json(path, exported_config(pid, LIB.registry[pid]))
        converted = atlas.import_config(path, LIB)
        if converted['preset'] != pid:
            raise AssertionError('Legacy config import changed preset identity')
    return pid


class AtlasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.lib = atlas.AtlasLibrary()

    def spec(self, pid='T01'):
        return self.lib.template(pid)

    def job(self, spec):
        return atlas.AtlasPreset(spec, self.lib)

    def test_package_and_native_baselines_cover_registry(self):
        self.assertEqual(len(self.lib.registry), 922)
        self.assertEqual(set(self.lib.registry), set(self.lib.contract['goldens']))
        self.assertTrue(all(len(x) == 3 for x in self.lib.contract['goldens'].values()))

    def test_unknown_and_locked_parameters_fail(self):
        for field, value in [('easing', 'linear'), ('stencil_step', .1), ('_transparent', True), ('textt', 'TYPO')]:
            spec = self.spec(); spec['params'][field] = value
            with self.assertRaises(atlas.AtlasError):
                self.job(spec)

    def test_pin_mismatch_and_changed_backend_fail(self):
        spec = self.spec(); spec['reference']['package_sha256'] = '0' * 64
        with self.assertRaises(atlas.AtlasError):
            self.job(spec)
        with patch.object(atlas, 'source_hashes', return_value={'core.py': 'changed'}):
            with self.assertRaises(atlas.AtlasError):
                atlas.AtlasLibrary()

    def test_malformed_output_and_colors_fail(self):
        for target, key, value in [('output', 'fps', True), ('output', 'width', 1080), ('output', 'height', 1920),
                                   ('output', 'duration', float('nan')), ('params', 'accent', '#GGGGGG')]:
            spec = self.spec(); spec[target][key] = value
            with self.assertRaises(atlas.AtlasError):
                self.job(spec)

    def test_scroll_cues_are_converted_once(self):
        spec = self.spec('CFX15'); spec['output']['duration'] = 8
        spec['params']['lines'] = ['SATU', 'DUA', 'TIGA', 'EMPAT']
        spec['cue_seconds'] = {'line_cues': [0, 2, 4, 6]}
        job = self.job(spec)
        self.assertEqual(job.cfg['line_cues'], [0, 1.25, 2.5, 3.75])
        expected = self.lib.render.configuration('CFX15', {'duration': 8, 'lines': spec['params']['lines'], 'line_cues': [0, 1.25, 2.5, 3.75]})
        self.assertEqual(job.frame(4.2).tobytes(), self.lib.render.frame('CFX15', 4.2, expected, False).tobytes())
        spec['cue_seconds']['line_cues'] = [0, 4, 2, 6]
        with self.assertRaises(atlas.AtlasError):
            self.job(spec)
        spec['cue_seconds'] = {}; spec['params']['lines'] = ['ONLY', 'THREE', 'LINES']
        with self.assertRaises(atlas.AtlasError):
            self.job(spec)

    def test_word_intervals_and_freeze(self):
        spec = self.spec('B05'); spec['params']['text'] = 'SATU DUA'; spec['output']['duration'] = 8
        spec['cue_seconds'] = {'word_intervals': [{'start': 0, 'end': 2}, {'start': 2, 'end': 4}]}
        self.assertEqual(self.job(spec).cfg['cues'], [{'start': 0, 'end': 1.25}, {'start': 1.25, 'end': 2.5}])
        spec = self.spec('CFX12'); spec['output']['duration'] = 8; spec['cue_seconds'] = {'freeze_at': 3.2}
        self.assertEqual(self.job(spec).cfg['freeze_at'], 2)

    def test_shared_cached_artwork_is_not_mutated(self):
        import core
        a = core.panel(160, 70); ImageDraw.Draw(a).rectangle((0, 0, 150, 60), fill='red')
        self.assertNotEqual(a.tobytes(), core.panel(160, 70).tobytes())
        a = core.text_img('CACHE'); a.putalpha(0)
        self.assertNotEqual(a.tobytes(), core.text_img('CACHE').tobytes())

    def test_catalogue_reference_frame_uses_original_labels(self):
        spec = self.spec(); spec['output']['catalogue_labels'] = True
        job = self.job(spec)
        cfg = self.lib.render.configuration('T01'); cfg['_fps'] = job.fps
        self.assertEqual(job.frame(2).tobytes(), self.lib.render.frame('T01', 2, cfg, True).tobytes())

    def test_preview_cache_rejects_stale_or_changed_files(self):
        from build_atlas import reusable, preview_key, sha_file
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); (root / 'previews').mkdir(); (root / 'posters').mkdir()
            video = root / 'previews/T01.mp4'; poster = root / 'posters/T01.jpg'
            video.write_bytes(b'video fixture'); poster.write_bytes(b'poster fixture')
            package = self.lib.contract['package_sha256']
            receipt = {'cache_key': preview_key('T01', self.lib.render.configuration('T01'), package),
                       'video_sha256': sha_file(video), 'poster_sha256': sha_file(poster)}
            atlas.write_json(root / 'previews/T01.atlas.json', receipt)
            self.assertTrue(reusable('T01', root, package))
            self.assertFalse(reusable('T01', root, 'different-package'))
            video.write_bytes(b'changed video')
            self.assertFalse(reusable('T01', root, package))

    def test_replaced_asset_invalidates_original_loader_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'art.png'
            spec = self.spec('CFX01'); spec['params']['image_path'] = str(path)
            Image.new('RGB', (1280, 720), 'red').save(path)
            before = self.job(spec).frame(1).tobytes()
            Image.new('RGB', (1280, 720), 'blue').save(path)
            after = self.job(spec).frame(1).tobytes()
            self.assertNotEqual(before, after)

    def test_remapped_media_time_must_be_declared(self):
        footage = Image.new('RGBA', (1280, 720), '#2468AC')
        spec = self.spec('CFX12'); spec['mode'] = 'footage'
        job = self.job(spec)
        with self.assertRaises(atlas.AtlasError):
            job.frame(5, footage=footage)
        result = job.frame(5, footage=footage, backdrop=footage, footage_seconds=job.source_seconds(5))
        self.assertEqual(result.size, (1280, 720))

    def test_seconds_presets_do_not_double_normalize(self):
        spec = self.spec('L01'); spec['cue_seconds'] = {'title': 2, 'resolve': 14}
        job = self.job(spec)
        self.assertEqual(job.cfg['cues'], {'title': 2, 'resolve': 14})
        expected = self.lib.render.configuration('L01', {'cues': spec['cue_seconds']})
        self.assertEqual(job.frame(3).tobytes(), self.lib.render.frame('L01', 3, expected, False).tobytes())

    def test_legacy_config_preserves_paths_and_timing(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); Image.new('RGB', (100, 80), 'red').save(root / 'picture.png')
            legacy = {'preset': 'C01', 'image_paths': ['picture.png'], 'duration': 6, 'fps': 30, 'width': 960}
            atlas.write_json(root / 'old.json', legacy)
            converted = atlas.import_config(root / 'old.json', self.lib)
            self.assertEqual(converted['params']['image_paths'], [str(root / 'picture.png')])
            legacy = {'preset': 'CFX15', 'duration': 8, 'line_cues': [0, 1.25, 2.5, 3.75]}
            atlas.write_json(root / 'old.json', legacy)
            converted = atlas.import_config(root / 'old.json', self.lib)
            self.assertEqual(converted['cue_seconds']['line_cues'], [0, 2, 4, 6])
            legacy['made_up_effect'] = 1; atlas.write_json(root / 'old.json', legacy)
            with self.assertRaises(atlas.AtlasError):
                atlas.import_config(root / 'old.json', self.lib)

    def test_footage_alpha_tracking_and_no_demo_fallback(self):
        footage = Image.new('RGBA', (1280, 720), '#2468AC')
        spec = self.spec('CFX05'); spec['mode'] = 'footage'
        job = self.job(spec)
        with self.assertRaises(atlas.AtlasError):
            job.frame(1, footage=footage)
        actual = job.frame(1, footage=footage, anchor=(300, 250))
        cfg = dict(job.cfg, _anchor=(300., 250.))
        expected = job.module.compose('CFX05', 1 / 6 * 5, cfg, footage=footage).convert('RGB')
        self.assertEqual(actual.tobytes(), expected.tobytes())
        spec = self.spec('CFX29'); spec['mode'] = 'footage'; job = self.job(spec)
        with self.assertRaises(atlas.AtlasError):
            job.frame(1, footage=footage)
        with self.assertRaises(atlas.AtlasError):
            job.frame(1, footage=footage, subject=footage, backdrop=footage)
        cutout = Image.new('RGBA', (220, 350)); ImageDraw.Draw(cutout).ellipse((30, 20, 190, 340), fill='#77CCAA')
        result = job.frame(1, footage=footage, subject=cutout, backdrop=footage)
        self.assertEqual(result.size, (1280, 720))

    def test_real_video_encode_verify_cache_and_wrong_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'source.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'testsrc2=size=640x360:rate=24', '-t', '2', '-c:v', 'libx264', '-threads', '1', str(source)], check=True)
            spec = self.spec('CFX01'); spec['mode'] = 'footage'
            spec['output'].update(duration=1, width=320, fps=24)
            spec['inputs'] = {'footage': {'path': str(source)}}
            output = root / 'out.mp4'
            report = atlas.render_job(self.job(spec), output, root / 'cache')
            self.assertFalse(report['cache_hit'])
            result = atlas.verify_video(self.job(spec), output)
            self.assertEqual(result['sampled_frame_match'], 'pass')
            again = atlas.render_job(self.job(spec), root / 'again.mp4', root / 'cache')
            self.assertTrue(again['cache_hit'])
            self.assertEqual(report['output_sha256'], again['output_sha256'])
            # Same metadata, deliberately different imagery must fail parity.
            wrong = root / 'wrong.mp4'
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=red:size=320x180:rate=24', '-t', '1', '-c:v', 'libx264', '-threads', '1', str(wrong)], check=True)
            with self.assertRaises(atlas.AtlasError):
                atlas.verify_video(self.job(spec), wrong, reference=True)

    def test_alpha_export_and_decode(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); spec = self.spec(); spec['output'].update(duration=.5, fps=24, width=320, transparent=True)
            job = self.job(spec)
            self.assertLess(job.frame(.2).getchannel('A').getextrema()[0], 255)
            output = root / 'title.mov'
            atlas.render_job(job, output, root / 'cache')
            info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=pix_fmt', '-of', 'json', str(output)]))
            self.assertIn('a', info['streams'][0]['pix_fmt'])
            self.assertEqual(atlas.verify_video(self.job(spec), output)['decode'], 'pass')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all', action='store_true'); parser.add_argument('--jobs', type=int, default=2); parser.add_argument('--report', type=Path)
    args = parser.parse_args(); started = time.monotonic()
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AtlasTests))
    if not result.wasSuccessful():
        return 1
    lib = atlas.AtlasLibrary()
    ids = sorted(lib.registry) if args.all else sorted({'T01', 'B04', 'B05', 'K01', 'K25', 'K45', 'L01', 'L06', 'MP40', 'CFX01', 'CFX15', 'CFX29', 'CFX40', 'CFX57', 'CFX71', 'CFX80'})
    with ProcessPoolExecutor(max_workers=args.jobs, initializer=worker_init) as pool:
        for i, pid in enumerate(pool.map(parity, ids, chunksize=6), 1):
            if i % 50 == 0 or i == len(ids):
                print(f'Native parity and seek {i}/{len(ids)}', flush=True)
    report = {'unit_tests': result.testsRun, 'native_parity_and_seek': len(ids), 'legacy_config_import': len(ids), 'baseline_frames_per_preset': 3,
              'package_sha256': lib.contract['package_sha256'], 'environment': atlas.environment(),
              'elapsed_seconds': round(time.monotonic() - started, 2), 'passed': True,
              'published_atlas_video_parity': 'not claimed; verify an actual reference MP4 separately'}
    if args.report:
        atlas.write_json(args.report, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
