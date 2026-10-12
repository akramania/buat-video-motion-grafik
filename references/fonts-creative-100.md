# 100 keluarga fon kreatif

Gunakan katalog `assets/fonts_creative_100/font_index.json`: FT0001–FT0100, 25 Arab dan 75 Latin. Setiap keluarga dikira sekali; satu gaya lengkap atau satu variable face disediakan, bukan semua weight keluarga. Semua fail font dan OFL asal dikekalkan byte-identical.

Materialisasikan font dengan `python assets/fonts_creative_100/prepare_fonts.py FT0002`, atau import `prepare_font("Amiri Quran")`. Gunakan `--list --search arabic` untuk pemilihan dan `--all` untuk penyediaan penuh. Cache dijana apabila diperlukan; hash arkib dan setiap fail disahkan sebelum digunakan.

Untuk ayat al-Quran, utamakan Amiri Quran (FT0002), Amiri (FT0001), Scheherazade New (FT0003), Noto Naskh Arabic (FT0004) dan Lateef (FT0011). Lima calon lulus semakan cmap, HarfBuzz shaping dan preview visual al-Fatihah 1:1, 1:2, 1:7 sahaja; jangan anggap seluruh al-Quran telah disahkan.

Gunakan sumber ayat yang disemak, `lang=ar`, arah RTL dan RAQM/HarfBuzz. Kekalkan codepoint dan harakat; animasikan blok ayat penuh melalui opacity atau transform. Jangan pecahkan sambungan huruf dengan typing per-codepoint, jangan reorder teks dan jangan jarakkan huruf Arab. Render sampel ayat sebenar projek, semak harakat dan tanda wakaf serta elakkan clipping sebelum publish.

Sertakan OFL.txt ketika mengedarkan font. Jangan jual fail font secara berasingan. ZIP download Atlas mengandungi TTF original, OFL dan provenance; kompresi arkib skill tidak mengubah font. Fon ini berlesen terbuka dengan estetika premium, bukan font berbayar dari Motion Array.
