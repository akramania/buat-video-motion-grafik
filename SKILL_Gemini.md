---
name: buat-video-motion-grafik-gemini
description: Cipta MP4 atau prompt motion grafik dalam Gemini Task/Spark. Semak cache dan storan VM dahulu, kemudian muat turun hanya pek yang diperlukan dan hilang atau tidak sah. Gunakan 922 preset Atlas termasuk Creator FX 80 melalui runtime Python asal terkunci; Python/FFmpeg untuk suntingan video dan HTML/GSAP + HyperFrames untuk animasi vektor/kartun. Sokong Whisper, matting RVM, 2000 komponen MA, 1500 SVG, 100 fon, 600 aset montaj dan bank V3 20 watak. Render offline selepas keperluan projek tersedia.
---

# Buat Video Motion Grafik — Gemini

Ikut arahan pengguna terkini dan bahasa Melayu Malaysia. Hasilkan MP4 sebenar apabila diminta video siap. Jika diminta prompt, tulis prompt lengkap dalam satu code block tanpa memulakan render. Kekalkan kandungan/audio/rujukan yang telah dipersetujui. Gunakan sumber dan fail sebenar; jangan dakwa telah diuji dalam akaun Gemini jika hanya diuji di runtime lain.

## 1. Semak cache dan storan VM dahulu

Baca `references/selective-cache.md` serta manifest keluaran terkini. Resolusi root sebenar daripada persekitaran Gemini; jangan andaikan `/root/.codex` atau storan sementara kekal. Gunakan direktori projek berasingan daripada cache toolkit.

1. Kenal pasti fungsi yang diperlukan: preset, kartun HTML, watak, SVG, fon tambahan, montaj, Whisper atau matting. Semak fail pada root skill, cache pakej dan storan VM yang diketahui; jangan mengimbas semua fail pengguna tanpa sebab.
2. Jalankan `scripts/gemini_cache.py plan` dengan manifest dan `--need` untuk kategori yang diperlukan sahaja. Cache sah memerlukan saiz dan SHA-256 fail sepadan, bukan kewujudan folder kosong.
3. Jika fail diekstrak sah tersedia, guna semula. Jika ZIP sah tersedia, ekstrak dari storan tempatan. Muat turun hanya pek bertanda `download-required` melalui saluran Drive yang benar-benar boleh memindahkan bait fail.
4. Jalankan `install` ke root keluaran berasingan. Jangan menimpa fail suntingan pengguna; pemasang menolak konflik. Kemudian `verify` untuk pek terpilih dan preflight runtime khusus. Status pek tersedia tidak membuktikan FFmpeg/model/Chrome sudah berfungsi.
5. Render offline selepas SEMUA keperluan projek terpilih tersedia. Jika perlu aset baharu, kembali ke persediaan dan ambil pek berkaitan sahaja. Jangan wajibkan SEMUA pek katalog pada setiap projek atau pemasangan pertama.
6. Kekalkan cache, ZIP sah, model, dependency serta receipt versi selepas membersihkan frame render. Semak semula selepas sesi/VM bertukar. Jika offline dan fail perlu tiada, laporkan fail tepat yang hilang; jangan mencuba muat turun berulang atau mendakwa berjaya.

Folder keluaran: https://drive.google.com/drive/folders/1QF3fxMu5ruysNbw92Jii5aU3xyb-tiJF
Rujuk `references/selective-cache.md` untuk pautan manifest dan pek terkini. Pakej lama 22 Oktober bukan lalai bagi runtime Atlas terkunci ini. Jangan mencampur renderer lama dengan kontrak baharu.

## 2. Pilih backend mengikut tugas

- Sunting video sedia ada terus dengan Python/FFmpeg: cut, reframe, subtitle, kinetic title, komposit, muzik, SFX dan eksport.
- Animasi vektor/kartun: HTML/GSAP + HyperFrames dengan SVG berlapis, pivot, rig/IK, kamera/parallax dan timeline seekable. HTML ialah struktur/render; GSAP mengurus animasi.
- Projek campuran: render lapisan yang diperlukan, kemudian komposit melalui Python/FFmpeg. Jangan mewajibkan HTML/GSAP pada setiap video.
- Baca `references/html-hyperframes-production.md` dan `references/hyperframes-motion-bank.md` hanya untuk laluan HTML. Semak dependency/cache dahulu; sediakan Node/Chrome yang serasi jika diperlukan. Gunakan `paused:true`, `window.__timelines`, masa eksplisit dan gate fon/aset, tiada ticker bebas.

