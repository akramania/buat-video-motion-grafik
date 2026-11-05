# HyperFrames dengan Codex: run, analisis contoh dan penerapan

## Kandungan

1. Sumber dan skop pemerhatian
2. Cara run rasmi dan laluan skill
3. Kajian sepuluh klip
4. Bahasa gerakan untuk produksi
5. Scene panjang dan gaya Salah Label
6. Pilih blok dan templat
7. Semakan dan had bukti

## 1. Sumber dan skop pemerhatian

Untuk pemilihan explainer, produk, grafik pendek, muzik, data/peta, avatar, GitHub PR, slideshow atau video campuran, gunakan `hyperframes-nine-workflows.md`.

Gunakan sumber primer berikut; semak `--help` versi terpasang apabila laman berubah:

- Codex: https://hyperframes.heygen.com/guides/with-codex
- Galeri: https://hyperframes.heygen.com/examples
- Motion: https://hyperframes.heygen.com/prompting/motion
- Render: https://hyperframes.heygen.com/guides/export-and-share
- Motion graphics: https://hyperframes.heygen.com/guides/motion-graphics
- Indeks dokumentasi: https://hyperframes.heygen.com/llms.txt
- Source rasmi: https://github.com/heygen-com/hyperframes

Kajian 1 November 2026 memeriksa **sepuluh MP4 kad galeri**, metadata ffprobe, sembilan sampel merentasi setiap klip dan sampel temporal lebih rapat untuk empat petikan. Ini ialah kajian visual pensampelan, bukan tontonan dengan pendengaran audio penuh, bukan semua video galeri, dan bukan audit source projek contoh. Jangan menamakan aset/subjek yang tersalah label pada kad sebagai bukti rig tertentu. Contohnya kad “Cartoon: The Frameys” yang diperiksa sebenarnya memaparkan pentas anugerah dan kad video berperspektif.

Bezakan tiga lapisan bukti: **diperhatikan** dalam piksel klip; **didokumentasikan** oleh HeyGen; **resipi adaptasi** HTML/SVG/GSAP kita. Video yang nampak 3D atau bermatting tidak membuktikan semua aset sumber ialah vektor atau semua teknik telah tersedia setempat. Jangan menyalin logo, watak, teks, footage atau tema contoh ke projek pengguna tanpa keperluan dan hak penggunaan.

## 2. Cara run rasmi dan laluan skill

Panduan Codex rasmi memerlukan **Node.js 22+**, npm dan FFmpeg. Pada pemasangan Codex biasa, arahan rasminya:

```bash
npx hyperframes skills update
npx hyperframes skills check
npx hyperframes doctor
npx hyperframes preview
npx hyperframes render --output renders/final.mp4
```

`skills update` memasang skill rasmi ke `~/.agents/skills`. Pilihan pemasangan per projek ialah `npx skills add heygen-com/hyperframes` melalui picker Core Skills + Codex. Bezakan pemasangan skill rasmi itu daripada mengemas kini **Buat Video Motion Grafik**: jangan memasangnya semula secara automatik hanya untuk membaca atau menggunakan rujukan. Jangan membawa aturan pihak ketiga tentang menunggu kelulusan, akaun, telemetri atau publish ke dalam kerja yang telah diberi kuasa pengguna.

Dalam skill ini, gunakan [lock komponen terkini](video-component-toolkit.md): HyperFrames **0.9.4**, GSAP **3.15.0**, Node **26.13.0 LTS** (minimum **22.12+** kerana tooling browser). Jalankan preflight semasa; pengesahan versi lama tidak mengesahkan versi baharu. Semakan 1 November 2026 berjaya melancarkan Chrome Headless sebenar menggunakan Node 24.22.1, FFmpeg/ffprobe, empat plugin GSAP dan tanpa pemasangan/rangkaian. Status itu ialah bukti mesin ujian pada tarikh tersebut; ulang preflight di mesin/sesi baharu. Jangan menjalankan `npx` tanpa pin sehingga versi lain dimuat turun semasa render.

Jalankan dari root skill, dengan laluan projek mutlak:

