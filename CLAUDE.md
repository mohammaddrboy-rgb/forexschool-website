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
The owner asked (2026-10-30): after EVERY completed task, remind them of the remaining item(s):
1. "Next class dates" on the Join page, if courses run in groups.
(Articles DONE 2026-11-01: 6 evergreen articles. A weekly market outlook needs the owner's own weekly view — offer to
publish it as an article whenever they send one.)
Dropped by the owner 2026-10-30 — do NOT suggest again: beginner self-test quiz + certificate, visitor analytics,
setting up the email address (`info@forexschool.store` in the footer is still a placeholder).
Done: lesson pages (intro-only, full content archived — see README), Student Stories, more tools, WhatsApp contact,
Brokers section (profiles on hold), Services page (2026-10-30).

## Podcast
- Episodes: `_podcast/episodes.py` → `python build-podcast.py` (before build-fa). Media in `assets/podcast/`.
- Episode 1 (2026-11-01) «چرا اکثر معامله‌گران تازه‌کار ضرر می‌کنند؟». Production recipe used (owner liked a "catchy" package):
  voice: highpass 75 Hz, light afftdn, EQ (−2.5 dB @200 Hz, +2.5 dB @3.2 kHz, +2 dB shelf @9 kHz), de-esser,
  compressor 3:1, long pauses trimmed to ~0.6 s; original synthesised intro/outro jingle (112 BPM, Am–F–C–G);
  podcast MP3 at −16 LUFS / 96 kbps joint stereo (owner wanted smaller files; no audible loss) with cover + ID3 tags; social versions at −14 LUFS: 9:16 Reel teaser and 1:1
  teaser (first ~75 s + outro chord) and a full 1:1 episode video (cover + live orange waveform + progress bar).
  Brand: navy #060C17, orange #FA9939; Vazirmatn/Jakarta fonts; host photo assets/img/founder.jpg.
