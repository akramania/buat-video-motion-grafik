#!/usr/bin/env python3
"""Offline, dependency-free PNG-sequence to MP4 bridge (requires FFmpeg).

Examples:
  python local_mp4.py preflight
  python local_mp4.py frames --input 'frames/frame_%06d.png' --fps 30 --output 'My video.mp4'
  python local_mp4.py qa --input 'My video.mp4'

Only numbered PNG input is supported. No packages are installed, no network is
used, and existing output files are preserved unless --overwrite is supplied.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile


ALLOWED_FPS = (24, 25, 30, 50, 60)


class BridgeError(Exception):
    pass


def run(argv: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, check=False)
    except OSError as exc:
        raise BridgeError(f"Could not run {argv[0]}: {exc}") from exc
    if proc.returncode:
        raise BridgeError(f"{Path(argv[0]).name} exited {proc.returncode}: {proc.stderr[-6000:].strip()}")
    return proc


def executable(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise BridgeError(f"Required executable unavailable: {name}. No installation was attempted.")
    return found


def preflight() -> dict:
    commands = {}
    for name in ("ffmpeg", "ffprobe", "node"):
        path = shutil.which(name)
        item = {"available": bool(path), "path": path}
        if path:
            try:
                item["version"] = run([path, "--version" if name == "node" else "-version"]).stdout.splitlines()[0]
            except BridgeError as exc:
                item["error"] = str(exc)
        commands[name] = item
    encoders = {"libx264": False, "aac": False}
    if commands["ffmpeg"].get("available") and not commands["ffmpeg"].get("error"):
        try:
            listing = run([commands["ffmpeg"]["path"], "-hide_banner", "-encoders"]).stdout
            for name in encoders:
                encoders[name] = re.search(r"^\s*[A-Z.]{6}\s+" + re.escape(name) + r"\s", listing, re.MULTILINE) is not None
        except BridgeError as exc:
            commands["ffmpeg"]["encoder_probe_error"] = str(exc)
    modules = {}
    for name in ("PIL", "numpy", "cairosvg", "cv2", "manim", "torch"):
        try:
            modules[name] = importlib.util.find_spec(name) is not None
        except (ImportError, ValueError):
            modules[name] = False
    node_modules = {}
    if commands["node"]["available"]:
        # Node resolves only installed local packages; this never invokes npm.
        script = "const out={};for(const n of process.argv.slice(1)){try{out[n]=require.resolve(n)}catch(e){out[n]=null}}process.stdout.write(JSON.stringify(out))"
        try:
            node_modules = json.loads(run([commands["node"]["path"], "-e", script, "p5", "playwright", "gsap", "three", "lottie-web", "sharp", "@napi-rs/canvas"]).stdout)
        except BridgeError as exc:
            node_modules = {"error": str(exc)}
    return {
        "ready": all(commands[name].get("available") and not commands[name].get("error") for name in ("ffmpeg", "ffprobe")) and encoders["libx264"],
        "python": sys.version.split()[0], "executables": commands, "encoders": encoders,
        "optional_python_modules": modules, "optional_node_modules": node_modules,
        "network_used": False, "installations_attempted": False,
    }


def png_dimensions(path: Path) -> tuple[int, int]:
    try:
        with path.open("rb") as handle:
            head = handle.read(33)
    except OSError as exc:
        raise BridgeError(f"Cannot read PNG {path}: {exc}") from exc
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n" or head[8:16] != b"\x00\x00\x00\rIHDR":
        raise BridgeError(f"Invalid PNG header: {path}")
    width, height = struct.unpack(">II", head[16:24])
    if not width or not height:
        raise BridgeError(f"Invalid PNG dimensions: {path}")
    return width, height


def inspect_sequence(pattern: str, expected_start: int | None, expected_count: int | None) -> dict:
    path = Path(pattern).expanduser().absolute()
    matches = list(re.finditer(r"%(?:0([1-9][0-9]*))?d", path.name))
    if len(matches) != 1 or "%" in path.name[:matches[0].start()] + path.name[matches[0].end():]:
        raise BridgeError("Input filename must contain exactly one %d or %0Nd placeholder, such as frame_%06d.png.")
    match = matches[0]
    if path.suffix.lower() != ".png":
        raise BridgeError("Only numbered PNG sequences are supported.")
    prefix, suffix = path.name[:match.start()], path.name[match.end():]
    minimum_width = int(match.group(1) or 0)
    candidate = re.compile(re.escape(prefix) + r"([0-9]+)" + re.escape(suffix) + r"\Z")
    if not path.parent.is_dir():
        raise BridgeError(f"Input directory does not exist: {path.parent}")
    frames = []
    for entry in path.parent.iterdir():
        number_match = candidate.fullmatch(entry.name)
        if number_match:
            number = int(number_match.group(1))
            canonical = prefix + (str(number).zfill(minimum_width) if minimum_width else str(number)) + suffix
            if entry.name != canonical:
                raise BridgeError(f"Frame filename does not follow the input pattern: {entry.name}")
            if not entry.is_file():
                raise BridgeError(f"Frame is not a regular readable file: {entry}")
            frames.append((number, entry))
    frames.sort()
    if not frames:
        raise BridgeError(f"No PNG frames match {path}")
    start = frames[0][0]
    if expected_start is not None and start != expected_start:
        raise BridgeError(f"Sequence starts at {start}; expected {expected_start}.")
    if expected_count is not None and len(frames) != expected_count:
        raise BridgeError(f"Found {len(frames)} frames; expected {expected_count}.")
    dimensions = png_dimensions(frames[0][1])
    if dimensions[0] % 2 or dimensions[1] % 2:
        raise BridgeError(f"H.264 yuv420p requires even dimensions; got {dimensions[0]}x{dimensions[1]}. No resize was performed.")
    total_bytes = 0
    for offset, (number, entry) in enumerate(frames):
        if number != start + offset:
            raise BridgeError(f"Nonconsecutive sequence: expected frame {start + offset}, found {number}.")
        if png_dimensions(entry) != dimensions:
            raise BridgeError(f"PNG dimensions differ at {entry}; expected {dimensions[0]}x{dimensions[1]}. No resize was performed.")
        total_bytes += entry.stat().st_size
    return {"pattern": str(path), "start_number": start, "frame_count": len(frames), "width": dimensions[0], "height": dimensions[1], "total_input_bytes": total_bytes}


def probe(path: Path) -> dict:
    data = json.loads(run([executable("ffprobe"), "-v", "error", "-count_frames", "-show_format", "-show_streams", "-of", "json", str(path)]).stdout)
    streams = []
    for stream in data.get("streams", []):
        keys = ("index", "codec_type", "codec_name", "pix_fmt", "width", "height", "avg_frame_rate", "r_frame_rate", "duration", "nb_frames", "nb_read_frames", "sample_rate", "channels")
        streams.append({key: stream[key] for key in keys if key in stream})
    return {"path": str(path), "duration_seconds": float(data.get("format", {}).get("duration", 0)), "size_bytes": int(data.get("format", {}).get("size", 0)), "streams": streams}


def qa(path: Path) -> dict:
    if not path.is_file():
        raise BridgeError(f"Input video does not exist: {path}")
    report = probe(path)
    if not any(stream.get("codec_type") == "video" for stream in report["streams"]):
        raise BridgeError(f"No video stream: {path}")
    run([executable("ffmpeg"), "-hide_banner", "-v", "error", "-xerror", "-err_detect", "explode", "-i", str(path), "-map", "0:v", "-map", "0:a?", "-f", "null", "-"])
    report["full_decode_passed"] = True
    return report


def encode(args: argparse.Namespace) -> dict:
    ffmpeg = executable("ffmpeg")
    executable("ffprobe")
    sequence = inspect_sequence(args.input, args.start_number, args.count)
    output = Path(args.output).expanduser().absolute()
    if output.suffix.lower() != ".mp4":
        raise BridgeError("Output must have an .mp4 extension.")
    if not output.parent.is_dir():
        raise BridgeError(f"Output directory does not exist: {output.parent}")
    if output.exists() and not args.overwrite:
        raise BridgeError(f"Output exists: {output}. Use --overwrite explicitly to replace it.")
    duration = Fraction(sequence["frame_count"], args.fps)
    duration_text = f"{float(duration):.12f}"
    audio = Path(args.audio).expanduser().absolute() if args.audio else None
    if audio and not audio.is_file():
        raise BridgeError(f"Audio does not exist: {audio}")
    if audio and audio == output:
        raise BridgeError("Audio input and video output must be different files.")
    fd, temporary_name = tempfile.mkstemp(prefix=".local_mp4_", suffix=".mp4", dir=output.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        # image2 parses printf escapes across the entire path, including parent
        # directories. Escape their literal percent signs, retaining the single
        # authoritative filename placeholder and the unescaped report metadata.
        input_path = Path(sequence["pattern"])
        image2_pattern = str(input_path.parent).replace("%", "%%") + os.sep + input_path.name
        command = [ffmpeg, "-hide_banner", "-v", "error", "-xerror", "-nostdin", "-y", "-framerate", str(args.fps), "-start_number", str(sequence["start_number"]), "-i", image2_pattern]
        if audio:
            command += ["-i", str(audio)]
        command += ["-map", "0:v:0", "-frames:v", str(sequence["frame_count"]), "-vf", "setsar=1", "-c:v", "libx264", "-preset", args.preset, "-crf", str(args.crf), "-pix_fmt", "yuv420p"]
        if audio:
            # Every permitted fps divides 48,000, so audio duration is exact in samples.
            samples = sequence["frame_count"] * 48000 // args.fps
            command += ["-map", "1:a:0", "-af", f"aresample=48000,apad,atrim=end_sample={samples},asetpts=N/SR/TB", "-c:a", "aac", "-b:a", "192k", "-t", duration_text]
        else:
            command += ["-an"]
        command += ["-movflags", "+faststart", str(temporary)]
        run(command)
        report = qa(temporary)
        video = next(stream for stream in report["streams"] if stream.get("codec_type") == "video")
        if int(video.get("nb_read_frames", -1)) != sequence["frame_count"]:
            raise BridgeError("Encoded frame count does not match the complete input sequence.")
        if (video.get("width"), video.get("height")) != (sequence["width"], sequence["height"]):
            raise BridgeError("Encoded dimensions do not match input dimensions.")
        if Fraction(video.get("avg_frame_rate", "0/1")) != args.fps:
            raise BridgeError("Encoded frame rate does not match the requested integer fps.")
        if abs(float(video.get("duration", 0)) - float(duration)) > 0.001:
            raise BridgeError("Encoded video duration does not match the visual timeline.")
        if audio:
            audio_stream = next((stream for stream in report["streams"] if stream.get("codec_type") == "audio"), None)
            if audio_stream is None or abs(float(audio_stream.get("duration", 0)) - float(duration)) > 0.025:
                raise BridgeError("Encoded audio duration does not match the visual timeline within one AAC packet.")
        if args.overwrite:
            os.replace(temporary, output)
        else:
            # A same-directory hard link commits atomically without clobbering a
            # file that another process may have created after the initial check.
            os.link(temporary, output)
            temporary.unlink()
        report["path"] = str(output)
        report["sequence"] = sequence
        report["expected_duration_seconds"] = float(duration)
        report["audio_policy"] = "pad silence or trim to visual duration; 48kHz AAC" if audio else "no audio"
        return report
    finally:
        if temporary.exists():
            temporary.unlink()


def positive_int(value: str) -> int:
    result = int(value)
    if result <= 0:
        raise argparse.ArgumentTypeError("Must be positive.")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="action", required=True)
    subparsers.add_parser("preflight", help="Report installed executables and optional packages; never install or download.")
    frames = subparsers.add_parser("frames", help="Validate a complete numbered PNG sequence, encode, and fully decode-check an MP4.")
    frames.add_argument("--input", required=True, help="PNG pattern, e.g. '/path/frame_%%06d.png'.")
    frames.add_argument("--output", required=True)
    frames.add_argument("--fps", type=int, choices=ALLOWED_FPS, required=True)
    frames.add_argument("--start-number", type=int, help="Require this first frame number; otherwise detect it.")
    frames.add_argument("--count", type=positive_int, help="Require this exact frame count.")
    frames.add_argument("--audio", help="Optional existing audio; pad silence or trim to visual duration.")
    frames.add_argument("--overwrite", action="store_true")
    frames.add_argument("--crf", type=int, choices=range(0, 52), default=18, metavar="0..51")
    frames.add_argument("--preset", choices=("ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"), default="medium")
    qa_parser = subparsers.add_parser("qa", help="Probe metadata/frame counts and decode all video/audio to null.")
    qa_parser.add_argument("--input", required=True)
    args = parser.parse_args()
    try:
        result = preflight() if args.action == "preflight" else encode(args) if args.action == "frames" else qa(Path(args.input).expanduser().absolute())
    except (BridgeError, OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps({"ok": True, **result}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
