# Forex School (forexschool.store) — notes for Claude

Read `README.md` for how the site is built. Key rules:

- **Bilingual:** English pages at the root are the source of truth; `/fa/` (Dari) is generated.
  After editing any root page run `python build-fa.py` then `python build-geo.py`.
  After editing CSS/JS run `python bump-assets.py` first. Every visible string needs both
  `<span class="lang-en">` and `<span class="lang-fa">`.
- **Brand names:** "Forex School" in English, «مکتب فارکس» in Dari.
- **Workflow agreed with the owner:** make changes on the working branch, open a PR and merge it into
  `main`; a separate Claude session deploys `main` to the server when the owner asks.
  Keep `DEPLOY-NOTES.md` up to date whenever a page/file is removed, so the server copy gets cleaned up.
- **Motion:** GSAP + ScrollTrigger (`assets/vendor/`). Never put CSS `transition: transform` on elements
  GSAP animates; respect `prefers-reduced-motion`.

## Archived content
- **Islamic Finance section** — removed 2026-10-01, kept for possible return:
  branch `archive/islamic-finance` (full site before removal) and `_archive/islamic-finance/`
  (`RESTORE.md` explains exactly what was removed and how to put it back).

## Pending / upcoming
- Podcast page (`podcast.html`) is a "coming soon" placeholder; the owner will supply episode files.
