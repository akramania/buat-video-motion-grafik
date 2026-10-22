# Bank 20 watak V3: 42 pose dan 34 gerakan

## Kandungan

- Identiti dan sudut
- Cari, render dan salin
- Gerakan tambahan V3
- Kamera, skala dan alpha
- Pek penuh lama dan sumber kemas kini
- Semakan produksi

## Identiti dan sudut

Gunakan `assets/character_bank_20/source/characters.json` untuk 10 lelaki dan 10 perempuan rekaan: dua kanak-kanak, dua remaja, empat dewasa dan dua warga emas bagi setiap jantina. Kekalkan ID L01–L10 dan P01–P10, rupa, pakaian, palet, personaliti dan `height_cm`. P02/P04/P05/P07/P08/P10 bertudung; P01/P03/P06/P09 tanpa tudung. Semua pakaian panjang, longgar dan legap.

Gunakan enam view: `front`, `back`, `side_right`, `side_left`, `three_quarter_right`, `three_quarter_left`. `side` dan `three_quarter` ialah alias kanan. Pandangan belakang menggunakan artwork belakang tanpa mata/mulut, butang atau poket hadapan. Pandangan kiri ialah pantulan seluruh tubuh, kepala, pakaian dan props. Untuk objek bertulis atau ciri pakaian yang khusus kiri/kanan anatomi, bina overlay berasingan; jangan memantulkan perkataannya.

Buka `assets/character_bank_20/Galeri_Pose_Gerakan.html`: semua 20 watak, 42 pose dan 34 aksi boleh dipratonton sebagai SVG langsung. Butang Simpan SVG mengeksport pose/frame semasa. Pautan PNG/MP4/JSON memerlukan cache yang berkaitan; pratonton langsung tidak memerlukan cache.

## Cari, render dan salin

Jalankan dari root skill. Salin komponen ke workspace projek untuk perubahan artwork/timeline; kekalkan induk. Python `list`/`copy` membaca roster dan registry. Render SVG memerlukan Node.js; PNG/MP4 memerlukan `sharp` sebenar; MP4 memerlukan FFmpeg dengan libx264. Gunakan dependency runtime atau projek setempat. Jangan salin shim `node_modules/sharp` daripada pek masuk sebagai pengganti native: shim itu meratakan gradasi SVG dan hanya melaksanakan sebahagian API.

```bash
python3 scripts/character_bank.py list --kind poses
python3 scripts/character_bank.py list --kind motions
python3 scripts/character_bank.py list --sex female --hijab yes
python3 scripts/character_bank.py render --character P05 --pose stand_back --output /tmp/nadia_back.svg
python3 scripts/character_bank.py render --character L05 --motion walk_side_left --width 720 --height 1200 --fps 30 --output /tmp/amir_walk_left.mp4
python3 scripts/character_bank.py render --character P04 --motion turn_back_to_front --frames /tmp/mira_frames --fps 30
```

Gunakan `--view` untuk memaksa satu orientasi; biarkan pilihan itu kosong untuk aksi bertukar view. `--duration` menetapkan jendela masa render, bukan retiming automatik. `copy --character <ID> --kind pose|motion --id <ID_ASET> --output <fail>` menggunakan cache jika ada, atau merender SVG/PNG/MP4 yang belum ada ke output projek. JSON cache boleh didapati daripada pek atau eksport baharu.

API: `poseState(id, character)` atau `sampleMotion(id, tSeconds, character, {loop:false})`, kemudian `rigSvg(character, state, options)`. Dapatkan tempoh melalui `durationForCharacter` kerana adaptasi umur. Gunakan `t = frame/fps`, bukan wall clock. `rigGeometry` memberikan landmark/bounds yang sudah mengambil kira pantulan dan unjuran; kawalan anggota kekal dalam ruang authored. Fail `.js` hanyalah alias kepada modul `.cjs` yang sama.

Untuk mengeksport semua aset V3, salin folder bank ke workspace projek dan jalankan `node source/export_motion_bank.cjs`. `--skip-clips` menghasilkan 840 SVG + 840 PNG pose dan 680 resipi JSON; tanpa flag itu ia turut merender 680 MP4. Galeri boleh dibina semula melalui `python3 source/build_motion_gallery.py --root <folder_bank>`. Render pilihan projek dahulu sebelum eksport pukal.

## Gerakan tambahan V3

