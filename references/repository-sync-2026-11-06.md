# Current skill versus GitHub: 6 November 2026

## Scope and comparison

Compared the installed `buat-video-motion-grafik` skill with GitHub `main` at `0f54b97081a3aaf29a74f41c069e09e7be85175c`, inspected in the signed-in browser. That GitHub snapshot was last updated on 28 October Malaysia time. The newer skill has a component lock and production guidance dated 3 November and later Gaya Ekstrem refinements.

| Area | GitHub before update | Current repository change |
| --- | --- | --- |
| Main instructions | Atlas/CFX and earlier HTML workflow | Current SKILL.md and agent metadata, including Gaya Ekstrem and component recovery |
| Gaya Ekstrem | No dedicated reference | Large kinetic typography, changing compositions, layered prop build/disassembly, image carousels, counters, audio and QA |
| HyperFrames | 0.8.185; GSAP 3.14.2 | 0.9.4; GSAP 3.15.0, matching vendored library/plugins and npm lock |
| Components | Earlier project-specific setup | Dated Node/npm, browser, FFmpeg, Whisper, Three.js, React and Remotion lock plus restoration/module checks |
| HyperFrames direction | General production and motion bank | Expanded official-example study, nine source/output workflows, updated setup/wrapper and QA |
| Whisper | Earlier medium helper | Exact dependency lock, model revision/manifest and load/decode requirements |
| Runtime evidence | Earlier validation | Imported new-version validation records installation checks and browser-launch failure accurately; legacy records retained separately |
| Usage examples | One short example | README table with exactly 30 use cases and complete English prompts |

## Preserved repository-specific work

Retained the existing Atlas contract, native renderer cache-copy fixes in `core.py` and `motionprompt.py`, content-based preview reuse and locked-job export in `build_atlas.py`, catalogue job links, full bank catalogue, SVG archive/restoration helper, Gemini entrypoint/installers and selective-cache files. The installed skill's versions of those files would undo GitHub-specific fixes or replace complete metadata with a partial generated sample. Materialized SVGs and L01 preview outputs were not duplicated into the repository. Preserved the 922-preset registry and all existing asset archives. No unrelated files were deleted.

This update targets repository source. It does not claim that npm, the historical v1.1.0 release, dated Drive packs, or the separate Gemini skill have been republished. Large runtime binaries, node_modules and model weights remain external caches as required by the skill.

## Verification scope

The 29 imported files below match the current installed skill byte-for-byte. Fresh checks: Python AST, JavaScript syntax and JSON parsing passed for imported code; package.json and package-lock.json pins match; local README/SKILL links resolve; the README contains exactly 30 sequential English prompts. All 16 existing Atlas unit tests passed, including real video/alpha encode and decode. The additional selected native-baseline sweep stopped at CFX71 with a baseline mismatch. Atlas renderer/contract files were unchanged by this update; no baselines were regenerated to hide the mismatch. Offline component preflight correctly returned ready:false because the dated Node/browser/FFmpeg binary cache is absent here; matching npm packages were found. No new HyperFrames MP4 or production transcription was claimed. Importing an existing validation file is evidence about its stated original environment, not a fresh rendering result. The runtime's original browser-launch limitation remains visible.

## Imported file checksums

