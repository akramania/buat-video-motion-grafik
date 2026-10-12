# Vektor sinematik dan gerakan berartikulasi

## Asas rujukan

Utamakan **panel atas** dalam `1000514096.mp4`, berlabel “GPT 6.1 Sol xhigh”, apabila pengguna meminta gaya vektor seperti rujukan ini. Label itu mengenal pasti panel pilihan pengguna; ia bukan bukti model, tetapan, perisian atau kod yang menghasilkan video. Jangan mengubah model berdasarkan label sahaja.

Fail yang diperiksa ialah rakaman skrin telefon 1080×2376 sepanjang 11.421 s, 380 bingkai dengan timestamp tidak seragam, tanpa trek audio. Kandungan atas berada kira-kira pada `x=52, y=500, w=976, h=548`, hampir 16:9. Jangan meniru status bar, label perbandingan, panel bawah, butang sosial atau nisbah telefon pembungkus. Anggaran crop hanya untuk fail rujukan ini.

Pemeriksaan meliputi bingkai sepanjang rakaman setiap 0.5 s, urutan 12 fps pada 1–2 s dan 4 fps pada 0.25–3.25 s. Watak penunggang kekal hampir pada tempatnya; kaki bertukar pose kayuhan, dan garisan jalan, pagar, tiang serta papan tanda melintas ke kiri. Kedudukan bukit berubah lebih perlahan. Ini menyokong olahan kamera menjejak subjek dengan latar parallax; ia tidak membuktikan hukum fizikal atau FPS asal. Playback biasa belum diperiksa melalui alat yang boleh memainkan video; jangan mendakwa kelancaran subjektif telah disahkan hanya daripada contact sheet.

## Artwork yang perlu dipindahkan

- Bina ilustrasi vektor original dengan siluet bersih, bentuk Bézier, perkadaran manusia natural dan garisan kontur yang terpilih. Kepala tidak dibesarkan seperti avatar, sendi tidak kelihatan seperti bebola, dan anggota tidak menjadi batang seragam.
- Beri watak bentuk pakaian, muka profil, leher yang bersambung, helmet/aksesori, tangan serta kasut yang jelas. Reka bahagian yang bergerak sebagai lapisan tersendiri; tutup sambungan sendi dengan bentuk pakaian apabila sesuai.
- Gunakan bahan dan butiran yang membantu objek dikenali: rangka, tayar, rim, hab, gear, rantai, pedal, kabel dan botol pada basikal. Ketebalan tiub dan perspektif kedua-dua roda mesti konsisten. Jangan tambah perincian kecil yang berkelip ketika bergerak.
- Gunakan palet terkawal dan sedikit desaturasi. Asingkan langit bergradasi, cahaya matahari lembut, bukit jauh yang pucat, bukit tengah, pepohon, padang, pagar dan jalan. Aksen pakaian mengikat mata kepada watak; latar tidak perlu sama terang.
- Letakkan bayang sentuhan di bawah roda/kaki dan highlight nipis pada bahan. Glow setempat memberi suasana; blur seluruh artwork akan merosakkan tepi vektor.
- Komposisi asal menggunakan penunggang dan basikal kira-kira separuh lebar kanvas dengan landskap yang luas. Gunakan saiz ini sebagai permulaan bagi adegan alam yang bermakna; jangan memaksa watak menjadi 70% lebar sehingga basikal atau anggota terpotong. Brief terbaru dan kebolehbacaan tetap menentukan saiz akhir.

## Sistem gerak

