# Caption tengah dan revisi tanpa transition

## Skop dan keutamaan

- Ikut brief terbaru. Bagi pengguna ini, utamakan clean cut dan caption tengah yang mudah dibaca pada telefon; jangan mengenakan pilihan ini apabila arahan terbaru meminta kedudukan lain, transition tertentu atau tiada caption.
- Jika pengguna sudah menyukai video dan meminta perubahan kecil, ubah komponen yang diminta sahaja. Kekalkan naratif, aset, palet, durasi dan suara yang dipersetujui.
- Kekalkan susunan caption atas/bawah atau foreground yang sudah diluluskan walaupun berbeza daripada lalai tengah. Untuk masalah sync, ikut [kaedah CME V3](cme-v3-audio-captions.md); baiki cue dan entrance tanpa mereka semula suara atau gaya visual.
- Kekalkan rasa bertenaga melalui gerakan objek, mockup video sebenar, bayang lembut dan variasi kinetic typography. Elakkan flash atau lapisan warna penuh yang menyakitkan mata.

## Buang transition sebenar

1. Semak compositor akhir dan renderer scene, termasuk preset, intro/outro, wipe, swish, flash, crossfade, dissolve dan pertindihan timeline. Metadata `type: cut` sahaja tidak membuktikan transition telah dibuang.
2. Buang panggilan kesan skrin penuh pada hujung dan awal segmen. Gabungkan segmen seragam dengan potongan terus. Kekalkan animasi masuk/semasa/keluar objek individu selagi tidak menjadi transition skrin penuh.
3. Jangan menggantikan transition yang dibuang dengan zoom skrin penuh atau kesan lain tanpa arahan pengguna.

## Susun caption sebagai sebahagian komposisi

1. Tetapkan ruang caption di sekitar pusat menegak sebelum mengalihkan tajuk, wajah, kad, mockup dan CTA. Jangan sekadar menindih panel caption di atas komposisi lama.
2. Letakkan elemen utama dalam ruang atas dan bawah. Pastikan seluruh laluan animasi, overshoot, tilt, bayang, connector dan parallax tidak melintasi ruang caption sehingga mengganggu bacaan.
3. Gunakan maksimum dua baris, font tebal yang jelas dan kontras tinggi. Ukur teks menggunakan fon sebenar. Kekalkan baris dan kedudukan perkataan stabil apabila highlight perkataan aktif berubah.
4. Untuk contoh 1080 × 1920 yang telah dirender: panel x66, y866, w948, h188; DejaVu Sans Bold 56 px; lebar teks maksimum 888 px. Pada kanvas logikal 720 × 1280, simpan y570–710 untuk caption; letakkan kandungan utama sekitar y65–535 dan y745–1180. Ini titik mula, bukan koordinat wajib bagi semua nisbah, fon atau bahasa.
5. Uji caption sebenar melalui renderer subtitle akhir, bukan panel contoh sahaja. Periksa frasa terpanjang serta contoh satu dan dua baris pada saiz telefon.
6. Semak bingkai awal/tengah/akhir pada durasi scene sebenar. Untuk scene kurang dua saat, pendekkan entrance supaya mesej utama sempat dilihat. Jika hook perlu menunjukkan produk serta-merta, pastikan mockup video sudah wujud pada frame sifar.

## Kekalkan hasil yang sudah diluluskan

- Untuk revisi visual sahaja, guna semula audio, skrip, cue dan cap masa perkataan. Jangan menjana semula Google voice, menjalankan ASR baharu, mengubah pitch/tempo atau mengubah tempoh tanpa keperluan nyata.
- Simpan trek audio daripada video diluluskan sebelum menggantikan fail akhir. Jika codec/container serasi, gunakan stream copy (`-c:a copy`) supaya audio tidak dikod semula. Bandingkan payload paket AAC melalui `ffprobe -show_packets -show_data_hash sha256`; hash fail MP4 keseluruhan memang berubah selepas suntingan visual.
- Kekalkan SRT jika teks, timing dan pembahagian baris tidak berubah. Simpan kedudukan serta gaya dalam ASS atau format projek yang menyokongnya; SRT biasa tidak menyimpan susun atur panel ini.
- Render ke fail sementara, tunggu proses selesai, semak durasi dan nyahkod, kemudian ganti fail akhir secara atomik. Jangan membungkus, membaca untuk QA atau memuat naik fail yang masih ditulis.
- Kemas kini manifest, arahan bina semula dan pakej projek agar merujuk caption serta audio sebenar yang digunakan. Kekalkan identiti fail pengguna apabila menyimpan revisi.
- Ikut arahan foreground terbaru. Apabila aset mesti berada paling depan, jangan menampal semula footage/matte muka atau stetoskop di atasnya sehingga aset terpotong. Jika muka perlu dilindungi, ubah laluan/kedudukan aset dan semak hasil; gunakan occlusion hanya apabila memang diminta dan mask telah diuji.

## Semakan akhir yang berkaitan

- Periksa setiap scene serta frame sebelum, tepat pada, dan beberapa frame selepas setiap potongan. Semak tiada baki wipe/flash dan caption tidak menutup subjek yang perlu dilindungi, tajuk, mockup atau CTA. Liputan muka yang dibenarkan pengguna bukan ralat; teks tetap perlu jelas dan aset tetap perlu lengkap.
- Periksa audio kekal sepadan, bilangan frame, FPS, dimensi, durasi dan hujung fail. Gunakan pemeriksaan warna penuh hanya sebagai petunjuk tambahan, bukan pengganti semakan visual.
- Tonton gerakan pada kelajuan biasa jika kemampuan tersedia. Jika hanya contact sheet dan semakan teknikal dapat dilakukan, catat batas itu dengan jujur; jangan mendakwa telah mendengar atau menonton audiovisual penuh.
- Hentikan ujian tambahan apabila risiko revisi telah disahkan. Jangan menjana semula suara atau mengulang keseluruhan penyelidikan untuk perubahan kedudukan caption.
