# Indeks 185 preset panduan daripada empat sumber

**Status 7 Oktober 2026:** 185 ID kini mempunyai demo adaptasi asal yang boleh dirender dalam `guide_a.py`–`guide_d.py`. Registry ialah **322 = 137 preset asal + 185 demo panduan**. Kesemua 322 preview MP4 dihasilkan pada 960×540/30fps dan lulus probe metadata serta penyahkodan penuh. Demo baharu berasaskan nama dan deskripsi indeks ini, bukan sumber terperinci yang diimport, enjin pihak ketiga dipasang atau reproduksi implementasi asal yang disahkan.

## Cara memilih dan merender

- Pilih ID mengikut shot, mesej dan aset. Periksa `render.py --list` dan sumber modul bagi parameter yang benar-benar tersedia.
- Gunakan `python render.py --preset PV128 --clean --output preview.mp4` atau konfigurasi JSON. PL/PV lalai enam saat, MS 12 saat, AD 15 saat; perubahan duration meretime scene penuh.
- MS ialah contoh terpilih untuk pek, bukan semua 53 kemahiran sumber. AD ialah aliran pendek tanpa audio, menggunakan produk dan testimoni fiksyen. PV ialah 152 demo satu per kad, bukan semua 209 variasi. Shot 3D menggunakan adaptasi 2.5D.
- Palette, text, subtitle dan beberapa parameter khusus boleh diubah; sesetengah label/demo props sengaja tetap. Caption belum sync suara, waveform ialah ilustrasi dan layout Arab/Jawi/portrait belum diuji. Sesuaikan dan QA untuk bahan projek sebenar.
- Kekalkan potongan terus sebagai lalai; keluarga transition hanya apabila diminta. Nisbah asal aset pengguna dan ruang caption mesti disemak dalam komposisi produksi.
- Katalog: https://motion-preset-atlas.akramania.chatgpt.site. Preview senyap, MP4 dan konfigurasi boleh muat turun. Perubahan konfigurasi dalam katalog tidak mengubah video preview secara langsung.

## MS01–MS16: keluarga arahan motion

