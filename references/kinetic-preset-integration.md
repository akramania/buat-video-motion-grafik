# Integrasi 30–50 preset tipografi dalam video bernarasi

Gunakan panduan ini apabila pengguna meminta jumlah variasi kinetic typography yang tinggi, caption daripada preset sebenar, bar suara atau teks di atas foto produk. Kes REMUS 600 membuktikan 35 ID K yang berbeza boleh digabungkan dengan foto, imej ilustrasi 3D, narasi Google AI Studio serta MP40 dalam satu video 16:9. Ambil mekanismenya sebagai pola kerja; sesuaikan orientasi, tempoh, palet dan jumlah ID kepada brief baharu.

## Pilih dan buktikan variasi

1. Ukur tempoh voice-over sebenar. Pecahkan kepada frasa yang mempunyai ruang bacaan; beri setiap frasa `start`, `end`, `display_text` dan satu `preset_id` daripada K01–K45. Jangan andaikan 50 frasa sesuai dengan 50 preset jika jumlah perkataan, tempo atau tempoh tidak memberi ruang bacaan. Katalog kini hanya mempunyai 45 ID K unik: jika diminta 46–50 ID K sahaja, bina serta daftar baki preset baharu yang benar-benar dirender, atau jelaskan had tersebut. Bagi permintaan umum kinetic typography, pilih juga mekanisme teks T/X/H/A/B yang sesuai seperti panduan di bawah; jangan kira ID K berulang sebagai ID baharu.
2. Semak mekanisme setiap calon dalam `render.registry()` atau katalog `render.py --list`. Pilih pelbagai gerak sebenar seperti mask glyph, leading, pertukaran baris, pantulan, binaan bertangga, bingkai, typewriter dan jalur bertentangan. Pendekkan ayat atau pecahkan baris untuk mekanisme yang memerlukan dua kata atau panel sempit.
3. Salin toolkit ke folder projek. Panggil `registry()` untuk mendapatkan dispatch, `configuration(preset_id, raw_config)` untuk menyediakan kawalan, dan fungsi dispatch pada setiap jam tempatan. `_transparent=True` membolehkan keluaran RGBA dilapis di atas media pengguna. Kosongkan `subtitle` dan label demo yang tidak diperlukan. Jangan tulis semula mekanisme lalu menyatakan ID K masih digunakan.
4. Simpan dalam manifest ID, nama, mekanisme, fail sumber preset, teks, cue audio, ruang selamat, konfigurasi dan jumlah **ID teks unik**. Senaraikan MP40 berasingan. Setiap segmen video perlu mempunyai frame animasi sebenar, bukan satu imej pratonton preset yang diulang.

## Masa, saiz dan kedudukan

Preset K menggunakan jam reka bentuk 0–5 saat. Tentukan jam apabila semua glyph dan teks sokongan benar-benar lengkap bagi preset serta teks yang digunakan; jangan menggunakan titik 1.65 yang sama untuk semua mekanisme. Petakan fasa hingga jam siap-baca kepada entrance singkat, baki hingga sekitar 4 kepada aksi/bacaan dan fasa akhir kepada exit. Mulakan entrance sebelum onset pertuturan apabila perlu supaya teks boleh dibaca ketika frasa disebut. Kekalkan hold yang mencukupi; letakkan gerak aksen dalam hold jika scene berlanjutan. Ikut [kaedah CME V3](cme-v3-audio-captions.md) untuk penjajaran perkataan, pre-roll dan semakan typewriter/counter.

Jika diminta 40–80 variasi, pilih juga ID teks yang benar-benar dirender daripada keluarga T/X/H/A/B jika mekanismenya sesuai. Bezakan jumlah frasa, ID teks unik dan preset grafik; jangan kira perubahan palet, pengulangan ID, bar suara atau gambar produk sebagai variasi teks baharu. Contoh CME V3 menggunakan 108 frasa dan 69 ID teks unik; angka ini bukti satu projek, bukan kuota setiap video.

Kira bounding box daripada beberapa saat jam reka bentuk, termasuk pembinaan, hold dan reflow. Gunakan satu bounds stabil sepanjang satu frasa untuk mengelak saiz atau kedudukan bergetar kerana crop frame berubah. Jika entrance preset memerlukan ruang lebih besar daripada hold, pilih bounds yang meliputi gerak itu atau gunakan mask yang disengajakan. Skala komposisi mengikut kawasan teks, bukannya crop seluruh video kepada preset 16:9.

Sediakan safe area subjek mengikut aset/scene. Foto produk atau kenderaan berlabel mesti dipaparkan lengkap apabila brief memintanya; semak hidung, ekor, sirip, label, logo dan teks yang sudah ada dalam foto. Caption boleh tindih foto tetapi elakkan subjek yang dilindungi. Tempatkan bar suara dan progress line dalam ruang kosong yang disemak pada setiap jenis latar. Pada foto berwarna cerah, ubah warna teks dan gunakan bahagian atas jika subjek berada di bawah; pada latar gelap, gunakan kontras dan bayang yang terkawal. Jangan menambah header kecil yang tidak diminta.

## Preset bar suara dan audio

MP40 ialah audiogram dengan 40 bar. Apabila hanya bar suara diperlukan, render preset MP40 dengan `amplitudes` yang dikira daripada tingkap RMS pendek fail narasi, lalu komposit bahagian bar dalam kad yang sesuai. Pastikan bar berubah mengikut audio, bukannya osilator hiasan yang tidak berkait. Jangan kira MP40 sebagai preset teks K. Sumber suara lalai pengguna ini ialah Google AI Studio; ikut pilihan suara, bahasa dan nada terkini. Revisi visual yang diminta "ulang yang sama" mengekalkan audio asal jika narasi sudah dipersetujui.

## Semakan hasil sebenar

Render pratonton satu frame pada waktu bacaan bagi **semua** ID dan urutan lima frame atau lebih bagi beberapa mekanisme yang berlainan. Pratonton daripada fungsi komposit belum cukup: ekstrak semula frame daripada MP4 yang telah dieksport. Semak teks tersusun pada masa yang tepat, perkataan tidak melekat akibat spacing negatif, tiada potongan pada mask/exit, audio bar tidak menutup subjek dan tiada ayat terlalu kecil. Jalankan `ffprobe` untuk dimensi, FPS, durasi dan frame count; nyahkod seluruh MP4 dengan FFmpeg. Untuk revisi visual, banding checksum paket audio yang diekstrak jika audio dikekalkan secara stream copy. Baiki segmen yang rosak dan semak MP4 gabungan semula.

Imej komposit atau model terjana yang tampak seperti 3D ialah ilustrasi 3D, bukan bukti mesh dan rig 3D sebenar. Label proses dan hasil dengan tepat.
