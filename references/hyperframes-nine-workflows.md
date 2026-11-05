# Sembilan aliran HyperFrames mengikut sumber dan hasil

## Kandungan

1. Pilih laluan
2. Explainer tanpa wajah
3. Pelancaran produk
4. Motion graphic pendek
5. Muzik dan lirik
6. Data dan peta
7. Avatar/presenter
8. GitHub pull request
9. Slideshow interaktif
10. Video custom/campuran
11. Selaraskan panduan dengan arahan pengguna
12. QA dan status kemampuan

Kajian dokumentasi rasmi: **1 November 2026**. Dokumen ini menerapkan cara memilih sumber, struktur dan pemeriksaan bagi sembilan genre; ia **bukan** bukti kesemua servis/genre telah dirender, akaun HeyGen tersedia atau semua blok registry dipasang. Gunakan bersama `hyperframes-codex-examples.md` bagi run/gerakan dan `html-hyperframes-production.md` bagi kontrak runtime versi terkunci.

## 1. Pilih laluan

| Bahan/hasil yang menentukan kerja | Laluan utama | Keputusan produksi |
|---|---|---|
| Nota, artikel atau satu konsep untuk diajar | Faceless explainer | Cari satu inti pembelajaran; bina mekanisme visual |
| URL/aset produk dan tindakan penonton | Product launch/tour | Tunjuk bukti produk dan hasil tugas |
| Satu tajuk, logo, nombor atau overlay | Motion graphic | Bina satu aksi ringkas dengan endpoint jelas |
| Trek muzik mengawal urutan | Music/lyric video | Analisis audio dahulu; susun visual pada frasa/beat |
| Dataset atau geografi | Data/maps | Tentukan encoding, sumber dan geometry sebelum gerak |
| Penyampai/avatar diperlukan | Avatar/presenter | Sahkan sumber klip, suara dan keperluan servis |
| URL pull request GitHub | PR to video | Semak perubahan sebenar dan status pelepasan |
| Pengguna mengklik reveal/branch ketika membentang | Interactive slideshow | Bina deck live dan gunakan `present` |
| Campuran sumber, story panjang atau format luar biasa | Custom video | Arahkan satu master timeline dan reka setiap format |

Pilih satu laluan utama dan tambah modul yang membantu, contohnya explainer + carta + muzik. Label genre tidak mengatasi arahan pengguna; satu scene boleh mempunyai banyak prop dan beberapa beat yang menyokong satu idea.

## 2. Explainer tanpa wajah

Sumber: https://hyperframes.heygen.com/guides/faceless-explainer

Mulakan daripada persoalan, sebab-akibat atau proses yang perlu difahami. Pilih sudut konsep, langkah kerja, senarai atau kisah kes. Buang sisipan yang tidak membantu inti; setiap beat mesti menunjukkan mekanisme, langkah atau implikasi. Cipta artwork berlapis daripada teks apabila tiada footage; rajah mesti menerangkan hubungan, carta mesti mempunyai data sah. Jangan menukar setiap perenggan menjadi slaid teks.

Tetapkan apa yang mesti verbatim dan apa yang boleh diolah. Semak fakta, angka dan sumber sebelum storyboard. Untuk narasi, ukur audio akhir dahulu; untuk tanpa VO, copy ringkas dan aksi visual mesti cukup membawa cerita. Gabungkan prop, path, kamera dan tipografi dalam bahasa visual yang konsisten. Semak sama ada penonton boleh menerangkan semula idea utama.

## 3. Pelancaran produk

Sumber: https://hyperframes.heygen.com/guides/product-launch-video

Bezakan iklan pelancaran, tour satu tugas dan teaser satu manfaat. Susun hook → nilai → bukti → satu CTA apabila sesuai. Dapatkan skrin/logo/palet/fon dan copy daripada sumber sebenar yang dibenarkan; jika brief sahaja diberi, reka ilustrasi yang jelas sebagai ilustrasi. Jangan mencipta butang, label, statistik jualan atau interaksi dan menganggapnya bukti produk.

Perlihatkan workspace penuh, rapatkan aksi penting, animasikan komponen yang berubah dan bawa hasil kembali ke konteks produk. Zoom pada satu screenshot sahaja tidak menunjukkan tugas berfungsi. Kekalkan nombor/label sebenar, lindungi bahan peribadi dan semak dakwaan masih semasa. Semak setiap scene/transisi selepas revisi warna supaya tween tidak membawa palet lama semula.

## 4. Motion graphic pendek

Sumber: https://hyperframes.heygen.com/guides/motion-graphics

