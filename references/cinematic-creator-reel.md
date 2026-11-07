# Gaya Cinematic Creator Reel

Gunakan nama ini apabila pengguna meminta **Gaya Cinematic Creator Reel**, **Cinematic Editorial Talking Head**, atau creator reel dengan penyampai, teks di belakang badan, kad terapung dan komposisi berubah. Jadikan ini pilihan pengarahan tambahan; kekalkan semua gaya terdahulu. Sesuaikan kepada topik, aset, nisbah, durasi, dialog dan tahap tenaga brief terbaru.

## Kandungan

1. Rujukan dan had pemerhatian
2. Identiti visual
3. Susunan lapisan dan teks di belakang subjek
4. Kad terapung 2.5D
5. Pertukaran komposisi, mosaic dan UI
6. Tipografi, kamera dan audio
7. Pelaksanaan dan QA
8. Contoh arahan

## 1. Rujukan dan had pemerhatian

Gunakan analisis visual pada 7 November 2026 daripada [reel hancybox yang diberi pengguna](https://www.instagram.com/reel/DfZ011XM62f/?mdxt=dGVjYmFqYmhpYWww). Pemain browser melaporkan durasi kira-kira 59.56 saat dengan media 1080×1920. Jangan menganggap tulisan HUD “60 FPS” sebagai pengesahan FPS fail atau menganggap gaya ini terhad kepada satu minit/format potret.

| Sampel waktu playback | Pemerhatian visual |
|---|---|
| Sekitar 0–3s | Penyampai berbaju merah, latar gelap bercahaya hangat, caption campuran fon dan inset grafik timeline; simbol/teks Claude kemudian muncul |
| Sekitar 4–5s | Komposisi menjadi pentas krim dengan kad aplikasi dan video penyampai dalam bingkai kecil |
| Sekitar 7–10s | Framing penyampai berubah; kata besar “TITLES” dan tulisan italic berada di belakang badan |
| Sekitar 10–11s | Beberapa kad video berperspektif bergerak di sisi dan hadapan penyampai |
| Sekitar 12–13s | Visual penyampai dipecahkan kepada panel bersudut bulat; panel bergerak dan mengubah komposisi |
| Sekitar 16s dan 31–40s | Kad laman/galeri dan demonstrasi UI menjadi fokus; latar terang dengan aksen limau serta caption di atas |
| Sekitar 48s | Foto watak, kad skrip, anak panah dan preview telefon disusun sebagai penjelasan input → hasil |

Anggap masa itu sebagai sampel playback, bukan ukuran tepat onset/keyframe. Bezakan hasil yang kelihatan daripada mekanisme penghasilannya. Caption pencipta menyebut **Higgsfield Genjutsu for Reels melalui Claude**; jangan mendakwa sumber dibuat menggunakan HyperFrames, RVM atau teknik tracking tertentu. Nama gaya ini ialah label pengarahan deskriptif yang dipilih bersama pengguna, bukan nama preset rasmi penyedia. Audio sumber tidak disahkan melalui pendengaran. Jangan menjanjikan padanan 100% atau mendakwa render baharu telah diuji hanya kerana panduan ini disimpan.

## 2. Identiti visual

- Kekalkan seorang penyampai sebagai anchor cerita. Bina elemen lain mengikut maksud frasa: perkataan penting → kad bukti → demonstrasi UI → hasil → CTA.
- Gunakan rupa sinematik dengan latar gelap, cahaya hangat/bokeh dan kontras terkawal apabila sesuai. Selang-selikan pentas terang/krim bagi penjelasan UI supaya hierarki berubah dengan tujuan.
- Gabungkan kinetic typography, video penyampai, gambar/kad bukti, panel bertopeng dan paparan aplikasi. Gerakkan lapisan berasingan; jangan menggantikan komposisi dengan satu poster penuh yang hanya di-zoom.
- Gunakan gradasi, bayang dan blur mengikut depth. Kekalkan warna kulit, produk dan kandungan skrin yang tepat serta satu fokus bacaan pada satu masa.
- Gunakan palet projek sendiri. Jangan menyalin pakaian merah, logo Claude/Higgsfield, warna jenama, wajah atau ayat promosi sumber tanpa keperluan brief/aset yang sesuai.
- Ikut pilihan pengguna untuk paparan bersih: jangan warisi label kecil REC, nombor/tajuk scene, timecode, FACE TRACK, bingkai kamera atau watermark. Tambah HUD hanya apabila diminta atau mempunyai fungsi yang jelas.

## 3. Susunan lapisan dan teks di belakang subjek

1. Bina z-order yang eksplisit: latar → grafik/teks depth → subjek beralpha → kad foreground → caption/CTA yang perlu terbaca.
2. Untuk footage manusia, gunakan matte temporal sebenar mengikut aliran RVM dalam `video-background-replacement.md` yang dipautkan oleh SKILL.md. Uji readiness/inferens dan cache mask; reset state pada cut. Jika input sudah mempunyai alpha yang sah, gunakan alpha itu.
3. Jika mengekalkan latar footage asal, gunakan video asal sebagai lapisan bawah, letakkan teks di atasnya dan komposit salinan foreground beralpha di hadapan teks. Selaraskan kedua-dua salinan pada sumber masa yang sama agar tiada ghosting.
4. Masukkan perkataan besar dari belakang atau sisi badan melalui mask, slide, scale-to-settle atau blur-to-sharp. Pastikan perkataan akhirnya dapat dikenal pasti walaupun sebahagiannya terlindung dengan sengaja.
5. Lindungi muka, tangan dan bukti produk mengikut brief. Kad boleh melintasi torso jika dibenarkan tetapi jangan menutup muka atau teks sumber yang perlu dibaca. Semak keseluruhan laluan entrance dan exit.
6. Periksa rambut, jari, bahu, tepi pakaian dan props yang dipegang. Gunakan mask override bagi props yang model manusia tidak mengekalkan dengan betul. Jangan menganggap segmentasi gambar tunggal membuktikan matting video stabil.

## 4. Kad terapung 2.5D

- Gunakan gambar, video atau screenshot sebenar dalam kad bersudut bulat. Kekalkan aspect ratio dan isi penting di dalam clip mask.
- Gabungkan perspektif parent, rotateY/rotateZ kecil, translate, skala dan bayang supaya kad mempunyai lapisan dekat/jauh. Ini ialah 2.5D; jangan mendakwa simulasi atau geometri 3D sebenar tanpa aset/perender yang sesuai.
- Bina laluan bersilang atau carousel kecil mengelilingi penyampai. Variasikan masa masuk, aras depth, arah dan saiz; jangan menggerakkan semua kad pada kadar serta lengkung yang sama.
- Gunakan beberapa kad pada beat yang memerlukan pilihan/bukti. Pastikan satu kad atau frasa utama sempat stabil untuk dibaca; kad sokongan boleh terus bergerak perlahan.
- Kecilkan, alihkan atau keluarkan kad yang selesai memainkan peranan sebelum aset baharu mengambil fokus. Gunakan kad yang relevan sebagai jambatan ke paparan telefon atau UI seterusnya.
- Ukur crop dan safe area selepas transform perspektif. Pastikan kad tidak melintas di luar kanvas tanpa sebab atau memotong produk/muka yang penting.

## 5. Pertukaran komposisi, mosaic dan UI

- Tukar framing dengan maksud: close-up untuk penegasan, medium shot untuk dialog/gestur dan paparan lebih luas bagi teks depth atau kad di sekeliling penyampai.
- Bawa penyampai daripada penuh skrin ke inset bersudut bulat apabila bukti/produk perlu menjadi hero. Kekalkan kesinambungan sumber video dan jam audio semasa perubahan layout.
- Untuk mosaic/split-panel, gandakan sumber yang sama dalam beberapa mask panel. Pastikan semua panel merujuk frame masa yang sama sebelum dileraikan; animasikan posisi, skala dan susunan panel sebagai handoff kepada scene berikutnya.
- Gunakan peleraian panel sebagai peralihan bermakna, bukan efek setiap kali shot bertukar. Jaga anatomi dan sambungan badan pada hold; pecahan visual sementara perlu jelas disengajakan.
- Bina UI showcase daripada screenshot/rakaman sebenar apabila tersedia: galeri → pilihan → input → butang → preview hasil. Zoom kepada tindakan yang perlu dilihat, bukan sekadar membesarkan seluruh halaman.
- Untuk menerangkan input → hasil, susun foto watak/aset, kad skrip dan anak panah menuju mockup telefon atau preview video. Labelkan bahan contoh sebagai ilustrasi apabila bukan demonstrasi produk sebenar.
- Gunakan hold yang cukup untuk skrin dibaca dan kembali kepada penyampai apabila cerita memerlukannya. Jangan menetapkan satu layout statik untuk keseluruhan video.

## 6. Tipografi, kamera dan audio

- Gabungkan sans-serif tebal dengan serif italic atau script terpilih. Gunakan italic/script untuk satu kata penekanan; kekalkan teks sokongan pendek dan mudah dibaca.
- Pelbagaikan entrance, aktiviti dan exit: word build, mask reveal, blur-swap, pop, scale-to-settle dan perubahan lokasi. Ukur glyph/font selepas dimuatkan; jangan memecahkan huruf Arab bersambung.
- Asingkan jam perkataan siap-baca daripada jam animasi supaya gerakan tidak melambatkan caption. Ambil cue daripada audio sebenar jika dialog/narasi wujud.
- Gunakan push-in, pull-back dan pan pada parent yang sesuai. Kekalkan koordinat scene, kad dan subjek supaya pergerakan kamera tidak menghasilkan crop muka atau drift yang tidak dirancang.
- Anggap muzik, whoosh, impak pendek, sentuhan kad dan ASMR sebagai keputusan produksi baharu mengikut brief. Jangan mendakwa bunyi itu telah didengar dalam rujukan. Duck muzik semasa suara dan periksa clipping.
- Kekalkan audio/dialog yang telah diluluskan; gunakan laluan suara pengguna sedia ada apabila narasi baharu diperlukan. Jangan menganggap imej watak akan menghasilkan pertuturan/lip-sync secara automatik; semak keupayaan penyedia dan bahan sebenar terlebih dahulu.

## 7. Pelaksanaan dan QA

Gunakan Python/FFmpeg bagi suntingan footage dan compositing yang sesuai. Gunakan HTML/SVG/CSS + GSAP melalui HyperFrames bagi komposisi/animasi baharu atau apabila pengguna menetapkan aliran itu. Pilihan gaya tidak mewajibkan penyedia Higgsfield atau menukar backend projek secara senyap. Baca `html-hyperframes-production.md`, `centre-word-showcase.md` dan aliran matting yang dipautkan oleh SKILL.md apabila mekanismenya diperlukan.

Catat gaya, sumber footage, matte/alpha, layer order, cue audio, laluan kad, tipografi dan backend sebenar dalam manifest. Gunakan masa deterministik, timeline seekable, fon/aset setempat dan video berclock sama. Nama gaya ini tidak menambah ID Atlas atau mengubah registry 922.

Render proof pendek yang merangkumi teks di belakang subjek, satu lintasan kad dan satu pertukaran layout/panel yang sukar. Periksa frame bersebelahan serta playback biasa: tepi matte stabil, tiada ghosting, muka selamat, kad tidak memotong isi penting, teks sempat dibaca dan inset video terus bersinkroni. Semak UI pada saiz telefon, ejaan, transisi, hujung CTA serta QA teknikal MP4/audio sebelum master diserahkan. Bezakan panduan gaya daripada hasil render yang benar-benar diuji.

## 8. Contoh arahan

`Guna @Buat Video Motion Grafik, Gaya Cinematic Creator Reel. Hasilkan MP4 60 saat menegak daripada bahan saya, dengan penyampai sebagai anchor, teks besar di belakang badan, kad video terapung 2.5D, satu transisi mosaic dan demonstrasi UI. Pelbagaikan komposisi, jaga muka dan teks asal, serta tambah muzik dan SFX mengikut aksi.`
