#!/usr/bin/env python3
"""Prepare the validated Arbain 480x854 preset without inheriting episode content."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile


GUARD = r'''"""Project identity and pre-render input guard; no external calls."""
import hashlib
import json
from pathlib import Path

def sha(p):
    h = hashlib.sha256()
    with Path(p).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def load(project):
    r = Path(project)
    c = json.loads((r / 'episode_config.json').read_text())
    p = Path(c['source'])
    s = p.stat()
    old = c['source_identity']
    if (s.st_size, s.st_mtime_ns) != (old['size'], old['mtime_ns']):
        if sha(p) != old['sha256']:
            raise RuntimeError('Source changed: use a fresh episode project; do not reuse chunks/camera/audio.')
    return c

def inputs(project):
    r = Path(project); c = load(r); tag = c['tag']
    names = [f'{tag}_production_edl.json', f'{tag}_camera_map_draft.json',
             f'{tag}_captions.ass', f'{tag}_base.png', f'{tag}_audio_encoded_v2.m4a',
             f'{tag}_reviewed_units.jsonl', f'{tag}_ar_draft.jsonl',
             f'render_{tag}_ass.py', f'{tag}_caption_style.py',
             f'{tag}_build_ass.py', 'episode_config.json', 'lecture_project_guard.py',
             f'{tag}_source_edge_feather.png']
    names += [str(p.relative_to(r)) for p in sorted((r / 'project_fonts').glob('*.ttf'))]
    return {name: sha(r / name) for name in names}

def audio_identity(r):
    r = Path(r); c = load(r); tag = c['tag']
    e = json.loads((r / f'{tag}_production_edl.json').read_text())
    return dict(source=c['source_identity']['sha256'],
                audio=sha(r / f'{tag}_audio_encoded_v2.m4a'),
                timeline={k: e[k] for k in ['duration', 'segments']})

def require_preflight(script):
    r = Path(script).parent
    p = json.loads((r / 'preflight_pass.json').read_text())
    if not p.get('reviewed') or p['inputs'] != inputs(r):
        raise RuntimeError('Preflight missing/stale: inspect changed inputs and reseal after real review.')
'''

PREFIX = """from lecture_project_guard import load as _load_lecture
LECTURE_CONFIG = _load_lecture(__import__('pathlib').Path(__file__).parent)
"""


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    p = Path(path)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    os.replace(tmp, p)


def rewrite(name, source, old, new):
    # Only implementation modules are supplied; never copy camera rules or overrides.
    s = source
    for a, b in [(f"ep{old}", f"ep{new}"), (f"Episod_{old}", f"Episod_{new}"),
                 (f"Episode{old}", f"Episode{new}"), (f"episode{old}", f"episode{new}")]:
        s = s.replace(a, b)
    if source.startswith(PREFIX):
        # A checkpoint made by this helper is already parameterized.
        s = re.sub(r"(['\"]episode['\"]\s*:\s*)" + str(old) + r"\b",
                   lambda m: m.group(1) + str(new), s)
        ast.parse(s)
        if '/workspace/scratch/' in s or (old != new and f'ep{old}_' in s):
            raise ValueError('Stale literal in parameterized toolkit: ' + name)
        return s
    if name.endswith("_caption_style.py"):
        s, n = re.subn(r'(["\x27])ARBA\x27IN IMAM GHAZALI \d+\1',
                       "LECTURE_CONFIG['title']", s)
        if n != 1:
            raise ValueError("Unrecognised title template")
    if name.startswith("classify_"):
        s, n = re.subn(r"(['\"])/workspace/scratch/Habib_Omar_Al_Arbain_Usul_al_Din_\d+_720p\.mp4\1",
                       "LECTURE_CONFIG['source']", s)
        if n != 1:
            raise ValueError("Unrecognised classifier source template")
        s = re.sub(r"cache=Path\('/dev/shm/[^']+'\)",
                   "cache=r/'cache/shot_samples.npy';cache.parent.mkdir(exist_ok=True)", s)
    if name.startswith("transcribe_"):
        s, n = re.subn(r"WhisperModel\('[^']+'",
                       "WhisperModel(LECTURE_CONFIG['asr_model']", s, count=1)
        if n != 1:
            raise ValueError("Unrecognised ASR template")
        s = s.replace("cpu_threads=4", "cpu_threads=LECTURE_CONFIG['asr_threads']")
        line = next(x for x in s.splitlines() if x.startswith('model=WhisperModel('))
        identity = """signature=dict(source=LECTURE_CONFIG['source_identity']['sha256'],model=LECTURE_CONFIG['asr_model'],language='ar',beam_size=3,vad_filter=False,word_timestamps=True,condition_on_previous_text=False)
receipt=R/'asr_cache_identity.json'
if list(chunks.glob('*.jsonl')):
 assert receipt.exists() and json.loads(receipt.read_text())==signature,'ASR cache identity/settings mismatch; use fresh chunks'
else:
 receipt.write_text(json.dumps(signature,indent=2))