## 3. Preset Atlas mesti menggunakan kod asal

Baca `references/atlas-python-runtime.md`, `references/creator-fx-80.md` dan metadata ID yang dipilih. Wajib gunakan `scripts/atlas_preset.py` atau API `AtlasPreset`. `gemini_atlas.py` ialah alias CLI yang sama, bukan renderer berasingan. Jangan membina semula efek berdasarkan nama/preview atau menukar easing/timing dalaman tanpa varian yang diuji.

```bash
python scripts/atlas_preset.py list --search scroll
python scripts/atlas_preset.py describe CFX15
python scripts/atlas_preset.py init CFX15 --output /path/project/job.json
python scripts/atlas_preset.py check /path/project/job.json
python scripts/atlas_preset.py render /path/project/job.json --output /path/project/layer.mp4
python scripts/atlas_preset.py verify /path/project/job.json --video /path/project/layer.mp4 --report /path/project/qa.json
```

Untuk konfigurasi katalog lama, gunakan `import-config old.json --output job.json`. Edit hanya parameter yang disokong. Cue dalam job menggunakan saat output sebenar; jangan menormalisasi dua kali. Wrapper mengesahkan registry, versi kod/aset/fon, baseline dan cache. Jangan membina semula lock untuk memintas kegagalan.

922 entri = 137 asal + 185 demo MS/PL/PV/AD + 120 EV + 400 PX + 80 CFX. MA ialah koleksi berasingan. ID preset bukan teks video; panggil fungsi sebenar bagi setiap frame. Default produksi tanpa label katalog.

Untuk footprint pada footage, pilih mode footage dan bekalkan frame sebenar, alpha subjek, backdrop, tracking atau sejarah frame sebagaimana kontrak ID. CFX15 default footage penuh; kemunculan panel ikut gerakan tangan memerlukan cue/anchor sebenar, bukan andaian tracking automatik. CFX12/40 memerlukan remap source time sebenar; CFX20 memerlukan sejarah echo. Jangan ganti input hilang dengan demo sintetik.

Native canvas 1280×720. Letakkan layer 16:9 secara berkadar atau bina varian portrait yang diuji; jangan meregang atau memotong teks untuk 9:16. Render senyap tidak membawa audio asal: campur audio dalam editor. Baseline bukan jaminan semua teks/layout atau semua preview luaran tepat.

## 4. Gaya, tipografi dan koreografi

Gunakan palet cerah lembut bagi projek baharu tanpa rujukan lain: cream #F8F3E8, panel #E8E0CF, teks #263645, aksen #447891. Jika diminta sama seperti Atlas, kekalkan palet/default Atlas. Tetapkan warna melalui params yang disokong; jangan mengubah fail renderer terpinkan atau fon global secara senyap.

Bezakan subtitle penuh daripada title kinetik. Jika diminta per perkataan, animasikan kemunculan setiap perkataan sambil mengekalkan perkataan terdahulu hingga ayat lengkap apabila sesuai. Variasikan mekanisme mengikut mesej dan ruang bacaan. Gunakan satu aksi utama; jadualkan entrance, hold, exit, handoff dan SFX secara eksplisit.

Jangan wajibkan semua 80 CFX atau bilangan preset tertentu tanpa brief. Untuk projek kompleks, baca `references/director-critic-qa.md`: brief, persistent hero, tiga signature moments, storyboard, timing audio, proof 3–5 saat, critic ledger dan QA sebelum master. Prinsip kreatif tidak mengatasi permintaan pengguna.

## 5. Aset, fon, model dan cache pilihan

| Keperluan | Pek/kandungan |
|---|---|
| Atlas/CFX | core + presets |
| Vektor/kartun HTML | core; sediakan dependency HTML hanya apabila perlu |
| Watak V3 | core + characters |
| SVG/MA | core + svg atau motion_array |
| Fon tambahan | fonts; gunakan fail TTF dan lesen sebenar |
| Montaj/LUT/SFX | core + hanya vlog_payload yang memuatkan aset terpilih |
| Preview katalog | previews pilihan; tidak wajib untuk render |

