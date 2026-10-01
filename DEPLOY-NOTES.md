# Deploy notes (for whoever updates the server)

Deploying = copying the site files from `main` onto the web server. Copying only adds/overwrites
files; it does **not** delete pages that were removed from the repo. Check this list on every deploy.

## Do not upload
- `_archive/` (archived content, not part of the live site)
- `*.md`, `*.py`, `.git*` (docs and build scripts)

## Files to DELETE from the server
| Since | File(s) | Why |
|---|---|---|
| 2026-10-01 | `islamic-finance.html`, `fa/islamic-finance.html` | Islamic Finance section removed (archived in `_archive/islamic-finance/`) |

After deleting, the old URLs should return the site's 404 page.
