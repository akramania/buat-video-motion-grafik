# Komponen video terkunci dan cache guna semula

## Versi dan bahan yang wajib disimpan

Semakan sumber primer: **3 November 2026**. Gunakan `assets/runtime-lock.json` untuk versi binari, URL tepat, hash dan provenance; gunakan `assets/hyperframes/package-lock.json` untuk keseluruhan dependency npm. Manifest berat medium dan revision tepat berada dalam `assets/whisper/model-medium.json`; helper menggunakan revision terkunci apabila perlu memuat turun medium baharu dan mengekalkan model projek sedia ada. Semak keluaran stabil semasa melalui sumber rasmi apabila pengguna meminta update; uji dalam cache versi baharu sebelum mengganti cache projek aktif. Jangan resolusi `latest` ketika render.

| Komponen | Versi dalam toolkit ini | Simpan untuk penggunaan semula |
| --- | --- | --- |
| Node.js + npm | Node **26.13.0 LTS**, npm **11.20.0**; minimum toolkit **22.12.0** | Arkib Linux yang sepadan CPU/glibc, direktori penuh Node termasuk npm/npx, checksum rasmi dan lesen. Jangan simpan executable Node sahaja. |
| HyperFrames | **0.9.4** | `package.json`, lockfile, **node_modules lengkap** termasuk dependency transitif/native/optional platform, CLI tempatan dan cache npm untuk pemulihan offline. |
| GSAP | **3.15.0** | Library serta DrawSVGPlugin, MorphSVGPlugin, MotionPathPlugin dan SplitText daripada versi sama; vendor setempat dan lesen. Salinan vendor dalam template telah dikemas kini. |
| Chromium / Chrome | Chrome for Testing Stable **156.0.8078.80** | Arkib dan folder browser penuh termasuk resource/locale/helper executable; laluan executable, hash dan manifest keperluan library Linux. Kewujudan fail atau `--version` sahaja tidak membuktikan browser boleh dilancarkan. |
| FFmpeg + ffprobe | Stable upstream **9.0.2**; binari cache **n9.0.2-45-g1e65c6cd5d**, binaan BtbN bertarikh 2 Nov | Kedua-dua binari daripada binaan sama, konfigurasi codec/filter, arkib dan hash release. Ini binaan cabang 9.0 yang diselenggara, bukan tarball tag 9.0.2 tanpa patch. |
| Whisper | **faster-whisper 1.2.1**; upstream `openai-whisper` **20250625** sebagai rujukan, bukan backend tambahan wajib | Python/ABI yang sesuai, dependency terkunci dalam `assets/whisper/requirements.lock.txt`, wheelhouse, CTranslate2/PyAV, berat model lengkap, tokenizer/config/vocabulary, revision, hash dan lesen. Kekalkan model projek yang sudah disahkan; `medium` multilingual lalai produksi. |
| Three.js | **0.187.0** | Pakej penuh termasuk build, `examples/jsm`/addons yang diperlukan; aset model, tekstur, shader dan decoder yang benar-benar digunakan. Import ES module diutamakan. |
| React + React DOM | **19.3.1** untuk kedua-duanya | Kedua-dua pakej sepadan versi, JSX runtime, lockfile dan alat build yang diperlukan oleh projek. React sahaja bukan renderer MP4. |
| Remotion | **4.0.540** | `remotion`, `@remotion/cli`, `@remotion/renderer`, `@remotion/bundler` dan semua `@remotion/*` pada versi sama, binari compositor platform serta browser sebenar. Jangan mendakwa pemasangan membuktikan render berjaya. |

Whisper 1.2.1 masih keluaran terkini semasa semakan; tiada nombor versi baharu untuk dipaksakan. Kekalkan **av==16.1.0**: PyAV terkini yang diperhatikan ialah 19.0.2 tetapi rekod ujian skill mendapati API `metadata_errors` tidak serasi. Uji calon baharu dengan load/decode/transkripsi sebenar dalam cache berasingan sebelum mengubah pin. Jangan menggantikan model produksi dengan tiny untuk mendapatkan status lulus.

## Semak, pulihkan dan guna semula

Mulakan projek baharu dengan semakan tanpa muat turun:

```bash
python3 scripts/setup_video_components.py --offline --report /path/project/components-ready.json

# Jika ada komponen hilang/tidak sepadan, pulihkan komponen berkaitan sahaja.
python3 scripts/setup_video_components.py --install --report /path/project/components-ready.json

# Pemulihan offline daripada arkib berhash dan cache npm yang lengkap.
python3 scripts/setup_video_components.py --install --offline --report /path/project/components-ready.json

# Untuk tugas audio, tambah semakan model dan decode Whisper sebenar.
python3 scripts/setup_video_components.py --install --whisper --model medium --report /path/project/components-ready.json
```

Helper memulihkan binari yang hilang/rosak/berbeza versi, mengekalkan cache lama jika muat turun/hash/ekstrak gagal, menyemak npm dan ffprobe, menguji library Linux, melancarkan browser melalui preflight HyperFrames serta menguji import GSAP/Three/React/Remotion. Ia tidak memasang semula node_modules apabila pin dan cap lockfile sepadan. `--offline` melarang muat turun; `--install` membenarkan pemulihan. Gunakan `--cache-root`/`--runtime` untuk storan VM lain. Lock binari ini khusus Linux x64 glibc; sediakan lock dan ujian berasingan bagi ARM64/musl.

