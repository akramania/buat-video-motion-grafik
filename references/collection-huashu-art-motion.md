# Koleksi Huashu Art Motion: seni hidup dan tatabahasa explainer

Gunakan koleksi ini apabila pengguna memilih Huashu, Art Motion, gaya HA atau tatabahasa HG. Pilih satu bahasa visual utama mengikut kandungan, kemudian bina objek dan gerak sebenar. HA/HG ialah label pemilihan resipi, bukan ID preset renderer atau penambahan kepada Atlas 922.

## Kandungan

1. Sumber dan kiraan
2. Aturan penggunaan
3. Seni sedia dilaksanakan di sumber (HA01–HA34)
4. Kajian gaya sumber (HA35–HA50)
5. Tatabahasa explainer (HG01–HG09)

## 1. Sumber dan kiraan

Semakan: 7 November 2026. Inventori terperinci disahkan melalui [INDEX sumber pada revisi 8a0d7d7](https://github.com/alchaincyf/huashu-art-motion/blob/8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c/references/%E9%A3%8E%E6%A0%BC%E9%85%8D%E6%96%B9/INDEX.md) dan [tatabahasa09](https://github.com/alchaincyf/huashu-art-motion/blob/8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c/references/09-%E8%A7%86%E9%A2%91%E5%8A%A8%E7%94%BB%E8%AF%AD%E6%B3%95.md). Badan SKILL.md semasa menyatakan 36 gaya sedia dilaksanakan + 17 kad kajian; tajuk/header lama masih menyebut 16 kajian atau 35 gaya. Gunakan baris inventori, bukan teks pemasaran lama.

| Kategori | Sumber | Dimasukkan di sini |
|---|---:|---:|
| Gaya seni sedia dilaksanakan di sumber |36|34|
| Kad kajian seni sumber |17|16|
| Tatabahasa explainer |9|9|
| Jumlah resipi yang boleh dipilih di sini |62|59|

Dalam 9 tatabahasa, 8 mempunyai demo/klip berparameter di sumber; yang kesembilan ialah snapshot penerangan berpenyampai yang memerlukan aset watak/audio sendiri. Jumlah 35 merujuk galeri Canvas lama; satu gaya outline SVG berasingan menjadikannya 36 gaya sedia dilaksanakan. Ketiga-tiga kad mural 02_egypt, 20_dunhuang dan 55_dunhuang tidak dimasukkan kerana motif agama bukan Islam.

Semua 59 entri ialah panduan yang diperluas daripada gaya asli yang disahkan. Tiada gaya tambahan direka lalu didakwa sebagai entri sumber. Tiada repo dipasang, skrip upstream dijalankan atau render baharu diuji dalam kemas kini ini. Status “implemented” pada HA01–HA34 ialah status sumber, bukan jaminan runtime setempat atau mutu padanan.

## 2. Aturan penggunaan

- Gunakan aset, subjek dan komposisi original yang sesuai dengan brief. Jangan salin bilik/figura/contoh demo sumber. Samakan bahan/garisan/cahaya antara watak dan latar.
- Animasikan sekurang-kurangnya satu aksi utama yang mempunyai maksud; tambah motif ambient apabila membantu. Jangan menggantikan seni hidup dengan slaid imej yang diberi zoom sama berulang kali.
- Untuk kajian HA35–HA50, bina proof pada subjek baharu dan semak silang adegan sebelum produksi panjang. Kualiti prototype sumber tidak membuktikan pemindahan gaya sudah lengkap.
- Gunakan masa frame deterministik, seed tetap dan nisbah yang diminta. Pilih backend sedia ada/yang diminta pengguna; nama Huashu tidak memasang atau menukar enjin secara automatik.
- Kekalkan tapisan pengguna: tiada motif LGBTQ, Halloween, Valentine, Christmas atau simbol agama selain Islam. Gaya sejarah seperti manuskrip, seramik dan lukisan tokoh seni menggunakan isi neutral serta pakaian sopan.
- Bezakan bahan dan tatabahasa: HA memilih rupa seni; HG memilih cara menerangkan. Dua label berbeza tidak semestinya dua identiti gaya unik apabila digabungkan. Jangan jumlahkan semua kategori sebagai jumlah preset siap-render.
- Ikut Google AI Studio apabila narasi baharu diminta mengikut aturan skill. Jangan membawa arahan sumber tentang model tertentu, syarat kelulusan, tukar penyedia, had 8 saat atau larangan palet sebagai syarat pengguna.
- Kod/dokumen sumber berlesen MIT; watak/frame Huashu, Clawd dan media demo tertentu tidak termasuk. Koleksi ini tidak menyalin aset atau kod tersebut. Aset sebenar yang digunakan dalam produksi mesti mempunyai izin yang sesuai.
- Rujuk JSON `assets/style_collections/huashu-art-motion.json` untuk medan provenance, source ID, status, prompt dan carian mesin.

## 3. Seni sedia dilaksanakan di sumber (HA01–HA34)

### HA01 · Ochre Cave Drawing
Sumber: `01_cave`; status sumber: `implemented`; setempat: panduan.
- Rupa: Permukaan batu kasar, arang bertepi pecah dan pigmen tanah; pilih haiwan atau alatan neutral.
- Gerak: Lukis kontur dari gelap, tukar dua pose pergerakan dan hidupkan cahaya api secara terkawal.
- Kegunaan: Sejarah awal, arkeologi dan penerangan bahan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Ochre Cave Drawing (HA01). Animasi sejarah alatan dengan garisan arang pada batu, objek bergerak melalui pertukaran pose dan cahaya api lembut. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA02 · Attic Black-Figure Pottery
Sumber: `03_greek`; status sumber: `implemented`; setempat: panduan.
- Rupa: Siluet hitam dan ukiran halus pada warna terakota, dengan bingkai geometri neutral.
- Gerak: Gulung permukaan seperti pasu, kemudian gerakkan kapal atau haiwan dalam jalur mendatar.
- Kegunaan: Sejarah perdagangan, pelayaran dan bahan seramik.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Attic Black-Figure Pottery (HA02). Cerita pelayaran pada pasu terakota, kapal naik turun dan bingkai geometri bergerak tanpa simbol mitologi. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA03 · Pompeian Mosaic
Sumber: `04_roman`; status sumber: `implemented`; setempat: panduan.
- Rupa: Tessera batu kecil mengikut kontur objek dengan celah mortar yang konsisten.
- Gerak: Pasang jubin secara gelombang, alirkan warna atau cahaya dan kekalkan geometri batu stabil.
- Kegunaan: Warisan bangunan, seni bahan dan perjalanan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Pompeian Mosaic (HA03). Bina peta perjalanan daripada jubin mozek, susun mengikut kontur dan hidupkan pantulan cahaya di atasnya. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA04 · Gilded Botanical Manuscript
Sumber: `05_gothic`; status sumber: `implemented`; setempat: panduan.
- Rupa: Halaman bertekstur dengan emas timbul, bingkai tumbuhan dan ruang teks terukur; gunakan isi sekular neutral.
- Gerak: Tulis huruf atau ilustrasi berperingkat, sapu kilauan emas dan lipat halaman sebagai peralihan.
- Kegunaan: Pembukaan buku, koleksi botani dan naratif ilmu.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Gilded Botanical Manuscript (HA04). Buka manuskrip botani emas dengan ilustrasi tumbuhan yang terbina perlahan dan kilauan menyapu margin. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA05 · Renaissance Sfumato
Sumber: `06_renaissance`; status sumber: `implemented`; setempat: panduan.
- Rupa: Peralihan tona lembut, lapisan warna hangat dan kedalaman atmosfera; subjek berpakaian sopan.
- Gerak: Gerakkan cahaya dan udara halus sambil satu objek menjalankan aksi jelas, kemudian dedahkan pandangan lebih luas.
- Kegunaan: Sejarah sains, alat mekanik dan cerita reflektif.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Renaissance Sfumato (HA05). Terangkan alat terbang awal dengan sfumato hangat, sayap mekanik bergerak dan cahaya jendela berubah perlahan. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA06 · Impressionist Light Strokes
Sumber: `08_impressionism`; status sumber: `implemented`; setempat: panduan.
- Rupa: Tompok warna pendek yang membina cahaya dan ruang tanpa garis keras berlebihan.
- Gerak: Tetapkan kedudukan sapuan, animasikan daun, awan dan pantulan; elakkan tekstur rawak berkelip setiap frame.
- Kegunaan: Alam, suasana petang dan perjalanan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Impressionist Light Strokes (HA06). Hasilkan taman bercahaya dengan sapuan pendek yang stabil, daun berayun dan pantulan air bergerak. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA07 · Post-Impressionist Flow Fields
Sumber: `09_postimp`; status sumber: `implemented`; setempat: panduan.
- Rupa: Sapuan tebal berarah, warna bertenaga dan kontur yang menyatukan komposisi.
- Gerak: Gerakkan medan sapuan mengikut objek, pusarkan langit dan kekalkan bentuk utama terbaca.
- Kegunaan: Naratif emosi, alam dan visual muzik.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Post-Impressionist Flow Fields (HA07). Bina landskap malam dengan sapuan berarah yang mengalir, cahaya berdenyut lembut dan pokok berayun. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA08 · Art Nouveau Organic Lines
Sumber: `10_nouveau`; status sumber: `implemented`; setempat: panduan.
- Rupa: Kontur organik dengan lebar berbeza, bentuk tumbuhan dan hiasan melengkung yang menyokong subjek.
- Gerak: Tumbuhkan garis menjadi bingkai, gerakkan daun dan bawa aksen melengkung kepada objek seterusnya.
- Kegunaan: Produk artisan, taman dan pembukaan budaya.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Art Nouveau Organic Lines (HA08). Perkenalkan produk artisan dengan bingkai tumbuhan yang tumbuh melalui garisan organik dan daun berayun. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA09 · Analytical Cubist Planes
Sumber: `11_cubism`; status sumber: `implemented`; setempat: panduan.
- Rupa: Objek dipecahkan kepada satah telus dan sudut pandang berbilang, dengan tona bumi terkawal.
- Gerak: Gelongsorkan satah untuk membina satu objek, kemudian gabungkan semula sebelum bertukar fokus.
- Kegunaan: Persepsi, sudut pandang dan struktur objek.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Analytical Cubist Planes (HA09). Terangkan sebuah kamera melalui satah kubis yang tersusun, bergerak berasingan lalu membentuk objek yang lengkap. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA10 · Bauhaus Geometric Stage
Sumber: `12_bauhaus`; status sumber: `implemented`; setempat: panduan.
- Rupa: Bulatan, grid, batang dan blok warna berfungsi sebagai struktur komposisi.
- Gerak: Putar mekanisme, susun grid dan hubungkan bentuk melalui sentuhan yang jelas.
- Kegunaan: Reka bentuk, mekanik asas dan identiti produk.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Bauhaus Geometric Stage (HA10). Bina pentas geometri untuk menerangkan mekanisme jam, dengan bulatan berputar dan grid menyusun secara berperingkat. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA11 · Halftone Pop Panels
Sumber: `13_pop`; status sumber: `implemented`; setempat: panduan.
- Rupa: Titik halftone, warna terhad, kontur hitam dan panel grafik dengan hierarki kuat.
- Gerak: Cetak panel secara berturutan, munculkan kata penekanan dan gunakan perubahan skala bagi reaksi.
- Kegunaan: Promosi, fakta ringkas dan perbandingan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Halftone Pop Panels (HA11). Bentangkan tiga manfaat produk dalam panel pop halftone dengan kata besar, aksi produk dan pertukaran fokus yang jelas. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA12 · 8-Bit Pixel World
Sumber: `14_8bit`; status sumber: `implemented`; setempat: panduan.
- Rupa: Siluet piksel terbaca pada resolusi reka bentuk rendah, palet terhad dan skala nearest-neighbour.
- Gerak: Gunakan pose piksel, langkah konsisten dan dunia tatal; elakkan interpolasi yang mencairkan piksel.
- Kegunaan: Permainan pendidikan, cabaran dan perjalanan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu 8-Bit Pixel World (HA12). Hasilkan dunia piksel untuk perjalanan belajar, watak original berjalan dan objek misi muncul mengikut laluan. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA13 · Early CGI Chrome Stage
Sumber: `15_raytrace`; status sumber: `implemented`; setempat: panduan.
- Rupa: Permukaan plastik, chrome dan lantai pantulan dengan bentuk geometri yang jelas.
- Gerak: Putar objek, dedahkan wireframe kepada permukaan dan gerakkan cahaya pantulan mengikut bentuk.
- Kegunaan: Sejarah komputer, teknologi retro dan intro objek.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Early CGI Chrome Stage (HA13). Perkenalkan objek teknologi pada pentas CGI retro, wireframe menjadi permukaan chrome dan cahaya menyapu bentuk. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA14 · Contemporary Grainy Flat Illustration
Sumber: `16_2026`; status sumber: `implemented`; setempat: panduan.
- Rupa: Blok warna tanpa kontur berat, tekstur berbutir dan siluet moden yang bersih.
- Gerak: Bina prop satu persatu, gunakan pose berartikulasi dan secondary motion selepas sentuhan.
- Kegunaan: Pendidikan umum, komuniti dan promosi ringan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Contemporary Grainy Flat Illustration (HA14). Terangkan rutin harian dengan ilustrasi flat berbutir, prop dibina mengikut aksi dan pose watak original yang jelas. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA15 · Expressive Ink Wash
Sumber: `17_ink`; status sumber: `implemented`; setempat: panduan.
- Rupa: Ruang kosong bermakna, hitam berlapis, tepi sapuan kering dan aliran dakwat.
- Gerak: Lukis objek melalui sapuan, kembangkan wash dan gerakkan satu motif seperti daun atau air.
- Kegunaan: Puisi, alam dan penerangan reflektif.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Expressive Ink Wash (HA15). Bina landskap dakwat dengan sapuan yang terhasil di skrin, air mengalir dan satu daun bergerak merentasi ruang kosong. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA16 · Ornamental Gold Patterns
Sumber: `18_klimt`; status sumber: `implemented`; setempat: panduan.
- Rupa: Bidang emas rata, corak geometri berulang dan subjek sopan yang mempunyai pemisahan tona.
- Gerak: Bentangkan corak mengikut siluet, sapu kilauan setempat dan alirkan serpihan emas sebagai jambatan.
- Kegunaan: Produk mewah, tekstil dan motif hiasan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Ornamental Gold Patterns (HA16). Perkenalkan tekstil dengan bidang emas bercorak geometri yang terbina mengikut lipatan dan kilauan setempat. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA17 · Expressionist Wave Space
Sumber: `19_munch`; status sumber: `implemented`; setempat: panduan.
- Rupa: Garis melengkung panjang, warna emosi dan ruang yang sengaja tidak stabil.
- Gerak: Herotkan latar secara halus mengikut lengkung besar, sambil subjek utama mempunyai aksi yang terbaca.
- Kegunaan: Perasaan, tekanan dan cerita psikologi.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Expressionist Wave Space (HA17). Visualkan keresahan dengan ruang bergelombang dan warna beremosi, tetapi kekalkan subjek original jelas dan sopan. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA18 · Rhythmic Dot Fields
Sumber: `21_kusama`; status sumber: `implemented`; setempat: panduan.
- Rupa: Titik tidak seragam, pola berulang dan skala motif yang memisahkan foreground daripada latar.
- Gerak: Sebarkan gelombang titik, ubah kepadatan secara bertahap dan gunakan pola untuk membuka ruang berikutnya.
- Kegunaan: Corak, perhatian, kreativiti dan produk.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Rhythmic Dot Fields (HA18). Hasilkan medan titik yang berkembang dalam gelombang untuk mendedahkan objek utama, dengan kepadatan terkawal. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA19 · Constructivist Photo Geometry
Sumber: `22_constructivism`; status sumber: `implemented`; setempat: panduan.
- Rupa: Kolaj foto berhalftone, bentuk pepenjuru dan tipografi sebagai struktur arah; gunakan kandungan neutral.
- Gerak: Cap frasa, seret bentuk sebagai penunjuk dan susun bahan bukti pada paksi yang konsisten.
- Kegunaan: Sejarah reka bentuk, kempen maklumat dan editorial.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Constructivist Photo Geometry (HA19). Susun bahan kempen neutral dalam kolaj geometri pepenjuru, foto halftone dan tipografi yang membina laluan bacaan. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA20 · Surreal Elastic Objects
Sumber: `23_dali`; status sumber: `implemented`; setempat: panduan.
- Rupa: Objek harian berubah bahan atau perkadaran dalam ruang berbayang panjang.
- Gerak: Lenturkan objek secara berterusan, panjangkan bayang dan gunakan transformasi bermakna untuk pertukaran idea.
- Kegunaan: Metafora masa, kebiasaan dan imaginasi.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Surreal Elastic Objects (HA20). Jadikan jam dan alat tulis sebagai metafora masa melalui perubahan bentuk lembut dan bayang yang bergerak. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA21 · Hard-Edge Quiet Light
Sumber: `24_hopper`; status sumber: `implemented`; setempat: panduan.
- Rupa: Blok cahaya keras, ruang bandar tenang dan warna yang memisahkan objek dengan jelas.
- Gerak: Alihkan tompok cahaya, gerakkan bayang atau satu aksi harian; kamera hanya berubah ketika fokus perlu dipandu.
- Kegunaan: Cerita harian, ruang kerja dan rasa sunyi.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Hard-Edge Quiet Light (HA21). Ceritakan satu petang di ruang kerja dengan cahaya keras menyapu meja dan aksi harian yang jelas. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA22 · Watercolour Background and Cel Shade
Sumber: `25_ghibli`; status sumber: `implemented`; setempat: panduan.
- Rupa: Latar wash cat air dengan watak original bercel-shading; tetapkan rujukan filem khusus sebelum menilai rupa.
- Gerak: Gerakkan rumput berkelompok, awan dan kain; selaraskan tekstur serta warna watak dengan dunia.
- Kegunaan: Cerita keluarga, alam dan pengembaraan lembut.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Watercolour Background and Cel Shade (HA22). Bina cerita keluarga dalam latar cat air, dengan rumput berayun dan watak original yang konsisten dengan palet. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA23 · Vaporwave Retro Signals
Sumber: `26_vaporwave`; status sumber: `implemented`; setempat: panduan.
- Rupa: Grid perspektif, jalur matahari dan tekstur isyarat retro; pilih aksen warna mengikut brief.
- Gerak: Tatal grid, gerakkan jalur dan gunakan gangguan isyarat pendek pada pertukaran fokus sahaja.
- Kegunaan: Sejarah media, nostalgia digital dan intro teknologi.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Vaporwave Retro Signals (HA23). Hasilkan intro teknologi retro dengan grid perspektif bergerak dan gangguan isyarat terkawal, tanpa simbol agama. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA24 · Dynamic Cosmic Comic Panels
Sumber: `27_kirby`; status sumber: `implemented`; setempat: panduan.
- Rupa: Foreshortening yang kuat, blok bayang, titik tenaga dan panel komik; bina watak serta produk original.
- Gerak: Tukar skala ekstrem secara terarah, lukis tenaga dan bawa panel kepada aksi sebab-akibat.
- Kegunaan: Aksi pendidikan, penerangan teknologi dan promosi.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Dynamic Cosmic Comic Panels (HA24). Terangkan tenaga elektrik melalui panel komik original dengan perspektif dinamik dan titik tenaga yang dibina berperingkat. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA25 · Water Garden Reflections
Sumber: `28_monet`; status sumber: `implemented`; setempat: panduan.
- Rupa: Permukaan air daripada sapuan pendek, warna pantulan bercampur dan bentuk taman lembut.
- Gerak: Kembangkan riak, gerakkan pantulan dan biarkan tumbuhan mengikut angin yang sama.
- Kegunaan: Alam, ketenangan dan kisah perjalanan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Water Garden Reflections (HA25). Animasikan taman air dengan riak berkembang, bayang daun dan pantulan yang berubah mengikut gerakan. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA26 · Pointillist Optical Mixing
Sumber: `29_seurat`; status sumber: `implemented`; setempat: panduan.
- Rupa: Bentuk daripada titik warna bersebelahan yang mencipta campuran optik, bukan tekstur grid rata.
- Gerak: Bina bentuk melalui taburan titik tetap, kemudian alirkan cahaya perlahan sambil siluet kekal stabil.
- Kegunaan: Persepsi warna, seni dan visual pendidikan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Pointillist Optical Mixing (HA26). Terangkan campuran warna melalui titik pointillist yang membina objek dan perubahan cahaya yang stabil. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA27 · Cut-Paper Organic Forms
Sumber: `30_matisse`; status sumber: `implemented`; setempat: panduan.
- Rupa: Siluet kertas bertepi tidak sempurna, bidang warna rata dan bayang lapisan yang nipis.
- Gerak: Gunting/reveal bentuk, susun lapisan dan gerakkan daun atau bentuk organik pada pivot yang betul.
- Kegunaan: Pendidikan awal, tumbuhan dan promosi ceria.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Cut-Paper Organic Forms (HA27). Bina taman daripada potongan kertas organik yang muncul satu persatu dan bergerak seperti ditiup angin. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA28 · Bold Outline Motion Figures
Sumber: `31_haring`; status sumber: `implemented`; setempat: panduan.
- Rupa: Garis hitam tebal dan seragam, bentuk simbolik ringkas serta garis aksi yang jelas.
- Gerak: Gunakan pose tegas, langkah berirama dan garis aksi yang muncul pada sentuhan; cipta figura baharu.
- Kegunaan: Aktiviti fizikal, komuniti dan komunikasi ringkas.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Bold Outline Motion Figures (HA28). Hasilkan kempen aktiviti fizikal dengan figura original bergaris tebal dan pose berirama yang mudah difahami. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA29 · Chiaroscuro Window Light
Sumber: `32_rembrandt`; status sumber: `implemented`; setempat: panduan.
- Rupa: Satu sumber cahaya dominan, tona gelap kaya dan bentuk yang diterangkan melalui nilai cahaya.
- Gerak: Gerakkan cahaya/bayang perlahan dan berikan subjek satu aksi konkrit; periksa kedalaman muka serta tangan.
- Kegunaan: Cerita reflektif, artisan dan objek bertekstur.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Chiaroscuro Window Light (HA29). Perkenalkan kerja artisan melalui cahaya jendela tunggal, bayang terkawal dan gerakan tangan yang dapat dilihat. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA30 · Rubber-Hose Vintage Cartoon
Sumber: `33_rubberhose`; status sumber: `implemented`; setempat: panduan.
- Rupa: Bentuk bulat, anggota seperti hos dan ekspresi jelas dengan tekstur filem yang sederhana.
- Gerak: Gunakan squash-and-stretch, laluan lengkung serta pose berirama; bunyi mengikuti sentuhan objek.
- Kegunaan: Komedi ringan, mekanisme mudah dan promo retro.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Rubber-Hose Vintage Cartoon (HA30). Animasikan mesin kopi original dalam kartun rubber-hose, dengan gerak lentur dan hubungan sebab-akibat yang jelas. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA31 · Translucent Shadow-Puppet Stage
Sumber: `34_shadowpuppet`; status sumber: `implemented`; setempat: panduan.
- Rupa: Bahan nipis lut cahaya, potongan hiasan dan sendi berpaksi di hadapan lampu belakang.
- Gerak: Putar anggota mengikut sendi, gerakkan alat kawalan secara tersirat dan jaga kontak kaki dengan pentas.
- Kegunaan: Cerita rakyat neutral, siluet dan demonstrasi gerak.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Translucent Shadow-Puppet Stage (HA31). Ceritakan perjalanan watak original melalui pentas bayang lut cahaya dengan sendi berpaksi dan kontak kaki stabil. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA32 · Luminous Anime Atmosphere
Sumber: `35_shinkai`; status sumber: `implemented`; setempat: panduan.
- Rupa: Awan padat, sinaran atmosfera, pantulan dan bayang cel yang mengekalkan lokasi jelas.
- Gerak: Gerakkan awan, zarah cahaya dan pantulan pada kadar berbeza; kamera menjejak peristiwa utama.
- Kegunaan: Cuaca, perjalanan dan cerita harapan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Luminous Anime Atmosphere (HA32). Bina suasana bandar selepas hujan dengan awan bercahaya, pantulan bergerak dan watak original berpakaian sopan. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA33 · Blue Tonal Figure Study
Sumber: `36_picasso_blue`; status sumber: `implemented`; setempat: panduan.
- Rupa: Palet biru terhad, kontur gelap dan bentuk memanjang; gunakan subjek sopan serta konteks neutral.
- Gerak: Animasikan pemindahan berat, nafas atau satu gestur bermakna sambil tekstur sapuan kekal stabil.
- Kegunaan: Renungan, kesunyian dan emosi naratif.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Blue Tonal Figure Study (HA33). Visualkan renungan seorang pengembara melalui tona biru, satu gestur perlahan dan tekstur sapuan yang stabil. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA34 · Rounded-Outline Flat Cartoon
Sumber: `37_rick_morty`; status sumber: `implemented`; setempat: panduan.
- Rupa: Kontur gelap bulat, warna rata, prop berlapis dan watak original dengan bentuk tersendiri.
- Gerak: Rig pivot untuk mata, kelip, tangan dan prop; uji pose perantaraan dan kontak objek sebelum master.
- Kegunaan: Dialog penerangan, humor neutral dan cerita pendek.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Rounded-Outline Flat Cartoon (HA34). Bina dialog dua watak original dalam kartun outline rata, dengan kelip mata, gestur tangan dan props yang berinteraksi. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

## 4. Kajian gaya sumber (HA35–HA50)

### HA35 · Fresco Narrative Volumes
Sumber: `38_giotto`; status sumber: `study`; setempat: panduan.
- Rupa: Isi padu mudah dibaca, kumpulan figura sopan dan ruang yang mengutamakan hubungan naratif.
- Gerak: Alihkan fokus antara gestur dan objek melalui pendedahan berperingkat, tanpa menyalin adegan keagamaan.
- Kegunaan: Cerita masyarakat, tindakan membantu dan naratif ilmu.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Fresco Narrative Volumes (HA35). Uji cerita masyarakat neutral dengan isi padu fresco dan gestur yang menerangkan hubungan antara watak original. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA36 · Geometric Calm Volumes
Sumber: `39_piero`; status sumber: `study`; setempat: panduan.
- Rupa: Susunan geometri seimbang, cahaya tenang dan objek dengan volume yang jelas.
- Gerak: Gerakkan satu mekanisme atau pertukaran perhatian dalam ruang stabil; biarkan perubahan geometri membawa makna.
- Kegunaan: Reka bentuk ruang, struktur dan penjelasan tertib.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Geometric Calm Volumes (HA36). Uji penerangan struktur dalam komposisi geometri tenang, dengan objek bergerak satu persatu mengikut logik. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA37 · Harmonious Group Composition
Sumber: `40_raphael`; status sumber: `study`; setempat: panduan.
- Rupa: Kumpulan objek/figura tersusun harmoni, garis pandang dan bentuk melengkung yang mengikat ruang.
- Gerak: Susun prop melalui laluan yang menghubungkan watak atau idea; kekalkan gestur sopan serta konteks neutral.
- Kegunaan: Kerjasama, pembelajaran dan hubungan sosial.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Harmonious Group Composition (HA37). Uji komposisi kumpulan belajar yang harmoni dengan garis pandang jelas dan props yang berpindah antara watak original. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA38 · Sculptural Pose Tension
Sumber: `41_michelangelo`; status sumber: `study`; setempat: panduan.
- Rupa: Bentuk berisi dan pose bertentangan yang memberi tenaga; gunakan pakaian sopan dan prop harian.
- Gerak: Bina anticipation, pemindahan berat dan release tenaga, dengan anatomi serta kontak yang disemak.
- Kegunaan: Usaha fizikal, ketabahan dan tindakan berfokus.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Sculptural Pose Tension (HA38). Uji watak original mengangkat objek dengan pose bersifat arca, anticipation dan pemindahan berat yang jelas. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA39 · Loose Atmospheric City Light
Sumber: `42_guardi`; status sumber: `study`; setempat: panduan.
- Rupa: Tepi terputus-putus, pantulan kecil dan ruang bandar yang terasa berudara.
- Gerak: Gerakkan pantulan, orang/laluan jauh dan kabus ringan; kekalkan bangunan utama stabil.
- Kegunaan: Bandar, perjalanan dan perubahan masa.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Loose Atmospheric City Light (HA39). Uji suasana bandar berudara dengan pantulan cahaya pecah dan pergerakan jauh yang membina kehidupan ruang. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA40 · Readable Social Panorama
Sumber: `43_lorenzetti`; status sumber: `study`; setempat: panduan.
- Rupa: Ruang masyarakat berlapis yang boleh dibaca melalui laluan, kumpulan dan kegiatan khusus.
- Gerak: Bina aktiviti mengikut zon, pandu kamera kepada hubungan sebab-akibat dan elakkan semua zon berebut fokus.
- Kegunaan: Komuniti, sistem bandar dan proses kerja.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Readable Social Panorama (HA40). Uji panorama komuniti neutral dengan beberapa aktiviti berhubung, kamera memandu satu hubungan pada satu masa. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA41 · Flowing Baroque Masses
Sumber: `44_cortona`; status sumber: `study`; setempat: panduan.
- Rupa: Kumpulan bentuk dinamik, lengkung besar dan lapisan mendalam; pilih objek serta cerita sekular neutral.
- Gerak: Gunakan laluan gerak berlengkung antara kumpulan, kawal skala dan selesaikan aksi pada satu hero.
- Kegunaan: Pergerakan ramai, transformasi dan naratif dramatik.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Flowing Baroque Masses (HA41). Uji komposisi objek berlapis dengan lengkung dramatik dan pergerakan kumpulan yang membawa mata kepada satu hero. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA42 · Warm-Cool Human Light
Sumber: `45_renoir`; status sumber: `study`; setempat: panduan.
- Rupa: Campuran warna hangat/sejuk, tepi lembut dan cahaya yang memberi rasa mesra.
- Gerak: Gerakkan gestur harian, cahaya celah daun dan sentuhan prop dengan penekanan pada hubungan.
- Kegunaan: Keluarga, taman dan cerita sosial ringan.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Warm-Cool Human Light (HA42). Uji pertemuan keluarga sopan dengan cahaya hangat-sejuk dan gestur harian yang natural. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA43 · Everyday Environmental Rhythm
Sumber: `46_pissarro`; status sumber: `study`; setempat: panduan.
- Rupa: Orang dan objek menjadi sebahagian daripada ruang, sapuan menyatukan kegiatan dengan persekitaran.
- Gerak: Susun aliran berjalan, kenderaan atau kerja berulang pada kadar berbeza, dengan anchor naratif jelas.
- Kegunaan: Pasar, pekerjaan dan sistem komuniti.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Everyday Environmental Rhythm (HA43). Uji suasana pasar dengan aktiviti berlapis, sapuan yang konsisten dan satu watak original sebagai anchor cerita. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA44 · Weather and Landscape Continuity
Sumber: `47_sisley`; status sumber: `study`; setempat: panduan.
- Rupa: Langit, tanah dan air berkongsi cahaya/cuaca yang konsisten dengan sapuan berarah.
- Gerak: Gerakkan angin, awan dan pantulan sebagai satu sistem, kemudian bawa kamera sepanjang ruang.
- Kegunaan: Cuaca, alam dan penerangan perubahan musim.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Weather and Landscape Continuity (HA44). Uji landskap berangin dengan awan, rumput dan pantulan yang bertindak balas kepada arah angin sama. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA45 · Flat Symbolic Colour Fields
Sumber: `48_gauguin`; status sumber: `study`; setempat: panduan.
- Rupa: Bidang warna besar, kontur kuat dan ruang rata; gunakan simbol harian neutral sahaja.
- Gerak: Tukar hubungan bidang melalui mask atau pertindihan; kekalkan aksi utama dalam siluet jelas.
- Kegunaan: Metafora warna, pengalaman dan cerita reflektif.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Flat Symbolic Colour Fields (HA45). Uji cerita harian dengan bidang warna rata dan kontur kuat, tanpa simbol keagamaan atau salinan watak sumber. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA46 · Memory-Space Colour Story
Sumber: `49_chagall`; status sumber: `study`; setempat: panduan.
- Rupa: Ruang kenangan dengan skala bebas dan warna emosi; pilih objek keluarga atau pengalaman neutral.
- Gerak: Biarkan objek ingatan melayang mengikut laluan bermakna, kemudian bersatu dalam satu komposisi.
- Kegunaan: Kenangan, keluarga dan cerita nostalgia.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Memory-Space Colour Story (HA46). Uji naratif kenangan keluarga melalui objek harian yang melayang dan berkumpul dalam ruang warna beremosi. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA47 · Asymmetric Ink Landscape
Sumber: `50_ma_yuan`; status sumber: `study`; setempat: panduan.
- Rupa: Pusat berat di satu sudut, ruang kosong luas dan sapuan yang menjimatkan bentuk.
- Gerak: Dedahkan ranting atau batu melalui sapuan, gerakkan kabus/air dan pandu satu subjek merentas ruang kosong.
- Kegunaan: Puisi, alam dan penerangan ringkas.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Asymmetric Ink Landscape (HA47). Uji landskap dakwat asimetri dengan batu di sudut, kabus bergerak dan satu perahu merentas ruang kosong. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA48 · Layered Miniature Narrative
Sumber: `51_persian_miniature`; status sumber: `study`; setempat: panduan.
- Rupa: Ruang bertingkat, hiasan teliti dan warna terkawal; pilih seni bina/aktiviti neutral dengan pakaian sopan.
- Gerak: Buka lapisan ruang seperti bab, gerakkan kegiatan kecil dan gunakan kamera untuk mengekalkan bacaan.
- Kegunaan: Kebudayaan, taman dan cerita ilmu.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Layered Miniature Narrative (HA48). Uji kisah pengembaraan ilmu dalam ruang miniatur berlapis, dengan kegiatan kecil dan seni bina neutral. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA49 · Limited Digital Paper-Cut Acting
Sumber: `52_south_park`; status sumber: `study`; setempat: panduan.
- Rupa: Figur geometri rata, mata ringkas dan bahan kertas nipis; watak serta latar original.
- Gerak: Tukar pose, mulut dan eyeline secara tepat; langkah perlu kontak, bukan sekadar seluruh tubuh meluncur.
- Kegunaan: Dialog pendidikan, humor neutral dan situasi harian.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Limited Digital Paper-Cut Acting (HA49). Uji perbualan dua pekerja original melalui digital paper-cut dengan pertukaran pose dan kontak kaki yang jelas. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

### HA50 · Expressive 3D Animation Family
Sumber: `53_pixar`; status sumber: `study`; setempat: panduan.
- Rupa: Bentuk, bahan dan ekspresi yang ditentukan untuk satu rujukan filem khusus; bukan satu penapis studio universal.
- Gerak: Bina anticipation, gestur, kontak dan reaksi berurutan; uji aset, rig serta pencahayaan sebelum mendakwa 3D sebenar.
- Kegunaan: Cerita emosi, produk berwatak dan hubungan keluarga.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Expressive 3D Animation Family (HA50). Uji gaya animasi 3D ekspresif untuk cerita keluarga dengan watak original, rig berkontak dan bahan yang konsisten. Sesuaikan durasi dan nisbah kepada brief; render proof dahulu.`

## 5. Tatabahasa explainer (HG01–HG09)

### HG01 · Flat Science Scale Journey
Sumber: `y1_kurzgesagt`; status sumber: `parameterized-demo`; setempat: panduan.
- Rupa: Objek vektor tanpa outline berat dalam dunia berskala besar-kecil.
- Gerak: Bawa kamera merentas skala dan transformasikan objek bagi menerangkan mekanisme, bukan mengulang zoom hiasan.
- Kegunaan: Konsep sains dan hubungan antara skala.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Flat Science Scale Journey (HG01) untuk bahan saya. Bawa kamera merentas skala dan transformasikan objek bagi menerangkan mekanisme, bukan mengulang zoom hiasan. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`

### HG02 · Investigative Material Collage
Sumber: `y2_vox`; status sumber: `parameterized-demo`; setempat: panduan.
- Rupa: Dokumen sebenar, keratan, foto dan aksen penanda dalam satu meja bukti.
- Gerak: Dedahkan bahan, sambungkan petunjuk dan highlight bukti; asingkan pergerakan kamera daripada langkah elemen.
- Kegunaan: Berita, sejarah dan penerangan berasaskan sumber.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Investigative Material Collage (HG02) untuk bahan saya. Dedahkan bahan, sambungkan petunjuk dan highlight bukti; asingkan pergerakan kamera daripada langkah elemen. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`

### HG03 · Progressive Whiteboard Reasoning
Sumber: `y3_whiteboard`; status sumber: `parameterized-demo`; setempat: panduan.
- Rupa: Garisan tangan, label ringkas dan hubungan yang disusun dalam ruang papan berterusan.
- Gerak: Lukis hujah mengikut frasa audio, sambung nod dan tarik keluar untuk menunjukkan hubungan lengkap.
- Kegunaan: Pengajaran, logik dan langkah penyelesaian.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Progressive Whiteboard Reasoning (HG03) untuk bahan saya. Lukis hujah mengikut frasa audio, sambung nod dan tarik keluar untuk menunjukkan hubungan lengkap. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`

### HG04 · Pose-and-Reaction Storytime
Sumber: `y4_storytime`; status sumber: `parameterized-demo`; setempat: panduan.
- Rupa: Watak original, prop yang konkrit dan latar yang menyokong pengalaman peribadi.
- Gerak: Tukar pose tegas, tahan reaksi dan potong dekat pada punchline; gunakan jeda yang disengajakan.
- Kegunaan: Cerita pengalaman, situasi harian dan humor neutral.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Pose-and-Reaction Storytime (HG04) untuk bahan saya. Tukar pose tegas, tahan reaksi dan potong dekat pada punchline; gunakan jeda yang disengajakan. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`

### HG05 · Meaning-Led Kinetic Type
Sumber: `y5_kinetic_type`; status sumber: `parameterized-demo`; setempat: panduan.
- Rupa: Kata utama dominan, teks sokongan minimum dan aksen warna berfungsi.
- Gerak: Letakkan kata pada cue bermakna, tukar skala/layout dan keluarkan frasa sebelum fokus baharu.
- Kegunaan: Senarai, petikan ringkas, penegasan dan struktur bab.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Meaning-Led Kinetic Type (HG05) untuk bahan saya. Letakkan kata pada cue bermakna, tukar skala/layout dan keluarkan frasa sebelum fokus baharu. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`

### HG06 · Concept-to-Concept Math Morph
Sumber: `t1_3b1b`; status sumber: `parameterized-demo`; setempat: panduan.
- Rupa: Objek/rajah tunggal dengan warna konsep yang konsisten pada pentas gelap terkawal.
- Gerak: Morph satu bentuk kepada konsep seterusnya dan tahan selepas langkah penting supaya penonton sempat memahami.
- Kegunaan: Matematik, rangkaian, kebarangkalian dan mekanisme.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Concept-to-Concept Math Morph (HG06) untuk bahan saya. Morph satu bentuk kepada konsep seterusnya dan tahan selepas langkah penting supaya penonton sempat memahami. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`

### HG07 · Product Keynote UI
Sumber: `t2_keynote_ui`; status sumber: `parameterized-demo`; setempat: panduan.
- Rupa: Screenshot atau produk sebenar sebagai hero, dengan label dan angka yang mudah dibaca.
- Gerak: Fokus kamera pada tindakan atau butiran, kembangkan kad menjadi paparan dan selesaikan angka pada cue audio.
- Kegunaan: Pelancaran produk, tutorial dan kemas kini fungsi.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Product Keynote UI (HG07) untuk bahan saya. Fokus kamera pada tindakan atau butiran, kembangkan kad menjadi paparan dan selesaikan angka pada cue audio. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`

### HG08 · Axes-Data-Annotation Charts
Sumber: `t3_finance_chart`; status sumber: `parameterized-demo`; setempat: panduan.
- Rupa: Paksi, unit dan data yang jujur dengan satu takeaway yang dominan.
- Gerak: Bina struktur dahulu, lukis data kedua dan tambah anotasi akhir; gunakan skala yang tidak mengelirukan.
- Kegunaan: Trend, perbandingan, kewangan dan data awam.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Axes-Data-Annotation Charts (HG08) untuk bahan saya. Bina struktur dahulu, lukis data kedua dan tambah anotasi akhir; gunakan skala yang tidak mengelirukan. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`

### HG09 · Presenter-Led Explanation
Sumber: `y6_presenter_explainer`; status sumber: `reference-snapshot`; setempat: panduan.
- Rupa: Penyampai bersama papan/rajah atau carta yang dipilih mengikut bahagian penerangan.
- Gerak: Alihkan fokus antara penyampai dan bukti, selaraskan gestur serta cue; gunakan aset watak/audio pengguna.
- Kegunaan: Kuliah ringkas, penerangan mekanisme dan video berpenyampai.
- Contoh arahan: `Guna @Buat Video Motion Grafik, koleksi Huashu Presenter-Led Explanation (HG09) untuk bahan saya. Alihkan fokus antara penyampai dan bukti, selaraskan gestur serta cue; gunakan aset watak/audio pengguna. Gunakan aset dan data sebenar; ikut durasi, nisbah serta audio yang saya tetapkan.`