Sepuluh pose tambahan: `stand_back`, `look_sky_back`, `walk_side_right`, `walk_side_left`, `sit_side_eat`, `call_phone_left`, `dua_stand`, `dua_sit`, `touch_lanyard`, `wipe_tear`.

Sepuluh gerakan tambahan: `turn_back_to_front`, `turn_left_to_right`, `walk_side_right`, `walk_side_left`, `sigh_tired`, `wipe_tears_sleeve`, `sit_eat_drink`, `dua_khusyuk`, `call_phone_converse`, `ride_motorcycle`. Meja/kerusi, makanan/minuman, telefon dan motosikal menggunakan prop prosedur. Gunakan ekspresi, genggaman, air mata dan bukaan mulut mengikut cerita. Aksi telefon tidak mengandungi audio, dan mulut demo tidak diselaraskan kepada fonem; cue daripada audio akhir diperlukan bagi dialog sebenar.

Dua aksi turn menggunakan beberapa orientasi artwork 2D dengan unjuran mendatar mengecil pada pertukaran, bukan morph 360° atau simulasi 3D. Aksi motor ialah pose menunggang dengan roda berputar dan gegaran kecil; compositor projek perlu menambah laluan dunia, latar/parallax dan bunyi. Pose doa ialah gestur ilustrasi, bukan demonstrasi lengkap urutan solat/tahiyyat. Aksi duduk/berjalan mempunyai permukaan sokongan tersendiri; jangan menyambung dua klip bebas tanpa menyelaraskan anchor dan kontak.

## Kamera, skala dan alpha

Gunakan satu viewBox sepanjang shot dan padankan skala dunia menggunakan `height_cm` serta tinggi watak berdiri. Fail cache mempunyai `view_box` yang dipadatkan bagi setiap aksi supaya tangan/prop tidak terpotong. Jangan fit setiap pose kepada kotak tinggi yang sama ketika menyambung aksi; pulangkan koordinat cache kepada unit authored atau render semula dengan viewBox bersama.

Gunakan SVG atau frame PNG untuk alpha. MP4 H.264 ialah pratonton berlatar warna pepejal; render semula daripada vektor pada resolusi master. `walk_side_left`/`walk_side_right` ialah loop berjalan setempat yang menghadap kiri/kanan. Untuk perjalanan melintasi skrin, pilih `walk_across` dengan `--view side_left` atau `--view side_right`. Walk in place menggunakan lantai treadmill; walk across memerlukan pemetaan stance foot pada world space. Gerakan kamera atau retiming tidak boleh menyebabkan kaki tergelincir. Baca `references/vector-camera-engine.md` untuk kamera/IK Python tambahan.

## Pek penuh lama dan sumber kemas kini

Pek cache V2: `Bank_Watak_20_Pose_Gerakan.zip`, Library ID `libfile_cdde403409e08191afea70c144ce6ca7`, 47,029,479 bait, SHA-256 `a8c9be7a08a6beafa8b8f37b6a077994b92543e57e312bc7fb4560eea42e3f10`. Ia mengandungi 640 pose SVG/PNG, 480 klip MP4, resipi dan PDF bible bagi versi 32/24. Gunakan skill Library semasa untuk materialize ke workspace projek, root arkib `Bank_Watak_20/`. Jangan ekstrak source V2 menimpa source V3; ambil hanya cache yang sesuai. `full_bank_package.json`, `motion_bank_manifest.json` dan `validation.json` lama merujuk pek V2 tersebut.

Tiga ZIP kemas kini V3 asal serta identiti Library/hash disenaraikan dalam `source_packages_v3.json`. Source yang dipasang telah disesuaikan untuk Work/Codex. `SKILL.md` Gemini di dalam pek ialah rujukan adaptasi, bukan pengganti nama skill ini. Registry semasa disimpan di `source/motion_catalog.json`; semakan V3 tersimpan di `validation_v3.json`. Tiada dakwaan semua 840/680 aset V3 sudah dieksport.

## Semakan produksi

Render pose mula/tengah/akhir serta petikan 3–5 saat pada resolusi projek. Semak bahu/siku/pergelangan, tangan menyentuh prop, pakaian legap, kasut/lantai, sudut wajah dan tubuh serta safe area. Semak frame bersebelahan dan playback; metadata sahaja tidak membuktikan gerakan natural. Untuk wajah/tangan dekat kamera atau interaksi kompleks, sesuaikan artwork dan kontak; rig ini ialah 2D berartikulasi, bukan model 3D atau motion capture.
