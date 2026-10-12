![Motion Atlas Studio](https://github.com/user-attachments/assets/d2c103cc-fcf8-4756-bbc7-5f6525ddf103)

# Motion Atlas Studio

### 5,042 creative entries. One adaptable video production toolkit.

Build motion graphics, animated explainers, product promos and editorial montages with an agent skill for **ChatGPT Work and Codex**, supported by reusable Python and Node renderers, original vector artwork, typography systems and production references.

**Explore the [Motion Atlas](https://motion-preset-atlas.akramania.chatgpt.site).**

## The collection

| Collection | Included | Creative possibilities |
|---|---:|---|
| Animation presets | **842** | Kinetic typography, UI, product reveals, maps, charts, counters, paper effects and transitions |
| Modular motion components | **2,000** | Shapes, arrows, HUD and data layers, transitions, particles and light |
| SVG assets | **1,500** | Explainer illustrations, icons, learning diagrams and promotional compositions |
| Vlog and montage assets | **600** | 100 LUTs, 100 transitions, 100 animated overlays, 100 vlog graphics, 100 montage graphics and 100 SFX |
| Curated font families | **100** | Display, editorial and Arabic typography, with original font license files |
| **Total creative entries** | **5,042** | Separate catalog entries across the five collections |

The **842 presets** comprise **137 core presets, 185 guide adaptations, 120 preview adaptations and 400 premium recipes**. The **2,000 modular components** comprise **100 design families with 20 structural variations each**. These categories remain distinct; font families are included in the total. Counts describe creative entries, not 5,042 standalone video templates.

## Design with motion

- Shape the story with layered compositions and separate entrance, activity and exit cues.
- Give words rhythm with measured kinetic typography, highlights, counters and captions.
- Explain products through dashboards, notifications, app screens and perspective mockups.
- Turn maps and example data into route animations, chart builds and geographic metrics.
- Finish montages with color treatments, moving overlays, transitions and sound accents.
- Follow a production workflow for scripting, audio timing, rendering and visual quality checks.

## Get started

Download the complete distribution from **[Releases](https://github.com/akramania/buat-video-motion-grafik/releases)**. Keep `SKILL.md`, `agents/`, `scripts/`, `references/` and `assets/` together. Follow your agent's skill installation instructions, then request a video with `$buat-video-motion-grafik`.

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
python3 assets/motion_presets/render.py --preset K16 --duration 6 --fps 30 --clean --output typography.mp4
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
