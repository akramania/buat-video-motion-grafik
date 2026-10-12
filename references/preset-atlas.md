# Preset Atlas: renderer boleh digunakan semula

## Kandungan

1. Skop dan fail
2. Pilihan genre dan ID
3. Render dan konfigurasi
4. Empat belas rujukan baharu
5. Had penggunaan produksi
6. Scene kompleks L01–L06
7. Text animation K01–K45
8. MotionPrompt MP01–MP48
9. Preset panduan MS/PL/PV/AD

## Jumlah semasa

Selepas pengembangan 11 Oktober 2026, registry mempunyai **842 preset**: 137 asal + 185 demo panduan + 120 EV + 400 PX. Tambahan 1,000 elemen SVG ialah aset vektor berasingan, bukan 1,000 preset animasi. Baca [PX400 dan SVG1000](premium-400-svg-1000.md) untuk modul, provenance dan penggunaan koleksi terkini. Jumlah lebih kecil di bawah merujuk peringkat sejarah kumpulan asal.

## 1. Skop dan fail

`assets/motion_presets/` ialah implementasi Python asli untuk 137 corak asal: 24 terdahulu, 14 tambahan, enam scene kompleks L01–L06, 45 text animation K01–K45 dan 48 preset MotionPrompt MP01–MP48. Ini komponen boleh dirender dan diubah melalui konfigurasi/sumber, bukan fail native After Effects, Premiere Pro atau DaVinci Resolve. Jangan menamakannya pemasangan `.aep`, `.mogrt`, `.prfpset` atau template Envato asal.

Tambahan **185 demo adaptasi panduan** daripada empat pustaka terbuka diterangkan dalam [indeks MS/PL/PV/AD](open-motion-185-guides.md). Selepas 7 Oktober 2026, `guide_a.py`–`guide_d.py` turut didaftarkan dalam registry; semua **322 entri** boleh dirender. Bezakan 137 preset asal daripada 185 interpretasi asal berdasarkan indeks: bukan implementasi sumber terperinci yang disahkan. MS ialah contoh pek, PL/PV ialah shot dan AD ialah aliran pendek.

- `render.py`: registry, config, overlay katalog, aliran frame kepada FFmpeg, eksport PNG/MP4/MOV.
- `build_atlas.py` dan `catalogue_template.html`: bina semua preview, konfigurasi, poster, HTML offline dan reel; gunakan `--skip-render` untuk memakai semula video/poster yang sudah lengkap dan merender fail yang belum ada. Padam media preset yang berubah sebelum membina semula kerana pilihan ini tidak mengesan perubahan kod secara automatik.
- `core.py`: kanvas 1280×720, palet, font, ukuran teks, lapisan, easing, mask, panel dan perspective warp.
- `ui.py`: U01–U04, N01–N04; `typography.py`: T01–T04, X01–X04, H01–H04; `carousels.py`: C01–C04.
- `new_a.py`: A01–A07; `new_b.py`: B01–B07. Setiap modul menyediakan `PRESETS` dan `render(pid,t,cfg)`.
- `long_a.py`: L01–L03; `long_b.py`: L04–L06; `long_scene_tools.py`: cue dan progress aksi setempat.
- `kinetic_a.py`: K01–K15; `kinetic_b.py`: K16–K30; `kinetic_c.py`: K31–K45. Metadata menyimpan mekanisme, sumber/timecode dan status pemerhatian/olahan.
- `guide_a.py`–`guide_c.py`: PV001–PV152; `guide_d.py`: MS01–MS16, PL01–PL14, AD01–AD03; `guide_index.json`: nama, rujukan dan kategori. Semua menggunakan clock normal 0–5, default 6/12/15 saat mengikut keluarga.
- `motionprompt.py`: MP01–MP48 dengan 48 fungsi render tersendiri, metadata sumber, imej pilihan dan input khusus.
- `fonts/`: empat font DejaVu serta lesen. Jangan memindahkan skrip tanpa direktori ini.

Kontrak imej modul ialah RGBA 1280×720. Modul lama, K01–K45 dan MP01–MP48 menerima masa reka bentuk `t` antara 0 hingga 5 saat. Modul L01–L06 dengan metadata `time_mode: seconds` menerima saat sebenar; fungsi awam `frame(pid,t,cfg)` menerima saat output dan melakukan dispatch yang sesuai. `render.py` membina `N=round(duration*fps)` frame pada indeks 0..N−1. Setiap frame dikira daripada masa; renderer tidak memperbanyak frame statik untuk mendakwa 60fps.

