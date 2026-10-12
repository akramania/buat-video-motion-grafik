# 600 aset vlogging dan montaj

Gunakan aset asal di `assets/vlog_montage/` untuk projek vlog, travel, lifestyle, recap, cinematic montage atau video promosi. Koleksi VL menambah 600 aset sebenar kepada 1,500 SVG terdahulu; registry preset gerak kekal 842. Semua VL ialah karya asal, bukan muat turun template atau stock Envato.

| ID | Bilangan | Format dan penggunaan |
|---|---:|---|
| VL0001–VL0100 | 100 | LUT `.cube` 33³; creative look untuk RGB SDR Rec.709 |
| VL0101–VL0200 | 100 | Definisi JSON dan matte MP4; putih mendedahkan B, hitam mengekalkan A |
| VL0201–VL0300 | 100 | Overlay MP4 + definisi JSON; gunakan Screen di atas footage |
| VL0301–VL0400 | 100 | Grafik vlog SVG transparent, layer boleh disunting |
| VL0401–VL0500 | 100 | Grafik montaj SVG transparent, bukaan frame kekal telus |
| VL0501–VL0600 | 100 | SFX sintesis asli WAV 48 kHz, 16-bit stereo |

Cari melalui `scripts/vlog_asset.py`; indeks `index_*.json` menyimpan kategori, tags, kegunaan dan fail sebenar. Rekod `vlog_asset_ids`, laluan, intensity/opacity, masa mula serta masa akhir dalam manifest projek. Salin aset yang dipilih ke projek, kekalkan fail induk dan lesen.

Fail sumber tersedia secara automatik apabila CLI menyalin atau merender aset kali pertama. Gunakan `python scripts/vlog_asset.py --prepare` jika mahu menyediakan semua fail dahulu. Persediaan mengesahkan checksum sebelum memasang fail asal; kesemua LUT kekal 33³ dan byte-identical dengan sumber. Indeks boleh dicari tanpa menyediakan semua fail.

```bash
python scripts/vlog_asset.py --type lut --search travel
python scripts/vlog_asset.py --type transition --limit 0
python scripts/vlog_asset.py --id VL0001 --copy-to project/assets
python scripts/vlog_asset.py --id VL0001 --input shot.mp4 --strength 0.65 --render graded.mp4
python scripts/vlog_asset.py --id VL0101 --input shot-a.mp4 --input-b shot-b.mp4 --duration 0.8 --render reveal.mp4
python scripts/vlog_asset.py --id VL0201 --input shot.mp4 --strength 0.3 --render overlay.mp4
python scripts/vlog_asset.py --id VL0301 --input shot.mp4 --animate --render vlog-graphic.mp4
python scripts/vlog_asset.py --id VL0401 --input shot.mp4 --render montage-frame.mp4
python scripts/vlog_asset.py --id VL0501 --input shot.mp4 --strength 0.35 --render whoosh.mp4
```

Gunakan Python 3.10+, FFmpeg/ffprobe dengan libx264, NumPy dan Pillow; tambah CairoSVG bagi komposisi SVG. Jalankan arahan dari akar skill atau toolkit. `--copy-to` menyalin fail utama serta pasangan JSON/matte tanpa menukar format. `--render` mengaplikasikan aset kepada footage tempatan dan mengeksport MP4 SDR. `--width` menukar resolusi dengan nisbah clip A dikekalkan; `--fps` lalai 30. Tempoh lalai ialah tempoh footage bagi efek satu clip dan tempoh metadata bagi transition.

Normalisasikan footage kamera Log atau HDR kepada SDR Rec.709 menggunakan transform kamera yang betul sebelum LUT kreatif; koleksi ini tidak menyediakan transform Log/HDR. Semak white balance, exposure, warna kulit, highlight dan intensity pada shot sebenar. Pratonton LUT ialah ilustrasi/chart asal, bukan bukti ketepatan kamera tertentu.

Transition VL ialah spatial reveal, bukan simulasi kamera atau motion blur. Preview matte 640×360/30fps dimampatkan H.264; gunakan `transition_engine.mask_frame(recipe, normalized_t, width, height)` bagi mask analitik pada resolusi akhir. CLI merender satu segmen A→B yang senyap daripada permulaan kedua-dua clip; trim bahan kepada titik potongan dahulu, kemudian susun segmen bersama timeline dan audio projek. `--strength` tidak mengubah endpoint transition.

Overlay sumber 640×360/24fps, dua saat, latar hitam dan Screen; latar hitam bukan alpha terbenam. Enjin prosedural `overlay_engine.frame(recipe, seconds, width, height)` boleh menjana resolusi akhir. CLI mengulang hanya overlay berlabel `loopable`; yang lain tamat selepas tempoh sumber. Kurangkan strength lazimnya 0.15–0.65 supaya subjek dan teks kekal jelas. Grain Screen menaikkan luminance; jangan anggap ia grain subtractive yang neutral.

Grafik SVG kekal boleh disunting, dengan layer dan ruang footage. CLI mengekalkan nisbah artwork 16:9 dan meletakkannya di tengah clip; `--animate` menambah fade masuk/keluar sahaja. Untuk lower third, lokasi atau layout portrait khusus, sunting SVG dan bina choreography group pada timeline projek. Jangan anggap semua label demo automatik bertukar menjadi teks pengguna.

CLI mengekalkan trek audio pertama bagi LUT/overlay/grafik. SFX bermula pada saat sifar; trim atau jadualkan fail WAV pada event sebenar dalam timeline, dengar dengan narasi/muzik, kemudian semak aras campuran. CLI menggabungkan audio dengan limiter untuk mengelakkan clipping digital; ini bukan mastering automatik. Fail SFX ialah efek ringkas, bukan lagu atau ambience rakaman.

Semak alpha, crop, teks dan ruang selamat bagi grafik; gerak sebenar dan endpoint bagi transition/overlay; serta bunyi pada kelajuan biasa sebelum eksport penuh. Atlas menyediakan 600 kad, pratonton, audio player, salin arahan, fail individu atau pek pasangan dan sembilan pek muat turun yang meliputi semua 600 ID. Empat pek LUT masing-masing 25 aset; lima pek lain masing-masing 100 aset. Bagi toolkit, ekstrak pek yang dipilih ke akar Toolkit yang sama dengan struktur `assets/vlog_montage/` dikekalkan.
