# Revisi visual potret: dialog kinetik dan galeri berlapis

Gunakan pola ini untuk footage penyampai, dialog sebagai kinetic typography, banyak preset dalam satu scene dan showcase slide/poster. Baca bersama [integrasi preset teks](kinetic-preset-integration.md) serta [penjajaran audio CME](cme-v3-audio-captions.md). Jangan jadikan rupa, angka atau kelonggaran occlusion satu projek sebagai aturan semua video.

## 1. Bekukan bahagian yang sudah diluluskan

- Rekod skop revisi, versi sumber, EDL, timeline, cue, word anchors, audio serta SHA-256 sebelum mengubah grafik. Jika pemotongan senyap dan dialog berulang sudah diluluskan, kekalkan julat sumber serta jumlah frame; jangan memotong semula atau mengubah pertuturan untuk memuatkan animasi.
- Bina semula daripada footage asal dan konfigurasi projek. Jangan melapis teks baharu di atas video rata yang masih mempunyai subtitle terbakar. Jika hanya video rata tersedia, nyatakan batas itu dan dapatkan sumber/projek apabila perlu.
- Apabila diminta “tiada subtitle di bawah, gunakan kinetic typography”, matikan laluan renderer caption lama. Jadikan perkataan dialog yang bermakna sebagai bahan tipografi, bukan sekadar tajuk hiasan di atas subtitle lama. Kekalkan SRT sebagai rujukan masa jika berguna, tetapi jangan membakarnya atau menambah trek subtitle yang tidak diminta.
- Kekalkan suara asal/Google AI Studio yang telah diluluskan. Perubahan grafik tidak memberi sebab untuk menjana semula suara, ASR, muzik atau suntingan audio yang sudah tepat.

## 2. Buktikan preset sebenar, bukan jumlah nama

Pilih mekanisme berdasarkan dialog, bentuk perkataan, tempoh dan orientasi. Gunakan sasaran jumlah hanya apabila brief menyatakannya; ulang ID yang paling sesuai apabila itu membantu bacaan. Jangan memaksa 40 preset pada video pendek atau menggunakan preset yang tidak muat semata-mata untuk mencapai angka.

Panggil fungsi dispatch asal ketika menghasilkan frame master. Adaptasi boleh mengubah copy, pecahan perkataan/baris, susun atur terukur, palet, skala isotropik, alpha dan jam event sambil mengekalkan mekanisme asal. Jika mekanisme disalin atau ditulis semula untuk galeri, labelkan sebagai adaptasi tersendiri dengan `derived_from`, bukan panggilan preset asal.

Simpan manifest dan audit runtime secara berasingan:

- Manifest: `cue_id`, teks bermakna, `preset_id`, modul/fungsi sumber, konfigurasi, cue/word anchors, jam siap-baca, tempoh hold, ruang selamat dan sebab pemilihan.
- Audit master: ID, fungsi yang benar-benar dipanggil, jumlah dispatch frame, klip, julat jam reka bentuk, teks dan hash renderer. Asingkan audit preview/styleframe daripada render master; kosongkan audit lama bagi render baharu.
- Hitung ID unik daripada dispatch master yang benar-benar berlaku, kemudian padankan dengan manifest. Pengulangan, perubahan warna, preview sahaja dan adaptasi galeri tidak menambah bilangan ID asal. Audit panggilan belum membuktikan perkataan kelihatan: semak frame output juga.

## 3. Reka semula portrait, jangan crop demo landscape

