# Rig kartun, props ibadah dan sari kata penuh

## Sambungkan tubuh sebelum menambah kesan

- Parent pelvis → torso → bahu/lengan → leher → kepala. Gunakan transform torso yang sama untuk baju, bahu dan leher; putaran kepala tambahan mesti berpivot di dalam sambungan leher. Jangan memutar baju sahaja sedangkan kepala dan lengan kekal pada koordinat lain.
- Bina overlap sebenar pada kepala/leher serta leher/kolar. Periksa pose paling ekstrem, gerak idle, langkah, tunduk, membaca, solat dan berdoa. Overlap numerik tidak menggantikan pemeriksaan siluet dan lapisan depan/belakang.
- Gunakan IK dengan panjang tulang tetap, stance terkunci dan swing berterusan. Hubungkan kaki, perjalanan dunia dan kamera melalui jarak/fasa yang sama. Perlahankan cadence secara sederhana; jangan menukar berjalan menjadi pose statik yang meluncur.
- Untuk naratif tenang, kecilkan bob, breathing dan goyangan sekunder. Kekalkan gerak artikulasi sebenar serta nilai dan kelajuan berterusan pada sempadan loop. FPS tinggi sahaja tidak membaiki rig.

## Props ibadah dan sokongan fizikal

- Tanggalkan kasut bagi watak yang berdiri di atas sejadah. Letakkan kasut di luar sempadan sejadah; periksa kedua-dua pose solat dan berdoa serta keseluruhan laluan kaki.
- Letakkan mushaf di atas meja, rak atau rehal yang jelas tinggi dari lantai. Semasa membaca, pastikan bawah buku menyentuh permukaan sokongan; elakkan buku terapung, diletakkan di lantai atau ditenggelamkan dalam paha.
- Parent buku dan perabot sokongan pada lapisan kamera yang sama. Jangan menggerakkan mushaf bersama breathing watak jika ia sedang diletakkan di atas meja. Semak bayang sentuhan dan kaki perabot.

## Parallax yang mempunyai kedalaman

- Pisahkan cahaya/langit, awan, bukit jauh, bukit tengah, bukit dekat, pokok dan tanah. Dalam bilik, pisahkan pemandangan tingkap, bingkai/langsir, perabot bersama watak dan tumbuhan depan; clip pemandangan pada bukaan tingkap.
- Gunakan kadar jarak berbeza. Proof ini menggunakan sun 0.012, clouds 0.025, hills 0.075/0.18/0.31, trees 0.67 dan ground 1. Ini nisbah permulaan, bukan nilai wajib.
- Kekalkan identiti objek berulang berdasarkan indeks dunia. Kamera menjejak boleh mengurangkan hanyutan subjek, tetapi titik kaki stance dan penanda tanah mesti berkongsi transform dunia yang konsisten.

## Dialog penuh dan caption kinetik

- Ikut permintaan terbaru tentang kedudukan. Apabila diminta dialog penuh di bawah, paparkan semua perkataan yang benar-benar dinarasikan, termasuk doa dan penutup. Jangan memaparkan seluruh bahan sumber panjang jika hanya skrip olahan ringkas yang dibaca.
- Kekalkan preset kinetik sebagai inti mesej dan sediakan lapisan sari kata berasingan di bawah. Simpan cue serta eksport SRT. Jangan menggantikan dialog penuh dengan ringkasan tajuk.
- Selaraskan dengan audio sebenar. Gunakan transkrip/forced alignment apabila tersedia; jika tiada, padankan frasa dengan jeda akustik yang diukur, semak padanan teks penuh dan nyatakan batas kaedah. Jangan mendakwa kiraan perkataan atau waveform sahaja membuktikan sebutan dan timing setiap perkataan.
- Ukur fon sebenar dan hadkan kepada dua baris yang stabil. Proof landscape 1920×1080 menggunakan DejaVu Sans 46 px, panel kontras, margin bawah 30 px dan artwork sehingga kira-kira y921. Sesuaikan nisbah, panjang frasa dan ruang telefon; jangan mengecilkan teks tanpa had.
- Tetapkan ruang selamat bagi keseluruhan gerak watak, parallax dan overshoot teks. Selepas membaiki rig, semak semula laluan kepala kerana kedudukan baharu boleh bertembung dengan tajuk. Alihkan atau susun semula tajuk sebelum merender.
- Sambungkan jam preset in/hold/out dengan nilai dan terbitan yang sama, contohnya interpolasi Hermite. Uji monotonicity serta sempadan; elakkan lonjakan masa reka bentuk yang membuat huruf tersentak ketika bertukar fasa.
- Untuk revisi visual, kekalkan audio diluluskan. Gunakan stream copy apabila serasi dan sahkan payload audio atau PCM terdekod sepadan. Jangan menjana suara baharu atau memecutkannya untuk muat caption.

## Komponen original dan bukti

`scripts/vector_small_steps.cjs` ialah SVG/Sharp renderer daripada projek ini. Ia mengekalkan 15 scene sebagai proof berasingan, bukan preset baharu dalam atlas dan bukan templat generik. Export `actor`, `actorState`, `walkState`, `ik`, `defs`, `palette`, `hills`, `outdoors` dan `room` boleh diadaptasi. Tukar teks, sumber agama dan props apabila menukar cerita. Renderer ini tiada audio atau sari kata.

```bash
node scripts/vector_small_steps.cjs --audit
node scripts/vector_small_steps.cjs reading 4 60 1280 reading.png 2
node scripts/vector_small_steps.cjs walk 4 60 1280 > walk.rgb
ffmpeg -f rawvideo -pix_fmt rgb24 -s 1280x720 -r 60 -i walk.rgb -c:v libx264 -pix_fmt yuv420p walk.mp4
```

Semak Node, Sharp dan FFmpeg sebelum render. Salin komponen ke projek dan adaptasi di situ; jangan menulis output/cache ke dalam skill. Audit CLI menyemak geometri beberapa pose, overlap leher dan cycle berjalan; ia tidak mengesahkan keseluruhan anatomi atau mutu estetik.

Proof penuh yang disiapkan: 116.133 s, 1920×1080, 60 fps, 15 babak, 20 preset K sebenar dan 31 cue sari kata meliputi 211 perkataan narasi. Audio asal sepadan selepas revisi. Pemeriksaan projek merangkumi 2889 sampel pose, 961 sampel cycle, overlap kepala/leher minimum 7.26 unit reka bentuk serta buku di atas meja. Nilai ini milik proof tersebut, bukan jaminan semua adaptasi.

Periksa frame sebenar MP4 untuk semua dialog, pose, pembukaan/penutup serta frame bersebelahan di toe-off, landing dan wrap. Periksa playback biasa dan dengar jika kemampuan tersedia. Jika tidak, catat batas itu dan jangan menyamakan contact sheet/audit numerik dengan pemeriksaan audiovisual masa nyata. Hentikan ujian tambahan setelah risiko perubahan disahkan.