Cache binari lalai: `~/.cache/km-video-components/2026-11-03-linux-x64/`. Cache node_modules: `~/.cache/km-video-hyperframes/0.9.4/`. Cache Whisper: `MOTION_MEDIA_CACHE` atau `~/.cache/video-motion-media/`. Pakej besar, browser, node_modules dan berat model disimpan dalam cache runtime/pek sandaran, bukan dimasukkan ke Git skill. Simpan `downloads/`, lockfile, keseluruhan direktori runtime dan `runtime-env.json` semasa menyediakan pek guna semula. Mengemas kini arahan/lock skill tidak dengan sendirinya memuat naik pek ke Drive atau memasangnya dalam Gemini.

`run_hyperframes.mjs` membaca laluan Node/FFmpeg daripada `runtime-env.json` yang disediakan helper. Gunakan CLI setempat selepas persediaan; jangan memuat turun melalui `npx` ketika render. Jangan menimpa runtime projek aktif atau memulakan render pendua. Jika tiada komponen hilang, terus guna pemasangan tersebut.

## Chromium dan library Linux

Simpan output `ldd <browser-executable>`, distro, seni bina, versi glibc, manifest pakej (`dpkg-query` atau setara) dan pakej `.deb`/`.rpm` sepadan jika menyediakan sandaran offline. Kekalkan dependency transitif; arkib browser sahaja tidak mengandungi semua library sistem. Semak NSS/NSPR, ATK/AT-SPI, libcups, DRM/GBM, X11/XCB, xkbcommon, ALSA, Pango/Cairo, fon dan library lain yang dilaporkan `ldd` pada binaan sebenar. Jangan menyalin library sistem antara distro/ABI berbeza secara rawak.

Jika library tiada, pulihkan hanya pakej distro yang diperlukan ke lokasi disokong, kemudian ulang `ldd` dan pelancaran browser sebenar. Jika proses disekat oleh polisi persekitaran, simpan ralat tepat dan status `ready:false`; jangan cuba mengatasi polisi atau melabelnya masalah versi. Helper ini melaporkan library yang hilang; ia tidak mengubah sistem operasi secara automatik.

## Laluan render dan bukti siap

HyperFrames kekal lalai bagi HTML/GSAP/Three.js apabila pengguna memintanya. React boleh menyusun komponen/UI; Remotion ialah laluan tambahan berasaskan frame React. Gunakan `useCurrentFrame()`/`useVideoConfig()` dan state deterministik jika memilih Remotion. Jangan menjalankan ticker GSAP bebas di dalam render Remotion atau menukar renderer projek sambungan secara senyap. Semak syarat penggunaan Remotion bagi konteks pengguna apabila laluan itu dipilih; jangan mendakwa ia sentiasa percuma untuk semua organisasi.

Sebelum master, jalankan `doctor → lint → check → snapshot → proof 1–3s → render → QA` menggunakan CLI dan kontrak versi dipin. Uji Three.js WebGL sebenar jika digunakan, seek maju/mundur/reload, plugin GSAP, font, teks dan audio. Bagi Remotion, render komposisi pendek menggunakan browser setempat yang sama dan sahkan output dengan ffprobe serta nyahkod penuh FFmpeg. Import modul, React server markup dan matriks scene Three.js hanya ujian CPU, bukan bukti render browser.

`ready` memerlukan preflight browser; `all_components_ready` turut memerlukan Whisper diperiksa dan berjaya load/decode. Tanpa `--whisper`, laporan mesti menyatakan Whisper belum diperiksa. Simpan laporan sebenar, bukti frame/MP4 dan checksum bersama projek. Baca `assets/hyperframes/validation.json` untuk batasan ujian versi semasa. `assets/hyperframes/legacy/` menyimpan lock lama 0.8.185 untuk rollback yang disengajakan; ini bukan projek render lengkap dan bukan lalai terkini. Jika menggunakannya, pulihkan vendor GSAP 3.14.2 yang sepadan dan ulang QA.

## Sumber primer

- Node LTS/binary/npm: https://nodejs.org/dist/index.json
- HyperFrames: https://registry.npmjs.org/hyperframes/latest dan https://github.com/heygen-com/hyperframes
- GSAP: https://registry.npmjs.org/gsap/latest dan https://gsap.com/docs/v3/Installation/
- Chrome Stable: https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json
- FFmpeg: https://ffmpeg.org/releases/ dan https://github.com/BtbN/FFmpeg-Builds/releases/tag/autobuild-2026-11-02-12-51
- Whisper: https://pypi.org/pypi/faster-whisper/json dan https://github.com/SYSTRAN/faster-whisper
- Three.js: https://registry.npmjs.org/three/latest dan https://threejs.org/docs/
- React: https://registry.npmjs.org/react/latest dan https://react.dev/versions
- Remotion: https://registry.npmjs.org/remotion/latest dan https://www.remotion.dev/docs/renderer/ensure-browser
