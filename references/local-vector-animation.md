# Vektor, rajah dan watak untuk frame deterministik

## Kandungan

- Tujuh langkah memperkemas vektor sebelum render panjang
- Lapan panduan seni lukisan dan bahasa visual
- SVG yang boleh dianimasikan
- Lapan langkah posisi tubuh natural dan gerakan smooth
- Enam panduan sudut watak, dialog, interaksi dan ujian rig
- Transform sebelum morph
- Raster dan capture

## Tujuh langkah memperkemas vektor sebelum render panjang

Utamakan reka bentuk artwork, perkadaran watak dan rig. Gunakan FFmpeg untuk
menyusun, menggabung dan mengekod hasil yang sudah dirender; baiki rupa watak pada
artwork serta pose sebelum mengejar resolusi atau FPS lebih tinggi. Gunakan aliran
ini untuk watak baharu dan untuk revisi apabila pengguna meminta vektor lebih
cantik, konsisten, smooth atau mempunyai nisbah badan yang logik.

1. Sediakan reka bentuk watak dahulu. Bina helaian model pandangan depan, sisi
   dan tiga suku. Tetapkan siluet, bentuk muka, mata, hidung, tangan, pakaian,
   ketebalan garisan dan palet warna. Simpan identiti serta ukuran dalam satu
   spesifikasi watak; guna semula artwork/rig itu sepanjang video. Kekalkan
   wajah, pakaian dan ciri individu merentas pose serta sudut kamera.

2. Bandingkan semua watak dalam satu gambar. Susun barisan watak pada garisan
   lantai dan skala dunia yang sama. Semak tinggi relatif, saiz kepala, lebar bahu,
   panjang lengan/kaki dan saiz tangan/kasut. Gunakan unit kepala atau ukuran
   reka bentuk yang tetap mengikut umur serta gaya. Simpan nilai sebagai parameter
   bersama, supaya setiap adegan tidak mereka ukuran baharu. Bezakan perubahan
   saiz akibat perspektif/kamera daripada perubahan anatomi yang tidak disengajakan.

3. Lukis bentuk dengan lengkung SVG yang kemas. Gunakan Bézier untuk muka,
   tudung/rambut, pakaian dan anggota, dengan kontur yang terkawal serta butiran
   yang terbaca pada saiz akhir. Pisahkan kepala, torso, lengan atas/bawah, tangan,
   paha, betis, kaki dan props kepada group/lapisan ber-ID stabil. Gunakan renderer
   setempat yang tersedia: contohnya Python mengira atribut SVG setiap frame,
   CairoSVG/sharp meraster PNG, kemudian FFmpeg menghasilkan MP4. Semak sokongan
   font, mask dan filter sebenar; jangan menganggap animasi SVG dibakar automatik.

4. Tambah kedalaman yang terkawal. Tetapkan satu arah cahaya utama, bayang lembut,
   sedikit highlight dan lipatan pakaian yang mengikuti bentuk serta pose. Letak
   bayang sentuhan di bawah kaki dan props. Asingkan foreground, midground dan
   background dengan kontras atau tona yang sesuai; kekalkan arah cahaya/bayang
   konsisten apabila kamera bergerak. Semak tepi alpha dan elakkan butiran yang
   berkelip atau menenggelamkan wajah.

5. Bina rig pada sendi sebenar. Letakkan pivot pada bahu, siku, pergelangan,
   pinggul, lutut dan buku lali. Hubungkan anggota secara parent–child, kekalkan
   panjang tulang dan sediakan pertindihan bentuk/pakaian pada sendi. Kunci tangan
   pada props semasa memegang dan tapak kaki pada tanah semasa menampung badan.
   Gunakan IK jika sesuai; laraskan sasaran yang tidak tercapai melalui pose atau
   komposisi. Uji pose paling ekstrem untuk celah leher, siku terputus dan lutut salah.

6. Reka gerakan mengikut aksi. Untuk mengambil telefon, selaraskan pandangan mata,
   bahu, siku, tangan dan genggaman dengan kedudukan telefon. Gunakan pecutan,
   nyahpecutan, anticipation dan settle mengikut berat serta tujuan aksi. Tambah
   kelipan mata, pernafasan dan gerak susulan pakaian pada amplitud kecil. Hubungkan
   gerakan melalui cue dan masa frame eksplisit; kekalkan pose yang mudah dibaca.
   Nilai kelancaran pada playback serta frame bersebelahan, bukan FPS sahaja.

