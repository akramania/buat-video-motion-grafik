# Adapter preset Python → JavaScript/GSAP

Gunakan `motion-bank.js` pada projek HTML; bekalkan GSAP daripada dependency projek yang sudah dikunci versinya. Kekalkan semua fail Python, registry, aset dan lesen asal. Jangan menggantikan bank Atlas atau mendakwa semua 842 entri telah diterjemahkan.

| Adapter HTML | Sumber sebenar | Mekanisme yang diterjemahkan | Batas adaptasi |
|---|---|---|---|
| `JS:T01` | `assets/motion_presets/typography.py`, `masked_words` | Perkataan naik dalam mask tetap, stagger masuk/keluar, cubic-out dan smooth exit | Susun atur/fon/palette ditetapkan HTML; adapter tidak meniru footer atau raster Python |
| `JS:B04` | `assets/motion_presets/new_b.py`, `_b04` | Counter nilai tepat, marker menyapu, hold dan exit | Bekalkan label/prefix/suffix sebagai elemen berasingan; titik hiasan demo tidak diterjemahkan |
| `JS:X02` | `assets/motion_presets/typography.py`, `bar_underline` | Wipe teks, bar pendahulu yang mengecil menjadi underline, exit | Underline lurus; gelombang sinus dekoratif versi Python tidak disalin |

`JS:` ialah namespace adapter setempat, bukan ID baharu dalam registry Atlas. Rekod kedua-dua `sourceId` dan `adapterId` dalam manifest projek. Resipi ini ialah adaptasi kod asal koleksi pengguna, bukan fail `.aep` atau jaminan rupa piksel yang sama dengan Pillow/After Effects.

## Kontrak pemasangan dan masa

1. Muatkan GSAP, plugin yang diperlukan dan `motion-bank.js` daripada fail tempatan sebelum skrip komposisi. Daftar plugin secara eksplisit.
2. Muatkan fon/aset dahulu; ukur lebar sebenar selepas `document.fonts.ready`. Bekukan layout sebelum membina animasi yang bergantung pada ukuran. Dalam HyperFrames, kekalkan pendaftaran timeline secara synchronous; sediakan pengukuran/layout semasa build atau gunakan readiness hook yang benar-benar disokong runtime sebelum render.
3. Bina satu `gsap.timeline({paused:true})` bagi setiap komposisi dan daftar dengan ID komposisi tepat pada `window.__timelines`. Jangan masukkan timeline komposisi terdaftar ke timeline induk secara manual. Gunakan timeline biasa dalaman yang tidak didaftar hanya sebagai komponen jika sesuai.
4. Tetapkan pose awal juga dalam CSS/markup. `seek(0)` tidak semestinya melintasi `set()` pada masa sifar. Gunakan elemen berlainan bagi scene berlainan dan elakkan dua tween yang menulis property sama pada masa bertindih.
5. Masa sumber preset ialah 0–5 saat. Adapter memetakan `sourceTime` kepada `start + sourceTime * duration/5` sekali sahaja. `duration` mesti positif dan terhingga; `start` bukan negatif. Durasi MP4 ditentukan oleh komposisi/CLI, bukan hanya panjang tween.

```html
<span class="word-mask"><span class="word">IDEA</span></span>
<style>
.word-mask { display:inline-block; overflow:hidden; vertical-align:top; padding-block:.15em; }
.word { display:inline-block; opacity:0; transform:translateY(100%); }
</style>
<script>
const tl = gsap.timeline({paused:true});
KMMotion.applyPreset(tl, 'JS:T01', Array.from(document.querySelectorAll('.word')), {start:0,duration:5});
window.__timelines = window.__timelines || {};
window.__timelines.root = tl; // mesti sepadan data-composition-id="root"
</script>
```

Untuk Arab, wrapper mengandungi perkataan lengkap atau satu baris lengkap dengan `lang="ar"`, `dir="rtl"` dan fon yang menyokong shaping. Jangan gunakan split karakter, reverse string atau letter-spacing. Perkataan yang dipisahkan menggunakan span boleh mengubah bidi sekitar tanda baca; semak ayat sebenar secara visual. Pilih animasi seluruh baris bagi ligatur, ayat al-Quran, campuran angka atau teks rumit. Gunakan SplitText pada perkataan/baris hanya selepas load fon; jangan pecahkan huruf Arab.

## Bank entrance → hold → exit dan rig