1. Bezakan **jam aksi** daripada durasi adegan. Nyatakan cadence dalam putaran sesaat, jarak perjalanan dalam unit reka bentuk sesaat dan fasa awal. Memanjangkan scene tidak patut memperlahankan kayuhan atau semua gerak latar.
2. Tetapkan hierarki parent dan pivot: root badan → torso → bahu/siku/pergelangan; pelvis → paha/lutut/buku lali; engkol → pedal; hab → roda. Simpan pivot dalam koordinat sumber dan asingkan transform kamera.
3. Gunakan satu fasa engkol bagi kedua-dua pedal: `theta = theta0 + 2*pi*cadence*t`, pedal jauh berbeza `pi`. Kasut mengekalkan titik sentuhan pada pedal. Jangan animasikan kaki dan pedal dengan sinus berasingan sehingga kaki terapung.
4. Selesaikan lutut dengan IK dua tulang yang mempunyai panjang tetap. Pilih sisi lenturan yang konsisten dan uji seluruh cycle. Sasaran di luar reach perlu dibetulkan melalui geometri/pose; jangan menyembunyikannya dengan memanjangkan anggota. Pegangan tangan kekal pada handlebar dan leher mesti bersambung ke torso.
5. Bagi roda pada satah jalan yang sama, hubungkan jarak dan putaran melalui `angle = distance / radius`. Gear menghubungkan cadence engkol kepada putaran roda. Lapisan latar yang jauh boleh bergerak lebih perlahan sebagai olahan kedalaman; itu bukan alasan tayar meluncur pada jalan.
6. Guna sela kedalaman yang jelas untuk parallax: langit/cahaya hampir tetap → bukit jauh sangat perlahan → bukit tengah → pepohon/pagar → penanda jalan paling pantas. Pastikan perspektif jalan dan arah bayang menyokong gerakan. Jangan memberi semua lapisan kelajuan sama.
7. Bina gerak berkala dengan fungsi masa berterusan. Gerak mekanikal tidak memerlukan ease-in-out yang berhenti pada setiap pusingan. Entrance, berhenti, membelok dan memindahkan fokus boleh menggunakan easing dan acceleration yang sesuai. Secondary motion badan perlu kecil dan terkait aksi, bukan goyangan serentak seluruh scene.
8. Bagi latar berulang, simpan identiti objek berdasarkan indeks dunia, bukan indeks slot skrin. Apabila offset dibalut pada sempadan tile, pokok/tiang yang sama mesti kekal sama. Semak bingkai sebelum dan selepas wrap; semua pokok tidak boleh bertukar bentuk serentak.

## Resipi yang boleh diadaptasi

- **Watak berkayuh/mesin berputar:** satu master phase, gear, titik sentuhan, IK dan kamera menjejak. Contoh executable disediakan di bawah.
- **Watak berjalan/berlari:** bezakan stance dan swing; kunci tapak pada tanah ketika stance, pindahkan pelvis, guna IK, kemudian toe-off. Rig kayuhan bukan rig berjalan; bina kitaran baharu.
- **Tangan menggunakan alat:** sasaran sentuhan pada objek, sendi panjang tetap, gerak alat memandu tangan dan reaksi badan kecil. Tukar pose genggaman apabila objek bertukar.
- **Kenderaan merentas landskap:** roda mengikut jarak, suspensi beramplitud kecil, lapisan alam berbeza kelajuan dan objek dunia beridentiti tetap.
- **Objek terpasang/terbuka:** bahagian vektor berasingan, pivot mekanikal tepat, anticipation ringkas, settle dan hold yang menerangkan fungsi.
- **Adegan alam atau sains:** lapisan atmosfera, aliran/path yang berterusan, tumpuan pada objek utama dan perubahan yang menjelaskan sebab/akibat. Jangan tambah gaya hentak promosi tanpa arahan.

Resipi selain kayuhan ialah panduan pengarahan, bukan preset renderer yang sudah dilaksanakan. Jangan mengira resipi, warna, sudut kamera atau FPS sebagai preset tambahan. Gaya ini ialah pilihan tambahan bagi watak, alam dan gerakan fizikal; rujukan terbaru pengguna mengatasi gaya Learnfly/live commerce hanya apabila berkaitan dengan brief.