7. Semak gambar pegun sebelum render panjang. Render sekurang-kurangnya tiga
   styleframe: close-up muka, seluruh badan dan dua watak bersama; jika hanya satu
   watak, gunakan pose/props yang menguji skala. Periksa wajah, sambungan anggota,
   nisbah, bayang, crop dan kebolehbacaan. Baiki isu, kemudian render petikan aksi
   3–5 saat yang merangkumi pose ekstrem serta sentuhan objek. Gunakan supersampling
   sederhana jika masa/memori mengizinkan dan downsample sekali ke resolusi akhir.
   Betulkan artwork serta rig dahulu; ketajaman eksport tidak membetulkan anatomi.
   Teruskan semakan dan pembetulan dalaman secara autonomi dalam skop yang diberi;
   jangan menjadikan langkah ini syarat menunggu kelulusan tambahan pengguna.

Untuk storytelling berlatar cream seperti yang dibincangkan pengguna, gunakan
vektor editorial semi-realistik sebagai titik mula: muka tiga suku, tubuh seimbang,
pakaian berstruktur, palet lembut dan bayang halus. Gunakan pilihan ini apabila
sesuai dengan brief itu; rujukan serta gaya terbaru pengguna tetap menentukan rupa
projek lain. Pastikan pakaian dan identiti watak kekal seperti diminta.

## Lapan panduan seni lukisan dan bahasa visual

Gunakan panduan ini untuk memperhalus artwork dalam tujuh langkah di atas.
Sesuaikan kepada gaya serta rujukan projek; kekalkan semakan dalaman autonomi.

1. Tetapkan rujukan gaya yang jelas. Gunakan 2–3 contoh rupa yang tersedia dan
   sesuai, atau styleframe asal projek, untuk menetapkan cara melukis muka,
   tangan, pakaian, garisan serta warna. Ringkaskan keputusan dalam satu helaian
   gaya dan guna semula sepanjang produksi. Ambil prinsip reka bentuk sambil
   mengekalkan artwork asal; patuhi arahan code-only atau larangan model generatif
   apabila dinyatakan pengguna.

2. Gunakan bentuk yang mempunyai karakter. Reka siluet badan, pipi, dagu, bahu
   dan pakaian dengan lengkung yang disengajakan. Pastikan aksi boleh dibaca
   melalui siluet; semak tangan tidak tenggelam pada torso. Gunakan sedikit
   asimetri pada pose serta ekspresi apabila sesuai dan kekalkan perkadaran model.

3. Perhalus wajah. Kawal jarak mata, kedudukan hidung, bentuk rahang dan lengkung
   mulut pada setiap pandangan. Sediakan ekspresi tenang, risau, tersenyum dan
   sedih yang sesuai dengan cerita. Kekalkan identiti wajah ketika bertukar
   ekspresi atau sudut; semak pada close-up untuk mata tersasar, kontur bertindih
   dan bentuk mulut yang tidak sesuai. Hormati umur, identiti dan gaya pengguna.

4. Beri perhatian khusus kepada tangan. Sediakan pose terbuka, menunjuk,
   menggenggam dan memegang props. Bentuk ibu jari, arah pergelangan serta lilitan
   jari perlu sepadan dengan aksi dan orientasi objek. Urus overlap/occlusion
   secara logik; jari yang terlindung tidak perlu dipaparkan semuanya. Kekalkan
   saiz tangan serta sambungan pergelangan dan semak genggaman pada close-up.

5. Gunakan sistem ketebalan garisan. Contohnya, tetapkan kontur luar sedikit
   tebal, garisan pakaian sederhana dan butiran muka lebih halus. Simpan nilai
   mengikut unit reka bentuk dan guna sistem yang sama pada watak serta props.
   Semak ketebalan pada zoom dan saiz eksport akhir supaya butiran tidak hilang
   atau menjadi terlalu berat. Sesuaikan kepada gaya tanpa memaksa outline bagi
   artwork yang memang direka tanpa garisan.

6. Kawal hierarki warna. Pilih palet terhad dengan warna utama, sokongan dan
   aksen. Bezakan watak daripada latar melalui tona serta kontras; jadikan wajah,
   aksi dan objek utama mudah dikenal pasti. Semak dalam grayscale sebagai
   bantuan menilai pemisahan tona, kemudian semak semula warna sebenar. Kekalkan
   palet merentas adegan dan pastikan warna aksen menyokong fokus cerita.

