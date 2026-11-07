# Gaya Cinematic Papercut

Gunakan nama tepat **Gaya Cinematic Papercut** bagi gaya paper-collage sinematik yang pengguna namakan selepas menerima revisi video Malaysia Siber pada 7 November 2026. Terima juga sebutan cinematic paper cut / cinematic paper collage. Ini gaya pengarahan, bukan skill berasingan atau preset rasmi Atlas/HyperFrames.

## Rujukan yang diterima

Video contoh: `Malaysia_Siber_Gaya_Ekstrem_1080p.mp4`, Library `libfile_42cb4ef46b988191b6ea000bf3dadfb3`, versi 2 yang diterima dalam rekod penghantaran. Hasil: 120 saat, 1920×1080 melintang, 30 fps sebenar, 50 PNG fotografi kolaj unik beralpha, 54 mekanisme tipografi custom, muzik/SFX/ASMR tanpa VO. Pengguna menolak versi terdahulu kerana gambar berulang, latar objek tidak telus dan gerakan terlalu kecil.

Sumber boleh guna semula: `Malaysia_Siber_Gaya_Ekstrem_Projek.zip`, Library `libfile_029f885929748191a3611ad8aef36a3c`, versi 2 dalam rekod penghantaran. Dapatkan kandungan semasa melalui Library apabila perlu; jangan andaikan versi tidak berubah. Pek mengandungi 50 PNG, prompt/ledger, kamera/compositor, 54 fungsi tipografi, timing, skor, renderer segmen dan QA. Adaptasi kepada topik baharu; jangan guna semula skrip atau 50 imej siber secara automatik.

## Artwork dan alpha

- Gunakan potongan fotografi editorial dengan tekstur cetakan/halftone terkawal dan tepi kertas koyak nipis mengikut siluet. Campurkan manusia, tangan, objek dan dokumen yang bermakna kepada cerita. Bina kedalaman daripada beberapa PNG berasingan; jangan ratakan seluruh adegan menjadi satu poster.
- Gunakan alpha sebenar pada semua potongan. Latar gelap, kotak putih, corak checkerboard yang terbakar dalam imej dan halo legap bukan transparency. Periksa statistik alpha, penjuru, tepi serta lubang dalaman pada latar kontras sebelum render.
- Jangan gunakan SVG atau lukisan vektor sebagai pengganti prop untuk gaya ini. Gunakan aset raster asal atau jana cutout sebenar apabila diminta/dibenarkan. Bentuk clipping, huruf dan operasi compositor tetap boleh digunakan tanpa menjadikannya artwork prop.
- Untuk padanan contoh dua minit, gunakan sekurang-kurangnya 50 imej berbeza yang benar-benar kelihatan. Ubah jumlah jika brief menetapkan lain; jangan paksa 50 untuk klip pendek. Crop, warna, flip dan duplikasi imej yang sama tidak dikira sebagai imej unik baharu.
- Rekod ID, sumber/lesen atau prompt, hash, fail alpha dan shot penggunaan. Dalam padanan contoh, tetapkan setiap imej kepada satu shot berterusan; jangan mengitar semula beberapa imej untuk memenuhi kuota. Sambungan lapisan semasa peralihan dibenarkan tanpa mengira imej itu dua kali.
- Mulakan dengan palet charcoal/navy, ivory dan aksen coral atau warna topik. Kekalkan tekstur fotografi, perkadaran subjek dan konsistensi bahan; ikut palet pengguna jika berbeza.

## Kamera dan koreografi

Bina dunia kolaj berlapis dengan foreground, midground dan background pada jarak berbeza. Gerakkan kamera melalui objek, bukan sekadar menggoyang semua gambar beberapa piksel. Gunakan perubahan skala/framing yang ketara, dari komposisi luas kepada close-up, dengan perspektif dan occlusion yang jelas.

