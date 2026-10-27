# Showcase: perkataan tengah → video → telefon perspektif

Gunakan untuk showcase/reel promosi, demonstrasi langkah ringkas, video yang masuk menindih teks, atau permintaan gaya daripada projek showcase yang terkini. Kekalkan arahan genre, orientasi, sumber, suara dan durasi terbaru. Gunakan aliran ceramah Arab sedia ada untuk suntingan ceramah; panduan ini tidak menggantikan aliran itu.

## 1. Koreografi setiap scene

1. Mulakan dengan frasa besar di tengah. Animasikan perkataan secara berasingan dan berperingkat; ukur teks sebenar sebelum menetapkan saiz.
2. Beri masa frasa lengkap dibaca. Asingkan jam entrance, siap-baca, hold, perpindahan teks dan kemasukan video.
3. Gerakkan kumpulan teks ke kiri, kanan, atas, bawah atau ke lapisan depth. Variasikan arah, skala, sudut dan bentuk susun atur mengikut mesej.
4. Masukkan video sebenar dari arah/laluan yang dikoreografi. Komposit video di atas teks supaya video boleh melintasi atau menindih perkataan yang sudah dibaca. Jadikan teks besar sebagai underlay apabila sesuai.
5. Akhiri dengan satu komposisi yang stabil untuk membaca manfaat, harga atau CTA. Tukar scene dengan mekanisme perkataan dan kemasukan video yang berbeza.

Pelbagaikan mekanisme yang nampak berbeza, bukan hanya warna atau arah. Gabungkan perkataan berengsel, potongan reben, orbit, kad, mask, lipatan, depth dan pantulan mengikut cerita. Kekalkan satu fokus utama pada satu masa. Semak semua perkataan akhirnya lengkap; glyph yang terpotong semasa reveal mesti pulih pada saat siap-baca.

Untuk perkataan Latin/Melayu, gunakan `scripts/showcase_layers.py`. Modul membekalkan 15 mekanisme **custom**, berasingan daripada registry Atlas:

| Nama custom | Gerakan utama |
| --- | --- |
| `stomp` | Hentak dan overshoot perkataan |
| `ribbon_split` | Dua jalur perkataan bercantum |
| `hinge` | Perkataan membuka pada paksi mendatar |
| `orbit` | Perkataan bergerak melalui lengkung orbit |
| `card_snap` | Kad perkataan snap dan settle |
| `fold` | Lipatan pada paksi menegak |
| `window` | Perkataan muncul melalui tingkap mask |
| `domino` | Putaran berturutan dari bawah |
| `depth` | Perkataan datang dari dekat dan fokus |
| `tracking` | Jarak huruf mengunci mengikut perkataan |
| `brush` | Reveal bertepi beralun yang lengkap pada hold |
| `magnet` | Kad berkumpul dari posisi berbeza |
| `rolling_word` | Perkataan bergulung dalam slot |
| `arc` | Laluan perkataan melengkung dengan putaran |
| `stencil` | Jalur mask memenuhi perkataan |

Pilih beberapa yang sesuai; 15 ialah kapasiti modul, bukan kuota semua video. Simpan dispatch custom di bawah nama fungsi sebenar. Jangan menamakannya K/PX/EV atau menambah bilangan preset Atlas. Jika menggunakan preset registry lain, panggil fungsi asal dan audit secara berasingan. Gunakan shaping dan fon Arab yang betul untuk teks Arab; modul baharu ini belum membuktikan semua skrip tulisan atau fon.

## 2. Penggunaan komponen

Import modul dari folder `scripts/` skill, atau salin ke projek dan beri `font_path` projek. Modul memerlukan Pillow, NumPy dan OpenCV. Fon lalainya ialah DejaVu Sans Bold yang sudah disertakan dalam skill; pilih fon lain mengikut brief dan lesen.

```python
from PIL import Image
from showcase_layers import draw_word_group, project_phone

canvas = Image.new('RGBA', (720, 1280), '#201C2D')
audit = {}  # kosongkan sebelum render master; asingkan audit preview
draw_word_group(
    canvas, ['IDEA BAHARU', 'JADI VISUAL'], t,
    mechanism='ribbon_split', complete_at=.7, lead_in=.08,
    centre=(360, 605), max_width=610, font_size=96,
    audit=audit, cue_id='scene_01',
)
# Selepas hold/perpindahan teks, lukis frame rakaman asal di atasnya.
quad = project_phone(
    canvas, source_frame, centre=(360, 800), width=400,
    yaw=8, roll=-2, fit='contain',
)
```

Animasikan `centre`, `scale`, `angle` dan `opacity` kumpulan teks sebagai parent transform. Mulakan `project_phone` hanya selepas frasa sempat dibaca. Animasikan posisi, lebar, yaw/pitch/roll telefon secara berasingan, kemudian settle. Gunakan masa `frame/fps`; modul tidak memainkan video, membina keseluruhan timeline, merakam audio atau merender master sendiri. Dekod sumber dan enkod MP4 menggunakan pipeline sedia ada.

Semak nilai pulangan `font_size`, `word_count`, `complete_by` dan quad telefon. Ukur bounds alpha dan keseluruhan laluan gerak. Reflow atau pecahkan frasa jika saiz akhir terlalu kecil. Overscan dekoratif dibenarkan selepas salinan penting sudah dibaca; bezakan daripada glyph penting atau telefon yang kekal terpotong.

## 3. Potongan langkah dan kelajuan