7. Bezakan sifat bahan. Gunakan lipatan lembut yang mengikuti bentuk pada
   tudung/baju, tepi tegas pada telefon dan pantulan terkawal pada kaca. Padankan
   highlight, bayang serta butiran dengan bahan dan arah cahaya. Kekalkan tahap
   perincian yang seimbang; semak supaya tekstur atau pantulan tidak berkelip
   apabila objek bergerak atau dikecilkan ke resolusi akhir.

8. Perkemas komposisi setiap shot. Sediakan ruang di arah pandangan serta
   pergerakan watak. Elakkan garisan latar bersilang secara mengganggu dengan
   muka atau menghasilkan tangent pada kontur badan. Pastikan props penting
   mudah dilihat, sediakan ruang subtitle/teks yang diminta, dan jaga safe area.
   Gunakan close-up untuk emosi serta shot lebih luas untuk menerangkan aksi;
   kekalkan arah pandangan, kedudukan dunia dan kesinambungan antara shot.

Bagi projek pengguna yang banyak zoom dekat pada watak, utamakan semakan wajah,
tangan, bentuk pakaian dan sistem garisan. Nilai keempat-empatnya pada styleframe
close-up serta petikan gerak sebenar sebelum master panjang. Perincian ini ialah
arahan seni dan QA, bukan dakwaan bahawa renderer baharu telah dibina atau diuji.

## SVG yang boleh dianimasikan

Mulakan dengan mesej, siluet dan hierarki bentuk. Tetapkan `viewBox`, palet kecil,
stroke konsisten, ruang negatif serta kontras teks. Gunakan path Bézier bersih,
gradient berarah dan clipping sederhana; elakkan menambah butiran yang hilang pada
telefon. Gunakan sistem koordinat yang boleh dibaca dan ID unik untuk `defs`.

Bahagikan artwork kepada group semantik: latar, tubuh, lengan kiri/kanan, kepala,
mata, mulut, props, label dan foreground. Simpan pivot berhampiran sendi dan origin
tempatan yang mudah digunakan. Kekalkan teks sebagai teks jika font/shaping tepat;
untuk logo pengguna atau huruf yang perlu kekal rupa, guna aset asal yang dibenarkan.

Untuk rajah/infografik, bina node, connector dan label secara berasingan. Simpan
geometri node supaya titik anak panah dikira daripada sempadan, bukan koordinat
agak-agak. Reveal proses mengikut urutan narasi, warnakan laluan aktif, dan biarkan
bahagian yang sedang dibaca stabil. Semak semua label/panah pada raster final.
Diagram klinikal/teknikal perlu ketepatan domain; rupa SVG bukan bukti kandungan.

## Lapan langkah posisi tubuh natural dan gerakan smooth

Gabungkan pose yang seimbang, rig sendi bersambung dan timing setiap anggota.
Sesuaikan kepada aksi, gaya, umur serta rujukan watak; gunakan panduan ini semasa
merancang pose dan membetulkan gerakan kaku. Utamakan pemindahan berat badan,
kaki berpijak, tangan memegang dengan tepat dan sela masa antara anggota.

1. Bentuk satu garis aksi pada badan. Tentukan arah badan sedang bergerak,
   mencapai atau membongkok, kemudian selaraskan kepala, tulang belakang dan
   pelvis dengan aksi itu. Beri perbezaan yang munasabah pada kedudukan bahu,
   tangan serta kaki supaya siluet mudah dibaca. Semak pose utama dan pose
   perantaraan; kekalkan bentuk watak ketika bertukar pose.

2. Tunjukkan pemindahan berat badan. Semasa mencapai objek, laraskan condongan
   torso, kedudukan pelvis dan kaki yang menyokong supaya imbangan meyakinkan.
   Semasa berjalan, bezakan fasa stance dan swing; kunci tapak kaki pada dunia
   semasa stance, gerakkan pelvis bersama langkah dan lepaskan contact pada
   toe-off. Selaraskan pergerakan dunia/kamera supaya kaki tidak meluncur.

