# Sunting ceramah Arab dengan subtitle Arab–Melayu

Gunakan aliran ini untuk ceramah Arab pengguna, termasuk permintaan "edit ceramah macam Filem dan Dajjal". Hasilkan MP4 sebenar, kekalkan pertuturan asal dan sesuaikan framing serta bacaan kepada telefon. Gunakan arahan projek terbaru untuk mengatasi mana-mana lalai di bawah.

## Kandungan

1. Skop dan turutan kerja
2. Transkrip Arab dan terjemahan Melayu
3. Cue dan highlight terjemahan
4. Reka bentuk potret dan tulisan Arab
5. Framing, masking dan penutup
6. Audio dan eksport
7. Semakan hasil dan simpanan
8. Rujukan projek yang telah dirender

## 1. Skop dan turutan kerja

- Gunakan 9:16, lazimnya 1080 × 1920, dengan tajuk kekal sepanjang video, subtitle Arab di atas Melayu, serta highlight emas pada teks Melayu. Kekalkan FPS sumber yang sesuai; jangan mewarisi 25 fps atau durasi klip lama tanpa pemeriksaan.
- Periksa metadata, semua sudut kamera, cutaway pendengar, dissolve, audio, pembukaan dan dua saat terakhir. Bezakan kekangan detail rakaman asal daripada saiz kanvas eksport.
- Sediakan transkrip Arab dan terjemahan Melayu lengkap sebelum render. Apabila pengguna meminta "tulis dulu subtitle penuh", hantar teks Melayu di chat dahulu dan berhenti pada fasa yang diminta. Apabila pengguna menyatakan setuju, mula atau terus siap, sambung kerja yang telah dibenarkan tanpa meminta persetujuan semula. Jangan tambah syarat kelulusan bagi arahan menghasilkan video penuh secara terus.
- Bekukan ejaan, istilah dan terjemahan yang telah diluluskan. Ubah pembahagian cue, line break atau layout untuk bacaan; jangan merumuskan semula isi secara senyap.
- Gunakan tajuk yang diberi. Jika tajuk tidak diberi dan kerja penuh dibenarkan, pilih tajuk ringkas yang mewakili isi. Jangan menggunakan semula tajuk, durasi, ayat atau naratif projek rujukan sebagai kandungan lalai.
- Kekalkan suara penceramah asal. Lalai Google AI Studio bagi narasi baharu dalam skill utama tidak terpakai kepada pertuturan rakaman yang sedang disunting. Tambah VO, muzik atau SFX hanya apabila diminta atau jelas sebahagian daripada brief.

## 2. Transkrip Arab dan terjemahan Melayu

1. Ekstrak salinan audio untuk ASR, misalnya WAV PCM 16-bit mono 16 kHz; kekalkan fail audio asal untuk master. Gunakan ASR setempat yang tersedia dengan bahasa `ar` dan timestamp perkataan apabila disokong.
2. Semak confidence, nama, istilah agama, pengulangan, perkataan terpotong dan akhir klip. Gunakan model lain atau crop ASR bagi bahagian yang meragukan; jangan memasang atau memuat turun semua model secara automatik. Dalam projek rujukan, large-v3-turbo dan large-v3 dibandingkan pada CPU int8. Dua model yang bersetuju masih tidak membuktikan setiap kata tepat.
3. Bezakan transkrip mesin daripada teks Arab editorial. Betulkan kesilapan ASR yang jelas berdasarkan bukti serta konteks; jangan mencipta perkataan yang tidak dapat dipastikan. Dengar petikan jika kemampuan audio benar-benar tersedia. Jangan mendakwa telah mendengar berdasarkan teks ASR atau waveform sahaja.
4. Terjemahkan sepenuhnya kepada Bahasa Melayu Malaysia yang lancar dan sesuai dengan bahasa ceramah/pengajian. Kekalkan penekanan, pengulangan yang bermakna, tahap kepastian, soalan dan penafian penceramah. Pilih makna istilah mengikut konteks; jangan memaksa satu padanan ke semua ceramah.
5. Kekalkan keterangan seperti "hadis ini daif" dan perbezaan antara petikan, tafsiran penceramah serta terjemahan. Bagi istilah luar biasa yang sedang dihuraikan, kekalkan istilah itu dengan tanda petik apabila perlu, seperti "filmani" dalam projek rujukan; jangan mengesahkan etimologi atau dakwaan tambahan melalui terjemahan sendiri.
6. Semak teks dan rujukan al-Quran atau petikan agama apabila perlu, mengikut aturan sumber dan tulisan Arab dalam skill utama. Jangan menambah ayat, sumber, nama perawi, hukum atau kesimpulan akidah yang tidak disebut. Kekalkan harakat/tanda Quran apabila ada; jangan membuangnya untuk mengatasi fon yang tidak lengkap.

