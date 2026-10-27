# Preset Atlas tepat melalui Python

## Kandungan

1. Laluan wajib dan arahan pantas
2. Konfigurasi dan cue
3. Footage, alpha dan tracking
4. Padanan preview dan cache
5. Batas layout dan penyelenggaraan

## 1. Laluan wajib dan arahan pantas

Gunakan `scripts/atlas_preset.py` sebagai pintu masuk bagi preset Atlas dalam
suntingan video. Pembungkus memanggil fungsi Python asal; jangan tulis renderer
pengganti, menukar easing/mask atau memindahkannya ke GSAP berdasarkan nama.
Gunakan HTML/GSAP untuk animasi vektor/kartun mengikut aturan pemilihan enjin.

Dari akar skill, jalankan:

```bash
python3 scripts/atlas_preset.py list --search scroll
python3 scripts/atlas_preset.py describe CFX15
python3 scripts/atlas_preset.py init CFX15 --output /path/project/scroll.json
python3 scripts/atlas_preset.py check /path/project/scroll.json
python3 scripts/atlas_preset.py render /path/project/scroll.json --output /path/project/scroll.mp4
python3 scripts/atlas_preset.py verify /path/project/scroll.json --video /path/project/scroll.mp4 --report /path/project/scroll-qa.json
```

Gunakan laluan skill sebenar apabila cwd ialah folder projek. Toolkit eksport
Atlas menyimpan pembungkus pada `runtime/atlas_preset.py`, backend pada
`renderer/` dan job terkunci pada `jobs/`. `reference_jobs/` menyimpan job
yang sepadan dengan eksport preview katalog berlabel; sidecar preview
mengikat versi kod serta hash fail video/poster dan menghalang reuse lapuk.
Konfigurasi Atlas lama boleh diimport:

```bash
python3 scripts/atlas_preset.py import-config /path/project/CFX15.json --output /path/project/scroll.json
```

Import mengekalkan aset relatif kepada fail asal dan menukar cue lama sekali
sahaja. Ia menolak override dalaman yang berubah atau medan tidak disokong.
Jangan memadam medan rujukan atau membina job daripada ingatan; gunakan `init`
atau `import-config` supaya fingerprint kod/default sepadan.

## 2. Konfigurasi dan cue

Gunakan struktur job yang dijana: `schema_version`, `preset`, `mode`, `params`,
`output`, `cue_seconds`, `inputs`, `reference`. Baca `describe` bagi parameter
yang benar-benar dibuka oleh pembungkus. Registry meliputi semua 922 ID;
pilihan pengubahsuaian sengaja lebih sempit daripada semua dalaman backend.
Tambahkan sokongan baharu melalui perubahan kod yang disemak dan ujian,
bukan dengan memintas validator.

Letakkan teks/aset/warna dalam `params`. Letakkan `duration`, `fps`, `width`
dan `transparent` dalam `output`. Struktur gerakan, fungsi, fon induk dan
default sumber dikunci oleh `renderer/atlas_contract.json`.

**Semua cue baharu menggunakan saat output sebenar**, bukan jam 0–5:

- CFX15: `cue_seconds: {"line_cues":[0,2,4,6]}` untuk empat baris dalam lapan
  saat. Bilangan cue mesti sama dengan `params.lines` dan meningkat ketat.
- B05: `word_intervals` ialah senarai `{"start":0,"end":0.5}` bagi setiap
  perkataan dalam `params.text`; interval mesti tersusun dan tidak bertindih.
- B06: `character_pauses` ialah senarai
  `{"after_character":11,"duration":0.4}`; jumlah pause tertakluk pada bajet
  masa preset asal.
- CFX12: `freeze_at` ialah masa output sebenar bagi frame yang hendak dipegang.
- L01–L06: guna nama cue daripada `describe`; backend ini menerima saat
  sebenar dan tidak dinormal semula.

Pembungkus memetakan masa output kepada jam backend sekali sahaja. Jangan
mendarab cue dengan `5/duration` sebelum menyerahkannya kepada pembungkus.
Tempoh output dikuantisasi kepada bilangan frame; semak receipt bagi tempoh
sebenar. Layer render senyap; kekalkan dan campurkan audio asal dalam editor.

## 3. Footage, alpha dan tracking

`mode: native` menghasilkan preset asal, termasuk artwork demonstrasi jika
belum diganti melalui parameter yang disokong. Ia tidak menerima `inputs`
dan tidak mendakwa menggunakan footage pengguna.

Untuk CFX yang menyokong komposit, gunakan `mode: footage` dan sediakan:

```json
{
  "footage": {"path":"/path/project/source.mp4","start":2.5,"fit":"contain"},
  "subject": {"path":"/path/project/subject-alpha.mov","start":2.5,"fit":"contain"},
  "backdrop": {"path":"/path/project/background.png","fit":"contain"},
  "anchor_track": [{"time":0,"x":650,"y":300},{"time":2,"x":730,"y":310}]
}
```