```bash
node scripts/setup_hyperframes.mjs --help
node scripts/setup_hyperframes.mjs
# Hanya apabila dependency tiada dan akses rangkaian tersedia:
node scripts/setup_hyperframes.mjs --online
# Pilihan apabila npm cache lengkap pada OS/CPU yang sama:
node scripts/setup_hyperframes.mjs --install-offline

# Salin assets/hyperframes/ ke projek baharu dan ubah semua kandungan demo.
node scripts/run_hyperframes.mjs doctor --json
node scripts/run_hyperframes.mjs lint /absolute/project
node scripts/run_hyperframes.mjs check /absolute/project --json
node scripts/run_hyperframes.mjs snapshot --help
node scripts/run_hyperframes.mjs snapshot /absolute/project --at 0,1,3,6,9 --describe false
node scripts/run_hyperframes.mjs preview /absolute/project
node scripts/run_hyperframes.mjs render /absolute/project --fps 30 --workers 1 --quality draft --output /absolute/project/proof.mp4
node scripts/run_hyperframes.mjs render /absolute/project --fps 30 --workers 1 --quality delivery --output /absolute/project/final.mp4
```

Sesuaikan timestamp snapshot dengan durasi sebenar. `preview` ialah server berterusan; rekod URL/PID/log dan semak responsnya jika digunakan. Ia bukan MP4 atau pengganti render. Projek yang pengguna sudah minta disiapkan terus boleh melalui review dalaman dan render tanpa hentian kelulusan tambahan. Untuk proof pendek daripada projek panjang, semak `render --help` dahulu bagi pilihan julat yang benar-benar disokong; jangan mengubah semua tween dengan timeScale hanya untuk memendekkan video.

Nilai `.ok` daripada `doctor --json` dan status setiap pemeriksaan; exit code doktor sahaja tidak membuktikan ready. Nilai keperluan mengikut laluan: ujian ini melaporkan `.ok:false` kerana Docker dan penyedia pilihan whisper-cpp/Kokoro/MusicGen tiada, walaupun Node, FFmpeg, ffprobe dan Chrome lulus. Itu tidak menghalang render HTML setempat tanpa VO. Jangan memasang semua ciri pilihan untuk menghijaukan doktor; sahkan preflight dan render sebenar laluan yang diperlukan. Whisper Python skill ini mempunyai preflight berasingan.

Jika lint gagal, `check` mungkin tidak menjalankan audit browser/layout: **0 samples bukan lulus**. Semak ralat, amaran, julat sampel dan output sebenar. Jangan mematikan pemeriksaan kontras/layout hanya untuk mendapat status lulus. Padankan temuan dengan piksel sebenar; dokumentasikan crop disengajakan dan baiki kecacatan sebenar. Gunakan `snapshot --describe false` untuk QA visual setempat tanpa panggilan analisis Gemini automatik apabila API key hadir; jangan menghantar frame/aset kepada penyedia luar tanpa keperluan dan kebenaran yang sesuai.

Dalam ujian 0.8.185, snapshot boleh menghasilkan PNG/contact sheet walaupun stdout `--json --describe false` kosong; semak artifak sebenar dan jangan anggap log kosong sebagai bukti lulus/gagal. Jika hash seek berbeza, simpan kedua-dua frame, diff piksel dan state transform/layout; asingkan isu rasterisasi daripada pose. Laporkan exact-hash gagal selagi belum diselesaikan, tanpa melonggarkan toleransi untuk menutup kecacatan.

Kekalkan template readiness `window.__hf.buildReady[compositionId]` yang diuji dahulu untuk **0.8.185** (source 0.9.4 turut mengandungi gate ini; ulang QA browser pada runtime baharu), timeline `paused:true`, `window.__timelines` dan pemuatan font/aset dalam `html-hyperframes-production.md`. Jangan mencampur runtime/template baharu tanpa proof. Kekalkan cache dependency, browser dan berat model di luar Git skill.

## 3. Kajian sepuluh klip

Nama fail berikut ialah MP4 kad yang dipautkan oleh DOM galeri, bukan janji versi penuh dalam Studio. Durasi ialah container ffprobe; titik pemerhatian ialah sampel, bukan ukuran tepat onset setiap aksi.

