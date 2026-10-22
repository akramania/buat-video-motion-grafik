---
name: buat-video-motion-grafik-gemini
description: Bina video motion grafik sebenar atau tulis prompt motion graphic yang menerapkan preset dan aset Atlas untuk Gemini Task/Spark. Sokong HTML/SVG + GSAP + HyperFrames untuk motion graphics 2D/2.5D ala After Effects, Whisper dan remove-background setempat. Pasang SEMUA fail sokongan dari Google Drive ke folder skill terlebih dahulu, kemudian render offline menggunakan 842 preset Atlas, 2000 komponen MA, 1500 SVG, 100 fon, 600 aset montaj serta bank V3 20 watak, 42 pose, 34 gerakan, enam sudut dan kamera vektor Python. Gunakan apabila diminta video, prompt animasi, kinetic typography, peta, graph, radar, LUT, transition atau Motion Atlas. Jadikan palet cerah lembut sebagai lalai.
---

# Buat Video Motion Grafik untuk Gemini Task/Spark

Ikut arahan pengguna terkini. Gunakan bahasa Melayu Malaysia untuk komunikasi kecuali diminta lain. Hasilkan MP4 sebenar yang boleh dimainkan apabila diminta video siap. Kekalkan audio/karakter/rujukan yang sudah dipersetujui ketika membuat revisi. Jangan berhenti setakat kod atau storyboard apabila enjin render tersedia.

## HTML/HyperFrames: setup dahulu, render offline

Untuk aliran HTML 2D/2.5D ala After Effects, baca [produksi HyperFrames](references/html-hyperframes-production.md), [bank gerakan/port preset JS](references/hyperframes-motion-bank.md) dan [Whisper serta remove-background](references/media-tools.md). Jalankan `node scripts/setup_hyperframes.mjs --help` dan preflight. Sediakan Node.js 22+, FFmpeg, HyperFrames, GSAP dengan DrawSVG/MorphSVG/MotionPath/SplitText, Chrome Headless, fon/aset serta model setempat dalam fasa SETUP. Pasang runtime yang serasi OS/CPU dan kekalkan cache/dependency sebenar melalui saluran kekal; jangan anggap pakej Python/Chrome ChatGPT sudah ada pada Gemini.

Salin `assets/hyperframes/` ke projek dan gunakan CLI versi terkunci. Bina SVG berlapis dengan ID/group/pivot, rig parent–child/IK, kamera/parallax, compositing dan cue audio. Animasikan Arab sebagai perkataan/baris, bukan huruf. Gunakan timeline terhingga, `paused:true`, `window.__timelines` yang sepadan dengan composition ID dan gate fon/aset yang benar-benar ditunggu runtime. Semua animasi mesti boleh di-seek secara tepat tanpa jam/ticker bebas. PixiJS/Three.js ditambah hanya apabila perlu dan diuji pada sandbox sasaran.

Release **HTML/HyperFrames — 22 Oktober 2026** menggunakan 12 pek Drive dalam seksyen 1. Pek core terkini membawa projek HTML/SVG, font/aset demo, empat plugin GSAP, adapter JavaScript, lockfile npm, skrip setup/render/QA serta pembantu Whisper/rembg dan requirements. Ia mengekalkan semua pek Atlas dan bank V3. Sediakan node_modules, Chrome dan model yang serasi OS/CPU secara berasingan semasa setup; pek kod bukan binari semua platform. Jalankan preflight HTML dan model selepas pemasangan, kerana status Atlas lama tidak mengesahkan backend baharu. Jangan mendakwa pemasangan dalam akaun Gemini telah diuji tanpa menjalankannya di sana. Kekalkan fail custom dan gunakan aliran upgrade di bawah.

Render petikan dan contoh projek sebenar sebelum master panjang; semak artwork, rig, teks Arab–Melayu, kelancaran, audio sync, transisi dan fail MP4 akhir. Semua aset/preset Python kekal sah. Adapter JS terpilih mesti merekod ID asal dan batasnya; preset lain boleh dirender Python sebagai layer tanpa melabelnya sebagai port JS.

## 0. Bezakan permintaan prompt daripada penghasilan video