3. Hubungkan anggota melalui hierarki sendi. Gunakan pelvis → torso → bahu/leher
   → kepala; bahu → lengan atas → siku → lengan bawah → pergelangan → tangan;
   pelvis → paha → lutut → betis → buku lali → kaki. Transform parent dahulu,
   kemudian transform setempat. Kekalkan panjang tulang, pivot pada sendi serta
   pertindihan bentuk/pakaian yang menutup sambungan semasa membengkok. Hadkan
   sudut mengikut pose dan rujukan, tanpa memaksa semua aksi kepada satu sudut.

4. Gunakan IK untuk titik sentuhan. Bagi tangan yang memegang props atau kaki
   yang menyokong badan, tentukan sasaran dalam koordinat dunia/objek yang jelas.
   Gunakan IK dua tulang jika sesuai dan kekalkan arah lenturan siku/lutut.
   Laraskan target atau pose yang tidak tercapai sambil mengekalkan panjang
   anggota. Kekalkan tangan pada titik genggaman dan objek mengikuti tangan
   selepas diangkat; tukar constraint secara beransur pada sentuh/lepas supaya
   tiada snapping. Semak IK tidak bertukar sisi secara mendadak.

5. Gerakkan anggota mengikut lengkung. Reka laluan tangan, siku dan kaki mengikut
   putaran sendi serta tujuan aksi, menggunakan arc atau spline apabila sesuai.
   Semak pose di antara keyframe untuk anggota menembusi tubuh, props atau lantai.
   Gabungkan laluan yang menarik dengan constraint sentuhan; jangan mengalihkan
   hujung anggota daripada titik contact semata-mata untuk mengekalkan arc.

6. Beri sela masa antara anggota. Jadualkan pandangan, kepala, torso, bahu,
   siku, pergelangan dan genggaman mengikut tujuan aksi. Gunakan contoh mengambil
   telefon di bawah sebagai panduan, kemudian sesuaikan urutan dan durasi.
   Pisahkan pose utama, ekspresi dan idle. Letakkan gesture pada cue narasi yang
   relevan; gunakan kelipan, pernafasan serta gerak susulan pakaian yang kecil
   dan berpusat pada anchor asal. Beri settle dan ruang membaca selepas aksi.

7. Kawal kelajuan serta perubahan arah. Reka acceleration, deceleration,
   anticipation dan follow-through mengikut berat objek serta sifat aksi.
   Sambungkan keyframe supaya kedudukan dan kelajuan berterusan; haluskan
   perubahan acceleration apabila perlu. Gunakan easing bagi mula/berhenti,
   sambil mengekalkan fasa berterusan untuk gerak berkala seperti kayuhan.
   Pilih easing/spring analitik atau cache fixed timestep yang boleh seek.
   Kekalkan amplitud gerak susulan kecil dan elakkan getaran pada akhir gerakan.

8. Kira gerakan daripada masa sebenar. Gunakan `t = frame / fps` dan kedudukan
   pecahan piksel; kira pose baharu bagi setiap frame, termasuk eksport 60 fps.
   Simpan geometri dalam koordinat dunia sebelum transform kamera dan raster.
   Elakkan pembundaran koordinat awal serta state yang bergantung pada jumlah
   panggilan render. Semak satu kitaran penuh dan setiap fasa contact pada playback
   biasa serta frame bersebelahan, termasuk sambungan segmen. Jika playback tidak
   tersedia, nyatakan had itu dan semak frame tanpa mendakwa kelancaran subjektif.

Contoh urutan aksi mengambil telefon; masa setiap fasa ditentukan oleh narasi,
jarak objek dan tujuan shot, tanpa mewajibkan satu tempo untuk semua aksi:

| Fasa | Pergerakan tubuh dan objek |
| --- | --- |
| Persediaan | Mata dan kepala memandang telefon; badan menyediakan imbangan. |
| Mencapai | Badan condong, bahu dan lengan bergerak ke sasaran. |
| Menyentuh | Pergelangan menyesuaikan arah; jari membentuk genggaman. |
| Mengangkat | Telefon mengikuti tangan; badan menyesuaikan imbangan. |
| Berhenti | Gerakan mengecil dan menetap; genggaman serta contact kekal. |

Gunakan tiga styleframe dan petikan aksi 3–5 saat daripada aliran semakan di atas
untuk menilai panduan ini sebelum master panjang. Baiki pose, contact dan timing
dalam skop kerja yang diberi tanpa menambah syarat kelulusan pengguna. Panduan
ini meluaskan arahan rig dan QA; ia tidak mendakwa enjin gerakan baharu sudah diuji.