- Dapatkan fail sumber yang sebenar. Jika pengguna menyebut "dari sini" tanpa pautan/fail yang boleh dikenal pasti, minta sumber itu; teruskan semakan projek yang tidak bergantung padanya.
- Periksa metadata, contact sheet sepanjang rakaman dan frame rapat sekitar aksi. Pilih tap, copy/paste, pemilihan gambar, arahan, submit dan hasil siap yang benar-benar ada.
- Apabila pengguna hanya mahu nampak langkah, potong jeda/menunggu dan passage input panjang. Percepat aksi mengikut keperluan; 2.5×–6× ialah contoh yang telah digunakan, bukan tetapan wajib semua sumber.
- Simpan EDL: sumber, SHA-256, in/out, speed, crop/mask, tempoh output dan scene. Untuk FFmpeg, gunakan `setpts=(PTS-STARTPTS)/speed`, normalkan FPS/SAR dan timestamp setiap potongan sebelum concat. Tentukan audio secara sengaja.
- Tahan frame hasil seketika jika perlu. Label seperti "DEMO DIPERCEPAT" membantu apabila mampatan masa boleh disalah anggap sebagai masa pemprosesan sebenar.

Contoh beat empat saat: teks masuk dan lengkap sekitar 0–0.55s; telefon mula masuk sekitar 0.66s; aksi sumber dipercepat dimainkan setelah telefon hampir stabil sekitar 1.1–3.9s. Ubah masa ini mengikut panjang frasa, tindakan dan narasi. Jangan mempercepat suara yang perlu difahami hanya untuk mengikut contoh ini.

Utamakan had durasi pengguna yang terbaru. Jika pengguna membenarkan lebih satu minit, tambah ruang demonstrasi apabila perlu. Jangan mewariskan 52/60 saat sebagai had universal.

## 4. Mockup telefon dan sumber UI

Gunakan `project_phone` untuk menyatukan hardware generik tanpa logo, rim, butang, kamera dan skrin dalam satu transform perspektif. Ini ialah 2.5D plane, bukan rekonstruksi 3D. `fit='contain'` mengekalkan semua kandungan sumber; gunakan `cover` selepas semakan crop yang sesuai.

Buang border luar atau caption terbakar yang tidak diperlukan sebelum memasukkan frame ke telefon. Tentukan crop daripada rakaman sebenar; jangan salin koordinat projek lama. Mask saki-baki caption hanya di kawasan yang tidak memadam aksi utama. Semak status bar, keyboard, butang upload/send, avatar, menu dan hasil. Slot kamera boleh dimatikan melalui `camera_slot=False` jika menutup UI penting.

Gunakan UI/rakaman asal sebagai bukti. Gunakan UI rekaan hanya sebagai ilustrasi yang dilabel jelas. Jangan membuat UI, logo, hasil, angka atau testimoni palsu apabila sumber tidak boleh diakses.

## 5. Revisi, audio dan QA

Bekukan sumber, copy dan audio yang tidak diminta berubah. Jika revisi hanya visual dan tempoh sama, semak checksum payload AAC/PCM selepas stream copy. Jika tempoh berubah, panjangkan atau susun muzik dan cue SFX pada timeline baharu; jangan mendakwa identiti bit yang tidak diuji. Kekalkan suara yang telah diluluskan.

1. Render tiga style frame dan proof 3–5s untuk handoff/telefon yang paling berisiko.
2. Semak frasa siap-baca, video di atas teks, susun atur selepas settle dan hasil setiap langkah daripada MP4 yang dieksport.
3. Semak semua perkataan pada hold, badge nombor, CTA, keyboard, notch, rim dan margin telefon. Periksa frame rapat sebelum/semasa/selepas handoff; crop sementara mesti disengajakan.
4. Sahkan durasi/resolusi/FPS/frame count, decode penuh dan audio akhir. Ukur true peak pada **AAC yang dienkod**, kerana encoding boleh menghasilkan intersample overshoot walaupun WAV sudah dihadkan.
5. Bezakan semakan frame/teknikal daripada playback/pendengaran sebenar. Catat batas yang belum diuji. Simpan master dan projek boleh bina semula. Jika sumber besar kekal dalam storan pengguna, sertakan potongan produksi serta inventori/hash/cara mendapatkan asal.

Pastikan pautan penghantaran menunjuk fail sebenar yang telah disahkan. Jika pengguna tidak dapat membuka pautan terdahulu, berikan pautan fail terus yang sah mengikut platform; nama versi/tempoh yang jelas membantu mengelakkan kekeliruan dengan hasil lama.

## Skop bukti

Projek showcase yang menjadi asas aliran ini menghasilkan V2 52s dengan 15 mekanisme perkataan, kemudian V3 60s dengan empat potongan tutorial dipercepat dalam telefon perspektif. V3 disahkan 720×1280/30 fps, 1,800 frame, decode penuh, 300 sampel pada 0.2s, 15 paparan frasa lengkap, 15 komposisi selepas settle dan 24 frame aksi telefon. Audio AAC diukur -16.69 LUFS dan -1.60 dBTP. Semakan playback audiovisual subjektif dan critic bebas tidak didakwa.

Kod komponen digeneralisasi daripada projek itu tanpa menyalin video, rekod akaun, URL sumber peribadi, harga atau copy produk. Ujian fungsi merangkumi 15 mekanisme pada frame masuk/hold, seek berulang, fon pilihan dan unjuran telefon; forward-test tugas lain menghasilkan proof 3s, 480×854/30 fps, 90 frame, decode penuh. Preview baharu tetap diperlukan pada teks, fon, footage, nisbah dan timing projek seterusnya. Kekalkan registry Atlas 842, aset VL, MA, SVG dan semua aliran skill lain.
