# Pek komponen boleh guna semula untuk video

## Lokasi dan pengambilan

- Nama fail: `Komponen_Boleh_Guna_Semula_Skill_Video.zip`.
- Library file ID yang disahkan: `libfile_ba1a2dff2e4c8191a73d6fb6c65107e5`.
- Saiz versi asal: 4,435,395 bait; 234 fail sumber daripada 11 projek, bersama `README.md` dan `MANIFEST.json`.
- Gunakan skill Library apabila perlu mendapatkan fail. Cari nama tepat dengan `search_title_only=true`, pilih identiti yang sepadan, kemudian gunakan laluan muat turun yang ditetapkan skill Library. Jangan bergantung pada laluan scratch daripada sesi lama. Jika fail tiada, laporkan kekurangan sumber; jangan andaikan ZIP projek asal yang telah dipadam masih tersedia.
- Baca `README.md` dan `MANIFEST.json` selepas mendapatkan pek. Manifest merekodkan ZIP sumber, laluan asal, laluan yang disimpan, saiz dan SHA-256 setiap fail. Folder teratas menggunakan nama ZIP sumber tanpa `.zip`; laluan asal di dalamnya dikekalkan.

## Pilih komponen mengikut keperluan

| Folder sumber dalam pek | Komponen utama untuk diperiksa |
| --- | --- |
| `Dalam_Sunyi_Projek_Watercolor` | `sunyi_video/parallax.py`, `build_video.py`, `align_audio.py` dan `motion_presets/`: parallax, render, penjajaran audio dan preset. |
| `Projek_Seni_Langkah_Kecil` | `Seni_Langkah_Kecil/project/vector_scene.cjs`, `composite.py`, `export_video.py`, `align_subtitles.py`, `sync_caption_timeline.py` dan `presets/`: rig vektor, komposit dan caption. |
| `Mengenang_Tun_Siti_Hasmah_Projek` | `Hasmah_Memorial_Project/build_video.py`, `import_audio.py`, `prepare.py`, `repair_export.py` dan `motion_presets/`: render dan import audio. |
| `Projek-CME-Menegak` | `Projek-CME-Menegak/project/portrait/` mengandungi `vcore.py`, `scenes_a.py`–`scenes_c.py`, `render_vertical.py`, `make_captions.py` dan `finalize_vertical.py`: komposisi potret. |
| `Projek-CME-Slide-AI` | `Projek-CME-Slide-AI/render_promo.py`, `build_timeline.py`, `render_all.py`, `mix_audio.py`, `audio/soundtrack.py` dan `captions/`: promosi landscape, timing dan audio. |
| `projek_video_explainer_pastel_origami` | `render.py`, `render_rujukan.py`, `character3d.py`, `photoreal3d.py`, `render_avatar_demo.py` dan `project_config.json`: contoh explainer, watak dan avatar. |
| `Projek_Tutorial_NotebookLM_CME_BM` | `build_script.py`, `compose.py`, `render.py`, `transcribe.py` dan konfigurasi suara: komposisi tutorial. |
| `Projek_Voiceover_Tutorial` | `assemble_tutorial.py`, `production_settings.json` dan `narration.json`: assembly tutorial dan konfigurasi narasi. |
| `Projek_Seni_Menahan_Menghukum` | `animate.py`, `collect_audio.py`, `finish.py`, `script_segments.json` dan `voice_settings.json`: animasi, pengumpulan audio dan master. |
| `Projek_Hujan_Rindu_Mak_Abah` | `Hujan_Rindu_Mak_Abah_Google/produce.py` dan konfigurasi timeline/cerita: produksi naratif. |
| `Projek_Teluk_Cempedak_Landscape` | `Teluk_Cempedak_Landscape_Project/teluk_landscape.py`, `teluk_landscape_audio.py` dan `render_landscape.sh`: render landscape dan audio. |

## Adaptasi dan perlindungan

Gunakan pek sebagai kod contoh yang boleh diadaptasi. Video akhir, imej adegan, rakaman suara dan aset media projek asal tidak disertakan. Sesetengah JSON dan README masih mengandungi cerita atau laluan lama sebagai konteks contoh; bekalkan media baharu serta ubah nama fail, teks, cue, tempoh, fon dan dependensi yang diperlukan. Semak import, konfigurasi dan ketersediaan perender sebelum menjalankan skrip. Nama fail `3d` sahaja tidak membuktikan render 3D sebenar atau mutu yang telah diuji.

Utamakan komponen dan preset terkini yang telah dibundel bersama skill apabila fungsi sama tersedia. Gunakan pek tambahan untuk rujukan atau komponen yang belum dibundel; jangan menimpa toolkit induk secara automatik. Salin hanya komponen diperlukan ke ruang kerja projek, kekalkan lesen fon, render styleframe serta petikan gerak dan jalankan QA biasa skill. Padankan gaya kepada brief terbaru; jangan mewarisi cerita, harga atau suara contoh sebagai pilihan lalai.

Kekalkan pek ini apabila mengemas fail projek lama, kecuali pengguna secara jelas meminta pek komponen dipadam. Tiga skrip 8 Pintu Rezeki masih tersedia secara berasingan dan dalam `scripts/` skill; pek ini tidak menggantikannya.
