# Produksi HTML/SVG → GSAP → HyperFrames → MP4

Baca bersama `hyperframes-motion-bank.md` untuk adapter preset dan `media-tools.md` untuk transkripsi/pengasingan subjek. Aliran ini menambah backend HTML kepada toolkit; kekalkan semua preset, aset, watak, fon, audio serta backend Python/FFmpeg lama.

## 1. Setup dan status sebenar

Jalankan preflight `node scripts/setup_hyperframes.mjs` dari root skill. Gunakan Node.js **22+** (sekurang-kurangnya 22.12 untuk lock browser yang disertakan), FFmpeg/ffprobe, versi HyperFrames/GSAP dalam `assets/hyperframes/package-lock.json`, dan Chrome Headless yang berjaya dilancarkan. Periksa keempat-empat plugin: DrawSVGPlugin, MorphSVGPlugin, MotionPathPlugin, SplitText. Import dependency sahaja belum membuktikan render berjaya.

Pasang dependency yang kurang melalui mod setup online yang dinyatakan dalam `--help`; jangan fetch semasa render. Simpan runtime besar di cache/pemasangan kekal, bukan dalam Git. Untuk Gemini, sediakan Node, FFmpeg, library OS Chrome, seluruh node_modules, browser sebenar, fon, aset dan model pada OS/CPU sasaran sebelum sandbox offline bermula. Npm cache atau nama pakej sahaja tidak mencukupi. Jalankan preflight serta render tanpa rangkaian selepas memindahkan pemasangan. Bezakan `html_ready`, `asr_ready` dan `remove_background_ready`; satu status lulus tidak membuktikan semua ciri tersedia.

Salin `assets/hyperframes/` ke folder projek; jangan edit template induk bagi setiap video. Ikut skrip setup untuk memuatkan dependency setempat. Jalankan CLI tempatan yang dipin; jangan menggunakan `npx` tanpa pakej tersedia sehingga ia memuat turun versi lain secara senyap.

```bash
node scripts/setup_hyperframes.mjs
# Setup sahaja, apabila dependency belum ada dan rangkaian tersedia:
node scripts/setup_hyperframes.mjs --online
# Untuk pemasangan daripada npm cache lengkap pada OS/CPU yang serasi:
node scripts/setup_hyperframes.mjs --install-offline

# Selepas menyalin template dan menyesuaikan projek:
node scripts/run_hyperframes.mjs lint /path/project
node scripts/run_hyperframes.mjs render /path/project --fps 30 --workers 1 --quality standard --output /path/project/final.mp4
```

Wrapper `run_hyperframes.mjs` menggunakan cache runtime/browser daripada preflight, menutup semakan kemas kini/telemetri dan tidak menjalankan installer. Override cache dengan `KM_HYPERFRAMES_RUNTIME` atau browser dengan `HYPERFRAMES_BROWSER_PATH` apabila berpindah mesin. Fallback Chromium npm dalam lock ialah Linux x86_64; OS/CPU lain mesti menggunakan browser sasaran yang serasi melalui `--browser` semasa setup. Rekod ujian contoh 10 saat terdapat dalam `assets/hyperframes/validation.json`; ia bukan pengesahan automatik bagi projek baharu.

## 2. Artwork dan rig

- Gunakan satu `viewBox` konsisten, SVG Bézier berlapis, ID unik serta group yang bermakna: `world`, `background`, `midground`, `character`, `torso`, `upperArm`, `forearm`, `hand`, `foreground` dan HUD screen-space. Pisahkan kulit/pakaian, bayang, highlight dan prop.
- Letakkan origin/pivot sendi dalam koordinat parent sebelum membuat tween. Gunakan group berhierarki untuk tulang atas → tulang bawah → tangan; putaran bahu mesti membawa siku/tangan bersama. Jangan beri transform berlawan pada parent dan anak.
- Gunakan gradient, mask, clipPath, blur/drop shadow dan pencahayaan untuk kedalaman 2.5D. Namakan setiap ID defs dengan awalan watak/scene supaya mask tidak bercampur. Besarkan filter region jika bayang terpotong. Hadkan filter besar yang memperlahankan render.
- Kekalkan identiti, pakaian sopan dan `height_cm` bank V3. Bagi adaptasi rig bank ke DOM, baca source SVG asal dan petakan ID/pivot sebenar; jangan dakwa semua 20 watak sudah dipindahkan ke rig GSAP.
- Gunakan garis aksi, pemindahan berat, anticipation pendek, overshoot terkawal dan follow-through yang berlainan antara torso, kepala dan anggota. Tahan kaki/tangan pada titik kontak; IK dua tulang mesti mengehadkan sasaran di luar jangkauan, memilih sisi siku/lutut dan mengekalkan panjang anggota.
- Kamera: gerakkan parent world untuk pan/zoom, beri lapisan depth faktor parallax berbeza dan asingkan caption daripada kamera. Untuk cut/whip, rancang akselerasi, arah dan overlap; periksa endpoint tanpa flash.

