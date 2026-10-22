# Whisper dan pengasingan subjek tempatan

Gunakan `scripts/media_tools.py` untuk transkrip sumber dengan pemasaan perkataan dan PNG subjek beralpha. Gunakan model tempatan sebelum render HTML; jangan bergantung pada cloud/CDN atau memulakan muat turun model semasa render. `rembg` di sini ialah backend remove-background, bukan nama pakej umum yang dianggap sudah tersedia.

## Runtime dan pemasangan

Runtime yang diuji: Python 3.12.14, faster-whisper 1.2.1, CTranslate2 4.8.3, PyAV **16.1.0**, rembg 2.0.86 dan ONNX Runtime 1.31.0 pada CPU Linux x86_64. Lock tepat dalam `assets/media_tools/requirements.txt` memerlukan Python 3.12+; jangan menganggap lock ini sesuai untuk Python 3.10, semua OS atau GPU. Pilih runtime Python 3.12+ yang sesuai jika enjin Python lama menggunakan versi lain. Kekalkan dependency media secara terasing.

Jangan naik taraf PyAV secara buta: ujian sebenar mendapati av 19.0.2 menyebabkan `TypeError: open() got an unexpected keyword argument 'metadata_errors'` pada faster-whisper 1.2.1. Pin av 16.1.0 sehingga versi lain diuji.

Cache lalai ialah `${XDG_CACHE_HOME:-~/.cache}/video-motion-media/` dengan `python-deps/` dan `models/`. Override melalui `MOTION_MEDIA_CACHE`, atau gunakan `--python-deps` dan `--model-root` secara eksplisit. Cache ini tidak termasuk dalam repo skill. Kedua-dua skill boleh menggunakan cache sama pada mesin ini.

```bash
# Semakan offline; tiada pemasangan atau download secara automatik.
python scripts/setup_media_tools.py
python scripts/media_tools.py preflight --strict --report /path/project/media-preflight.json

# Fasa persediaan online yang memasang lock serta model smoke test.
python scripts/setup_media_tools.py --install

# Atau gunakan wheelhouse offline yang sepadan OS/CPU/Python.
# Salin cache model lengkap termasuk model-manifest.json sebelum arahan ini.
python scripts/setup_media_tools.py --install --wheelhouse /path/wheels
```

Installer membuat target pakej baharu, memeriksa import dan checksum model, kemudian menukar target cache. Kegagalan sebelum pertukaran mengekalkan target lama. Ia tidak memasang FFmpeg sistem; semak `ffmpeg` dan `ffprobe` berasingan. `preflight` memeriksa import sebenar, fail model dan SHA-256 terhadap manifest, bukan sekadar kejayaan pip.

Model default smoke test: multilingual `tiny` pada commit Hugging Face `d90ca5fe260221311c53c58e660288d3deb8d356` serta `u2netp` (ringan). Ketepatan ceramah Arab/Melayu tidak disahkan oleh smoke test Inggeris. Pilih model Whisper lebih besar mengikut perkakasan dan ketepatan, kemudian uji audio projek. Bagi model lain, bekalkan revision yang sepadan dan jangan guna commit tiny.

```bash
python scripts/media_tools.py download-models --model-root /path/cache/models --whisper-model small --revision MATCHING_HF_COMMIT --rembg-model u2netp
```

Simpan `model-manifest.json` bersama cache; fail ini merekod commit Whisper, saiz dan hash setiap fail. Kekalkan lesen/provenance model. rembg ialah alat berlesen MIT tetapi model mempunyai lesen tersendiri. Semak sumber model khusus apabila menukar backend; jangan menganggap semua model rembg berlesen sama atau bebas kos cloud.

Untuk Gemini offline, muat turun pakej, browser, fon dan model dalam fasa online, pindahkan cache yang serasi ke sandbox, lalu jalankan preflight di situ. Pemasangan cache pada ChatGPT Work tidak membuktikan pemasangan dalam akaun Gemini pengguna.

## Transkrip dan subtitle Arab–Melayu

```bash
ffmpeg -y -i /path/input.mp4 -vn -ac 1 -ar 16000 /path/project/source.wav
python scripts/media_tools.py transcribe --input /path/project/source.wav --model-path /path/cache/models/whisper-small --language ar --vad --output /path/project/arabic-words.json --srt /path/project/arabic.srt
```

Whisper menggunakan `task=transcribe` dan `word_timestamps=True`; ia tidak menterjemah kepada Melayu dalam helper ini. API Whisper translate lazimnya menjana Inggeris, jadi jangan menggunakannya sebagai terjemahan Melayu. Output JSON menyimpan perkataan, masa mula/akhir, kebarangkalian serta segmen. VAD mengurangkan bahagian senyap; semak hallucination, perkataan berulang, nama, istilah agama, ayat dan nombor dengan audio sebenar. Jika audio dipotong daripada tengah video, bekalkan `--offset SECONDS` supaya masa merujuk timeline induk. Selepas edit/reorder klip, remap semua cue kepada edit decision list akhir.

