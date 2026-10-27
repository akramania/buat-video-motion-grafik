# Cache dan muat turun terpilih

Gunakan manifest Gemini_Motion_Manifest.json keluaran atlas-locked-cache-first-2026-10-27 dari folder keluaran dalam SKILL.md. Manifest memetakan key kategori kepada pautan Drive, saiz dan SHA-256 ZIP serta setiap fail. Jangan campur manifest/pek legacy 22 Oktober.

```bash
python scripts/gemini_cache.py plan --manifest /path/Gemini_Motion_Manifest.json --need core presets --root /vm/cache/motion-2026-10-27 --cache-root /path/existing/toolkit --packs-dir /path/cached-zips
python scripts/gemini_cache.py install --manifest /path/Gemini_Motion_Manifest.json --need core presets --root /vm/cache/motion-2026-10-27 --cache-root /path/existing/toolkit --packs-dir /path/cached-zips
python scripts/gemini_cache.py verify --manifest /path/Gemini_Motion_Manifest.json --need core presets --root /vm/cache/motion-2026-10-27
```

Helper tidak menggunakan rangkaian. plan memulangkan ready jika fail diekstrak sah; install-local jika ZIP sah tersedia; download-required hanya bagi pek hilang/tidak sah. Muat turun pek itu sahaja melalui saluran Drive yang tersedia di Gemini. Semak storan VM/root cache yang diketahui dahulu. Jangan muat turun semua pek atau mengimbas fail pengguna tanpa keperluan.

install mengekalkan fail custom dan menolak ZIP palsu, hash salah, traversal dan symlink. Untuk pemasangan lama tanpa receipt, gunakan root versi baharu. verify menyemak pek terpilih sahaja, bukan semua koleksi/dependency. Selepas itu jalankan preflight khusus dan Atlas check. Jangan mengaku ready untuk model atau HTML daripada semakan aset sahaja.

Atlas memerlukan core + presets. Watak: characters. SVG: svg. MA: motion_array. Fon tambahan: fonts. Untuk VL cari path/payload dalam packs[].files dan ambil key pek berkaitan sahaja. Preview adalah pilihan. Pemasang gemini_install.py lama untuk pemulihan legacy penuh sahaja.

Dalam cache kosong, ambil helper gemini_cache.py dan manifest kecil dahulu. Kekalkan cache/receipt/model selepas buang frame render. Jika offline dan fail perlu tiada, laporkan fail tepat; jangan cuba rangkaian berulang atau reka status pemasangan.

## Pautan keluaran yang disahkan

- Manifest: https://drive.google.com/file/d/1if4Fo75apN7t_mMP4qQqfMEPiM3feiaT/view
- SHA-256 manifest: `eb5ade93a00d4ce951dcecdfa2775906fb7a121278974e04f44410e502b06eb0`.
- Helper cache: https://drive.google.com/file/d/1-V1lM14cVPCyhyvWo3UhuugeSHnllMC1/view
- Semua 10 pek dipautkan melalui `packs[].drive_url` dalam manifest. Simpan nama tempatan mengikut `packs[].name`.
- Atlas versi 12: https://motion-preset-atlas.akramania.chatgpt.site

Semakan portabiliti setempat: 9 senario cache lulus; ujian bebas menggunakan hanya core + presets dari cache berjaya merender title T01 dan komposisi 2 saat, 640×360/24fps, 48 frame, nyahkod penuh serta enam sampel parity lulus. Ini bukan ujian dalam akaun Gemini.
