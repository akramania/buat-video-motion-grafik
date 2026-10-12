# Adaptasi 28 preview Envato — EV001–EV120

Kandungan: [pemerhatian](#pemerhatian-dan-status), [render](#pilih-dan-render), [sumber](#pemetaan-sumber), [indeks](#indeks-mekanisme), [production](#penggunaan-production-dan-semakan).

## Pemerhatian dan status

28 MP4 preview awam diperiksa melalui 12 sampel sepanjang setiap video dan urutan lima bingkai pada sela 0.2s. Video asal, audio, foto, logo dan template Envato tidak dimasukkan dalam renderer atau atlas. 120 preset ialah implementasi asal berpandukan mekanisme yang terlihat, dengan olahan komposisi; bukan semua variasi produk atau kod asal Envato.

Jumlah registry: 442 = 137 asal + 185 demo panduan + 120 EV. Preview EV: 960×540/30 fps, 6 saat, senyap; kanvas reka bentuk 1280×720. Atlas sama: https://motion-preset-atlas.akramania.chatgpt.site.

## Pilih dan render

```bash
python assets/motion_presets/render.py --preset EV024 --clean --output revenue.mp4
python assets/motion_presets/render.py --config config.json --clean --output chart.mp4
```

Gunakan `--list` atau `envato_index.json` untuk nama, mekanisme, parameter dan sumber. Tukar teks/label/data, kemudian semak layout. `duration` meretime keseluruhan aksi EV; untuk scene lama dengan aksi tetap pantas, gubah beberapa event EV pada jam scene berasingan. `show_titles:false` membuang tajuk dan label demo pada transisi EV089–EV096. `image_paths` menerima dua imej pada transisi ini; imej di-contain untuk mengekalkan subjek. Renderer ini tidak menerima footage video sebagai input secara terus.

Nilai KPI, goal, ring, delta dan demographic yang tidak mempunyai kawalan input khusus ialah data contoh; semak kod sebelum menghasilkan statistik sebenar. Glyph Latin sahaja; Arab/Jawi memerlukan shaping khusus. Peta menggunakan geometri Natural Earth public domain. Semak fokus/pin selepas menukar kod atau geometri. Glass ialah simulasi alpha/rim/blur 2D, bukan shader refraksi 3D. Blur kamera dan paper tear ialah mask/transform raster.

## Pemetaan sumber

| Sumber | Preset | Sampel rapat diperiksa |
|---|---|---|
| [Match Cut - MOGRT MPVTHDZ](https://elements.envato.com/match-cut-mogrt-MPVTHDZ) | EV001–EV004 | 5.6–6.4s |
| [World Map Y3N8ENZ](https://elements.envato.com/world-map-Y3N8ENZ) | EV005–EV008 | 3–3.8s |
| [Liquid Glass Widgets XDX2XW7](https://elements.envato.com/liquid-glass-widgets-XDX2XW7) | EV009–EV014 | 7–7.8s |
| [AI Workflow 539QW2F](https://elements.envato.com/ai-workflow-539QW2F) | EV015–EV018 | 1.7–2.5s |
| [Counters |MOGRT LJ2JL87](https://elements.envato.com/counters-mogrt-LJ2JL87) | EV019–EV022 | 9–9.8s |
| [Number Counter - AE M7PVL8C](https://elements.envato.com/number-counter-ae-M7PVL8C) | EV023–EV026 | 1.4–2.2s |
| [Saas Infographic Pack 82DFS5S](https://elements.envato.com/saas-infographic-pack-82DFS5S) | EV027–EV030 | 3.7–4.5s |
| [World Map Infographic Template SUFMMDH](https://elements.envato.com/world-map-infographic-template-SUFMMDH) | EV031–EV034 | 6–6.8s |
| [UI Infographic Data Widget F4BGXEB](https://elements.envato.com/ui-infographic-data-widget-F4BGXEB) | EV035–EV040 | 7–7.8s |
| [Counter Pro Toolkit - for DaVinci Resolve 9T6R6YR](https://elements.envato.com/counter-pro-toolkit-for-davinci-resolve-9T6R6YR) | EV041–EV044 | 2.8–3.6s |
| [Infographic Builder R2S6WVF](https://elements.envato.com/infographic-builder-R2S6WVF) | EV045–EV050 | 82–82.8s |
| [Planner XXUPJR6](https://elements.envato.com/planner-XXUPJR6) | EV051–EV054 | 1.4–2.2s |
| [Infographics 2Q5SUHM](https://elements.envato.com/infographics-2Q5SUHM) | EV055–EV058 | 134–134.8s |
| [Social Media Infographic 2PJ4A94](https://elements.envato.com/social-media-infographic-2PJ4A94) | EV059–EV062 | 14–14.8s |
| [Animated Chart Pack | MOGRT 2AM3QW8](https://elements.envato.com/animated-chart-pack-mogrt-2AM3QW8) | EV063–EV068 | 21–21.8s |
| [Marketing & Business Flat Design Icons PMHC3NZ](https://elements.envato.com/marketing-business-flat-design-icons-PMHC3NZ) | EV069–EV072 | 4.5–5.3s |
| [Pros And Cons 4ZXN84U](https://elements.envato.com/pros-and-cons-4ZXN84U) | EV073–EV076 | 11.5–12.3s |
| [Elegant Infographics Vol.3 for Premiere Pro A42ANM8](https://elements.envato.com/elegant-infographics-vol-3-for-premiere-pro-A42ANM8) | EV077–EV080 | 2.5–3.3s |
| [Hook & Captions for Social Media - Mogrt BEQ96TA](https://elements.envato.com/hook-captions-for-social-media-mogrt-BEQ96TA) | EV081–EV084 | 4.1–4.9s |
| [Documentary Style Pack V8HAEEQ](https://elements.envato.com/documentary-style-pack-V8HAEEQ) | EV085–EV088 | 11–11.8s |
| [Camera Transitions for Final Cut Pro 49WGM3Q](https://elements.envato.com/camera-transitions-for-final-cut-pro-49WGM3Q) | EV089–EV092 | 7.1–7.9s |
| [Kinetic Paper Rip Transitions P9QV59N](https://elements.envato.com/kinetic-paper-rip-transitions-P9QV59N) | EV093–EV096 | 13.6–14.4s |
| [Text Animation CW3VJ8V](https://elements.envato.com/text-animation-CW3VJ8V) | EV097–EV100 | 3.5–4.3s |
| [Text Animation DGUDXLS](https://elements.envato.com/text-animation-DGUDXLS) | EV101–EV104 | 1–1.8s |
| [Text Animation 82ZADCZ](https://elements.envato.com/text-animation-82ZADCZ) | EV105–EV108 | 11.7–12.5s |
| [Text Animation 4C6SYD3](https://elements.envato.com/text-animation-4C6SYD3) | EV109–EV112 | 6.8–7.6s |
| [Text Animation RUC2VZW](https://elements.envato.com/text-animation-RUC2VZW) | EV113–EV116 | 7.6–8.4s |
| [Text Animation YZTFUH4](https://elements.envato.com/text-animation-YZTFUH4) | EV117–EV120 | 5.9–6.7s |

## Indeks mekanisme

| ID | Nama | Mekanisme renderer |
|---|---|---|
| EV001 | Keyword Page Match | `match_page` |
| EV002 | Headline Anchor Match | `match_headline` |
| EV003 | Map Target Match | `match_map` |
| EV004 | Feature Window Match | `match_feature` |
| EV005 | Network Arc Reveal | `map_network` |
| EV006 | Country Focus Camera | `map_focus` |
| EV007 | Destination Media Callout | `map_callout` |
| EV008 | Hub Route Pulses | `map_hub` |
| EV009 | Glass Media Controls | `glass_media` |
| EV010 | Glass Project Status | `glass_status` |
| EV011 | Glass Activity Bars | `glass_bars` |
| EV012 | Glass Progress Ring | `glass_ring` |
| EV013 | Glass Balance Sparkline | `glass_balance` |
| EV014 | Glass Metric Capsule | `glass_metric` |
| EV015 | Input Agent Output | `workflow_pipeline` |
| EV016 | Agent Tool Hub | `workflow_hub` |
| EV017 | Branching Knowledge Router | `workflow_branch` |
| EV018 | Reasoning Handoff | `workflow_chain` |
| EV019 | Strike Band Counter | `counter_strike` |
| EV020 | Currency Label Counter | `counter_currency` |
| EV021 | Delta Badge Metric | `counter_badge` |
| EV022 | Metric Ring Counter | `counter_ring` |
| EV023 | Compact Unit Counter | `counter_compact` |
| EV024 | Decimal Revenue Counter | `counter_decimal` |
| EV025 | Discount Percent Counter | `counter_discount` |
| EV026 | Subscriber Trend Counter | `counter_trend` |
| EV027 | KPI Capsule Cascade | `kpi_stack` |
| EV028 | SaaS Agenda Timeline | `agenda` |
| EV029 | Data Streams Merge | `stream_merge` |
| EV030 | Automation Comparison | `automation_bars` |
| EV031 | Dashed Travel Route | `map_travel` |
| EV032 | Region Data Overlay | `map_region` |
| EV033 | Place Pin Labels | `map_pins` |
| EV034 | Itinerary Camera Move | `map_itinerary` |
| EV035 | Revenue Widget Build | `widget_revenue` |
| EV036 | Mini Area Tooltip | `chart_mini` |
| EV037 | Goal Tracker Widget | `widget_goal` |
| EV038 | Sales Funnel Widget | `funnel` |
| EV039 | Traffic Donut Widget | `donut` |
| EV040 | Ranking Bars Widget | `rank_bars` |
| EV041 | Neon Money Counter | `counter_neon` |
| EV042 | Signed Capsule Counter | `counter_capsule` |
| EV043 | Social Icon Metrics | `counter_social` |
| EV044 | Color Block Counter | `counter_block` |
| EV045 | Stacked Column Builder | `chart_stacked` |
| EV046 | Radar Polygon Trace | `radar` |
| EV047 | Stepped Ranking Bars | `rank_steps` |
| EV048 | Nested Ring Builder | `nested_rings` |
| EV049 | People Unit Grid | `people_grid` |
| EV050 | Process Step Connectors | `process_steps` |
| EV051 | Daily Agenda Cards | `planner_agenda` |
| EV052 | Month Event Grid | `planner_calendar` |
| EV053 | Checklist Completion | `planner_check` |
| EV054 | Timebox Ribbon | `planner_ribbon` |
| EV055 | Demographic Pictogram | `people_compare` |
| EV056 | Pie Legend Reveal | `pie_legend` |
| EV057 | Geographic Pin Metric | `map_metric` |
| EV058 | Icon Matrix Cascade | `icon_matrix` |
| EV059 | Platform Column Race | `social_columns` |
| EV060 | Butterfly Audience Chart | `butterfly` |
| EV061 | Platform Ranking Bars | `social_rank` |
| EV062 | Two Year Mirror Bars | `mirror_bars` |
| EV063 | Area Chart Hover | `chart_area` |
| EV064 | Candlestick Trace | `chart_candle` |
| EV065 | Spending Stacked Bars | `chart_spending` |
| EV066 | Dual Area Comparison | `chart_dual` |
| EV067 | Mixed Bar Line Chart | `chart_mixed` |
| EV068 | Transaction Lollipop | `chart_lollipop` |
| EV069 | Megaphone Burst | `icon_megaphone` |
| EV070 | Stopwatch Assembly | `icon_clock` |
| EV071 | Pie Icon Assemble | `icon_pie` |
| EV072 | Dashboard Icon Build | `icon_screen` |
| EV073 | Pros Cons Checklists | `compare_checks` |
| EV074 | Pros Cons Pill Rows | `compare_pills` |
| EV075 | Benefit Risk Ladder | `compare_ladder` |
| EV076 | Image Comparison Cards | `compare_media` |
| EV077 | Gradient Dual Lines | `chart_elegant` |
| EV078 | Personal Radar Profile | `radar_profile` |
| EV079 | History Event Timeline | `timeline_history` |
| EV080 | Profile Rings Sliders | `profile_rings` |
| EV081 | Orbit Badge Hook | `hook_orbit` |
| EV082 | Number Hero Hook | `hook_number` |
| EV083 | Accent Word Caption | `type_accent` |
| EV084 | Caption Label Swap | `type_label` |
| EV085 | Documentary Grouped Bars | `doc_bars` |
| EV086 | Documentary Point Line | `doc_line` |
| EV087 | Vintage Timeline Cards | `doc_history` |
| EV088 | Newspaper Headline Marker | `doc_headline` |
| EV089 | Camera Zoom Blur | `camera_zoom` |
| EV090 | Camera Whip Pan | `camera_whip` |
| EV091 | Camera Roll Transition | `camera_roll` |
| EV092 | Camera Stretch Transition | `camera_stretch` |
| EV093 | Horizontal Torn Wipe | `rip_horizontal` |
| EV094 | Diagonal Paper Tear | `rip_diagonal` |
| EV095 | Layered Paper Shards | `rip_shards` |
| EV096 | Paper Cutout Punch | `rip_cutout` |
| EV097 | Bold Light Line Stack | `type_weight` |
| EV098 | Glyph Compression Reveal | `type_compress` |
| EV099 | RGB Glitch Settle | `type_glitch` |
| EV100 | Tall Phrase Cascade | `type_tower` |
| EV101 | Glow Caret Typing | `type_glow` |
| EV102 | Delete Retype Cursor | `type_delete` |
| EV103 | Completed Word Highlight | `type_finish` |
| EV104 | Code Line Typewriter | `type_code` |
| EV105 | Marker Keyword Wipe | `type_marker` |
| EV106 | Mixed Serif Word Stagger | `type_serif` |
| EV107 | Reverse Erase Caption | `type_erase` |
| EV108 | Side Aligned Word Lift | `type_side` |
| EV109 | Red Strip Stack | `type_redstack` |
| EV110 | Slanted Strip Reveal | `type_slant` |
| EV111 | Oversized Inset Keyword | `type_inset` |
| EV112 | Alternating Tag Layout | `type_tags` |
| EV113 | Expanding Outline Box | `type_box` |
| EV114 | Glyph Window Strip | `type_window` |
| EV115 | Tracking Letter Strip | `type_tracking` |
| EV116 | Line Flip Typography | `type_flip` |
| EV117 | Magenta Stencil Text | `type_stencil` |
| EV118 | Gradient Panel Reveal | `type_gradient` |
| EV119 | Outline Echo Words | `type_outline` |
| EV120 | Scribble Stack Draw | `type_scribble` |

## Penggunaan production dan semakan

`--clean` menutup label ID renderer serta tajuk demo tipografi. Gunakan `show_titles:true` jika tajuk demo diperlukan; `status_label` menerima teks pilihan pada counter, dan lalai kosong dalam mod bersih. Counter perpuluhan mengekalkan satu baseline untuk angka, titik dan koma. Semak sekali lagi selepas menukar format nombor, fon atau panjang teks.

Semakan 10 Oktober 2026: semua 442 MP4 atlas lulus ffprobe dan penyahkodan penuh. Custom EV024 (RM 9,876.54), EV063 (enam titik data gantian) dan EV105 (dua baris BM) dirender dan diperiksa; baseline perpuluhan dan mod bersih diperbaiki. QA interaksi browser belum tersedia kerana control-browser tidak terdedah.