Hormati pakaian, identiti dan posisi pengguna apabila diberi rujukan. Jangan
mewarisi branding, watak demo, tema atau teks repo ke projek pengguna.

## Enam panduan sudut watak, dialog, interaksi dan ujian rig

Lengkapkan panduan artwork dan gerakan di atas dengan semakan berikut. Utamakan
sinkroni audio/subtitle, pertukaran sudut wajah dan bentuk anggota ketika membengkok
apabila isu tersebut muncul dalam projek. Sesuaikan lip-sync kepada watak yang
benar-benar bercakap; narasi luar skrin tidak mewajibkan mulut semua watak bergerak.

1. Rancang pertukaran sudut watak. Sediakan pandangan depan, sisi dan tiga suku
   daripada model yang sama. Tetapkan landmark muka, telinga, tudung/rambut, leher
   serta bahu untuk setiap sudut. Semasa menoleh, ubah bentuk dan pertindihan
   bahagian mengikut perspektif; kekalkan identiti, ukuran dunia dan sambungan
   tubuh. Semak pose di antara sudut supaya mata, hidung, telinga atau kontur tidak
   melompat. Gunakan artwork pandangan khusus jika transform rata tidak memadai.

2. Kekalkan bentuk anggota ketika membengkok. Sediakan bentuk siku, lutut,
   bahu dan pakaian bagi pose ekstrem, dengan pertindihan atau deformation yang
   sesuai. Kekalkan panjang tulang serta isipadu/siluet yang meyakinkan; semak
   anggota tidak mengecil, mengembang atau kelihatan seperti getah tanpa tujuan.
   Bezakan foreshortening akibat perspektif daripada perubahan saiz yang tidak
   disengajakan. Sesuaikan exaggeration kepada gaya pengguna dan semak kedua-dua
   hujung serta pertengahan gerakan.

3. Selaraskan ekspresi dan arah pandangan. Nyatakan objek/orang yang sedang
   dilihat serta emosi atau tujuan watak dalam setiap beat. Padankan mata,
   kening, mulut dan kepala dengan aksi serta reaksi. Kekalkan pandangan pada
   sasaran yang bergerak melalui koordinat dunia yang sama, kemudian transform
   ke kamera. Gunakan kelipan dan perubahan ekspresi pada cue yang sesuai sambil
   mengekalkan identiti wajah dan ruang untuk penonton membaca emosi.

4. Selaraskan suara, mulut dan subtitle kepada audio sebenar. Gunakan satu jam
   master berasaskan fail audio akhir. Ambil masa frasa/perkataan daripada audio
   melalui alignment yang tersedia atau semakan manual; tandakan anggaran jika
   belum disahkan. Bagi dialog watak, gunakan bentuk mulut/viseme yang sesuai
   dengan bunyi dan transisi yang lembut; bentuk waveform sahaja tidak mengenal
   pasti fonem. Kekalkan mulut pada pose yang sesuai ketika jeda dan mendengar.
   Paparkan subtitle mengikut frasa, jeda serta ruang bacaan; kira masa entrance
   supaya animasi tidak menyebabkan teks lewat siap dibaca. Semak awal, tengah,
   hujung, cut dan sambungan segmen untuk offset/drift. Selepas audio berubah,
   bina semula cue yang terjejas. Hormati lokasi subtitle dan suara yang telah
   diluluskan. Rujuk [cue audio dan caption](cme-v3-audio-captions.md) serta
   [caption dan revisi visual](center-captions-clean-cuts.md) apabila berkaitan.

5. Rancang interaksi antara watak. Semak eyeline, jarak, skala, arah tubuh,
   giliran bercakap dan reaksi pendengar dalam sistem koordinat dunia yang sama.
   Kekalkan arah pandangan serta hubungan ruang merentas shot. Untuk menyerahkan
   objek, tetapkan saat pemberi melepaskan dan penerima mengambil alih; kekalkan
   satu pemilik transform utama objek pada setiap fasa, dengan peralihan contact
   yang terkawal. Semak tangan, genggaman, occlusion dan lintasan objek supaya
   tiada teleport, pendua objek atau anggota menembusi tubuh.