Sumber: [iart-ai/motion-skills](https://github.com/iart-ai/motion-skills), semakan `91834c6`. Hab menyenaraikan **16 pek** yang mengandungi **53 kemahiran**. Setiap MS di bawah ialah satu pintu pemilihan pek, bukan salinan semua kemahiran dalam pek.

| ID | Pek dan deskripsi | Aset sesuai | Video sesuai |
|---|---|---|---|
| MS01 | [tiktok-video-skills](https://github.com/iart-ai/tiktok-video-skills) — Video menegak dengan hook, rentak dan ruang selamat skrin telefon | Klip menegak, hook, audio | Reels/TikTok/Shorts |
| MS02 | [text-message-video-skills](https://github.com/iart-ai/text-message-video-skills) — Cerita menerusi mesej dan respons berturutan | Skrip chat, avatar, notifikasi | Cerita chat |
| MS03 | [youtube-video-skills](https://github.com/iart-ai/youtube-video-skills) — Segmen YouTube, podcast dan potongan panjang kepada klip | Rakaman, audio, petikan | YouTube/podcast |
| MS04 | [ecommerce-video-skills](https://github.com/iart-ai/ecommerce-video-skills) — Paparan produk, ciri, harga dan bukti visual | Foto produk, harga, ulasan | Iklan e-dagang |
| MS05 | [ad-video-skills](https://github.com/iart-ai/ad-video-skills) — Varian iklan, filem pelancaran dan testimoni | Brand kit, CSV, ulasan | Iklan A/B |
| MS06 | [data-animation-skills](https://github.com/iart-ai/data-animation-skills) — Carta, angka dan naratif data yang tepat | CSV, metrik, label | Laporan/infografik |
| MS07 | [explainer-video-skills](https://github.com/iart-ai/explainer-video-skills) — Urutan penerangan yang dibina mengikut konsep | Skrip, ikon, rajah | Explainer/pendidikan |
| MS08 | [map-animation-skills](https://github.com/iart-ai/map-animation-skills) — Peta editorial dan perjalanan lokasi | Peta, geodata, lokasi | Geografi/dokumentari |
| MS09 | [web-animation-skills](https://github.com/iart-ai/web-animation-skills) — Gerak laman web dan mikrointeraksi | UI web, SVG, komponen | Demo laman web |
| MS10 | [motion-design-skills](https://github.com/iart-ai/motion-design-skills) — Gerak jenama, logo, komposisi dan kesan visual | Logo, tipografi, bentuk | Identiti/promosi |
| MS11 | [kinetic-typography-skills](https://github.com/iart-ai/kinetic-typography-skills) — Tipografi kinetik berasaskan masa dan hierarki | Skrip, tajuk, voice-over | Hook/caption |
| MS12 | [freelance-motion-skills](https://github.com/iart-ai/freelance-motion-skills) — Brief, semakan dan penyerahan kerja klien | Brief, brand kit, aset klien | Produksi komersial |
| MS13 | [webgl-animation-skills](https://github.com/iart-ai/webgl-animation-skills) — Adegan 3D/WebGL dengan kamera dan shader apabila runtime ada | Model 3D, tekstur | Hero teknologi |
| MS14 | [manim-skills](https://github.com/iart-ai/manim-skills) — Animasi langkah matematik dan visual pembuktian | Formula, graf, rajah | Pendidikan matematik |
| MS15 | [generative-illustration-skills](https://github.com/iart-ai/generative-illustration-skills) — Ilustrasi terjana kod dengan variasi gerak | Palet, bentuk, seed | Visual abstrak |
| MS16 | [javascript-animation-skills](https://github.com/iart-ai/javascript-animation-skills) — Animasi dilukis bingkai demi bingkai dengan JavaScript | Skrip, bentuk kod | Cerita animasi asli |

## PL01–PL14: shot pelancaran produk

Sumber: [product-launch-motion](https://github.com/AbubakrChan/product-launch-motion/blob/main/references/09-shot-catalog.md), semakan `951d614`. Ini **binaan shot dan fungsi naratif**, bukan layout tetap. Pilih satu dakwaan utama bagi setiap shot; ikat pendedahan visual kepada kata narasi sebenar jika audio tersedia.

| ID | Shot dan deskripsi | Aset sesuai | Video sesuai |
|---|---|---|---|
| PL01 | Kinetic type beats — Frasa utama tiba tepat pada kata narasi | Tajuk, VO | Hook pelancaran |
| PL02 | Crowding problem — Objek memenuhi ruang untuk menunjukkan masalah | UI lama, banyak tugas | Masalah pengguna |
| PL03 | Held thesis — Satu pernyataan dikekalkan agar jelas dibaca | Satu janji produk | Tesis jenama |
| PL04 | Prompt / composer — Input dimasukkan ke medan dan mencetus respons | UI input, teks prompt | Demo AI |
| PL05 | Results surface — Hasil produk tersingkap selepas input | Tangkap layar hasil | Bukti demo |
| PL06 | Two-pane workspace — Dua panel kerja menunjukkan hubungan input dan output | UI dua panel | Produktiviti SaaS |
| PL07 | Pipeline / status tracker — Langkah dan status berubah secara berurutan | Status, langkah proses | Aliran kerja |
| PL08 | Hero stat count-up — Angka utama meningkat tepat kepada nilai sah | Data/angka sebenar | Bukti prestasi |
| PL09 | Testimonial with a face — Petikan disanding dengan orang sebenar | Foto pelanggan, ulasan | Bukti sosial |
| PL10 | Comparison columns — Dua pilihan dibanding dengan hierarki jelas | Data perbandingan | Sebelum/selepas |
| PL11 | End card / CTA lockup — Jenama dan ajakan tindakan dikunci untuk bacaan | Logo, URL, CTA | Penutup iklan |
| PL12 | Hardware hero — Produk fizikal menjadi fokus dengan gerak kamera | Foto/imej produk | Pelancaran perkakasan |
| PL13 | Terminal / dev-tool shot — Perintah atau respons terminal dipaparkan dengan jelas | Teks kod, terminal | Produk pembangun |
| PL14 | Map and chart reveal — Lokasi atau carta dibuka mengikut makna narasi | Peta, carta, data | Cakupan/data |

## PV001–PV152: kad shot produk

Sumber: [ai-product-video](https://github.com/dlazy-ai/ai-product-video/tree/main/references/shots), semakan `55501b4`. Repositori menyatakan **152 kad / 209 variasi**; indeks ini memetakan **152 kad** satu persatu, bukan 209 variasi sebagai ID berasingan. Klik nama kad untuk butir timing, mekanisme, parameter dan perangkap sumber. Lajur aset/video dipetakan mengikut keluarga kad sebagai panduan awal; semak butir kad sebelum melaksanakannya. Kad berkategori `transition` bukan pilihan lalai untuk pengguna ini.

| ID | Kad dan deskripsi ringkas | Aset sesuai | Video sesuai |
|---|---|---|---|
| PV001 | [basic-3d-scene](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/basic-3d-scene.md) — Gerakan kamera/ruang: basic 3d scene | Mockup, UI, imej berlapis | Promo produk |
| PV002 | [crash-zoom-punch](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/crash-zoom-punch.md) — Gerakan kamera/ruang: crash zoom punch | Mockup, UI, imej berlapis | Promo produk |
| PV003 | [cursor-flyover](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/cursor-flyover.md) — Gerakan kamera/ruang: cursor flyover | Mockup, UI, imej berlapis | Promo produk |
| PV004 | [depth-layer-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/depth-layer-moves.md) — Gerakan kamera/ruang: depth layer moves | Mockup, UI, imej berlapis | Promo produk |
| PV005 | [graze-face-tour](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/graze-face-tour.md) — Gerakan kamera/ruang: graze face tour | Mockup, UI, imej berlapis | Promo produk |
| PV006 | [overhead-camera-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/overhead-camera-moves.md) — Gerakan kamera/ruang: overhead camera moves | Mockup, UI, imej berlapis | Promo produk |
| PV007 | [space-camera-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/space-camera-moves.md) — Gerakan kamera/ruang: space camera moves | Mockup, UI, imej berlapis | Promo produk |
| PV008 | [steep-tilt-glide](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/steep-tilt-glide.md) — Gerakan kamera/ruang: steep tilt glide | Mockup, UI, imej berlapis | Promo produk |
| PV009 | [tension-camera-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/tension-camera-moves.md) — Gerakan kamera/ruang: tension camera moves | Mockup, UI, imej berlapis | Promo produk |
| PV010 | [terminal-3d](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/camera/terminal-3d.md) — Gerakan kamera/ruang: terminal 3d | Mockup, UI, imej berlapis | Promo produk |
| PV011 | [avatar-grid-radial-build-colorize](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/avatar-grid-radial-build-colorize.md) — Pendedahan angka, carta atau perbandingan: avatar grid radial build colorize | Data sah, carta, metrik | Explainer data |
| PV012 | [before-after-slider-scrub](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/before-after-slider-scrub.md) — Pendedahan angka, carta atau perbandingan: before after slider scrub | Data sah, carta, metrik | Explainer data |
| PV013 | [chart-live-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/chart-live-moves.md) — Pendedahan angka, carta atau perbandingan: chart live moves | Data sah, carta, metrik | Explainer data |
| PV014 | [counter-confetti](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/counter-confetti.md) — Pendedahan angka, carta atau perbandingan: counter confetti | Data sah, carta, metrik | Explainer data |
| PV015 | [gauge-readout-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/gauge-readout-moves.md) — Pendedahan angka, carta atau perbandingan: gauge readout moves | Data sah, carta, metrik | Explainer data |
| PV016 | [hatch-depth](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/hatch-depth.md) — Pendedahan angka, carta atau perbandingan: hatch depth | Data sah, carta, metrik | Explainer data |
| PV017 | [odometer-digit-roll](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/odometer-digit-roll.md) — Pendedahan angka, carta atau perbandingan: odometer digit roll | Data sah, carta, metrik | Explainer data |
| PV018 | [particle-celebrate-hits](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/particle-celebrate-hits.md) — Pendedahan angka, carta atau perbandingan: particle celebrate hits | Data sah, carta, metrik | Explainer data |
| PV019 | [particle-sand-fill](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/particle-sand-fill.md) — Pendedahan angka, carta atau perbandingan: particle sand fill | Data sah, carta, metrik | Explainer data |
| PV020 | [scroll-brake-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/scroll-brake-moves.md) — Pendedahan angka, carta atau perbandingan: scroll brake moves | Data sah, carta, metrik | Explainer data |
| PV021 | [timeline-travel](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/data/timeline-travel.md) — Pendedahan angka, carta atau perbandingan: timeline travel | Data sah, carta, metrik | Explainer data |
| PV022 | [assemble-then-type-flyin](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/assemble-then-type-flyin.md) — Kesan visual untuk fokus dan penekanan: assemble then type flyin | Logo, UI, bentuk grafik | Promo kreatif |
| PV023 | [aurora-bloom-bg-flip](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/aurora-bloom-bg-flip.md) — Kesan visual untuk fokus dan penekanan: aurora bloom bg flip | Logo, UI, bentuk grafik | Promo kreatif |
| PV024 | [brand-frame-snap](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/brand-frame-snap.md) — Kesan visual untuk fokus dan penekanan: brand frame snap | Logo, UI, bentuk grafik | Promo kreatif |
| PV025 | [dashboard-glow-highlight-pill](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/dashboard-glow-highlight-pill.md) — Kesan visual untuk fokus dan penekanan: dashboard glow highlight pill | Logo, UI, bentuk grafik | Promo kreatif |
| PV026 | [fui-hud-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/fui-hud-moves.md) — Kesan visual untuk fokus dan penekanan: fui hud moves | Logo, UI, bentuk grafik | Promo kreatif |
| PV027 | [glow-flyline-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/glow-flyline-moves.md) — Kesan visual untuk fokus dan penekanan: glow flyline moves | Logo, UI, bentuk grafik | Promo kreatif |
| PV028 | [icon-performance-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/icon-performance-moves.md) — Kesan visual untuk fokus dan penekanan: icon performance moves | Logo, UI, bentuk grafik | Promo kreatif |
| PV029 | [impact-feedback](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/impact-feedback.md) — Kesan visual untuk fokus dan penekanan: impact feedback | Logo, UI, bentuk grafik | Promo kreatif |
| PV030 | [light-play-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/light-play-moves.md) — Kesan visual untuk fokus dan penekanan: light play moves | Logo, UI, bentuk grafik | Promo kreatif |
| PV031 | [line-boil](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/line-boil.md) — Kesan visual untuk fokus dan penekanan: line boil | Logo, UI, bentuk grafik | Promo kreatif |
| PV032 | [radial-ripple-phone-chips](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/radial-ripple-phone-chips.md) — Kesan visual untuk fokus dan penekanan: radial ripple phone chips | Logo, UI, bentuk grafik | Promo kreatif |
| PV033 | [riso-print-hits](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/riso-print-hits.md) — Kesan visual untuk fokus dan penekanan: riso print hits | Logo, UI, bentuk grafik | Promo kreatif |
| PV034 | [scan-bracket-sweep](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/scan-bracket-sweep.md) — Kesan visual untuk fokus dan penekanan: scan bracket sweep | Logo, UI, bentuk grafik | Promo kreatif |
| PV035 | [scanline-annotate-focus](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/scanline-annotate-focus.md) — Kesan visual untuk fokus dan penekanan: scanline annotate focus | Logo, UI, bentuk grafik | Promo kreatif |
| PV036 | [scanline-assemble-flyin](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/scanline-assemble-flyin.md) — Kesan visual untuk fokus dan penekanan: scanline assemble flyin | Logo, UI, bentuk grafik | Promo kreatif |
| PV037 | [slam-entrance-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/slam-entrance-moves.md) — Kesan visual untuk fokus dan penekanan: slam entrance moves | Logo, UI, bentuk grafik | Promo kreatif |
| PV038 | [spotlight-sweep-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/effects/spotlight-sweep-moves.md) — Kesan visual untuk fokus dan penekanan: spotlight sweep moves | Logo, UI, bentuk grafik | Promo kreatif |
| PV039 | [ai-stream-response](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/ai-stream-response.md) — Interaksi pengguna dan keadaan UI: ai stream response | Tangkap layar, kursor, input | Demo SaaS |
| PV040 | [autolayout-gap-dial](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/autolayout-gap-dial.md) — Interaksi pengguna dan keadaan UI: autolayout gap dial | Tangkap layar, kursor, input | Demo SaaS |
| PV041 | [canvas-materialize-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/canvas-materialize-moves.md) — Interaksi pengguna dan keadaan UI: canvas materialize moves | Tangkap layar, kursor, input | Demo SaaS |
| PV042 | [chip-grid-single-select-blackout](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/chip-grid-single-select-blackout.md) — Interaksi pengguna dan keadaan UI: chip grid single select blackout | Tangkap layar, kursor, input | Demo SaaS |
| PV043 | [chip-lift-to-user-pill](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/chip-lift-to-user-pill.md) — Interaksi pengguna dan keadaan UI: chip lift to user pill | Tangkap layar, kursor, input | Demo SaaS |
| PV044 | [collab-cursor-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/collab-cursor-moves.md) — Interaksi pengguna dan keadaan UI: collab cursor moves | Tangkap layar, kursor, input | Demo SaaS |
| PV045 | [command-palette-summon](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/command-palette-summon.md) — Interaksi pengguna dan keadaan UI: command palette summon | Tangkap layar, kursor, input | Demo SaaS |
| PV046 | [glass-pill-dictation-typing](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/glass-pill-dictation-typing.md) — Interaksi pengguna dan keadaan UI: glass pill dictation typing | Tangkap layar, kursor, input | Demo SaaS |
| PV047 | [hashtag-to-pill-materialize](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/hashtag-to-pill-materialize.md) — Interaksi pengguna dan keadaan UI: hashtag to pill materialize | Tangkap layar, kursor, input | Demo SaaS |
| PV048 | [input-trigger-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/input-trigger-moves.md) — Interaksi pengguna dan keadaan UI: input trigger moves | Tangkap layar, kursor, input | Demo SaaS |
| PV049 | [picker-carousel-feature-cycle](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/picker-carousel-feature-cycle.md) — Interaksi pengguna dan keadaan UI: picker carousel feature cycle | Tangkap layar, kursor, input | Demo SaaS |
| PV050 | [segmented-thumb-hero](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/segmented-thumb-hero.md) — Interaksi pengguna dan keadaan UI: segmented thumb hero | Tangkap layar, kursor, input | Demo SaaS |
| PV051 | [theme-switch-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/theme-switch-moves.md) — Interaksi pengguna dan keadaan UI: theme switch moves | Tangkap layar, kursor, input | Demo SaaS |
| PV052 | [type-and-filter](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/type-and-filter.md) — Interaksi pengguna dan keadaan UI: type and filter | Tangkap layar, kursor, input | Demo SaaS |
| PV053 | [voice-waveform-live](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/interaction/voice-waveform-live.md) — Interaksi pengguna dan keadaan UI: voice waveform live | Tangkap layar, kursor, input | Demo SaaS |
| PV054 | [brand-ink-open](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/brand-ink-open.md) — Bukaan yang memperkenalkan jenama atau mesej: brand ink open | Logo, produk, tajuk | Pembukaan pelancaran |
| PV055 | [crane-rise-reveal](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/crane-rise-reveal.md) — Bukaan yang memperkenalkan jenama atau mesej: crane rise reveal | Logo, produk, tajuk | Pembukaan pelancaran |
| PV056 | [dataviz-landscape-open](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/dataviz-landscape-open.md) — Bukaan yang memperkenalkan jenama atau mesej: dataviz landscape open | Logo, produk, tajuk | Pembukaan pelancaran |
| PV057 | [fracture](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/fracture.md) — Bukaan yang memperkenalkan jenama atau mesej: fracture | Logo, produk, tajuk | Pembukaan pelancaran |
| PV058 | [icon-field-colorize](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/icon-field-colorize.md) — Bukaan yang memperkenalkan jenama atau mesej: icon field colorize | Logo, produk, tajuk | Pembukaan pelancaran |
| PV059 | [letterspace-materialize](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/letterspace-materialize.md) — Bukaan yang memperkenalkan jenama atau mesej: letterspace materialize | Logo, produk, tajuk | Pembukaan pelancaran |
| PV060 | [magician-card-flourish](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/magician-card-flourish.md) — Bukaan yang memperkenalkan jenama atau mesej: magician card flourish | Logo, produk, tajuk | Pembukaan pelancaran |
| PV061 | [spotlight-hero-card](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/spotlight-hero-card.md) — Bukaan yang memperkenalkan jenama atau mesej: spotlight hero card | Logo, produk, tajuk | Pembukaan pelancaran |
| PV062 | [stroke-segment-build](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/stroke-segment-build.md) — Bukaan yang memperkenalkan jenama atau mesej: stroke segment build | Logo, produk, tajuk | Pembukaan pelancaran |
| PV063 | [text-as-mask](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/opening/text-as-mask.md) — Bukaan yang memperkenalkan jenama atau mesej: text as mask | Logo, produk, tajuk | Pembukaan pelancaran |
| PV064 | [edit-hook-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/outro/edit-hook-moves.md) — Penutup yang mengunci mesej akhir: edit hook moves | Logo, URL, CTA | Penutup promo |
| PV065 | [grain-dissolve](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/outro/grain-dissolve.md) — Penutup yang mengunci mesej akhir: grain dissolve | Logo, URL, CTA | Penutup promo |
| PV066 | [logo-shrink-wordmark-lockup](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/outro/logo-shrink-wordmark-lockup.md) — Penutup yang mengunci mesej akhir: logo shrink wordmark lockup | Logo, URL, CTA | Penutup promo |
| PV067 | [neon-triple-marquee](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/outro/neon-triple-marquee.md) — Penutup yang mengunci mesej akhir: neon triple marquee | Logo, URL, CTA | Penutup promo |
| PV068 | [outro-group-photo-launch](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/outro/outro-group-photo-launch.md) — Penutup yang mengunci mesej akhir: outro group photo launch | Logo, URL, CTA | Penutup promo |
| PV069 | [ui-strip-away-outro](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/outro/ui-strip-away-outro.md) — Penutup yang mengunci mesej akhir: ui strip away outro | Logo, URL, CTA | Penutup promo |
| PV070 | [ui-to-brand-morph](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/outro/ui-to-brand-morph.md) — Penutup yang mengunci mesej akhir: ui to brand morph | Logo, URL, CTA | Penutup promo |
| PV071 | [beat-cut-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/beat-cut-moves.md) — Rentak montaj dan perubahan fokus: beat cut moves | Beberapa klip/gambar, muzik | Teaser/promo |
| PV072 | [beat-step-list-theme-cycle](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/beat-step-list-theme-cycle.md) — Rentak montaj dan perubahan fokus: beat step list theme cycle | Beberapa klip/gambar, muzik | Teaser/promo |
| PV073 | [montage-rhythm-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/montage-rhythm-moves.md) — Rentak montaj dan perubahan fokus: montage rhythm moves | Beberapa klip/gambar, muzik | Teaser/promo |
| PV074 | [panel-grid-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/panel-grid-moves.md) — Rentak montaj dan perubahan fokus: panel grid moves | Beberapa klip/gambar, muzik | Teaser/promo |
| PV075 | [quad-split-parallel-scenes](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/quad-split-parallel-scenes.md) — Rentak montaj dan perubahan fokus: quad split parallel scenes | Beberapa klip/gambar, muzik | Teaser/promo |
| PV076 | [rhythm-interrupt-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/rhythm-interrupt-moves.md) — Rentak montaj dan perubahan fokus: rhythm interrupt moves | Beberapa klip/gambar, muzik | Teaser/promo |
| PV077 | [sakuga-timing-shift](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/sakuga-timing-shift.md) — Rentak montaj dan perubahan fokus: sakuga timing shift | Beberapa klip/gambar, muzik | Teaser/promo |
| PV078 | [smear-multiples](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/smear-multiples.md) — Rentak montaj dan perubahan fokus: smear multiples | Beberapa klip/gambar, muzik | Teaser/promo |
| PV079 | [spectrum-morph-ui](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/spectrum-morph-ui.md) — Rentak montaj dan perubahan fokus: spectrum morph ui | Beberapa klip/gambar, muzik | Teaser/promo |
| PV080 | [speed-ramp-freeze](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/speed-ramp-freeze.md) — Rentak montaj dan perubahan fokus: speed ramp freeze | Beberapa klip/gambar, muzik | Teaser/promo |
| PV081 | [trailer-grammar-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/rhythm/trailer-grammar-moves.md) — Rentak montaj dan perubahan fokus: trailer grammar moves | Beberapa klip/gambar, muzik | Teaser/promo |
| PV082 | [bottom-push-stack-wipe](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/bottom-push-stack-wipe.md) — Peralihan antara dua shot: bottom push stack wipe | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV083 | [bubble-swarm-takeover](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/bubble-swarm-takeover.md) — Peralihan antara dua shot: bubble swarm takeover | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV084 | [card-flip-reveal](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/card-flip-reveal.md) — Peralihan antara dua shot: card flip reveal | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV085 | [card-flock-tumble](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/card-flock-tumble.md) — Peralihan antara dua shot: card flock tumble | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV086 | [circle-match-iris](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/circle-match-iris.md) — Peralihan antara dua shot: circle match iris | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV087 | [color-block-step-wipe](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/color-block-step-wipe.md) — Peralihan antara dua shot: color block step wipe | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV088 | [cube-navigation](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/cube-navigation.md) — Peralihan antara dua shot: cube navigation | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV089 | [gradient-transition](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/gradient-transition.md) — Peralihan antara dua shot: gradient transition | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV090 | [line-carry-transition](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/line-carry-transition.md) — Peralihan antara dua shot: line carry transition | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV091 | [mosaic-reframe](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/mosaic-reframe.md) — Peralihan antara dua shot: mosaic reframe | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV092 | [page-turn-transitions](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/page-turn-transitions.md) — Peralihan antara dua shot: page turn transitions | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV093 | [paper-plane-messenger](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/paper-plane-messenger.md) — Peralihan antara dua shot: paper plane messenger | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV094 | [print-texture-transitions](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/print-texture-transitions.md) — Peralihan antara dua shot: print texture transitions | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV095 | [shot-transitions](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/shot-transitions.md) — Peralihan antara dua shot: shot transitions | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV096 | [tear-streak-transitions](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/tear-streak-transitions.md) — Peralihan antara dua shot: tear streak transitions | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV097 | [transition-hidden-cut](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/transition-hidden-cut.md) — Peralihan antara dua shot: transition hidden cut | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV098 | [transition-travel](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/transition-travel.md) — Peralihan antara dua shot: transition travel | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV099 | [white-flash-logo-simplify-cut](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/white-flash-logo-simplify-cut.md) — Peralihan antara dua shot: white flash logo simplify cut | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV100 | [wipe-transitions](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/transition/wipe-transitions.md) — Peralihan antara dua shot: wipe transitions | Dua adegan, warna jenama | Montaj; guna hanya jika diminta |
| PV101 | [blur-slide](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/blur-slide.md) — Gerak kata, huruf atau ayat: blur slide | Tajuk, skrip, VO | Hook/kinetic typography |
| PV102 | [brace-expand](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/brace-expand.md) — Gerak kata, huruf atau ayat: brace expand | Tajuk, skrip, VO | Hook/kinetic typography |
| PV103 | [cel-flash-stomp](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/cel-flash-stomp.md) — Gerak kata, huruf atau ayat: cel flash stomp | Tajuk, skrip, VO | Hook/kinetic typography |
| PV104 | [countdown-arc-scatter](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/countdown-arc-scatter.md) — Gerak kata, huruf atau ayat: countdown arc scatter | Tajuk, skrip, VO | Hook/kinetic typography |
| PV105 | [document-typewriter-reveal](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/document-typewriter-reveal.md) — Gerak kata, huruf atau ayat: document typewriter reveal | Tajuk, skrip, VO | Hook/kinetic typography |
| PV106 | [flying-words](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/flying-words.md) — Gerak kata, huruf atau ayat: flying words | Tajuk, skrip, VO | Hook/kinetic typography |
| PV107 | [glitch-cycle](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/glitch-cycle.md) — Gerak kata, huruf atau ayat: glitch cycle | Tajuk, skrip, VO | Hook/kinetic typography |
| PV108 | [gradient-word-sweep](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/gradient-word-sweep.md) — Gerak kata, huruf atau ayat: gradient word sweep | Tajuk, skrip, VO | Hook/kinetic typography |
| PV109 | [marker-underline-title](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/marker-underline-title.md) — Gerak kata, huruf atau ayat: marker underline title | Tajuk, skrip, VO | Hook/kinetic typography |
| PV110 | [outline-word-fill](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/outline-word-fill.md) — Gerak kata, huruf atau ayat: outline word fill | Tajuk, skrip, VO | Hook/kinetic typography |
| PV111 | [paper-title-card](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/paper-title-card.md) — Gerak kata, huruf atau ayat: paper title card | Tajuk, skrip, VO | Hook/kinetic typography |
| PV112 | [pill-chip-slot-cycle-handled](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/pill-chip-slot-cycle-handled.md) — Gerak kata, huruf atau ayat: pill chip slot cycle handled | Tajuk, skrip, VO | Hook/kinetic typography |
| PV113 | [pill-slot-cycle](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/pill-slot-cycle.md) — Gerak kata, huruf atau ayat: pill slot cycle | Tajuk, skrip, VO | Hook/kinetic typography |
| PV114 | [scramble](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/scramble.md) — Gerak kata, huruf atau ayat: scramble | Tajuk, skrip, VO | Hook/kinetic typography |
| PV115 | [split-flap-title](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/split-flap-title.md) — Gerak kata, huruf atau ayat: split flap title | Tajuk, skrip, VO | Hook/kinetic typography |
| PV116 | [text-column-converge](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/text-column-converge.md) — Gerak kata, huruf atau ayat: text column converge | Tajuk, skrip, VO | Hook/kinetic typography |
| PV117 | [title-demote-to-label](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/title-demote-to-label.md) — Gerak kata, huruf atau ayat: title demote to label | Tajuk, skrip, VO | Hook/kinetic typography |
| PV118 | [type-assembly-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/type-assembly-moves.md) — Gerak kata, huruf atau ayat: type assembly moves | Tajuk, skrip, VO | Hook/kinetic typography |
| PV119 | [type-entrance-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/type-entrance-moves.md) — Gerak kata, huruf atau ayat: type entrance moves | Tajuk, skrip, VO | Hook/kinetic typography |
| PV120 | [type-rhythm-sync](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/type-rhythm-sync.md) — Gerak kata, huruf atau ayat: type rhythm sync | Tajuk, skrip, VO | Hook/kinetic typography |
| PV121 | [typewriter-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/typewriter-moves.md) — Gerak kata, huruf atau ayat: typewriter moves | Tajuk, skrip, VO | Hook/kinetic typography |
| PV122 | [typing-code-block](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/typing-code-block.md) — Gerak kata, huruf atau ayat: typing code block | Tajuk, skrip, VO | Hook/kinetic typography |
| PV123 | [vertical-word-roll-blur-cycle](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/vertical-word-roll-blur-cycle.md) — Gerak kata, huruf atau ayat: vertical word roll blur cycle | Tajuk, skrip, VO | Hook/kinetic typography |
| PV124 | [word-relay-filmstrip](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/word-relay-filmstrip.md) — Gerak kata, huruf atau ayat: word relay filmstrip | Tajuk, skrip, VO | Hook/kinetic typography |
| PV125 | [word-relay-geometry](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/typography/word-relay-geometry.md) — Gerak kata, huruf atau ayat: word relay geometry | Tajuk, skrip, VO | Hook/kinetic typography |
| PV126 | [avatar-bracket-carousel](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/avatar-bracket-carousel.md) — Kemasukan komponen dan susunan skrin: avatar bracket carousel | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV127 | [bezier-source-converge-merge](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/bezier-source-converge-merge.md) — Kemasukan komponen dan susunan skrin: bezier source converge merge | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV128 | [card-stack](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/card-stack.md) — Kemasukan komponen dan susunan skrin: card stack | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV129 | [carousel-3d](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/carousel-3d.md) — Kemasukan komponen dan susunan skrin: carousel 3d | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV130 | [cloner-depth-echo](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/cloner-depth-echo.md) — Kemasukan komponen dan susunan skrin: cloner depth echo | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV131 | [deck-deal-flyin](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/deck-deal-flyin.md) — Kemasukan komponen dan susunan skrin: deck deal flyin | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV132 | [doc-park-left-pill-deal](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/doc-park-left-pill-deal.md) — Kemasukan komponen dan susunan skrin: doc park left pill deal | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV133 | [draw-svg-trace](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/draw-svg-trace.md) — Kemasukan komponen dan susunan skrin: draw svg trace | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV134 | [element-body-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/element-body-moves.md) — Kemasukan komponen dan susunan skrin: element body moves | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV135 | [floating-glossy-label-pills](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/floating-glossy-label-pills.md) — Kemasukan komponen dan susunan skrin: floating glossy label pills | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV136 | [integration-hub-map](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/integration-hub-map.md) — Kemasukan komponen dan susunan skrin: integration hub map | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV137 | [list-reveal](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/list-reveal.md) — Kemasukan komponen dan susunan skrin: list reveal | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV138 | [list-stack-press](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/list-stack-press.md) — Kemasukan komponen dan susunan skrin: list stack press | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV139 | [morph-from-primitive](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/morph-from-primitive.md) — Kemasukan komponen dan susunan skrin: morph from primitive | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV140 | [neon-frame-forerun](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/neon-frame-forerun.md) — Kemasukan komponen dan susunan skrin: neon frame forerun | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV141 | [neon-frame-orbit-drop](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/neon-frame-orbit-drop.md) — Kemasukan komponen dan susunan skrin: neon frame orbit drop | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV142 | [page-waterfall-wall](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/page-waterfall-wall.md) — Kemasukan komponen dan susunan skrin: page waterfall wall | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV143 | [paper-craft-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/paper-craft-moves.md) — Kemasukan komponen dan susunan skrin: paper craft moves | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV144 | [product-card-progressive-assemble](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/product-card-progressive-assemble.md) — Kemasukan komponen dan susunan skrin: product card progressive assemble | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV145 | [radial-wave](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/radial-wave.md) — Kemasukan komponen dan susunan skrin: radial wave | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV146 | [research-card-stack-scroll](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/research-card-stack-scroll.md) — Kemasukan komponen dan susunan skrin: research card stack scroll | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV147 | [row-embed](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/row-embed.md) — Kemasukan komponen dan susunan skrin: row embed | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV148 | [runway-ground-skim](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/runway-ground-skim.md) — Kemasukan komponen dan susunan skrin: runway ground skim | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV149 | [skeleton-reveal](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/skeleton-reveal.md) — Kemasukan komponen dan susunan skrin: skeleton reveal | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV150 | [svg-shape-morph](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/svg-shape-morph.md) — Kemasukan komponen dan susunan skrin: svg shape morph | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV151 | [value-stagger-gradient](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/value-stagger-gradient.md) — Kemasukan komponen dan susunan skrin: value stagger gradient | UI, kad, ikon, tangkap layar | Demo aplikasi |
| PV152 | [wall-reveal-moves](https://github.com/dlazy-ai/ai-product-video/blob/main/references/shots/ui-entrance/wall-reveal-moves.md) — Kemasukan komponen dan susunan skrin: wall reveal moves | UI, kad, ikon, tangkap layar | Demo aplikasi |

## AD01–AD03: format video iklan

Sumber: [iart-ai/ad-video-skills](https://github.com/iart-ai/ad-video-skills), semakan `0de0f2a`. AD ialah rancangan video menyeluruh, bukan satu animasi lima saat.

| ID | Format dan deskripsi | Aset sesuai | Video sesuai |
|---|---|---|---|
| AD01 | [Ad creative variants](https://github.com/iart-ai/ad-video-skills/tree/main/skills/ad-creative-video) — Satu struktur iklan menghasilkan beberapa versi hook dan mesej | CSV mesej, brand kit, CTA | Ujian iklan A/B |
| AD02 | [Launch film](https://github.com/iart-ai/ad-video-skills/tree/main/skills/launch-video) — Hook, teaser, reveal, ciri dan CTA disusun kepada cerita pelancaran | Foto produk, UI, logo, muzik | Pelancaran produk |
| AD03 | [Testimonial quote](https://github.com/iart-ai/ad-video-skills/tree/main/skills/testimonial-video) — Petikan, frasa utama, skor dan identiti pemberi ulasan berurutan | Ulasan sah, avatar, skor | Bukti sosial |

## Nota sumber dan pemakaian

- Sumber asal ialah rujukan terbuka; olah komposisi sendiri mengikut produk dan aset pengguna. Jangan dakwa komponen, 3D, suara, muzik, CLI, dependensi atau rendering asal tersedia tanpa memasang dan mengujinya.
- `motion-skills` ialah hab pek kemahiran, jadi 16 MS ialah pintu pemilihan, bukan 16 motion tunggal. `product-launch-motion` memberi 14 binaan shot. `ad-video-skills` memberi tiga aliran video. `ai-product-video` memberi 152 kad shot dan 209 variasi dalam kad.
- Preset sedia ada boleh digunakan bersama resipi ini pada adegan berlainan; pemilihan gaya Learnfly untuk explainer/promosi tanpa gaya khusus masih terpakai.
