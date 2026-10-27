#!/usr/bin/env python3
"""Human video matting, transparent cutouts and replacement backgrounds, locally."""
from __future__ import annotations
import argparse
import fcntl
import json
import math
import os
import re
from pathlib import Path
import subprocess
import sys
import time
from background_runtime import CACHE, MODEL, add_deps, digest, model_path, probe, read_exact, run_checked, session, signature, write_json


def default_meta(mask):
    return Path(str(mask)+'.json')


def cuts(path, fps):
    if not path:
        return set()
    values = json.loads(Path(path).read_text())
    if not isinstance(values, list) or any(not isinstance(v, (float, int)) or not math.isfinite(v) or v < 0 for v in values):
        raise ValueError('Cuts must be a JSON list of nonnegative seconds on this selected clip clock')
    return {round(v*fps) for v in values}


def partial(path):
    return path.with_name(path.stem+f'.partial-{os.getpid()}'+path.suffix)


def matte(a):
    source = Path(a.input).resolve()
    output = Path(a.output).resolve()
    if output == source:
        raise ValueError('Mask output must differ from the source')
    if output.suffix.lower() not in {'.mkv', '.mp4'}:
        raise ValueError('Use .mkv for lossless FFV1 mask, or .mp4 for compact grayscale mask')
    output.parent.mkdir(parents=True, exist_ok=True)
    meta_path = Path(a.metadata) if a.metadata else default_meta(output)
    if meta_path.resolve() in {source, output}:
        raise ValueError('Metadata must not overwrite the source or mask')
    with Path(str(output)+'.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        ready = output.parent/(output.stem+'.background-ready.json')
        command = [sys.executable, str(Path(__file__).with_name('ensure_background.py')), '--cache-root', str(a.cache_root), '--report', str(ready)]
        if a.offline:
            command.append('--offline')
        if a.model_path:
            command += ['--model-path', str(a.model_path)]
        run_checked(command, output.parent/(output.stem+'.setup.log'))
        add_deps(a.cache_root)
        import numpy as np
        from PIL import Image, ImageFilter
        info = probe(source)
        video = next(s for s in info['streams'] if s['codec_type'] == 'video')
        if video.get('sample_aspect_ratio', '1:1') not in {'1:1', 'N/A', '0:1'}:
            raise ValueError('Normalize nonsquare pixels before matting: scale=iw*sar:ih,setsar=1')
        rotation = next((float(z['rotation']) for z in video.get('side_data_list', []) if 'rotation' in z), 0)
        sw, sh = video['width'], video['height']
        if round(rotation) % 180 == 90:
            sw, sh = sh, sw
        scale = min(1, a.inference_long_edge/max(sw, sh))
        w, h = max(2, round(sw*scale/2)*2), max(2, round(sh*scale/2)*2)
        ratio = a.downsample_ratio or min(1, 480/max(w, h))
        planned = cuts(a.cuts, a.fps)
        overrides = {kind: dict(path=str(Path(path).resolve()), sha256=digest(path)) for kind, path in [('keep', a.keep_mask), ('erase', a.erase_mask)] if path}
        config = dict(source_signature=signature(source), source_start=a.start, requested_duration=a.duration, fps=a.fps, inference_size=[w, h], downsample_ratio=ratio, cuts=sorted(planned), scene_threshold=a.scene_threshold, feather=a.feather, overrides=overrides, model_sha256=MODEL['sha256'])
        if not a.force and output.exists() and meta_path.exists():
            prior = json.loads(meta_path.read_text())
            if prior.get('complete') and prior.get('configuration') == config and prior.get('mask_signature') == signature(output):
                print(json.dumps(dict(reused=True, mask=str(output), metadata=str(meta_path), frames=prior['frames'])))
                return 0
        masks = {kind: np.asarray(Image.open(data['path']).convert('L').resize((w, h), Image.Resampling.BILINEAR), np.float32)/255 for kind, data in overrides.items()}
        model = session(model_path(a.cache_root, a.model_path), a.threads)
        rec = [np.zeros((1, 1, 1, 1), np.float32) for _ in range(4)]
        temporary = partial(output)
        dec_command = ['ffmpeg', '-v', 'error', '-threads', '1', '-ss', str(a.start), '-i', str(source)]
        if a.duration is not None:
            dec_command += ['-t', str(a.duration)]
        dec_command += ['-an', '-vf', f'fps={a.fps}:start_time=0,scale={w}:{h}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-']
        enc_command = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', f'{w}x{h}', '-r', str(a.fps), '-i', '-', '-an']
        enc_command += ['-c:v', 'ffv1', '-level', '3', '-g', '1', '-threads', '2'] if output.suffix == '.mkv' else ['-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '8', '-pix_fmt', 'yuv420p', '-threads', '2']
        enc_command.append(str(temporary))
        logs = [output.parent/(output.stem+s) for s in ['.decode.log', '.encode.log']]
        opened = [p.open('w') for p in logs]
        decoder = subprocess.Popen(dec_command, stdout=subprocess.PIPE, stderr=opened[0])
        encoder = subprocess.Popen(enc_command, stdin=subprocess.PIPE, stderr=opened[1])
        n = 0
        reset_frames = []
        previous = None
        started = time.time()
        alpha_min, alpha_max = 255, 0
        try:
            while True:
                data = read_exact(decoder.stdout, w*h*3)
                if data is None:
                    break
                frame = np.frombuffer(data, np.uint8).reshape(h, w, 3)
                small = frame[::16, ::16].astype(np.float32)/255
                detected = previous is not None and a.scene_threshold > 0 and float(np.abs(small-previous).mean()) > a.scene_threshold
                if n == 0 or n in planned or detected:
                    rec = [np.zeros((1, 1, 1, 1), np.float32) for _ in range(4)]
                    reset_frames.append(n)
                previous = small
                feed = dict(src=frame.transpose(2, 0, 1)[None].astype(np.float32)/255, downsample_ratio=np.array([ratio], np.float32))
                feed.update({f'r{i+1}i': value for i, value in enumerate(rec)})
                _, pha, *rec = model.run(None, feed)
                alpha = pha[0, 0]
                if not np.isfinite(alpha).all():
                    raise RuntimeError(f'Nonfinite alpha at frame {n}')
                if 'keep' in masks:
                    alpha = np.maximum(alpha, masks['keep'])
                if 'erase' in masks:
                    alpha = np.minimum(alpha, 1-masks['erase'])
                image = Image.fromarray((alpha.clip(0, 1)*255).round().astype(np.uint8))
                if a.feather:
                    image = image.filter(ImageFilter.GaussianBlur(a.feather))
                lo, hi = image.getextrema()
                alpha_min, alpha_max = min(alpha_min, lo), max(alpha_max, hi)
                encoder.stdin.write(image.tobytes())
                n += 1
                if n % 30 == 0:
                    write_json(Path(str(output)+'.progress.json'), dict(frames=n, seconds=n/a.fps, elapsed=time.time()-started, fps=n/(time.time()-started)))
            encoder.stdin.close()
            if encoder.wait() or decoder.wait() or not n:
                raise RuntimeError('Matting decode/encode failed or produced no frames; inspect logs')
        finally:
            for proc in [decoder, encoder]:
                if proc.poll() is None:
                    proc.terminate()
                proc.wait()
            for f in opened:
                f.close()
        temporary.replace(output)
        metadata = dict(complete=True, backend='RVM MobileNetV3 FP32 / CPU', configuration=config, mask=str(output), mask_signature=signature(output), frames=n, fps=a.fps, duration=n/a.fps, source_display_size=[sw, sh], mask_size=[w, h], recurrent_reset_frames=reset_frames, alpha_range=[alpha_min, alpha_max], elapsed_seconds=time.time()-started, quality_review_required=True, note='Human segmentation; inspect hair, hands, blur and held props. Use targeted keep/erase masks when needed.')
        write_json(meta_path, metadata)
        print(json.dumps(dict(mask=str(output), metadata=str(meta_path), frames=n, duration=n/a.fps, reused=False)))
    return 0


def qa(path, frames, fps):
    data = probe(path)
    v = next(s for s in data['streams'] if s['codec_type'] == 'video')
    packets = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_packets', '-show_entries', 'packet=pts_time', '-of', 'json', str(path)]))['packets']
    pts = sorted(float(p['pts_time']) for p in packets)
    error = max((abs(b-a-1/fps) for a, b in zip(pts, pts[1:])), default=0)
    if len(pts) != frames or abs(pts[0]) > 1e-5 or error > 2e-6:
        raise RuntimeError(f'Output cadence mismatch: {len(pts)} frames, start {pts[0]}, interval error {error}')
    audios = [s for s in data['streams'] if s['codec_type'] == 'audio']
    audio_durations = [float(s['duration']) for s in audios if s.get('duration') not in {None, 'N/A'}]
    if any(abs(d-frames/fps) > max(.06, 1/fps) for d in audio_durations):
        raise RuntimeError(f'Audio/video duration mismatch: audio {audio_durations}, video {frames/fps}')
    run_checked(['ffmpeg', '-v', 'error', '-xerror', '-threads', '2', '-i', str(path), '-f', 'null', '-'], Path(str(path)+'.decode-qa.log'))
    return dict(status='PASS_MEDIA_ONLY', frames=len(pts), fps=fps, width=v['width'], height=v['height'], duration=frames/fps, first_pts=pts[0], last_pts=pts[-1], maximum_interval_error=error, full_decode=True, audio_streams=len(audios), audio_durations=audio_durations, visual_review_required=True)


def render(a):
    source = Path(a.input).resolve()
    mask = Path(a.mask).resolve()
    output = Path(a.output).resolve()
    metadata = json.loads((Path(a.metadata) if a.metadata else default_meta(mask)).read_text())
    if not metadata.get('complete') or metadata['configuration']['source_signature'] != signature(source) or metadata['mask_signature'] != signature(mask):
        raise ValueError('Source/mask changed or mask incomplete; regenerate the matching matte')
    if output in {source, mask}:
        raise ValueError('Output must differ from input and mask')
    if a.background and output == Path(a.background).resolve():
        raise ValueError('Output must not overwrite the supplied background asset')
    alpha_export = not a.background
    if alpha_export and output.suffix.lower() != '.mov':
        raise ValueError('Transparent video needs .mov (ProRes 4444); H.264 MP4 cannot retain alpha')
    if not alpha_export and output.suffix.lower() != '.mp4':
        raise ValueError('Replacement-background output uses .mp4')
    output.parent.mkdir(parents=True, exist_ok=True)
    with Path(str(output)+'.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if output.exists() and not a.overwrite:
            raise FileExistsError('Output exists; use a new path or --overwrite')
        fps, n = metadata['fps'], metadata['frames']
        temporary = partial(output)
        w, h = a.width, a.height
        cmd = ['ffmpeg', '-hide_banner', '-y', '-threads', '2', '-ss', str(metadata['configuration']['source_start']), '-i', str(source), '-threads', '1', '-i', str(mask)]
        graph = [f'[0:v]fps={fps}:start_time=0,trim=end_frame={n},setpts=N/({fps}*TB),setsar=1,eq=contrast={a.contrast}:brightness={a.brightness}:saturation={a.saturation},format=rgba[src]', f'[1:v]setpts=N/({fps}*TB),scale={metadata["source_display_size"][0]}:{metadata["source_display_size"][1]}:flags=lanczos,format=gray[m]', '[src][m]alphamerge[p]']
        if a.subject_fit == 'contain':
            geometry = f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=0x00000000'
        else:
            geometry = f'scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}'
        graph.append('[p]'+geometry+',setsar=1[subject]')
        if alpha_export:
            graph.append('[subject]format=yuva444p10le[out]')
        else:
            background = Path(a.background).resolve()
            from PIL import Image
            try:
                with Image.open(background) as image:
                    image.verify()
                still = True
            except Exception:
                still = False
            cmd += ['-loop', '1', '-framerate', str(fps)] if still else ['-stream_loop', '-1']
            cmd += ['-i', str(background)]
            graph.append(f'[2:v]fps={fps}:start_time=0,setpts=N/({fps}*TB),scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,format=rgba[bg]')
            if a.rim_strength:
                graph += ['[subject]split=3[s][sa][sb]', '[sa]alphaextract[a]', '[sb]alphaextract,gblur=sigma=8[blur]', f'[a][blur]blend=all_mode=subtract,lut=y=val*{a.rim_strength}[edge]']
                # A static color layer is masked by the true inner silhouette.
                graph += [f'color=c={a.rim_color}:s={w}x{h}:r={fps},format=rgb24[color]', '[color][edge]alphamerge[rim]', '[bg][s]overlay=0:0:format=auto:shortest=1[base]', '[base][rim]overlay=0:0:format=auto:shortest=1,format=yuv420p[out]']
            else:
                graph.append('[bg][subject]overlay=0:0:format=auto:shortest=1,format=yuv420p[out]')
        graph_path = Path(str(output)+'.filter.txt')
        graph_path.write_text(';\n'.join(graph))
        cmd += ['-filter_complex_threads', '2', '-filter_complex_script', str(graph_path), '-map', '[out]']
        if not a.no_audio:
            cmd += ['-map', '0:a:0?', '-af', f'asetpts=PTS-STARTPTS,atrim=duration={n/fps}', '-c:a', 'pcm_s16le' if alpha_export else 'aac', '-ar', '48000']
            if not alpha_export:
                cmd += ['-b:a', '192k']
        else:
            cmd += ['-an']
        cmd += ['-frames:v', str(n), '-r', str(fps), '-fps_mode', 'cfr', '-threads', '2']
        cmd += ['-c:v', 'prores_ks', '-profile:v', '4', '-pix_fmt', 'yuva444p10le'] if alpha_export else ['-c:v', 'libx264', '-preset', 'fast', '-crf', str(a.crf), '-pix_fmt', 'yuv420p', '-movflags', '+faststart']
        cmd.append(str(temporary))
        run_checked(cmd, Path(str(output)+'.render.log'))
        report = qa(temporary, n, fps)
        temporary.replace(output)
        report.update(output=str(output), transparent=alpha_export, background=str(Path(a.background).resolve()) if a.background else None, subject_fit=a.subject_fit, source_audio='recorded input; encoded to output codec' if not a.no_audio else 'disabled')
        write_json(Path(str(output)+'.qa.json'), report)
        print(json.dumps(report, indent=2))
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    m = sub.add_parser('matte')
    for flag in ['input', 'output']:
        m.add_argument('--'+flag, required=True)
    m.add_argument('--metadata')
    m.add_argument('--cache-root', type=Path, default=CACHE)
    m.add_argument('--model-path', type=Path)
    m.add_argument('--offline', action='store_true')
    m.add_argument('--fps', type=int, choices=[24, 25, 30, 50, 60], default=30)
    m.add_argument('--inference-long-edge', type=int, default=1280)
    m.add_argument('--downsample-ratio', type=float, default=0)
    m.add_argument('--threads', type=int, default=2)
    m.add_argument('--start', type=float, default=0)
    m.add_argument('--duration', type=float)
    m.add_argument('--cuts', help='JSON seconds relative to selected clip, e.g. [1.0, 3.5]')
    m.add_argument('--scene-threshold', type=float, default=.28, help='0 disables automatic hard-cut detection')
    m.add_argument('--keep-mask', help='Source-oriented grayscale image; white protects a prop/region')
    m.add_argument('--erase-mask', help='Source-oriented grayscale image; white removes a region')
    m.add_argument('--feather', type=float, default=0)
    m.add_argument('--force', action='store_true')
    m.set_defaults(fn=matte)
    r = sub.add_parser('render')
    for flag in ['input', 'mask', 'output']:
        r.add_argument('--'+flag, required=True)
    r.add_argument('--metadata')
    r.add_argument('--cache-root', type=Path, default=CACHE)
    r.add_argument('--background', help='Local still or video; omit for transparent MOV')
    r.add_argument('--width', type=int, default=1080)
    r.add_argument('--height', type=int, default=1920)
    r.add_argument('--subject-fit', choices=['contain', 'cover'], default='contain')
    r.add_argument('--contrast', type=float, default=1)
    r.add_argument('--brightness', type=float, default=0)
    r.add_argument('--saturation', type=float, default=1)
    r.add_argument('--rim-strength', type=float, default=0)
    r.add_argument('--rim-color', default='0xAC4EFF')
    r.add_argument('--crf', type=int, default=19)
    r.add_argument('--no-audio', action='store_true')
    r.add_argument('--overwrite', action='store_true')
    r.set_defaults(fn=render)
    a = p.parse_args()
    numeric = [a.start, a.downsample_ratio, a.scene_threshold, a.feather] + ([a.duration] if a.duration is not None else []) if a.command == 'matte' else [a.contrast, a.brightness, a.saturation, a.rim_strength]
    if not all(math.isfinite(x) for x in numeric):
        p.error('Numeric parameters must be finite')
    if a.command == 'render' and not re.fullmatch(r'(?:0x|#)[0-9A-Fa-f]{6}', a.rim_color):
        p.error('Rim color must be 0xRRGGBB or #RRGGBB')
    if a.command == 'matte' and (a.start < 0 or a.duration is not None and a.duration <= 0 or a.inference_long_edge < 64 or not 0 <= a.downsample_ratio <= 1 or a.threads < 1 or not 0 <= a.scene_threshold <= 1 or a.feather < 0):
        p.error('Invalid time, size, ratio, threads or mask parameters')
    if a.command == 'render' and (min(a.width, a.height) < 32 or a.width % 2 or a.height % 2 or not 0 <= a.rim_strength <= 1 or not 0 <= a.contrast <= 3 or not -1 <= a.brightness <= 1 or not 0 <= a.saturation <= 3):
        p.error('Use even output dimensions and valid grading/rim values')
    try:
        if a.command == 'render':
            add_deps(a.cache_root)
        return a.fn(a)
    except Exception as e:
        print(f'{type(e).__name__}: {e}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
