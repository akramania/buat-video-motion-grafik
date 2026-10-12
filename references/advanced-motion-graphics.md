# Motion grafik lanjutan

## 1. Analisis rujukan secara nyata

- Periksa `ffprobe`: durasi, stream, dimensi, time base dan purata FPS. Jangan menyimpulkan frame rate asal daripada rakaman skrin VFR.
- Bezakan canvas kandungan daripada status bar, komen, butang dan letterbox. Tetapkan orientasi daripada kandungan serta brief, bukan dimensi fail pembungkus.
- Ambil bingkai keseluruhan setiap 2–3 saat untuk memahami cerita; tambah sampel 4–12 fps di sekitar entrance, perubahan susun atur dan exit. Semak playback biasa jika tersedia. Bingkai pegun sahaja tidak membuktikan easing, motion blur atau kelancaran.
- Catat timecode, fokus utama, teks, aset, kamera, jenis transisi dan perkara yang belum disahkan. Bezakan lapisan yang kelihatan daripada bilangan objek animasi bebas; jangan meneka bilangan keyframe atau perisian sumber.
- Dengar audio jika alat membenarkan. Metadata, loudness, waveform dan transkrip membantu QA teknikal tetapi bukan semakan sebutan, kemanusiaan suara atau mutu sound design.

### Rujukan pengguna yang diperiksa pada 24 September 2026

Fail `1000509675.mp4` ialah rakaman skrin telefon sepanjang kira-kira 63.6 saat, 1080×2376, dengan kandungan promosi LearnAI.my landscape di tengah. Kedudukan kawasan kandungan boleh berubah pada permulaan rakaman. Anggaran masa merujuk rakaman ini, bukan projek sumber.

| Masa | Pemerhatian visual | Teknik yang boleh dipindahkan |
|---|---|---|
| 0–2s | Frasa carian terisi beransur dalam search bar | Typing dengan caret dan tempo aksara |
| 2–4.5s | Kad laman memenuhi grid; label HUNDREDS menjadi fokus | Kemunculan berturutan, gerak kumpulan, skala kamera, hierarki teks |
| 4.5–8s | Carian kedua disusuli grid kad berwarna, frasa even more | Variasi aset dalam komposisi yang konsisten |
| 8–12.5s | Foto cutout, ayat terbina berperingkat, bulatan dan highlight | Kinetic typography, draw-on, pengasingan subjek |
| 12.5–18s | Kumpulan kad dan pembesar muncul; panel kedua membina laluan bernombor | Gerak objek sekunder, split-screen, path reveal berperingkat |
| 18–20s | Pertukaran latar ungu, logo dan nama muncul | Peralihan identiti dan logo reveal |
| 21–29s | Panel produk condong, katalog, cutout dan badge 180+ | Mockup berperspektif, bayang, susunan berlapis |
| 30–38s | Kad kursus, pin, cap FREE dan node di sepanjang laluan yang bergerak mendatar | Susunan berturutan, tracking komposisi, rotation dan scale |
| 38–41s | Mockup browser condong, progress strip, mesej penggunaan dan kawalan kelajuan | Perspektif dan bayang, sorotan kata, cue komponen berasingan |
| 41–44s | Dinding thumbnail terbina sebelum latar ungu dan kad tawaran masuk | Stagger grid, pertukaran palet, rotation dan scale |
| 44–52s | Kad keahlian, harga dan manfaat muncul satu demi satu | Hierarki tawaran, kemunculan bullet/checkmark, hold untuk membaca |
| 52–59s | Kad mengelilingi mesej akhir, nama jenama, CTA dan cutout | Gerak seperti kamera menjauh, reveal logo, penutupan berfokus |
| 59–63s | Search bar berulang dan typing, diikuti overlay kawalan telefon | Typing loop; asingkan UI pemain daripada komposisi asal |

Jangan menganggap grafik laluan bernombor itu carta data kuantitatif. Jangan menganggap susunan dua panel itu bukti before/after terukur. Kedua-duanya boleh dibina sebagai ciri projek baharu apabila kandungan menyokongnya. Pemeriksaan ini tidak mengesahkan aplikasi asal, enjin suara, projek 3D atau bilangan animasi bebas. Jangan simpan salinan video rujukan besar dalam skill.

## 2. Tetapkan bahasa gerak sebelum render

