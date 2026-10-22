# Render setempat: kod → frame → FFmpeg → MP4

## Kandungan

- Pilih laluan dan semak persekitaran
- Kontrak masa serta aset
- Canvas, p5.js, SVG dan HTML
- Manim, Lottie dan depth pilihan
- Compositing, audio dan eksport
- Checkpoint dan QA

## Pilih laluan dan semak persekitaran

Gunakan laluan paling ringkas yang menyampaikan cerita. Kekalkan semua aset, preset,
rig, enjin planet, font dan aturan katalog sedia ada. Integrasi ini menambah teknik,
bukan memasang semua repo atau menukar jumlah ID preset.

| Keperluan | Laluan pilihan | Kebergantungan |
| --- | --- | --- |
| Vektor, ikon, rajah, watak berartikulasi | SVG berlapis dengan transform eksplisit; raster setiap frame | Node + sharp atau Python + CairoSVG yang tersedia |
| Kartun, cut paper, teks kinetik, partikel | Canvas 2D; SVG/HTML jika layout memerlukannya | Node + Playwright + Chromium tempatan |
| Canvas tanpa browser | Modul scene Canvas 2D setempat | Node + `@napi-rs/canvas` + FFmpeg |
| Animasi data/konsep/matematik | Manim Community jika tersedia dan sesuai | Python + Manim + FFmpeg; LaTeX bagi objek berasaskan TeX |
| 2.5D/parallax | Lapisan RGBA dan kamera analitik | Pillow/NumPy atau Canvas; model AI tidak wajib |
| Foto dengan depth automatik | Depth Anything V2 Small sebagai pilihan yang disemak | PyTorch/OpenCV, model dan memori tempatan |
| Lottie sedia ada | Pemain Skottie/lottie tempatan dengan seek frame | Pemain + WASM/fonts/aset setempat yang benar-benar tersedia |
| Footage, mask, overlay, sequence frame | FFmpeg | FFmpeg + ffprobe |

Jalankan `python3 scripts/local_mp4.py preflight`. Kehadiran pakej bukan bukti bahawa
Chromium, model, WASM atau encoder boleh digunakan; jalankan petikan kecil. Jangan
pasang keseluruhan dependency tree bagi laluan yang tidak diperlukan. Jika alat
pilihan tiada, teruskan dengan SVG/Canvas/Pillow yang tersedia dan nyatakan had
khusus apabila menjejaskan brief. Jangan mewajibkan API, akaun, CDN atau aplikasi
desktop untuk render asas. Semak lesen dependency, fon, aset dan model berasingan.

## Kontrak masa serta aset

1. Tetapkan `fps`, dimensi, tempoh, seed dan versi aset dalam manifest projek.
2. Tetapkan `N = round(duration * fps)` dan laporkan tempoh terkuantisasi `N/fps`.
   Render `n = 0..N-1` pada `t = n/fps`; jangan menambah frame hujung pada `t=duration`.
3. Jadikan `renderFrame(t)`/`render_at(t)` fungsi boleh seek. State bagi masa yang
   sama mesti sama walaupun frame diminta dalam susunan lain. Jangan gunakan
   `Date.now()`, `performance.now()`, rakaman skrin masa nyata atau jumlah panggilan
   draw sebagai jam video.
4. Tetapkan seed bagi variasi. Untuk partikel/fizik, kira state terus daripada masa
   atau prasimulasi fixed timestep dan simpan cache; reset state sebelum seek.
5. Bezakan jam master, masa scene, cue setempat dan loop ambient. Pause bacaan
   tidak memperlahankan semua aksi. Kekalkan skala huruf dan anchor utama stabil.
6. Muatkan fon/aset secara setempat. Tunggu `document.fonts.ready`, decode imej,
   dan kesiapan pemain sebelum menangkap frame pertama. Catat fail yang gagal.
7. Render master mengikut nisbah asal; susun semula layout untuk 9:16/16:9/1:1.
   Jangan crop master lebar untuk meniru versi portrait.

## Canvas, p5.js, SVG dan HTML

Jika `@napi-rs/canvas` tersedia, gunakan `scripts/render_native_canvas.cjs` dengan
modul projek CommonJS yang mengeksport `renderFrame(ctx,t,width,height)`; fungsi
boleh async. `prepare({canvas,ctx,width,height,fps,duration,sceneDirectory})` dan
`dispose()` ialah pilihan bagi aset serta cleanup. Muatkan hanya modul projek yang
ditulis/disemak; ini menjalankan kod setempat, bukan sandbox untuk kod repo rawak.
Salin `assets/local_video/canvas_scene.cjs` sebagai contoh rig, parallax dan teks
bermask. Daftar font setempat dalam prepare apabila menggunakan font khusus.