| Kad / fail | Metadata diperiksa | Pemerhatian visual | Resipi penerapan |
|---|---|---|---|
| Studio launch / `studio-launch-v1.mp4` | 30.00s, 1280×720 | Footage pembuka → notifikasi rapat → prompt UI → maskot/buku → kad hasil → timeline/editor; skala shot berubah untuk memperlihatkan butiran | Gunakan footage sebenar apabila diberi; bina wrapper UI berlapis, zoom ke tindakan, kemudian kecilkan hasil ke ruang seterusnya. Jangan fabrikasi produk sebenar |
| Going through a change / `kinetic-type-curiosity-v1.mp4` | 20.416s, 960×720 | Kontras hitam/putih; frasa besar kemudian prop kamera, rekod muzik, tangan dan huruf berselerak; susun atur berubah dengan objek fokus | Gunakan mask perkataan, blur-swap pendek, ikon/prop berkaitan makna dan pertukaran lokasi. Bezakan teks utama, prop dan teks sokongan |
| The journey of “k” / `k-v1.mp4` | 53.61s, 720×1280 | Mesej kecil menjadi objek penghubung merentas bilik, laluan kabel, dasar laut, server dan penerima; pandangan dekat/jauh menjelaskan perjalanan | Pilih satu hero yang kekal, path SVG dan kamera world-space; lapisan jauh/dekat bergerak berbeza. Lukis persekitaran dan laluan berperingkat |
| Jake & the Taycan / `jake-taycan-bricks-v1.mp4` | 18.10s, 720×720 | Dari papak/jubin ke bangunan dan kereta; pandangan tinggi beralih ke hampir aras kereta; watak/kereta beraksi | Pecahkan binaan kepada subassembly, stagger mengikut struktur, kemudian kamera menuju hero. Gunakan 2.5D jika tiada model/runtime 3D; label dengan tepat |
| Storyboard first / `launch-storyboard-first-v1.mp4` | 57.051s, 1280×720 | Huruf hero sangat besar; kad kaca dan preview; UI/editor sebenar; label, path dan maskot; babak produk bersudut | Tulis beat masalah → bina → tunjuk hasil. Gunakan DOM/SVG berasingan untuk kad, label, cursor dan skrin; perspektif pada wrapper, teks tidak terlalu senget |
| It’s just HTML / `just-html-v1.mp4` | 54.57s, 1280×720 | Logo berdepth, partikel berpusar, code bertulis/beranotasi bersebelahan output, grid kemampuan, penutup | Untuk tutorial, tunjuk kod dan perubahan output berkait; anotasi pada satu baris penting. Partikel/shader ialah pilihan berasingan yang perlu readiness/seek proof |
| Wordmark / `wordmark-sting-v1.mp4` | 5.00s, 720×720 | Wordmark kecil, garis bawah, huruf tercerai dan melengkung kembali bersama aksen hijau | Bina huruf Latin berasingan pada path; arahkan peleraian → pemasangan → hold logo. Jangan pecahkan huruf Arab atau menyalin wordmark sumber |
| How do cameras focus / `real-ui-google-search-v1.mp4` | 8.00s, 1280×720 | Ruang carian sebenar, query ditaip bertahap; framing mendekat kepada medan aktif dan butiran skrin | Gunakan tangkapan sumber sah, animasi pembesaran pada wrapper dan cue typing deterministik. Label replika sebagai ilustrasi jika bukan rakaman sebenar |
| Background removal / `vfx-background-removal-launch-v1.mp4` | 42.98s, 1280×720 | Manusia cutout di depan pentas/teks kolaj; telefon, UI editing dan contoh foto bertukar; kedalaman melalui occlusion | Gunakan matte temporal/alfa sebenar, susunan latar → teks → manusia → HUD. Kekalkan suara/muka apabila menyunting footage; semak tepi matte dan z-order |
| The Frameys / `cartoon-frameys-launch-one-take-v1.mp4` | 43.513s, 1280×720 | Pentas/objek bercahaya, kad tajuk, video tersusun di ruang perspektif, grid, data dan pingat | Adaptasi pentas editorial dan kamera kad berlapis untuk showcase; jangan menganggap label “cartoon” membuktikan rig kartun. Jangan bawa tema/branding contoh |

