# Sambungan siri ceramah dengan checkpoint

Gunakan aliran ini untuk episod bersiri seperti Arbain Ghazali. Ikut arahan projek terkini, sumber yang dibenarkan dan nombor episod yang diminta. Jangan render semula episod yang sudah selesai.

## Mulakan daripada keadaan sah

Periksa checkpoint, proses yang masih berjalan, lock dan resit upload dahulu. Guna semula transkripsi lengkap yang sepadan dengan identiti sumber. Jangan jalankan model atau audit berat kedua jika kerja sah masih berjalan atau sudah lulus dan input tidak berubah.

Checkpoint Arbain terakhir yang diketahui: `Arbain_Episod_23_Checkpoint.zip`, Library ID `libfile_f115906719d0819194714e70171a36ea`; ambil versi terkini melalui Library. Checkpoint 21–22: `libfile_acb987423c108191bd0344737ccd979e`. Gunakan checkpoint baharu yang lebih lengkap jika wujud. Jangan anggap path scratch atau cache model lama masih tersedia.

Guna semula kod renderer, fon, gaya dan kaedah analisis. Setiap sumber baharu mesti mempunyai transkrip, terjemahan, peta kamera, trim dan resitnya sendiri. Cluster ID, masa potongan dan indeks Quran episod lama tidak boleh diwarisi.

## Sediakan projek tanpa menyalin isi episod

Jalankan dari direktori skill, dengan sumber dan checkpoint yang telah tersedia:

```bash
python scripts/prepare_lecture_episode.py init \
  --project /workspace/scratch/arbain_ep24 \
  --source /workspace/scratch/source_ep24.mp4 \
  --checkpoint /workspace/scratch/Arbain_Episod_23_Checkpoint.zip \
  --episode 24 --template-episode 23 \
  --title "ARBA'IN IMAM GHAZALI 24" \
  --speaker "Nama penceramah yang disahkan" \
  --asr-model /path/to/local/whisper/snapshot \
  --tashkeel-runtime /path/to/runtime_tashkeel_v2
```

Preset ini khusus sumber 1280×720 pada 30000/1001 fps kepada hasil 480×854. Format lain ditolak: sesuaikan renderer secara nyata dahulu. Ia menyediakan modul berparameter, fon, identiti sumber dan EDL belum dipotong; ia tidak menjana terjemahan, peta crop atau kelulusan semakan. Tentukan path model setempat yang benar; jangan muat turun model berulang.

Untuk sambung projek yang sama, tambah `--resume` kepada arahan init yang sama. Ia memeriksa nombor episod, path dan SHA-256 sumber tanpa menulis semula fail. Cache sampel kamera diasingkan dalam projek. Jangan tukar sumber di bawah projek yang mengandungi hasil ASR lama.

Ukur senyap awal/akhir sebelum mengubah EDL. Potong senyap terminal sahaja mengikut arahan pengguna; kekalkan jeda dalaman, qasidah dan audio penutup yang berbunyi. Had 30 minit explainer tidak memendekkan ceramah penuh.

## ASR, terjemahan dan harakat

Gunakan Whisper dengan konteks audio. Chunk 300 saat membolehkan sambungan selepas gangguan dan terjemahan bermula ketika chunk seterusnya diproses. Terima cache hanya jika identiti sumber, tetapan dan JSONL lengkap sah; fail kosong atau separa bukan chunk selesai. Simpan teks, timestamp dan perkataan sekali. Hadkan proses mengikut CPU/RAM; jangan muatkan model kedua hanya untuk menunggu hasil yang sedang ditulis.

Gunakan model kedua hanya pada petikan yang meragukan. Jika audio berbunyi tetapi teks kosong, semak RMS/channel dan dengar petikan; uji `no_speech_threshold=None` pada petikan tersebut sahaja. Jangan mengada-adakan bacaan daripada konteks. Label bahagian yang tidak dapat dipastikan.

Untuk assembler checkpoint, gunakan TSV tiga medan: julat segmen ASR 1-based, Arab disemak, Melayu Malaysia. Liputi setiap segmen sekali. Terjemah gaya kitab turath, transliterasi dengan maksud dalam kurungan apabila sesuai, selaras Akidah ASWJ Asya'irah–Maturidiah. Kekalkan kata yang sudah disahkan; jangan terjemah semula semua cue kerana satu pembetulan.