Bina satu styleframe padat dan satu petikan 8–15 saat yang menguji bahagian paling sukar sebelum render panjang. Jika pengguna meminta hasil lengkap, teruskan hingga video akhir tanpa menjadikan petikan itu alasan berhenti. Bagi pertanyaan kemampuan sahaja, jangan menghasilkan kempen penuh yang tidak diminta.

Tetapkan palet, sistem fon, grid, safe area, hierarchy, arah cahaya/bayang, amplitud gerak, tempo dan keluarga transisi. Untuk padanan rujukan ini, bina gaya editorial produk dan UI; jangan mewarisi kartun projek agama terdahulu.

Setiap adegan perlu ada satu fokus dominan. Animasi berpuluh objek boleh berlaku serentak tetapi kumpulkan kepada foreground, subject, support dan background; kurangkan kontras, saiz atau amplitud gerak sokongan. Jangan menambah kesan semata-mata bagi mencapai kuota.

## 3. Timeline per objek: in / during / out

Gunakan unit saat atau frame secara konsisten. Simpan bagi setiap objek: `id`, `asset_id`, `parent`, `z`, `anchor`, bounds, `in`, `during`, `out`, easing, mask dan audio cue. Takrifkan property track serta precedence supaya position semasa tidak melompat pada sempadan fasa.

- In: translasi, scale, mask reveal, clip-path, blur-to-sharp, path draw atau perspective settle. Gunakan anticipation dan overshoot hanya apabila sesuai dengan bahan.
- During: hold untuk bacaan ialah pilihan sah; gerak boleh berupa drift, parallax, orbit, pan, scroll, fokus, counter, ekspresi atau interaksi. Jangan beri semua objek ayunan sinus yang sama.
- Out: mask close, stagger collapse, keluar mengikut arah, shrink into target, matched transform atau cut yang bermakna.
- Tetapkan sela berturutan mengikut baris, jarak daripada pusat, perkataan atau prioriti. Gunakan seed stabil bagi variasi rawak agar render berulang sama.
- Gunakan ease-out untuk banyak entrance, ease-in bagi exit yang memecut, dan ease-in-out bagi reposisi. Pastikan sambungan posisi dan kelajuan masuk akal. Spring perlu settle, bukan bergetar tanpa tamat.
- Pisahkan transform objek, transform parent dan kamera; jangan meratakannya terlalu awal. Transisi boleh berkongsi objek yang sama merentas adegan untuk kesinambungan.

Julat awal untuk ujian, bukan syarat keras: kemunculan 0.25–0.7s, sela 0.04–0.12s, exit 0.2–0.5s. Kesesuaian sebenar ditentukan voice-over, saiz gerak dan masa membaca.

## 4. Komponen yang boleh diguna semula

| Komponen | Pelaksanaan dan semakan penting |
|---|---|
| Kinetic typography | Pecah baris/perkataan, ukur susun atur akhir terlebih dahulu, animate transform/opacity/mask. Elakkan reflow yang menggoncang perkataan lain. Gunakan sokongan shaping bagi Arab; jangan pecahkan huruf bersambung menjadi kotak aksara. |
| Typing | Gunakan grapheme dan caret dengan sela aksara yang munasabah; jadualkan jeda selepas frasa; tahan hasil cukup lama untuk dibaca. |
| Sorotan teks | Animate lebar highlight di belakang teks, underline atau stroke; pastikan z-order dan padding tepat. |
| Mockup realistik | Gunakan aset resolusi cukup, clipping skrin, perspektif konsisten, bezel/ketebalan jika perlu, bayang sentuhan dan pencahayaan. Perspektif 2.5D sesuai untuk skrin/kad; objek yang berputar besar dan memperlihatkan belakang memerlukan geometri/aset tambahan. Jangan panggil kad rata berbayang sebagai 3D fotorealistik. |
| Grid puluhan/ratusan imej | Bina daftar aset dengan ID unik, hash, sumber dan saiz. Resize thumbnail, cull luar viewport, cache decode dan gunakan parent group. Jangan mengira salinan imej sama sebagai aset unik atau memuat semua full-resolution ke setiap frame. |
| Carta data | Gunakan data sebenar, skala paksi dan unit; animate bar/path/point/counter mengikut nilai, tanpa overshoot yang mengelirukan. Labelkan data demonstrasi dengan jelas. |
| Before/after | Selaraskan crop, sudut, skala dan exposure; gunakan slider/wipe/split yang membaca jelas. Label kedua-dua keadaan dan jangan mereka bukti peningkatan. |
| Laluan/diagram | Lukis path secara progresif, munculkan node pada waktu path sampai, animate fokus tanpa menyamar sebagai data statistik. |
| Caption | Masa daripada audio sebenar atau alignment yang diperiksa; pecah kepada frasa pendek, warna kata aktif jika berguna, semak telefon dan CTA. Tiada caption jika pengguna melarang. |