## 3. Plugin dan teks Arab–Melayu

Daftar plugin secara eksplisit selepas GSAP dimuatkan. Gunakan fail `gsap/dist/*.min.js` daripada pemasangan tempatan, bukan CDN ketika produksi offline.

| Plugin | Gunakan untuk | Semak |
|---|---|---|
| DrawSVGPlugin | stroke reveal/erase | panjang path, stroke, tiada dash bocor pada hold |
| MorphSVGPlugin | perubahan bentuk path | siluet, winding, shapeIndex dan bentuk pertengahan; pecahkan objek jika morph keseluruhan buruk |
| MotionPathPlugin | objek mengikut Bézier | align/origin, autoRotate hanya jika aksi sesuai, kelajuan serta sentuhan |
| SplitText | kinetic typography perkataan/baris | font final, ukuran, line wrapping, stagger dan hold bacaan |

Untuk Arab, gunakan `lang="ar" dir="rtl"`, fon yang meliputi glyph/harakat dan baris yang mempunyai line-height mencukupi. Animasikan **perkataan lengkap atau baris**, tanpa `chars`, reverse string atau letter-spacing. Bagi teks bercampur, asingkan angka/Latin menggunakan elemen `bdi`/arah yang betul. Utamakan baris penuh apabila penyambungan atau susunan tanda baca terganggu. Gunakan satu sumber teks untuk layer dasar/highlight supaya glyph, wrapping dan kedudukan kekal serupa. Subtitle Melayu berhighlight mengikuti maksud frasa Arab; timestamp perkataan Arab bukan alignment automatik perkataan terjemahan Melayu.

Muatkan fail fon sebenar sebelum `getBBox`, `getBoundingClientRect`, SplitText atau pengiraan line breaks. Tunggu `document.fonts.ready`, panggil `document.fonts.load` untuk family/weight yang digunakan, semak `document.fonts.check`; decode imej dan lengkapkan pemuatan aset. Gagal awal jika aset tiada, bukan menggunakan fallback senyap. Bekukan layout setelah diukur; jangan auto-reflow/SplitText semula ketika capture.

## 4. Kontrak HyperFrames dan masa

Root mesti menyatakan composition ID, saiz dan tempoh positif mengikut schema versi dipin. Daftar timeline yang **terhingga** melalui `window.__timelines[compositionId]`, sepadan dengan `data-composition-id`, dan cipta dengan `gsap.timeline({paused:true})`. Gunakan `repeat` terhingga dan posisi saat eksplisit. HyperFrames mengawal clip lifecycle dan media; animasikan rupa anak/wrapper, bukan mengambil alih play/pause/currentTime video atau audio. Jangan nest semula timeline sub-composition yang sudah didaftar; runtime mengurus offsetnya.

Ikut readiness API **versi yang dipin dan sudah diuji** dalam template. Pendaftaran async selepas fon mesti berada dalam gate yang runtime tunggu; jangan daftar timeline kosong kemudian menambah tween selepas render bermula. Jika versi lama hanya menyokong setup sinkron, preload/ukur dahulu pada langkah build lalu gunakan timeline sinkron; jangan mencipta flag readiness sendiri dan menganggap HyperFrames membacanya. Rujuk template/QA sebenar untuk mekanisme yang disahkan.

Untuk versi **0.8.185** yang diuji, deklarasikan promise secara sinkron pada `window.__hf.buildReady[compositionId]`; runtime menunggunya sebelum capture. Bina semua tween selepas font/aset siap, daftar timeline pada akhir, kemudian panggil `window.__hfForceTimelineRebind?.()` seperti template. Jangan menggunakan pola ini pada versi lain tanpa menyemak source/QA. Bentuk minimumnya:

```javascript
window.__hf = window.__hf || {};
window.__hf.buildReady = window.__hf.buildReady || {};
window.__timelines = window.__timelines || {};
window.__hf.buildReady.root = (async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(image => image.decode()));
  // Muatkan/check family+weight tertentu sebelum ukuran dan SplitText.
  const timeline = gsap.timeline({paused: true});
  timeline.fromTo('#title', {opacity: 0}, {opacity: 1, duration: .6}, .2);
  timeline.to({clock: 0}, {clock: 1, duration: .1}, 9.9);
  // Inisialisasi plugin lazy; state render mestilah bebas callback/event.
  timeline.seek(10, true).seek(0, true).pause();
  window.__timelines.root = timeline; // root data-composition-id="root"
  window.__hfForceTimelineRebind?.();
})();
```

Demo menginisialisasi plugin lazy pada hujung timeline sebelum kembali ke sifar dan didaftar. Uji semula selepas warmup; jangan menganggap warmup sahaja membuktikan determinisme. Rasterisasi teks statik juga perlu stabil apabila lapisan compositor berubah; demo menetapkan lapisan brand sendiri. Jangan longgarkan toleransi hash untuk menyembunyikan perubahan pose/layout.

