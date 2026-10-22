# Enjin planet 2.5D dan ruang angkasa advanced

Gunakan panduan ini apabila video memerlukan planet, bulan, sfera bercahaya, orbit, gelang, atmosfera, bintang parallax atau penerbangan kamera dalam ruang angkasa. Pelaksanaan yang boleh diguna semula berada di `scripts/advanced_planet_engine.py`. Ia ialah komponen sprite RGBA deterministik, bukan perender scene lengkap, enjin 3D sebenar atau simulasi astronomi.

## Bahasa visual yang terbukti

- Bentuk planet datang daripada tekstur equirectangular prosedur yang dipetakan pada sfera dengan `lat = asin(y)` dan `lon = atan2(x, z)`.
- Pensampelan bilinear, interpolasi dua fasa putaran dan tepi alpha berfeather mengelakkan lonjakan fasa serta tepi bergerigi.
- Diffuse, specular setempat dan Fresnel rim memisahkan isipadu sfera daripada latar tanpa mengaburkan tekstur.
- Awan Bumi bergerak pada jam berasingan daripada permukaan. Gunakan lapisan berasingan juga bagi atmosfera atau ribut lain; jangan melekatkan semua detail pada albedo tunggal.
- Gelang Zuhal/Uranus disusun `belakang → badan → bayang gelang → hadapan`. Jangan lukis gelang sebagai satu elips di atas planet kerana z-order itu merosakkan kedalaman.
- Bulan dan satelit menggunakan nilai depth daripada orbit; lukis `z < 0` sebelum planet dan `z >= 0` selepas planet.
- Untuk video potret, susun dunia dalam ruang kamera tetapi pin tajuk, caption, kad fakta dan HUD dalam screen space. Gerak kamera tidak boleh menggoncang teks bacaan.

## Penggunaan komponen

Keperluan: Python 3, NumPy dan Pillow.

```bash
python3 scripts/advanced_planet_engine.py \
  --kind saturn --time 8.4 --diameter 640 \
  --output /tmp/saturn.png
```

Sebagai modul:

```python
from advanced_planet_engine import Planet25DEngine, orbit_position

engine = Planet25DEngine(size=512, phases=72, max_cache_frames=192)
sprite = engine.render_planet("earth", t_seconds=4.2, diameter=560)
x, y, z = orbit_position(theta=1.1, rx=210, ry=72)
```

Nama yang disokong: `sun`, `mercury`, `venus`, `earth`, `moon`, `mars`, `jupiter`, `saturn`, `uranus`, `neptune`. Salin skrip ke folder projek sebelum mengubah tekstur atau gaya. Gunakan nama dalaman bahasa Inggeris untuk API dan label BM pada scene.

## Komposisi scene premium

1. Tetapkan satu arah cahaya utama dan kekalkan terminator yang masuk akal merentas shot bersebelahan.
2. Bina tiga lapisan bintang dengan kelajuan kamera berbeza. Tambah nebula atau debu secara setempat; jangan beri semua partikel kecerahan dan kelajuan sama.
3. Gunakan micro-drift kamera yang kecil semasa hold. Untuk zoom, gerakkan kamera/world transform; jangan menjana tekstur planet pada diameter baharu bagi setiap frame.
4. Render sprite pada saiz sasaran, kemudian animasikan parent scale ketika entrance. Diameter yang berubah setiap frame menghasilkan terlalu banyak entri cache dan boleh menyebabkan saiz gelang kelihatan melompat.
5. Kekalkan satu fokus dominan. Label ringkas boleh mengikuti objek, tetapi fakta panjang berada pada kad stabil dalam safe area mudah alih.
6. Jika perbandingan saiz atau jarak dipermudah, paparkan `Ilustrasi tidak mengikut skala sebenar` dan jangan gambarkan susunan visual sebagai ukuran saintifik.

## Masa, cache dan prestasi

- Semua gerak menggunakan `t = frame / fps`; seed prosedur mesti tetap.
- `phases=72` biasanya memadai untuk sprite 512 px kerana enjin mengadun dua fasa bersebelahan. Tambah fasa hanya selepas membuktikan artefak pada playback biasa.
- Cache badan ialah LRU terkawal. `approximate_cache_mib` menganggar bajet piksel badan; NumPy, tekstur, awan dan gelang menambah overhead.
- `light_angle` dikuantum kepada beberapa bin. Jangan mengubahnya secara sangat halus setiap frame jika cahaya tidak perlu bergerak.
- Gelang dikuantum mengikut diameter dan dicache. Untuk entrance, scale sprite siap pada compositor seperti di atas.
- Render video panjang mengikut julat frame tepat, contohnya `[start_frame, end_frame)`, dengan dimensi, FPS, pixel format dan encoder sama. Segmen boleh dirender selari apabila fungsi frame tulen dan sumber mencukupi, kemudian disambung menggunakan concat demuxer.
- Jangan menahan semua frame video dalam memori. Hantar bingkai RGB terus ke FFmpeg atau simpan hanya segmen yang sedang diproses.

Contoh enkod asas:

```bash
ffmpeg -f rawvideo -pix_fmt rgb24 -s 1080x1920 -r 30 -i - \
  -c:v libx264 -preset veryfast -crf 17 -tune animation \
  -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 \
  -colorspace bt709 -movflags +faststart visual.mp4
```

Tetapan ini ialah titik mula yang telah diuji, bukan syarat universal. Gunakan audio master berasingan, kemudian mux AAC selepas visual diluluskan.

## QA minimum

Render dan periksa sekurang-kurangnya Matahari, Bumi, Zuhal, Uranus dan satu planet gelap pada tiga masa berlainan. Uji:

- tepi alpha, terminator, arah cahaya dan banding planet;
- interpolasi putaran pada bingkai bersebelahan;
- awan Bumi tidak terkunci pada permukaan;
- gelang belakang/hadapan, bayang pada badan dan crop sprite;
- depth orbit ketika objek bertukar dari belakang ke hadapan;
- teks kekal stabil semasa kamera bergerak;
- penggunaan memori dan masa render bagi resolusi sebenar.

Selepas master siap, semak metadata, bilangan frame dan nyahkod penuh. Gunakan `blackdetect` serta `freezedetect` sebagai pengesan awal, bukan pengganti pemeriksaan visual. Semak loudness/true peak jika audio ada. Untuk hasil pendidikan, audit fakta, ejaan dan penafian skala berasingan daripada QA teknikal.

## Batas tuntutan

Tekstur prosedur menjadikan planet mudah dikenal dan sesuai untuk motion graphic, tetapi bukan peta topografi atau imej teleskop yang tepat. Komponen tidak mengandungi kamera, typography, voice-over, muzik, caption atau master timeline. Projek Sistem Suria advanced membuktikan penggunaan komponen dan teknik pada video 1080×1920/30 fps; ia tidak membuktikan semua projek ruang angkasa akan mencapai mutu sama tanpa art direction, integrasi scene dan QA penuh.
