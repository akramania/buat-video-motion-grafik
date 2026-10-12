# Koleksi PX400 dan SVG1000

## Kandungan

1. Pemilihan dan skop
2. Render preset PX
3. Elemen SVG
4. Provenance dan had

## Pemilihan dan skop

Gunakan PX001–PX400 untuk tipografi editorial, caption, peta/laluan, kamera mengikuti kenderaan, data dan infografik, UI/app/workflow, produk, promosi serta collage/peralihan. Registry keseluruhan mempunyai 842 preset: 137 asal, 185 demo panduan, 120 EV dan 400 PX. Kekalkan katalog [Motion Atlas](https://motion-preset-atlas.akramania.chatgpt.site).

| ID | Modul | Kegunaan |
| --- | --- | --- |
| PX001–PX100 | `premium_type.py` | Tipografi, title, lower third, caption |
| PX101–PX200 | `premium_maps_data.py` | Peta skematik, route camera, data, infografik |
| PX201–PX300 | `premium_ui_product.py` | UI, SaaS, workflow, mockup, produk |
| PX301–PX400 | `premium_promo_fx.py` | Promosi, photo/collage, papercraft, peralihan |

Pilih mengikut medan `mechanism`, `asset_types`, `use_cases` dan `parameters` dalam empat indeks JSON di `assets/motion_presets/`. Pilih struktur yang menjelaskan mesej sebelum memilih warna. Indeks menyimpan resipi yang dilaksanakan; perubahan arah atau palet semata-mata bukan ID baharu.

## Render preset PX

Gunakan CLI sedia ada:

```bash
python assets/motion_presets/render.py --preset PX101 --clean --output route.mp4
python assets/motion_presets/render.py --config scene.json --clean --output scene.mp4
python assets/motion_presets/render.py --preset PX001 --frame 3 --output sample.png
```

Kanvas dalaman 1280×720, default enam saat, clock reka bentuk 0–5 diretime mengikut `duration`. Atlas menerbitkan MP4 senyap 960×540, 30 fps, enam saat. Subtitle/label ialah kandungan visual, bukan caption automatik selari audio. Parameter berbeza mengikut modul; periksa indeks sebenar. Untuk durasi lama, gunakan jam cue/scene berasingan atau komposisi produksi; memanjangkan duration hanya memperlahankan resipi ini.

Peta ialah ilustrasi skematik. Gantikan geometri dan laluan dengan data lokasi sebenar bersumber jika projek memerlukan ketepatan geografi. Perspektif ialah 2.5D; bukan mesh 3D atau simulasi optik kaca. Bina semula layout portrait. Semak teks/angka/paksi/mask dan media gantian selepas mengubah konfigurasi. Jangan anggap endpoint transisi, penggunaan alpha atau imej tersuai seragam bagi semua PX; baca metadata dan render sampel pilihan sebenar.

## Elemen SVG

Koleksi kini mempunyai 1,500 SVG; tambahan SV1001–SV1500 diterangkan dalam [aset explainer dan promosi](svg-assets-explainer-promotion.md).

`assets/svg_elements/files/SV0001.svg` hingga `SV1000.svg` ialah 1,000 elemen vektor asal dengan latar transparent. Dua indeks, `svg_icons_index.json` dan `svg_motion_index.json`, menyimpan nama, kategori dan tags. SVG mempunyai kumpulan yang boleh dipilih dan dianimasikan; periksa ID sebenar pada fail sebelum menggunakan selector. Tidak mengandungi skrip atau rujukan luar.

```bash
python scripts/svg_element.py --search medical
python scripts/svg_element.py --id SV0001 --output asset.svg
python scripts/svg_element.py --id SV0001 --output asset.png --width 1024
```

Eksport PNG memerlukan CairoSVG. Untuk animasi vektor, baca SVG terus dalam SVG/HTML/Canvas renderer dan jadualkan entrance, hold/ambient dan exit pada group yang sesuai. Eksport raster hanya apabila perender projek memerlukannya. Kekalkan viewBox dan nisbah; jangan menganggap fail SVG terus disokong `PIL.Image.open`. Gunakan aset untuk membantu mesej dan elakkan penambahan hiasan tanpa fungsi. Ikon perubatan ialah simbol, bukan ilustrasi anatomi atau bukti klinikal.

## Provenance dan had

Rujukan Envato diperiksa pada 11 Oktober 2026. Metadata `observation_basis` membezakan `listing-description` daripada `preview-inspected`. Bagi listing sahaja, jangan mendakwa animasi asal ditonton atau ditiru tepat. Bagi preview, simpan masa/bingkai sebenar yang diperiksa dan bezakan pemerhatian visual daripada resipi baru. Audio sumber tidak dinilai melainkan dinyatakan secara khusus.

Semua renderer PX dan SVG dibuat secara asal untuk koleksi ini; tiada template berbayar, imej stok, logo jenama, rakaman preview atau audio Envato dimasukkan dalam toolkit. Koleksi ialah komponen Python/SVG, bukan fail `.aep`, `.mogrt` atau projek Resolve. Empat fon DejaVu dan data Natural Earth sedia ada mengekalkan lesen masing-masing.

### Pemeriksaan tambahan tipografi

Preview awam [Kinetic Typography MOGRT SJC43GQ](https://elements.envato.com/kinetic-typography-mogrt-SJC43GQ) diperiksa pada contact sheet setiap tiga saat dan media diukur 39.178 saat, 3840×2160, 60 fps. Bingkai memperlihatkan stack bold tengah, reveal kata melalui mask, teks fill di hadapan echo outline besar, susunan outline mendatar/menegak, inversi hitam-putih dan offset fill/outline. Pemeriksaan ini menyokong arah visual; ia tidak mengesahkan expressions, graph layer, easing atau semua variasi sumber. Rekod setiap PX tetap mengikut pemeriksaan pembinanya sendiri.

### Pengesahan koleksi ini

Semua 400 MP4 PX didekod penuh, disemak 960×540/30 fps/180 frame dan dibandingkan dengan bingkai renderer semasa. Semua 1,000 SVG diparse XML serta diraster melalui CairoSVG; geometri unik, kumpulan main/accent/details, tiada rujukan luar atau clipping dikesan. Perubahan teks/imej projek masih perlu QA baru.
