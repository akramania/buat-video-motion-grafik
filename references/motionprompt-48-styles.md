# Bank 48 gaya MotionPrompt yang diadaptasi untuk motion grafik

Sumber rujukan: [MotionPrompt oleh Ahmad Saiful Bahri](https://epool86.github.io/motionprompt/). Disemak pada 27 September 2026. Katalog sumber mempunyai 48 entri dalam `styles.json`: 42 terpapar dalam galeri dan enam bertanda `hidden` tetapi masih mempunyai prompt. Bank ini ialah olahan resipi produksi, bukan salinan prompt asal. Semua ID MP01–MP48 kini mempunyai implementasi 2D/2.5D sendiri dalam `assets/motion_presets/motionprompt.py` dan boleh dieksport melalui `render.py`. Preview kod ialah titik mula yang lebih ringkas daripada arahan kreatif penuh dalam resipi di bawah.

## Indeks pilihan mengikut fungsi adegan

| Kegunaan | ID yang wajar diperiksa |
| --- | --- |
| Tipografi dan latar abstrak | MP07, MP13, MP15, MP19, MP28, MP35, MP38, MP46, MP48 |
| Penerangan, carta dan ruang | MP02, MP03, MP05, MP11, MP17, MP34, MP37 |
| Produk, peranti dan tawaran | MP04, MP06, MP09, MP21, MP27, MP30, MP31, MP47 |
| Budaya dan tempat Malaysia | MP08, MP16, MP22, MP25, MP26, MP29, MP33, MP41 |
| Perayaan lain dan majlis | MP20, MP36, MP44 |
| Bahan buatan tangan dan watak | MP10, MP18, MP32, MP42 |
| Cerita, foto dan suasana retro | MP01, MP12, MP14, MP23, MP24, MP39, MP40, MP43, MP45 |

## Cara pakai

1. Salin **arahan induk** di bawah.
2. Pilih satu atau beberapa ID `MP01` hingga `MP48` dan salin blok resipinya di bawah arahan induk.
3. Tambah skrip, aset, nisbah, tempoh, bahasa dan arahan suara. Untuk gabungan gaya, pilih satu gaya asas per adegan dan satu aksen daripada gaya kedua; jangan campurkan semua gaya dalam satu frame.
4. Render ID yang dipilih sebagai preview enam saat, semak hasilnya, kemudian tambah aset sebenar dan gerak tambahan untuk projek kompleks. Semua ID MP boleh dipanggil terus oleh `render.py`.

## Render terus melalui preset sedia ada

Dari direktori `assets/motion_presets/`:

```bash
python render.py --preset MP03 --frame 2.6 --clean --output roda.png
python render.py --preset MP09 --duration 6 --fps 30 --clean --output aplikasi.mp4
python render.py --config /path/projek/MP24.json --clean --output foto.mp4
python render.py --list
```

Gunakan JSON untuk `text`, `subtitle`, `genre`, `accent`, `image_paths`, `items` dan input khusus seperti `values` pada MP17, `rooms` pada MP37 atau `amplitudes` pada MP40. Fail gambar digunakan dengan nisbah asal melalui contain. Enam gaya yang berimej 3D di laman sumber (`MP06`, `MP21`, `MP27`, `MP35`, `MP37`, `MP47`) diimplementasikan di sini sebagai ilustrasi kedalaman 2.5D, tanpa mesh atau rig 3D. Semua MP dalam CLI semasa ialah scene senyap 16:9; susun semula layout untuk 9:16 dan sync dengan suara pada projek video lengkap. Angka, pelan dan waveform demo mesti diganti oleh data pengguna sebelum video fakta diterbitkan.

## Arahan induk untuk ChatGPT Work/Codex atau Hermes

```text
Gunakan skill buat-video-motion-grafik untuk menghasilkan SATU video MP4 siap ditonton, bukan hanya prompt atau slaid statik. Kandungan: [SKRIP/TOPIK]. Gaya visual: [SALIN RESIPI MPxx]. Sasaran: [AUDIENS]. Format: [9:16 / 16:9 / 4:5 / 1:1], [TEMPOH], [30/60 fps selepas ujian], Bahasa Melayu Malaysia kecuali dinyatakan sebaliknya.

Bina scene daripada lapisan sebenar: subjek hero, elemen tengah, elemen depan, latar dan tekstur/cahaya. Dalam setiap scene, tetapkan gerak masuk, aksi semasa dipaparkan dan keluar bagi objek utama. Gunakan beberapa beat pantas setempat dalam scene yang lama; gerakkan objek, UI, angka atau kamera mengikut sebab cerita. Pilih kinetic typography yang berubah mekanismenya menurut mesej. Satu fokus visual paling kuat pada setiap beat. Sediakan ruang selamat 9:16 dan baca di skrin telefon; jangan ada header kecil yang tidak perlu, teks bertindih, atau ruang kosong tanpa fungsi.

Jika saya bekalkan foto, slaid, logo, video atau screenshot, kekalkan kandungan dan nisbahnya: gunakan contain serta panel/latar pelengkap apabila perlu, bukan crop subjek atau teks. Caption, jika diminta, berada di tengah pada lapisan paling atas; alihkan elemen lain daripada zon ini. Gunakan potongan terus antara scene, tanpa transition; animasi DALAMAN scene dan reveal objek tetap aktif. Suara latar/sound hanya jika diminta; sejajarkan animasi dengan audio sebenar. Semua nombor, tarikh, ukuran, peta, harga dan fakta mesti berpunca daripada bahan yang diberi atau sumber yang diperiksa. Cipta artwork dan bunyi asal atau gunakan bahan yang dibenarkan.

Sediakan manifest bertanda masa, render MP4, kemudian semak frame utama serta gerak sepanjang video untuk teks, overlap, crop, masa bacaan, audio dan ketepatan fakta. Jika ciri 3D sebenar tidak tersedia, guna komposit 2.5D yang ditandai secara jujur dan jangan dakwa model 3D telah dirender.
```

## Panduan padanan dengan toolkit sedia ada

- `T01–T04`, `X01–X04`, `H01–H04`, `K01–K45`: blok teks, huruf, highlight dan caption.
- `U01–U04`, `N01–N04`, `C01–C04`: UI, telefon, notifikasi dan galeri.
- `L01–L06`: scene panjang yang mengekalkan gerak aksi pantas setempat; `B04/B07` untuk angka sebenar.
- MP01–MP48 ialah preset renderer yang tersedia. Ia melukis visual contoh dan gerak tersendiri; scene produksi dengan identiti, aset, geografi, budaya atau 3D sebenar masih memerlukan bahan tepat serta komposisi tambahan.

## Semua 48 resipi

### MP01 · Kaiju attack

**Arah:** 2.5D + tipografi sinematik. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#kaiju-attack).

Bina bandar miniatur berlapis: siluet bangunan depan, bumbung, lampu tingkap, asap dan langit berasingan. Gegaran tanah menggerakkan bangunan pada kadar berlainan; raksasa rekaan asal naik dari belakang, matanya menyala dan pancaran cahaya melukis tajuk huruf demi huruf. Selit jalur berita taip, pesawat mainan dan ribbon tawaran. Gerakkan kamera perlahan ke tajuk yang masih berasap. Tekstur filem lama dan SFX gemuruh menyokong komedi retro.

### MP02 · Infographic

**Arah:** 2D data explainer. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#infographic).

Bina satu poster infografik besar yang kamera jelajah mengikut urutan masalah → langkah → bukti → perbandingan → rumusan. Setiap badge nombor, ikon, anak panah bertitik, bar atau angka mempunyai animasi masuk yang tersendiri dan gerak kecil semasa ditahan. Buat kiraan angka hanya daripada data diberi. Jadikan seksyen aktif besar dan terang; seksyen lain kekal konteks. Paparkan tajuk sebagai word reveal, kemudian pullback untuk melihat poster penuh.

### MP03 · Radial infographic

**Arah:** 2.5D radial data. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#radial-infographic).

Mulakan dengan hub pusat, kemudian bentukkan 4–8 bilah warna satu persatu seperti shutter. Pada setiap beat, bilah terpilih mengembang, ikon dilukis, garis penghubung memanjang dan label muncul melalui mask. Kamera bergerak secara orbit kecil tanpa memusingkan teks bacaan. Titik lain redup sewaktu poin aktif. Tamat pada roda lengkap dengan ripple dan sapuan cahaya; ruang label dibesarkan bagi format menegak.

### MP04 · Slide deck

**Arah:** 2.5D galeri slaid. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#slide-deck).

Letakkan slaid sebenar pengguna sebagai kad berbayang di atas meja perspektif; pelihara keseluruhan imej melalui contain, tanpa crop. Slaid jatuh berturutan, kamera bergerak dari satu kad hero ke kad berikutnya dan membesarkan kad aktif. Animasikan elemen di atas kad seperti nombor, penunjuk, garis carta dan callout tanpa mengubah kandungan asal. Selit potongan terus antara penerokaan utama; penutup pullback menunjukkan koleksi penuh.

### MP05 · Flat illustration

**Arah:** 2D ilustrasi watak. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#flat-illustration).

Bina watak dan props vektor sebagai komponen berasingan: torso, lengan, tangan, mata, papan, ikon dan carta. Masukkan tajuk per perkataan; papan dan watak muncul berturutan dengan spring terhad. Ketika narasi, tangan menunjuk item, carta melukis dirinya, checklist ditanda dan ekspresi muka berubah. Susun staging supaya hanya satu tindakan utama menguasai setiap beat, sementara aksi latar tetap hidup dengan pergerakan kecil.

### MP06 · Isometric diorama

**Arah:** 3D toon atau 2.5D isometrik. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#isometric-diorama).

Bina pentas bulat dengan 5–8 objek topik yang benar-benar berlapis dan mempunyai bayang kontak. Objek bangun dari lantai satu persatu, berputar kecil dan bergerak bebas semasa kamera orbit lembut antara sudut lebar dan close-up. Skrin produk memaparkan bahan sebenar pengguna. Jika tiada enjin 3D, gunakan ilustrasi isometrik berlapis dan gerak kamera 2.5D yang jujur. Tajuk ringkas berada di zon bacaan yang stabil.

### MP07 · Kinetic typography

**Arah:** Tipografi kinetik. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#kinetic-type).

Pecahkan mesej kepada frasa 1–3 perkataan; padankan kemunculan dengan beat suara atau muzik, bukan tempo rawak. Variasikan mekanisme: glyph berputar, perkataan jatuh, potongan mask, outline menjadi fill dan echo skala. Setiap frasa mempunyai tempoh hold yang cukup untuk dibaca; kata kunci terakhir tersusun menjadi satu komposisi kuat. Gunakan potongan warna latar yang terkawal dan elakkan teks bertindih.

### MP08 · Malaysian heritage

**Arah:** 2.5D warisan Malaysia. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#malaysian-heritage).

Pisahkan latar sawah/kampung, wau bulan, motif batik dan panel songket kepada lapisan kedalaman. Wau terbang dengan tali dan tassel berayun; motif bunga raya dilukis bagai canting lalu warna meresap. Panel songket terbuka di tengah untuk tajuk besar, sementara corak emas berdenyut halus. Gunakan unsur budaya yang sesuai dengan mesej, bukan menimbun semua motif; kekalkan susunan huruf BM yang jelas.

### MP09 · App showcase

**Arah:** 2.5D UI produk / 3D peranti. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#app-showcase).

Paparkan telefon dengan skrin sebenar, bukan mockup kosong. Peranti tilt dan mengapung lembut; screenshot bersilih melalui scroll dalaman, butang disentuh dengan ripple, dan kad ciri keluar dari sempadan skrin mengikut susunan narasi. Gunakan bayang, reflection dan parallax untuk kedalaman. Setiap fungsi mesti ditunjukkan beroperasi, kemudian ringkaskan manfaat dengan kinetic type besar. Pastikan skrin tidak dipotong.

### MP10 · Kawaii pastel

**Arah:** 2D kawaii berlapis. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#kawaii-pastel).

Watak chibi ialah focal point dengan rig mata, tangan dan mulut ringkas. Pelekat, hati, bintang dan gelembung melantun pada beat berlainan dengan overshoot kecil. Teks bubble berskala besar masuk per kata; watak menghadap, menunjuk atau menyentuh kata kunci. Hadkan jumlah pelekat aktif agar tajuk kekal boleh dibaca. Palet pastel dan bayang lembut mengekalkan rasa comel tanpa menjadi statik.

### MP11 · Tech noir

**Arah:** 2.5D noir teknologi. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#tech-noir).

Bina glob titik, grid perspektif, peranti garis cahaya dan partikel pada kedalaman berlainan. Garis peranti dilukis dari node, data bergerak melalui sambungan dan teks terbentuk daripada titik sebelum settle menjadi glyph jelas. Kamera push-in perlahan pada bukti/produk, sementara cahaya rim dan kabus volumetrik menghidupkan latar. Gunakan scanline sebagai aksen pendek dan bukan gangguan berterusan pada maklumat.

### MP12 · Food menu

**Arah:** 2.5D flat lay makanan. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#food-menu).

Susun meja, pinggan, bahan, bayang, wap dan kad menu sebagai elemen berasingan. Bahan jatuh dari beberapa arah dan tersusun menjadi hidangan hero; kamera top-down bergerak ke hidangan, wap naik perlahan dan kad nama/harga muncul melalui fold serta mask. Kekalkan foto makanan asal jika diberikan, gunakan cutout dan gerak props di sekelilingnya. Utamakan satu hidangan pada satu beat supaya harga mudah dibaca.

### MP13 · Neon sign

**Arah:** Tipografi neon. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#neon-sign).

Lukis laluan tiub huruf pada dinding, hidupkan segmen mengikut urutan dengan flicker singkat, kemudian kekalkan nyalaan stabil. Pantulan cahaya pada bata dan haze bergerak berasingan, sementara kata penting menerima pulse dan bloom yang terkawal. Tambah subteks melalui reveal bersih, bukan flicker yang mengganggu. SFX transformer dan hum halus boleh menyokong, dengan kontras huruf cukup pada skrin telefon.

### MP14 · Map journey

**Arah:** 2D peta animasi. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#map-journey).

Gunakan peta sebenar yang sesuai dengan lokasi. Kamera menjejak laluan yang dilukis, pin jatuh dengan pantulan kecil, label tempat muncul dekat pin dan kad hari/fakta meluncur ke zon bacaan. Ikon kenderaan bergerak sepanjang path secara berterusan, dengan parallax halus awan atau terrain. Urutan lokasi mengikut data, bukan rekaan; buat jeda pada setiap destinasi dan elakkan label bersilang.

### MP15 · Liquid gradient

**Arah:** Latar abstrak berlapis. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#liquid-gradient).

Animasikan blob gradien yang berubah bentuk secara organik dan bergerak pada kelajuan berbeza. Letakkan butir tekstur dan beberapa garis cahaya halus bagi kedalaman, sementara tajuk putih besar muncul melalui soft mask dan kata penting mendapat displacement pendek. Pastikan kontras di belakang teks stabil sepanjang masa. Sesuai sebagai medan visual untuk narasi, tetapi selit kad data atau objek apabila ada maklumat yang perlu ditunjukkan.

### MP16 · Festive Raya · tersembunyi dalam galeri, tersedia melalui pautan terus

**Arah:** 2.5D Raya bercorak. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#festive-raya).

Lapiskan ketupat berayun, pelita bercahaya, bintang dan corak geometri emas pada ruang malam yang hangat. Hidupkan pelita secara berurutan, kemudian dedahkan ucapan utama dari panel kain atau kertas dengan garis emas melukis tepi. Partikel cahaya bergerak perlahan di belakang teks. Gerak mengikuti rentak tenang; simpan motif jauh daripada tulisan Arab atau mesej utama.

### MP17 · Data story

**Arah:** 2D data story. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#data-story).

Bina naratif angka dalam 3–5 kad yang berkongsi grid yang sama. Setiap kad mengangkat satu metrik: counter sampai nilai sebenar, bar naik dengan label, garis menjejak titik, donut berisi mengikut nisbah, lalu satu insight besar dikunci di tengah. Selaraskan digit dan graf dari sumber data yang sama. Tandakan data demo jika belum diberi; jangan cipta statistik. Gunakan morph objek setempat untuk hubungan sebab akibat.

### MP18 · Claymation

**Arah:** 3D clay stop motion. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#claymation).

Gunakan watak dan props dengan bahan tanah liat, cap jari halus serta bayang fizikal. Gerakan watak di-step pada sekitar 12 pose sesaat, sementara kamera bergerak lebih halus untuk rasa produksi sebenar. Watak menolak kad, menggumpal menjadi ikon dan meregang sebagai bentuk penanda; tajuk muncul seperti huruf clay yang ditekan satu persatu. Pastikan aksi sebab-akibat dapat dilihat dan ekspresi berubah dalam shot.

### MP19 · Retro synthwave

**Arah:** 2.5D retro synthwave. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#retro-synthwave).

Grid neon bergerak ke horizon pada beberapa plane, matahari berjalur turun perlahan dan siluet gunung mempunyai parallax. Tajuk chrome timbul dengan highlight yang menyapu mengikut beat, kemudian baris sokongan muncul melalui wipe bersih. Sediakan ruang tengah yang kukuh untuk tawaran atau mesej; gunakan refleksi lantai dan bintang tanpa menenggelamkan teks. Kekalkan gaya 80-an sebagai latar bagi maklumat, bukan hiasan semata.

### MP20 · Elegant wedding

**Arah:** 2D bunga cat air elegan. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#elegant-wedding).

Bina motif bunga cat air yang mekar dari sapuan pigmen dan cabang yang dilukis. Gerak kamera ringan menyusuri lengkung gerbang emas; nama atau tajuk ditulis dengan mask strok yang konsisten dengan bentuk huruf. Partikel foil bergerak sekali sekala, bunga pinggir berayun kecil dan tarikh/CTA muncul dalam kad yang stabil. Latar tenang dan masa hold panjang memastikan ucapan dapat dibaca.

### MP21 · 3D logo spin

**Arah:** 3D logo identiti. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#logo-spin-3d).

Gunakan fail logo asal sebagai sumber bentuk; extrude geometri jika sesuai, atau pasang logo rata pada plane 3D jika bentuk tidak sesuai untuk extrusion. Logo berputar satu paksi terkawal, menangkap sapuan cahaya, settle menghadap kamera dan terapung sedikit. Cipta bayang serta refleksi studio, kemudian reveal tagline melalui mask pendek. Jangan ubah proporsi, ejaan atau warna identiti tanpa arahan.

### MP22 · Kopitiam · tersembunyi dalam galeri, tersedia melalui pautan terus

**Arah:** 2.5D kopitiam. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#kopitiam).

Bina ruang kopitiam berlapis dengan meja, cawan, teko, wap, papan kapur dan cahaya pagi. Teh ditarik sebagai aliran lentur yang bersambung, percikan berhenti sebelum mengganggu teks, lalu tulisan menu muncul seperti kapur strok demi strok. Kamera beralih daripada aksi minuman kepada produk/harga pada kad yang besar. Gerak kipas dan wap berulang lembut untuk memberi kehidupan pada hold.

### MP23 · Comic pop art

**Arah:** 2D komik pop art. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#comic-pop-art).

Pecahkan cerita kepada panel komik dengan satu aksi dominan pada setiap panel. Panel meluncur dan berhenti pada grid, halftone muncul melalui mask, bubble bercakap mengembang dari watak dan kata impak seperti POW dihentak pada beat. Gunakan tangan/lengan atau objek produk sebagai cutout untuk keluar dari sempadan panel. Teks fakta kekal dalam kotak berkontras tinggi; variasikan skala dan posisi tanpa bertindih.

### MP24 · Photo slideshow

**Arah:** 2.5D foto editorial. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#photo-slideshow).

Gunakan foto sebenar sebagai kad penuh yang tidak dipotong, dengan latar blur atau perluasan reka letak untuk memenuhi ruang. Animasikan kad masuk mengikut jalur, susunan lapis dan gerak kamera Ken Burns yang halus; topeng teks berada di ruang kosong gambar atau pada panel berasingan. Selit penanda lokasi/tarikh hanya apabila relevan. Variasikan pemindahan fokus antarfoto melalui potongan terus dan gerak dalaman kad.

### MP25 · Batik fashion

**Arah:** 2.5D fesyen batik. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#batik-fashion).

Pisahkan model/pakaian sebenar daripada latar, kekalkan corak kain dan bentuk baju. Buat turntable lembut atau camera arc pada look hero, sementara motif batik bergerak keluar dari kain menjadi bingkai animasi. Kad warna, butiran fabrik dan harga muncul satu demi satu dengan garis penghubung. Sambungkan look dengan padanan motif yang melintas skrin dalam scene, tetapi gunakan potongan terus antara scene jika diminta tanpa transition.

### MP26 · Merdeka · tersembunyi dalam galeri, tersedia melalui pautan terus

**Arah:** 2.5D Merdeka. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#merdeka).

Lapiskan siluet bandar Malaysia, langit senja, Jalur Gemilang dan bunga api. Bendera berkibar dengan proporsi dan susunan jalur/bintang yang tepat; kamera bergerak dari rakyat atau bangunan ke ruang langit untuk tajuk besar. Kembang bunga api jauh di belakang teks, selit garis sejarah atau nilai satu per beat. Utamakan semakan simbol kebangsaan dan keterbacaan ucapan daripada efek berlebihan.

### MP27 · Product turntable

**Arah:** 3D produk studio. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#product-turntable).

Letakkan model produk sebenar atau foto cutout berkualiti pada pedestal studio; bahan label mesti kekal tepat. Kamera orbit sederhana, lampu jalur menyapu permukaan, titisan/partikel hanya jika sesuai. Pada setiap beat, satu callout menunjuk ciri fizikal dengan garis yang melekat pada titik produk; harga dan CTA menjadi kad hero pada akhir. Jika hanya gambar 2D, gunakan multi-plane dan putaran terhad tanpa mendakwa produk telah dimodelkan 3D.

### MP28 · Glitch

**Arah:** Tipografi glitch terkawal. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#glitch).

Gunakan gangguan RGB split dan slice selama beberapa frame pada saat kemasukan kata kunci, diikuti teks stabil yang jelas dibaca. Kad terminal menaip konteks; garis scan dan grid tipis bergerak di belakang. Bentuk hierarki: satu kata besar, satu baris sokongan, satu CTA. Jangan jalankan glitch berterusan, memecah angka atau mengubah ejaan fakta penting. Potong terus ke scene seterusnya selepas hold.

### MP29 · Kampung sunset · tersembunyi dalam galeri, tersedia melalui pautan terus

**Arah:** 2.5D senja kampung. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#kampung-sunset).

Bangunkan rumah kampung, pokok kelapa, sawah dan bukit dalam 5 atau lebih lapisan jarak. Matahari turun, awan beralih perlahan, lampu rumah menyala, kelip-kelip muncul selepas senja. Kamera truck perlahan mengikuti satu elemen cerita seperti basikal atau figura; narasi didukung oleh aksi persekitaran. Tajuk muncul dalam ruang langit yang kontras tanpa menutup subjek; emosi disampaikan oleh perubahan cahaya.

### MP30 · Chat story

**Arah:** 2D UI perbualan. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#chat-story).

Skrin telefon menunjukkan bubble perbualan yang muncul mengikut masa narasi, typing dots hidup dan voice note memaparkan waveform tepat pada durasi audio. Bubble aktif besar dan jelas, sejarah perbualan bergerak ke atas tanpa bertindih dengan zon caption. Reaksi emoji atau lampiran bergerak keluar dari telefon hanya pada beat penting. Tutup dengan mesej penyelesaian atau CTA yang dipin dan ditahan cukup lama untuk dibaca.

### MP31 · Sale countdown

**Arah:** 2.5D promosi hitung mundur. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#sale-countdown).

Bina angka 3, 2, 1 sebagai objek tipografi besar yang bertukar melalui snap, split dan scale; setiap angka mempunyai aksen gerak berbeza. Tag harga berayun masuk, harga lama keluar, harga baharu settle dan confetti muncul sesudah maklumat difahami. Arahkan semua pergerakan ke satu CTA, bukan ke banyak label kecil. Semak harga dan tarikh tawaran tepat; beri hold yang jelas pada tawaran akhir.

### MP32 · Watercolour ink

**Arah:** 2D cat air dan dakwat. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#watercolour-ink).

Animasi resapan cat pada tekstur kertas menggunakan matte organik yang berkembang, bukan crossfade biasa. Dahan plum atau motif topik dilukis stroke demi stroke, kemudian warna mengisi secara bertompok lembut. Tajuk berus terdedah mengikut gerakan berus sementara maklumat sokongan muncul secara bersih pada bidang kertas yang tidak sibuk. Titik dakwat dan grain bergerak minimum untuk memberi tekstur hidup.

### MP33 · Pasar malam · tersembunyi dalam galeri, tersedia melalui pautan terus

**Arah:** 2.5D pasar malam. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#pasar-malam).

Bina lorong gerai dalam lapisan perspektif: kanopi, lampu, asap sate, orang lalu dan papan harga. Lampu menyala berturutan sewaktu kamera masuk; produk makanan hero muncul daripada gerai dengan wap beranimasi. Kad harga besar berayun ringan dan ikon bahan muncul di sekeliling makanan. Kekalkan suasana Malaysia yang khusus, sambil memberi ruang bersih untuk nama hidangan dan tawaran.

### MP34 · Whiteboard sketch

**Arah:** 2D papan putih pedagogi. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#whiteboard-sketch).

Mulakan dengan persoalan atau objektif, kemudian tangan/pen melukis ikon, anak panah, rajah dan langkah mengikut urutan penerangan. Setiap garisan mempunyai masa tulis yang nyata, tetapi potong masa menulis yang tidak penting. Apabila seksyen selesai, kecilkan kelompok lukisan lama sebagai konteks dan fokuskan yang baharu. Gunakan warna pen untuk hierarki, bukan teks panjang atau handwrite yang sukar dibaca di telefon.

### MP35 · Y2K chrome

**Arah:** 3D chrome Y2K. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#y2k-chrome).

Gunakan blob chrome bermorf dengan pantulan studio yang bergerak, sticker holografik pada kedalaman lain dan grid kilat halus. Tajuk Y2K bersinar masuk melalui extrusion pendek atau reveal reflektif; kamera orbit kecil mengubah highlight tanpa memusingkan teks. Letakkan mesej sebenar pada permukaan rata berkontras; elemen chrome mengelilinginya. Jika render 3D tidak tersedia, hasilkan aset chrome dahulu lalu komposisikan gerak 2.5D.

### MP36 · Chinese heritage

**Arah:** 2.5D warisan Tahun Baharu Cina. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#chinese-new-year).

Bangunkan potongan kertas merah, tanglung, jalur emas dan produk sebagai beberapa lapisan. Motif potong terbuka secara simetri; tanglung turun dan berayun; cop merah muncul selepas tajuk atau tawaran. Produk berada di tengah dengan cahaya dan bayang kontak, sementara corak bergerak di pinggir. Gunakan ungkapan sambutan dan simbol budaya yang tepat; beri ruang besar untuk teks dalam bahasa yang diminta.

### MP37 · Property tour

**Arah:** 3D pelan hartanah. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#property-tour).

Bina pelan lantai mengikut ukuran dan susun atur sebenar. Dinding naik dari pelan, bilik menyala mengikut perjalanan kamera, label keluasan terikat pada bilik lalu perspektif bergerak ke ruang hero. Harga dan lokasi akhir muncul sebagai kad besar. Jika tiada model 3D, gunakan SVG pelan berlapis yang diextrude secara 2.5D. Jangan reka bilik, dimensi atau ciri yang tidak disahkan.

### MP38 · Particle field

**Arah:** Medan partikel sinematik. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#particle-field).

Alirkan titik cahaya melalui medan vektor dengan beberapa aras kedalaman, saiz dan kelajuan; kelompok boleh membentuk garis, ikon atau tajuk untuk beberapa saat sebelum berurai. Kamera push halus dan volumetric glow memberi ruang visual tanpa flicker. Gunakan kawasan pusat yang lebih tenang untuk narasi/caption. Partikel bertindak sebagai mekanisme reveal atau suasana latar, bukan pengganti isi cerita.

### MP39 · Nostalgia 90s

**Arah:** 2.5D TV 90-an. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#nostalgia-90s).

Bina televisyen CRT dengan casing, refleksi kaca dan skrin sebagai lapisan berasingan. Suis ditekan, garis skan muncul, color bars bergerak singkat dan footage sebenar pengguna dimainkan di dalam skrin dengan nisbah selamat. Tajuk VHS bertipe besar, date stamp hanya jika diberi, dan noise pita seketika. Kamera mendekati skrin untuk poin utama, kemudian keluar ke set nostalgia; jangan rosakkan keterbacaan footage.

### MP40 · Podcast audiogram

**Arah:** 2D audiogram podcast. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#podcast-audiogram).

Letakkan wajah/cover dan klip audio sebenar dalam kad utama; waveform bar bergerak berdasarkan amplitud atau cue audio, bukan gelung rawak. Karaoke highlight mengikuti perkataan yang disebut, sambil teks kekal di tempat supaya mudah dibaca. Reaksi visual kecil muncul pada penekanan suara, kemudian quote utama menjadi tipografi besar. Letak caption pada zon tengah dan alih avatar/waveform agar tidak bertindih.

### MP41 · Borneo rainforest

**Arah:** 2.5D hutan Borneo. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#borneo-rainforest).

Susun kanopi, batang, akar banir, paku pakis, kabus dan sinar sebagai lapisan jarak. Kamera meluncur antara lapisan; enggang bergerak dengan kepakan yang perlahan, bunga berkembang mengikut masa dan kabus mendedahkan tajuk. Gunakan imej/spesies yang tepat dan unsur alam yang relevan dengan mesej. Gerak tenang tetapi adegan tidak beku kerana daun, cahaya dan kabus aktif berterusan.

### MP42 · Paper cut-out

**Arah:** 2.5D paper cut-out. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#paper-cutout).

Bina setiap bukit, matahari, awan, prop dan karakter sebagai potongan kertas dengan grain dan bayang yang menunjukkan ketinggian lapisan. Setiap kepingan meluncur, berpusing sedikit dan mendarat dengan wobble stop motion; tajuk pada label kertas jatuh lalu dilekatkan pita. Alih kamera beberapa darjah untuk menonjolkan kedalaman. Gerak karakter dan props semasa narasi, bukan sekadar pembukaan set.

### MP43 · Pixel art

**Arah:** Pixel motion graphic. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#pixel-art).

Paparkan tawaran sebagai permainan pixel asli: kad Player 1, peta side scroll, tiga blok ciri, inventory dan ganjaran CTA. Animasi dalam resolusi asas rendah, di-scale tanpa blur; avatar meloncat ke blok, ikon ciri keluar lalu terbang ke slot, counter meningkat hanya dengan nilai diberi. Teks pixel kekal ringkas dan besar. Setiap aksi permainan menunjukkan manfaat produk, bukan hanya efek retro.

### MP44 · Deepavali · tersembunyi dalam galeri, tersedia melalui pautan terus

**Arah:** 2D Deepavali bercorak. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#deepavali).

Kolam dibina daripada titik, garis putih dan gelang warna secara berurutan. Diyas menyala satu demi satu dengan api lembut; garland marigold turun dan berayun di atas. Tajuk emas muncul selepas kolam lengkap, manakala cahaya bergerak perlahan di belakang tulisan. Kekalkan gerak lembut tanpa strobe dan gunakan simbol yang tepat untuk sambutan yang dimaksudkan. Teks berada pada bidang gelap yang lapang.

### MP45 · Vintage archive

**Arah:** 2.5D arkib dokumentari. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#vintage-archive).

Letakkan foto pengguna berbingkai di atas kertas bertekstur; setiap foto jatuh, condong sedikit dan bergerak Ken Burns sambil cap tahun melekat pada timeline dakwat. Caption ditaip ringkas mengikut tarikh; kamera bergerak mengikut urutan peristiwa. Grain, flicker dan light leak sangat ringan supaya wajah serta teks tidak rosak. Gunakan hanya tarikh/fakta sebenar; jika tiada, nyatakan ruang pengganti.

### MP46 · Swiss geometric

**Arah:** 2D Swiss graphic system. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#swiss-geometric).

Kunci komposisi pada grid tipografi dan bentuk geometri rata. Bentuk bergerak hanya di sepanjang sel grid, berputar suku pusingan dan snap tepat; baris servis didedah oleh mask satu demi satu tanpa wobble. Semasa item aktif, satu bentuk berpindah untuk menunjuk item itu; item lama mengecil atau redup. Akhir sekali bina kad fakta/CTA besar melalui susun semula blok sedia ada. Tiada gradien atau hiasan kecil.

### MP47 · Floating 3D icons

**Arah:** 3D ikon / 2.5D komposit. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#floating-3d-icons).

Paparkan monitor/telefon sebagai objek pusat, kemudian 3–5 ikon 3D berlainan kedalaman keluar dari skrin melalui lintasan melengkung dan settle mengelilingi produk. Setiap ikon mewakili fungsi sebenar; satu ikon aktif membesar pada beat narasi sementara yang lain terus bob perlahan. Tajuk besar muncul per perkataan di ruang bersih. Gunakan geometri 3D jika boleh; alternatif ialah cutout ikonik dengan bayang dan parallax 2.5D.

### MP48 · Neon tech

**Arah:** 2.5D HUD teknologi. **Sumber:** [lihat gaya asal](https://epool86.github.io/motionprompt/#neon-tech).

Lapiskan cincin HUD, grid, jejak litar, peranti isometrik, panel hologram dan teks. Cincin spin-up lalu bergerak perlahan; laptop terbuka, panel naik dari skrin, node disambung dan pulse mengikuti garis ke bukti produk. Tajuk decode singkat sebelum settle; kata utama slam besar dengan glow terkawal. Panel tidak menutup caption tengah. Potong terus keluar daripada scene setelah CTA jelas, tanpa glitch transition yang menyakitkan mata.

## Contoh gabungan yang terkawal

**Promo Slide AI, 9:16, 60 saat:** MP04 untuk galeri slide asal dan kamera antara mockup; MP09 untuk demonstrasi UI telefon; MP07 untuk hook 1–3 perkataan dan CTA; MP17 bagi satu angka yang mempunyai bukti. Pilih satu gaya asas per scene. Caption tengah, slaid melalui contain, potongan terus antara scene, serta VO Melayu Malaysia yang diselaraskan dengan beat gerak.

**Explainer psikologi, 16:9:** MP34 untuk membina konsep di papan putih; MP02 untuk proses dan MP17 untuk data yang ada sumber; MP42 bagi analogi paper cut-out. Teks penting sekurang-kurangnya cukup besar untuk dibaca pada output sebenar.

**Produk 3D dan fotorealistik:** MP27 bagi produk utama dengan label tepat, MP47 untuk ciri sebagai ikon 3D, MP09 bagi skrin produk. Biarkan produk fotorealistik dan ikon/grafik sebagai lapisan penerangan; uji bayang, perspektif dan depth supaya integrasinya meyakinkan. 3D sebenar bergantung pada model, tekstur, lampu dan renderer yang tersedia.

## Pemeriksaan akhir

- Bahan rujukan penuh kelihatan, tiada crop yang merosakkan wajah/teks/logo.
- Pada setiap beat ada satu hero, tindakan yang boleh diterangkan, dan tempoh hold boleh dibaca.
- Animasi teks tidak berulang dengan mekanisme yang sama untuk seluruh video.
- Ruang caption tengah bebas sepanjang lintasan gerak elemen lain.
- Tiada header kecil, angka rekaan, simbol budaya tersalah, glitch berpanjangan atau slide statik berkamera zoom berulang.
- Nisbah 9:16 dibina semula, bukan dipotong daripada komposisi 16:9.
