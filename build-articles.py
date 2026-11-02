#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the article pages (articles/*.html) and the article list on articles.html from _articles/articles.py.

Each article page has: a short "In short" box, the sections, a link to the matching free tool, a call to
join the classes and previous/next links. The page shell and the content blocks (tables, callouts,
formulas…) are shared with the lesson pages (build-lessons.py), so they look the same.
The list on articles.html sits between <!-- articles:list --> and <!-- /articles:list -->.

Run after editing _articles/articles.py (or the nav/footer), BEFORE build-fa.py:

    python build-articles.py && python build-fa.py && python build-geo.py
"""
import importlib.util, io, json, os, re, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "_articles"))
import articles as A  # noqa: E402

_spec = importlib.util.spec_from_file_location("build_lessons", os.path.join(ROOT, "build-lessons.py"))
L = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(L)
bi, render_block, fa, plain = L.bi, L.render_block, L.fa, L.plain

BASE = L.BASE
WA = L.WA

def read(p): return io.open(p, encoding="utf-8").read()
def write(p, s): io.open(p, "w", encoding="utf-8").write(s)

def file_of(a): return "articles/%s.html" % a["slug"]

def date_pair(d):
    y, m, day = (int(x) for x in d.split("-"))
    return ("%d %s %d" % (day, A.MONTHS[m - 1], y), "%s %s %s" % (fa(day), A.MONTHS_FA[m - 1], fa(y)))

def mins_pair(n): return ("%d min read" % n, "%s دقیقه مطالعه" % fa(n))

def shell():
    s = L.make_shell()
    # no menu item is "active" on article pages (Articles lives in the footer)
    s["header"] = s["header"].replace(' class="active"', "")
    s["after"] = s["after"].replace("Join the WhatsApp channel to get the lessons", "Get every new article — join the WhatsApp channel")
    s["after"] = s["after"].replace("برای دریافت درس‌ها به کانال واتساپ بپیوند", "هر مقالهٔ جدید را دریافت کنید — به کانال واتساپ بپیوندید")
    return s

def block(b):
    """Article blocks: the lesson blocks plus h3 sub-headings and a list of source links."""
    if b[0] == "h3":
        return "<h3>%s</h3>" % bi((b[1], b[2]))
    if b[0] == "links":   # [(label_en, label_fa, url)]
        return '<ul class="bullets art-sources">%s</ul>' % "".join(
            '<li><a href="%s" target="_blank" rel="nofollow noopener">%s</a></li>' % (html.escape(u), bi((en, f))) for en, f, u in b[1])
    if b[0] == "wa":      # WhatsApp channel button
        return '<p><a class="btn btn-gold" href="%s" target="_blank" rel="noopener">%s</a></p>' % (WA, bi(b[1]))
    return render_block(b)

def build_page(a, prev, nxt, sh):
    fn = file_of(a)
    cat = A.CATEGORIES[a["cat"]]
    title_en = "%s | Forex School" % plain(a["title"][0])
    title_fa = "%s | مکتب فارکس" % plain(a["title"][1])
    keys = '<ul class="check">%s</ul>' % "".join("<li>%s</li>" % bi(k) for k in a["key"])
    secs = "".join('<section class="lsec art-sec"><h2>%s</h2><div class="prose">%s</div></section>'
                   % (bi(h), "".join(block(b) for b in blocks)) for h, blocks in a["sections"])
    tool = ""
    if a.get("tool"):
        href, name, desc = a["tool"]
        tool = ('<a class="art-tool" href="%s"><span class="art-tool-ic" aria-hidden="true">🧮</span>'
                '<span class="art-tool-txt"><span class="art-tool-k">%s</span><b>%s</b><span>%s</span></span>'
                '<span class="art-tool-go" aria-hidden="true">→</span></a>'
                % (href, bi(("Free tool", "ابزار رایگان")), bi(name), bi(desc)))

    def pager(x, dirn):
        if not x:
            return '<span class="pager-empty"></span>'
        lab = {"prev": ("← Previous article", "→ مقالهٔ قبلی"), "next": ("Next article →", "مقالهٔ بعدی ←")}[dirn]
        return ('<a class="pager-%s" href="/%s"><span class="pager-dir">%s</span><span class="pager-title">%s</span></a>'
                % (dirn, file_of(x), bi(lab), bi(x["title"])))

    crumbs = ('<nav class="crumbs" aria-label="Breadcrumb"><a href="/articles.html">%s</a><span aria-hidden="true">/</span><span>%s</span></nav>'
              % (bi(("Articles", "مقالات")), bi(cat)))
    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": plain(a["title"][0]), "alternativeHeadline": plain(a["title"][1]),
          "description": a["desc"][0], "datePublished": a["date"], "dateModified": a.get("updated", a["date"]),
          "inLanguage": ["en", "fa"], "isAccessibleForFree": True, "articleSection": cat[0],
          "url": BASE + "/" + fn, "mainEntityOfPage": BASE + "/" + fn,
          "image": BASE + "/assets/img/og-image.jpg",
          "author": {"@type": "Organization", "name": "Forex School", "url": BASE},
          "publisher": {"@type": "EducationalOrganization", "name": "Forex School", "url": BASE,
                        "logo": {"@type": "ImageObject", "url": BASE + "/assets/img/logo.png"}}}

    body = """
  <section class="page-head lesson-head">
    <div class="container">
      %(crumbs)s
      <span class="badge">%(badge)s</span>
      <h1>%(h1)s</h1>
      <p>%(sub)s</p>
      <div class="lmeta">%(series)s<span class="chip-lite">%(date)s</span><span class="chip-lite">%(mins)s</span></div>
    </div>
  </section>

  <section class="section">
    <div class="container art-wrap">
      <article class="lesson-article">
        <div class="card lkeys">
          <h2 class="lkeys-title">%(keys_t)s</h2>
          <div class="prose">%(keys)s</div>
        </div>
        %(secs)s
        %(tool)s
        <div class="lintro-cta">
          <h2>%(cta_h)s</h2>
          <p>%(cta_p)s</p>
          <div class="lintro-btns">
            <a class="btn btn-gold" href="%(wa)s" target="_blank" rel="noopener">%(cta_join)s</a>
            <a class="btn btn-outline" href="/courses.html">%(cta_courses)s</a>
          </div>
        </div>
        <p class="art-disc">%(disc)s</p>
        <nav class="lesson-pager" aria-label="Article navigation">%(prev)s%(next)s</nav>
        <p class="lesson-back"><a href="/articles.html">%(back)s</a></p>
      </article>
    </div>
  </section>
