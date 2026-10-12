# Scene panjang dengan aksi pantas

## Kandungan

1. Bukti daripada rujukan pengguna
2. Reka teks dan susunan perhatian
3. Pisahkan tiga jam animasi
4. Bina gerakan kompleks
5. Gunakan preset L01–L06
6. Semak hasil

## 1. Bukti daripada rujukan pengguna

Rujukan `1000509726.mp4` diperiksa melalui metadata, sampel 0.5 saat sepanjang video dan sampel 0.1 saat pada urutan pembinaan. Rakaman telefon 1080×2376 sepanjang 67.605 saat mengandungi video landscape kira-kira 1080×608 di tengah, sekitar y=744 selepas paparan feed awal. Rakaman ini tidak mempunyai stream audio. Purata kadar frame rakaman sekitar 30.6 fps tidak membuktikan FPS projek asal. Jangan mendakwa audio, sumber After Effects, font tepat atau jumlah keyframe telah disahkan.

| Masa rakaman | Pemerhatian | Mekanisme yang dipindahkan |
|---|---|---|
| 2.5–5.7s | Kata uppercase tebal bermula sangat besar, menetap di tengah; frasa/warna penekanan berganti | Scale-to-settle, hierarki warna, baseline stabil |
| 7.0–10.8s | Eyebrow monospaced berjarak, tajuk tebal, rule nipis, tag, deskripsi dan angka tiba berturutan; karakter terapung | Reveal berlapis, bacaan stabil, loop karakter bebas |
| 17.5–21.7s | Dua baris perbandingan, harga lama dipotong, anak panah, harga baharu, pill rumusan tiba lewat | Rantaian bukti sebelum rumusan |
| 23–27.8s | Tiga bar berkembang secara stagger bersama angka; kertas/karakter bergerak semasa carta menetap | Satu progress bagi panjang bar dan angka; props dalam ruang bebas |
| 29–33.8s | Carta tetap, conveyor ikon bergerak, aksi tangan robot, rumusan muncul kemudian | Pergerakan berterusan di pinggir dan event setempat |
| 35–39.9s | Blok jatuh/bertimbun, bar/count-up, karakter melintas di bawah | Parent/child transform, impak setempat, aksi selari |
| 41–45.8s | Kelompok tingkap kod, pointer melawat tingkap, carta kiri dan timer bawah | Laluan berurutan, beberapa workspace dalam satu scene |
| 46–50.8s | Bar sebelum/selepas berubah panjang dengan jejak nilai lama; rumusan lewat | Ghost track, interpolasi nilai, pembacaan before/after |
| 51–53.4s | Counter besar, cincin orbit, glow dan partikel dokumen | Titik fokus tetap, orbit pelbagai fasa |
| 53.5–58.4s | Tiga kad dibina berasingan; karakter terus bergerak; tajuk/rumusan lewat | Penyelesaian komposisi secara berperingkat |

Scene rujukan biasanya sekitar 4.5–6 saat. Scene 16 saat dalam preset baharu ialah adaptasi asal untuk permintaan scene yang bertahan lebih lama, bukan ukuran tempoh sumber. Angka, nama model dan harga dalam rakaman tidak disahkan sebagai fakta. Gunakan data demo neutral dalam pratonton dan data bersumber untuk produksi sebenar.

Sumber mempunyai flash, speed tunnel dan kad serong untuk sesetengah pertukaran scene. Pilihan pengguna semasa tetap potongan terus tanpa transition. Ambil mekanisme dalaman scene tanpa mewarisi transition tersebut.

## 2. Reka teks dan susunan perhatian

- Tetapkan lima lapisan: latar/glow; grid atau garis perspektif; objek sokongan; panel/subjek; teks bacaan dan sorotan. Teks penting kekal di atas objek hiasan.
- Gunakan sans serif berat untuk tajuk ringkas. Gunakan label monospaced kecil berjarak untuk kategori, bukan perenggan. Pilih fon berdasarkan bentuk yang tersedia, jangan menamakan fon sumber secara tekaan.
- Bentuk hierarki dengan saiz, berat, warna dan ruang: eyebrow → tajuk → rule → tag → deskripsi/angka → rumusan. Jangan jadikan semua baris sama besar atau semuanya glow.
- Ukur perkataan pada kedudukan akhir sebelum animasi. Beri keyword slot berlebar cukup supaya pertukaran perkataan tidak mengubah kedudukan keseluruhan ayat.
- Untuk teks besar: masuk melalui mask/offset/scale, settle cepat, tahan tajam untuk dibaca. Echo/outline di belakang mesti berkontras rendah.
- Buat underline/highlight sebagai objek tersendiri. Kekalkan stroke/padding, jangan ubah skala teks hanya untuk memanjangkan garis.
- Jika caption diperlukan, sediakan ruang tengah sebelum meletakkan carta atau subjek. Jika brief meminta tanpa caption, jangan tambah caption automatik. Label data bukan caption suara.

## 3. Pisahkan tiga jam animasi

Jangan menghasilkan scene panjang dengan melambatkan klip lima saat sahaja. Bezakan:

1. **Jam scene:** menentukan tempoh keseluruhan, masa bacaan dan akhir scene.
2. **Jam event:** cue mutlak dan tempoh gerak untuk setiap entrance, update, pointer, angka, underline atau exit.
3. **Jam loop:** float, orbit, conveyor, blink atau partikel dengan fasa/period sendiri.