Selesaikan penulis harakat sebelum membina ASS atau menerapkan teks Quran. Gunakan lock yang sama, hasil atomik dan proses unit baharu/berubah sahaja. Semak baris penuh; model tashkeel bukan pengesah ayat Quran. Untuk teks yang telah disahkan daripada sumber primer, sediakan JSON:

```json
[{"index": 1, "source_ar": "teks Arab tepat dalam ar_official", "text": "teks berbaris yang telah disahkan"}]
```

```bash
python scripts/apply_lecture_arabic_overrides.py \
  --draft /workspace/scratch/arbain_ep24/ep24_ar_draft.jsonl \
  --overrides /workspace/scratch/arbain_ep24/reviewed_arabic_overrides.json
```

Helper menolak penulis serentak, indeks berganda dan sumber yang tidak sepadan; ia tidak menulis semula hasil yang sudah sama. Jangan salin indeks override episod terdahulu. Kekalkan tanda Quran yang disahkan selepas tashkeel selesai.

## Framing, subtitle dan preflight

Gunakan ASS untuk teks/highlight satu perkataan Melayu pada satu masa; elakkan PNG setiap perkataan. Kekalkan Amiri Arabic Regular berbaris penuh, gradient atas/bawah, tajuk episod serta nama penceramah dan kawasan muka yang selamat. Dalam preset teruji, saiz Pillow Amiri 34 kira-kira ASS 59.772; faktor metrik DejaVu 2384/2048 hanya untuk fon tersebut, bukan formula universal.

Bina peta kamera baharu daripada sumber semasa. Semak setiap sudut, pertukaran kamera, dissolve, foreground yang melintas dan bingkai akhir. Periksa bingkai bersebelahan pada pertukaran; gunakan guard shot lebih lebar yang pendek jika perlu. Jangan pindahkan cluster ID atau tempoh guard lama secara automatik.

Sebelum master, semak audio asal lawan audio dipotong/encoded, lag, channel, kelantangan dan petikan yang diragui. Semakan teknikal bukan bukti telah mendengar. Encode pratonton pendek yang meliputi risiko sebenar: framing, teks panjang, pertukaran kamera dan penutup. Jika thumbnail nampak terpotong, lihat imej saiz penuh sebelum mengubah crop atau render semula.

Selepas semakan sebenar, tulis review JSON dengan `reviewer`, `camera_samples_reviewed` dan `preview_windows` (masa serta hasil semakan), kemudian:

```bash
python scripts/prepare_lecture_episode.py seal-preflight \
  --project /workspace/scratch/arbain_ep24 \
  --review /workspace/scratch/arbain_ep24/preflight_review.json
```

Ia memerlukan laporan sync lulus dan mengikat resit kepada hash input. Master ditolak jika sumber, EDL, audio, peta kamera, teks atau kod berkaitan berubah. Selepas pembetulan, semak bahagian terjejas dan seal semula; jangan palsukan resit untuk melangkaui semakan.

## Render, upload dan pembersihan

Kekalkan preset teruji CRF20/veryfast, AAC192k dan kadar bingkai asal; jangan janjikan kelajuan berdasarkan satu host. Sediakan audio AAC sekali dan copy semasa master. Jalankan full decode akhir sekali, semak kelantangan serta padanan paket AAC dan simpan resit yang terikat pada fail. Ulang hanya jika input berubah, semakan gagal atau isu baharu ditemui.

Ikut pilihan browser pengguna untuk download/upload fail besar. Jika pengguna mengarahkan “Download anyway”, teruskan dialog itu. Ralat browser kadangkala berlaku selepas fail telah tiba; periksa fail/proses sebelum menekan download lagi, tetapi jangan anggap semua ralat berjaya.

Selepas upload, tunggu status selesai dan sahkan nama, folder serta saiz melalui UI/metadata yang tersedia. Tidak perlu mainkan atau muat turun fail untuk mengesahkan kewujudannya. Pilih baris fail dan Share untuk pautan; jika clipboard kosong, gunakan ID yang benar-benar diperhatikan dan disahkan, bukan ID rekaan. Jangan ubah kebenaran perkongsian tanpa arahan.

Hantar pautan selepas satu episod disahkan, kemudian terus episod berikutnya hanya dalam skop yang diminta. Simpan checkpoint boleh sambung dahulu. Selepas upload disahkan, buang cache render episod tersebut; kekalkan model boleh guna semula, input semakan, sumber dan hasil akhir mengikut arahan projek. Laporkan sekatan sebenar dan progress yang dapat dibuktikan tanpa ETA rekaan.
