![Motion Atlas Studio](https://github.com/user-attachments/assets/d2c103cc-fcf8-4756-bbc7-5f6525ddf103)

# Motion Atlas Studio

### 5,122 creative entries. One adaptable video production toolkit.

Build motion graphics, animated explainers, product promos and editorial montages with an agent skill for **ChatGPT Work and Codex**, supported by reusable Python and Node renderers, original vector artwork, typography systems and production references.

**Explore the [Motion Atlas](https://motion-preset-atlas.akramania.chatgpt.site).**

## Current skill update: 6 November 2026

The repository now incorporates the current **Buat Video Motion Grafik** instructions, **Gaya Ekstrem**, the expanded HyperFrames production guidance and the **3 November 2026 component lock**. Read the [comparison and verification record](references/repository-sync-2026-11-06.md), [Gaya Ekstrem direction](references/gaya-ekstrem.md), [nine HyperFrames workflows](references/hyperframes-nine-workflows.md) and [component restoration guide](references/video-component-toolkit.md).

Gaya Ekstrem uses large kinetic typography, changing position and scale, progressive layered SVG builds, several coordinated motion speeds, accurate numeric counters, perspective image carousels and action-linked music/SFX/ASMR. Preserve supplied images; generate actual raster assets when requested. Keep reading time while the composition evolves. Do not add decorative scene numbers, scene titles or branding. Other styles remain available, including Learnfly educational/editorial, live-commerce promotion, word-and-phone showcases, vector character stories, paper-cut compositions and the 48 MotionPrompt style recipes. Select the style for the brief.

### Locked video components

These are the versions recorded in the installed skill's dated lock, rather than a claim that every upstream package is the newest today. Full URLs, checksums and provenance are in [runtime-lock.json](assets/runtime-lock.json).

| Component | Pinned version / role |
| --- | --- |
| Node.js / npm | 26.13.0 / 11.20.0; minimum Node 22.12.0 |
| HyperFrames | 0.9.4; local CLI and complete dependency lock |
| GSAP | 3.15.0, with DrawSVGPlugin, MorphSVGPlugin, MotionPathPlugin and SplitText |
| Chrome for Testing | 156.0.8078.80; Linux x64 glibc binary lock |
| FFmpeg / ffprobe | Maintained 9.0 build n9.0.2-45-g1e65c6cd5d, dated 2 November |
| Whisper | faster-whisper 1.2.1; av 16.1.0; pinned multilingual medium model revision |
| Three.js | 0.187.0; use actual WebGL proof when selected |
| React / React DOM | 19.3.1 for both |
| Remotion | 4.0.540 and matching renderer, CLI and bundler; optional workflow |

Check existing caches before restoring missing components:

```bash
python3 scripts/setup_video_components.py --offline --report components-ready.json
# Restore only if required; add --offline to use complete local archives/cache.
python3 scripts/setup_video_components.py --install --report components-ready.json
# Add production audio readiness when the task requires transcription.
python3 scripts/setup_video_components.py --install --whisper --model medium --report components-ready.json
```

Keep large binaries, complete node_modules and model weights in reusable runtime caches; repository locks and helpers restore them. Actual readiness requires browser launch or model load/decode, then a short proof. The imported [3 November validation record](assets/hyperframes/validation.json) reports a browser-launch block in its original execution environment; it does **not** certify successful MP4/WebGL/Remotion rendering with these versions. Run `doctor → lint → check → snapshot → proof → render → QA` in the target environment. Preserve the original Python Atlas renderer and its deterministic cache fixes. This source update does not republish npm, historical GitHub releases or external Drive packs.

## Atlas v12 — locked presets and selective Gemini cache

The current source matches the published Atlas v12 workflow: use the original Python renderer through `scripts/atlas_preset.py`, with pinned source hashes, validated job parameters and reference-frame checks across all **922 presets**. Download a job from Atlas or generate it with `init`; do not recreate a preset from its name or prompt.

Edit existing video directly with **Python/FFmpeg**. Use **HTML/GSAP + HyperFrames** for vector/cartoon animation. The engine follows the task, not a mandatory HTML conversion.

For Gemini, follow `SKILL_Gemini.md` and `references/selective-cache.md`. Check VM storage, installed-file hashes and cached ZIPs first. Download only the required missing or invalid packs from the dated Drive manifest; never install every pack by default. The current manifest has **10 selective packs**, including Creator FX 80. The cache helper performs local planning, verification and safe installation without network access.

Current downloads: [Drive folder](https://drive.google.com/drive/folders/1QF3fxMu5ruysNbw92Jii5aU3xyb-tiJF). The compact locked toolkit and full manifest are linked in `references/atlas-drive-runtime.md` and `references/selective-cache.md`. Existing v1.1.0 release assets and the dated Drive packs describe their original snapshots; use repository source for this November skill update.

## Creator FX 80 — current repository source

The current source adds **80 Creator FX recipes** (CFX01–CFX80), including 60 new techniques for layered reels, product inserts, animated captions, charts, routes and editorial compositions. Explore the [Creator FX 80 previews in Motion Atlas](https://motion-preset-atlas.akramania.chatgpt.site/?family=CFX#catalogue). These are original adaptations of observed principles, rendered as silent vector demonstrations; use prepared footage, masks and timing for a real project. The new set was informed by 11 accessible Instagram references; three unavailable references were skipped. See `references/creator-fx-80.md` for provenance, inputs and QA.

Use the current source or the dated 27 October Drive packs for Creator FX 80. The older v1.1.0 release assets predate this update.

## Historical v1.1.0 — HTML/HyperFrames and Gemini offline packs

The 22 October 2026 release adds a seekable HTML/SVG + GSAP + HyperFrames workflow, DrawSVG/MorphSVG/MotionPath/SplitText, local Whisper and background removal helpers, a 20-character V3 bank, and Arabic–Malay lecture editing guidance. The original Python/FFmpeg toolkit and all five Atlas collections remain available.

Download the complete ChatGPT/Codex distribution or the Gemini installer bundle from [Releases](https://github.com/akramania/buat-video-motion-grafik/releases). The Gemini bundle contains all 12 independently extractable packs, its manifest, entrypoint and offline installer. Provision Node 22.12+, compatible npm dependencies, Chrome and optional ASR/rembg models during setup; runtime binaries are not bundled for every OS/CPU. See `references/html-hyperframes-production.md` and `references/character-bank-20.md`.

## The collection

| Collection | Included | Creative possibilities |
|---|---:|---|
| Animation presets | **922** | Kinetic typography, UI, product reveals, maps, charts, counters, paper effects, transitions and 80 Creator FX recipes |
| Modular motion components | **2,000** | Shapes, arrows, HUD and data layers, transitions, particles and light |
| SVG assets | **1,500** | Explainer illustrations, icons, learning diagrams and promotional compositions |
| Vlog and montage assets | **600** | 100 LUTs, 100 transitions, 100 animated overlays, 100 vlog graphics, 100 montage graphics and 100 SFX |
| Curated font families | **100** | Display, editorial and Arabic typography, with original font license files |
| **Total creative entries** | **5,122** | Separate catalog entries across the five collections |

The **922 presets** comprise **137 core presets, 185 guide adaptations, 120 preview adaptations, 400 premium recipes and 80 Creator FX recipes**. The **2,000 modular components** comprise **100 design families with 20 structural variations each**. These categories remain distinct; font families are included in the total. Counts describe creative entries, not 5,122 standalone video templates.

## Design with motion

- Shape the story with layered compositions and separate entrance, activity and exit cues.
- Give words rhythm with measured kinetic typography, highlights, counters and captions.
- Explain products through dashboards, notifications, app screens and perspective mockups.
- Turn maps and example data into route animations, chart builds and geographic metrics.
- Finish montages with color treatments, moving overlays, transitions and sound accents.
- Follow a production workflow for scripting, audio timing, rendering and visual quality checks.

## 30 use cases and English prompts

Replace the bracketed fields and attach the named sources. `@Buat Video Motion Grafik` in ChatGPT and `$buat-video-motion-grafik` in Codex refer to this skill. Prompts below are in English; change the requested output language as needed. Every request is for a rendered video, with project-specific preflight, proof and final media QA. For HyperFrames projects, follow the guidelines, motion rules and production workflow already adapted in the skill and use the actual HyperFrames runtime. If a required capability is blocked, report it accurately.

| # | Use case | Copy-ready English prompt |
| --- | --- | --- |
| 1 | Website launch | Use $buat-video-motion-grafik to create a 120-second landscape 1920x1080 launch video for [URL]. Inspect the live website, capture real browsing b-roll and screenshots, and build a hook, problem, demonstration, benefits and CTA. Combine full-frame website footage with perspective browser and phone mockups. Use HyperFrames for the animated compositions, energetic music, synchronized SFX and subtle ASMR, without voice-over. Deliver the final MP4. |
| 2 | Product explainer | Use $buat-video-motion-grafik to create a 60-second 16:9 explainer for [product] using the attached product images and [verified features]. Show the problem, how the product works and the resulting benefit through layered 2D/2.5D artwork and varied camera moves. Preserve original product photos and labels. Add concise English text, music and action-linked SFX, without voice-over. Render with HyperFrames and deliver an MP4. |
| 3 | Gaya Ekstrem social ad | Use $buat-video-motion-grafik, Gaya Ekstrem, to create a 30-second 1080x1920 ad for [offer]. Use a strong hook, short English phrases, aggressive kinetic typography, large position and scale changes, progressively assembled SVG props and accurate counters for every project-created number. Keep the sequence flowing without scene pauses while preserving reading time. Add high-energy music, SFX and ASMR, without voice-over. Follow HyperFrames and deliver the MP4. |
| 4 | SaaS feature demo | Use $buat-video-motion-grafik to create a 60-second landscape demo of [feature] from [URL or supplied screen recording]. Show the actual user actions and outcomes, removing loading and idle time. Animate real interface crops, cursor focus, magnification and perspective mockups in HyperFrames. Keep interface text readable and do not invent unavailable screens. Add English feature callouts, music and precise click SFX, without voice-over. Export an MP4. |
| 5 | Animated poster | Use $buat-video-motion-grafik to animate the attached poster into a 30-second 16:9 MP4. Preserve its actual photos, offer, dates, prices and contact details. Separate suitable artwork and text into layers, create a hook from the supplied facts, and choreograph entrance, activity and exit with HyperFrames. Keep the original poster clearly recognizable. Add music and synchronized SFX. Do not add unsupported claims or decorative scene labels. |
| 6 | Supplied-image carousel | Use $buat-video-motion-grafik, Gaya Ekstrem, to animate all attached images into a 45-second landscape carousel. Use perspective conveyors, layered depth, dramatic position and scale changes, varied entrances and exits, and occasional full-frame hero images. Preserve image proportions and important subjects. Do not regenerate the original images or cover them with unnecessary text. Add music, SFX and ASMR, without voice-over. Render the final MP4 through HyperFrames. |
| 7 | Generated-image carousel | Use $buat-video-motion-grafik, Gaya Ekstrem, to create a 40-second 16:9 visual story about [topic]. Generate a coherent set of [number] distinct raster images first using the available image-generation tool, inspect them, then animate the real assets in a perspective carousel with continuous depth and scale changes. Keep kinetic text separate from the images. Add music, SFX and ASMR, without voice-over. Use HyperFrames and deliver the MP4 with its project assets. |
| 8 | Slide-deck showcase | Use $buat-video-motion-grafik to turn the attached slide deck into a 60-second landscape showcase. Select representative slides, preserve their content and proportions, and animate them as overlapping perspective planes with changes of depth, focus and screen coverage. Include clean readable moments and varied handoffs between slides. Add brief English benefits based only on the supplied material, music and paper-like SFX. Render with HyperFrames and export an MP4. |
| 9 | Classroom lesson | Use $buat-video-motion-grafik to create a three-minute 16:9 lesson on [topic] for [student age] from the attached teaching notes. Use a question-led opening, layered diagrams, concrete examples and a final recap. Introduce labels progressively and allow enough reading time. Use clear English on-screen text, music and restrained SFX, without voice-over. Follow the educational HyperFrames workflow and deliver one continuous MP4. |
| 10 | CME explainer | Use $buat-video-motion-grafik to create a two-minute landscape CME explainer on [clinical topic] for [audience], using the attached current guideline. Verify clinical statements against the source, distinguish recommendations from illustrative examples, and animate accurate clinical diagrams and a decision pathway. Use readable English text and an appropriate professional pace. Keep source details in accompanying notes. Add restrained music and SFX, without voice-over. Render an MP4 through HyperFrames. |
| 11 | Patient education | Use $buat-video-motion-grafik to create a 90-second 16:9 patient-education video on [topic] using [authoritative source]. Explain the key actions in plain English with recognizable objects, clear demonstrations and a short recap. Verify medical facts and avoid unsupported promises. Use calm layered animation, readable text and gentle SFX. No voice-over. Use HyperFrames for the animated scenes and deliver the final MP4. |
| 12 | Myth-versus-fact video | Use $buat-video-motion-grafik to create a 60-second vertical myth-versus-fact video on [topic] using the supplied evidence. Structure each comparison as a meaningful visual transformation with a clear correction and practical takeaway. Use bold English typography, accurate numbers and varied prop motion. Keep the tone appropriate to the topic. Add music and synchronized SFX, without voice-over. Follow HyperFrames and export a 1080x1920 MP4. |
| 13 | Research summary | Use $buat-video-motion-grafik to turn the attached research paper into a two-minute landscape explainer. Cover the research question, design, key findings, limitations and practical meaning without overstating causation. Animate supplied data, participant flow and concise English statements using HyperFrames. Preserve exact final values and units. Add restrained music and SFX, without voice-over. Deliver the MP4 and source notes. |
| 14 | Animated data story | Use $buat-video-motion-grafik to create a 60-second 16:9 data story from the attached CSV. Identify one clear takeaway and build animated charts, comparisons and counters around it. Keep axes, units, dates and final values accurate; do not invent missing data. Use readable English labels, purposeful transitions and an accessible palette. Add music and subtle SFX, without voice-over. Render the animated composition with HyperFrames and deliver an MP4. |
| 15 | Map and route animation | Use $buat-video-motion-grafik to create a 60-second landscape route story for [places and route]. Use verified geographic positions and licensed map data, animate the route and camera in a clear sequence, and reveal labels only when needed. Distinguish illustrative travel timing from supplied facts. Combine map motion with the attached destination images. Add music and movement-linked SFX, without voice-over. Use HyperFrames and deliver an MP4. |
| 16 | Historical timeline | Use $buat-video-motion-grafik to create a 90-second 16:9 timeline about [topic] from the attached chronology. Verify dates and order, carry one visual anchor across milestones, and vary the composition as the story develops. Use concise English text, layered objects and accurate date reveals. Avoid small scene numbers and decorative chapter labels. Add suitable music and SFX, without voice-over. Render with HyperFrames and export the MP4. |
| 17 | Character storytelling | Use $buat-video-motion-grafik to create a two-minute landscape animated story from [script]. Choose suitable characters from the included 20-character bank and preserve their appearance across shots. Use articulated joints, grounded feet, natural hand-to-object contact, matching view angles and layered parallax environments. Tell the story with English subtitles and character action, without voice-over. Use the HTML/GSAP and HyperFrames workflow, then deliver a fully rendered MP4. |
| 18 | Whiteboard explanation | Use $buat-video-motion-grafik to create a 90-second 16:9 whiteboard explainer on [topic]. Build original vector illustrations progressively with draw-on strokes, grouped reveals and a camera that follows the explanation. Use short English phrases and distinct visual examples instead of a wall of text. Keep timing seekable and deterministic in HyperFrames. Add a light original soundtrack and drawing SFX, without voice-over. Deliver the final MP4. |
| 19 | Paper-cut explainer | Use $buat-video-motion-grafik to create a 60-second landscape paper-cut explainer for [message]. Use coherent paper textures, cut-out props, layered shadows, parallax and purposeful folds or tears. Keep the typography and objects separate so they animate independently. Use concise English text with readable holds, music and tactile paper ASMR, without voice-over. Follow HyperFrames and export the MP4. |
| 20 | Space and science story | Use $buat-video-motion-grafik to create a 120-second 16:9 science explainer about [space topic] from [verified sources]. Combine layered orbital diagrams, planets, moving labels and cinematic camera travel. Use the supplied 2.5D planet engine where appropriate and describe simplified scale accurately. Verify dates and scientific claims. Add space ambience and synchronized SFX, without voice-over. Use HyperFrames for the animated composition and deliver an MP4. |
| 21 | Kinetic typography or lyrics | Use $buat-video-motion-grafik to create a 45-second landscape kinetic-typography video from the attached authorized text and audio. Align phrases to actual audio timing, vary glyph, word and parent-group choreography, and preserve readable endpoints. Use masks, rails, pivots and scale changes with meaningful visual hierarchy. Keep the supplied audio intact. Follow the HyperFrames workflow and deliver the synchronized MP4. |
| 22 | Logo opener | Use $buat-video-motion-grafik to create a ten-second 16:9 logo opener from the attached original logo. Preserve the mark, proportions and brand colors. Build a distinctive reveal through separate shape, mask and typography cues, followed by a clean final logo hold. Do not invent a replacement logo. Add a short original sonic accent, without voice-over. Render the animation using HyperFrames and deliver an MP4. |
| 23 | Event invitation | Use $buat-video-motion-grafik to create a 30-second 1080x1920 invitation for [event] using the supplied date, time, venue, speaker images and registration link. Establish the event's value, reveal the practical details clearly and finish with a readable CTA. Preserve all original portraits and names. Add suitable music and SFX, without voice-over. Use HyperFrames and deliver the final MP4. |
| 24 | Annual recap or montage | Use $buat-video-motion-grafik to edit the attached photos and footage into a 90-second landscape recap of [organization or project]. Build a coherent opening, milestones, achievements and closing from supplied facts. Use Python/FFmpeg for the footage edit and create separate HyperFrames layers only where useful. Apply selected montage assets, licensed music and synchronized SFX. Preserve important subjects and accurate numbers. Deliver one continuous MP4. |
| 25 | Long-form educational video | Use $buat-video-motion-grafik to produce a 15-minute 16:9 explainer from the attached script and sources. Organize chapters and scenes on one continuous timeline, with varied layered artwork and reusable visual anchors. Record natural English narration using Google AI Studio if available; report any provider blocker accurately. Align animation to the final audio, cache scene renders, use HyperFrames for vector scenes, and verify the complete MP4 before delivery. |
| 26 | Edit existing footage | Use $buat-video-motion-grafik to edit the attached footage into a 60-second landscape video. Remove dead air and repetition, preserve the meaning and approved speech, add timed English callouts and selected real Atlas overlays, and finish with music ducking and action-linked SFX. Use Python/FFmpeg directly for editing and compositing. Keep source assets and useful edit metadata. Deliver the final MP4 after full decode and audio checks. |
| 27 | Landscape-to-portrait adaptation | Use $buat-video-motion-grafik to adapt the attached approved landscape video into a 1080x1920 MP4 of the same duration. Recompose text, props and mockups for portrait; use subject-aware footage reframing instead of a blind center crop. Preserve approved audio, wording, important image content and timing. Use the original project renderer for animation revisions and FFmpeg for footage/compositing. Check all motion paths and mobile-safe reading areas before export. |
| 28 | Talking-head kinetic captions | Use $buat-video-motion-grafik to improve the attached talking-head video with meaningful kinetic typography synchronized to the real spoken words. Run the Whisper readiness check before transcription, preserve approved cuts and audio, and replace the old bottom subtitle layer if present. Keep the speaker's face and key gestures readable. Use actual rendered preset implementations and audit their IDs. Composite with Python/FFmpeg and deliver the final vertical MP4. |
| 29 | Human background replacement | Use $buat-video-motion-grafik to replace the human background in the attached video with [provided image or video]. Run the background readiness check and real inference first. Use temporal RVM matting with state resets at cuts, preserve original speech and keep important held objects with appropriate masks. Inspect hair, hands and edge stability on a proof before compositing the full clip with Python/FFmpeg. Deliver an MP4 with the original duration. |
| 30 | Arabic lecture with Malay subtitles | Use $buat-video-motion-grafik to edit the attached Arabic lecture into a 9:16 video while preserving its full duration and original speech. Verify Whisper readiness with the production multilingual model, prepare an accurate Arabic transcript and complete Bahasa Melayu Malaysia translation, and check religious quotations against authoritative sources. Keep the supplied title throughout, Arabic above Malay, and meaning-aligned gold highlights on Malay words. Check RTL shaping and export the final MP4 with Python/FFmpeg. |


## Get started

Use the current repository source for Creator FX 80, or download the earlier complete v1.1.0 distribution from **[Releases](https://github.com/akramania/buat-video-motion-grafik/releases)**. Keep `SKILL.md`, `agents/`, `scripts/`, `references/` and `assets/` together. Follow your agent's skill installation instructions, then request a video with `$buat-video-motion-grafik`.

For example:

> Use $buat-video-motion-grafik to create a 30-second product explainer with kinetic typography, a layered UI demo and animated charts. Use a clean teal-and-navy palette, a 16:9 layout and readable mobile-safe text.

Restore archived assets when needed:

```bash
python3 scripts/materialize_svg_assets.py
python3 scripts/prepare_vlog_assets.py --verify
python3 assets/fonts_creative_100/prepare_fonts.py --all
```

Render a preset:

```bash
python3 scripts/atlas_preset.py init K16 --output typography.json
python3 scripts/atlas_preset.py check typography.json
python3 scripts/atlas_preset.py render typography.json --output typography.mp4
python3 scripts/atlas_preset.py verify typography.json --video typography.mp4 --report typography-qa.json
```

Render a modular vector component:

```bash
node assets/motion_array/render_motion.mjs --id MA0501 --width 1920 --height 1080 --fps 30 --output component.mp4
```

## Runtime and output

The preset renderer needs **Python 3.10+, Pillow, NumPy and FFmpeg**. The modular vector renderer needs **Node.js, sharp and FFmpeg**. The npm distribution delivers the skill and its assets; it does not install these rendering dependencies automatically.

Video workflows can produce a continuous MP4 up to **30 minutes** when the runtime and project assets support the brief. Individual preset previews and showcase reels demonstrate selected mechanisms. Portrait compositions, audio alignment and complex scripts require project-specific layout and quality checks. Voice-over providers, accounts and music subscriptions are separate from the toolkit.

## Original implementation and licenses

This distribution contains original procedural renderers and adaptations of motion techniques, together with provenance notes. It includes no commercial Envato or Motion Array template files. Preserve the included font, geographic data and asset license notices. The repository currently declares no blanket open-source license for all toolkit code; consult the author for broader redistribution terms.