## 2. Pilihan genre dan ID

`genre` mengubah palet asas, bukan menggantikan semua artwork atau mereka bentuk semula preset. `genres` dalam metadata ialah cadangan kesesuaian; semua enam nilai genre diterima oleh konfigurasi.

| Nilai `genre` | Latar / aksen utama | Pilihan awal yang praktikal |
|---|---|---|
| `saas` | Navy `#0B1220` / mint `#71E8C4` | U01, U02, N03, A04; gunakan B04 untuk bukti angka |
| `education` | Krim `#F4F0E8` / biru `#2163DA` | T01, T04, A06, B06; utamakan masa bacaan |
| `creator` | Ungu gelap `#161222` / limau `#DEFF70` | H01, H02, A01, A02, B05 |
| `documentary` | Kertas `#E8E1D4` / terakota `#BD4C35` | A06, B01, B06, C04; gerakan lebih tenang |
| `corporate` | Navy `#101C33` / biru muda `#7AB5FF` | U04, T04, C03, B04, B07 |
| `promo` | Plum `#23112C` / jingga `#FF966B` | X01, X04, C01, A05, A07, B02 |

| Keluarga lama | ID dan corak yang dilaksanakan |
|---|---|
| Produk/UI | U01 logo→dashboard; U02 data dashboard; U03 ikon keluar telefon; U04 panel perspektif |
| Notifikasi | N01 susun semula kad; N02 kumpulan berlapis; N03 isi mesej berturutan; N04 notifikasi pada skrin telefon |
| Tipografi | T01 reveal perkataan bermask; T02 glyph ke baseline; T03 taip/padam/ganti; T04 frasa mengikut beat |
| Impak | X01 kata besar/echo; X02 wipe/underline; X03 outline→fill; X04 blur/pinggir warna/glow |
| Carousel | C01 fokus beralih; C02 kipas melengkung; C03 hero berkembang/kembali; C04 dua trek berulang |
| Hook/caption | H01 kata aktif; H02 penanda kata; H03 ikon menyokong hook; H04 counter dan punch |

Pilih satu gerakan utama setiap beat. Contoh susunan fungsi: A04 memperkenalkan soalan → U01/U02 menunjukkan produk → C03 memberi fokus → B04 menunjukkan metrik → X02 menutup dengan tindakan. Ini cadangan pemilihan; CLI sekarang merender satu preset setiap arahan, bukan penyunting timeline berbilang scene.

## 3. Render dan konfigurasi

Keperluan: Python 3.10+, Pillow, NumPy dan FFmpeg yang mempunyai encoder `libx264`. Dari direktori `assets/motion_presets/`, jalankan:

```bash
python build_atlas.py --output /path/projek/atlas --standalone --reel
python render.py --list
python render.py --preset C01 --output carousel.mp4 --clean
python render.py --config contoh.json --output hasil.mp4 --clean
python render.py --preset A06 --duration 8 --fps 60 --width 1920 --output nota.mp4 --clean
python render.py --preset C03 --frame 2.6 --output bingkai.png
python render.py --preset T01 --transparent --output title.mov
```

Pakej pengguna menyimpan skrip dalam `renderer/`; dari akar pakej, arahan sepadan ialah `python renderer/render.py --config configs/T01.json --clean --output output.mp4`.

```json
{
  "preset": "C01",
  "genre": "promo",
  "text": "KOLEKSI BAHARU",
  "subtitle": "Pilih perspektif anda.",
  "accent": "#FF966B",
  "duration": 6,
  "fps": 60,
  "width": 1280,
  "image_paths": ["/path/absolut/foto-1.jpg", "/path/absolut/foto-2.jpg"]
}
```