Apabila pengguna berkata “tulis prompt”, “cadangkan prompt”, “prompt motion graphic”, “buatkan prompt untuk video” atau maksud seumpamanya, TERUS tulis prompt produksi siap salin dalam satu code block. Jangan mulakan render, jangan memerlukan fail MP4 dan jangan meminta “Mula” untuk menulis prompt. Jika pengguna meminta prompt dan video sekali, lengkapkan kedua-duanya mengikut skop itu.

Semasa menulis prompt, terapkan preset dan aset toolkit secara automatik apabila sesuai, walaupun pengguna tidak menyebut Atlas. Jangan berhenti pada arahan umum “guna animasi cantik” atau “gunakan preset Atlas”. Pilih mekanisme yang menyampaikan isi: reveal teks untuk hook, graph/counter untuk data sebenar, peta/route untuk lokasi, radar untuk perbandingan paksi yang sah, SVG/rig untuk objek/karakter, transition dan SFX pada event yang relevan. Jangan memaksa LUT pada vektor pastel atau graph/peta/radar pada cerita yang tidak memerlukannya.

Sediakan prompt berdasarkan brief dan rujukan terbaru pengguna, dengan:

- Tajuk, objektif, audiens, orientasi, resolusi, FPS, tempoh dan bahasa.
- Palet cerah lembut dengan HEX sebenar; latar krim menjadi titik mula jika tiada arahan lain.
- Scene/beat, masa mula–akhir, teks on-screen ringkas, visual utama, aksi, kamera dan ruang bacaan. Jika skrip belum ada, olah kandungan mengikut tujuan; label angka contoh sebagai data demo.
- Preset ID yang SAH beserta nama/mekanisme, peranan, onset/offset dan kombinasi layer. Baca registry tempatan semasa tersedia; jangan reka ID daripada nombor yang kelihatan munasabah.
- Aset SVG/MA/VL/watak dan fon sebenar: ID/path yang telah disahkan, cara load/compose serta animasinya. Jika indeks tidak tersedia dalam konteks penulisan prompt, nyatakan kriteria pemilihan dan arahkan pelaksana menyelesaikan ID/path daripada indeks tempatan SEBELUM render; jangan menyamar ID andaian sebagai aset yang sudah disemak.
- Kontrak offline: SEMUA fail sudah dipasang dalam skill; resolve `SKILL_ROOT` sebenar, guna aset tempatan, tiada CDN/Drive/API ketika render.
- Kontrak animasi: panggil enjin preset setiap frame pada `t=i/fps`, `labels=False`; ID/kod bukan kandungan video. Gabungkan hasil preset ke layer/scene, jangan mengulang screenshot statik.
- VO, subtitle penuh, caption kinetik, waveform, SFX dan muzik jika diminta; penjajaran berpunca daripada audio akhir. Ikut arahan tanpa VO/model generatif jika ada.
- QA petikan sebenar, semakan pergerakan/teks/alpha, metadata, nyahkod MP4 penuh dan fail yang perlu diserahkan.

Gunakan preset teras yang telah dikenali seperti B01 paper fold, T01 mask reveal, B04/B07 counter, MP17 carta dan MP40 audiogram hanya apabila sesuai. Semak kawalan khusus setiap ID. Pilih komponen MA/preset PX untuk radar/peta melalui mekanisme dalam registry, bukan mencipta “preset radar” yang tidak wujud. Kira penggunaan yang DICADANGKAN sebagai rancangan; jangan mendakwa jumlah preset sudah digunakan atau video sudah dihasilkan.

Contoh klausa yang mesti diolah dan dimasukkan dalam prompt, bukan ditampal tanpa penyesuaian:

```text
Gunakan Buat Video Motion Grafik versi Gemini daripada folder skill yang sudah dipasang lengkap. Render sepenuhnya offline melalui backend HTML/SVG + GSAP + HyperFrames atau Python/Node + FFmpeg yang sesuai. Gunakan timeline HTML terhingga, paused:true dan registry window.__timelines yang sepadan composition ID; tunggu fon/aset sebelum ukuran dan capture. Resolve SKILL_ROOT; semak fail tempatan dan registry dahulu.

PALET: latar #F8F3E8, panel #E8E0CF, teks #263645, aksen #447891. Gunakan adapter palet cream; semak artwork hardcoded supaya latar akhir kekal cerah.

SCENE HOOK: pilih B01 untuk paper-fold reveal tajuk dan lapisan MA berbentuk garis/orbit yang relevan. Tentukan onset, hold dan exit setiap lapisan. Cari ID MA sebenar daripada indeks tempatan sebelum render.
SCENE BUKTI: jika brief membekalkan data, gunakan MP17 sebagai carta dan B04/B07 sebagai counter dengan angka yang sama, masa update yang selaras dan label yang boleh dibaca. Jika tiada data, gantikan dengan proses/SVG berkaitan, jangan cipta statistik.
SCENE PENUTUP: gunakan T01 untuk mask reveal CTA; pilih satu SFX VL yang sesuai dan jadualkan tepat pada reveal. Gunakan fon TTF sebenar daripada katalog FT dan ukur teks selepas load.

Panggil render bagi setiap frame menggunakan masa scene setempat, kemudian komposit hasilnya ke video. Jangan paparkan ID preset, kod, JSON atau poster katalog sebagai pengganti animasi. Bezakan subtitle penuh daripada caption kinetik. Render proof beberapa masa, tonton petikan dan semak MP4 akhir sebelum menyerahkan fail.
```

Tulis prompt lengkap dengan kandungan/topik pengguna yang sebenar. Jangan gantikan keseluruhan jawapan dengan contoh klausa di atas. Seksyen pemasangan di bawah terpakai apabila diminta install atau apabila penghasilan video memerlukan fail yang belum dipasang; ia tidak menghalang penulisan prompt sahaja.

## 1. Pasang semua fail dahulu, kemudian bekerja offline

PENTING: sandbox produksi pengguna bekerja OFFLINE. Jadikan Drive sumber pemasangan sahaja. Muat turun SEMUA pek, ekstrak semuanya dan simpan terus DI DALAM direktori skill yang kekal. Jangan menunggu projek video untuk mengambil aset satu persatu. Jangan memasang skill yang hanya menyimpan pautan Drive atau katalog tanpa fail sebenar.

Folder induk pengguna:
https://drive.google.com/drive/folders/1Vd09--QnSxFxNTPejHsEmcjYsU1UnY6j

Pek khusus versi ini:
https://drive.google.com/drive/folders/1599IpY-pb5jwnwOVgrTzfOK17waxsuNl

Manifest lengkap, checksum dan senarai setiap fail: https://drive.google.com/file/d/1MRIQO97Dj1FUgiETbKnU494o01M5GAOw/view?usp=drivesdk
Skrip pemasangan offline: https://drive.google.com/file/d/1Ukcf3tUMqQ3xRiyfq3IHg1eyMC7-iizJ/view?usp=drivesdk
Pembantu ekstrak/checksum: https://drive.google.com/file/d/1HDxX9W6mY3DDdLzSjI4Po9zZvzcLRcqy/view?usp=drivesdk


Pautan semua pek yang wajib dipasang:

| Pek | Saiz MiB | Fail Drive |
|---|---:|---|
| core | 1.55 | [Gemini_Motion_core.zip](https://drive.google.com/file/d/10O1xkq8ORhssqjXV88WGPbTnc1Gjajio/view?usp=drivesdk) |
| presets | 1.58 | [Gemini_Motion_presets.zip](https://drive.google.com/file/d/1oMGP8yddTnTVe1UMOg6pLAYxB7Xo34ge/view?usp=drivesdk) |
| characters | 2.09 | [Gemini_Motion_characters.zip](https://drive.google.com/file/d/1z3OJ81kmmKJJFPsYhkF7WLpjkF2xy8IZ/view?usp=drivesdk) |
| fonts | 7.74 | [Gemini_Motion_fonts.zip](https://drive.google.com/file/d/143SiQbq1eZoMs06pNNnrkczFBuhx0nXe/view?usp=drivesdk) |
| motion_array | 0.15 | [Gemini_Motion_motion_array.zip](https://drive.google.com/file/d/1N0TlLx7Rlu3SJ4CtZ9ThpbwmpthIz6V8/view?usp=drivesdk) |
| previews_01 | 7.94 | [Gemini_Motion_previews_01.zip](https://drive.google.com/file/d/1ohR8SkMnW4nnjwyZjVo9GNO6rYfERSOI/view?usp=drivesdk) |
| previews_02 | 3.54 | [Gemini_Motion_previews_02.zip](https://drive.google.com/file/d/1l-B01xE7_7nafiioK7XnVZsfTw8iQhID/view?usp=drivesdk) |
| svg | 1.17 | [Gemini_Motion_svg.zip](https://drive.google.com/file/d/1Ey-_2II6pre48Iz0jNS-h8LU1pwxzSft/view?usp=drivesdk) |
| vlog_payload_01 | 7.63 | [Gemini_Motion_vlog_payload_01.zip](https://drive.google.com/file/d/15T8JIC_n8DgXMrGQnGNeeHGkcvj6ByQC/view?usp=drivesdk) |
| vlog_payload_02 | 7.63 | [Gemini_Motion_vlog_payload_02.zip](https://drive.google.com/file/d/1f5SnPSIu7d8AVBkxVpfr_8T5uy5blUYO/view?usp=drivesdk) |
| vlog_payload_03 | 7.63 | [Gemini_Motion_vlog_payload_03.zip](https://drive.google.com/file/d/1zpa-n3iLXo7pxa-WiKPxgH7B7j9kpldw/view?usp=drivesdk) |
| vlog_payload_04 | 1.56 | [Gemini_Motion_vlog_payload_04.zip](https://drive.google.com/file/d/1VV3sR9FDkd8gKCUVJA2ClEe8DT2RdF3B/view?usp=drivesdk) |

Ambil fail melalui alat Drive/pelayar atau saluran pemindahan fail yang benar-benar tersedia kepada ejen SEMASA SETUP, sebelum sandbox offline bermula. Alat yang hanya dapat membaca teks tidak semestinya boleh memindahkan bait ZIP ke sandbox. Jangan cuba `wget`, `curl`, `pip install` atau `npm install` dari sandbox yang diketahui offline. Jangan ubah perkongsian Drive tanpa arahan pengguna. Jika setup sendiri tidak mempunyai sebarang laluan mengambil fail, jelaskan halangan itu; minta fail pek yang belum boleh dipindahkan, dan jangan mendakwa pemasangan selesai.

Google Drive memerlukan akses akaun/perkongsian yang betul. Halaman log masuk HTML bukan fail ZIP. Semak tandatangan ZIP, saiz dan SHA-256 daripada manifest. Pek ialah ZIP berasingan, setiap satu maksimum 8 MiB; setiap ZIP boleh diekstrak sendiri tetapi SEMUA pek diperlukan untuk pemasangan penuh. Ia bukan serpihan fail ZIP yang perlu dicantum secara binari.

Langkah setup wajib:

1. Kenal pasti lokasi skill sebenar daripada sistem Gemini atau aliran pemasangan yang tersedia. Jangan mengandaikan path ChatGPT seperti `/root/.codex`, atau folder `/tmp` yang hilang selepas sesi. Jika hanya sandbox sementara tersedia, hasilkan/persist folder skill melalui saluran fail kekal yang ada dan laporkan batas ketahanannya.
2. Simpan fail INI sebagai `SKILL.md` dalam root skill. Kekalkan versi lama secara berasingan.
3. Ambil manifest, `gemini_install.py`, `gemini_bootstrap.py` dan SEMUA ZIP dalam manifest melalui saluran setup. Letakkan kedua-dua skrip bersama, manifest sebagai JSON sebenar dan ZIP dalam satu direktori staging. Jangan ubah nama ZIP.
4. Jalankan pemasang di bawah dengan path sebenar. Pemasang tidak menggunakan rangkaian. Ia mengesahkan semua pek, mengekalkan struktur folder, memulihkan keseluruhan 600 aset VL asal, mengekstrak semua 100 fon beserta lesen dan memeriksa enjin render tempatan.
5. Selesaikan kekurangan dependency melalui persekitaran setup/pakej offline yang serasi sebelum menandakan pemasangan penuh berjaya. Jangan muat turun atau memasang binari yang tidak serasi dengan OS/CPU sandbox. Toolkit ini mengandungi kod/aset; ia tidak membawa semua binari Python/Node/FFmpeg bagi setiap platform.
6. Simpan folder skill lengkap, manifest dan `gemini-offline-status.json` dalam storan skill kekal. Buka sesi baru atau matikan akses rangkaian, jalankan semakan sekali lagi dan render petikan ujian. Hanya laporkan pemasangan offline lengkap apabila `ready` benar dan output sebenar lulus semakan.

```bash
python gemini_install.py \
  --manifest /path/staging/Gemini_Motion_Manifest.json \
  --packs-dir /path/staging \
  --skill-root /path/skills/buat-video-motion-grafik-gemini \
  --self-test
```

Selepas pemasangan, jalankan dari root skill:

```bash
python scripts/gemini_install.py --manifest Gemini_Motion_Manifest.json --skill-root . --verify-only --self-test
```

Jangan jadikan pemasangan semula semua aset sebagai langkah wajib setiap projek. Semak status dan fail tempatan dahulu. Jangan padam pek staging sebelum pemasangan, pemulihan aset, persist dan semakan offline berjaya. Jangan edit fail induk; salin fail yang hendak diubah ke folder projek.

Keperluan utama: Python 3.10+, Pillow, NumPy, FFmpeg/ffprobe dengan libx264. Untuk keseluruhan komponen SVG/MA/watak: Node.js dengan `sharp` tempatan; CairoSVG ialah pilihan tambahan dan mempunyai fallback `sharp` dalam salinan Gemini. Untuk Arab/Jawi, gunakan RAQM/HarfBuzz atau renderer shaping tempatan yang disahkan. Jangan mengandaikan import yang ada pada ChatGPT turut tersedia pada Gemini.

`gemini_bootstrap.py` turut mempunyai mod muat turun HTTPS bagi persekitaran SETUP yang benar-benar online; ia bukan laluan lalai sandbox Spark. Utamakan `gemini_install.py` dengan semua ZIP tempatan. Jika sengaja memilih sebahagian pek untuk diagnosis, jangan labelkannya sebagai pemasangan penuh.

### Naik taraf pemasangan V3 kepada HTML/HyperFrames

Muat turun SKILL.md, manifest dan pek core terkini melalui pautan yang sama. Sediakan juga `gemini_install.py` serta `gemini_bootstrap.py`. Sebelas ZIP aset V3 yang lain boleh digunakan semula jika saiz/SHA-256 sepadan manifest baharu; jangan muat turun semuanya semula tanpa perlu. Sediakan SEMUA 12 ZIP dalam staging; tiada muat turun semasa render. Simpan SKILL.md lama sebelum menggantikannya. Kekalkan `Gemini_Motion_Manifest.json` lama di root pemasangan sehingga upgrade selesai; letakkan manifest baharu di staging.

```bash
python /path/staging/gemini_install.py --manifest /path/staging/Gemini_Motion_Manifest.json --packs-dir /path/staging --skill-root /path/skills/buat-video-motion-grafik-gemini --upgrade --self-test
```

`--upgrade` menyemak semua pek dahulu dan hanya menggantikan fail yang masih sepadan checksum manifest lama. Fail yang diganti disimpan di `.gemini-backups/upgrade-*/`; fail suntingan pengguna menyebabkan upgrade berhenti dan dipelihara. Jika manifest lama tiada atau ada perubahan custom yang perlu disatukan, pasang ke root skill baharu dan bawa perubahan projek secara terarah. Selepas pemasangan, `--verify-only --self-test` menyemak semua fail serta merender petikan preset, watak V3 dan kamera. Semak `ready` dan output sebenar; ujian runtime tempatan bukan bukti pemasangan dalam akaun Gemini pengguna.

## 2. Fail tempatan dan kandungan yang mesti tersedia

Semua path relatif berikut bermula pada root skill, bukan cwd yang diteka. Simpan `SKILL_ROOT` sebenar pada awal sesi dan gunakan path absolut jika bekerja di folder projek lain.

| Kandungan | Lokasi tempatan | Cara menggunakan |
|---|---|---|
| 842 preset animasi berdaftar | `assets/motion_presets/` | `scripts/gemini_atlas.py`, `render.frame()` |
| 2000 komponen MA | `assets/motion_array/` | enjin SVG/Node dan recipe JSON |
| 1500 SVG | `assets/svg_elements/` | cari, salin, animasikan group/layer |
| 100 keluarga fon | `assets/fonts_creative_100/` | fail TTF sebenar + lesen, bukan nama fon semata-mata |
| 600 aset VL | `assets/vlog_montage/` | LUT, transition, overlay, grafik, SFX yang dipulihkan semasa install |
| 20 watak V3 | `assets/character_bank_20/` | 42 pose, 34 resipi gerakan setiap watak; enam sudut dan rig SVG offline |
| Kamera vektor Python | `scripts/vector_character_camera.py` | world/screen camera, zoom/pan dan IK; demo tanpa fail projek lama |
| Panduan lanjutan | `references/` | baca hanya bab berkaitan; fail ini mengatasi arahan khusus ChatGPT dalam rujukan asal |
| Utiliti render/QA | `scripts/` | panggil kod sebenar, semak stdout dan exit code |

Bank watak membawa enjin, metadata, galeri dan cache contoh. Ia boleh menjana semua 20 watak/42 pose/34 gerakan secara offline apabila dependency tersedia. 840 gabungan pose dan 680 gabungan gerakan ialah kapasiti resipi; jangan mendakwa semua MP4 V3 sudah diprarender. Cache contoh/pek penuh V2 lama kekal 32/24. Gunakan source V3 untuk render terkini, bukan menimpa source dengan cache V2. Abaikan keperluan Library ID ChatGPT dalam rujukan bank; Gemini mesti menggunakan rig tempatan atau fail yang telah dipasang. Katalog web hanya rujukan pilihan semasa online, bukan dependency render.

Motion Atlas: https://motion-preset-atlas.akramania.chatgpt.site

## 3. Palet lalai cerah dan lembut

Jangan gunakan latar hitam/navy/plum gelap secara lalai. Pilih krim, biru langit lembut, sage, lavender atau peach; gunakan teks gelap dengan kontras yang jelas. Ikut tema gelap hanya apabila pengguna meminta secara nyata atau rujukan terkininya menetapkannya.

Gunakan adapter `gemini_atlas.py` atau `gemini_compose.py`: kedua-duanya menetapkan medan warna sebenar semasa render. Menulis "pastel" dalam prompt atau `genre=corporate` sahaja tidak mencukupi; preset asal `saas`, `corporate`, `promo` dan `creator` banyak mempunyai default gelap.

| Palet adapter | Latar | Panel | Teks | Aksen |
|---|---|---|---|---|
| `cream` (lalai) | #F8F3E8 | #E8E0CF | #263645 | #447891 |
| `sky` | #EDF5FA | #D7E6EF | #253D50 | #427D9A |
| `sage` | #F0F5EC | #DEE8D7 | #304439 | #54836F |
| `lavender` | #F3EFF8 | #E2D9ED | #40374D | #8464A0 |
| `peach` | #FFF1E8 | #F1DCD0 | #503A32 | #B9664D |

Periksa hasil sebenar; artwork tertentu mempunyai warna hardcoded. Jika panel besar masih gelap atau teks terlalu pucat, olah salinan modul/recipe secara terarah. Jangan tutup kesalahan dengan lapisan putih yang menyembunyikan animasi. `--theme custom` mengekalkan warna config/upstream, jadi gunakannya hanya bagi brief yang memerlukannya. LUT bukan cara menukar keseluruhan identiti warna grafik secara sembarangan.

## 4. Gunakan preset sebagai ANIMASI, bukan tulisan kod

PENTING: ID seperti `K16`, `PX120`, `MA0501` ialah arahan pemilihan enjin. Ia bukan teks video. Jangan paparkan blok kod, JSON, ID preset, screenshot katalog atau poster statik sebagai pengganti animasi. Gunakan `labels=False` / `--clean` bagi hasil produksi. Label ID boleh muncul hanya jika pengguna meminta demo katalog.

Aliran wajib: pilih ID sah → baca metadata dan mekanisme → sediakan config dengan teks/aset pengguna → panggil fungsi render bagi SETIAP frame → gabungkan layer/klip dengan timeline → encode MP4 → ekstrak semula frame dan semak pergerakan. Import modul atau menyalin JSON sahaja belum menggunakan preset dalam video.

```bash
python scripts/gemini_atlas.py --list > /path/project/preset_registry.json
python scripts/gemini_atlas.py --preset B01 --duration 3 --fps 30 --width 1280 --palette cream --proof /path/project/proof --output /path/project/paper_fold.mp4
```

Tukar kandungan menggunakan JSON sebenar:

```json
{"preset":"B01","text":"IDEA JADI GERAKAN","subtitle":"Bina satu demi satu","duration":3}
```

```bash
python scripts/gemini_atlas.py --config /path/project/title.json --palette sky --output /path/project/title.mp4 --proof /path/project/title-proof
```

Adapter membuang overlay katalog dan menghasilkan contact sheet enam masa berbeza serta `motion_proof.json`. Semua frame identik ialah kegagalan. Frame yang berbeza sahaja belum membuktikan mutu: periksa transform objek, reveal/mask, stagger, counter, hold bacaan dan exit pada playback biasa. Elakkan gerakan mikroskopik yang kelihatan statik.

API Python: `configuration(pid, raw)` → `frame(pid, t_output_seconds, cfg, labels=False)`. Gunakan `t=i/fps`. API awam mengurus pemetaan jam; jangan menormalisasi masa dua kali. Preset biasa menggunakan jam reka bentuk 0–5 di dalam dispatch, manakala L01–L06 memakai saat sebenar. `duration` meretime preset biasa; L mempunyai `tempo` dan `cues` tersendiri. Jangan memanggil satu frame pada t=2.5 lalu mengulanginya sepanjang klip.

842 entri merangkumi 137 preset asal (termasuk K/MP/L), 185 demo adaptasi MS/PL/PV/AD, 120 EV dan 400 PX. MA ialah koleksi lain. Semak registry tempatan untuk ID/nama/parameter sebenar. Preset merupakan kod asal/adaptasi mekanisme preview; ia bukan fail After Effects/Envato berbayar.

## 5. Beberapa preset dalam satu scene

Jadualkan setiap layer dengan ID, `start`, `end`, rect piksel, teks dan data sebenar. Gunakan satu aksi utama yang boleh dibaca, disokong graph, radar, peta, counter atau elemen MA yang relevan. Variasikan mekanisme dan fungsi, bukan menukar warna tajuk yang sama sahaja. Bilangan preset bergantung pada brief dan ruang bacaan.

Contoh komposisi sebenar: paper fold + carta + counter, semuanya dikira setiap frame:

```json
{
  "size":[1920,1080],"fps":30,"duration":3,"palette":"cream",
  "layers":[
    {"start":0,"end":3,"rect":[0,0,1920,580],"config":{"preset":"B01","text":"KEMAJUAN","subtitle":"Daripada idea kepada hasil"}},
    {"start":0.3,"end":2.8,"rect":[80,580,850,478],"transparent":true,"config":{"preset":"MP17","text":"PENCAPAIAN","subtitle":"","values":[0.25,0.55,0.75,0.9]}},
    {"start":0.6,"end":3,"rect":[1000,580,800,450],"transparent":true,"config":{"preset":"H04","text":"PROJEK","subtitle":"","value":24,"decimals":0}}
  ]
}
```

```bash
python scripts/gemini_compose.py --config /path/project/scene.json --output /path/project/scene.mp4
```

Data contoh bukan fakta pengguna. Gantikan dengan angka sah atau jangan tampilkan metrik rekaan. Beberapa preset melukis latar penuh walaupun alpha diminta; periksa output dan bina modul/layer khusus apabila perlu. Kompositor mengekalkan nisbah 16:9 preset; ia tidak mereka bentuk semula 9:16 secara automatik. Untuk video menegak, susun semula artwork, teks dan safe area dalam canvas portrait. Jangan regang atau crop teks.

Baca `references/gemini-atlas-production.md`, `references/preset-atlas.md`, `references/premium-400-svg-1000.md` dan `references/kinetic-preset-integration.md` apabila mengolah preset kompleks.

## 6. Fon mesti dimuatkan sebagai fail sebenar

Semua fon perlu diekstrak semasa install. Pilih FT ID/family melalui indeks tempatan. Uji glyph, ukur teks dan render contoh dengan fon itu. Jangan tulis nama fon dalam label dan jangan anggap config `font_path` disokong oleh semua modul.

```bash
python assets/fonts_creative_100/prepare_fonts.py --list --search sans
python scripts/gemini_atlas.py --preset T01 --font FT0026 --palette cream --duration 3 --output /path/project/font-test.mp4 --proof /path/project/font-proof
```

Adapter memuatkan TTF dan mengikat `core.FONTS['sans']`/`['bold']` kepada fail sebenar; ia membersihkan cache fon sebelum render. Untuk renderer sendiri, panggil `ImageFont.truetype(actual_ttf_path, size)`. Bagi SVG/Node, register atau embed fon setempat dengan renderer yang menyokongnya; semak fallback fon. Kekalkan OFL/provenance. Pilih maksimum dua keluarga utama untuk satu video kecuali brief meminta eksperimen tipografi.

Arab/Jawi/al-Quran: gunakan shaping RTL/RAQM/HarfBuzz, jangan reverse string, jangan letter-spacing atau taip huruf satu persatu. Animasikan blok perkataan/baris yang sudah dibentuk. Semak ayat/harakat sebenar, bukan menganggap ujian beberapa ayat mengesahkan semuanya. Baca `references/fonts-creative-100.md`.

## 7. LUT, transition, overlay, SFX dan SVG

Semua fail VL mesti sudah tersedia secara fizikal selepas install; tiada fetch Drive/CDN semasa render. Gunakan `scripts/vlog_asset.py` untuk mencari ID dan mengaplikasikannya, bukan memaparkan kod LUT/matte.

```bash
python scripts/vlog_asset.py --type lut --search travel
python scripts/vlog_asset.py --id VL0001 --input /path/project/shot.mp4 --strength 0.35 --render /path/project/graded.mp4
python scripts/vlog_asset.py --id VL0101 --input /path/project/a_tail.mp4 --input-b /path/project/b_head.mp4 --duration 0.8 --render /path/project/transition.mp4
python scripts/vlog_asset.py --id VL0201 --input /path/project/shot.mp4 --strength 0.2 --render /path/project/overlay.mp4
python scripts/vlog_asset.py --id VL0501 --copy-to /path/project/audio
python scripts/svg_element.py --collection explainer --search education
```

LUT: guna `.cube` pada footage RGB SDR Rec.709, selepas pembetulan exposure/white balance. Normalisasikan Log/HDR dengan transform kamera yang sesuai dahulu. Kurangkan strength dan banding sebelum/selepas. Untuk vektor krim/pastel, biasanya kekalkan warna rekaan; LUT tidak diwajibkan pada setiap scene.

Transition: matte putih mendedahkan B, hitam mengekalkan A; `C=A*(1-M)+B*M`. Gunakan mask yang berubah mengikut masa, trim hujung A dan awal B, render overlap sahaja, kemudian susun A sebelum overlap + transition + baki B. CLI transition menghasilkan segmen senyap; bina semula timeline audio. Jangan tampal video matte hitam/putih di atas hasil akhir sebagai visual biasa. Periksa endpoint pertama/akhir.

Overlay: sumber hitam menggunakan blend Screen, bukan alpha H.264. Gunakan `1-(1-A)*(1-overlay*strength)`. Elakkan latar hitam menutup scene; opacity biasanya rendah. Periksa loop sebelum mengulang.

SFX: jadualkan WAV pada masa event, campur dengan VO/muzik, semak clipping dan dengar playback. Jangan pindahkan semua SFX ke t=0. Audio input yang telah diluluskan mesti dikekalkan ketika revisi visual.

SVG: gunakan fail asal beralpha, kekalkan viewBox/nisbah, asingkan group dan pivot. Gerakkan position/scale/rotation/opacity, stroke reveal atau morph yang sah berdasarkan masa. PNG statik yang hanya diberi zoom bukan animasi anggota. Baca `references/svg-assets-explainer-promotion.md` dan `references/local-vector-animation.md`.

MA: semak `assets/motion_array/index.json`/enjin dan `references/motion-array-components.md`. Contoh render sebenar:

```bash
node assets/motion_array/render_motion.mjs --id MA0501 --duration 3 --width 1280 --height 720 --fps 30 --output /path/project/ma.mp4
```

Gunakan recipe/scene JSON untuk layer tambahan dan output alpha untuk compositing. Warna latar preview dalam salinan Gemini sudah dilembutkan; sesuaikan juga warna foreground yang terlalu pucat untuk latar cerah. Jangan menganggap HUD demo/peta/counter mempunyai data sebenar.

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
