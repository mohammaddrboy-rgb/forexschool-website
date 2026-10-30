# Deploy notes (for whoever updates the server)

Deploying = copying the site files from `main` onto the web server. Copying only adds/overwrites
files; it does **not** delete pages that were removed from the repo. Check this list on every deploy.

## Do not upload
- `_archive/` (archived content, not part of the live site)
- `_lessons/` (lesson source text used by `build-lessons.py`; the built pages are `lessons/` and `fa/lessons/` — DO upload those)
- `_brokers/` (broker data used by `build-brokers.py`; the built pages are `brokers.html` and `fa/brokers.html` — DO upload those.
  Since 2026-10-29 they show a "coming soon" box instead of the broker profiles — overwrite the old copies on the server)
- `*.md`, `*.py`, `.git*` (docs and build scripts)

## New pages (2026-10-30)
- `services.html` and `fa/services.html` — new Services page. Every HTML page changed too (menu/footer link and
  asset version `?v=20261030`), so upload all `*.html`, `fa/`, `lessons/`, `fa/lessons/`, `sitemap.xml` and `assets/css/global.css`.

## Files to DELETE from the server
| Since | File(s) | Why |
|---|---|---|
| 2026-10-01 | `islamic-finance.html`, `fa/islamic-finance.html` | Islamic Finance section removed (archived in `_archive/islamic-finance/`) |

After deleting, the old URLs should return the site's 404 page.