Semak indeks untuk menentukan pek aset. Payload VL perlu dipulihkan hanya bagi aset/pek terpilih dengan utiliti yang tersedia; jangan label koleksi penuh tersedia jika sebahagian sahaja dipasang. Model besar tidak dibundel dalam ZIP kod. Semak cache model dan inferens dahulu. Untuk Whisper baca `references/media-tools.md`; gunakan model projek yang disahkan dan jangan turun taraf secara senyap. Untuk matting manusia baca `references/video-background-replacement.md`; RVM temporal, reset pada cut, proof alpha/tepi dan jaga audio. Semak offline dahulu; jika fail perlu hilang, sediakan hanya dependency/model berkaitan semasa online.

## 6. Prompt dan komposisi

Prompt mesti mengandungi objektif, orientasi/resolusi/durasi, scene/timing, teks, aset, preset ID sah, palet, cue audio, backend dan QA. Masukkan aturan cache-first dan muat turun terpilih; jangan menyatakan semua fail sudah dipasang tanpa bukti. Jika indeks tidak tersedia, arahkan semakan ID sebelum render dan jangan cipta ID.

Untuk beberapa preset dalam scene, sediakan setiap job terpinkan, start/end dan rect. Gunakan API `AtlasPreset.frame(t_local)` atau komposit hasil layer yang telah dirender. Gunakan masa `i/fps`, nisbah berkadar, alpha sah dan manifest ID sebenar. `scripts/gemini_compose.py` menerima `layers[].job` sebagai path job terpinkan; ia kompositor native, bukan pengganti penyedia footage/tracking.

## 8. Watak, 2.5D, kamera dan audio

Gunakan bank V3 20 watak sopan tempatan; kekalkan ID, rupa, pakaian dan `height_cm` supaya nisbah antara kanak-kanak/dewasa logik. Baca `references/character-bank-20.md`, `references/local-vector-animation.md` dan `references/vector-cinematic-motion.md`. Pastikan hierarki sendi bersambung, garis aksi, pemindahan berat, tangan menggenggam props, kaki berpijak, overlap dan easing lancar. Render tiga styleframe dan petikan aksi 3–5s secara dalaman sebelum master. Jangan menambah gate kelulusan jika pengguna sudah meminta penghasilan penuh.

Gunakan orientasi `front`, `back`, `side_right`, `side_left`, `three_quarter_right`, `three_quarter_left`; `side` dan `three_quarter` ialah alias kanan. Artwork belakang tidak mempunyai ciri wajah/butang hadapan; sudut kiri memantulkan tubuh, kepala dan props. Asingkan tulisan/logo dan perincian pakaian anatomi yang tidak boleh dipantulkan. Jangan paksa `--view` pada aksi turn yang perlu bertukar sudut.

```bash
python scripts/character_bank.py list --kind motions
python scripts/character_bank.py render --character P04 --motion walk_across --view side_left --width 720 --height 1200 --fps 30 --output /path/project/mira_walk_left.mp4
python scripts/character_bank.py render --character L05 --pose stand_back --output /path/project/amir_back.png
python scripts/vector_character_camera.py --demo --duration 4 --fps 30 --width 1280 --height 720 --output /path/project/camera.mp4
```

`walk_side_left`/`walk_side_right` ialah loop berjalan setempat; `walk_across` dengan view sisi menghasilkan perjalanan merentasi skrin. Gunakan satu viewBox sepanjang shot, skala `height_cm` sebenar dan `t=frame/fps`. Panggil `poseState`/`sampleMotion` diikuti `rigSvg` bagi komposisi tersendiri. Gerakan baharu meliputi turn belakang/hadapan dan kiri/kanan, mengeluh, mengelap air mata, makan/minum, doa, perbualan telefon dan menunggang prop motosikal. Turn ialah pertukaran artwork 2D dengan unjuran mendatar, bukan morph 360°/3D; mulut demo tidak menyediakan lip-sync audio automatik. Periksa kontak, genggaman, kaki dan lipatan pakaian.

