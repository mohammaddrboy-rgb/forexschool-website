# Forex School (forexschool.store) — notes for Claude

Read `README.md` for how the site is built. Key rules:

- **Bilingual:** English pages at the root are the source of truth; `/fa/` (Dari) is generated.
  After editing any root page run `python build-fa.py` then `python build-geo.py`.
  Lessons: edit `_lessons/*.py` (never `lessons/*.html`), then run `python build-lessons.py` before build-fa.
  Articles: edit `_articles/articles.py` (newest first), then run `python build-articles.py` before build-fa.
  Brokers: edit `_brokers/brokers.py`, then run `python build-brokers.py` before build-fa.
  The live list is EMPTY on purpose (owner, 2026-10-29) — the page shows "coming soon" until the owner sends broker
  info; then add each broker (template in the file) with its `register_url` for the "Open an account" button.
  Old profiles (8 brokers) are in `_brokers/archive_2026-10.py` / branch `archive/brokers-v1` — don't republish unasked.
  Testimonials: add them to the carousel in `index.html` only, then run `python build-students.py`
  (before build-fa) — it syncs `students.html` and all student/city counts.
  After editing CSS/JS run `python bump-assets.py` first. Every visible string needs both
  `<span class="lang-en">` and `<span class="lang-fa">`.
- **Brand names:** "Forex School" in English, «مکتب فارکس» in Dari.
- **Wording (owner, 2026-11-01):** in Dari use «سشن», never «جلسه», for sessions (market sessions and class/service
  sessions alike). Only a central bank's *meeting* (e.g. FOMC) may stay «جلسه».
- **Workflow agreed with the owner:** make changes on the working branch, open a PR and merge it into
  `main`; a separate Claude session deploys `main` to the server when the owner asks.
  Keep `DEPLOY-NOTES.md` up to date whenever a page/file is removed, so the server copy gets cleaned up.
- **Motion:** GSAP + ScrollTrigger (`assets/vendor/`). Never put CSS `transition: transform` on elements
  GSAP animates; respect `prefers-reduced-motion`.

## Archived content
- **Islamic Finance section** — removed 2026-10-01, kept for possible return:
  branch `archive/islamic-finance` (full site before removal) and `_archive/islamic-finance/`
  (`RESTORE.md` explains exactly what was removed and how to put it back).

## Improvement backlog
- Owner (2026-11-01): do NOT remind them of suggestions after each task any more.
- Parked idea — "Next class dates" on the Join page (if courses run in groups): not to be built now. Mention it ONLY
  when the owner explicitly asks what could make the website better, together with any other suggestions.
- Weekly market outlook = the owner's **Forex TradeChi** editions (bilingual .md files). Publish each one as an article:
  `cat="outlook"`, `series=("Forex TradeChi · Edition N", "Forex TradeChi · شمارهٔ N")`, newest first, keep the owner's
  wording (incl. «دالر»), swap "[WHATSAPP CHANNEL LINK]" for the real channel (`wa` block), "comments" → Instagram/Facebook
  group, sources as a `links` block, hashtags left off the page. Edition 15 (2026-11-02) = `tradechi-15-triple-central-bank-week`.
Dropped by the owner 2026-10-30 — do NOT suggest again: beginner self-test quiz + certificate, visitor analytics,
setting up the email address (`info@forexschool.store` in the footer is still a placeholder).
Done: lesson pages (intro-only, full content archived — see README), Student Stories, more tools, WhatsApp contact,
Brokers section (profiles on hold), Services page (2026-10-30), Articles (2026-11-01, 6 evergreen articles),
Podcast Episode 1 (2026-11-01).

## Podcast — STANDING INSTRUCTIONS (owner, 2026-11-01): every new episode = exactly the Episode 1 package
Full step-by-step + scripts: `_podcast/production/README.md` (synth.py, assemble.py, design.html, render.js,
bars.py, mkvideo3.sh). Episode data: `_podcast/episodes.py` → `python build-podcast.py` (before build-fa). Media: `assets/podcast/`.
For each new recording the owner sends (they give the Dari title + subtitle; ask if missing):
1. **Audio**: voice chain (highpass 75 Hz, light afftdn, EQ −2.5 dB@200 Hz / +2.5 dB@3.2 kHz / +2 dB shelf@9 kHz, de-esser,
   compressor 3:1, long pauses trimmed to ~0.6 s) + the SAME original jingle (synth.py: 112 BPM, Am–F–C–G) as intro/outro.
2. **Website MP3**: −16 LUFS, **96 kbps joint stereo**, cover + ID3 tags → `assets/podcast/forex-school-podcast-eNN.mp3`,
   1400² cover JPG, new dict in `episodes.py` (newest first), build-podcast → build-fa → build-geo, PR + merge, DEPLOY-NOTES.
3. **Artwork** (design.html, same layout): 3000² episode cover, 1080² Instagram image, **1080×1920 Reel cover** (render-rc.js,
   static bars, fits the 3:4 grid crop), 1080² + 1080×1920 video backgrounds.
   Episode number in the ring («قسمت دوم», …), Dari title with one key word highlighted, English title, host photo.
4. **Social video** (−14 LUFS, `mkvideo3.sh`, CRF 24, 20 fps, AAC 128 kbps — scrolling orange level-bars, NOT the raw
   waveform; owner wants SMALL files with no visible quality loss): the full episode 1:1 (≈ 1.7 MB/min; E01 was 30.8 MB).
   **NO teasers** for future episodes (owner, 2026-11-02) — E01 had a Reel + square teaser, don't make them again.
5. **Deliver** the files in the chat with SendUserFile `display: "render"` (owner: "in the chat, not in the outputs").
6. **Always give a ready-to-paste caption + hashtags** (Dari first, short English line optional) for Instagram and the
   Facebook group — hook question/title, 1–2 lines on what the episode covers, "listen on forexschool.store (link in bio)",
   then hashtags, e.g. #فارکس #مکتب_فارکس #پادکست #ترید #معامله_گری #مدیریت_ریسک #افغانستان #forex #trading
   plus 2–4 topic-specific tags. Template in `_podcast/production/README.md`.
Episodes so far: E01 (2026-11-01) «چرا اکثر معامله‌گران تازه‌کار ضرر می‌کنند؟» — سه علت اصلی ضرر‌ده بودن تریدرهای تازه‌کار.
Brand: navy #060C17, orange #FA9939, Vazirmatn/Jakarta fonts, host photo assets/img/founder.jpg (480², keep it small).
Note: speech-to-text models can't be downloaded here (HuggingFace blocked), so ask the owner for the title/topic.