## 5. Pilih perender berdasarkan keperluan

Semak runtime dan versi yang tersedia sebelum menjanjikan stack tertentu. Remotion, SVG, Canvas dan HTML ialah pilihan, bukan dependencies yang dijamin dipasang. Rujuk dokumentasi primer semasa jika memerlukan API yang belum diketahui. Untuk raster ilustrasi ringkas, Pillow boleh mencukupi; untuk tipografi padat dan mask, pilih perender vektor/komposit yang menyokong keperluan.

- Render deterministik daripada masa `t = frame / fps`; bagi browser, set playhead/frame dengan sengaja. Jangan menggunakan screen recording masa nyata sebagai kaedah eksport utama kerana dropped frame dan beban browser boleh mengubah timing.
- Tunggu fon, imej dan shader siap sebelum tangkap frame. Elakkan transition CSS berasaskan masa dinding yang mengabaikan seek.
- Guna 30 fps untuk banyak projek; uji 60 fps bagi gerak pantas apabila perender mampu menghasilkan frame berbeza. Jangan gandakan frame 24/30 fps dan mendakwanya gerak 60 fps asli. Pilih 24 fps apabila gaya sesuai.
- Motion blur memerlukan sampling temporal atau sokongan perender, bukan Gaussian blur seluruh imej. Kawal pada objek pantas; pastikan teks sewaktu hold tajam. Semak alpha supaya tiada pinggir gelap.
- Render segmen dengan dimensi, fps, warna dan codec seragam; simpan projek serta manifest yang boleh diedit. Rekod peak memory, masa render dan batas sebenar; jangan janjikan durasi, bilangan aset atau resolusi tanpa mengambil kira sumber.

## 6. Voice-over, caption dan bunyi

Gunakan penyedia suara yang pengguna pilih. Untuk Google AI Studio, ikuti skill `google-ai-studio-voiceover`, eksport fail sebenar, pecahkan narasi panjang kepada bahagian semula jadi dan kekalkan suara/style. Ukur durasi, semak sebutan dan sambungan sebelum menetapkan animation cue akhir. Jangan mengubah erti narasi bagi memuatkan jadual yang terlalu pendek.

Pisahkan VO, muzik, ambience dan SFX. Letakkan click, tap, whoosh, tick, impact atau chime pada peristiwa yang bermakna; jangan memberi setiap objek bunyi tersendiri. Periksa masking pertuturan, clipping dan aras bunyi pada master. Laporkan semakan pendengaran yang belum dapat dibuat, bukan meneka suara itu natural.

## 7. Syarat penerimaan hasil

- Semak opening, fasa in/during/out, adegan paling padat, typography, mockup, peralihan dan ending pada kelajuan biasa serta frame sekitar sempadan.
- Pastikan tiada jerking, one-frame flash, font berubah, glyph hilang, tepi crop, aset pecah, pop pada z-order atau exit terpotong. Periksa arah/kelajuan gerak merentas transisi.
- Pastikan setiap mesej utama sempat dibaca. Jumlah objek/animasi tidak menggantikan fokus, kontras dan ruang.
- Padankan cue suara dan caption; bezakan QA berangka dengan QA pendengaran. Jika playback tidak tersedia, nyatakan semakan kelancaran masih terhad.
- Sahkan fail akhir dengan probe dan decode. Untuk ratusan aset, periksa bilangan unik dalam manifest dan sampel setiap keluarga komposisi.
- Bezakan tiga kenyataan: kaedah ini boleh dibina; petikan ini telah dirender dan diperiksa; video ini telah memenuhi sasaran. Panduan skill sahaja tidak membuktikan kemampuan render atau mutu setara. Jangan menjamin "10× lebih baik" atau mendakwa penguasaan baharu tanpa hasil yang boleh dinilai.