Gunakan satu unit gerakan untuk tajuk, logo, counter, carta, callout atau route. Tetapkan copy tepat, mekanisme, entrance, hold dan exit. Kebanyakan unit pendek; gabungkan unit ke video berbilang scene jika idea panjang. Saranan durasi pendek artikel bukan had global skill atau larangan narasi yang diminta pengguna.

MP4 sesuai untuk reka bentuk penuh. WebM/MOV beralfa sesuai untuk elemen overlay yang mempunyai ruang kosong; uji alfa di atas footage sebenar dan semak frame masuk/keluar bersih. Cari ID blok sebenar sebelum `add`; rekod custom apabila membina sendiri. Sahkan nilai akhir counter dan keterbacaan pada kelajuan sebenar.

## 5. Muzik dan lirik

Sumber: https://hyperframes.heygen.com/guides/music-to-video

Jadikan trek diluluskan sebagai master masa. Analisis frasa, tenaga, onset, jeda, drop dan penutup sebelum menyusun visual; `beats` dan `audio` ialah alat CLI yang perlu disemak melalui `--help`. Trek berirama boleh menggunakan beat grid; muzik ambient lebih sesuai mengikut frasa/tenaga. Jangan menukar setiap beat menjadi scene.

Jika lirik diperlukan, sahkan teks dan align kepada vokal sebenar dengan ASR/alignment serta review. Reka perubahan kuat pada perubahan muzik yang bermakna; beri masa bacaan dan penutup muzik yang lengkap/loop disengajakan. Ikut julat masa atau turutan aset tepat yang pengguna tetapkan. Tanpa trek, gunakan sumber muzik sah/komposisi tersedia; jangan mendakwa generasi muzik berbayar tersedia. Jangan menambah TTS pada brief tanpa VO.

## 6. Data dan peta

Sumber: https://hyperframes.heygen.com/prompting/data-and-maps

Pisahkan data daripada cara dipaparkan. Pilih bar/line/counter, choropleth, bubble, hex atau flow mengikut soalan. `data-chart` dan blok peta ialah pilihan registry; SVG/GSAP custom memberi kawalan tambahan. Parse CSV dan bake data/geometry ketika build, tanpa fetch CDN semasa render. Gunakan projection sama untuk gabungan warna kawasan, pin dan arcs.

Blok wilayah mempunyai geografi khusus. Untuk Malaysia/negeri, sediakan sempadan/koordinat sah; menukar nama pada `us-map` atau `spain-map` tidak menghasilkan peta Malaysia. Semak sumber, tarikh, unit, denominator, legend, domain paksi dan missing values. Counter mesti berhenti pada nilai tepat tanpa overshoot palsu. Jangan menjadikan interpolasi/bar crossing rekaan sebagai sejarah data sebenar. Semak titik asal/tujuan route dan alfa/label pada hasil akhir.

## 7. Avatar/presenter

Sumber: https://hyperframes.heygen.com/guides/avatar-presenter

Bezakan klip penyampai sedia ada daripada avatar baharu. Servis avatar HeyGen memerlukan akaun dan kredit melalui API/CLI; kajian halaman tidak menyediakan akaun, kredit atau izin menggunakan identiti seseorang. Gunakan rakaman pengguna apabila diberikan dan kekalkan suara/skrip diluluskan. Jangan memasang, mendaftar, berbelanja atau menjana digital twin hanya kerana panduan menyebutnya.

Rancang posisi penyampai dan cutaway supaya muka, produk, carta serta caption tidak berlindung. Untuk teks di belakang manusia, sediakan matte temporal sebenar dan semak pinggirnya. Subtitle perlu mengikuti pertuturan yang benar-benar terhasil. Cache klip final setempat sebelum render; semak sebutan nama/angka, lip-sync apabila relevan, muzik dan playback audio sebenar. Brief tanpa VO tidak memerlukan avatar.

## 8. GitHub pull request

Sumber: https://hyperframes.heygen.com/guides/pr-to-video

**PR di sini ialah pull request**, bukan press release. Baca diff, commit, target branch dan status sebenar. Bezakan cadangan, merged dan released; versi mesti disahkan melalui release/tag/manifest yang berkaitan. Jika akses sumber gagal, laporkan bukti yang kurang dan jangan mereka perubahan.

Untuk pengguna umum, mulakan dengan perubahan yang dilihat dan before/after. Untuk pembangun, terangkan masalah, tradeoff dan laluan kod penting. Hadkan snippet kepada baris yang terbaca; pilih `code-diff`, `code-morph` atau `code-typing` mengikut fungsi dan ketersediaan sebenar. Ujian/refactor tidak semestinya feature baharu. Semak contributor, breaking change, versi dan repo URL; jangan publish kod/bahan peribadi secara automatik.

## 9. Slideshow interaktif