Gunakan masa mutlak `t=frame/fps`. Larang `Date.now`, `performance.now`, `Math.random` tanpa seed, setTimeout, animasi CSS tak terkawal, ticker/RAF bebas dan `repeat:-1` bagi gerakan kritikal. Kira state sebagai fungsi t; animasi yang dibina dengan tween nilai langsung mesti boleh di-seek balik ke t=0. Jangan mengubah teks, menambah node atau mencetus SFX secara imperatif dalam `onComplete`/`tl.call` untuk state yang perlu boleh di-seek. Untuk IK/prosedural/canvas, gunakan adapter seek versi runtime yang sah atau bake keyframe; `onUpdate` yang hanya berjalan semasa play bukan kontrak capture.

Sediakan cue manifest: scene/layer ID, start/end, posisi, font path, preset asal/adapter, seed, onset/offset audio dan masa siap-baca. Pisahkan entrance, hold dan exit supaya retime scene tidak memperlahankan semua aksi. Jadualkan VO/SFX dengan elemen audio bertiming atau campuran FFmpeg deterministik; jangan memainkan bunyi melalui callback JS.

## 5. PixiJS dan Three.js apabila perlu

Gunakan PixiJS bagi jumlah sprite/partikel yang membebankan SVG; jangan pasang hanya kerana tersedia. Matikan automatic/private/shared ticker yang berkaitan; seed taburan partikel, kira posisi daripada t dan panggil renderer tepat selepas state selesai. Bagi Three.js, sediakan model, material, lampu, kamera, renderer dan masa animasi/mixer mutlak; hentikan loop bebas. Tunggu texture/shader siap, gunakan backend GPU/headless yang benar-benar berfungsi dan panggil render selepas seek. Integrasikan melalui frame adapter HyperFrames yang disokong versi dipin. Uji seek bukan berurutan dan capture; jika adapter tidak berjalan, render segmen PNG/alpha secara berasingan dan komposit dengan FFmpeg. Bezakan panduan ini daripada backend yang sudah diuji; demo HTML asas tidak mengesahkan PixiJS/Three.js.

## 6. Uji sebelum master panjang

1. Semak tiga styleframe: artwork, nisbah, kontak rig, glyph Arab–Melayu, safe area dan kontras. Render petikan aksi 3–5 saat serta sekurang-kurangnya satu transisi.
2. Jalankan lint/check versi CLI dipin dan QA seek. Banding frame t yang sama selepas urutan maju, mundur, ulang dan reload. Periksa frame pertama/akhir, clip boundary, hold serta morph pertengahan. Simpan hasil hash dan toleransi yang digunakan; jangan dakwa deterministik merentas OS/GPU/font berbeza.
3. Render MP4 melalui HyperFrames; sahkan resolusi/FPS/frame count/durasi dengan ffprobe dan nyahkod penuh menggunakan FFmpeg. Ekstrak frame daripada MP4 akhir. Semak glyph, rig, clipping, perubahan frame, transisi dan penutup. Perbezaan hash sahaja tidak membuktikan gerakan cantik.
4. Audio: semak onset SFX/VO/subtitle pada awal, tengah dan akhir, clipping/true peak serta durasi trek. Dengar playback apabila keupayaan audio tersedia; jangan mendakwa telah mendengar berdasarkan waveform sahaja. Ujian nada sintesis hanya membuktikan cue nada, bukan ketepatan VO/subtitle ceramah.
5. Simpan manifest, versi, preflight, QA, MP4 serta kod HTML/SVG projek. Nyatakan komponen/model yang belum boleh dipasang atau backend yang belum diuji. Ujian runtime ChatGPT tidak membuktikan pemasangan dalam akaun Gemini pengguna.

`scripts/qa_hyperframes.mjs` menguji **template demo** (ID, dimensi dan probes demo tertentu), bukan validator universal bagi semua HTML. Adaptasi selector/viewport/probes kepada projek baharu atau gunakan capture engine versi dipin; jangan mendakwa ia memeriksa subtitle, audio VO dan semua watak secara automatik.

## Sumber primer

- HyperFrames GSAP: https://hyperframes.app/docs/3-guides/3-gsap-animation
- Schema HTML: https://hyperframes.app/docs/6-reference/html-schema
- Enjin capture: https://hyperframes.app/docs/5-packages/engine
- Determinisme: https://hyperframes.app/docs/2-concepts/4-determinism
- GSAP pemasangan/plugin: https://gsap.com/docs/v3/Installation/
- DrawSVG: https://gsap.com/docs/v3/Plugins/DrawSVGPlugin/
- MorphSVG: https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/
- MotionPath: https://gsap.com/docs/v3/Plugins/MotionPathPlugin/
- SplitText: https://gsap.com/docs/v3/Plugins/SplitText/
- PixiJS ticker: https://pixijs.com/8.x/guides/components/ticker
- Three.js renderer: https://threejs.org/docs/pages/WebGLRenderer

Semak source versi terpasang jika dokumentasi awam bercanggah tentang readiness/schema; jangan menggabungkan kontrak versi berbeza tanpa ujian.
