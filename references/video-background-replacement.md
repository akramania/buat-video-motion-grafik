# Remove dan replace background video manusia

Gunakan RVM MobileNetV3 FP32 untuk penyampai/manusia. Model menyimpan empat recurrent states antara bingkai; jangan menggunakan sesi baharu bagi setiap imej. Kekalkan `media_tools.py cutout`/rembg untuk imej dan pilihan lain yang sesuai. RVM bukan segmenter semua objek dan tidak menjamin rambut, gerakan kabur atau props sentiasa sempurna.

## Pasang dan sahkan sebelum kerja

```bash
python3 scripts/ensure_background.py --report /path/project/background-ready.json
# Semakan tanpa pip atau rangkaian:
python3 scripts/ensure_background.py --offline --report /path/project/background-ready.json
```

Teruskan hanya apabila `ready: true`: FFmpeg/ffprobe ditemui, import dependency berjaya, saiz/SHA-256 model sepadan dan dua inferens sebenar menggunakan recurrent state yang sama berjaya. Installer menggunakan runtime serasi yang tersedia; jika import gagal, pasang lock minimal dalam cache terasing. Ujian input rata membuktikan enjin berjalan, bukan mutu pengasingan manusia sebenar. Jangan dakwa GPU telah diuji; laluan ini menggunakan CPU.

Simpan berat model di `${MOTION_MEDIA_CACHE:-${XDG_CACHE_HOME:-~/.cache}/video-motion-media}/models/rvm/`, bukan Git. Kekalkan cache ini ketika membersihkan render. Persekitaran baharu mungkin kehilangan cache: jalankan semula ensure; model dimuat turun daripada release rasmi v1.0.0 dan disahkan dengan hash terpin. Kekalkan lesen GPL-3.0 serta provenance dalam `assets/media_tools/background-models.json`. Jangan mengganti model atau menaik taraf pakej Whisper untuk kerja background.

Runtime diuji: Python 3.12.14, ONNX Runtime 1.31.0, NumPy 2.3.5, Pillow 12.3.0 dan FFmpeg CPU. Jika FFmpeg/ffprobe tiada, pasang build FFmpeg yang serasi melalui persekitaran yang dibenarkan, kemudian ulang ensure. Kegagalan akses/rangkaian/ruang mesti dilaporkan; jangan cipta laporan ready.

## Matte dahulu, komposit kemudian

```bash
python3 scripts/background_video.py matte \
  --input /path/source.mp4 --output /path/project/alpha.mkv \
  --fps 30 --cuts /path/project/cuts.json

python3 scripts/background_video.py render \
  --input /path/source.mp4 --mask /path/project/alpha.mkv \
  --background /path/studio.png --output /path/project/final.mp4 \
  --width 1080 --height 1920
```

`cuts.json` ialah senarai saat pada clock klip terpilih, contohnya `[3.2, 8.7]`. Gunakan EDL yang disahkan untuk cut sebenar; pengesan beza imej kasar bukan jaminan semua jump cut ditemui. `--scene-threshold 0` mematikan pengesanan automatik. Reset state pada cut; jangan bawa state dari shot/individu lain.

Gunakan `--start` dan `--duration` ketika membina matte untuk proof atau petikan. Render membaca julat sama daripada metadata; jangan seek kedua-dua input secara berbeza. `fps=...:start_time=0` digunakan pada matte dan sumber supaya VFR ditukar pada clock yang sama. Mask dan overlay mesti mengikuti EDL selepas dialog dipotong; jangan trim hanya video atau hanya mask. Helper menolak sumber/mask yang berubah selepas metadata ditulis.

Mask `.mkv` ialah FFV1 grayscale lossless; `.mp4` ialah pilihan mask padat yang lossy. Fail mask bukan cutout transparen. `--inference-long-edge 1280` mengehadkan kos inference; komposit menggunakan footage asal pada resolusi output. Nisbah downsample automatik menyasarkan sisi dalaman kira-kira 480 px; override hanya selepas menguji shot sebenar. Kekalkan foreground asal untuk identiti/warna dan laras grading secara sengaja.

Latar boleh berupa gambar atau video setempat; video latar diulang apabila lebih pendek. Latar diisi dengan cover. Foreground lalai `contain`, mengekalkan seluruh bingkai dan muka; `--subject-fit cover` boleh crop dan mesti disemak pada shot sebenar. Nisbah piksel bukan 1:1 perlu dinormalisasi dahulu. Rotasi metadata 90/270 diambil kira sebelum ukuran mask; semak orientasi sebenar pada proof.

## Alpha transparen dan pencahayaan

