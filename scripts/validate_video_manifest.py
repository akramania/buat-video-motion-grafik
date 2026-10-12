#!/usr/bin/env python3
"""Validate a scene-based motion-graphics timeline for one final MP4.

The manifest is JSON and uses absolute seconds on the FINAL timeline. Overlaps
are represented by the incoming scene starting before the previous scene ends.
This tool checks metadata and arithmetic; it does not inspect media or verify
that quotations and sources are factually correct.

    python3 validate_video_manifest.py --example > example.json
    python3 validate_video_manifest.py example.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys
from typing import Any


MAX_DURATION = 30 * 60


def example_manifest() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "title": "Contoh video motion grafik",
        "output_file": "video_akhir.mp4",
        "duration_seconds": 14.0,
        "fps": 24,
        "default_voice": "ms-MY-OsmanNeural",
        "chapters": [
            {
                "id": "bab_01", "order": 1, "title": "Pembukaan",
                "scene_ids": ["babak_001", "babak_002"],
            },
        ],
        "scenes": [
            {
                "id": "babak_001", "order": 1, "chapter_id": "bab_01",
                "start_seconds": 0.0, "end_seconds": 8.0,
                "visual": {
                    "description": "Watak masuk ke kedai; kamera mengikuti langkahnya.",
                    "characters": ["Watak utama"],
                    "motion": "Pergerakan watak, parallax dan perubahan ekspresi.",
                },
                "on_screen_text": "Ada kisah di sebalik setiap langkah.",
                "narration": {"text": "Petang itu aku berhenti sebentar di hadapan kedai."},
                "transition_in": {"type": "cut"},
            },
            {
                "id": "babak_002", "order": 2, "chapter_id": "bab_01",
                "start_seconds": 7.5, "end_seconds": 14.0,
                "visual": "Pintu terbuka dan cahaya lembut memenuhi bingkai.",
                "narration": {"text": "Dari situ, cerita kami bermula."},
                "transition_in": {"type": "overlap", "duration_seconds": 0.5},
            },
        ],
    }


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def is_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(manifest: Any) -> list[str]:
    errors: list[str] = []

    def err(location: str, message: str) -> None:
        errors.append(f"{location}: {message}")

    if not isinstance(manifest, dict):
        return ["manifest: expected a JSON object"]
    if not isinstance(manifest.get("schema_version"), int) or isinstance(manifest.get("schema_version"), bool) or manifest["schema_version"] != 1:
        err("schema_version", "expected integer 1")

    output_file = manifest.get("output_file")
    if not is_text(output_file) or Path(output_file).name != output_file or "\\" in output_file or not output_file.lower().endswith(".mp4") or output_file.lower() == ".mp4":
        err("output_file", "provide exactly one .mp4 filename, without a directory")

    total = manifest.get("duration_seconds")
    if not is_number(total) or not 0 < total <= MAX_DURATION:
        err("duration_seconds", "must be finite and greater than 0, at most 1800 seconds")

    fps = manifest.get("fps", 24)
    if not isinstance(fps, int) or isinstance(fps, bool) or not 1 <= fps <= 120:
        err("fps", "must be an integer from 1 to 120")
        fps = 24
    # Half a frame accounts for timestamps rounded to two or three decimals.
    tolerance = 0.5 / fps + 1e-6

    default_voice = manifest.get("default_voice")
    if default_voice is not None and not is_text(default_voice):
        err("default_voice", "must be a nonempty voice identifier")

    scenes = manifest.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        err("scenes", "must be a nonempty list")
        scenes = []

    seen_ids: set[str] = set()
    scene_ids: list[str] = []
    scene_by_id: dict[str, dict[str, Any]] = {}
    previous: dict[str, Any] | None = None
    before_previous: dict[str, Any] | None = None
    for index, scene in enumerate(scenes, 1):
        location = f"scenes[{index - 1}]"
        if not isinstance(scene, dict):
            err(location, "expected an object")
            continue

        ident = scene.get("id")
        if not is_text(ident):
            err(location + ".id", "must be a nonempty string")
        elif ident in seen_ids:
            err(location + ".id", f"duplicate ID {ident!r}")
        else:
            seen_ids.add(ident)
            scene_ids.append(ident)
            scene_by_id[ident] = scene
        if scene.get("order") != index or isinstance(scene.get("order"), bool):
            err(location + ".order", f"must be the contiguous sequence number {index}")

        start, end = scene.get("start_seconds"), scene.get("end_seconds")
        good_interval = is_number(start) and is_number(end) and 0 <= start < end
        if not good_interval:
            err(location, "start_seconds/end_seconds must be finite with 0 <= start < end")

        visual = scene.get("visual")
        if not (is_text(visual) or (isinstance(visual, dict) and is_text(visual.get("description")))):
            err(location + ".visual", "provide a nonempty string or an object with description")

        screen_text = scene.get("on_screen_text")
        if screen_text is not None and not (is_text(screen_text) or
                                            (isinstance(screen_text, list) and screen_text and all(is_text(x) for x in screen_text))):
            err(location + ".on_screen_text", "must be nonempty text or a nonempty list of text")

        narration = scene.get("narration")
        if narration is not None:
            if not isinstance(narration, dict):
                err(location + ".narration", "must be an object with text")
            else:
                if not is_text(narration.get("text")):
                    err(location + ".narration.text", "must be nonempty")
                voice_id = narration.get("voice_id", default_voice)
                if not is_text(voice_id):
                    err(location + ".narration.voice_id", "set voice_id or top-level default_voice")
                if "audio_file" in narration and not is_text(narration["audio_file"]):
                    err(location + ".narration.audio_file", "must be a nonempty path when supplied")

        sources = scene.get("sources")
        if sources is not None:
            if not isinstance(sources, list):
                err(location + ".sources", "must be a list")
            else:
                for source_index, source in enumerate(sources):
                    source_location = f"{location}.sources[{source_index}]"
                    if is_text(source):
                        continue
                    if not isinstance(source, dict) or not (is_text(source.get("url")) or is_text(source.get("reference"))):
                        err(source_location, "provide a nonempty URL/reference string or object")
                    elif "claim" in source and not is_text(source["claim"]):
                        err(source_location + ".claim", "must be nonempty when supplied")
        requires_source = scene.get("requires_source", False)
        if not isinstance(requires_source, bool):
            err(location + ".requires_source", "must be true or false")
        elif requires_source and (not isinstance(sources, list) or not sources):
            err(location + ".sources", "at least one source required for this scene")

        quran = scene.get("quran")
        if quran is not None:
            quran_items = quran if isinstance(quran, list) else [quran]
            if not quran_items:
                err(location + ".quran", "must contain at least one verse")
            for verse_index, verse in enumerate(quran_items):
                verse_location = location + ".quran" + (f"[{verse_index}]" if isinstance(quran, list) else "")
                if not isinstance(verse, dict):
                    err(verse_location, "must be an object with verse, translation, translator and source")
                    continue
                surah = verse.get("surah")
                if not isinstance(surah, int) or isinstance(surah, bool) or not 1 <= surah <= 114:
                    err(verse_location + ".surah", "must be a surah number from 1 to 114")
                for field in ("ayah", "source_url"):
                    if not is_text(verse.get(field)):
                        err(verse_location + f".{field}", "must be nonempty")
                show_translation = verse.get("display_translation")
                if not isinstance(show_translation, bool):
                    err(verse_location + ".display_translation", "choose true or false explicitly")
                if show_translation is True:
                    for field in ("translation", "translator"):
                        if not is_text(verse.get(field)):
                            err(verse_location + f".{field}", "must be nonempty when showing a translation")

        transition = scene.get("transition_in", {"type": "cut"})
        if not isinstance(transition, dict) or transition.get("type") not in ("cut", "overlap"):
            err(location + ".transition_in", "choose type cut or overlap")
            transition = {"type": "cut"}
        transition_type = transition.get("type")
        transition_duration = transition.get("duration_seconds", 0)
        if not is_number(transition_duration):
            err(location + ".transition_in.duration_seconds", "must be finite")
        elif transition_type == "cut" and transition_duration != 0:
            err(location + ".transition_in.duration_seconds", "cut must have zero duration")
        elif transition_type == "overlap" and transition_duration <= 0:
            err(location + ".transition_in.duration_seconds", "overlap must have positive duration")

        if index == 1:
            if good_interval and abs(start) > tolerance:
                err(location + ".start_seconds", "first scene must start at zero")
            if transition_type != "cut":
                err(location + ".transition_in", "first scene must enter by cut")
        elif previous and good_interval and previous.get("good_interval"):
            previous_end = previous["end"]
            target = previous_end if transition_type == "cut" else (
                previous_end - transition_duration if is_number(transition_duration) else math.nan
            )
            if is_number(target) and abs(start - target) > tolerance:
                err(location + ".start_seconds", f"{transition_type} must start at {target:g}s; no gap or unplanned overlap")
            if end <= previous_end + tolerance:
                err(location + ".end_seconds", "each next scene must extend the final timeline")
            if transition_type == "overlap" and is_number(transition_duration):
                if transition_duration >= min(end - start, previous_end - previous["start"]) - tolerance:
                    err(location + ".transition_in.duration_seconds", "overlap must be shorter than both adjacent scenes")
                if before_previous and before_previous.get("good_interval") and start < before_previous["end"] - tolerance:
                    err(location + ".transition_in", "three scenes overlap; use a dedicated composite scene instead")

        before_previous, previous = previous, {"start": start, "end": end, "good_interval": good_interval}

    if scenes and previous and previous.get("good_interval") and is_number(total):
        if abs(previous["end"] - total) > tolerance:
            err("duration_seconds", f"must equal final scene end ({previous['end']:g}s), not the sum of overlapping scene lengths")

    chapters = manifest.get("chapters")
    if chapters is not None:
        if not isinstance(chapters, list) or not chapters:
            err("chapters", "if supplied, must be a nonempty list")
        else:
            flattened: list[str] = []
            seen_chapter_ids: set[str] = set()
            for chapter_index, chapter in enumerate(chapters, 1):
                location = f"chapters[{chapter_index - 1}]"
                if not isinstance(chapter, dict):
                    err(location, "expected an object")
                    continue
                ident = chapter.get("id")
                if not is_text(ident):
                    err(location + ".id", "must be nonempty")
                elif ident in seen_chapter_ids:
                    err(location + ".id", f"duplicate ID {ident!r}")
                else:
                    seen_chapter_ids.add(ident)
                if chapter.get("order") != chapter_index or isinstance(chapter.get("order"), bool):
                    err(location + ".order", f"must be the contiguous sequence number {chapter_index}")
                if not is_text(chapter.get("title")):
                    err(location + ".title", "must be nonempty")
                listed = chapter.get("scene_ids")
                if not isinstance(listed, list) or not listed or not all(is_text(x) for x in listed):
                    err(location + ".scene_ids", "must be a nonempty list of scene IDs")
                    continue
                flattened.extend(listed)
                for scene_id in listed:
                    matched = scene_by_id.get(scene_id)
                    if matched is not None and matched.get("chapter_id") != ident:
                        err(location + ".scene_ids", f"scene {scene_id!r} must set chapter_id {ident!r}")
            if flattened != scene_ids:
                err("chapters", "scene_ids must partition all scenes once, in timeline order")
    else:
        for scene_index, scene in enumerate(scenes):
            if isinstance(scene, dict) and "chapter_id" in scene:
                err(f"scenes[{scene_index}].chapter_id", "define chapters to use chapter_id")

    return errors


def reject_nonfinite(value: str) -> None:
    raise ValueError(f"non-finite JSON number {value!r} is not allowed")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path, help="path to a JSON project manifest")
    parser.add_argument("--example", action="store_true", help="print an example valid manifest as JSON")
    args = parser.parse_args()
    if args.example:
        if args.manifest:
            parser.error("--example takes no manifest path")
        print(json.dumps(example_manifest(), indent=2, ensure_ascii=False))
        return 0
    if not args.manifest:
        parser.error("provide a manifest path or --example")
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"), parse_constant=reject_nonfinite)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"INVALID {args.manifest}: {exc}", file=sys.stderr)
        return 2
    errors = validate(manifest)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        print(f"INVALID: {len(errors)} error(s)", file=sys.stderr)
        return 1
    print(f"VALID: {len(manifest['scenes'])} scene(s), {manifest['duration_seconds']:g}s, one MP4 ({manifest['output_file']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
