# Text animation dan kinetic typography K01–K45

## Kandungan

1. Skop dan bukti
2. Cara memecahkan rujukan kepada preset
3. Tipografi, layout dan masa
4. Peta sembilan sumber
5. Penggunaan semula

## 1. Skop dan bukti

Gunakan catatan pemeriksaan sembilan preview MP4 awam pada sesi 24–25 September 2026 sebagai asas. Preview diperiksa sepanjang klip serta melalui urutan bingkai rapat. Audio tidak dinilai. K01–K45 ialah 45 implementasi Python asal, lima bagi setiap rujukan, meluaskan katalog daripada 44 kepada 89. Aset, footage, fon komersial dan kod expression sumber tidak disertakan; easing serta graph layer asal tidak diketahui.

Tafsir `observed` sebagai mekanisme utama yang terlihat pada preview, bukan padanan semua butiran. Tafsir `adapted` sebagai resipi asal yang mengembangkan pemerhatian. Masa sumber bagi olahan menunjuk inspirasi, bukan bukti keseluruhan resipi baharu wujud dalam sumber. Jangan mengira perubahan warna, arah atau ayat sahaja sebagai preset tambahan.

## 2. Cara memecahkan rujukan kepada preset

1. Inventori setiap contoh dalam preview, termasuk montage awal. Periksa urutan rapat pada gerakan yang dipilih. Catat masa mutlak preview; tambahkan offset jika analisis dibuat daripada trim.
2. Pecahkan komposisi kepada glyph, perkataan, baris, kumpulan, bingkai dan props. Kenal pasti anchor, objek bebas dan hubungan seperti badge bergerak dahulu untuk memberi ruang kepada teks.
3. Bezakan mekanisme: tracking huruf vs leading baris; slant glyph vs putaran kumpulan; pantulan vs extrusion; glow typingfront vs cahaya merentas teks lengkap. Jangan cipta ID baharu untuk warna/arah sahaja.
4. Reka masuk, aktiviti dan keluar dengan sela bacaan tajam. Gerakkan aksen atau props semasa hold tanpa terus menggoncang semua huruf.
5. Ukur teks dengan font sebenar sebelum membina mask, badge atau laluan. Teks yang bertukar tempat perlu jarak berdasarkan lebar kedua-duanya. Gunakan baseline font bersama bagi glyph, termasuk lowercase dan descender.
6. Semak hasil render pada entrance, bacaan, pertukaran layout dan exit. Periksa ejaan, clipping, perlanggaran, alpha dan masa output. Contact sheet sahaja tidak membuktikan kelancaran; semak frame bersebelahan serta encode/decode video.

## 3. Tipografi, layout dan masa

Bina hierarki headline, penekanan, label kecil dan subline melalui saiz, berat serta ruang. Pisahkan glyph tajam daripada lapisan glow. Tetapkan stagger supaya teks panjang selesai masuk sebelum masa bacaan. Semasa reflow, ukur kumpulan sasaran dan gerakkan jiran; perubahan skala sahaja boleh menyebabkan pertindihan.

Gunakan glyph berasingan untuk teks Latin yang sesuai. Jangan andaikan shaping Arab/Jawi, Indic atau emoji kompleks terpelihara; gunakan unit perkataan/baris yang telah dibentuk dan semak renderer khusus.

Semua K memakai masa reka bentuk 0–5 saat. Fungsi awam `frame()` menerima saat output dan meretime melalui `duration`. Demo ialah 5 saat, 1280×720/60fps, senyap. Untuk scene yang stay lama tetapi banyak aksi pantas, gunakan jam scene, event tempatan dan loop ambient berasingan seperti [panduan scene panjang](long-scene-choreography.md). K01–K45 tidak menyediakan timeline multiobjek secara automatik. Tulis cue dalam scene projek dan kekalkan potongan terus antara scene mengikut pilihan pengguna.

## 4. Peta sembilan sumber

35 resipi berdasarkan mekanisme yang diperhatikan; 10 olahan asal. Masa di bawah ialah saat mutlak preview.

### 1. [YVTH2U2](https://elements.envato.com/text-animation-YVTH2U2)
Tempoh preview sumber: 157.023 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K01 | Glyph Stencil Steps | 32.20–33.30 s | Diperhatikan | Setiap huruf terbuka melalui topeng bertangga pada dua paksi. |
| K02 | Upright to Slant | 27.40–28.20 s | Diperhatikan | Teks tegak berubah ke condongan melalui shear yang berterusan. |
| K03 | Negative Badge Reveal | 81.80–84.20 s | Diperhatikan | Lencana berkembang dengan huruf berlubang yang mendedahkan latar. |
| K04 | Pierced Hero Label | 93.20–95.00 s | Diperhatikan | Label kecil bergerak berasingan lalu merentasi tajuk utama. |
| K05 | Hierarchy Exchange | 121.30–121.70 s | Diperhatikan | Dua baris bertukar saiz utama dan sokongan pada jajaran kiri yang sama. |

