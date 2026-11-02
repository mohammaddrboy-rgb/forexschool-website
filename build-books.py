#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build books.html (the "Books" page, linked from the footer under Resources) from _books/books.py.

Each book is a card: cover, title and author, chips (main focus, level, pages, year), an introduction,
a short summary and a download button for the book file (or a link to its official page).
While the list is empty the page shows a "coming soon" box. The page shell is copied from courses.html.

Run after editing _books/books.py (or the nav/footer), BEFORE build-fa.py:

    python build-books.py && python build-fa.py && python build-geo.py
"""
import io, os, re, sys, html

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_books"))
import books as B  # noqa: E402

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
WA = "https://whatsapp.com/channel/0029VbEBu2aKLaHmFI6owX2b"

def read(p): return io.open(p, encoding="utf-8").read()
def write(p, s): io.open(p, "w", encoding="utf-8").write(s)
def fa(s): return str(s).translate(FA_DIGITS)
def bi(pair):
    if isinstance(pair, str):
        pair = (pair, pair)
    return '<span class="lang-en">%s</span><span class="lang-fa">%s</span>' % pair

DL_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 4h2v8.2l3.3-3.3 1.4 1.4L12 16l-5.7-5.7 1.4-1.4 3.3 3.3zM5 18h14v2H5z"/></svg>'

def book_card(b):
    chips = ['<span class="chip-lite bk2-focus">%s</span>' % bi(b["focus"])]
    if b.get("level"):
        chips.append('<span class="chip-lite">%s</span>' % bi(b["level"]))
    if b.get("pages"):
        chips.append('<span class="chip-lite">%s</span>' % bi(("%s pages" % b["pages"], "%s صفحه" % fa(b["pages"]))))
    if b.get("year"):
        chips.append('<span class="chip-lite">%s</span>' % bi((b["year"], fa(b["year"]))))
    summary = "".join("<p>%s</p>" % bi(p) for p in b["summary"])
    if b.get("file"):
        meta = ""
        if b.get("size") or b.get("lang"):
            en = " · ".join(x for x in [b.get("lang", ("", ""))[0], b.get("size", "")] if x)
            f = " · ".join(x for x in [b.get("lang", ("", ""))[1], fa(b.get("size", "")).replace(".", "٫").replace("MB", "مگابایت")] if x)
            meta = ' <span class="bk2-meta">(%s)</span>' % bi((en, f))
        action = ('<a class="btn btn-gold bk2-dl" href="%s" download>%s<span>%s</span>%s</a>'
                  % (b["file"], DL_ICON, bi(("Download the book", "دانلود کتاب")), meta))
    elif b.get("link"):
        action = ('<a class="btn btn-outline bk2-dl" href="%s" target="_blank" rel="noopener">%s <span aria-hidden="true">↗</span></a>'
                  % (html.escape(b["link"]), bi(("Official page", "صفحهٔ رسمی کتاب"))))
    else:
        action = ""
    return """
        <article class="card bk2-book" id="%(id)s">
          <div class="bk2-cover"><img src="%(cover)s" alt="%(alt)s" loading="lazy"></div>
          <div class="bk2-body">
            <h2 class="bk2-title">%(title)s</h2>
            <p class="bk2-author">%(by)s</p>
            <div class="bk2-chips">%(chips)s</div>
            <h3 class="bk2-h">%(intro_t)s</h3>
            <p>%(intro)s</p>
            <h3 class="bk2-h">%(sum_t)s</h3>
            <div class="bk2-summary">%(summary)s</div>
            <div class="bk2-actions">%(action)s</div>
          </div>
        </article>""" % {
        "id": b["id"], "cover": b["cover"], "alt": html.escape("%s — %s" % (b["title"][0], b["author"][0])),
        "title": bi(b["title"]), "by": bi(("by " + b["author"][0], "نویسنده: " + b["author"][1])),
        "chips": "".join(chips), "intro_t": bi(("About the book", "معرفی کتاب")), "intro": bi(b["intro"]),
        "sum_t": bi(("Summary", "خلاصهٔ کتاب")), "summary": summary, "action": action,
    }

def build():
    src = read("courses.html")
    head_end = src.index('<div class="nav-backdrop"></div>\n') + len('<div class="nav-backdrop"></div>\n')
    foot_start = src.index('  <!-- Disclaimer band -->')
    top, bottom = src[:head_end], src[foot_start:]

    top = top.replace('data-title-en="Courses | Forex School"', 'data-title-en="Trading Books | Forex School"')
    top = top.replace('data-title-fa="درس‌ها | مکتب فارکس"', 'data-title-fa="کتاب‌های معامله‌گری | مکتب فارکس"')
    top = re.sub(r"<title>.*?</title>", "<title>Trading Books | Forex School</title>", top, count=1)
    desc = "Trading books recommended by Forex School — an introduction to each book and its author, a short summary, and a download link. In Dari and English."
    top = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, top, count=1)
    top = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + "Trading Books | Forex School", top, count=1)
    top = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + "Trading books with an introduction, summary and download link", top, count=1)
    top = top.replace("https://forexschool.store/courses.html", "https://forexschool.store/books.html")
    top = re.sub(r'  <link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', "", top)
    top = re.sub(r'  <script type="application/ld\+json">.*?</script>\n', "", top, flags=re.S)
    top = top.replace('<a href="/courses.html" class="active">', '<a href="/courses.html">')   # Books is footer-only
    bottom = re.sub(r'  <script src="/assets/js/lessons\.js[^"]*" defer></script>\n', "", bottom)
    bottom = bottom.replace("Join the WhatsApp channel to get the lessons", "Join the Forex School WhatsApp channel")
    bottom = bottom.replace("برای دریافت درس‌ها به کانال واتساپ بپیوند", "به کانال واتساپ مکتب فارکس بپیوندید")

    n = len(B.BOOKS)
    seen = set()
    for b in B.BOOKS:
        assert b["id"] not in seen, b["id"]; seen.add(b["id"])
        for k in ("title", "author", "focus", "cover", "intro", "summary"):
            assert b.get(k), (b["id"], "missing " + k)
    if n:
        listing = '\n      <div class="bk2-list">%s\n      </div>' % "".join(book_card(b) for b in B.BOOKS)
    else:
        listing = """
      <div class="empty-state">
        <span class="empty-ic" aria-hidden="true">📚</span>
        <h2>%s</h2>
        <p>%s</p>
        <a class="btn btn-gold" href="%s" target="_blank" rel="noopener">%s</a>
      </div>""" % (bi(("The first books are on their way", "نخستین کتاب‌ها در راه است")),
                   bi(("Here we will introduce the trading books we recommend — what each book focuses on and who wrote it, a short summary, and a link to download it. Join our WhatsApp channel to hear when the first books are added.",
                       "در اینجا کتاب‌های معامله‌گری پیشنهادی ما را معرفی می‌کنیم — موضوع اصلی هر کتاب و نویسندهٔ آن، خلاصه‌ای کوتاه و لینک دانلود. به کانال واتساپ ما بپیوندید تا از افزوده شدن نخستین کتاب‌ها باخبر شوید.")),
                   WA, bi(("Follow on WhatsApp", "دنبال کردن در واتساپ")))

    body = """
  <section class="page-head">
    <div class="container">
      <h1>%(h1)s</h1>
      <p>%(intro)s</p>
    </div>
  </section>

  <section class="section">
    <div class="container bk2-wrap">%(listing)s
    </div>
  </section>

""" % {
        "h1": bi(('Trading <span class="accent">Books</span>', 'کتاب‌های <span class="accent">معامله‌گری</span>')),
        "intro": bi(("Good books shorten the learning curve. Here we introduce trading books worth reading — what each one is about and who wrote it, a short summary of its main ideas, and a link to download it.",
                     "کتاب‌های خوب مسیر یادگیری را کوتاه‌تر می‌کنند. در اینجا کتاب‌های معامله‌گری ارزشمند را معرفی می‌کنیم — موضوع هر کتاب و نویسندهٔ آن، خلاصه‌ای کوتاه از ایده‌های اصلی و لینک دانلود.")),
        "listing": listing,
    }
    write("books.html", top + body + bottom)
    print("Built books.html with %d book(s)%s." % (n, "" if n else ' ("coming soon" box shown)'))

if __name__ == "__main__":
    build()
