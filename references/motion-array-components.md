# 2,000 komponen gerak Motion Array

Gunakan `assets/motion_array/index.json` untuk MA0001–MA2000. Empat kumpulan masing-masing 500: bentuk/anak panah, HUD/data, transition/liquid/asap dan partikel/cahaya. 100 keluarga reka bentuk mempunyai 20 adaptasi struktur setiap satu, dengan perubahan geometri, topologi, laluan atau susunan; bukan variasi warna sahaja.

Preview sebenar Motion Array diperiksa melalui frame berurutan dan timestamp; `assets/motion_array/evidence.json` mengandungi 100 pemerhatian daripada 14 sumber yang digunakan. 16 preview ditinjau. Setiap resipi mempunyai `source_ids`, `observation_ids`, `variant_basis` dan parameter. Jangan laporkan 2,000 fail sumber atau mendakwa setiap pergerakan sumber telah disalin tepat. Fail yang disertakan ialah implementasi vektor asli.

## Gunakan dan render

Cari komponen melalui `python scripts/motion_asset.py --search ring --group hud`. Salin resipi atau render pada 1920×1080 melalui `python scripts/motion_asset.py --id MA0508 --output scene.mp4`. Enjin vektor portable eksport `records()`, `render()` dan `compose()`; CLI menggunakan Node, Sharp dan FFmpeg. Pasang Sharp jika runtime tidak menyediakannya.

Jalankan terus: `node assets/motion_array/render_motion.mjs --id MA0508 --width 1920 --height 1080 --fps 30 --output component.mp4`. Untuk alpha, gunakan `--alpha --output component.mov` (ProRes 4444) atau `--png-sequence --output png-frames` bagi PNG transparent. MP4 preview Atlas ialah 320×180/24fps/3s pada latar gelap; ia bukan video alpha. Geometri boleh dirender semula pada resolusi projek. SVG statik daripada kad ialah satu frame; gerak sebenar dihasilkan oleh enjin.

Salin resipi dengan `python scripts/motion_asset.py --id MA0001 --copy component.json`, sunting medan `parameters` yang diketahui, kemudian render melalui `--recipe component.json --output custom.mp4`. Nilai struktur dan susun atur disahkan oleh `customize()`. Layer scene juga boleh membawa objek `parameters`; transform layer kekal berasingan.

## Banyak komponen dalam satu scene

Gunakan `scene-example.json` sebagai contoh 16 layer serentak. Setiap layer mempunyai `id,x,y,scale,start,duration,opacity`, dan `duration` scene mengawal panjang output. Koordinat asas 640×360; `scale=1` ialah saiz penuh. Susun foreground, focal object dan ambience dengan hierarchy yang jelas. Jangan jadikan scene sekadar grid kad.

Render: `node assets/motion_array/render_motion.mjs --scene assets/motion_array/scene-example.json --output showcase.mp4`. ID gradient/clip dinamespace bagi setiap layer untuk mengelakkan pertembungan. Tempoh layer memetakan gerak enter/active/exit 3s kepada tempoh layer projek. Untuk beat atau subaksi, pecahkan layer kepada beberapa cue dengan start berbeza.

Rekod semua MA IDs, observation IDs, timing dan perubahan parameter dalam manifest projek. Semak video akhir pada saiz paparan, alpha, cropping, susunan layer dan kelancaran. Kekalkan tapisan tema pengguna. Media sumber Motion Array digunakan untuk pemerhatian sahaja dan tidak disertakan dalam skill/Atlas.
