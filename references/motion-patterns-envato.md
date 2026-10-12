# Bank gerakan UI, teks dan carousel

## Kandungan

1. Bukti dan sempadan pemeriksaan
2. Daftar 12 sumber
3. Dua puluh empat resipi gerakan
4. Parameter dan cara menggabungkan komponen
5. Semakan produksi

## 1. Bukti dan sempadan pemeriksaan

Gunakan rujukan ini bersama `advanced-motion-graphics.md`. Pada 24 September 2026, halaman produk dan fail MP4 preview rasmi bagi semua 12 pautan pengguna berjaya diakses. Pemeriksaan meliputi metadata, contact sheet sepanjang setiap preview dan urutan temporal rapat pada contoh gerakan. Audio tidak dinilai melalui pendengaran. Pemeriksaan bingkai tidak mengesahkan lengkung easing tepat, expression, keyframe, plugin, layer graph atau kualiti playback berterusan.

Ambil MP4 hanya daripada pautan preview awam yang benar-benar terpapar pada halaman. Label web extractor yang menyebut video tidak tersedia tidak semestinya bermakna MP4 preview rosak; periksa player/Download preview melalui browser yang dibenarkan jika carian sudah berjaya tetapi media belum dapat diperiksa. Jangan meneka URL fail, membuka projek berbayar tanpa akses atau memintas sekatan. Jangan simpan video, foto, muzik, template atau watermark pihak lain dalam skill ini. Gunakan aset sendiri/berlesen bagi produksi.

Bezakan tempoh preview daripada atribut panjang template. Contohnya preview boleh mengandungi beberapa variasi, demonstrasi placeholder dan end card. Angka di bawah diukur daripada MP4 preview; ia bukan spesifikasi projek asal. Jika pengguna membekalkan versi baharu, periksa semula sebelum membuat dakwaan khusus.

Resipi pada bahagian 3 ialah kaedah pelaksanaan asal berdasarkan prinsip yang diperhatikan. Nombor durasi, amplitud dan easing yang dicadangkan bukan parameter yang diekstrak daripada projek Envato. Jangan mendakwa skill ini memasang preset AE asal atau telah membuktikan padanan visual penuh.

## 2. Daftar 12 sumber

Masa dalam lajur terakhir merujuk MP4 preview yang diperiksa, bukan masa relatif dalam contact sheet potongan.