### Pulihkan laluan ASR apabila perlu

- Jika klien muat turun memerlukan SOCKS, pasang dependency yang dilaporkan hilang sahaja, misalnya `socksio`; jangan menganggap perkhidmatan/model tidak dapat dicapai berdasarkan dependency yang hilang.
- Jika PyAV menolak parameter `metadata_errors`, elakkan laluan decode yang tidak serasi dengan menghantar array PCM NumPy terus kepada `model.transcribe`. Pastikan terlebih dahulu WAV mono 16 kHz dan sampel 16-bit, kemudian tukar kepada float32 dalam julat −1..1. Ini jalan pemulihan yang telah digunakan, bukan jaminan keserasian semua versi.
- Simpan model dan dependency ASR sebagai cache runtime; jangan menambahnya ke dalam skill atau pakej projek pengguna.

## 3. Cue dan highlight terjemahan

- Gunakan audio Arab sebagai jam master. Simpan sekurang-kurangnya `start`, `end`, `visual_start`, `visual_end`, `ar`, `bm` dan senarai highlight dengan teks serta anchor masa. Kekalkan bukti word alignment dan pembetulan editorial untuk revisi.
- Bahagikan mengikut frasa bermakna dan kelajuan bacaan. Sasarkan Arab 1–2 baris dan Melayu 1–3 baris; benarkan 4 baris pendek hanya apabila masih jelas pada telefon. Gabungkan klausa berkaitan apabila terjemahan lebih panjang daripada frasa audio yang sangat singkat, tanpa menghilangkan perkataan yang diluluskan.
- Paparkan keseluruhan frasa dari awal cue. Gerakkan highlight ke perkataan/frasa pendek yang berkaitan, dengan teks lain terus kelihatan; jangan menjadikan typewriter lambat sebagai satu-satunya cara membaca terjemahan.
- Padankan highlight Melayu kepada unit makna Arab secara monotonic. Gunakan anchor perkataan/frasa sebenar dan agihkan perkataan Melayu dalam unit tersebut. Susunan bahasa mungkin berbeza; jangan mendakwa highlight terjemahan sebagai timestamp fonetik Melayu apabila tiada suara Melayu.
- Gunakan pre-roll kecil yang disemak, misalnya satu frame 40 ms pada 25 fps, bukan offset besar seragam untuk semua masalah. Clamp permulaan kepada sifar. Pastikan satu cue sahaja memiliki kawasan subtitle pada satu masa.
- Tahan frasa melalui jeda semula jadi untuk memberi masa membaca. Akhiri sebelum cue berikutnya; elakkan teks lama bertindih, hilang sebelum ucapan selesai atau ruang kosong yang tidak disengajakan. Tahan soalan penutup hingga hujung yang sesuai.
- Gunakan highlight emas di belakang perkataan aktif dengan teks gelap, manakala perkataan lain kekal putih/ivory. Ukur padding supaya highlight tidak menutup huruf atau menghilangkan jarak perkataan bersebelahan. Elakkan kotak latar penuh yang menenggelamkan rakaman kecuali diminta.

## 4. Reka bentuk potret dan tulisan Arab

Gunakan gaya biru gelap, ivory dan emas sebagai titik mula bagi ceramah ini. Kekalkan hierarki tajuk → penceramah → Arab → Melayu. Susun semula layout jika sumber atau brief berbeza; koordinat di bawah ialah contoh projek 1080 × 1920, bukan aturan semua video.