Masukkan hanya input yang diperlukan. CFX15 pada footage tidak memerlukan
subject/backdrop; CFX dengan occlusion memerlukan alpha sebenar. Subjek RGB
atau alpha penuh legap ditolak. Sediakan alpha menggunakan aliran RVM yang
telah disahkan. CFX05 pada footage memerlukan anchor/track yang disemak;
tracking tidak diinfer oleh pembungkus. Koordinat ialah kanvas 1280×720.
Mode footage menggunakan `presentation: full` secara lalai supaya bingkai
katalog tidak mengecilkan footage atau memotong hujung klip.

Untuk editor Python sedia ada, import `AtlasPreset` dan `AtlasLibrary` dari
`scripts/atlas_preset.py`. Bina library sekali, bina sesi preset sekali bagi
job, kemudian panggil `session.frame(seconds, footage=rgba, subject=rgba,
backdrop=rgba, anchor=(x,y))` bagi setiap frame yang diperlukan. Input ialah
PIL RGBA yang telah disediakan. Komposit layer dengan Python dan campurkan
audio/enkod melalui FFmpeg. Jangan menulis semula pergerakan preset.

CLI menyahkod video secara berurutan dan mengekalkan seek deterministik;
imej statik dibaca sekali. CFX12 memegang frame sumber sebenar. CFX40
memetakan frame sumber melalui `clock_remap`, bukan menggerakkan imej statik.
Untuk kedua-dua preset ini melalui API editor, pilih frame pada
`session.source_seconds(t)` dan serahkan `footage_seconds` yang sama kepada
`frame()`; pembungkus menolak frame semasa yang disalah anggap sebagai freeze
atau speed ramp.
CFX20 memerlukan cache `echo_subjects` sebenar melalui API editor; jangan
mendakwa laluan CLI sudah menyediakan sejarah tersebut. CFX14 pada footage
ditolak sehingga adapter before/after sebenar disediakan; demo native kekal.
Sesetengah preset masih menggunakan elemen ilustrasi yang memang sebahagian
daripada reka bentuknya. Semak hasil pada footage; sediakan imej projek bagi
slot media yang diwajibkan dan jangan menganggapnya tracker/3D automatik.

## 4. Padanan preview dan cache

Pembungkus mengesahkan hash kod, JSON/data geografi dan empat fon; registry
serta default preset turut dikunci. Sebelum preset digunakan buat kali
pertama dalam sesi, tiga frame native dibandingkan secara tepat dengan
baseline yang dihantar. Perubahan dependency/fon yang mengubah piksel akan
menghasilkan ralat, bukannya kelulusan palsu.

`verify` menyahkod seluruh MP4 dan membandingkan enam sampel frame mengikut
indeks tepat dengan renderer. Perbezaan codec dibenarkan pada ambang ralat
purata piksel lima; ini bukan skor estetika atau jaminan semua frame identik.
Semak playback, entrance/hold/exit, ejaan, overlap dan pemasaan audio secara
berasingan selepas menukar teks/aset atau memasukkan footage.

Untuk mengesahkan **MP4 Atlas yang diterbitkan**, gunakan video sebenar serta
job yang sepadan dengan dimensi, fps, tempoh, kandungan dan tetapan preview:

```bash
python3 scripts/atlas_preset.py verify /path/project/reference-job.json --video /path/project/atlas-preview.mp4 --reference --report /path/project/reference-qa.json
```

Jangan mendakwa preview laman semasa telah disahkan hanya kerana baseline
Python lulus. Untuk preview lama berlabel katalog, tetapkan
`output.catalogue_labels: true` serta dimensi/fps/tempoh yang sepadan
(pembina katalog asal menggunakan 1280×720/60fps). Preview CFX di laman
mungkin menggunakan eksport clean 960×540/30fps. Gunakan metadata video
sebenar; jangan menutup ketidakpadanan dengan menaikkan ambang.

Cache lalai berada pada cache runtime pengguna; `--cache /path/cache`
menukar lokasi. Kunci cache meliputi konfigurasi, versi wrapper/backend,
dependency, FFmpeg dan hash kandungan aset. Perubahan input menghasilkan
kunci baharu. Hash fail cache turut disemak sebelum digunakan semula.
Receipt `<output>.atlas.json` merekod ID, cap jari, aset, dimensi, frame,
status decode dan cache hit. Receipt tidak menggantikan semakan visual.

## 5. Batas layout dan penyelenggaraan

Semua preset asal menggunakan kanvas 1280×720. Eksport boleh diskala secara
berkadar; eksport besar tidak menambah perincian vektor. Jangan mendakwa
native 9:16 tersedia. `output.height` yang mengubah nisbah ditolak. Untuk
video menegak, letakkan layer 16:9 secara berkadar dalam ruang yang dirancang
atau bina dan uji varian portrait berasingan; jangan crop/reka semula secara
senyap sambil mendakwa preset asal yang sama.

Jangan jana semula lock untuk mengatasi ralat biasa. Selepas perubahan
backend yang disengajakan, semak kod, jalankan
`python3 scripts/build_atlas_contract.py --goldens all`, kemudian
`python3 scripts/test_atlas_preset.py --all` dan semak proof video. Ini
penyelenggaraan implementasi, bukan langkah bagi setiap projek pengguna.
Baseline baharu mengesahkan implementasi baharu; ia tidak membuktikan
padanan dengan preview lama yang telah diterbitkan.