Baca `references/vector-camera-engine.md` untuk kamera/IK Python. Demo Python mempunyai tiga role contoh `amir`, `mak`, `abah`; ia bukan pemuat automatik bank 20 ID L/P. Gunakan renderer SVG untuk bank 20, kemudian komposit ke scene. Contoh 16-scene asal ialah mod pilihan yang memerlukan path projek, fon, RMS dan audio eksplisit; jangan menganggap fail projek lama tersedia atau menyalin kandungan khusus itu ke semua video.

Bezakan world space dan screen space; bina foreground/midground/background untuk parallax, kamera dolly/zoom/pan dan fokus subjek. Gunakan `scripts/advanced_planet_engine.py` untuk planet 2.5D serta `references/advanced-planet-rendering.md` jika relevan. Jangan mendakwa 2.5D ialah mesh/rig 3D penuh.

Voice-over BM Malaysia: utamakan fail audio yang dibekalkan atau diluluskan. Jika perlu suara neural baharu, buat dalam fasa online melalui akses yang sah, kemudian masukkan WAV/MP3 ke projek sebelum render offline. Jangan janji TTS cloud boleh dipanggil dari sandbox offline. Jika pengguna melarang model generatif, ikut larangan itu. Sintesis muzik/SFX melalui kod jika diminta, tanpa sampel/model. Teks sari kata penuh mesti dipisahkan daripada caption kinetik ringkas.

Jadikan audio akhir jam utama. Ukur durasi sebenar, sediakan cue onset/offset perkataan/frasa dan semak subtitle awal, pertengahan serta akhir. Jangan guna anggaran perkataan semata-mata sebagai bukti sync. Bar waveform/audiogram hendaklah berpunca daripada RMS/envelope audio sebenar jika disebut sebagai bar suara.

## 9. Produksi dan QA wajib

1. Tetapkan orientasi, resolusi, FPS, tempoh, nada, bahasa dan kandungan daripada brief; jika tiada, pilih 1920×1080/30 fps dengan palet krim dan durasi yang sesuai dengan mesej. Had setiap scene mengikut arahan pengguna, bukan sentiasa 3s bagi semua projek.
2. Bina manifest scene: start/end, teks, preset ID sah, ID aset, font path, palet, data, cue audio dan mekanisme gerak. Kira ID unik yang benar-benar digunakan; jangan kira pengulangan sebagai preset baharu.
3. Render petikan beberapa mekanisme, font dan palet; buka frame dan tonton petikan. Baiki ejaan, clipping, alpha, kontras, gerakan kaku serta perkadaran.
4. Render scene menggunakan masa `i/fps`, seed tetap dan aset tempatan. Jangan menahan semua frame video panjang dalam RAM; stream ke FFmpeg atau render segmen dengan saiz/FPS/codec seragam. Simpan checkpoint untuk projek panjang.
5. Gabungkan scene dan audio. Periksa potongan, tiada flash bingkai hitam, subtitle penuh, waveform sebenar, SFX dan penutup. Jangan anggap menukar metadata kepada 60 fps menghasilkan 60 frame animasi unik.
6. Jalankan ffprobe untuk resolusi/FPS/durasi/frame count dan nyahkod seluruh MP4. Ekstrak semula frame daripada fail akhir, bukan hanya frame sebelum encode. Semak awal/akhir setiap scene, puncak animasi, semua teks dan audio pada kelajuan biasa.
7. Serahkan MP4 sebenar serta kod/projek apabila diminta. Nyatakan batas yang benar-benar ditemui. Jangan mendakwa sudah diuji pada Gemini Spark jika hanya diuji pada runtime lain; bezakan ujian portabiliti offline daripada ujian dalam akaun Gemini pengguna.

```bash
ffprobe -v error -show_streams -show_format -of json /path/project/final.mp4
ffmpeg -v error -i /path/project/final.mp4 -f null -
```

Untuk projek kompleks/hingga 30 minit baca `references/master-instruction-v6.md`, `references/advanced-motion-graphics.md`, `references/motion-patterns-envato.md` dan `references/local-video-pipeline.md`. Gunakan isi teknikal yang berkaitan; jangan import tool, path, storan, aturan penerbitan atau andaian akses ChatGPT ke Gemini. Kekalkan semua kerja render sepenuhnya tempatan selepas pemasangan.
