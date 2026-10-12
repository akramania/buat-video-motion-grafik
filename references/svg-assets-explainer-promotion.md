# Aset SVG untuk explainer dan promosi

Simpan dan gunakan fail sebenar `assets/svg_elements/files/SV0001.svg` hingga `SV1500.svg`. Koleksi ini sebahagian aset skill buat-video-motion-grafik. Ia berasingan daripada 842 preset animasi; tambahan 500 ialah artwork SVG statik yang boleh dianimasikan.

## Koleksi tambahan

| ID | Bilangan | Fokus |
| --- | ---: | --- |
| SV1001–SV1100 | 100 | Pembelajaran, props cerita, masalah/penyelesaian, perjalanan servis |
| SV1101–SV1200 | 100 | Proses digital, maklumat/privasi, kerjasama, sistem bandar mampan |
| SV1201–SV1250 | 50 | Keputusan/tradeoff, sebab dan akibat |
| SV1251–SV1300 | 50 | Promosi kursus, produk digital, servis dan acara |
| SV1301–SV1400 | 100 | Pentas produk, packaging/unboxing, beauty/food, retail showcase |
| SV1401–SV1500 | 100 | Tawaran/nilai, engagement, live commerce, pelancaran |

Baca tujuh indeks `assets/svg_elements/svg_*_index.json` melalui helper; jangan muatkan 1,500 fail ke konteks sekaligus. Metadata baharu menyimpan `collection`, `use_cases`, `layers` dan `suggested_motion`. `suggested_motion` ialah cadangan produksi, bukan animasi terbina atau bukti rig tubuh/fizik. Semak nama ID dan group sebenar sebelum menggunakan selector.

## Pilih dan masukkan ke projek

```bash
python scripts/svg_element.py --collection explainer --search learning
python scripts/svg_element.py --collection promotion --search product
python scripts/svg_element.py --id SV1301 --output product-stage.svg
python scripts/svg_element.py --id SV1301 --output product-stage.png --width 1024
```

Carian CLI memaparkan maksimum 20 hasil secara lalai; guna `--limit 0` hanya apabila perlu semua padanan. Salin aset terpilih ke folder projek dan rekod `svg_asset_ids` serta laluan salinan dalam manifest adegan. PNG mengekalkan alpha; Pillow tidak membaca SVG terus, jadi raster melalui CairoSVG dahulu. Kekalkan nisbah viewBox. Palet pastel dan outline boleh disunting pada SVG, tetapi semak kontras dengan latar projek. Layout asal mempunyai margin; semak semula clipping selepas scale, rotation atau blur.

Bagi explainer, pilih komposisi yang menerangkan tindakan, hubungan atau sebab-akibat. Bagi promosi, gabungkan pentas produk dengan foto/packaging pengguna, teks manfaat dan CTA. Gunakan placeholder sebagai struktur komposisi; jangan menggantikannya dengan logo atau tuntutan produk yang tidak dibekalkan. Gantikan apa-apa data ilustrasi dan nilai demo dengan bahan sebenar projek.

## Komposisi beranimasi

`python scripts/svg_asset_scene.py --scene assets/svg_elements/svg_scene_example.json --output sample.mp4` menghasilkan komposisi senyap asas melalui Pillow, CairoSVG dan FFmpeg. Gunakan `--output sample.png --frame 3` untuk satu bingkai. Skrip menganimasikan setiap aset sebagai satu lapisan, mengekalkan alpha artwork dan nisbah, dengan entrance rise/fade, float/pulse ringan dan exit fade. Ia tidak memisahkan objek dalaman atau menyediakan watak berartikulasi; untuk gerakan dalaman gunakan group `main`, `accent`, `details` dalam SVG/DOM/renderer projek.

Scene menggunakan `width`, `height`, `duration`, `fps`, `background` dan `assets`. Setiap aset menerima `id`, koordinat top-left `x`,`y`, `width`, `start`,`end`, `entrance`,`exit` dan `ambient` (`none`,`float`,`pulse`). Background `transparent` disokong untuk PNG; MP4 biasa memerlukan latar opaque. Pilih 16:9 atau 9:16 projek dan bina semula posisi untuk nisbah tersebut. Tetapkan start/end berdasarkan audio sebenar apabila voice-over diperlukan, kemudian semak entrance, hold, exit dan overlap teks pada bingkai/video sebenar.

Katalog dan muat turun aset berada pada [Motion Atlas](https://motion-preset-atlas.akramania.chatgpt.site/#svg-library). Semua aset ialah vektor asal, tanpa skrip atau rujukan luar. Simbol perubatan dan peta bersifat ilustrasi. Lesen DejaVu/Natural Earth bagi komponen lain tidak berubah.

Pengesahan koleksi: 1,500 geometri unik selepas mengetepikan warna; 1,000 fail asal mengekalkan hash; semua 500 tambahan diparse dan diraster, alpha dan margin disemak. Komposisi enam aset baharu diuji sebagai MP4 senyap 1280×720/30 fps/enam saat dan didekod penuh. Penyesuaian projek memerlukan QA baharu.