```bash
# Omit --background untuk ProRes 4444 MOV dengan alpha:
python3 scripts/background_video.py render \
  --input /path/source.mp4 --mask /path/project/alpha.mkv \
  --output /path/project/person.mov --width 1080 --height 1920

# Grading dan rim pada siluet; padankan nilai kepada latar sebenar:
python3 scripts/background_video.py render \
  --input /path/source.mp4 --mask /path/project/alpha.mkv \
  --background /path/studio.mp4 --output /path/project/cinematic.mp4 \
  --contrast 1.025 --brightness -0.02 --saturation 0.9 \
  --rim-color 0xAC4EFF --rim-strength 0.2
```

MP4 H.264 tidak menyimpan alpha. Gunakan MOV alpha atau mask berasingan untuk compositing. Audio rakaman asal dibawa melalui julat masa yang sama dan dikod kepada codec output; jangan mendakwa bit-identical selepas encode. Untuk audio yang sudah dimix/disahkan, mux trek akhir secara berasingan tanpa had video yang boleh memotong paket akhir, kemudian semak sync, tempoh serta awal/akhir suara. `--no-audio` ialah pilihan sengaja.

## Props, rambut dan depth caption

Semak rambut, cermin mata, jari, baju cerah dan objek dipegang pada latar hitam/putih/latar akhir. Gunakan `--keep-mask /path/keep.png` untuk melindungi objek tertentu dan `--erase-mask /path/erase.png` untuk membuang kawasan tertentu; putih ialah kawasan terpakai. Mask dibaca pada orientasi sumber dan diskala bersama sumber. Erase menang jika bertindih. Mask statik hanya sesuai jika objek tidak berubah kedudukan; bagi objek bergerak, gunakan tracking/rotoscope atau pecahkan julat klip dengan mask yang disemak. Jangan isi seluruh torso secara membuta tuli untuk menutup kesilapan cawan/pakaian putih.

Untuk teks bergerak di belakang badan, susun latar → caption belakang → subjek dengan alpha → caption depan → URL/tajuk kekal. Simpan sprite teks yang sama ketika handoff; jangan render caption kedua dengan font/saiz berlainan. Rim hanya pada siluet; jangan menukar seluruh muka atau menambah halo putih tebal. Kekalkan wajah bersih dan semak semua laluan teks.

## QA dan cache

Helper menggunakan fail sementara dengan PID dan lock output supaya dua encoder tidak menulis fail yang sama. Jangan melancarkan pembaikan kedua ke output aktif. Metadata cache melibatkan sumber, model, FPS, julat, cut dan mask override. Matte lengkap yang serasi digunakan semula; gunakan `--force` hanya untuk membina semula. Render sedia ada memerlukan laluan baharu atau `--overwrite`.

`render` memeriksa frame count, PTS mula 0, sela FPS dan decode penuh, lalu menulis `.qa.json`. `PASS_MEDIA_ONLY` tidak meluluskan estetika atau mutu alpha. Sebelum master, render proof 3–5s dan shot sukar 6–12s; semak bingkai bersebelahan, awal/pertengahan/akhir, cut, held props, kontras, audio dan URL. Jangan mengatasi kegagalan cadence dengan mengubah laporan; baiki timebase/mux. Untuk repair packet timestamp, tetapkan `pts=PTS` secara eksplisit apabila menukar DTS menggunakan `setts`; lalai TS boleh menghilangkan composition offsets B-frame. Sahkan packet PTS dan decode sekali lagi.

## Ujian sebenar yang selesai

- Pemasangan dependency terasing daripada kosong berjaya; model 14,975,696 bait sepadan SHA-256 terpin, diikuti semakan offline `ready: true`.
- Fixture manusia dua saat, 24 fps → mask/MP4 30 fps (60 bingkai), reset tepat pada cut 1.0s, serta keep/erase mask diuji pada piksel sasaran. Cache serasi digunakan semula; cache offline kosong dan sumber tidak sepadan ditolak.
- Komposit latar gambar, latar video 0.5s yang diulang hingga 2s, grading/rim dan MOV ProRes alpha pada 480×854 lulus cadence, audio dua saat dan decode penuh.
- Forward test berasingan menghasilkan 1080×1920, 24 fps, 48 bingkai/2.0s; helmet dipegang dipulihkan dengan mask bersasar mengikut shot. Semua 95 payload paket AAC dan timestamp sumber kekal sama selepas mux berasingan. Sumber, output dan bingkai bersebelahan cut diperiksa; tiada dakwaan playback normal atau listening penuh.

Ujian pendek ini bukan bukti mutu semua video panjang atau semua props; tetap jalankan proof pada sumber pengguna.

## Sumber primer

- https://github.com/PeterL1n/RobustVideoMatting
- https://github.com/PeterL1n/RobustVideoMatting/blob/master/documentation/inference.md
- https://github.com/PeterL1n/RobustVideoMatting/releases/tag/v1.0.0
