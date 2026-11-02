# Deploy notes (for whoever updates the server)

Deploying = copying the site files from `main` onto the web server. Copying only adds/overwrites
files; it does **not** delete pages that were removed from the repo. Check this list on every deploy.

## Do not upload
- `_archive/` (archived content, not part of the live site)
- `_lessons/` (lesson source text used by `build-lessons.py`; the built pages are `lessons/` and `fa/lessons/` — DO upload those)
- `_brokers/` (broker data used by `build-brokers.py`; the built pages are `brokers.html` and `fa/brokers.html` — DO upload those.
  Since 2026-10-29 they show a "coming soon" box instead of the broker profiles — overwrite the old copies on the server)
- `_articles/` (article source text used by `build-articles.py`; the built pages are `articles/` and `fa/articles/` — DO upload those)
- `_podcast/` (episode data used by `build-podcast.py`; the media lives in `assets/podcast/` — DO upload that)
- `_books/` (book data used by `build-books.py`; the built pages are `books.html` / `fa/books.html`, files go in `assets/books/` — DO upload those)
- `*.md`, `*.py`, `.git*` (docs and build scripts)

## New pages (2026-10-30)
- `services.html` and `fa/services.html` — new Services page. Every HTML page changed too (menu/footer link and
  asset version `?v=20261030`), so upload all `*.html`, `fa/`, `lessons/`, `fa/lessons/`, `sitemap.xml` and `assets/css/global.css`.

## New pages (2026-11-01)
- New folders `articles/` and `fa/articles/` (6 article pages each). `articles.html` and `fa/articles.html` changed,
  and every HTML page has the new asset version `?v=20261101b` — upload all `*.html`, `fa/`, `lessons/`, `fa/lessons/`,
  `articles/`, `fa/articles/`, `sitemap.xml` and `assets/css/global.css`.

## Wording update (2026-11-01)
- Dari «جلسه» → «سشن» across the site: upload `index.html`, `students.html`, `services.html`, `tools.html`,
  `market-hours.html`, `articles.html`, `articles/` and the matching `fa/` pages (or simply all `*.html` + `fa/` + `articles/`).

## Podcast (2026-11-01)
- New folder `assets/podcast/` (episode MP3 ~13.6 MB at 96 kbps — replaced 2026-11-01 from the first 18 MB upload, overwrite it — + cover JPGs) — upload it. `podcast.html` / `fa/podcast.html` now show
  Episode 1 with an audio player; every HTML page has asset version `?v=20261101c` (upload all `*.html`, `fa/`, `lessons/`,
  `articles/`, `fa/lessons/`, `fa/articles/`, `sitemap.xml`, `assets/css/global.css`).
- The web server must serve `.mp3` with byte-range support (nginx/Apache do this by default) so listeners can skip/seek.
  Check after deploy: `curl -sI -H "Range: bytes=0-99" https://forexschool.store/assets/podcast/forex-school-podcast-e01.mp3`
  should answer `206 Partial Content`.

## New article (2026-11-02)
- `articles/triple-central-bank-week-november-2026.html` + `fa/articles/…` (weekly outlook).
  (It was first published as `…/tradechi-15-triple-central-bank-week.html` — see the delete list below.)
  `articles.html` / `fa/articles.html` and all article pages changed; every HTML page has asset version `?v=20261102`
  — upload all `*.html`, `fa/`, `lessons/`, `articles/`, `fa/lessons/`, `fa/articles/`, `sitemap.xml`, `assets/css/global.css`.

## New page (2026-11-02): Books
- `books.html` and `fa/books.html` (new, "coming soon" for now) + a "Books / کتاب‌ها" footer link on every page; asset
  version `?v=20261102b` — upload all `*.html`, `fa/`, `lessons/`, `articles/`, `fa/lessons/`, `fa/articles/`, `sitemap.xml`,
  `assets/css/global.css`. Later, book files will be added under `assets/books/`.

## Files to DELETE from the server
| Since | File(s) | Why |
|---|---|---|
| 2026-10-01 | `islamic-finance.html`, `fa/islamic-finance.html` | Islamic Finance section removed (archived in `_archive/islamic-finance/`) |
| 2026-11-02 | `articles/tradechi-15-triple-central-bank-week.html`, `fa/articles/tradechi-15-triple-central-bank-week.html` | Article renamed to `triple-central-bank-week-november-2026.html` (owner: no brand/edition in URLs) — delete if it was uploaded |

After deleting, the old URLs should return the site's 404 page.