- `--preset`, `--duration`, `--fps` dan `--width` mengatasi nilai JSON apabila dibekalkan. Tanpa override, metadata preset menjadi asas config. `text` ialah kandungan; warna teks menggunakan `text_color`.
- Warna yang diterima: `bg`, `panel`, `text_color`, `muted`, `accent`, `secondary`, semuanya `#RRGGBB`. Warna artwork tertentu sengaja kekal; ubah sumber jika perlu kawalan setiap bentuk.
- `duration`: maksimum 120 saat bagi renderer preset. Bagi 38 preset lama dan K01–K45, minimum 0.5s, lalai 5s dan keseluruhan gerakan diretime. Bagi L01–L06, lalai/minimum mengikut metadata (contoh 16s); tempoh scene berasingan daripada `tempo` dan cue. Jangan gunakan duration panjang sebagai ganti naratif baharu.
- `fps`: 24, 25, 30, 50 atau 60; lalai 60. `width`: 320–3840, gandaan 32, tinggi sentiasa `width×9/16`. Reka bentuk raster dalaman kekal 1280×720; eksport lebih besar ialah resize, bukan perincian vektor baharu.
- `--clean` membuang tajuk ID, penanda fasa dan progress katalog; ia tidak mengubah layout scene. Tanpanya, overlay membantu memilih preset. `--frame` mengekspot PNG pada masa output yang diminta, dengan saiz reka bentuk 1280×720. `--transparent` membuang latar/overlay katalog dan mengekspot ProRes 4444 beralpha; nama output video mesti `.mov`. Ia juga boleh digabungkan dengan `--frame` untuk PNG beralpha.
- `text` dan `subtitle` maksimum 160 aksara setiap satu. Had ini bukan jaminan muat; gunakan tajuk pendek, semak frame dan pecahkan ayat panjang. Font mengecil supaya muat pada beberapa corak, yang boleh mengurangkan keterbacaan.
- T03 menerima `draft` dan `caret` (`vertical`, `underscore`, `bracket`). H04 menerima `value`, `decimals` (0–3), `prefix`, `suffix`; nombor dipaparkan dengan pemisah ribu koma dan titik perpuluhan.
- B04/B07 menerima `from_value`, `to_value`, `prefix`, `suffix`, `decimals` (0–6) dan `grouping` (boolean, lalai true). Kedua-dua nilai mesti finite. Contoh: `{"from_value":0,"to_value":12500,"prefix":"RM ","suffix":"","decimals":2,"grouping":true}`. Pemisah ribu ialah koma dan perpuluhan ialah titik; format ini bukan pemilihan locale automatik.
- B05 menerima `cues:[{"start":0.8,"end":1.4},...]` mengikut indeks perkataan dalam `text`; teks perkataan tetap datang daripada `text`, bukan medan `word` pada cue. Masa menggunakan scene normal lima saat dan turut berubah apabila `duration` berubah. Tanpa cue, giliran kata ialah demo.
- B06 menerima `pauses:[{"after_character":11,"duration":0.4}]`. Durasi pause menggunakan saat scene lima saat, jumlah mesti kurang 2.95s; kelajuan taip diselaraskan untuk selesai pada 3.65s. Ini cue renderer, bukan penjajaran audio automatik.
- A02, A06, A07 menyokong `\n` untuk baris yang disengajakan; gunakan dua/tiga/tiga baris sebagai titik mula. A01 mengumpulkan teks kepada baris; A03, A04, A05 meratakan newline.
- C01–C04 menerima `image_paths`, senarai fail imej tempatan. A05 menerima satu `image_path`; B02 dan K25 menerima satu `asset`. Gunakan path absolut untuk konsistensi. CLI menyelesaikan `image_paths`, `image_path` dan `asset` relatif terhadap lokasi JSON; jika memanggil fungsi Python terus, sediakan path absolut. Imej pengguna di-cover-crop secara berkadar; carousel mengulang senarai aset jika slot lebih banyak daripada imej.
- Tanpa imej pengguna, carousel menggunakan poster geometri asli, A05 menggunakan ilustrasi bandar asli. Tiada footage atau artwork preview pihak ketiga dimasukkan.

## 4. Empat belas rujukan baharu

Pada 24 September 2026, preview MP4 awam diteliti melalui metadata, contact sheet dan urutan rapat. Masa berikut merujuk preview sebenar, bukan panjang template dalam listing. Audio tidak dinilai. Sumber memberi bukti bentuk dan urutan yang terlihat; easing, expression, keyframe serta layer graph asal tidak diketahui. Implementasi renderer ialah resipi baharu yang dipilih daripada mekanisme ini, bukan semua varian produk asal.