Pelbagaikan dolly-through, crane reveal, orbital fan, lateral tracking, overhead-to-front, rack focus, diagonal rise dan reverse reveal. Pilih berdasarkan maksud dan geometri adegan; jangan sekadar mengulang kitaran yang sama. Hantar perhatian daripada subjek kepada prop seterusnya sementara lapisan yang berlalu keluar melalui tepi frame. Gunakan foreground melintas, perbezaan kelajuan parallax, putaran perspektif dan blur gerak terkawal. Alih fokus beransur antara jarak, tanpa pertukaran blur binari yang mengejut.

Pastikan setiap imej yang dikira mempunyai waktu dan keluasan paparan yang bermakna. Memuatkan imej ke memori atau menamakannya dalam manifest tidak membuktikan ia muncul. Lindungi muka, elemen utama, ruang baca dan tepi siluet; jangan crop subjek secara tidak sengaja.

## Tipografi dan audio

Gunakan frasa pendek berturutan dengan animasi masuk, semasa dan keluar yang pelbagai. Ubah kedudukan, saiz, tracking, pivot, mask, jenis gerak dan hierarki mengikut makna. Pastikan fasa siap-baca jelas walaupun kamera bergerak laju. Untuk padanan contoh dua minit, sediakan 54 mekanisme berbeza; perubahan warna atau penggunaan berulang satu mekanisme bukan variasi baharu.

Gunakan preset Atlas sebenar jika dipilih dan tersedia; jejak fungsi/ID yang benar-benar dirender. Jika menggunakan mekanisme custom, laporkan sebagai custom dan jangan menambah kiraan registry Atlas. Kekalkan teks yang diluluskan dan nilai akhir nombor tepat. Jangan tambah label kecil nombor/tajuk scene, sumber, REC, HUD atau watermark tanpa diminta.

Selaraskan muzik rancak, hentakan rendah, whoosh mengikut perjalanan kamera, klik tipografi dan ASMR kertas dengan cue visual. Sesuaikan intensiti dengan topik. Mod tanpa VO ialah ciri contoh asal, bukan larangan narasi pada semua projek; ikut brief semasa dan aturan penyedia suara sedia ada.

## Pelaksanaan dan QA

Gunakan backend yang diminta dan tersedia. Sokong scene raster berperspektif melalui HTML/Canvas/Three.js + timeline yang sesuai atau compositor native. Rujukan yang diterima menggunakan native Canvas + Sharp + FFmpeg; jangan melabelnya sebagai hasil HyperFrames browser CLI. Nama gaya tidak menukar backend secara automatik.

Nilai keadaan daripada masa mutlak setiap frame, dengan seed dan kamera yang boleh di-seek. Untuk mesh raster bersubdivisi, komposit seluruh plane ke lapisan sementara dahulu, kemudian gunakan opacity sekali pada lapisan itu. Fade per segi tiga bersama klip bertindih menghasilkan garis grid; periksa close-up dan frame akhir semasa alpha kurang daripada satu. Kekalkan alpha premultiplied yang betul pada blur, trail dan blend fokus.

Render proof sukar sebelum master. Periksa entrance/fade, rack focus, mesh seam, teks bergerak, close-up dan penutup. Gunakan segmen terhingga yang disahkan jumlah framenya; cache mesti mengikut fingerprint kod, timing dan aset supaya revisi tidak menggunakan semula segmen lama. Satukan dengan audio berterusan dan enkod FPS sebenar, bukan menaikkan video FPS rendah.

Semak 50 hash/alpha apabila jumlah itu diminta, penggunaan visual sebenar, kepelbagaian mekanisme tipografi, seek deterministik, safe area, frame bersebelahan dan playback apabila tersedia. Sahkan MP4 akhir melalui metadata, jumlah frame, durasi, audio/true peak dan nyahkod penuh; periksa lagi hasil enkod, termasuk sebelum/selepas sambungan segmen dan frame terakhir. Bezakan semakan bingkai/teknikal daripada tontonan atau pendengaran yang benar-benar dilakukan. Simpan sumber, aset dan bukti QA yang berguna untuk revisi.