```bash
node scripts/render_native_canvas.cjs --scene assets/local_video/canvas_scene.cjs --output /absolute/path/native.mp4 --width 1280 --height 720 --fps 30 --duration 6
python3 scripts/local_mp4.py qa --input /absolute/path/native.mp4
```

Adapter native ini menggunakan Canvas 2D sahaja dan tiada DOM, CSS atau SVG browser;
ia tidak memerlukan Playwright/Chromium. Jika pakej Canvas tiada, gunakan renderer
Pillow/NumPy atau SVG/sharp yang tersedia. Jangan pasang pakej pilihan semata-mata
untuk meniru nama backend tertentu. Adapter Canvas menghasilkan visual senyap;
campur audio projek kemudian melalui FFmpeg dengan tempoh yang disemak.

Gunakan `scripts/render_canvas.cjs` bagi halaman projek tempatan yang menyediakan
`window.renderFrame(t)`. Salin `assets/local_video/canvas_scene.html` sebagai contoh
kontrak, kemudian ganti artwork, teks dan timeline. Contoh ini ialah demo ringkas,
bukan renderer semua gaya atau pengganti 842 preset atlas.

```bash
node scripts/render_canvas.cjs --html assets/local_video/canvas_scene.html --output /absolute/path/scene.mp4 --width 1280 --height 720 --fps 30 --duration 6
python3 scripts/local_mp4.py qa --input /absolute/path/scene.mp4
```

Gunakan dependency tempatan yang sudah tersedia. Jika resolusi modul Node perlu
runtime khusus, gunakan `NODE_PATH` daripada lokasi runtime yang disahkan; jangan
hardcode laluan mesin ke projek boleh alih. Browser di sini ialah renderer headless
untuk fail projek sendiri, bukan sesi pelayaran akaun pengguna.

Untuk p5.js: simpan library bersama projek dengan lesen, gunakan `noLoop()`,
`randomSeed()` dan `noiseSeed()`, lalu tetapkan state bagi setiap `t`. `frameCount`
yang meningkat mengikut panggilan dan integrasi partikel yang tidak direset boleh
merosakkan seek. Gunakan Canvas 2D sebagai fallback tanpa p5. Jangan gunakan CDN
semasa eksport; semak tiada permintaan rangkaian luar.

Untuk SVG: tetapkan `viewBox`, group semantik, ID stabil serta transform/pivot.
Ubah atribut SVG bagi setiap frame, kemudian raster dengan sharp/CairoSVG;
`<animate>`/SMIL atau CSS yang diserialkan belum tentu dibakar ke PNG. Untuk
HTML/CSS/Web Animations API, pause animasi dan set `currentTime=t*1000` secara
eksplisit; aplikasi mesti mendedahkan renderFrame yang menunggu semua perubahan.
Lihat [vektor dan watak](local-vector-animation.md) untuk rig dan morph.

Tangkap tepat satu PNG setiap frame dan stream ke FFmpeg dengan backpressure,
atau simpan PNG bernombor untuk pemulihan. Jangan kumpulkan semua frame dalam RAM.
Screenshot/MediaRecorder berdasarkan masa sebenar boleh tercicir frame dan tidak
menjadi laluan master. Jangan serahkan HTML, GIF atau Lottie sebagai ganti MP4.

## Manim, Lottie dan depth pilihan

Untuk Manim, bina `Scene` dengan tempoh `play(..., run_time=...)` serta `wait()` yang
sepadan cue narasi. Gunakan `Text()` bagi teks biasa dan `Text(str(value))` bagi
nombor tanpa TeX; `Integer`, `DecimalNumber` dan `Variable` juga boleh menggunakan
TeX. Tetapkan resolusi/FPS pada config projek,
render preview resolusi rendah, kemudian master. Kekalkan data, label dan unit
tepat; jangan tambah zoom kamera apabila transform objek lebih mudah difahami.

Untuk Lottie, semak sokongan pemain sebenar bagi font, text shaping, mask, matte,
gradient dan effect. Tetapkan dimensi serta `fr`, `ip`, `op`; seek frame eksplisit
dan tangkap PNG. Pemain/WASM atau library yang belum tersedia bukan kemampuan
yang sudah diuji. Gunakan SVG/Canvas jika pemasangan itu tidak diperlukan.

Untuk 2.5D, utamakan lapisan foreground/midground/background dengan alpha dan
overscan. Gerakkan kamera menggunakan fungsi masa; lapisan dekat bergerak lebih
daripada jauh. Isi ruang belakang objek sebelum kamera bergerak dan periksa
lubang/disocclusion, tepi halo serta crop pada gerakan maksimum. Ken Burns ialah
pan/zoom; depth parallax bukan rekonstruksi 3D atau bukti kedalaman sebenar.