1. Ukur teks sebenar dan susun baris/perkataan sebelum skala. Pilih fon yang sesuai dengan lebar potret; jangan meratakan huruf secara horizontal untuk memuatkannya.
2. Ukur bounds alpha yang kelihatan pada entrance, pertukaran baris, hold dan exit, termasuk glow/stroke serta overshoot. Gunakan satu union bounds yang stabil bagi unit animasi supaya saiz tidak berdenyut akibat crop yang berubah setiap frame.
3. Hadkan keseluruhan laluan gerak kepada margin selamat, bukan pose akhir sahaja. Semak kedua-dua tepi potret bagi row-swap dan glyph yang melantun keluar.
4. Tentukan kawasan muka/subjek bagi setiap shot dan sepanjang pergerakan, bukan satu kotak tetap untuk semua klip. Wide/body shot dan close-up memerlukan ruang berbeza.
5. Hormati izin liputan semasa projek. Jika badan boleh ditindih, manfaatkan ruang itu. Jika pengguna membenarkan sedikit overlap muka, kekalkan ia minimum dan jangan menutup mata, mulut atau ekspresi utama; jangan simpan izin itu sebagai lalai projek lain.
6. Pisahkan stage tipografi daripada artwork apabila slide/poster perlu dibaca. Pada showcase, boleh kecilkan penyampai kepada inset dan pindahkan dialog ke stage atas yang jelas. Jangan tampal semula muka di atas kad sehingga kandungan kad terpotong.

Ukur saiz huruf yang benar-benar terhasil selepas transform dan semak preview skala telefon. Jangan menganggap saiz fon dalam konfigurasi sama dengan saiz output selepas crop/skala, atau menjadikan satu ukuran projek sebagai had fon universal.

## 4. Pisahkan kelajuan gerak daripada masa bacaan

Gunakan jam scene, jam event setempat, word anchors dan hold yang berasingan. Tentukan jam siap-baca setiap mekanisme pada teks sebenar, kemudian petakan entrance sederhana/laju/sangat laju kepada onset. Jangan meretime keseluruhan kitaran preset lima saat secara seragam untuk cue yang panjang atau pendek.

- Benarkan aksen sangat laju tetapi kekalkan frasa lengkap cukup lama untuk dibaca. Pendekkan exit sebelum mengorbankan hold; jangan memecutkan suara.
- Bagi tiga reaksi pendek berturut-turut seperti “Zap / Zup / Zap”, bina perkataan secara kumulatif dan kekalkan perkataan terdahulu dalam hold. Kekalkan masa audio/word anchors asal; ubah persistence visual sahaja.
- Tahan frasa penutup hingga frame terakhir apabila ruang visual penutup sudah tersedia. Jangan mengubah SRT, durasi atau audio semata-mata kerana cue teks berakhir lebih awal.
- Semak frame sebelum onset, saat lengkap dan selepas onset. Jangan menganggap glyph yang belum tiba pada frame entrance sebagai perkataan hilang; semak juga bahawa semua perkataan akhirnya benar-benar muncul.

## 5. Animasi slide/poster sebagai artwork asli

Gunakan fail asal, nisbah asal dan kandungan penuh pada hero hold. Rekod hash aset supaya revisi tidak menukar ejaan, reka letak atau butiran artwork. Bina lapisan dengan aperture/mask, depth rack, pane reveal, whip exchange, perspective dan registration marks yang sesuai; jangan sekadar mengulang zoom pada imej statik.

Gunakan jam kad dan jam tipografi yang bebas tetapi koreografi perhatian bersama. Gerak masuk/keluar boleh pantas dan berlapis; berikan satu hold front-facing yang bersih sebelum menukar hero. Letakkan aksen di luar artwork, bukan lapisan warna atau teks baharu di atas kandungan asal. Bezakan crop sementara yang disengajakan ketika reveal daripada artwork yang kekal terpotong.

Rekod bounds artwork, stage tipografi, presenter inset, z-order, mekanisme asal/adaptasi dan interval bacaan dalam manifest. Semak geometri pada semua frame aktif jika mampu. Banyak lapisan dalam satu scene bukan alasan untuk menggerakkan semua lapisan dengan kekuatan yang sama.

## 6. Uji kontras pada permukaan sebenar

Periksa latar tepat di belakang glyph, termasuk baju, kulit, kad dan jalur preset; label “scene gelap” tidak menjamin teks cerah terbaca. Gunakan stroke/rim legap setempat, ink gelap atau penempatan lain apabila perlu, tanpa menghidupkan semula subtitle strip yang dilarang.