| File | SHA-256 |
| --- | --- |
| `SKILL.md` | `aa68e707edc2a2b10de6173e5c75da6030c2beaa32f4d8df873234d9b0ce801e` |
| `agents/openai.yaml` | `bdb18e250dc883d8e36df8f5c0942adbf14b1c91b85ff8a0aa31242bf843efcb` |
| `assets/hyperframes/package.json` | `939d57cc234da95041ca628c67c429e908513ab1f59a7472fd709802955113f2` |
| `assets/hyperframes/package-lock.json` | `c8cbc8001e3efa5ef5fc965d59a749d0a368a0166a59becc67110c876f1a8cba` |
| `assets/hyperframes/validation.json` | `e9ebd2240978baaca8541a4ced7c3d77d25b524980ea9a007261336ccd31b71a` |
| `assets/hyperframes/legacy/package.json` | `939d57cc234da95041ca628c67c429e908513ab1f59a7472fd709802955113f2` |
| `assets/hyperframes/legacy/package-lock.json` | `c8cbc8001e3efa5ef5fc965d59a749d0a368a0166a59becc67110c876f1a8cba` |
| `assets/hyperframes/legacy/validation.json` | `e9ebd2240978baaca8541a4ced7c3d77d25b524980ea9a007261336ccd31b71a` |
| `assets/runtime-lock.json` | `abc636c41680c21d9bdec39758014956a0f28d0e1230c65dd3b978ae7a2c0fea` |
| `assets/whisper/model-medium.json` | `f0aadcbbfc20ce0ab8dcd509d04d200305beda5e7f9c067b6328d5ea39ce7780` |
| `assets/whisper/requirements.lock.txt` | `790ba4ee520662a032ecddde299e2ac3e268eacfec6605d9c686b1724642febc` |
| `references/gaya-ekstrem.md` | `a56ba00d9a78a0285e33f3e9c1cd488ae3fac51dc481bf90cc300516ba8b42e8` |
| `references/hyperframes-codex-examples.md` | `d43ed78d56cb71b3225450c25fa6d4f986f1bd1c0f656fc848fb611909ad863e` |
| `references/hyperframes-nine-workflows.md` | `c19ff105708fdc39e828dd2677b2233aa078d377436685bb29ef5ba8ae54fe88` |
| `references/video-component-toolkit.md` | `0921e4a706180825a8da93a451a7e86b4bd9f9a4921c105aeb37876e3d2f6211` |
| `references/html-hyperframes-production.md` | `e614effa11b874eb87e986b3c33a931c14eda9522a1a2c0117924cc4afe1d89c` |
| `references/hyperframes-motion-bank.md` | `a350cb4d87863fe903220a580c63fd4492f184f23d8f5f2e7c54bfd8a2f8024b` |
| `references/media-tools.md` | `aacdedf2163e7d49cfc3a41c73029df4a0863135e89eaf4cc44b3cfc3406340c` |
| `scripts/check_video_modules.mjs` | `13c380897b50d777762cf0c9b6b2092462470559a4f33938be89d7a380c0b08d` |
| `scripts/setup_video_components.py` | `d0abbb70c78eda2616e646f8ba4ee37dd1ef37124969609b80b01cc188e9401e` |
| `scripts/ensure_whisper.py` | `759724bea08b5a71abfaa44fbb2eb8d317ebbbc655b52ea1a93607176e7908bf` |
| `scripts/qa_hyperframes.mjs` | `006aab114846553a9f8a9c1cd8fa12341344cc9a6f2099c2d1a5629102beb5aa` |
| `scripts/run_hyperframes.mjs` | `f9793e480249b6c4096636349f5bb3358a1b684142d97aab1a0b6981f8a66f98` |
| `scripts/setup_hyperframes.mjs` | `e281a29fd38cc43ea9b26d855e6eb9c5fdc7c9cb837797a6896c3c11ec698634` |
| `assets/hyperframes/vendor/DrawSVGPlugin.min.js` | `2d2b28b7b1ad56cd5ca0d3032ed0f56503d0aaba6b5467169dc596d96e1125e3` |
| `assets/hyperframes/vendor/MorphSVGPlugin.min.js` | `40e4246c7f898f5204a9d3f02c34672e7da589c297c157cdff714e87a362b045` |
| `assets/hyperframes/vendor/MotionPathPlugin.min.js` | `aa5f955ca4ce3095ebe5726f43a46b72532230edb3501b28fb853f189f023cab` |
| `assets/hyperframes/vendor/SplitText.min.js` | `3c38c97c364b3048ed6f7756388d2aa32580b81cf42932ea251b77fc626b3831` |
| `assets/hyperframes/vendor/gsap.min.js` | `c174bfce53a729418d57a8ad8625e7247c793a22fef8e2851e3cfa3de9cd8280` |