### 2. [DXMD7HL](https://elements.envato.com/text-animation-DXMD7HL)
Tempoh preview sumber: 55.147 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K06 | Elastic Row Squeeze | 11.00–13.80 s | Diperhatikan | Baris dipadatkan, condong seketika dan melantun ke bentuk yang jelas. |
| K07 | Keyword Push Reflow | 21.00–23.50 s | Olahan asal | Satu kata membesar dan kata bersebelahan bergerak mengikut ruang baharu. |
| K08 | Highlighted Row Swap | 25.50–26.00 s | Diperhatikan | Dua baris bertukar tempat melalui tiga tahap yang mengelakkan teks bertindih. |
| K09 | Glyph Spacing Accordion | 27.75–30.75 s | Olahan asal | Jarak huruf mengembang, mengecil dan kembali ke susunan bacaan. |
| K10 | Fixed Edge Justification | 38.25–40.00 s | Olahan asal | Lebar baris berubah sambil satu tepi kekal pada paksi susunannya. |

### 3. [84TY5RP](https://elements.envato.com/text-animation-84TY5RP)
Tempoh preview sumber: 30.550 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K11 | Luminous Glyph Scanner | 0.80–1.80 s; 2.40–3.20 s | Diperhatikan | Cahaya lembut melintas pada bentuk huruf yang lengkap. |
| K12 | Curved Word Dock | 5.00–5.80 s | Diperhatikan | Kata besar mengikut lengkung dan bertukar berat sebelum berlabuh di sisi awalan. |
| K13 | Type Depth Tunnel | 7.20–8.60 s | Diperhatikan | Lapisan teks pada skala berbeza merapat menjadi satu tajuk. |
| K14 | Light Veil Inversion | 9.70–10.20 s; 10.60–11.00 s | Olahan asal | Tabir cahaya setempat mengubah polariti teks ketika melintas. |
| K15 | Baseline Wave Settle | 21.00–21.60 s; 23.00–23.30 s | Diperhatikan | Gelombang bergerak melalui huruf lalu menetap pada garis dasar. |

### 4. [R7E9UER](https://elements.envato.com/text-animation-R7E9UER)
Tempoh preview sumber: 46.175 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K16 | Mirror Floor Tracking Zoom | 12.3–19.9 s | Diperhatikan | Teks mengembang dengan jarak huruf berubah dan pantulan lantai yang mengikut gerakan. |
| K17 | Mixed Weight Glyph Slingshot | 7.75–11.9 s | Diperhatikan | Huruf berlainan ketebalan bergoyang secara individu sebelum tajuk meluncur sebagai satu kumpulan. |
| K18 | Opposing Word Hinge | 25.0–30.4 s | Diperhatikan | Dua baris huruf masuk berturutan, kemudian berengsel keluar dalam arah bertentangan. |
| K19 | Vertical Glyph Totem | 35.0–39.8 s | Diperhatikan | Huruf dibina sebagai tiang menegak; setiap huruf jatuh keluar mengikut ritma tersendiri. |
| K20 | Punctuation Bounce Baseline | 40.0–44.5 s | Diperhatikan | Ayat mendarat pada garis dasar; tanda baca melantun secara berasingan untuk memberi tekanan. |

### 5. [QBTKNGF](https://elements.envato.com/text-scene-QBTKNGF)
Tempoh preview sumber: 52.404 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K21 | Chevron Light Gate | 2.0–5.5 s | Olahan asal | Chevron bercahaya membuka teks dengan topeng berterusan, kemudian memadamkannya ketika kembali. |
| K22 | Perimeter Light Runner | 12.0–20.0 s | Diperhatikan | Cahaya bergerak mengelilingi bingkai teks sementara ayat di tengah kekal jelas. |
| K23 | Living Bullet Panel | 21.8–27.2 s | Olahan asal | Panel bertambah tinggi sebelum setiap baris masuk, dengan gerakan kecil pada kata pilihan. |
| K24 | Plus Anchor Assembly | 29.0–33.0 s | Olahan asal | Tanda tambah membesar; dua frasa berpusing dan berlabuh di sisinya. |
| K25 | Luminous Media Caption | 36.0–45.0 s | Diperhatikan | Bukaan media berkembang dan tajuk bercahaya berlabuh pada bahagian bawah bingkai. |

### 6. [YZHKP5W](https://elements.envato.com/text-animation-YZHKP5W)
Tempoh preview sumber: 50.000 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K26 | Angled Border Circuit | 5.5–9.8 s | Diperhatikan | Garis mengelilingi bingkai serong sebelum tajuk masuk pada satah yang sama. |
| K27 | Diagonal Divider Reveal | 10.0–14.8 s | Diperhatikan | Garis serong membuka ruang antara dua perkataan yang muncul dari pusat. |
| K28 | Slanted Row Unfold | 15.0–19.8 s | Diperhatikan | Baris teks serong membuka satu persatu seperti engsel, kemudian melipat semula. |
| K29 | Staircase Word Assembly | 30.0–34.8 s | Diperhatikan | Perkataan bergerak daripada lajur menegak kepada tangga lalu terkunci pada satu baris. |
| K30 | Inserted Keyword Lockup | 40.0–44.8 s | Diperhatikan | Kata tengah disisipkan untuk menolak dua baris luar, kemudian susunan mengecil semula. |