| Elemen | Contoh yang telah digunakan |
| --- | --- |
| Palet | Navy `#09111C`, ivory `#F8F7F0`, emas `#EEC26B`, dakwat highlight `#0F1926` |
| Tajuk | Lora 600, sekitar 93 px, kawasan atas; tajuk kekal pada semua frame |
| Arab | Noto Naskh Arabic 600, sekitar 60–64 px, di atas Melayu |
| Melayu | Manrope 700, sekitar 54–60 px mengikut kepadatan |
| Lebar teks | Sekitar 900–920 px dengan margin sisi yang diperiksa |
| Kawasan subtitle | Susunan adaptif sekitar y1290–1784; ruang bawah kekal untuk bacaan telefon |
| Footage | Crop berlapis di tengah, diadun lembut ke navy pada tepi atas/bawah |

- Gunakan fon berlesen beserta lesen, sama ada daripada aset skill yang tersedia atau sumber asal yang sah. Jangan menganggap satu sampel Quran membuktikan semua glif telah diuji.
- Gunakan shaping RTL sebenar, misalnya Pillow dengan RAQM, `direction="rtl"` dan `language="ar"`. Wrap teks Arab dalam urutan logikal, kemudian shape setiap baris; jangan membalikkan huruf secara manual.
- Ukur teks dengan fon sebenar. Semak tanda baca, ligatur, harakat, glyph yang hilang, ascender/descender, padding highlight dan keseluruhan bounding box. Jangan membetulkan overflow dengan mengecilkan semua teks sehingga sukar dibaca.
- Letakkan subtitle di kawasan bacaan yang tidak menutup wajah. Laraskan kedudukan blok untuk cue panjang sambil mengekalkan hierarki serta margin selamat. Arahan kedudukan pengguna terbaru mengatasi lalai caption tengah dalam skill utama.

## 5. Framing, masking dan penutup

- Ikut penceramah pada setiap sudut kamera; gunakan crop dan zoom lembut yang mengekalkan nisbah asal, muka, serban/rambut dan gerak tangan yang penting. Jangan menggunakan satu crop tetap untuk semua sudut atau memotong muka pada shot sisi.
- Gabungkan pengesanan cut dengan pemeriksaan bingkai. Dissolve panjang dan perubahan sudut berkontras rendah mungkin tidak dikesan oleh threshold cut yang tinggi. Kekalkan cutaway pendengar asal apabila membantu kesinambungan.
- Gunakan koordinat crop pecahan ketika resampling, misalnya `resize(..., box=(left, top, right, bottom))`, supaya zoom perlahan tidak melompat akibat pembundaran crop pada setiap frame.
- Kekalkan framing lebih luas apabila detail sumber kecil; jangan menjanjikan pemulihan detail hanya melalui upscale. Gunakan crop/zoom yang bermakna, bukannya gerakan rawak pada setiap perkataan.
- Gunakan masking/pembuangan latar hanya apabila membantu komposisi dan backend benar-benar tersedia. Periksa tepi serban, tangan, mikrofon, motion blur dan temporal flicker. Jika crop serta feather sudah sesuai, teruskan dengannya dan jangan mendakwa latar telah dibuang.
- Feather tepi footage mengikut sempadan lapisan sebenar serta kawasan global supaya tiada garis mendatar keras di titik mula/akhir imej. Pastikan feather tidak memadamkan bahagian kepala.
- Semak dua saat terakhir serta sempadan fail. Jika sumber berakhir ketika dissolve masih separuh, gunakan bingkai bersih selepas ucapan selesai untuk hold singkat atau potong ke penutup bersih yang dibenarkan. Kekalkan audio/timing yang dipersetujui; jangan membekukan mulut ketika ucapan aktif atau menyalin masa hold daripada projek lama. Dalam rujukan, bingkai bersih 73.28 s ditahan hingga 74.36 s sahaja.

## 6. Audio dan eksport

