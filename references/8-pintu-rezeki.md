# Rujukan produksi: 8 Pintu Rezeki

Gunakan nota ini apabila pengguna meminta video seperti hasil terdahulu. Ia menyimpan keputusan visual dan audio projek, bukan fakta ayat yang boleh disalin membuta tuli.

- Video akhir: sekitar 3 minit 20 saat; 9:16, 1080×1920, 24 fps. Versi awal 160 saat dipanjangkan 1.25× setelah mengukur durasi sebenar 10 potongan narasi.
- Struktur: pembukaan 12 saat, lapan adegan bertema 16 saat setiap satu, penutup 20 saat sebelum pelarasan masa. Tiga beat teks bagi setiap tema, dengan terjemahan di panel bawah yang berasingan daripada teks komik utama.
- Rupa: warna krim, teal/jed, emas dan koral; lapisan langit/persekitaran lembut; garis kartun tebal; Amir dan burung Ciak muncul berulang. Aksi berbeza mengikut topik: burung keluar mencari makan, kerja, roti dan syukur, pintu/kompas, hujan istighfar, pasangan, keluarga, dan sedekah. Gunakan prinsip itu untuk reka karakter dan metafora baharu yang sesuai topik.
- Bunyi: skor instrumental asal yang dijana programatik, SFX mengikut aksi, narasi `ms-MY-OsmanNeural` pada kadar `-5%`. Voice stem disejajarkan pada permulaan setiap adegan; `sidechaincompress` FFmpeg merendahkan muzik sewaktu suara berbunyi; `loudnorm` sasaran sekitar -16 LUFS, puncak benar -1.5 dBTP.
- Teks agama: panel bawah menunjukkan terjemahan Bahasa Melayu Abdullah Muhammad Basmeih, rujukan surah dan ayat, serta kredit penterjemah. Dua segmen dipaparkan sebagai **petikan**, lengkap dengan elipsis. Teks ini milik projek tersebut; untuk projek baharu semak semula terhadap sumber yang dipercayai.
- Projek sebenar menghasilkan MP4, skrip narasi TXT, MP3 voice-over berasingan dan fail sumber Python. Skrip dalam folder sebelah boleh dicuba dengan `--preview`, `--help`, atau argumen yang didokumenkan setelah menyesuaikan persekitaran. Ia menggunakan `numpy`, `Pillow`, `scipy`, `edge-tts`, `ffmpeg` dan fon sistem; suara memerlukan akses servis TTS.

Petua revisi: ukur dahulu apa yang berubah (narasi, ayat, reka bentuk atau durasi); ubah komponen berkaitan, kemudian render dan periksa video penuh semula. Teks di bahagian bawah mesti cukup besar untuk dibaca walaupun pengguna membenarkan saiz kecil.
