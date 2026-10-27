# Akses runtime Atlas yang dipinkan

## Sumber dan integriti

- Folder: https://drive.google.com/drive/folders/1QF3fxMu5ruysNbw92Jii5aU3xyb-tiJF
- Fail: https://drive.google.com/file/d/1wElWbb9VbWJijX9MnySMrE7xn1Gikoi5/view
- Nama: `Motion_Atlas_Locked_Toolkit_2026-10-27.zip`
- Saiz: 4415383 bait.
- SHA-256 ZIP: `fc98b5512e9ab36a48cd62365987ce4928c88fff58f27f358114995c29463e7c`.
- SHA-256 pakej renderer: `bb9e0626ba58cd207455120af1930c5d171ab96cd38d9b9a2059556be6dd72c7`.
- Sandaran penuh terdahulu (struktur skill berbeza): https://drive.google.com/file/d/19mXljWkVq5YhijqXlqCfCBtmD5iS9G3t/view . SHA-256 `05fcd2811d9e787131dc52da081897ab61b398c265677b72ed7f734200db2d64`; gunakan subfolder skill dalam ZIP itu sebagai root.
- Sandaran kedua: Library `libfile_2fb376991bdc8191b3791450eeb6483f` jika Drive benar-benar tidak dapat dicapai.

## Muat sekali dan guna semula

1. Gunakan Google Drive connector untuk metadata ID fail di atas, kemudian fetch fail ZIP asal dengan download_raw_file. Materialisasikan rujukan fail yang dikembalikan melalui mekanisme yang disokong. Jika connector tidak mencukupi, ikut aturan fallback browser; kekalkan sesi Google, jangan logout atau padam cookies.
2. Guna cache projek berasaskan SHA pakej. Jika ZIP/cache sah sudah ada, jangan muat turun semula untuk setiap preset atau scene. Semak hash ZIP sebelum ekstrak; jika tidak sepadan, hentikan penggunaan dan laporkan. Jangan menggantikan pin secara automatik.
3. Ekstrak ke direktori runtime projek berasingan. Tolak laluan mutlak, traversal `..` atau symlink yang keluar direktori. Sahkan SHA-256 ZIP di atas; wrapper mengesahkan hash fail renderer daripada `renderer/atlas_contract.json`. Jangan menimpa pemasangan skill semasa atau mengikuti SKILL.md lama di dalam arkib sebagai pengganti arahan skill terkini.
4. Root runtime ialah direktori ekstrak yang mengandungi `renderer/`, `scripts/`, `jobs/` dan `references/`. Baca `references/atlas-python-runtime.md` di root itu, kemudian panggil `scripts/atlas_preset.py` dari root runtime. Pastikan Python, Pillow, NumPy, FFmpeg dan ffprobe tersedia; ikut kontrak persekitaran dan jangan bina semula baseline untuk menutup kegagalan.
5. Gunakan `describe ID`, `init ID --output job.json` atau `import-config old.json --output job.json`; kemudian `check job.json`, `render job.json --output layer.mp4` dan `verify job.json --video layer.mp4 --report qa.json`. Untuk footage, ikut mode footage dan input/cue/alpha/tracking dalam panduan runtime. Jangan anggap init sahaja menyediakan footage sebenar.
6. Gunakan cache render yang mengesahkan job, kod dan aset. Semak visual pada footage sebenar, masa title, muka, crop, alpha, kontras dan audio selepas compositing. Jangan dakwa semua video Atlas diterbitkan sudah diaudit; baseline menguji renderer asal.

## Pilih laluan produksi

- Sunting video sebenar terus melalui Python/FFmpeg.
- Gunakan HTML/GSAP + HyperFrames untuk animasi vektor/kartun. Preset Python boleh dirender sebagai lapisan video/alpha dan dikompositkan.
- Runtime asli 16:9. Jangan meregangkan atau memotongnya secara senyap untuk 9:16; gunakan peletakan berkadar atau varian portrait yang diuji berasingan.
- Pakej mengandungi 922 preset, kod, fon/aset yang dibundel, validator, cache dan laporan ujian. Ia tidak membekalkan matting/tracking sebenar secara automatik.

## Keluaran laman semasa

Motion Atlas versi 12 diterbitkan pada 27 Oktober 2026: https://motion-preset-atlas.akramania.chatgpt.site . Setiap preset mempunyai job terkunci. Kesemua 922 preview lulus nyahkod penuh dan tiga sampel setiap video dibandingkan dengan renderer terkunci dalam toleransi MAE 5. Ini semakan sampel, bukan jaminan setiap frame/layout baharu. Jangan render semula katalog untuk permintaan pautan sahaja.