Contoh scene 16 saat: 0–2s bina konteks; 2–5s tunjuk fungsi pertama; 5–8s proses kedua; 8–11s perubahan data/keyword; 11–14s hasil atau rumusan; baki masa baca/keluar. Ini resipi awal, bukan jadual wajib. Selaraskan dengan audio sebenar apabila voice-over wujud.

Julat gerak awal untuk diuji: event kecil 0.18–0.55s; stagger 0.06–0.14s; reposisi besar 0.45–0.9s; loop ambient 2–6s. Bezakan tempoh bergerak daripada tempoh membaca. Teks utama perlu dwell yang mencukupi walaupun objek lain pantas.

`tempo` memendekkan atau memanjangkan aksi setempat; ia tidak mengubah tempoh scene atau semua cue. Cue mutlak boleh disesuaikan satu demi satu. Jika scene dipanjangkan banyak, tambah beat bermakna atau cue baharu; loop lebih lama sahaja tidak menjadikannya naratif yang lengkap.

## 4. Bina gerakan kompleks

- Tentukan fokus bagi setiap beat. Benarkan beberapa aksi selari, tetapi hanya satu kumpulan berkontras tinggi mengambil perhatian utama pada satu masa.
- Kekalkan tajuk, paksi, label, skala dan panel sebagai anchor. Pergerakan dekoratif menggunakan zon pinggir atau ruang di antara panel, bukan melintasi teks penting.
- Gunakan parent untuk gerak kumpulan; child untuk blink, ayunan lengan, putaran badge, progress atau teks. Tambahkan offset pada posisi parent, jangan ganti posisinya dan menyebabkan lompatan.
- Untuk carta, kira bar dan angka daripada progress yang sama, tanpa spring overshoot pada nilai data. Simpan ghost track nilai asal apabila perbandingan memerlukannya. Labelkan unit, maksud arah yang lebih baik, dan data demo.
- Untuk conveyor, guna indeks modulo dengan jarak seragam dan cull objek luar viewport. Jangan reset keseluruhan jalur dalam frame yang kelihatan.
- Untuk partikel, gunakan seed dan fasa stabil. Ubah beberapa sifat sahaja supaya tidak menjadi noise. Cache sprite, bayang dan glow yang tidak berubah.
- Untuk path, gerakkan titik/cursor secara berterusan melalui waypoint. Tunjukkan respons pada panel sasaran selepas tiba, bukan sebelum pointer sampai.
- Untuk before/after, kekalkan skala dan asas perbandingan yang sama. Gunakan masa update tersendiri dan rumusan hanya selepas nilai settle.
- Untuk akhir scene, gunakan `end_behavior: hold` jika objek perlu kekal hingga cut. L01–L06 kini melaksanakan `hold` sahaja. Tambah exit setempat pada kod/cue apabila brief memerlukannya; jangan padam seluruh kanvas dengan flash.

## 5. Gunakan preset L01–L06

Enam preset tambahan menggunakan scene 16 saat, masa sebenar dalam saat dan cue setempat. Metadata semasa daripada `render.py --list` ialah sumber parameter autoritatif. Baca juga [Preset Atlas](preset-atlas.md) untuk 38 corak terdahulu dan batas format.

| ID | Komposisi | Gunakan untuk |
|---|---|---|
| L01 | Hero Orbit Ensemble | Pengenalan produk/karakter dengan feature chips dan orbit |
| L02 | Task Conveyor | Aliran tugasan, pemprosesan, ikon dan progress dalam satu stage |
| L03 | Benchmark Race | Carta beberapa bar, pembinaan awal dan update kedua |
| L04 | Workflow Window Cluster | Beberapa tingkap, typing, sambungan dan handoff |
| L05 | Kinetic Editorial Stage | Tajuk berat, mask perkataan, keyword swap dan elemen editorial |
| L06 | Before After Rebuild | Kad sebelum/selepas, ghost values, perubahan metrik dan rumusan |

Gunakan `time_mode: seconds` yang ditetapkan metadata, `duration`, `tempo` dan `cues`. Enjin menyimpan `_seconds` dan `_duration` untuk renderer; jangan menulis medan dalaman ini dalam konfigurasi pengguna. Modul lama masih menerima masa dinormalisasi lima saat supaya preset sedia ada kekal serasi.

Pratonton ialah ilustrasi raster 1280×720/60fps yang boleh diubah, bukan projek After Effects atau simulasi 3D penuh. Warna genre sahaja tidak menjamin komposisi sesuai untuk setiap topik. Ubah teks, data, aset dan cue mengikut kandungan; untuk portrait bina semula layout.

## 6. Semak hasil

- Semak 0s, setiap cue, cue±1 frame, kemunculan teks, perubahan data, adegan paling padat dan hujung scene.
- Periksa bahawa tajuk/data tidak bergerak tanpa tujuan sewaktu dibaca. Props tidak menutup label/caption; nilai akhir sama dengan config.
- Uji seek deterministik dan dua tempo pada cue yang sama: cue harus kekal pada saat yang sama, aksi berubah kelajuan, tempoh video tidak berubah.
- Uji durasi lebih panjang: entrance tidak menjadi perlahan dan end cue masih berfungsi. Tempoh terlalu pendek untuk jadual preset mesti ditolak atau jadual direka semula dengan nyata.
- Semak frame bersebelahan semasa gerak serta video penuh melalui decoder. Contact sheet membantu komposisi tetapi tidak membuktikan kelancaran playback atau motion blur.
- Pastikan kepadatan gerak tidak menjejaskan bacaan. Jangan mendakwa bilangan animasi bebas, puluhan lapisan atau ratusan aset berdasarkan rupa sahaja; kira daripada manifest jika metrik tersebut diperlukan.