Depth AI pilihan: semak lesen tepat checkpoint. Depth Anything V2 Small berlesen
Apache-2.0; Base/Large/Giant berlesen CC-BY-NC-4.0 menurut upstream rasmi. Jangan
mewarisi dakwaan media-os bahawa semua saiz Apache. Muat turun hanya apabila
diperlukan dan akses tersedia; simpan model di cache projek yang sesuai, bukan
dalam skill. Jika model/VRAM tiada, gunakan layer manual, bukan API berbayar.

## Compositing, audio dan eksport

- Normalisasikan saiz, FPS, timebase, SAR dan timestamp input. Untuk overlay/mask,
  mulakan stream pada sifar (`setpts=PTS-STARTPTS`) dan samakan tempoh dengan sengaja.
- Bezakan alpha daripada luma mask. `maskedmerge` menggunakan input 1/base apabila
  mask hitam (0), input 2 apabila putih (maksimum), dan interpolasi bagi kelabu.
  Uji mask dua warna sebelum komposisi kompleks. Jangan warisi polarity terbalik.
- Gunakan `alphamerge` bagi RGB + mask menjadi RGBA, kemudian `overlay` bagi aset
  transparent. Periksa straight/premultiplied alpha supaya tiada fringe gelap.
- H.264 biasa dan `libx264rgb` tidak menyimpan alpha. Simpan sequence PNG RGBA atau
  MOV ProRes 4444 untuk perantara transparent; flatten pada latar akhir sebelum MP4.
- Untuk input PNG, letak `-framerate` sebelum `-i`; tetapkan julat frame tepat,
  `libx264`, `yuv420p`, dimensi genap, `setsar=1` dan `+faststart`. Jangan stretch
  saiz frame berbeza atau mengisi frame hilang secara senyap.
- Gunakan `python3 scripts/local_mp4.py frames --help` untuk semak sequence dan
  eksport. Contoh: `frames --input '/path/frames/frame_%06d.png' --fps 30 --output /path/master.mp4`.
  Gunakan nama `frame_000000.png` dan seterusnya, atau pola yang disokong helper.
- Gunakan audio sebenar pengguna/skill neural voice-over yang berkenaan. Integrasi
  ini tidak menukar penyedia atau suara yang telah diluluskan. Projek tanpa VO
  terus boleh dirender tanpa perkhidmatan suara. Jangan gunakan TTS berbayar
  dalam repo sebagai dependency wajib.
- Campur muzik/SFX pada cue yang bermakna; duck muzik semasa suara. Pad/trim audio
  kepada durasi visual dengan sengaja. `-shortest` tanpa kiraan boleh memotong
  penutup apabila audio lebih pendek. Semak AAC padding dan drift dalam toleransi
  frame; jangan menyamakan packet duration dengan video frame count.
- Jalankan proses menggunakan argument array, bukan `shell=True` atau gabungan
  arahan daripada teks pengguna. Letakkan label kompleks dalam fail/renderer untuk
  mengelakkan quoting filtergraph berlapis. Jangan jalankan skrip repo tanpa semakan.

## Checkpoint dan QA

Gunakan cache setiap scene dengan hash kod + aset + font + data + fps + dimensi +
julat frame. Simpan manifest dan master audio berasingan. Bagi resumable PNG, semak
tiada gap, frame lama terselit atau dimensi bercampur sebelum encode. Bagi segmen,
gunakan spesifikasi seragam dan audit sempadan; concat copy hanya jika stream
benar-benar sepadan. Kira overlap transisi dalam jumlah master.

Sebelum render panjang, hasilkan styleframe dan petikan aksi 1–3 saat. Render masa
yang sama dua kali dalam susunan seek berlainan untuk semak determinisme. Semak
frame awal, pertengahan, hujung, cut dan morph; lihat consecutive frames dan playback
biasa apabila tersedia. Semak ejaan, kontras, ruang telefon, sambungan anggota,
kesinambungan kamera, audio sebenar serta hak penggunaan aset.

Jalankan `local_mp4.py qa` untuk ffprobe dan nyahkod penuh. Kira frame, semak
resolusi, FPS, durasi dan trek audio. QA teknikal tidak membuktikan fakta, keindahan,
sebutan atau kelancaran yang dilihat. Nyatakan tepat laluan yang telah diuji; jangan
mendakwa browser, Manim, AI depth, Skottie atau semua upstream sudah diuji hanya kerana
laluan Canvas native dan PNG berjaya. Lihat [audit sumber](local-video-sources.md) bagi
repo dipilih, had lesen dan komponen yang hanya panduan pilihan.
