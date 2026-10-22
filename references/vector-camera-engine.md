# Kamera vektor dan IK Python

Gunakan `scripts/vector_character_camera.py` sebagai komponen Pillow/NumPy untuk kamera 2D/2.5D, bukan mesh 3D. `CamCanvas(image, cx, cy, zoom)` memetakan world space ke screen space; geometri, ketebalan garisan dan fon diskalakan semasa melukis pada kanvas sasaran. Zoom semula geometri, bukan membesarkan PNG kecil. `solve_ik` memilih calon siku lebih rendah untuk mod elbow dan calon lutut mengikut arah `f_dir` untuk mod knee; ini heuristik dua tulang, bukan solver sendi/fizik manusia penuh.

```bash
python3 scripts/vector_character_camera.py --frame --time 1 --width 1280 --height 720 --output /tmp/camera.png
python3 scripts/vector_character_camera.py --demo --duration 4 --fps 30 --width 1280 --height 720 --output /tmp/camera.mp4
```

Demo senyap memerlukan Python, NumPy, Pillow, fon DejaVu setempat dan FFmpeg bagi MP4; ia tidak memerlukan audio, akaun luar atau fail projek lama. Import tidak membaca RMS atau mencipta folder output. `draw_character` di fail ini menggunakan role contoh `amir`, `mak`, `abah`; ia tidak memuatkan 20 ID L/P secara automatik. Untuk bank 20 watak, gunakan perender SVG bank. Jangan menyamakan role contoh Amir dengan identiti L05 secara automatik.

Bina foreground/midground/background, pilih target kamera dari landmark atau bounds objek dan interpolasi center/zoom dengan easing. Kekalkan subtitle, logo dan UI dalam screen space. Uji close-up wajah/tangan dan alihkan perhatian sebelum zoom, bukan memotong subjek sewaktu masih bergerak. Palet krim dan prop demo boleh diubah mengikut brief.

Fail ini turut mengekalkan contoh 16 scene asal Seni Mengira Cukup sebagai projek pilihan. `--test-styleframes` dan `--render-full` memerlukan `--project-dir`, `--intermediate-dir` dan `--out-dir` secara eksplisit. Project-dir perlu `fonts.json` dengan `sans`, `bold`, `arabic` (laluan setempat), dan intermediate-dir perlu `vo_norm_rms_30fps.npy` yang sah. `--render-full` juga memerlukan `master_audio.wav`. Subtitle, dialog, ayat/hadis, timing, role dan susun atur asal ialah contoh khusus projek; ubah serta semak sumber agama, shaping Arab dan audio sebenar sebelum digunakan pada topik lain. Mode asal menggunakan timeline RMS 30 fps. Tiada fail audio/projek lama dibekalkan oleh ZIP ini.

Arahan tiada kinetic typography dan subtitle penuh di bawah dalam contoh itu hanya digunakan apabila diminta pengguna. Ia tidak mengubah semua video promosi, Atlas, caption tengah atau pilihan suara sedia ada. Gunakan frame deterministik, output atomik, streaming ke FFmpeg dan semak nyahkod penuh selepas render.