`entranceHoldExit(tl, elementOrArray, config)` menyediakan `up`, `left`, `pop`, stagger, anticipation, overshoot easing, follow-through dan exit berhingga. Masukkan `start`, `enterDuration`, `holdUntil`, `exitDuration`, `stagger`, `anticipation` dan `followThrough` mengikut audio/ruang bacaan. Fungsi menolak hold yang bertindih dengan entrance; ia tidak menganggar durasi bacaan pengguna. Gunakan `ease` tersendiri jika bahan klinikal/kitab memerlukan gerakan tenang. Semua masa ialah saat; tiada loop kekal atau jam dinding.

`solveTwoBone(root, target, upperLength, lowerLength, bend)` ialah IK analitik tulen. Output `elbow`, `end`, `upperDegrees`, `lowerLocalDegrees`, `reachable`. `bend` ialah +1/-1. Sasaran terlalu jauh/dekat di-clamp supaya panjang anggota kekal. Tentukan sisi siku/lutut yang natural daripada pose, bukan memilih bend secara rawak.

Bina hierarki `body → shoulder → upperArm → elbow → forearm → hand/prop`, dengan group ber-ID dan pivot berangka. Koordinat root/target mesti berada dalam ruang yang sama; tukarkan target world kepada ruang rig apabila parent/kamera mempunyai transform. `svgPivot(gsap, element, x, y)` menetapkan `svgOrigin` dalam ruang SVG; tentukan koordinat pivot sebenar dan periksa selepas parent transform. Jangan menganggap koordinat lokal sendi sama dengan root SVG.

Untuk IK beranimasi, kira pose daripada `t` mutlak sebelum render atau bake sudut sendi pada sampel masa tetap ke tween/keyframe berhingga. Jangan menyandarkan pose pada `onUpdate`, `onComplete`, frame sebelumnya atau penambahan delta; seek yang menyekat callback mesti tetap menghasilkan pose yang betul. Uji sentuhan tapak kaki, genggaman, panjang anggota dan lengan di atas/bawah objek pada pertengahan gerakan.

## Tambah adapter lain apabila diperlukan

Baca renderer Python sebenar dan kontrak `duration` dahulu, termasuk perbezaan L01–L06. Pisahkan layout statik, sampel gerak, shader/compositing dan cue. Terjemah fungsi gerak serta parameter sebenar; jangan menyamakan nama preset dengan penggunaan. Jika algoritma/fon/raster sukar diterjemah, kekalkan render Python kepada sequence alpha/klip dan komposit ke HTML. Sesuaikan semula untuk 9:16 tanpa meregang/crop teks. Banding tiga styleframe serta petikan gerak sebelum menandakan adapter baharu diuji.

## PixiJS dan Three.js sebagai pilihan

Gunakan PixiJS apabila jumlah sprite/partikel memerlukan GPU; hentikan ticker automatik dan tetapkan position/alpha/texture daripada masa mutlak serta seed tetap sebelum `renderer.render`. Preload texture/font, tunggu GPU siap, jangan gunakan `deltaTime` atau simulasi berasaskan urutan seek. Simulasi fizikal perlu cache/bake keadaan atau penyelesaian analitik.

Gunakan Three.js apabila adegan memerlukan mesh 3D, material, cahaya atau depth sebenar. Preload model/texture, kemas kini kamera/world matrices dan pilih pose melalui masa mutlak (`AnimationMixer.setTime(t)` bagi animasi yang sesuai). Render eksplisit ke WebGL canvas; jangan hidupkan RAF/Clock autonomi. Semak renderer adapter dan readiness HyperFrames versi terpasang; GSAP registry tidak secara automatik mengawal semua renderer WebGL. Kunci OS/browser/GPU untuk kebolehulangan; toleransi imej GPU tidak semestinya bit-identik merentas peranti. Label parallax 2.5D dengan tepat.

## Ujian adapter

Jalankan `KM_GSAP_PATH=/absolute/node_modules/gsap/dist/gsap.js node assets/hyperframes/test-motion-bank.cjs`. Ujian meliputi nilai counter tepat, easing sumber, seek songsang/berulang dengan callback disekat, kesetaraan sampel T01, panjang IK dan guard masa. Ia bukan pengganti QA visual/fonts atau bukti Pixi/Three telah dipasang/dirender. Periksa frame 0, onset, hold, peak dan exit pada MP4 akhir; dengar sync teks/SFX dengan audio sebenar.
