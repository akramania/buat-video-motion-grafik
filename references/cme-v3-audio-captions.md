# Caption mengikut audio dan lapisan aset: CME V3

Gunakan pola ini untuk revisi video bernarasi yang sudah diluluskan, caption lewat, banyak preset teks dan bukti produk berlapis. Kekalkan panduan rig Seni Langkah Kecil untuk kartun; pola CME ini menangani penyuntingan footage, timing dan hierarki grafik. Jangan menjadikan aset hospital, skrip jualan atau angka projek ini kandungan wajib bagi video lain.

## Acuan yang diluluskan

V3 CME ialah video menegak 160 saat, 720 × 1280, 30 fps, dengan 108 frasa dan 69 ID teks unik daripada K/T/X/H/A/B. Ia mengekalkan visual foreground V2 serta audio yang sama, kemudian membetulkan timing caption berdasarkan pertuturan sebenar. Gunakan hasil V3 sebagai acuan bagi permintaan ini; tambahan dengue dan PowerPoint dalam V4 ialah revisi berasingan, bukan asas pembelajaran yang diminta.

Adaptasi mekanisme: label audiens jatuh dan bergegar; props jadual, PDF, laptop dan jam mengikut cerita; counter 20/100; logo sebenar; kad slide, potongan video PowerPoint berperspektif dan telefon dengan demo video yang benar-benar bergerak. Berikan objek fasa masuk, aksi/hold dan keluar dengan stagger. Selang-selikan sangat laju, laju dan sederhana tanpa memendekkan bacaan hingga hilang. Gunakan shadow, stroke, depth atau glow untuk kejelasan, bukan untuk menutup huruf. Tahan CTA terakhir hingga penghujung yang dipersetujui.

## Padankan skrip kepada pertuturan

1. Gunakan narasi asal atau audio bersih yang sudah diluluskan. Ukur audio sebenar; jangan menjana suara baharu untuk pembetulan caption.
2. Dapatkan timestamp perkataan melalui ASR/forced alignment yang tersedia. Dalam V3, Whisper Small tempatan pada CPU int8 menghasilkan 334 perkataan dikenali; penjajaran transkrip memadankan 335 token ternormal kepada 108 cue. Ini contoh pemprosesan tempatan, bukan keperluan memasang model/versi tersebut bagi setiap projek.
3. Padankan urutan skrip tepat secara monotonic. Normalkan angka dan nama produk untuk pemadanan sahaja, contohnya `20` dengan `dua puluh`, `PowerPoint` dengan `power point` dan `NotebookLM` dengan `notebook LM`. Kekalkan ejaan, ayat dan tanda baca caption pengguna; jangan menggantikannya dengan kesilapan pengecaman ASR.
4. Simpan onset/akhir perkataan, skor keyakinan, teks dikenali dan pemetaan cue. Flag perkataan tidak sepadan, onset meragukan, senyap panjang atau frasa terlalu pendek. Semak waveform, konteks jiran dan crop ASR tambahan; dengar jika keupayaan audio tersedia. Jangan mendakwa semakan pendengaran daripada waveform sahaja.
5. Gunakan perkataan pertama/akhir yang sepadan sebagai anchor setiap frasa. Jangan membahagi blok 10 saat mengikut panjang aksara, menganggap semua babak bermula dengan ucapan, atau menggeser seluruh caption dengan satu offset untuk masalah yang berbeza-beza.

Contoh V3: frasa bukti `20 slide` dalam babak 100–110 saat mempunyai onset model sekitar 102.86 saat, bukan 100.00. Crop tanpa VAD memberi julat 102.30–102.86, sementara tenaga pertuturan kuat bermula sekitar 102.8. Jadualkan visual sedikit mendahului onset yang disemak; rekod ketidakpastian, jangan mendakwa ketepatan fonetik mutlak.

## Pisahkan entrance, siap-baca dan hold

Jangan menyamakan `cue.start`, bunyi pertama dan saat semua teks terbaca. Entrance 120/210/350 ms yang bermula selepas onset boleh menyebabkan caption terasa lewat walaupun cue audio betul.

Simpan `audio_start`, `audio_end`, `motion_start`, `visual_start`, `complete_at`, `complete_design_clock`, `visual_end` dan exit secara berasingan. Gunakan titik mula berikut dan adaptasi kepada mekanisme serta FPS sebenar:

- Sangat laju: entrance 80 ms, pre-roll 80 ms.
- Laju: entrance 125 ms, pre-roll 110 ms.
- Sederhana: entrance 180 ms, pre-roll 150 ms.

Kira `motion_start = audio_start − pre_roll` dan `complete_at = motion_start + entrance`. Sasarkan teks utama siap sekitar onset +0–40 ms terhadap timestamp yang disemak. Pada 30 fps, satu frame menambah hingga kira-kira 33 ms; V3 mempunyai maksimum kelewatan terjadual 30 ms dan maksimum frame siap-baca 60 ms terhadap anggaran model. Angka ini metrik jadual/render, bukan jaminan terhadap masa fonetik sebenar.