| ID dan sumber | Preview yang diukur | Pemerhatian visual untuk produksi |
|---|---|---|
| [5EN4HC8 — SaaS Product Promo](https://elements.envato.com/saas-product-promo-5EN4HC8), M_Yunusoglu | 53.16s, 2560×1440, ~59.94fps | 7–11s logo mengecil menjadi komponen panel, rim bercahaya, dashboard condong dan komponen UI terbina berperingkat. Kemudian ada tumpukan panel, kad metrik, garisan carta, ikon seperti syiling dan sfera sekitar logo. Gunakan hubungan objek yang berterusan ketika komposisi bertukar. |
| [G827UET — Mobile Notification](https://elements.envato.com/mobile-notification-G827UET), PrivalFX | 22.12s, 1920×1080, ~29.97fps | 0–4s notifikasi baharu muncul di bawah dan mengalihkan yang terdahulu ke atas; ikon, nama dan mesej mempunyai kemunculan berbeza. Kad berkumpulan menunjukkan lapisan di belakang. Selepas itu komponen dipaparkan dalam skrin telefon bersama bar panggilan. |
| [S5KXBDW — Text Animation](https://elements.envato.com/text-animation-S5KXBDW), vio_25 | 21.65s, 3840×2160, 60fps | Tipografi minimal pada latar cerah, perkataan berwarna gradien, pertukaran saiz antara ayat dan kata besar, reveal berturutan dan caret typing di penutup. Simpan layout akhir agar teks tidak tersentak sewaktu muncul. |
| [HSWFFKR — Text Animation Kit AE](https://elements.envato.com/text-animation-kit-ae-HSWFFKR), ePatmos | 38.87s, 2560×1440, 30fps | Banyak preset pendek: aksara berputar ke posisi, perkataan masuk berperingkat, baris bertingkat, aksen berwarna, cursor dan ikon kecil. Bezakan animasi aksara, perkataan dan seluruh blok. |
| [C5QWBQD — Carousel](https://elements.envato.com/carousel-C5QWBQD), 2FFrame | 15.02s, 3840×2160, 30fps | Variasi kad profil berselerak, kipas mendatar, aliran menegak dan versi dalam mockup telefon. Kad aktif lebih besar/jelas; nama kekal pada kad. Perubahan kipas kepada susunan menegak sekitar 5.9–6.0s ialah cut, bukan bukti morph berterusan. |
| [TVD7DLH — Text Animations](https://elements.envato.com/text-animations-TVD7DLH), KineticFlow | 67.14s, 3840×2160, 30fps | Kata sangat besar/cropped, pengulangan teks memenuhi skrin, bar wipe, typing, pertukaran ketebalan huruf, outline/fill, highlight dan garisan bawah. Pilih satu gerakan dominan bagi setiap beat. |
| [7Z8RTC7 — Text Animation](https://elements.envato.com/text-animation-7Z8RTC7), Grizzlies1 | 53.33s, 3840×2160, 30fps | Blur/glow dan pinggir warna terpisah ketika huruf masuk atau keluar; teks kemudian menjadi lebih tajam. Baris neon, underline dan gabungan tajuk/subtajuk dipaparkan atas footage gelap. Blur transition tidak boleh mengurangkan masa bacaan. |
| [DM5284R — App Promo](https://elements.envato.com/app-promo-DM5284R), gerak_visual | 87.36s, 960×540, ~29.97fps | 6–10s telefon bergerak keluar sementara ikon aplikasi berpisah dari grid dan menjadi logo utama. Bab lain menggunakan beberapa telefon dengan kedalaman/perspektif. Preview kemudian mengulang struktur dengan placeholder; jangan anggap semuanya naratif akhir. |
| [FYUV3JN — Text Animation](https://elements.envato.com/text-animation-FYUV3JN), RadiantFX | 36.23s, 3840×2160, ~29.97fps | Kinetic words bersaiz besar, typing/caret, blur-to-sharp, aksen gradien, ikon kecil dan contoh teks dalam video telefon. Typing jelas sekitar 11.0–11.8s; urutan blur masuk/keluar sekitar 23.2–24.6s. |
| [G4AP6AB — SaaS Product Promo](https://elements.envato.com/saas-product-promo-G4AP6AB), New-Motion | 26.63s, 1920×1080, 60fps | 11–15s counter naik sebelum panel metrik keluar; 15–17s kad bergambar tersebar dalam jalur melengkung di bawah tajuk yang masuk berperingkat. Ada outlined pill, glow limau, prompt typing dan cursor menuju butang sebelum logo penutup. |
| [JZE2XRQ — Hook & Captions for Social Media](https://elements.envato.com/hook-captions-for-social-media-JZE2XRQ), 142videos | 16.53s, 960×540, 25fps | Preview menunjukkan beberapa video menegak serentak: kata kunci berwarna/berlatar, perubahan saiz frasa, angka bergerak, ikon mengelilingi teks dan sisipan gambar. Paparan grid ialah demonstrasi pilihan, bukan susun atur wajib untuk video akhir. |
| [LYWTLZ3 — Carousel](https://elements.envato.com/carousel-LYWTLZ3), GrussGott | 39.02s, 1920×1080, 60fps | Variasi mendatar/menegak, crop bucu bulat/kapsul dan fokus kad tengah. Sekitar 20.0–20.5s satu panel berputar pada engsel menegak. Preview memotong antara variasi sekitar 19.9s dan 20.8s; ini bukan bukti semua layout bermorph. |

## 3. Dua puluh empat resipi gerakan

Gunakan ID berikut dalam manifest. Pilih berdasarkan fungsi cerita, bukan mengisi semua preset dalam satu video. Bentuk geometri dan nilai awal ialah resipi sendiri, bukannya pengesahan teknik dalaman pembuat sumber.

### UI produk dan peralihan objek

- **U01 — Logo menjadi header dashboard.** Kekalkan satu objek logo, interpolasi posisi/skala ke slot header; panel masuk di belakangnya dan widget menyusul. Tukar parent hanya dengan world transform yang sepadan. Tahan logo sehingga panel cukup jelas.
- **U02 — Dashboard terbina dengan data.** Susun shell → tab/label → KPI → carta. Gunakan satu progress untuk nilai angka dan panjang bar/path; lock sasaran akhir. Animasi angka tidak boleh melepasi nilai sebenar. Letakkan unit dan sumber data.
- **U03 — Ikon keluar daripada skrin.** Gunakan ikon berasingan atas screenshot/texture, sejajarkan tepat dengan posisi asal, kemudian lepaskan daripada clipping dan gerakkan menjadi hero. Mulakan exit telefon selepas ikon mempunyai identiti visual sendiri; elakkan ikon berganda kelihatan.
- **U04 — Tumpukan panel berperspektif.** Parent scene mengawal kamera, setiap panel mempunyai depth, offset, sudut dan shadow konsisten. Masuk dengan sela, tahan panel utama lebih tajam, keluar sebagai kumpulan atau berpindah ke panel seterusnya. Kad rata berperspektif tidak menggantikan model 3D penuh.

### Notifikasi dan mesej

- **N01 — Masuk dan susun semula stack.** Ukur tinggi kad sebelum animasi. Kira kedudukan lama/baharu menggunakan jumlah tinggi+gap; padankan melalui ID stabil, bukan indeks yang berubah selepas insertion. Interpolate kad sedia ada dengan progress bersama supaya tiada teleport. Kad baharu muncul dari bawah/atas mengikut arah naratif, kemudian berhenti untuk bacaan.
- **N02 — Kumpulan kad berlapis.** Render kad aktif dan 1–3 lapisan belakang dengan offset kecil, skala/opacity berkurang dan clipping yang terkawal. Tambah/removekan lapisan melalui transisi; jangan membiarkan bayang gelap bertindan berlebihan.
- **N03 — Isi kad secara berturutan.** Container/icon masuk dahulu, nama kemudian mesej dengan typing atau reveal. Ruang teks ditetapkan daripada hasil akhir; bekukan dimensi semasa typing supaya stack tidak mengepam naik turun.
- **N04 — Notifikasi dalam mockup telefon.** Letakkan stack dan bar panggilan sebagai anak screen mask. Selaraskan scale, radius dan perspektif dengan telefon; jika kamera mendekat, gerakkan group. Button panggilan dan status ialah grafik demo, bukan kawalan interaktif sebenar.

### Tipografi asas

- **T01 — Reveal perkataan melalui mask.** Ukur baseline dan pecahkan kepada unit, animate y serta opacity di dalam mask tetap; sela mengikut susunan baca. Ketika hold, semua unit kembali tepat ke baseline; keluar berturutan atau sebagai satu frasa.
- **T02 — Huruf berputar lalu menetap.** Simpan anchor per glyph, animate rotation+translation menuju transform neutral. Hadkan amplitud agar perkataan masih dikenali. Untuk tulisan Arab bersambung, gunakan unit perkataan/baris atau shaping yang menyokongnya.
- **T03 — Typing, caret dan penggantian.** Gunakan grapheme, bukan byte. Tetapkan cue aksara/jeda; letak caret pada hujung teks terukur. Sokong cursor garis tegak, underscore atau bracket sebagai objek berasingan. Gunakan state typing → hold → deleting → replacing → exit, bukan sekadar substring masa. Tahan hasil akhir dan tamatkan caret sebelum cut.
- **T04 — Bina frasa atau baris mengikut beat.** Tetapkan slot akhir dan reveal kata penting pada cue narasi. Jika layout sengaja berubah, interpolasi blok lama ke layout baharu; jangan membenarkan reflow browser tanpa kawalan.

### Tipografi berimpak

- **X01 — Kata besar dan pengulangan.** Bina satu kata hero, lattice berulang atau echo menegak dengan delay berbeza; animasikan parent scale/pan dan kekalkan satu frasa tajam sebagai fokus. Cropping mesti disengajakan; tunjuk bentuk lengkap sebelum/selepas jika makna memerlukannya.
- **X02 — Bar wipe dan underline.** Animate rectangle/stroke secara berasingan daripada teks; gunakan mask reveal atau perpindahan bar ke kata sasaran. Untuk underline beralun, bina path dengan amplitud kecil dan reveal mengikut panjang path; exit boleh berbeza daripada teks. Akhiri pada bounding box+padding yang betul, bukan anggaran lebar huruf.
- **X03 — Gelombang ketebalan atau outline/fill.** Gunakan font variable hanya jika perender menyokong paksi font. Alternatif ialah crossfade font weight dengan posisi terukur. Kekalkan lebar slot dan baseline supaya hasil tidak menggeletar.
- **X04 — Blur, pinggir warna dan glow.** Layer teks utama kekal tajam ketika hold; salinan blur/tint bergerak dengan offset yang mengecil semasa settle. Blur spatial ini efek gaya, berbeza daripada motion blur temporal. Hadkan glow agar bentuk huruf tidak hilang.

### Carousel dan galeri

- **C01 — Kad pusat sebagai fokus.** Kira jarak setiap kad daripada focus index yang berterusan. Derive posisi, scale, depth, tilt, blur dan opacity daripada jarak; sort depth secara deterministik. Nama/caption diparent kepada kad.
- **C02 — Kipas atau jalur melengkung.** Gunakan parameter lengkung untuk posisi pusat kad dan tangent untuk sudut. Ubah spread melalui satu progress, kekalkan gap serta crop. Pastikan z-order konsisten semasa kad bersilang.
- **C03 — Hero berkembang dan kembali.** Promosikan kad terpilih dengan interpolasi posisi, saiz dan radius mask; jiran mengecil/berundur. Texture menggunakan cover-crop yang mengekalkan nisbah asal, bukan stretch. Simpan focal point wajah/produk.
- **C04 — Carousel mendatar/menegak berulang.** Gunakan offset modular dengan card IDs stabil dan padding luar skrin. Recycle hanya ketika seluruh kad tidak kelihatan atau opacity sifar. Semak seam loop; pembalutan matematik sahaja tidak menjamin loop visual bersih.

### Hook dan caption

- **H01 — Frasa dengan kata aktif.** Bina cue daripada audio sebenar; reveal frasa mengikut kumpulan makna, beri satu kata warna/weight dominan. Tetapkan safe area agar teks tidak menutup muka atau demo. Abaikan komponen ini jika pengguna meminta tanpa caption.
- **H02 — Penanda kata kunci.** Letakkan pill, marker atau outline di belakang kata terukur; animate padding/width dengan settle kecil. Kekalkan urutan layer dan kontras, serta elak highlight melompat kerana perbezaan font fallback.
- **H03 — Ikon dan sisipan menyokong hook.** Munculkan ikon/ring/cutout sebagai cue sekunder, kemudian kurangkan amplitud/opacity semasa frasa dibaca. Tetapkan pusat orbit yang stabil. Jangan menambah ikon yang mengubah makna ucapan.
- **H04 — Punch frasa dan counter.** Animate satu kata/angka besar bersama frasa sokongan lebih kecil; hold selepas settle, kemudian exit mengikut cue. Gunakan angka berasas atau label demonstrasi. Caption transkrip mesti mengekalkan erti, bukan bertukar kepada dakwaan pemasaran yang tidak disebut.

## 4. Parameter dan cara menggabungkan komponen

Simpan preset sebagai data dengan sekurang-kurangnya `pattern_id`, `unit`, `start`, `in_duration`, `hold_duration`, `out_duration`, `order`, `stagger`, `easing`, `amplitude`, `seed`, `parent`, `mask`, `assets` dan `cue_source`. Nilai `unit` boleh objek, glyph, grapheme, word, line atau group. Pisahkan teks caption daripada teks grafik supaya arahan tanpa caption dapat dipatuhi tanpa membuang label penting.

Julat cadangan awal: entrance 0.25–0.70s, exit 0.20–0.50s, sela unit 0.035–0.10s dan settle 0.10–0.25s. Uji pada saiz/fps sebenar. Spring sesuai pada kad atau ikon; elakkan overshoot pada angka data. Tempoh membaca dan VO mengatasi keinginan memadatkan preset.

Gabungan contoh: `T03 → U03 → U01+U02 → C01 → H02/CTA`. Tafsir sebagai struktur pilihan, bukan urutan wajib. Dalam satu beat, bezakan gerak primer (mesej), sekunder (bukti/produk) dan tertier (latar). Offset cue supaya semuanya tidak mencapai puncak serentak. Transisi patut membawa posisi, warna, bentuk atau objek yang bermakna ke scene seterusnya.

Gunakan helper `scripts/motion_primitives.py` hanya untuk pengiraan yang didokumenkan dalam docstring. Ia tidak menyediakan font shaping, glyph segmentation, perspektif 3D, clipping, audio alignment, render browser atau export MP4. Bina komponen renderer yang sebenar di projek, dan uji satu adegan sebelum menggunakannya sepanjang video. Bagi fungsi spring yang overshoot, clamp opacity tetapi jangan clamp transform secara membuta tuli.

API ringkas: `progress(t,start,duration)` memberi 0..1; `ease(p,curve)` memberi easing terbatas; `spring(p)` memberi settle yang boleh overshoot; `stagger(count,...)` memberi cue mengikut indeks asal; `in_hold_out(t,...)` memberi fasa/progress/visibility; `carousel(...)` memberi pose relatif dan visibility; `notification_stack(heights,...)` memberi layout endpoint. Pakai `t = frame_index / fps`, kemudian renderer mengaplikasikan transform/mask/alpha.

Helper carousel ialah ring mendatar: `count >= 2` dan `count*spacing >= viewport_width+card_width`. Ia menolak ring terlalu pendek untuk menyembunyikan seam. Untuk satu/dua aset yang tidak memenuhi syarat, bina gallery tidak berulang atau slot render berulang dengan identiti sumber aset dikekalkan; jangan mengira slot salinan sebagai imej unik. Jika mahu carousel menegak, petakan paksi secara sengaja dalam renderer. Helper belum melaksanakan perspective hinge, fan curve atau depth blur. Layout notifikasi ialah endpoint; pergerakan silang/reorder memerlukan semakan collision berasingan.

## 5. Semakan produksi

1. Ukur teks dan kad menggunakan font akhir. Semak ayat Melayu panjang, nombor, tanda baca dan glyph Arab. Pastikan line break stabil dan panjang mesej baharu tidak memotong UI.
2. Semak frame sebelum/selepas setiap perubahan parent, mask, z-order, state stack dan carousel wrap. Bandingkan posisi serta kelajuan; cari single-frame pop, overlap kad dan ghost duplicate.
3. Semak tipografi pada entry, readable hold dan exit. Hadkan flash serta glitch; jika blur memakan masa bacaan, pendekkan efek atau panjangkan scene.
4. Semak mockup dengan texture bergerak bersama skrin, perspektif konsisten dan shadow yang tidak beralih arah tanpa sebab. Geometri tambahan diperlukan untuk sudut yang memperlihatkan sisi/belakang.
5. Semak carousel untuk center crop, identiti aset, susunan depth dan seam pada loop. Uji bilangan kad ganjil/genap, satu kad, dua kad, serta kad yang bertukar saiz.
6. Semak VO/caption dengan audio sebenar apabila ada. Penilaian visual preset tidak membuktikan lip-sync, sebutan atau kualiti suara.
7. Periksa preview pada kelajuan biasa dan eksport berframe tetap. Kira `N = round(duration*fps)` dan render indeks `0..N-1`; state akhir mesti sudah tercapai pada frame terakhir, bukan hanya pada `t=duration` yang tidak dirender. Jumlah frame mesti datang daripada masa render deterministik; menyisip frame duplikat bukan bukti animasi 60fps asli.
8. Laporkan status secara berasingan: rujukan diperiksa, resipi ditambah, helper diuji, komponen dirender, video akhir dinilai. Jangan menukar kejayaan ujian matematik menjadi dakwaan semua preset telah dirender atau setanding Envato.
