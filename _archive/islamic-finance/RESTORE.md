# Islamic Finance section — archived

Removed from the live site on **2026-10-01** at the owner's request. Everything is kept so it can be
brought back quickly.

## Where the content lives
1. **Branch `archive/islamic-finance`** on GitHub — a frozen copy of the whole site *with* the
   section (commit `91f53ee`, the last version before removal). Never deploy or delete this branch.
2. **This folder** (`_archive/islamic-finance/`, not deployed to the server):
   - `islamic-finance.html` — the full English source page (the Dari page `fa/islamic-finance.html`
     is generated from it by `build-fa.py`, so it doesn't need its own copy).
   - `snippets.json` — every other piece that was removed, verbatim, keyed by where it came from.

## What was removed (keys in `snippets.json`)
| Key | Where | What |
|---|---|---|
| `nav-link` | every page, main menu | "Islamic Finance / فارکس اسلامی" link (after Courses) |
| `footer-link` | every page, footer "Explore" column | same link (after Courses) |
| `index-islamic-section` | `index.html` | "Forex in Islam" feature band (crescent icon), between the learning path and the tools section |
| `index-hero-chip` | `index.html` hero | "Halal framework / چارچوب حلال" floating chip (`chip-3`) |
| `faq-halal-item` | `faq.html` | first FAQ item, "Is forex halal? / آیا فارکس حلال است؟" |
| `faq-meta-description` | `faq.html` `<meta description>` | the words "is forex halal," |
| `disclaimer-clause-7` | `disclaimer.html` | clause "7. Islamic content is not a fatwa" (it was the last clause) |
| `about-bullet` | `about.html` | "Dedicated content on forex in Islam" bullet (last item of "What makes Forex School different") |
| `landing-feature-card` | `landing.html` | "Forex in Islam" feature card — replaced by a "A clear path / مسیری روشن" card |
| `llms-*` | `llms.txt` | summary line, page entry, FAQ wording, Dari link |
| `build-fa-desc`, `build-fa-faq-desc` | `build-fa.py` `FA_DESC` | Dari meta description for the page; FAQ description wording |
| `build-geo-knowsAbout` | `build-geo.py` | `"Islamic finance"` in the founder's `knowsAbout` |

The section's CSS (`.band-islamic`, `.crescent`) and JS (crescent animation) were left in
`assets/css/global.css` and `assets/js/site.js`, so restored markup will look and animate exactly as before.

## How to restore
1. `git checkout archive/islamic-finance -- islamic-finance.html` (or copy it from this folder).
2. Put each snippet from `snippets.json` back in its place (table above). For `nav-link` and
   `footer-link`, insert after the Courses link on every root `*.html` page. Undo the `landing.html`
   card swap and re-add the removed words/lines in `faq.html`, `llms.txt`, `build-fa.py`, `build-geo.py`.
3. Run `python build-fa.py` then `python build-geo.py` (regenerates `/fa/`, sitemap, structured data).
4. Commit, merge to `main`, then deploy as usual.