Semak mekanisme inverse/knockout dan callback warna aktif per preset. K36/K41/K45 menggunakan permukaan atau polariti yang perlu dijaga; satu callback umum boleh membuat perkataan aktif hilang atau sama warna dengan plate. Semak setiap jalur secara berasingan: sebagai contoh, ink krim boleh sesuai pada biru tetapi ink navy diperlukan pada jalur emas muda. Selepas mengubah callback, semak alpha, glif aktif dan glif biasa pada frame sebenar.

## 7. QA, pembaikan dan serahan

1. Render petikan dengan mekanisme paling berisiko dahulu: row-swap, inverse ink, cue sangat pendek, teks di atas baju cerah, showcase dan penutup.
2. Semak completed-word moment setiap cue, urutan frame rapat sekitar motion/cut, serta skala telefon. Gunakan review visual bebas jika tersedia. Periksa MP4 akhir yang diekstrak semula, bukan compositor sahaja.
3. Selepas pembaikan, render semula segmen terjejas, susun semula pada jam frame yang sama, kemudian sahkan EDL/SRT/timeline, sumber artwork dan audio yang sepatutnya tidak berubah.
4. Gunakan hash PCM atau payload AAC apabila audio benar-benar dikekalkan; hash keseluruhan MP4 tidak sesuai kerana video telah berubah. Jika encoding audio berubah, jangan mendakwa identiti bit berdasarkan persamaan durasi atau loudness.
5. Semak dimensi, FPS, frame count, durasi audio/video, subtitle stream, loudness/true peak dan decode penuh. Semak tag warna pada master selepas concat/remux; flag encoder segmen belum tentu kekal pada fail akhir.
6. Periksa flag freeze/black secara kontekstual. Hold artwork yang sengaja stabil bukan automatik rosak; dokumentasikan semakan, jangan menyembunyikan flag atau menyamakan decode berjaya dengan semua ujian lulus.
7. Tonton kelajuan biasa dan dengar audio apabila keupayaan tersedia. Jika tidak, labelkan “semakan frame/teknikal sahaja”; jangan mendakwa kelancaran, sebutan, lip-sync atau semakan audiovisual penuh daripada ASR, waveform, contact sheet dan decode.
8. Simpan master serta projek yang boleh dibina semula. Jika had lampiran lebih kecil daripada had storan, sediakan salinan mampat yang dilabel jelas dan kekalkan master. Pek kod/aset boleh mengecualikan footage asal yang besar hanya dengan inventori, hash serta arahan memulihkannya; jangan menyebut pek itu lengkap tanpa sumber. Jangan masukkan video pengguna, model ASR atau cache frame ke dalam skill.

## Bukti kes 10video V2 dan batasnya

V2 mengubah visual sambil mengekalkan 14 julat potongan, 60 cue, 177 word anchors, 81.5 saat dan 1,956 frame pada 1080 × 1920/24 fps. Sebanyak 40 ID K benar-benar digunakan: K01–K45 kecuali K04, K19, K25, K39 dan K43. ID yang dikecualikan tidak sesuai dengan dialog/layout kes ini, bukan larangan penggunaan. Adaptasi galeri tidak dimasukkan dalam angka 40; jumlah registry skill kekal 842.

Bukti projek merangkumi audit dispatch master, hash edit/audio/artwork, decode penuh, semua 60 completed-word moments, sampel encoded master, urutan sekitar 13 cut, 703 frame geometri galeri serta pembaikan row-swap, polariti ink, build tiga reaksi, kontras baju/jalur dan hold akhir. Normal-speed playback, pendengaran perseptual dan ketepatan fonetik tidak berjaya disahkan. Bezakan pencapaian ini daripada janji bahawa setiap frame dinilai secara perseptual atau setiap projek mesti menggunakan bilangan preset yang sama.