""" % {
        "crumbs": crumbs, "badge": bi(cat),
        "series": ('<span class="chip-lite chip-series">%s</span>' % bi(a["series"])) if a.get("series") else "", "h1": bi(a["title"]), "sub": bi(a["sub"]),
        "date": bi(date_pair(a["date"])), "mins": bi(mins_pair(a["mins"])),
        "keys_t": bi(("In short", "به‌طور خلاصه")), "keys": keys, "secs": secs, "tool": tool,
        "cta_h": bi(("Learn it properly — in our classes", "این را درست بیاموزید — در کلاس‌های ما")),
        "cta_p": bi(("This article is a short guide. In our free online classes we go deeper — with live charts, practice and answers to your questions. Join the Forex School WhatsApp channel to take part.",
                     "این مقاله یک راهنمای کوتاه است. در کلاس‌های آنلاین و رایگان ما عمیق‌تر می‌رویم — با نمودارهای زنده، تمرین و پاسخ به پرسش‌های شما. برای شرکت، به کانال واتساپ مکتب فارکس بپیوندید.")),
        "wa": WA, "cta_join": bi(("Join the online classes", "پیوستن به کلاس‌های آنلاین")),
        "cta_courses": bi(("See the courses", "دیدن دوره‌ها")),
        "disc": bi(("Educational content only — not financial advice. Forex trading carries a high risk of losing money.",
                    "این مطلب فقط آموزشی است و توصیهٔ مالی نیست. معامله در فارکس با ریسک بالای از دست دادن پول همراه است.")),
        "prev": pager(prev, "prev"), "next": pager(nxt, "next"),
        "back": bi(("↑ All articles", "↑ همهٔ مقالات")),
    }

    head = sh["head"]
    head = head.replace("__TITLE_EN__", html.escape(title_en)).replace("__TITLE_FA__", html.escape(title_fa))
    head = head.replace("__DESC__", html.escape(a["desc"][0])).replace("__DESC_FA__", html.escape(a["desc"][1]))
    head = head.replace("__URL__", BASE + "/" + fn)
    head = head.replace("__JSONLD__", json.dumps(ld, ensure_ascii=False))
    write(fn, head + sh["header"] + body + sh["after"])
    return fn

def card(a):
    cat = A.CATEGORIES[a["cat"]]
    return """
        <article class="card art-card" data-cat="%(cat_id)s">
          <div class="art-card-top"><span class="art-ic" aria-hidden="true">%(icon)s</span><span class="badge">%(cat)s</span></div>
          <h3><a href="/%(href)s">%(title)s</a></h3>
          <p>%(summary)s</p>
          <div class="art-card-foot">
            <span class="art-card-meta">%(date)s · %(mins)s</span>
            <span class="art-more" aria-hidden="true">%(read)s</span>
          </div>
        </article>""" % {
        "cat_id": a["cat"], "icon": a["icon"], "cat": bi(cat), "href": file_of(a), "title": bi(a["title"]),
        "summary": bi(a["summary"]), "date": bi(date_pair(a["date"])), "mins": bi(mins_pair(a["mins"])),
        "read": bi(("Read →", "خواندن ←")),
    }

def build_list():
    used = [c for c in A.CATEGORIES if any(a["cat"] == c for a in A.ARTICLES)]
    chips = ['<button type="button" class="art-chip" data-filter="all" aria-pressed="true">%s</button>' % bi(("All", "همه"))]
    chips += ['<button type="button" class="art-chip" data-filter="%s" aria-pressed="false">%s</button>' % (c, bi(A.CATEGORIES[c])) for c in used]
    block = """<!-- articles:list (generated by build-articles.py from _articles/articles.py — do not edit by hand) -->
      <div class="art-filter" role="group" aria-label="Filter articles by topic">%(chips)s</div>
      <div class="grid-3 art-grid">%(cards)s
      </div>
      <script>
        /* Articles: filter the cards by topic */
        (function () {
          var chips = document.querySelectorAll('.art-chip');
          chips.forEach(function (c) {
            c.addEventListener('click', function () {
              var f = c.getAttribute('data-filter');
              chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
              document.querySelectorAll('.art-card').forEach(function (card) {
                card.hidden = !(f === 'all' || card.getAttribute('data-cat') === f);
              });
            });
          });
        })();
      </script>
      <!-- /articles:list -->""" % {"chips": "".join(chips), "cards": "".join(card(a) for a in A.ARTICLES)}
    src = read("articles.html")
    new, n = re.subn(r"<!-- articles:list.*?<!-- /articles:list -->", lambda m: block, src, count=1, flags=re.S)
    if not n:
        raise SystemExit("articles.html: markers <!-- articles:list --> ... <!-- /articles:list --> not found")
    write("articles.html", new)

def main():
    os.makedirs("articles", exist_ok=True)
    sh = shell()
    seen, built = set(), []
    arts = A.ARTICLES
    for i, a in enumerate(arts):
        assert a["slug"] not in seen, a["slug"]; seen.add(a["slug"])
        assert a["cat"] in A.CATEGORIES, (a["slug"], a["cat"])
        built.append(build_page(a, arts[i - 1] if i else None, arts[i + 1] if i + 1 < len(arts) else None, sh))
    for f in os.listdir("articles"):
        if f.endswith(".html") and "articles/" + f not in built:
            os.remove(os.path.join("articles", f))
            print("removed stale articles/" + f)
    build_list()
    print("Built %d article pages and the list on articles.html." % len(built))

if __name__ == "__main__":
    main()
