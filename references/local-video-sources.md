# Audit sumber integrasi video setempat

Semakan: 19 Oktober 2026. Baca SKILL.md dan bukti lesen sebelum memilih teknik.
Jangan anggap senarai cadangan pengguna membuktikan lesen, dependency atau render.
Kod utiliti integrasi ditulis asal; repo berikut ialah sumber teknik dan rujukan,
bukan dependency yang dipasang atau kod yang disalin seluruhnya. Simpan notis lesen
asal jika kemudian menyalin implementasi, teks atau aset yang substansial; bagi
Apache-2.0, kekalkan NOTICE jika wujud serta tandakan pengubahsuaian.

## Pemilihan

| # | Sumber SKILL.md | Keputusan dan teknik yang diterapkan |
| --- | --- | --- |
| 1 | [SVG Skill](https://github.com/linyaosky/svg-skill/blob/2103b92cb47f588a97a6c38aa6c40571fadbd4f8/SKILL.md) | Teras: viewBox, ID/defs stabil, SVG kendiri, validasi XML dan raster sebenar. MIT disahkan. |
| 2 | [SVG Diagram](https://github.com/bybit-exchange/svg-diagram/blob/c30c9e3bc9a70f2b77b60c7ea27157de3a88d81a/SKILL.md) | Teras: ukuran teks, baseline, connector ke sempadan node, urutan layer dan reveal. MIT disahkan. |
| 3 | [SVG Creator](https://github.com/upbrew-tech/svg-creator-skill/blob/1eb83d602a992b69a1771c4e0116a9f7de6ffaa2/SKILL.md) | Teras: ilustrasi berlapis, anggota bersambung, render–inspect–fix. Apache-2.0 disahkan. |
| 4 | [SVG Character Animator](https://github.com/molauu/svg-character-animator/blob/5ee1e7845caefe2c9ab51c64a2aa6f386e72ef5b/SKILL.md) | Terapkan transform/rig/topologi morph. Ganti eksport masa nyata dan CDN dengan masa frame eksplisit. MIT disahkan. |
| 5 | [Text to Lottie](https://github.com/diffusionstudio/lottie/blob/3c72912fad543897f90045ed4d355813837927fc/skills/text-to-lottie/SKILL.md) | Pilihan: frame range, group, font/aset setempat dan seek. Memerlukan pemain Skottie/WASM sebenar; bukan backend asas. MIT disahkan. |
| 6 | [Animate](https://github.com/cth9191/animate/blob/main/plugins/animate/skills/animate/SKILL.md) | Teras teknik: Canvas deterministik, seed, spring analitik, beat dan review per shot. MIT disahkan. Jangan import approval gate atau API narasi. |
| 7 | [Manim Animation](https://github.com/awesome-skills/manim-skill/blob/main/SKILL.md) | Pilihan: Scene/Transform/ValueTracker, draft → final, label Text. README mengisytiharkan MIT; fail lesen berasingan tidak berjaya disahkan. Jangan vendor kod/teksnya. |
| 8 | [Manim Video](https://huggingface.co/spaces/bodaya/hermes-agent/blob/main/skills/creative/manim-video/SKILL.md) | Rujukan pilihan: scene bebas, palette/cue, render bersegmen. Lesen perubahan mirror belum disahkan; jangan salin kod/teks. LaTeX hanya untuk formula. |
| 9 | [p5.js Production](https://github.com/NousResearch/hermes-agent/blob/main/skills/creative/p5js/SKILL.md) | Terapkan noLoop, readiness, seed/noise, cache dan capture frame tepat. MIT Hermes disahkan; semak lesen library p5 berasingan. Utamakan sumber primer ini berbanding mirror. |
| 10 | [ASCII Video](https://huggingface.co/spaces/bodaya/hermes-agent/blob/main/skills/creative/ascii-video/SKILL.md) | Efek khusus sahaja; terapkan cache glyph, vectorization dan frame streaming. Lesen mirror belum disahkan. TTS bukan dependency asas. |
| 11 | [Media Depth](https://github.com/damionrashford/media-os/blob/5014c1e8b23fd3e18d49926d9aa147d15a3aa08e/skills/media-depth/SKILL.md) | Pilihan: depth/overscan/occlusion QA; layer manual lalai. Repo MIT, tetapi lesen model berasingan; betulkan dakwaan semua checkpoint Apache. |
| 12 | [FFmpeg Video Filter](https://github.com/damionrashford/media-os/blob/5014c1e8b23fd3e18d49926d9aa147d15a3aa08e/skills/ffmpeg-video-filter/SKILL.md) | Teras: probe, filtergraph, dimensi genap, SAR, font, mapping stream. MIT disahkan. |
| 13 | [FFmpeg Compose Mask](https://github.com/damionrashford/media-os/blob/5014c1e8b23fd3e18d49926d9aa147d15a3aa08e/skills/ffmpeg-compose-mask/SKILL.md) | Teras: timestamp, alpha/matte, compositing. MIT disahkan; betulkan polarity maskedmerge dan alpha codec. |
| 14 | [FFmpeg Frames Images](https://github.com/damionrashford/media-os/blob/5014c1e8b23fd3e18d49926d9aa147d15a3aa08e/skills/ffmpeg-frames-images/SKILL.md) | Teras: input framerate, sequence bernombor, tiada gap, contact sheet dan FFmpeg akhir. MIT disahkan. |
| 15 | [Bang Motion](https://github.com/bangtutorial/bang-motion/blob/c1aa65e921c970d858705fcb4a53a8294d1a4131/SKILL.md) | Terapkan kamera bermakna, timeline seek, watak dan penegasan kata secara native. Repo MIT; GSAP mempunyai lesen sendiri dan tidak diwajibkan. |
| 16 | [Three.js Parallax](https://github.com/JudyZZ/threejs-parallax-skill/blob/2e9e083cba725a734791710ccc043116572f0be7/threejs-parallax/SKILL.md) | Terapkan layer/aspect/overscan. Asal interaktif mouse/scroll perlu diganti camera(t). Repo MIT; Three.js/WebGL setempat pilihan sahaja. |
| 17 | [Remotion Best Practices](https://github.com/remotion-dev/skills/blob/1441a11e95db35443bd76bb318386c0d3ca00053/skills/remotion-best-practices/SKILL.md) | Ketepikan daripada asas percuma; lesen repo tidak ditemui ketika semakan dan runtime mempunyai syarat berbayar mengikut organisasi. Jangan vendor teks. |

Pautan p5 mirror yang diberi pengguna:
https://huggingface.co/spaces/bodaya/hermes-agent/blob/main/skills/creative/p5js/SKILL.md
tidak berjaya diambil ketika semakan; ia tidak dikira backend tambahan. HF Manim dan
ASCII menunjukkan commit ringkas `934eaed`; hash penuh tidak diperoleh. Animate,
Manim dan Hermes di atas menggunakan branch yang boleh berubah; semak versi sebenar
jika hendak vendor kemudian. Jangan mereka hash yang tidak diperoleh.

## Pembetulan penting berbanding sumber

- [FFmpeg maskedmerge rasmi](https://ffmpeg.org/ffmpeg-filters.html#maskedmerge):
  mask 0 memilih input pertama, maksimum memilih input kedua. H.264/libx264rgb
  bukan format alpha; gunakan PNG RGBA/ProRes 4444 sebelum flatten master.
- [Depth Anything V2 rasmi](https://github.com/DepthAnything/Depth-Anything-V2#license):
  Small Apache-2.0; Base/Large/Giant CC-BY-NC-4.0. Semak model card tepat termasuk
  varian metric; jangan menganggap semua fail yang boleh dimuat turun sesuai komersial.
- [GSAP Standard License](https://gsap.com/community/standard-license/): bezakan
  lesen repo Bang Motion daripada library GSAP. Integrasi native tidak mewajibkan GSAP.
- [Lesen/harga Remotion](https://www.remotion.dev/docs/license/pricing): percuma
  bagi individu dan syarikat sehingga tiga orang; kategori empat atau lebih
  mungkin memerlukan lesen berbayar. Ia tidak sesuai sebagai syarat asas pengguna.
- [FFmpeg seeking](https://ffmpeg.org/ffmpeg.html#Main-options): input `-ss` ketika
  transcode boleh menggunakan accurate seeking; jangan anggap sentiasa keyframe sahaja.
  Mod yadif 0 ialah send_frame; mod 1 send_field. Animasi progresif tidak memerlukan
  deinterlace. Semak dokumentasi versi FFmpeg yang tersedia.

## Status pelaksanaan

`local_mp4.py` ialah bridge asal untuk PNG → H.264/AAC dan QA nyahkod penuh.
`render_native_canvas.cjs` ialah adapter Canvas tanpa browser menggunakan
`@napi-rs/canvas`; contoh `assets/local_video/canvas_scene.cjs` ialah artwork asal.
Semakan 19 Oktober 2026: laluan PNG lulus ujian frame/audio serta decode; Canvas
native lulus 12 frame, 320×180, 1 saat, SAR 1:1, decode penuh dan seek deterministik.
`render_canvas.cjs` ialah adapter projek tempatan dengan Playwright; ia memerlukan
Chromium yang boleh dilancarkan, yang tidak tersedia dalam persekitaran semakan itu.
Keberhasilan browser belum diuji. Kejayaan sequence PNG/Canvas native tidak membuktikan laluan
browser/Manim/Skottie/depth sudah berfungsi. Gunakan preflight dan petikan sebenar
sebelum mendakwa backend diuji dalam sesi baharu. Semua 842 preset, 2,000 komponen,
1,500 SVG dan aset sedia ada kekal; teknik repo ini tidak dikira ID preset tambahan.

Rujuk [aliran setempat](local-video-pipeline.md) dan [rig vektor](local-vector-animation.md)
untuk implementasi. Jangan mengimport syarat kelulusan, had tempoh pendek, larangan
aset pengguna, penyedia TTS berbayar, path mesin atau UI khusus platform asal.