## Komponen SVG yang boleh dirender

Gunakan `scripts/vector_cyclist.cjs` sebagai proof renderer berasingan, bukan entri baharu `assets/motion_presets/render.py`. Ia menyediakan SVG original, IK dua tulang, kaki pada pedal, putaran roda yang terkait jalan, lapisan parallax dan frame deterministik. Modul mengeksport `configuration`, `state`, `twoBone`, `frameSvg`, `audit` dan `render` untuk adaptasi projek.

Dependencies yang diuji: Node, `sharp` dan FFmpeg. Modul mencari `sharp` pada projek atau melalui `CODEX_PRIMARY_RUNTIME_NODE_MODULES`. Semak dependencies setempat; jangan menganggap Remotion/Blender diperlukan atau telah dipasang. SVG source kekal editable walaupun eksport video ialah raster.

```bash
node scripts/vector_cyclist.cjs --frame 0.5 --output styleframe.svg
node scripts/vector_cyclist.cjs --frame 0.5 --output styleframe.png
node scripts/vector_cyclist.cjs --duration 8 --fps 60 --output proof.mp4
node scripts/vector_cyclist.cjs --config config.json --audit
```

Contoh konfigurasi:

```json
{"duration":8,"fps":60,"width":1280,"cadence":0.82,"gear":1.35,"phase":0.45,"jersey":"#234c60","accent":"#dc8156","skyTop":"#426272","skyBottom":"#e8c4a0","seed":17,"supersample":1.5}
```

Salin komponen ke projek sebelum mengubah watak, lokasi, cerita atau cue. `duration` menentukan panjang petikan; `cadence` dan `gear` menentukan aksi tanpa retime scene. `--frame` menerima masa sebenar dalam saat. Kanvas renderer ini 16:9; bina semula framing dan safe area bagi portrait, jangan crop automatik. Tiada audio/VO pada proof asal. Had 120 s ialah had petikan komponen, bukan had 30 minit video akhir skill.

Proof asal pada 1280×720, 60 fps, 8 s menghasilkan 480 frame yang dinilai pada masa berlainan. Audit geometri menunjukkan panjang tulang dan titik kasut/pedal kekal dalam ralat floating point, serta jarak jalan sama dengan sudut roda×radius. Ini mengesahkan constraint kod, bukan keseluruhan anatomi, estetika, renderer sumber atau kesamaan sempurna dengan rujukan. Jangan mendakwa demo ini video kempen lengkap atau engine vektor generik.

## QA sebelum video sebenar

- Render styleframe pada pose paling ekstrem dan satu petikan aksi lengkap. Semak siluet, leher/bahu, panjang anggota, bentuk lutut, titik pegangan, lapisan depan/belakang, kontak pedal/tanah serta crop.
- Gunakan frame deterministik `t=frame/fps`, subpixel transform dan antialias. Pilih 60 fps untuk aksi berterusan apabila mampu; jangan menyalin setiap frame 30 fps dua kali dan menyebutnya animasi asli 60 fps. FPS tinggi sahaja tidak menjamin gerak baik.
- Audit satu cycle penuh dan semua sempadan wrap, entrance, stop serta exit. Semak tiada pop pada pose, z-order, bayang, bentuk latar atau identiti objek. Bagi loop seluruh scene, samakan pose **dan** keadaan dunia pada hujung; pose berkala sahaja tidak menjadikan MP4 loop seamless.
- Periksa playback biasa dan bingkai bersebelahan. Jika alat playback tiada, nyatakan batas itu dan berikan petikan sebenar untuk dinilai; contact sheet serta nombor audit tidak menggantikan pemeriksaan masa nyata.
- Semak `ffprobe`, jumlah frame, dimensi, FPS dan nyahkod penuh. Untuk VO/caption, ikut pilihan sedia ada dan audio sebenar; jangan mencipta bukti mutu suara daripada rujukan tanpa audio.
