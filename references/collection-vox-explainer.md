# Koleksi Documentary / Editorial Explainer (Vox-inspired)

Gunakan koleksi ini untuk explainer berasaskan bukti, dokumentari ringkas, sejarah, data, dokumen dan mekanisme. Baca indeks JSON `assets/style_collections/vox-explainer.json` untuk pemilihan mesin. Semakan sumber: **7 November 2026**.

## Kandungan

1. Kedudukan sumber dan kiraan
2. Prinsip pelaksanaan
3. Empat look daripada sumber
4. Dua belas pengembangan asal
5. Pemilihan dan QA

## 1. Kedudukan sumber dan kiraan

Caption reel pengguna menyebut “Vox Explainer” tanpa pautan repo. Kekalkan ketidakpastian itu: tiga projek bernama serupa di bawah tidak disahkan sebagai repo yang digunakan dalam reel.

- [bestuserever121/vox-explainer](https://github.com/bestuserever121/vox-explainer): README bahagian Styles menyenaraikan empat look `papier`, `dunkel`, `blaupause`, `riso`; `docs/spec.md` menerangkan scene berparameter.
- [CK42BB/vox-explainer-skill](https://github.com/CK42BB/vox-explainer-skill): pipeline API berasingan; `references/vox-style-guide.md` menerangkan penulisan dan kolaj editorial. Jangan mewarisi penyedia suara/API atau dakwaan kosnya.
- [HeyGen community Vox Explainer](https://github.com/heygen-com/hyperframes-community-skills/blob/master/skills/vox-explainer/SKILL.md): panduan plain-sight documentary dan rujukan layout/motion. Resipi frame ialah mekanisme komposisi, bukan tambahan look rasmi.

Koleksi ini mengandungi **16 resipi: 4 `native-source` + 12 `original-adaptation`**. Empat yang pertama mengekalkan nama look sumber; dua belas seterusnya ialah pengembangan pengarahan asal yang boleh dipadankan dengan look tersebut. Jangan menyebutnya 16 preset rasmi, 16 renderer siap atau 16 varian daripada satu repo. ID VX01–VX16 ialah label resipi dan tidak mengubah registry Atlas 922. Tiada pemasangan, panggilan API, render atau ujian upstream dilakukan melalui penambahan panduan ini.

## 2. Prinsip pelaksanaan

- Bina satu cerita yang dapat diikuti: persoalan konkrit → konteks → mekanisme → komplikasi → hasil. Gunakan satu objek pembawa atau hubungan kausal untuk menyambung beat; ubah susunan apabila bahan sebenar memerlukannya.
- Gunakan foto, scan, peta dan data sebenar yang dibenarkan. Nyatakan ilustrasi atau pembinaan semula apabila digunakan. Jangan mereka bukti, saksi, dokumen, angka atau keputusan eksperimen.
- Tentukan look dasar dan satu pengembangan naratif bagi setiap kelompok scene. Bezakan rupa permukaan daripada mekanisme penjelasan; perubahan warna sahaja tidak menjadi pengembangan baharu.
- Gunakan Python/FFmpeg untuk footage, HTML/SVG/CSS + GSAP melalui HyperFrames apabila sesuai atau diminta. Ikut runtime, aliran suara dan arahan pengguna sedia ada; panduan sumber tidak menukar backend secara automatik.
- Sesuaikan layout potret/landskap daripada ukuran teks dan safe area, bukan crop buta. Kekalkan bahan asal, muka serta teks sumber yang perlu dibaca. Jangan menyalin logo atau identiti Vox.
- Kekalkan tapisan pengguna: jangan gunakan tema LGBTQ, Halloween, Valentine, Christmas atau simbol/perayaan agama selain Islam. Pilih contoh neutral seperti pendidikan, sains, teknologi, sejarah institusi dan budaya Malaysia.

## 3. Empat look daripada sumber

### VX01 · Papier / Editorial Kertas

Asal: `native-source`. [Sumber](https://github.com/bestuserever121/vox-explainer#styles); bahagian: README.md → Styles; native token stil=papier.

- Visual: Gunakan pentas kertas putih hangat, grain halus dan tipografi hitam dengan sedikit rasa cetakan. Jadikan foto atau objek sebagai bahan editorial yang tersusun.
- Gerak: Bawa mata melalui objek, kata utama dan anak panah mengikut narasi, kemudian tarik kamera keluar untuk menunjukkan hujah lengkap.
- Kegunaan: Penerangan awam, sejarah ringkas dan kisah asal-usul objek harian.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX01 Papier. Terangkan topik ini melalui objek editorial di atas kertas, bina hubungan berperingkat dan akhiri dengan pandangan menyeluruh.`

### VX02 · Dunkel / Editorial Gelap

Asal: `native-source`. [Sumber](https://github.com/bestuserever121/vox-explainer#styles); bahagian: README.md → Styles; native token stil=dunkel.

- Visual: Gunakan pentas hampir hitam, tulisan berkontras dan aksen bercahaya terkawal. Kekalkan siluet foto serta label mudah dibaca.
- Gerak: Dedahkan satu bukti terang pada satu masa; sambungkan dengan laluan cahaya ringkas, kemudian kecilkan keseluruhan scene untuk memperlihatkan hubungan.
- Kegunaan: Teknologi, sistem kompleks dan penerangan berfokus yang memerlukan suasana serius.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX02 Dunkel. Bina explainer teknologi ini pada pentas gelap dengan satu aksen cahaya dan satu bukti utama bagi setiap beat.`

### VX03 · Blaupause / Blueprint Editorial

Asal: `native-source`. [Sumber](https://github.com/bestuserever121/vox-explainer#styles); bahagian: README.md → Styles; native token stil=blaupause.

- Visual: Gunakan kertas grid teknikal, garis tepat dan label yang rapat kepada objek. Biar rupa teknikal membantu menerangkan struktur.
- Gerak: Lukis rajah daripada komponen kepada hubungan; alihkan kamera mengikuti susunan fungsi, kemudian tampilkan keseluruhan pelan.
- Kegunaan: Mekanisme alat, infrastruktur, operasi dan aliran kerja.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX03 Blaupause. Terangkan cara sistem ini berfungsi menggunakan rajah blueprint, pembinaan komponen dan kamera yang mengikuti aliran.`

### VX04 · Riso / Duotone Editorial

Asal: `native-source`. [Sumber](https://github.com/bestuserever121/vox-explainer#styles); bahagian: README.md → Styles; native token stil=riso.

- Visual: Gunakan pentas krim dengan cetakan duotone beranjak dan bentuk editorial tegas. Kekalkan isi penting tajam walaupun tekstur cetakan kelihatan.
- Gerak: Susun lapisan objek secara bersela, hadirkan kata kunci dengan cap visual, kemudian selaraskan lapisan ketika kesimpulan muncul.
- Kegunaan: Budaya visual, penerangan sosial dan pengumuman berwatak cetakan.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX04 Riso. Hasilkan explainer ini dengan rupa cetakan duotone, objek berlapis dan tajuk yang masuk mengikut beat narasi.`

## 4. Dua belas pengembangan asal

### VX05 · Meja Arkib dan Bukti

Asal: `original-adaptation`. [Sumber](https://github.com/heygen-com/hyperframes-community-skills/blob/master/skills/vox-explainer/references/vox-collage-layout.md); bahagian: Frame recipes → Evidence stack; olahan asal keluarga dokumentari.

- Visual: Susun foto berlesen, petikan dokumen dan label tarikh di atas meja editorial. Beri satu kad bukti dominan dan simpan kredit berdekatan bahan.
- Gerak: Timbunkan bukti pada lokasi tumpuan, sorot butiran yang dirujuk, kemudian pindahkan kad yang sama ke kedudukan kesimpulan.
- Kegunaan: Sejarah, siasatan dokumen dan penerangan yang mempunyai bahan arkib sebenar.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX05 Meja Arkib dan Bukti. Gunakan dokumen serta foto yang saya beri untuk membina hujah melalui kad bukti yang berkait.`

### VX06 · Investigasi Peta dan Laluan

Asal: `original-adaptation`. [Sumber](https://github.com/CK42BB/vox-explainer-skill/blob/main/references/vox-style-guide.md); bahagian: Visual grammar → Cultural adaptation; olahan asal spatial daripada kolaj editorial.

- Visual: Jadikan peta tepat sebagai pentas, disertai foto lokasi dan penanda berlabel. Bezakan laluan utama, konteks dan inset detail melalui hierarki visual.
- Gerak: Lukis perjalanan atau penyebaran secara berperingkat; kamera mengikuti lokasi penting, mengezum kepada bukti dan kembali kepada peta keseluruhan.
- Kegunaan: Geografi, jaringan pengangkutan, migrasi dan perjalanan sesuatu idea atau produk.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX06 Investigasi Peta dan Laluan. Terangkan perjalanan ini dengan peta disahkan, pin bermakna dan bukti lokasi yang muncul mengikut urutan.`

### VX07 · Rantaian Sebab-Akibat

Asal: `original-adaptation`. [Sumber](https://github.com/bestuserever121/vox-explainer); bahagian: README.md → Why, free canvas, camera and arrows; olahan asal susunan kausal.

- Visual: Bina satu kanvas hujah dengan objek bagi setiap sebab dan akibat. Letakkan connector pada anchor objek sebenar dan gunakan satu kata kerja pada hubungan utama.
- Gerak: Aktifkan sebab, lukis hubungan, kemudian tunjuk akibat; teruskan rantaian dalam ruang sama dan tarik keluar untuk memeriksa keseluruhan logik.
- Kegunaan: Proses sosial, penerangan risiko, operasi dan konsep yang sering disalahfahami.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX07 Rantaian Sebab-Akibat. Jadikan setiap dakwaan satu objek dan tunjuk bagaimana satu perubahan membawa kepada perubahan seterusnya.`

### VX08 · Kronologi Dokumen

Asal: `original-adaptation`. [Sumber](https://github.com/heygen-com/hyperframes-community-skills/blob/master/skills/vox-explainer/SKILL.md); bahagian: Source mode → person/date, turn and receipts; olahan asal kronologi.

- Visual: Gunakan rel masa dengan dokumen bertarikh, foto dan penanda perubahan. Pastikan tarikh diperoleh daripada sumber dan jarak visual tidak menyiratkan skala palsu.
- Gerak: Gerakkan kamera sepanjang kronologi; buka dokumen pada titik perubahan, sorot bukti dan satukan peristiwa dengan hasil semasa.
- Kegunaan: Sejarah dasar, evolusi produk dan perubahan amalan dari masa ke masa.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX08 Kronologi Dokumen. Bina cerita daripada tarikh dan sumber ini, dengan satu titik perubahan yang jelas dan bukti bagi setiap peristiwa.`

### VX09 · Mitos vs Data

Asal: `original-adaptation`. [Sumber](https://github.com/heygen-com/hyperframes-community-skills/blob/master/skills/vox-explainer/SKILL.md); bahagian: Source mode → mechanism verified on screen; olahan asal perbandingan dakwaan.

- Visual: Letakkan dakwaan ringkas berhadapan unit data yang boleh dibanding. Gunakan paksi, skala dan unit yang sama untuk membuat beza mudah dilihat.
- Gerak: Paparkan jangkaan, bina data titik demi titik atau bar demi bar, kemudian ubah susunan untuk mendedahkan kesimpulan tanpa menukar jumlah.
- Kegunaan: Literasi data, penerangan statistik dan pembetulan salah faham berdasarkan sumber sah.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX09 Mitos vs Data. Bandingkan dakwaan ini dengan dataset yang saya beri menggunakan unit dan skala konsisten serta penjelasan berperingkat.`

### VX10 · Keratan Mekanisme

Asal: `original-adaptation`. [Sumber](https://github.com/heygen-com/hyperframes-community-skills/blob/master/skills/vox-explainer/references/vox-collage-layout.md); bahagian: Frame recipes → Zoom-isolation pair; olahan asal penerangan dalaman.

- Visual: Mulakan dengan foto objek dalam konteks, kemudian asingkan bahagian yang menerangkan fungsi. Gunakan keratan atau rajah berlabel apabila bahan tepat tersedia.
- Gerak: Masuk kepada butiran, keluarkan latar untuk mendedahkan komponen, gerakkan satu komponen penting dan kembali kepada fungsi objek keseluruhan.
- Kegunaan: Sains asas, perkakasan, instrumen dan mekanisme objek harian.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX10 Keratan Mekanisme. Mulakan dengan objek sebenar, masuk kepada bahagian penting dan tunjuk bagaimana komponennya menghasilkan fungsi ini.`

### VX11 · Skala yang Boleh Dibanding

Asal: `original-adaptation`. [Sumber](https://github.com/bestuserever121/vox-explainer/blob/master/docs/spec.md); bahagian: Panel schema → counters and bars; olahan asal demonstrasi skala.

- Visual: Gunakan unit berulang, siluet atau bekas dengan kapasiti sama supaya nilai abstrak boleh dibanding secara visual. Letakkan unit ukuran berhampiran nilai.
- Gerak: Bina satu unit rujukan, gandakan mengikut data, kemudian zoom keluar pada skala terkawal untuk memperlihatkan perbezaan saiz atau kuantiti.
- Kegunaan: Kuantiti besar, kos, jarak, masa dan penerangan statistik kepada awam.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX11 Skala yang Boleh Dibanding. Tukarkan angka ini kepada unit visual yang konsisten dan tunjuk skala sebenar tanpa mengubah nisbah.`

### VX12 · Petikan dan Saksi

Asal: `original-adaptation`. [Sumber](https://github.com/heygen-com/hyperframes-community-skills/blob/master/skills/vox-explainer/references/vox-collage-layout.md); bahagian: Frame recipes → Lower-third; source receipts; olahan asal petikan.

- Visual: Gabungkan foto atau footage sumber dengan petikan pendek yang diatribusi. Bezakan petikan verbatim, parafrasa dan penerangan penyampai.
- Gerak: Sorot frasa yang menjadi bukti, bawa petikan ke kad kesimpulan dan hubungkan kepada dokumen sokongan tanpa memotong makna ucapan.
- Kegunaan: Wawancara, sejarah lisan, laporan dan analisis pernyataan yang disahkan.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX12 Petikan dan Saksi. Gunakan petikan tepat serta atribusi daripada bahan saya dan sambungkan setiap petikan kepada bukti sokongannya.`

### VX13 · Peta Pilihan Dasar

Asal: `original-adaptation`. [Sumber](https://github.com/bestuserever121/vox-explainer); bahagian: README.md → free canvas, causal arrows; olahan asal cabang keputusan.

- Visual: Susun pilihan sebagai cabang dengan akibat yang dapat dibanding. Gunakan ikon dan label pendek bagi hasil, syarat serta batas setiap laluan.
- Gerak: Buka satu pilihan pada satu masa, gerakkan token contoh melalui laluan yang relevan, kemudian paparkan dua hasil pada skala setara.
- Kegunaan: Pilihan program, SOP, dasar organisasi dan penerangan aliran keputusan.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX13 Peta Pilihan Dasar. Terangkan pilihan dan akibat berdasarkan SOP ini melalui cabang keputusan yang jelas dan contoh laluan pengguna.`

### VX14 · Gelung Sistem

Asal: `original-adaptation`. [Sumber](https://github.com/bestuserever121/vox-explainer); bahagian: README.md → connected causal argument; olahan asal gelung maklum balas.

- Visual: Bentangkan aktor, sumber dan hasil dalam satu gelung yang lengkap. Bezakan aliran fizikal, wang atau maklumat menggunakan label dan gaya garisan yang konsisten.
- Gerak: Gerakkan token mengikut aliran, ubah satu parameter berdasarkan contoh sebenar dan tunjuk bagaimana kesannya kembali kepada titik asal.
- Kegunaan: Ekonomi asas, rantaian bekalan, ekosistem organisasi dan gelung maklum balas.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX14 Gelung Sistem. Tunjukkan aktor, sumber dan maklum balas dalam sistem ini menggunakan satu gelung visual yang boleh diikuti.`

### VX15 · Dokumen Beranotasi

Asal: `original-adaptation`. [Sumber](https://github.com/heygen-com/hyperframes-community-skills/blob/master/skills/vox-explainer/references/vox-collage-layout.md); bahagian: Assets and composition → source artifacts and measured annotations; olahan asal audit dokumen.

- Visual: Jadikan halaman, jadual atau screenshot sebenar sebagai hero. Letakkan anotasi pada koordinat isi yang tepat dan kekalkan konteks serta nombor halaman jika diperlukan.
- Gerak: Masuk kepada petikan, jejak bacaan dengan highlight, keluarkan satu angka atau klausa ke panel sisi, kemudian kembali kepada sumber asal.
- Kegunaan: Laporan, polisi, kajian, pekeliling dan penerangan bahan kerja sebenar.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX15 Dokumen Beranotasi. Terangkan halaman ini melalui highlight tepat, zoom pada butiran dan panel penjelasan yang mengekalkan sumber asal.`

### VX16 · Bukti Sebelum-Selepas

Asal: `original-adaptation`. [Sumber](https://github.com/heygen-com/hyperframes-community-skills/blob/master/skills/vox-explainer/references/vox-collage-layout.md); bahagian: Frame recipes → Two-panel compare; olahan asal perbandingan perubahan.

- Visual: Letakkan keadaan awal dan akhir pada ukuran, sudut serta crop sepadan. Gunakan label neutral dan bezakan perubahan sebenar daripada anotasi penerangan.
- Gerak: Tunjuk keadaan awal, gerakkan pembahagi atau lakukan match cut, sorot bahagian yang berubah dan tutup dengan bukti pada kedua-dua panel.
- Kegunaan: Perubahan reka bentuk, penambahbaikan proses dan demonstrasi hasil yang mempunyai bahan setara.

Contoh arahan: `Guna @Buat Video Motion Grafik, gaya Vox VX16 Bukti Sebelum-Selepas. Bandingkan bahan ini pada skala dan crop sepadan, kemudian sorot hanya perubahan yang benar-benar dapat dilihat.`

## 5. Pemilihan dan QA

Gunakan VX01–VX04 sebagai look asas. Pilih VX05–VX16 apabila bentuk bukti atau cerita memerlukan mekanisme tertentu, contohnya VX01 + VX15 untuk dokumen atau VX03 + VX10 untuk mekanisme. Gabungan itu bukan entri atau jumlah gaya tambahan.

Catat `style_recipe_ids`, sumber/aset, data, cue dan backend sebenar dalam manifest. Berikan setiap elemen entrance, waktu siap-baca, hold dan exit. Jika audio wujud, gunakan durasi serta cue audio sebenar; jika tanpa VO, arahkan jam visual yang terhingga. Jangan memaksa hold, palet, fps atau minimum teknik upstream apabila brief pengguna lebih khusus.

Render proof bagi mekanisme tersukar melalui backend projek sebenar. Semak koordinat anotasi, label/unit, skala perbandingan, teks pada telefon, titik sambungan, alpha cutout dan kesinambungan objek pembawa. Semak playback biasa serta frame bersebelahan; kemudian jalankan QA MP4/audio sedia ada sebelum penghantaran. Jangan menganggap panduan atau pemasangan kod membuktikan padanan rupa dan kelancaran.
