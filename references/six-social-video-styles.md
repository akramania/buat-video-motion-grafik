# Enam gaya video sosial daripada rujukan pengguna

Gunakan enam gaya ini sebagai pilihan pengarahan tambahan dalam Buat Video Motion Grafik. Kekalkan Gaya Ekstrem, Salah Label, Learnfly dan gaya terdahulu. Pilih satu gaya utama; gabungkan aksen gaya lain hanya apabila brief memerlukannya. Nama gaya ialah label pengarahan yang dipersetujui pengguna, bukan nama blok rasmi HyperFrames atau ID preset Atlas.

## Kandungan

1. Asas pemerhatian dan sumber
2. Pemilihan gaya dan backend
3. Clean Product Commercial
4. Podcast Promo Layout
5. Headline News / TV Broadcast
6. Dark Hormozi Sales Edit
7. Soft UGC TikTok / Boutique Review
8. Fashion Editorial / Luxury Lookbook
9. Pelaksanaan, audio dan QA

## 1. Asas pemerhatian dan sumber

Gunakan pemerhatian visual browser pada 7 November 2026 daripada [siaran rujukan pengguna](https://www.facebook.com/share/p/1GxQg5jREy/), termasuk video dalam balasan komen. Empat contoh selipar lelaki menggunakan footage asas yang sama dengan grafik berlainan. Pemain melaporkan lima video pertama sekitar 9.89 saat dan contoh fesyen sekitar 15 saat, pada media 360×640. Jangan menganggap metadata pemain sebagai resolusi master, FPS asal atau bukti perisian pembuat.

| Gaya | Rujukan yang diperiksa | Asas visual |
|---|---|---|
| Clean Product Commercial | https://www.facebook.com/reel/1161338010170384 | Lelaki berjas, selipar hitam, tajuk putih–kuning, label ciri dan CTA |
| Podcast Promo Layout | https://www.facebook.com/reel/1649863310009770 | Footage sama dalam bingkai bulat, tajuk atas, waveform dan caption bawah |
| Headline News / TV Broadcast | https://www.facebook.com/reel/1590199489813147 | Footage sama dengan lower third berita, ticker dan inset produk |
| Dark Hormozi Sales Edit | https://www.facebook.com/reel/39667643692879517 | Footage gelap, teks tengah putih/kuning/hijau, bar kemajuan dan kad produk |
| Soft UGC TikTok / Boutique Review | https://www.facebook.com/reel/2217221525804006 | Wanita bertudung, kasut coklat, caption bulat putih/merah jambu dan shot pemakaian |
| Fashion Editorial / Luxury Lookbook | https://www.facebook.com/reel/1774001880345142 | Montaj pakaian, panel menegak, kad serif, perkataan besar dan end card |

Bezakan pemerhatian daripada resipi produksi di bawah. Semakan sumber meliputi bingkai sepanjang playback serta perubahan komposisi; audio tidak disahkan melalui pendengaran. Jangan mendakwa fon tepat, easing tepat, waveform yang benar-benar dipacu audio, muzik atau SFX sumber telah dikenal pasti. Angka timing yang dicadangkan di bawah ialah keputusan pengarahan baharu, bukan ukuran keyframe sumber. Jangan menjanjikan padanan 100% atau menganggap enam resipi ini telah diuji melalui render baharu hanya kerana panduannya disimpan.

## 2. Pemilihan gaya dan backend

| Nama / alias arahan | Gunakan untuk |
|---|---|
| Clean Product Commercial; Commercial Produk Bersih; iklan produk clean | Demo produk dengan ciri dan CTA yang jelas |
| Podcast Promo Layout; Podcast Promo; gaya podcast | Promo penyampai atau petikan perbualan dengan bingkai editorial |
| Headline News; TV Broadcast; gaya berita TV | Grafik siaran, headline bertukar dan maklumat berterusan |
| Dark Hormozi; Dark Hormozi Sales Edit | Caption jualan dominan dan penekanan kata demi kata |
| Soft UGC TikTok; Boutique Review; gaya TikTok ringkas | Ulasan natural, fesyen, produk pengguna dan caption lembut |
| Fashion Editorial; Luxury Lookbook; lookbook fesyen | Montaj foto/video fesyen dan penutup tawaran berkelas |

Untuk suntingan footage, teruskan laluan Python/FFmpeg sedia ada bagi potongan, crop, caption dan compositing. Gunakan HTML/SVG/CSS + GSAP melalui HyperFrames bagi grafik baharu atau apabila pengguna menetapkan aliran HyperFrames; render lapisan berasingan jika sesuai. Pilihan gaya tidak menukar backend secara automatik. Hormati backend yang diminta pengguna dan laporkan sekatan sebenar jika laluan itu gagal.

Gunakan footage/gambar pengguna atau aset yang sesuai dan dibenarkan; jangan menganggap HyperFrames menghasilkan manusia, produk atau close-up sumber secara automatik. Kekalkan identiti, dialog dan kandungan produk yang telah diluluskan. Adaptasi kepada topik lain tanpa menyalin jenama, ayat jualan, harga atau produk contoh. Jadikan format 9:16 sumber sebagai rujukan komposisi sahaja; bina semula susun atur untuk nisbah dan durasi yang diminta.

## 3. Clean Product Commercial

- Bina cerita ringkas: hook produk → ciri pertama → bukti dekat → ciri seterusnya → hero produk → satu CTA. Pilih shot mengikut bukti yang benar-benar ada.
- Letakkan tajuk ringkas di atas dengan fon sans-serif tebal, putih dan satu warna aksen. Kekalkan muka dan produk utama terbuka.
- Potong antara medium shot penyampai, close-up struktur/bahan dan demonstrasi penggunaan. Gunakan crop atau punch-in ringan apabila membantu melihat ciri; jangan menukar semua shot menjadi zoom berulang.
- Bina label ciri berbentuk pil dengan kontras tinggi, titik/ikon kecil dan bayang lembut. Masukkan dari sisi atau scale-to-settle, tahan ketika ciri kelihatan, kemudian keluarkan sebelum label baharu mengambil fokus.
- Masukkan kad gambar produk berbayang sebagai picture-in-picture apabila memberi bukti tambahan. Jaga nisbah produk dan laluan masuk supaya tidak melintasi muka atau teks sedia ada.
- Akhiri dengan produk besar di ruang bersih dan CTA berkontras tinggi. Gunakan vignette atau gradasi ringan hanya untuk membantu hierarki.
- Cadangan gerak: entrance label/kad 0.2–0.4 saat, sedikit overshoot dan hold yang cukup untuk membaca. Padankan dengan panjang frasa sebenar.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Clean Product Commercial. Sunting video produk ini kepada MP4 30 saat menegak dengan close-up ciri, label ringkas dan CTA yang saya beri.`

## 4. Podcast Promo Layout

- Bina pentas gelap daripada warna/blur footage, kemudian letakkan footage utama dalam bingkai bersudut bulat dengan bayang terkawal.
- Susun tajuk kekal di atas, bingkai penyampai di tengah, caption frasa di bawah dan waveform pada jalur tersendiri. Kekalkan margin antara keempat-empat kawasan.
- Gunakan label editorial seperti PODCAST atau episod jika berkaitan. Gunakan LIVE/ON AIR hanya apabila konteks sebenar menyokong label itu; label tersebut bukan elemen wajib gaya.
- Potong footage kepada close-up atau B-roll di dalam bingkai yang sama supaya identiti layout berterusan. Masukkan inset produk berasingan dengan entrance/hold/exit yang jelas.
- Gunakan caption sans-serif tebal putih dengan kata penting berwarna aksen. Tukar mengikut frasa audio, bukan mengulang seluruh tajuk sebagai subtitle.
- Untuk waveform yang dipanggil audio-reactive, suapkan envelope/RMS audio sebenar pada masa timeline yang sama. Jika hanya animasi hiasan, nyatakan sebagai waveform dekoratif dan jangan mendakwa analisis suara.
- Cadangan gerak: fade/slide pendek untuk bingkai dan inset; animasi waveform boleh berterusan sementara tajuk stabil. Jangan menggoncang seluruh pentas.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Podcast Promo Layout untuk petikan ini. Hasilkan MP4 45 saat dengan bingkai bulat, tajuk atas, caption frasa dan waveform mengikut audio sebenar.`

## 5. Headline News / TV Broadcast

- Bina grafik siaran berlapis: identiti segmen di atas → footage → jalur kategori → panel headline → maklumat sokongan → ticker bawah. Utamakan satu headline pada satu masa.
- Gunakan panel putih dengan teks hitam dan kata penting merah; letakkan aksen kuning atau warna jenama pada label kategori. Jaga kontras apabila footage bertukar.
- Tukar headline mengikut bukti atau topik shot melalui mask wipe, slide atau blur-swap pendek. Jangan biarkan glyph separa kabur ketika teks perlu dibaca.
- Gerakkan ticker secara mendatar pada kelajuan bacaan yang sesuai. Gunakan pemisah, jarak dan loop tanpa lompatan; ticker tidak menggantikan maklumat penting dalam headline.
- Masukkan inset produk/bukti berbingkai dengan bayang ringan pada kawasan yang tidak menutup muka. Semak laluan animasi penuh, bukan posisi akhirnya sahaja.
- Gunakan label seperti Berita Produk atau Info Terkini mengikut konteks. Jangan mencipta status LIVE, waktu, sumber berita atau dakwaan BREAKING NEWS; gunakan butiran yang tepat atau label editorial yang sesuai.
- Adaptasi ketebalan lower third dan bilangan jalur untuk skrin telefon. Elakkan ticker, caption dan CTA serentak berebut ruang yang sama.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Headline News / TV Broadcast. Jadikan bahan ini video info produk 30 saat dengan headline bertukar, inset bukti dan ticker berisi maklumat yang saya beri.`

## 6. Dark Hormozi Sales Edit

- Gelapkan footage dengan overlay/gradasi dan vignette terkawal supaya teks menjadi fokus sambil subjek serta produk masih dikenal pasti.
- Letakkan frasa uppercase besar di tengah, lazimnya dua hingga empat perkataan pada satu beat. Gunakan font tebal, outline gelap dan bayang; bezakan kata penting dengan kuning atau hijau mengikut palet projek.
- Animasikan kata demi kata melalui pop/scale-to-settle, slide pendek, blur-to-sharp atau mask reveal. Pelbagaikan gerak mengikut penekanan; asingkan entrance, saat siap-baca, hold dan exit.
- Potong kepada B-roll ciri ketika frasa menerangkannya. Biarkan bukti produk kekal kelihatan; pindahkan teks jika pusat skrin menghalang aksi penting atau ruang muka yang dilindungi.
- Masukkan kad produk berbingkai aksen pada beat manfaat, kemudian keluarkan sebelum hero produk akhir. Bar kemajuan di bawah ialah pilihan, bukan kewajipan.
- Tutup dengan hero produk dan CTA besar yang diberi pengguna. Kekalkan punch-in dan kesan hentak setempat; jangan menjadikan semua teks bergegar sepanjang masa.
- Gunakan cue perkataan sebenar untuk caption. Cadangan entrance 0.12–0.25 saat mesti selesai sebelum frasa perlu dibaca; jangan memotong ayat semata-mata untuk mengejar tempo.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Dark Hormozi. Sunting video ini kepada MP4 30 saat dengan caption besar putih–kuning–hijau, B-roll produk dan CTA, tanpa menutup muka.`

## 7. Soft UGC TikTok / Boutique Review

- Kekalkan penyampai dan produk sebagai fokus. Gunakan susunan medium shot → demonstrasi/pemakaian → full body apabila relevan → close-up produk, berpandukan bahan sebenar.
- Pilih fon bulat tebal yang mudah dibaca, teks putih dan satu aksen lembut seperti merah jambu. Tambah outline/bayang cukup untuk latar yang berubah; jangan mendakwa fon sumber dikenal pasti.
- Paparkan caption dalam frasa pendek berhampiran bahagian bawah torso atau kawasan selamat yang tersedia. Gunakan highlight perkataan, pop kecil atau fade/slide pendek dengan cue audio sebenar.
- Gunakan tona warna hangat dan vignette ringan jika sesuai dengan produk. Kekalkan warna produk yang tepat; jangan menggelapkan atau mewarnakan produk sehingga mengelirukan.
- Utamakan potongan terus dan punch-in kecil. Kekalkan ekspresi, genggaman, langkah dan aksi yang membuktikan penggunaan; buang jeda hanya apabila tidak mengubah makna.
- Kurangkan kad hiasan, stiker dan transisi besar. Jangan memaksa rupa Dark Hormozi atau Gaya Ekstrem apabila pengguna memilih gaya lembut ini.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Soft UGC TikTok / Boutique Review. Kekalkan dialog video ini dan tambah caption bulat putih–merah jambu, cut kemas serta close-up produk.`

## 8. Fashion Editorial / Luxury Lookbook

- Bina urutan editorial: imej pemikat → kad tajuk ringkas → variasi rupa/butiran → frasa besar → end card dengan satu CTA. Gunakan foto atau video berkualiti yang mengekalkan potongan pakaian sebenar.
- Gabungkan paparan penuh, crop butiran dan panel menegak bertopeng. Masukkan panel secara stagger, geser atau scale-to-reveal; gunakan sumber sebenar pada setiap panel dan jaga nisbah.
- Selang-selikan serif berjarak luas pada kad tajuk gelap, serif italic untuk caption pendek dan sans-serif sangat besar untuk penekanan. Gunakan perbezaan tipografi bagi fungsi yang berbeza.
- Gunakan ruang kosong, palet hangat/neutral dan fade hitam atau pertukaran krim yang disengajakan. Light leak/glow boleh menjadi aksen apabila sesuai; jangan biarkan imej produk tidak terbaca.
- Animasikan foto melalui crop, pan atau push-in yang terarah; ubah komposisi dan susunan panel supaya montaj tidak menjadi zoom foto yang sama berulang kali.
- Bina end card berlapis: foto digelapkan → label sokongan kecil jika perlu → frasa italic → manfaat/tawaran utama → CTA berbingkai. Gunakan hanya stok, tarikh, harga dan tawaran yang diberikan atau disahkan.
- Kekalkan watak fesyen/pakaian sopan dan tapisan kandungan pengguna. Gaya ini boleh diadaptasi kepada produk lain tanpa menyalin wajah, pakaian atau jenama sumber.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Fashion Editorial / Luxury Lookbook. Hasilkan MP4 30 saat daripada foto ini dengan panel menegak, serif elegan, montaj butiran dan CTA yang saya beri.`

## 9. Pelaksanaan, audio dan QA

1. Catat nama gaya, aset sebenar, palet, font, susun atur, cue caption, shot/B-roll dan audio yang dipilih dalam manifest projek. Jika menggunakan preset Atlas, rekod ID sebenar; jangan memberikan ID baharu kepada nama gaya ini atau mengubah jumlah registry 922.
2. Ukur font selepas dimuatkan. Semak keseluruhan entrance/hold/exit untuk muka, tangan, produk, teks sumber dan safe area. Untuk ticker, waveform, panel dan caption, gunakan masa deterministik supaya seek ke frame yang sama menghasilkan keadaan sama.
3. Pilih muzik/SFX baharu mengikut brief, bukan berdasarkan andaian audio sumber: bunyi sentuhan ringan bagi label produk, aksen peralihan bagi berita, hentak perkataan terpilih bagi Hormozi, sentuhan lembut bagi UGC dan skor editorial bagi lookbook. Kekalkan dialog/audio yang telah diluluskan, duck muzik semasa pertuturan dan semak clipping. Hormati tanpa VO, tanpa muzik atau tanpa SFX apabila diminta.
4. Render proof komposisi utama dan satu pertukaran shot yang sukar melalui backend projek sebenar. Semak bacaan telefon, masa caption, ticker loop, waveform, bayang, crop dan akhir CTA; baiki isu sebelum master.
5. Jalankan QA MP4 sedia ada bagi resolusi, durasi, FPS, decode penuh, audio dan frame peralihan. Bezakan panduan gaya tersimpan daripada komponen yang benar-benar dipanggil dan video yang benar-benar dirender.