| Preset / pautan sumber | Masa preview diperiksa | Mekanisme yang diperhatikan |
|---|---|---|
| A01 — [Subtitles/Captions XNKHM6X](https://elements.envato.com/subtitles-captions-text-animations-XNKHM6X) | 4.75–6.25s; keseluruhan 76.36s | Perkataan tiba dengan blur/opacity, scribble neon melukis di bawah, hold tajam |
| A02 — [Text W3Y3XNA](https://elements.envato.com/text-animation-W3Y3XNA) | 16.00–19.25s; 37.66s | Dua baris merapat/membesar; gelung pada kata; varian strip putih senget |
| A03 — [Text GNG3GYE](https://elements.envato.com/text-animation-GNG3GYE) | 3.00–5.75s; 26.71s | Kata ditaip besar, mengecil untuk bacaan, kemudian blur sebelum contoh seterusnya |
| A04 — [Typewriter N25CE6N](https://elements.envato.com/typewriter-N25CE6N) | 14.75–17.75s; 31.39s | Bingkai carian bercahaya tumbuh; ikon, type-on, caret bergerak dan berkelip |
| A05 — [Intro Opener U2Q448Q](https://elements.envato.com/intro-opener-U2Q448Q) | 0.00–4.75s; 30.01s | Bukaan mendatar, footage/tajuk, echo besar, grid dan peralihan zoom/strip |
| A06 — [Diary Titles Y74AGUM](https://elements.envato.com/diary-titles-dr-Y74AGUM) | 0.00–4.50s; 47.02s | Baris blur masuk pada kertas grid; gelung dakwat biru dilukis lalu dipadam |
| A07 — [Text EU7UMQT](https://elements.envato.com/text-animation-EU7UMQT) | 2.25–5.75s; 35.79s | Kata berasingan merapat menjadi stack dengan bayang kedalaman, lalu berpisah |
| B01 — [Ripped Paper 62SS98C](https://elements.envato.com/ripped-paper-text-presets-62SS98C) | 12.50–14.20s; 40.85s | Ketulan kecil menjadi lipatan tengah; panel kertas membuka ke kedua sisi |
| B02 — [Opener V3BHS5Y](https://elements.envato.com/opener-V3BHS5Y) | 4.70–6.30s; 52.64s | Jalur imej serong/offset, bina huruf, echo besar dan camera drift ketika hold |
| B03 — [Text 5FDKCMH](https://elements.envato.com/text-animation-5FDKCMH) | 11.20–12.80s; 35.01s | Glyph berpindah dan beberapa glyph berubah sebelum frasa menjadi stabil |
| B04 — [Number Text FL3YXDY](https://elements.envato.com/number-text-animation-pp-FL3YXDY) | 9.00–12.00s; 78.50s | Awalan ayat, count-up berformat, marker magenta melebar di belakang angka |
| B05 — [Creator Subtitle KHLUZHK](https://elements.envato.com/modern-creator-subtitle-KHLUZHK) | 10.80–12.40s; 27.01s | Kata aktif menjadi cyan/glow; kata lama kembali putih, layout ayat tetap |
| B06 — [Typewriter Pro GURUKWQ](https://elements.envato.com/typewriter-pro-GURUKWQ) | 46.50–49.05s; 53.07s | Perkataan ditaip; latar hijau muncul hanya selepas perkataan lengkap |
| B07 — [Number Counter 7LZ6EUM](https://elements.envato.com/number-counter-7LZ6EUM) | 8.80–10.50s; 59.66s | Digit menegak di dalam clip window, settle kepada angka dan label sokongan |

Nama asli tambahan: A01 Neon Scribble Caption; A02 Sticker Keyword Loops; A03 Type Scale Focus; A04 Search Bar Typing; A05 Graphic Editorial Opener; A06 Notebook Ink Notes; A07 Compressed Depth Stack; B01 Paper Fold Reveal; B02 Diagonal Glass Opener; B03 Decode Typography; B04 Inline Metric Marker; B05 Neon Cue Captions; B06 Finished Word Typewriter; B07 Gradient Metric Reels. Gunakan metadata `--list` sebagai sumber nama semasa jika modul dikemas kini.

## 5. Had penggunaan produksi

Preview ialah video senyap 16:9. Eksport biasa H.264 MP4; eksport alpha ProRes 4444 MOV memerlukan FFmpeg `prores_ks` dan boleh digubah atas footage sendiri. Tiada voice-over, muzik, penjana subtitle audio automatik atau layout 9:16 dalam CLI ini. Cue caption dan angka lalai ialah demonstrasi; untuk produksi, gunakan data sebenar dan sejajarkan cue dengan audio sebelum render akhir. Jangan menafsir kemunculan perkataan demo sebagai pengesahan sync suara.

UI dan telefon ialah ilustrasi raster berperspektif, bukan model telefon 3D penuh. Glyph-per-glyph Latin tidak menjamin shaping tulisan Arab, Indic atau emoji kompleks; gunakan unit perkataan/baris yang dibentuk dengan betul dan semak renderer khusus untuk skrip tersebut. Jangan menggunakan scramble pada teks suci atau angka yang mesti betul sepanjang masa.

Katalog offline memaparkan MP4 yang telah dirender; mengubah config tidak menukar video itu secara langsung. Eksport JSON, kemudian render semula. Untuk video akhir panjang, susun klip/preset mengikut skrip dan render scene berasingan; menukar `duration` kepada 120s sahaja tidak mencipta naratif 120s.


## 6. Scene kompleks L01–L06

Baca [scene panjang dengan aksi pantas](long-scene-choreography.md) untuk analisis sumber, prinsip anchor bacaan dan aturan tiga jam animasi. Enam preset ini mempunyai beberapa beat dalam satu kanvas berterusan; semuanya pratonton senyap 16 saat. Jumlah sebelum MP01–MP48 ialah 89 preset; katalog kini mempunyai 137 preset.

| ID | Nama | Mekanisme |
|---|---|---|
| L01 | Hero Orbit Ensemble | Tajuk/feature chips berturutan, subjek geometrik, orbit dan loop bebas |
| L02 | Task Conveyor | Ikon berterusan, panel pemprosesan, progress dan counter |
| L03 | Benchmark Race | Stagger bar/angka, update nilai kedua, rumusan lewat |
| L04 | Workflow Window Cluster | Tingkap bertindih, typing, sambungan, pointer dan handoff |
| L05 | Kinetic Editorial Stage | Teks besar settle, mask/reveal, garis, keyword replacement |
| L06 | Before After Rebuild | Pasangan kad, ghost nilai lama, perubahan setempat dan rumusan |

Gunakan metadata semasa melalui `--list` untuk medan khusus dan `cue_defaults`. `cues` ialah objek nama cue kepada saat mutlak. `tempo` mengubah panjang aksi setempat, bukan meretime seluruh scene. Menambah `duration` menambah masa scene tanpa memperlahankan entrance. Untuk scene jauh lebih lama, tambah kandungan/beat melalui modul dan cue, bukan sekadar loop.

```bash
python render.py --preset L05 --duration 16 --clean --output tipografi.mp4
python render.py --config configs/L03.json --duration 20 --output carta.mp4
python render.py --preset L01 --frame 8 --output hero.png
```

Angka contoh ialah DATA DEMO. Gantikan dengan nilai sebenar bersumber sebelum produksi. Medan palet, teks, tempo dan cue membantu penggunaan semula; renderer ini tetap perlu QA layout apabila teks/genre/angka berubah.


Medan kandungan khusus L01–L06 (senarai penuh tersedia dalam metadata):

- L01–L03: `items`, `summary`; L01 juga `eyebrow`, `trail_label`; L02 `stage_labels` dan nama baris daripada `items`.
- L03: `initial_values`, `values`, `max_value`, `value_suffix`. Bar dan counter berkongsi progress, label DATA DEMO kekal.
- L04: `items` (tiga tajuk panel), `words` (tiga input), `code_lines` (empat baris proses), `output_items` (tiga hasil), `ready_label`, `processing_label`, `complete_label`, `summary_text`.
- L05: `words` (empat frasa berganti), `items` (tiga jubin), `eyebrow`, `summary_text`.
- L06: `items` (tiga metrik), `before_values`, `after_values`, `suffix`, `before_label`, `after_label`, `progress_label`, `summary_text`. Nilai peratus contoh menggunakan skala yang sama.

Sesuaikan cue berantai selepas mengubah tempo. Contohnya, panel penerima patut aktif selepas packet/pointer tiba; kelewatan ini perlu dijadualkan dalam config, bukan disimpulkan secara automatik daripada nama cue. Semak semua teks sokongan apabila menukar genre/topik.


## 7. Text animation K01–K45
8. MotionPrompt MP01–MP48

Baca [pemetaan 45 preset daripada sembilan rujukan](kinetic-typography-expansion.md) untuk mekanisme, timecode dan kawalan. Lima preset setiap sumber dipilih berdasarkan perbezaan gerakan, bukan warna/arah. Katalog mempunyai penapis keluarga/sumber serta eksport semua medan khusus. Contoh:

```bash
python render.py --preset K16 --clean --output pantulan.mp4
python render.py --config configs/K29.json --duration 7 --output tipografi.mp4
python render.py --preset K43 --frame 2.6 --output badge.png
```

Gunakan tajuk pendek dan semak pergerakan selepas menukar kandungan. K01–K45 memakai jam normal lima saat; `tempo` L01–L06 tidak mengawal aksi setempat K. Gunakan metadata `--list` atau JSON katalog untuk kawalan sebenar setiap ID. Preview senyap; tiada sync voice-over automatik.

## 8. MotionPrompt MP01–MP48

Baca [bank 48 gaya](motionprompt-48-styles.md) untuk indeks serta arahan produksi. Semua 48 ID berdaftar dalam `render.py`, mempunyai fungsi scene sendiri di `motionprompt.py`, menerima `--frame`, `--config` dan eksport MP4 H.264 melalui CLI sama seperti preset lama. Katalog HTML menunjukkan keluarga `MotionPrompt · 48 gaya`. Default ialah enam saat pada jam normal 0–5; menukar `duration` meretime scene penuh. Preview senyap dan visual contoh dilukis pada 1280×720 16:9.

```bash
python render.py --preset MP01 --frame 2.6 --clean --output kaiju.png
python render.py --preset MP17 --duration 6 --fps 30 --clean --output carta.mp4
python render.py --preset MP24 --config /path/projek/foto.json --clean --output foto.mp4
```

Gunakan `text`, `subtitle`, `genre`, palet dan `items` untuk kandungan. `image_paths`/`image_path` boleh menggantikan imej demo pada preset yang menggunakan foto, skrin atau produk; ia disusun dengan contain dalam slot yang tersedia. MP17 menerima `values` empat nisbah 0–1, MP37 menerima `rooms` lima kotak `(x0,y0,x1,y1)`, MP40 menerima `amplitudes` senarai sampel 0–1. Tanpa data, angka/pelan/waveform ditanda demo apabila berkenaan. MP06/21/27/35/37/47 menggunakan ilustrasi 2.5D, bukan mesh 3D. Sesetengah scene memenuhi keseluruhan frame; eksport `--transparent` tidak menjamin latar alpha bersih bagi setiap MP.

Setiap MP ialah scene boleh dirender dan disesuaikan, bukan pelaksanaan penuh semua objek dan aksi dalam prompt laman sumber. Bina aset dan gerak tambahan untuk video komersial, khususnya identiti manusia, simulasi produk sebenar, peta tepat, bendera sebenar, 3D fizikal atau tipografi tulisan kompleks. Bina semula layout untuk 9:16; jangan potong komposisi 16:9. Uji frame, potongan dan teks pada bahan pengguna sebelum menyatukan scene ke video akhir.

## 9. Preset panduan MS/PL/PV/AD

Lihat [indeks 185 panduan](open-motion-185-guides.md) bagi status, deskripsi, aset dan sumber. Empat keluarga: MS01–MS16 (contoh pek motion), PL01–PL14 (shot pelancaran), PV001–PV152 (shot produk), AD01–AD03 (aliran iklan). Semua ID kini berfungsi dengan `render.py --preset`, sebagai **demo adaptasi asal**, bukan pemasangan komponen upstream. Registry dan builder kini 322 entri. Semak sumber modul untuk parameter khusus yang tersedia dan QA selepas perubahan.

```bash
python render.py --preset PV128 --clean --output card-stack.mp4
python render.py --preset PL08 --clean --output counter.mp4
python render.py --preset MS14 --clean --output maths.mp4
python render.py --preset AD02 --clean --output launch.mp4
```

Preview keseluruhan boleh dilihat di https://motion-preset-atlas.akramania.chatgpt.site. Pengesahan ialah semakan bingkai dan penyahkodan 322 MP4; interaksi katalog belum diuji melalui browser kerana control-browser tidak tersedia semasa penerbitan. Preview senyap 960×540/30fps, artwork reka bentuk 1280×720. Jangan mendakwa semua kemahiran pek, variasi shot, 3D fizikal, suara atau parameter upstream dilaksanakan.

## 10. EV001–EV120 — 28 rujukan baharu

Baca [pengembangan 28 preview Envato](envato-28-expansion.md). Tambahan ini meningkatkan registry kepada 442 entri. Semua ID EV menggunakan jam normal 0–5, durasi contoh 6s dan dispatcher `envato2026.py`. Peta menggunakan Natural Earth public domain; transisi menerima dua imej melalui `image_paths` dan `show_titles`. Fail `envato_index.json` merekod sumber, sampel dan kawalan. Semua resipi asal berpandukan preview, bukan template atau aset Envato.