Pemasaan perkataan ialah anggaran cross-attention/DTW, bukan ground truth atau forced alignment teks yang dibetulkan. Semak awal, pertengahan, akhir dan sempadan frasa sambil mendengar. Kekalkan transkrip/terjemahan yang sudah diluluskan; betulkan cue tanpa menulis semula teks itu secara senyap.

Terjemahkan kepada **Bahasa Melayu Malaysia** mengikut maksud frasa/baris yang lengkap. Petakan frasa Melayu kepada julat audio Arab yang sepadan; susunan perkataan antara bahasa berbeza, jadi jangan salin timestamp Arab satu-ke-satu kepada perkataan Melayu. Highlight Melayu mengikut cue semantik yang disemak; gunakan highlight per frasa jika penjajaran perkataan tidak pasti. Bezakan highlight berasaskan makna daripada forced alignment suara Melayu, kerana audio Melayu tiada dalam ceramah asal.

Dalam HTML, gunakan `lang="ar"`, `dir="rtl"`, fon Arab setempat dan shaping browser; tunggu fon siap sebelum ukuran. Animasikan perkataan/baris/blok yang sudah dibentuk. Jangan pecahkan aksara, reverse string, letter-spacing atau menjadikan huruf Arab terputus. Simpan terjemahan Melayu dalam elemen LTR yang berasingan. Muatkan cue ke timeline GSAP; jangan bergantung pada callback playback audio atau jam masa nyata.

## Pengasingan subjek dan video

```bash
python scripts/media_tools.py cutout --input /path/photo.png --output /path/project/subject.png --report /path/project/cutout-proof.json

# Untuk klip, tentukan FPS projek dan kekalkan frame ID tepat.
ffmpeg -y -i /path/clip.mp4 -an -vf fps=30 /path/project/source/%06d.png
python scripts/media_tools.py cutout --input /path/project/source --output /path/project/cutout --report /path/project/masks.json
```

Bina folder `source/` dahulu. Perintah batch memproses urutan imej mengikut nama dan menggunakan satu sesi ONNX untuk semua frame. Ia tidak menghasilkan mask yang stabil secara temporal secara automatik. Semak rambut, jari, pakaian, props, tepi muka dan motion blur pada latar terang/gelap serta playback biasa. Jika perlu, gunakan tracking/optical flow untuk mengalih alpha bingkai sebelumnya dan campuran kecil/histeresis di sempadan; reset pada cut dan occlusion. Jangan licinkan secara berlebihan hingga menghasilkan ghosting. Gunakan mask manual/rotoscope apabila model gagal, bukan menyembunyikan kehilangan anggota dengan blur.

Komposit PNG beralpha dalam HTML/SVG/Canvas. Kekalkan warna subjek, betulkan spill, cahaya dan exposure supaya sepadan latar. Output H.264 MP4 tidak menyimpan alpha: render komposisi akhir, atau gunakan codec alpha seperti ProRes 4444 jika lapisan berasingan diminta. Kekalkan audio asal dengan timeline induk; pemprosesan imej/sequence tidak mengekalkan audio secara automatik.

## Bukti ujian yang tersedia

- Cache pada mesin ini diperiksa offline dengan import sebenar serta 5 hash model yang sepadan.
- Sampel pertuturan `tests/data/jfk.flac` daripada repo rasmi faster-whisper berjaya ditranskrip menjadi 22 perkataan dengan timestamp; VAD turut diuji. Ini ialah smoke test ASR, bukan bukti ketepatan bahasa Arab/Melayu atau semua audio.
- `skimage.data.astronaut` diuji dengan u2netp: PNG 512×512 mempunyai alpha 0–255. Pemeriksaan visual menunjukkan subjek dikekalkan dengan sedikit sisa latar di bahu kiri; penalaan mask masih perlu untuk produksi.
- Pemeriksaan ini berasingan daripada QA HyperFrames, rig, tipografi dan MP4.

## Sumber primer

- [faster-whisper dan contoh word timestamps](https://github.com/SYSTRAN/faster-whisper)
- [API local_files_only, transcribe dan word_timestamps](https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/transcribe.py)
- [rembg: pemasangan, sesi, model dan contoh batch](https://github.com/danielgatis/rembg)
- [Lokasi cache dan pemilihan model tempatan rembg](https://github.com/danielgatis/rembg/blob/main/rembg/sessions/base.py)
- [U2netp: model dan checksum upstream](https://github.com/danielgatis/rembg/blob/main/rembg/sessions/u2netp.py)