Sampel temporal rapat diperiksa pada `k` 4.5–7.5s, kinetic type 6.1–9.1s, Studio launch 14–17s dan Taycan 0–4.5s, 16 frame setiap petikan. Gunakan petikan/transition yang relevan bagi kajian seterusnya; metadata, poster atau satu contact sheet tidak membuktikan kelancaran, audio sync atau kesetaraan source.

## 4. Bahasa gerakan untuk produksi

Gunakan panduan motion rasmi dan klip sebagai titik mula; angka berikut ialah **cadangan pengarahan**, bukan ukuran semua klip:

- **Berikan tugas kepada gerakan.** Prop dipasang, mesej merentas laluan, data berubah, kamera tiba pada subjek. Teks/UI yang selesai masuk berhenti untuk dibaca. Elakkan breathing/pulse/drift hiasan sebagai pengganti aksi.
- **Entrance bertindih.** Cuba gerak 0.3–0.6s, seterusnya bermula ketika sebelumnya 30–50% selesai; stagger perkataan sekitar 60–120ms. Ubah mengikut bacaan BM, mesej dan tempo. Binaan berurutan tidak bermaksud menunggu setiap prop berhenti sepenuhnya.
- **Padankan ease dengan peranan.** `expo.out`/`power4.out` untuk mendarat; `power2.inOut` untuk perjalanan kamera; `power3.in` untuk keluar/zoom-through. Overshoot terkawal untuk objek bermassa; jangan membuat nombor sebenar melampaui nilai atau UI/teks melantun tanpa sebab.
- **Variasikan mekanisme.** Mask per perkataan, ink/warna emphasis, wipe bar menjadi underline, whole-line blur reveal, rolling satu perkataan, stroke draw, crop/panel reveal. Gunakan stroke/shadow/highlight/glow/neon/2.5D mengikut palet dan fungsi; jangan meletakkan semua efek serentak pada setiap frasa.
- **Pertukaran layout ialah aksi.** Gerakkan teks/prop ke kiri, kanan, tengah, atas atau bawah untuk memberi ruang; pastikan anchor dan reading order jelas. Selepas berpindah, sediakan hold. Jangan menggerakkan semua elemen secara bebas ketika penonton perlu membaca.
- **Bawa satu hubungan melalui transisi.** Hero mengecil masuk ke kad seterusnya; kad membesar menjadi pentas; garis menjadi laluan; isi butang menjadi latar. Rancang posisi, arah dan halaju di kedua-dua sisi seam. Gunakan whip/morph/colour flood hanya apabila kandungan menyokongnya.
- **Kamera ada destinasi.** Ruang world lebih luas daripada frame, kamera pergi dari prop A ke B dengan jiran masih kelihatan; foreground occlusion dan kadar parallax menjelaskan depth. HUD/caption kekal screen-space.
- **Baca dahulu.** Anggar hold sekitar 0.5s + 0.3s/perkataan sebagai permulaan, kemudian semak pada saiz telefon dan bahasa sebenar. Rehat penutup sekitar 2s apabila sesuai. Kadar showreel 1–4s/idea tidak dipaksa pada pengajaran atau demo 7–10s yang masih beraksi.
- **Audio berasaskan event.** Cue sentuhan, whoosh, klik, paper/ASMR apabila aksi berlaku; beat muzik dikira daripada indeks beat untuk mengelakkan drift. Muzik/SFX tetap boleh digunakan tanpa VO. Jangan mendakwa didengar jika hanya analisis waveform.

## 5. Scene panjang dan gaya Salah Label

Jika pengguna menyebut **Salah Label** atau meminta satu scene panjang dengan banyak prop dan perkataan, gunakan ruang berterusan dengan beberapa beat. Contoh **olahan asal**, bukan tiruan timestamp sumber:

| Beat contoh | Perubahan keadaan | Fokus dan handoff |
|---|---|---|
| 0–2s | Hero dan hook ringkas masuk; prop sokongan dibina selepas hero | Satu frasa utama; elakkan textbox besar |
| 2–5s | Prop A dipecah/dipasang; perkataan baharu menggantikan perkataan lama dalam mask | Hero berganjak ke sisi untuk memberi ruang |
| 5–8s | Kamera menuju komponen; prop B masuk semasa A menyusut/beralih menjadi latar | Teks lama keluar; bukti/demonstrasi mengambil fokus |
| 8–11s | Hubungan sebab-akibat divisualkan dengan path, morph atau susunan semula | Campur flat SVG dan 2.5D/perspektif terpilih |
| 11–14s | Hasil terbina; satu prop menjadi jambatan ke beat/scene berikut | Frasa hasil mendarat dan sempat dibaca |