### 7. [N8UXUU6](https://elements.envato.com/text-animation-N8UXUU6)
Tempoh preview sumber: 33.034 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K31 | Tracking Frame Assembly | 0.30–1.35 s | Diperhatikan | Jarak huruf mengembang, dua jalur menyapu dan bingkai membesar mengikut tajuk. |
| K32 | Skew Baseline Extrusion | 4.85–5.90 s | Diperhatikan | Tajuk naik dari satah condong dengan lapisan kedalaman dan garis sokongan berlawanan arah. |
| K33 | Elastic Leading Accordion | 8.00–9.05 s | Olahan asal | Tiga baris merapat dan membuka ruang menegak dengan huruf kekal pada saiz yang sama. |
| K34 | Leading Block Reflow | 14.60–16.00 s | Diperhatikan | Blok warna membuka tajuk pertama, kemudian dua baris lain berpindah ke susunan akhir. |
| K35 | Split Caption Aperture | 20.50–21.55 s | Diperhatikan | Bingkai bermula sebagai celah nipis sebelum dua pengatup terbuka dan mendedahkan tajuk. |

### 8. [7NXC4GG](https://elements.envato.com/text-animation-7NXC4GG)
Tempoh preview sumber: 24.000 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K36 | Live Typeset Pill | 8.20–9.40 s | Diperhatikan | Kotak kapsul mengukur setiap huruf yang ditaip dan membesar bersama teks. |
| K37 | Travelling Glyph Glow | 5.90–6.90 s | Diperhatikan | Cahaya pendek mengikuti hadapan taip, kemudian semua huruf kekal tajam untuk dibaca. |
| K38 | Icon Cursor Handoff | 11.40–12.80 s; 16.00–17.40 s | Diperhatikan | Kursor mengikuti huruf yang sedang ditaip dan bertukar bentuk pada hentian perkataan. |
| K39 | Live Wrap Story | 8.20–9.40 s; 17.85–18.30 s | Olahan asal | Teks ditaip mengikut ukuran sebenar, membalut baris dan menatal dalam tetingkap bacaan. |
| K40 | Contour to Ink | 0.35–1.55 s | Olahan asal | Empat suku kontur setiap huruf berkumpul terlebih dahulu sebelum isi huruf mengunci. |

### 9. [TQ2SPTQ](https://elements.envato.com/text-animation-TQ2SPTQ)
Tempoh preview sumber: 26.015 saat.

| ID | Nama | Masa sumber | Asas | Mekanisme |
|---|---|---|---|---|
| K41 | Counter-Sliding Strips | 0.20–1.60 s | Diperhatikan | Dua jalur teks negatif meluncur bertentangan sebelum berlabuh dalam susunan akhir. |
| K42 | Offset Quote Reveal | 6.00–7.40 s | Diperhatikan | Dua kumpulan baris menyapu dari arah berlawanan bersama garisan dan atribusi. |
| K43 | Badge Docking | 9.60–12.20 s | Diperhatikan | Lencana bergerak ke kiri untuk memberi ruang kepada label dua baris di sebelah kanan. |
| K44 | Bracket Window Sweep | 17.00–18.75 s | Diperhatikan | Kurungan membuka tetingkap sementara tajuk dan subjudul menyapu di dalam kawasan klip. |
| K45 | Polarity Token | 21.60–23.00 s | Diperhatikan | Token bulat dilukis mengikut kontur, diisi sapuan terbalik dan diikuti frasa sokongan. |


## 5. Penggunaan semula

Gunakan `assets/motion_presets/render.py --list` untuk metadata semasa dan medan khusus. Semua ID menerima teks/subtajuk dan palet; kawalan geometri berbeza mengikut mekanisme. K25 menerima `asset` untuk imej sendiri, menggunakan ilustrasi asal jika kosong. Eksport JSON katalog menyimpan kawalan renderer; metadata sumber berada dalam kad dan `presets.json`.

```json
{"preset":"K16","genre":"corporate","text":"IDEA ANDA","subtitle":"Bina sesuatu yang bermakna.","tracking":18,"reflection":0.32,"depth":6,"duration":6,"fps":60,"width":1280}
```

Daripada akar toolkit pengguna:

```bash
python renderer/render.py --config pilihan.json --clean --output hasil.mp4
python renderer/render.py --preset K16 --transparent --output pantulan.mov
```

Preview katalog tidak berubah secara langsung selepas edit JSON; render semula. Eksport alpha menggunakan MOV ProRes 4444. Ini renderer Python yang boleh diguna semula, bukan pemasangan projek native After Effects/Premiere/Resolve.