Sumber: https://hyperframes.heygen.com/guides/slideshow

Deck ini dikawal presenter: reveal setiap klik, branch/hotspot, Back ke keadaan asal, notes dan timer. Satu slaid membawa satu dakwaan dan bukti; butiran opsyenal masuk branch. Gunakan `run_hyperframes.mjs present /absolute/project` selepas menyemak `present --help` versi terkunci.

**Jangan `render` deck interaktif terus sebagai MP4.** Dokumentasi semasa menyatakan tiada master composition seluruh deck; output boleh hanya mengandungi slaid pertama walaupun command berjaya. Jika pengguna mahu MP4, bina komposisi video biasa dengan root master, tempoh serta offset eksplisit bagi semua adegan, kemudian render dan sahkan bilangan adegan/durasi. Jika pengguna mahu PowerPoint, guna skill slaid/Presentations; HTML live deck bukan fail PPTX. Jangan menambah gate perancangan slaid pada permintaan video biasa.

## 10. Video custom/campuran

Sumber: https://hyperframes.heygen.com/guides/general-video

Gunakan bagi gabungan interview, footage, grafik, data, muzik dan sumber lain, cerita panjang atau format luar biasa. Tentukan hasil/audiens, sumber mana mesti kekal, dan tahap kerja bersama yang pengguna mahukan. Jika pengguna sudah meminta terus siap, buat keputusan pengarahan dalam skop yang diberi; storyboard dan review dalaman tidak memerlukan kelulusan baharu secara automatik.

Susun satu cerita dan master masa; setiap sumber mesti mempunyai fungsi. Kekalkan kata-kata penyampai apabila diwajibkan. Reka semula komposisi bagi setiap nisbah, bukan crop buta. Semak pembukaan, penutup, peranan audio/senyap dan semua scene sebelum eksport. Gunakan laluan khusus bagi sumber dominan; jangan menjadikan custom alasan mengabaikan fakta atau bukti sebenar.

## 11. Selaraskan panduan dengan arahan pengguna

- **Satu idea bukan satu prop.** Banyak objek, teks keluar masuk dan scene panjang gaya Salah Label dibenarkan jika menyokong satu fokus dengan pertukaran keadaan yang jelas.
- **Durasi dan skrip.** Dengan VO, audio akhir menentukan timing; saranan `~60s` membantu anggaran. Arahan pengguna mengenai durasi tepat dan perkataan verbatim tetap diutamakan. Jangan potong, tambah atau memecutkan skrip secara senyap apabila kedua-duanya bercanggah; siapkan timing/bukti dan nyatakan tradeoff sebenar.
- **Narasi pilihan.** Banyak contoh rasmi menggunakan TTS, ambient idle atau palet tertentu; itu bukan default wajib. Kekalkan tanpa VO apabila diminta; gunakan Google AI Studio mengikut skill suara sedia ada apabila narasi diperlukan. Jangan menukar penyedia secara senyap.
- **Gerak selepas mendarat.** Contoh prompt tertentu mencadangkan breathing/pulse, tetapi panduan motion semasa mengutamakan teks/UI yang berhenti selepas masuk. Pilih aksi produk/prop dan kamera yang bermakna; jangan copy loop hiasan untuk mengelak frame statik.
- **Studio berbanding runtime setempat.** Reference API, avatar, cloud render, generasi muzik dan publish mempunyai keperluan berasingan. Render HTML setempat tidak memerlukan semua servis itu; semak kemampuan sebenar dan kebenaran sebelum menggunakannya.
- **Kekalkan alat pengguna.** Python/FFmpeg untuk footage, Whisper/matte, Atlas/CFX asal, lesen fon, aset serta checkpoint kekal. Jangan memindahkan semuanya ke HTML atau mendakwa semua blok/preset telah diuji.

## 12. QA dan status kemampuan

Gunakan aliran preflight → lint/check → snapshot/proof → review → render → metadata/decode dalam `hyperframes-codex-examples.md`. Tambah bukti mengikut genre: takeaway explainer, aksi/bukti produk, alfa overlay, sync muzik/lirik, nilai/projection data, suara/matte presenter, status PR dan navigation deck.

Untuk deck, ujian yang sesuai ialah klik reveal/branch/Back dan notes; untuk MP4, periksa seluruh urutan dan durasi. Satu skrin/slaid atau exit code renderer sahaja tidak membuktikan hasil lengkap. Untuk semua genre, label perkara **dibaca**, **diadaptasi**, **diuji** dan **belum tersedia** dengan tepat. Kajian sembilan panduan ini tidak menjalankan API avatar, capture laman produk sebenar, transkripsi lirik, akses PR pengguna atau render sembilan video baharu.
