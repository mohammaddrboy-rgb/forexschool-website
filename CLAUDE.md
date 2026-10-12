# Forex School (forexschool.store) — notes for Claude

Read `README.md` for how the site is built. Key rules:

- **Bilingual:** English pages at the root are the source of truth; `/fa/` (Dari) is generated.
  After editing any root page run `python build-fa.py` then `python build-geo.py`.
  Testimonials: add them to the carousel in `index.html` only, then run `python build-students.py`
  (before build-fa) — it syncs `students.html` and all student/city counts.
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

## Improvement backlog (suggested to the owner 2026-10-12, in priority order)
The owner asked: after finishing each item, remind them of the remaining ones in this order.
1. Lesson pages — one page per beginner lesson (key points, diagram, 3-question quiz); needs the owner's lesson material.
2. Fill the Articles page — weekly outlook, "5 beginner mistakes", "What is a pip" etc.
3. ~~Student Stories page~~ — DONE 2026-10-12 (`students.html`, synced by `build-students.py`).
4. ~~More tools~~ — DONE 2026-10-12: pip value calculator, margin & leverage calculator (the risk calculator already covers position size from stop-loss), market hours clock in Kabul time.
5. Beginner self-test quiz + shareable completion certificate.
6. Visitor analytics (privacy-friendly, e.g. Plausible/Umami) — needs the owner to pick/create an account.
7. Confirm the contact email (`info@forexschool.store` is a placeholder) / add a WhatsApp contact button.
8. "Next class dates" on the Join page, if courses run in groups.

## Pending / upcoming
- Podcast page (`podcast.html`) is a "coming soon" placeholder; the owner will supply episode files.