Ubah semua masa mengikut kandungan; scene lebih lama dibenarkan selagi ada perubahan bermakna. Gunakan group berlapis dengan ID/pivot, mask dan z-order. Nyatakan entrance, aksi semasa, exit, lokasi sebelum/selepas dan cue bunyi dalam manifest. Bina prop baharu sedikit demi sedikit; keluarkan atau kecilkan yang selesai tanpa membersihkan seluruh pentas setiap kali teks berubah. Kekalkan hero/ruang yang penonton boleh ikuti. Jika tiada VO, visual dan copy mesti menjelaskan cerita sendiri.

Untuk animasi vektor baharu, artwork utama mestilah SVG/DOM/Canvas yang elemennya benar-benar bergerak. Imej, tekstur, foto dan footage boleh menjadi aset jika relevan; satu poster penuh yang digerakkan kamera sahaja tidak memenuhi permintaan animasi objek. Jangan menganggap semua contoh HyperFrames menggunakan kaedah yang sama.

## 6. Pilih blok dan templat

Galeri menyenaraikan blok seperti `logo-outro`, `data-chart`, `flowchart`, `code-typing`, `mk-progress-stat`, `mk-callout-highlight`, `lt-dark-card` dan `cinematic-zoom`. Cari ID sebenar melalui `catalog --help`/`catalog` versi terpasang sebelum `add`. Registry online boleh berubah; ketiadaan blok mesti dilaporkan dan resipi custom dilabel **custom**, tanpa mendakwa blok asal telah digunakan.

Templat projek yang disenaraikan: `warm-grain`, `play-mode`, `swiss-grid`, `kinetic-type`, `decision-tree`, `product-promo`, `nyt-graph`, `vignelli`, `blank`. Gunakan templat hanya jika sesuai/diminta; projek custom boleh bermula daripada starter skill atau blank. Semak `init --help` sebelum `init my-video --example <name>`. Jangan menggantikan projek/checkpoint sedia ada atau membuat pemasangan besar yang tidak diperlukan.

Koleksi HyperFrames ini berasingan daripada Atlas/CFX pengguna. Jangan menambah ID Atlas palsu, menukar jumlah 922, atau mendakwa 100 kinetic typography pengguna sudah dipindahkan ke GSAP. Preset Python yang belum diport kekal dirender melalui implementasi asal sebagai layer video/alfa.

## 7. Semakan dan had bukti

1. Jalankan preflight sebenar; jangan muat turun semula jika runtime sah tersedia.
2. Bina/read font dan aset tempatan, kemudian lint dan check dengan sampel yang meliputi setiap scene/transisi.
3. Lihat snapshot terpilih, petikan gerak dan frame bersebelahan pada aksi sukar. Semak crop, perspective readability, occlusion, layer keluar, lokasi teks dan hold.
4. Uji seek maju, mundur, rawak, ulang dan cold load dengan callback disekat. Banding frame pada masa sama; jangan gunakan jam dinding/ticker bebas, random tanpa seed atau DOM mutation dalam callback untuk state visual.
5. Render proof melalui **HyperFrames sebenar**, bukan FFmpeg slideshow; ffprobe dan decode penuh output. Semak MP4 akhir dan audio mengikut keupayaan sebenar. `check` lulus tidak menjamin cerita atau estetika.
6. Sebelum sambung render panjang, semak PID/log/checkpoint/output. Pantau proses aktif dan guna master/segmen sah; jangan memulakan producer pendua.
7. Kekalkan Python/FFmpeg untuk suntingan footage, Whisper, matte, mixing dan backend Atlas. Jangan memaksa semua jenis kerja berpindah ke HTML atau menukar projek pengguna yang sudah stabil.

Simpan versi dan keputusan ujian projek yang benar-benar dijalankan. Jangan mengiklankan pemasangan Gemini, PixiJS/Three.js, shader, matting atau model tertentu sebagai siap hanya kerana demo HTML asas berjaya.