Clamp `visual_start` kepada sifar tetapi kekalkan jam motion yang telah bermula lebih awal supaya cue pertama tidak lewat. Pastikan hanya satu cue memiliki kawasan caption pada setiap frame, kecuali reka bentuk overlap memang dirancang. Cap akhir cue sebelum entrance cue berikutnya. Panjangkan hold ke ruang senyap yang sesuai; jangan membiarkan cue pendek seperti Patient/Referral/Meeting hilang ketika perkataan masih disebut. Pendekkan atau buang exit sebelum mengorbankan bacaan. Kekalkan jurang sebenar dan tahan CTA penutup jika diperlukan.

Kalibrasi jam siap-baca melalui implementasi preset dan sprite teks sebenar, termasuk subtitle/support text. Jangan menggunakan satu completion clock untuk semua K, typewriter atau counter. Dalam V3, B06 memerlukan sekitar jam reka bentuk 3.65; menggunakan 3.48 membuat huruf terakhir muncul lewat semasa hold. K45 juga memerlukan semakan teks sokongan, bukan token utama sahaja. Kekalkan dispatch preset sebenar, bounds stabil, konfigurasi, fon, warna dan safe area; ubah timing tanpa menghilangkan mekanisme.

Padankan 20/100 kepada ucapan angka pada cue masing-masing. Semak kiraan awal, pertengahan, nilai akhir dan akhiran. Pastikan nilai akhir boleh dibaca ketika angka disebut. Jangan memulakan counter dua saat lebih awal hanya kerana babak bermula lebih awal. Letakkan aksen animasi dalam hold selepas mesej lengkap.

## Lapisan dan ruang bacaan

- Ikut urutan yang diluluskan: footage → aset/props/UI → kinetic caption. Letakkan aset lengkap di foreground apabila diminta; jangan memulihkan potongan muka atau stetoskop di atasnya sehingga skrin, huruf atau ilustrasi terpotong.
- Hormati arahan liputan muka terbaru. Jika pengguna membenarkan muka ditutup, jangan menambah semula larangan muka. Jika muka perlu jelas, reka kedudukan serta laluan aset, bukan menebuk aset dengan patch footage. Occlusion artistik perlu mask yang sengaja dirancang dan disemak.
- Kekalkan posisi atas/bawah yang diluluskan dalam revisi. V3 menggunakan caption bawah bagi banyak cue dan kawasan atas bagi beberapa cue sekitar 123–125 saat; jangan memindahkannya ke tengah semata-mata kerana lalai skill.
- Tetapkan safe rectangle setiap cue dan semak keseluruhan jejak entrance, hold, exit, glow serta shadow pada preview telefon. Bounds projek 720 × 1280 seperti x50–620 dan y810–1050 ialah contoh komposisi, bukan ukuran rasmi UI Facebook yang kekal. Sesuaikan kepada nisbah video dan kawasan UI sasaran sebenar.
- Gunakan keseluruhan nisbah slide/video dalam telefon atau kad. Crop hanya apabila disengajakan dan tidak membuang label/ilustrasi penting. Jangan menukar demo bergerak kepada satu screenshot. Bezakan perspektif 2.5D daripada model telefon 3D sebenar.
- Sahkan sumber tersedia sebelum mendakwa aset dimasukkan. Jika fail hilang atau tidak boleh dipindahkan, siapkan kerja yang tidak bergantung padanya dan minta hanya fail yang diperlukan untuk sambungan.

## Revisi dan bukti akhir

Untuk masalah timing sahaja, bekukan visual dan master audio yang diluluskan. Selaraskan semula cue serta entrance; jangan menggantikan fon, jumlah preset, layout, narasi atau muzik. Untuk revisi visual kemudian, guna semula cue V3 yang telah diluluskan; jangan jalankan semula ASR tanpa sebab.

Semak semua cue secara monotonic, tiada durasi negatif, cue hilang atau overlap tidak dirancang. Render sprite onset dan hold bagi setiap mekanisme unik; sampel typewriter, support text, counter dan cue pendek pada frame sebelum/onset/selepas. Ekstrak frame daripada MP4 akhir. Periksa safe area, perkataan lengkap, nilai angka dan aset foreground, bukan sekadar nama preset dalam manifest.

Salin audio yang diluluskan apabila serasi dan banding payload paket AAC atau hash audio yang diekstrak. V3 mengekalkan trek V2 tanpa perubahan. Semak frame count, FPS, resolusi, durasi, hujung dan decode penuh. Rekod batas QA: ASR ialah anggaran model dan contact sheet bukan bukti mendengar atau menonton audiovisual penuh.

Simpan master yang selesai, skrip/cue, bukti word alignment, aset, renderer/config dan audio yang diperlukan dalam projek revisi yang boleh dibina semula. Simpan hasil secara berterusan melalui aliran Library yang sesuai; pautan scratch sahaja tidak menjamin pemulihan selepas penyelenggaraan ruang kerja. Jika hanya video rata tersedia, nyatakan bahawa caption lama sudah terbenam dan revisi overlay bukan projek lapisan asal. Jangan memasukkan model ASR besar, dependency/cache RGB atau video pengguna ke dalam skill; simpan prosedur yang boleh digunakan semula di sini.