- Kekalkan kelajuan dan identiti suara asal. Laraskan bunyi berdasarkan ukuran; gunakan high-pass/penapisan ringan hanya jika perlu, tanpa memusnahkan konsonan Arab atau menghasilkan bunyi berair.
- Sasarkan aras selesa, misalnya sekitar −16 LUFS bersepadu dan true peak tidak melebihi −1 dBTP; ukur hasil sebenar. Projek rujukan mencapai −16.18 LUFS dan −2.30 dBTP. Jangan menganggap satu tetapan normalisasi menghasilkan angka sama untuk sumber lain.
- Elakkan fade audio yang memotong hujung perkataan. Jangan menggantikan suara atau menambah muzik secara senyap.
- Eksport MP4 H.264, `yuv420p`, audio AAC dan `+faststart`, dengan resolusi/FPS yang dipilih selepas memeriksa sumber. Tulis metadata warna yang sesuai dan kekalkan aspect ratio.
- Render sampel pendek sebelum master. Gunakan masa deterministik, bingkai berurutan, cache teks yang munasabah dan stream ke FFmpeg; jangan menahan semua frame dalam memori.

## 7. Semakan hasil dan simpanan

1. Bandingkan semua perkataan Melayu dengan teks yang telah diluluskan. Semak teks Arab editorial, cue monotonic, durasi positif, tiada overlap tidak dirancang dan tajuk hadir sepanjang video.
2. Periksa frame pembukaan, semua cue, shot lebar, shot sisi, cut/dissolve dan penutup daripada MP4 yang telah dienkod. Semak glyph, cropping, kontras, highlight serta ruang selamat; tambah pemeriksaan frame rapat dan playback biasa apabila tersedia. Contact sheet sahaja tidak membuktikan ketepatan audio atau kelancaran keseluruhan.
3. Apabila mengekstrak frame terpilih dengan `select` dan `tile`, gunakan `-fps_mode vfr` atau laluan passthrough yang sesuai. Semak jumlah halaman dan cue: output ber-FPS tetap boleh menduplikasi halaman pertama walaupun fail kedua mempunyai nama lain.
4. Semak metadata, bilangan frame, durasi, audio, loudness dan nyahkod penuh. Jika audio master hanya dimux semula, bandingkan hash paket AAC untuk mengesahkan ia tidak berubah.
5. Simpan MP4, SRT Arab dan Melayu, teks diluluskan, cue/anchor, fon berlesen, kod/config dan sumber yang diperlukan untuk revisi melalui aliran Library yang sesuai. Kekalkan identiti fail yang disunting. Jangan bergantung pada pautan scratch selepas penyelenggaraan ruang kerja.
6. Ringkaskan hanya perubahan yang benar-benar dibuat. Bezakan crop/feather daripada pembuangan latar, ukuran teknikal daripada semakan pendengaran, serta timestamp model daripada ketepatan fonetik.

## 8. Rujukan projek yang telah dirender

Gunakan `Filem_dan_Dajjal_Subtitle_dan_Projek.zip` sebagai contoh implementasi yang boleh dipulihkan melalui skill Library apabila kod/fon diperlukan. Library file ID semasa simpanan: `libfile_778ad9df888c8191a39b2593241778b5`. Resolve/read atau materialize mengikut aliran Library semasa; jangan menganggap fail scratch lama masih ada.

Pakej itu mengandungi `build_captions.py`, `render.py`, `finalize.py`, `captions/timeline.json`, SRT kedua-dua bahasa, fon dengan lesen, sumber dan bukti QA. Salin hanya komponen yang diperlukan ke projek baharu dan ubah semua teks, cue, kamera, dimensi, FPS, fail sumber serta masa penutup. Jika pakej tidak tersedia, teruskan menggunakan panduan ini dan alat setempat yang tersedia; jangan menjadikan rujukan itu syarat kelulusan atau mendakwa telah memuatkannya.

Jangan tambah video pengguna, model ASR, dependency cache atau hasil raster besar ke dalam skill ini. Kekalkan sumber projek dalam simpanan projek; simpan prosedur boleh guna semula di sini.