model=None"""
        s = s.replace(line, identity)
        s = s.replace("  raw=subprocess.check_output(",
                      "  if model is None:\n"
                      "   if not LECTURE_CONFIG['asr_model']:raise RuntimeError('Set asr_model in episode_config.json to a local Whisper snapshot')\n"
                      "   " + line + "\n  raw=subprocess.check_output(")
        # A crash must not turn a partially written state into an apparently valid chunk.
        s = s.replace("if p.exists():continue",
                      "if p.exists():\n   cached=[json.loads(line) for line in p.read_text().splitlines()]\n"
                      "   assert all(set(['start','end','ar_asr','words']).issubset(row) for row in cached),'Invalid cached chunk'\n   continue")
    if name.endswith("_draft_harakat.py"):
        s = s.replace("P=R/'runtime_tashkeel_v2'",
                      "P=__import__('pathlib').Path(LECTURE_CONFIG['tashkeel_runtime'])")
        s = s.replace("(R/'" + f"ep{new}_ar_draft.jsonl" + "').write_text(",
                      "(R/'" + f"ep{new}_ar_draft.jsonl.tmp" + "').write_text(")
        needle = ");print('draft harakat'"
        s = s.replace(needle, ");(R/'" + f"ep{new}_ar_draft.jsonl.tmp" +
                      "').replace(R/'" + f"ep{new}_ar_draft.jsonl" +
                      "');print('draft harakat'")
    if name.endswith("_audio_sync.py"):
        s = s.replace("def au(p,t):", "D=e['duration']\ndef au(p,t):")
        s = s.replace("a=au(src,t);b=au(dst,t)",
                      "seg=next(s for s in e['segments'] if s['output_start']<=t<s['output_end']);"
                      "assert seg['type']=='video' and seg['scale']==1 and t+5<=seg['output_end'],'Use a comparison window inside one normal-speed video segment';"
                      "a=au(seg['path'],seg['source_start']+t-seg['output_start']);b=au(dst,t)")
        s, n = re.subn(r"for t in \[[^\]]+\]:",
                       "for t in [max(0,min(D-5,t)) for t in [25,D/4,D/2,3*D/4,D-60]]:", s)
        if n != 1:
            raise ValueError("Unrecognised sync template")
        s = s.replace("o=dict(source_comparison_samples=rows,",
                      "from lecture_project_guard import audio_identity\no=dict(input_identity=audio_identity(r),source_comparison_samples=rows,")
    if name.startswith("render_"):
        marker = "cmd=['ffmpeg'"
        if s.count(marker) != 1:
            raise ValueError("Unrecognised renderer")
        s = s.replace(marker, "from lecture_project_guard import require_preflight\n"
                      "if master:require_preflight(__file__)\n" + marker)
    # This is a tested format-specific preset, not a generic FPS/geometry converter.
    s = re.sub(r"(['\"]episode['\"]\s*:\s*)" + str(old) + r"\b",
               lambda m: m.group(1) + str(new), s)
    s = PREFIX + s
    ast.parse(s)
    stale = [f"ep{old}_", f"Episod_{old}_", f"Usul_al_Din_{old}_"]
    if old != new and any(token in s for token in stale):
        raise ValueError(f"Stale episode literal in {name}")
    if "/workspace/scratch/" in s:
        raise ValueError(f"Hardcoded workspace source in {name}")
    return s


def initialize(a):
    source = a.source.resolve(strict=True); dest = a.project.resolve()
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", str(dest)):
        raise ValueError("Use a project path without spaces, quotes or colons (FFmpeg filter paths).")
    cfg_path = dest / "episode_config.json"
    if a.resume:
        c = json.loads(cfg_path.read_text())
        if c["episode"] != a.episode or Path(c["source"]) != source or c["source_identity"]["sha256"] != sha(source):
            raise ValueError("Resume identity mismatch; do not reuse this episode's work.")
        print(json.dumps({"status": "reuse_existing", "project": str(dest), "no_files_rewritten": True}))
        return
    if dest.exists():
        raise FileExistsError("Project already exists; use --resume after checking its identity.")
    probe = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(source)]))
    video = next(x for x in probe["streams"] if x["codec_type"] == "video")
    if (video["width"], video["height"], video["r_frame_rate"]) != (1280, 720, "30000/1001"):
        raise ValueError("Fast preset requires 1280x720 30000/1001 input; adapt another format explicitly.")
    if not any(x["codec_type"] == "audio" for x in probe["streams"]):
        raise ValueError("Source has no audio")
    d = float(probe["format"]["duration"]); old = a.template_episode; ep = a.episode; tag = f"ep{ep}"
    names = [f"transcribe_video_ep{old}.py", f"classify_ep{old}_shots.py",
             f"ep{old}_caption_style.py", f"ep{old}_build_ass.py", f"render_ep{old}_ass.py",
             f"ep{old}_draft_harakat.py", f"ep{old}_audio_sync.py",
             f"ep{old}_all_camera_proof.py", f"qa_ep{old}_final.py",
             f"assemble_ep{old}_units.py", "build_episode_audio.py"]
    dest.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".lecture-init-", dir=dest.parent))
    try:
        copied = []
        with zipfile.ZipFile(a.checkpoint) as z:
            font_names = [n for n in z.namelist() if n.startswith("project_fonts/") and
                          Path(n).suffix in [".ttf", ".txt"]]
            selected = names + font_names + [f"ep{old}_source_edge_feather.png"]
            if sum(z.getinfo(n).file_size for n in selected) > 64 * 1024 * 1024:
                raise ValueError("Toolkit unexpectedly exceeds 64MiB")
            for name in selected:
                if ".." in Path(name).parts or stat.S_ISLNK(z.getinfo(name).external_attr >> 16):
                    raise ValueError("Unsafe toolkit member")
                target_name = name.replace(f"ep{old}", tag)
                target = staging / target_name; target.parent.mkdir(parents=True, exist_ok=True)
                if name in names:
                    target.write_text(rewrite(name, z.read(name).decode(), old, ep))
                else:
                    target.write_bytes(z.read(name))
                copied.append(target_name)
        for name in ["Amiri-Regular.ttf", "DejaVuSans.ttf", "Sora[wght].ttf"]:
            if not (staging / "project_fonts" / name).is_file():
                raise ValueError("Missing font: " + name)
        ss = source.stat()
        c = dict(episode=ep, tag=tag, source=str(source), title=a.title, speaker=a.speaker,
                 source_identity=dict(size=ss.st_size, mtime_ns=ss.st_mtime_ns, sha256=sha(source)),
                 asr_model=str(a.asr_model.resolve()) if a.asr_model else None,
                 asr_threads=a.asr_threads,
                 tashkeel_runtime=str(a.tashkeel_runtime.resolve()) if a.tashkeel_runtime else str(dest / "runtime_tashkeel_v2"),
                 drive_parent_id=a.drive_parent_id, template_episode=old, toolkit_files=copied)
        write_json(staging / "episode_config.json", c)
        write_json(staging / f"{tag}_source_metadata.json", dict(path=str(source), probe=probe))
        write_json(staging / f"{tag}_production_edl.json",
                   dict(episode=ep, trim_start=0, trim_end=d, duration=d,
                        segments=[dict(type="video", output_start=0, output_end=d, source_start=0, scale=1, path=str(source))],
                        render_ready=False, cut_policy="Measure first; silence at beginning/end only unless user says otherwise.",
                        speaker_labels=[dict(start=0, end=d, label=a.speaker)]))
        (staging / "lecture_project_guard.py").write_text(GUARD)
        (staging / "cache").mkdir()
        # Camera maps, reviewed units, Quran overrides, QA and upload receipts are deliberately absent.
        os.rename(staging, dest)
        print(json.dumps({"status": "created", "project": str(dest), "toolkit_files": len(copied),
                          "next": "Measure terminal silence; start ASR/audio/camera work once; review new camera map."}))
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def seal(a):
    r = a.project.resolve()
    import importlib.util
    spec = importlib.util.spec_from_file_location("lecture_guard", r / "lecture_project_guard.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    c = module.load(r); tag = c["tag"]
    review = json.loads(a.review.read_text())
    if not review.get("reviewer") or review.get("camera_samples_reviewed", 0) < 1 or not review.get("preview_windows"):
        raise ValueError("Real camera/encoded-preview review is required before sealing.")
    sync = json.loads((r / f"{tag}_audio_pre_render_sync.json").read_text())
    if not sync.get("all_lag_under45ms"):
        raise ValueError("Source audio sync has not passed.")
    if sync.get('input_identity') != module.audio_identity(r):
        raise ValueError('Audio/timeline changed since sync check; rerun audio sync.')
    e = json.loads((r / f"{tag}_production_edl.json").read_text())
    e["render_ready"] = True
    write_json(r / f"{tag}_production_edl.json", e)
    try:
        write_json(r / "preflight_pass.json", dict(reviewed=True, review=review, inputs=module.inputs(r)))
    except BaseException:
        e["render_ready"] = False; write_json(r / f"{tag}_production_edl.json", e)
        raise
    print("Preflight sealed; master refuses changed source/text/camera/audio/code inputs.")


def main():
    p = argparse.ArgumentParser(description=__doc__); sub = p.add_subparsers(dest="action", required=True)
    i = sub.add_parser("init")
    for name in ["project", "source", "checkpoint"]:
        i.add_argument("--" + name, type=Path, required=True)
    i.add_argument("--episode", type=int, required=True)
    i.add_argument("--template-episode", type=int, required=True)
    i.add_argument("--title", required=True); i.add_argument("--speaker", required=True)
    i.add_argument("--asr-model", type=Path); i.add_argument("--asr-threads", type=int, default=4)
    i.add_argument("--tashkeel-runtime", type=Path); i.add_argument("--drive-parent-id")
    i.add_argument("--resume", action="store_true")
    s = sub.add_parser("seal-preflight"); s.add_argument("--project", type=Path, required=True)
    s.add_argument("--review", type=Path, required=True)
    a = p.parse_args()
    if a.action == "init":
        if a.episode < 1 or a.template_episode < 1 or a.asr_threads < 1:
            p.error("Episode and thread values must be positive.")
        initialize(a)
    else:
        seal(a)


if __name__ == "__main__":
    main()