6. Gunakan rutin ujian rig yang boleh diulang. Uji aksi berdiri, berjalan,
   duduk, menoleh, mencapai dan memegang objek seperti jadual di bawah apabila
   rig menyokongnya. Jika aksi baharu diperlukan cerita, tambah ujian itu sebelum
   render panjang. Semak sendi, panjang anggota, foot sliding, interpenetration,
   pertukaran z-order dan perubahan pose mendadak. Gunakan julat masa serta seed
   tetap untuk membandingkan revisi. Ukuran geometri membantu mengesan ralat;
   semakan frame dan playback masih diperlukan untuk menilai rupa serta gerak.

| Aksi ujian | Semakan utama |
| --- | --- |
| Berdiri | Imbangan, contact tanah, pernafasan kecil dan sambungan anggota. |
| Berjalan | Stance/swing, kaki berpijak, pergerakan pelvis dan kesinambungan kitaran. |
| Duduk | Contact kerusi, lipatan pinggul/lutut, pakaian dan tubuh tidak menembusi tempat duduk. |
| Menoleh | Identiti wajah, landmark perspektif, arah mata dan sambungan leher/bahu. |
| Mencapai | Arc tangan, sasaran dalam reach, arah siku dan pemindahan berat badan. |
| Memegang | Genggaman, pergelangan, objek mengikuti tangan dan release yang berterusan. |

Jalankan semakan dalaman ini dalam skop kerja yang diberi tanpa menambah gate
kelulusan pengguna. Ini ialah panduan produksi serta rutin QA yang perlu
dilaksanakan pada rig projek; jangan melaporkannya sebagai ujian render yang
sudah lulus hanya kerana arahan ini telah disimpan dalam skill.

## Transform sebelum morph

Utamakan translate/rotate/scale/opacity/reveal untuk gerak biasa. Morph path hanya
apabila perubahan bentuk menyampaikan makna. Samakan bilangan path, subpath,
bilangan serta jenis command, arah winding dan correspondence titik sebelum
interpolasi. Jangan interpolate dua rentetan `d` yang tidak sepadan terus.

Jika menggunakan normalizer seperti flubber, semak library/lesen dan simpan salinan
tempatan; jangan bergantung pada CDN sewaktu render. Uji bentuk pada p=0, .25, .5,
.75, 1 untuk lubang, self-intersection, fill-rule dan bounding box. Jika topologi
berbeza besar, gunakan wipe, split menjadi beberapa path atau crossfade yang jelas.

## Raster dan capture

Jadikan setiap frame hasil `svg_at(t)` atau `renderFrame(t)`. Untuk SVG statik yang
berubah melalui kod, raster semula atribut yang sudah dikira. SMIL/CSS animasi di
dalam XML belum tentu disokong CairoSVG/sharp. Untuk browser, tunggu font dan imej,
pause/seek animasi dan tangkap selepas state stabil; elakkan eksport berdasarkan
`performance.now()`/`requestAnimationFrame` yang mengikut kelajuan mesin.

Gunakan oversampling sederhana bagi garisan halus, kemudian downsample sekali.
Periksa huruf, clipping, filter, gradient dan mask dalam renderer sebenar. Semak
alpha pada latar terang dan gelap. Jangan membuat andaian bahawa SVG sah XML akan
memberikan piksel sama dalam Chromium, CairoSVG, sharp dan pemain Lottie.

Rujuk `scripts/vector_cyclist.cjs` dan `scripts/vector_small_steps.cjs` untuk contoh
rig sedia ada. Salin/adaptasi komponen sesuai; jangan ubah contoh induk menjadi teks
projek baharu. Gunakan adapter Canvas serta panduan eksport dalam
[aliran setempat](local-video-pipeline.md). Semua teknik tambahan ialah integrasi
terpilih daripada [audit sumber](local-video-sources.md), bukan pemasangan penuh
atau penambahan ID preset baharu.


## Bank multi-sudut dan kamera V3

Gunakan [bank watak V3](character-bank-20.md) untuk enam orientasi penuh, 42 pose dan 34 gerakan. Padankan tubuh, kepala, pakaian dan kasut; view kiri memantulkan keseluruhan artwork. Elakkan teks/logo terbalik dan gunakan perubahan artwork 2D yang sesuai untuk turn. Baca [kamera vektor Python](vector-camera-engine.md) untuk kamera world/screen, elbow IK dan zoom yang merender geometri pada kanvas sasaran. Kekalkan caption/VO/preset mengikut brief projek, termasuk storytelling tanpa kinetic typography apabila diminta.
