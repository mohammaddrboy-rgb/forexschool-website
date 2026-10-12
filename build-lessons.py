#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the lesson pages (lessons/*.html) from the lesson content in _lessons/.

Every beginner and advanced lesson has its own bilingual page: key points, the lesson
itself (sections, tables, a diagram), homework and a 3-question quiz. The text lives in
  _lessons/beginner.py   — the 13 beginner lessons
  _lessons/advanced.py   — the 21 advanced lessons (modules F, A, AS, B, C, D — in that order)
  _lessons/diagrams.py   — the inline SVG diagrams (one per lesson)
The header/footer are copied from courses.html, so nav/footer changes carry over.
It also points every lesson row on courses.html at its page.

Run it after editing any lesson (or the nav/footer), BEFORE build-fa.py:

    python build-lessons.py && python build-fa.py && python build-geo.py
"""
import io, os, re, sys, json, html

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lessons"))
import beginner, advanced, diagrams, intros  # noqa: E402

# The owner decided (2026-10-12) that the website shows only a SHORT INTRODUCTION per lesson
# (_lessons/intros.py) and a call to join — the full lessons are an incentive
# to join the online classes. The full text stays in _lessons/ (and on branch archive/full-lessons);
# set PUBLISH_FULL = True to publish complete lesson pages again (key points, diagrams, quiz…).
PUBLISH_FULL = False

BASE = "https://forexschool.store"
FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
WA = "https://whatsapp.com/channel/0029VbEBu2aKLaHmFI6owX2b"

def read(p): return io.open(p, encoding="utf-8").read()
def write(p, s): io.open(p, "w", encoding="utf-8").write(s)
def fa(n): return str(n).translate(FA_DIGITS)

def bi(pair, tag="span", cls=""):
    """Bilingual text: ("en", "fa") -> <span class="lang-en">…</span><span class="lang-fa">…</span>."""
    if isinstance(pair, str):
        pair = (pair, pair)
    en, f = pair
    c = (" " + cls) if cls else ""
    return '<%s class="lang-en%s">%s</%s><%s class="lang-fa%s">%s</%s>' % (tag, c, en, tag, tag, c, f, tag)

def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s))

# --------------------------------------------------------------------------- lessons
COURSES = {
    "beginner": {"lessons": beginner.LESSONS, "name": ("Beginner Course — Forex from Zero", "دوره پایه — فارکس از صفر"),
                 "short": ("Beginner course", "دورهٔ پایه"), "anchor": "beginner"},
    "advanced": {"lessons": advanced.LESSONS, "name": ("Advanced Course — Level Two", "دوره پیشرفته — سطح دوم"),
                 "short": ("Advanced course", "دورهٔ پیشرفته"), "anchor": "advanced"},
}
MODULES = advanced.MODULES

def file_of(L):
    return "lessons/%s-%s-%s.html" % (L["course"], L["code"].lower(), L["slug"])

def code_label(L):
    """'01' / 'F1' — Persian digits for the Dari side."""
    return (L["code"], fa(L["code"]) if L["course"] == "beginner" else L["code"])

# --------------------------------------------------------------------------- blocks
def li_items(items, cls):
    return '<ul class="%s">%s</ul>' % (cls, "".join("<li>%s</li>" % bi(i) for i in items))

def cell(c, tag):
    if isinstance(c, str):
        return "<%s>%s</%s>" % (tag, c, tag)
    return "<%s>%s</%s>" % (tag, bi(c), tag)

def render_block(b):
    k = b[0]
    if k == "p":
        return "<p>%s</p>" % bi((b[1], b[2]))
    if k == "ul":
        return li_items(b[1], "bullets")
    if k == "check":
        return li_items(b[1], "check")
    if k == "ol":
        return '<ol class="steps-list">%s</ol>' % "".join("<li>%s</li>" % bi(i) for i in b[1])
    if k in ("note", "warn", "tip"):
        title, body = b[1], b[2]
        icon = {"note": "💡", "warn": "⚠️", "tip": "✅"}[k]
        t = '<strong class="callout-title">%s</strong>' % bi(title) if title else ""
        return '<div class="callout callout-%s"><span class="callout-ic" aria-hidden="true">%s</span><div>%s<p>%s</p></div></div>' % (k, icon, t, bi(body))
    if k == "quote":
        return '<blockquote class="lquote"><p>%s</p><cite>%s</cite></blockquote>' % (bi(b[1]), bi(b[2]))
    if k == "table":
        head, rows = b[1], b[2]
        ltr = ' dir="ltr"' if len(b) > 3 and b[3] == "ltr" else ""
        th = "".join(cell(c, "th") for c in head)
        body = "".join("<tr>%s</tr>" % "".join(cell(c, "td") for c in r) for r in rows)
        return '<div class="table-wrap ltable"><table class="data"%s><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (ltr, th, body)
    if k == "cmp":
        cols = []
        for tone, title, items in b[1]:
            cols.append('<div class="cmp-col cmp-%s"><h4>%s</h4><ul>%s</ul></div>' % (tone, bi(title), "".join("<li>%s</li>" % bi(i) for i in items)))
        return '<div class="cmp">%s</div>' % "".join(cols)
    if k == "stats":
        return '<div class="lstats">%s</div>' % "".join(
            '<div class="lstat"><b>%s</b><span>%s</span></div>' % (bi(big), bi(lbl)) for big, lbl in b[1])
    if k == "formula":
        exp = '<p class="formula-exp">%s</p>' % bi(b[2]) if len(b) > 2 and b[2] else ""
        if isinstance(b[1], tuple):   # a bilingual formula written in words
            return '<div class="formula"><div class="formula-eq">%s</div>%s</div>' % (bi(b[1]), exp)
        return '<div class="formula"><div class="formula-eq" dir="ltr">%s</div>%s</div>' % (b[1], exp)
    if k == "fig":
        svg = diagrams.render(b[1])
        cap = '<figcaption>%s</figcaption>' % bi(b[2]) if len(b) > 2 and b[2] else ""
        return '<figure class="lfig">%s%s</figure>' % (svg, cap)
    if k == "case":
        items = "".join("<li>%s</li>" % bi(i) for i in b[2])
        return '<div class="case"><span class="case-tag">%s</span><h4>%s</h4><ul>%s</ul><p class="case-out">%s</p></div>' % (
            bi(("Case study", "مطالعهٔ موردی")), bi(b[1]), items, bi(b[3]))
    raise ValueError("unknown block %r" % (k,))

# --------------------------------------------------------------------------- page
def extract(src, start, end):
    i = src.index(start); j = src.index(end, i) + len(end)
    return src[i:j]

def build_page(L, prev, nxt, idx, total, shell):
    course = COURSES[L["course"]]
    fn = file_of(L)
    en_t, fa_t = L["title"]
    title_en = "%s — Lesson %s | Forex School" % (plain(en_t), L["code"])
    title_fa = "%s — درس %s | مکتب فارکس" % (plain(fa_t), code_label(L)[1])
    desc_en, desc_fa = L["desc"]
    num_en, num_fa = code_label(L)

    if L["course"] == "beginner":
        where = (("Lesson %s of %d" % (L["code"], total)), ("درس %s از %s" % (fa(L["code"]), fa(total))))
    else:
        m = MODULES[L["module"]]
        where = (("Module %s · %s" % (L["module"], m["en"])), ("ماژول %s · %s" % (L["module"], m["fa"])))

    # table of contents
    toc = [("keys", ("Key points", "نکات کلیدی"))]
    sec_html = []
    for i, (h, blocks) in enumerate(L["sections"], 1):
        sid = "s%d" % i
        toc.append((sid, h))
        sec_html.append(
            '<section class="lsec" id="%s"><h2><span class="lsec-num">%s</span>%s</h2><div class="prose">%s</div></section>'
            % (sid, bi((str(i), fa(i))), bi(h), "".join(render_block(b) for b in blocks)))
    toc.append(("homework", ("Homework", "کارخانگی")))
    toc.append(("quiz", ("Quick quiz", "آزمونک")))

    keys = '<ul class="check">%s</ul>' % "".join("<li>%s</li>" % bi(k) for k in L["key"])

    hw = []
    for item in L["homework"]:
        if len(item) == 3:
            q, ans = (item[0], item[1]), item[2]
            hw.append('<li>%s<details class="hw-ans"><summary>%s</summary><p>%s</p></details></li>'
                      % (bi(q), bi(("Show answer", "نمایش جواب")), bi(ans)))
        else:
            hw.append("<li>%s</li>" % bi(item))

    quiz = []
    for qi, (q, opts, correct, why) in enumerate(L["quiz"], 1):
        ob = "".join('<button type="button" class="q-opt" data-i="%d"><span class="q-letter" aria-hidden="true">%s</span>%s</button>'
                     % (oi, bi(("ABCD"[oi], "الف ب ج د".split()[oi])), bi(o)) for oi, o in enumerate(opts))
        quiz.append('<div class="q" data-correct="%d"><p class="q-text"><span class="q-n">%s</span>%s</p><div class="q-opts">%s</div><p class="q-why" hidden>%s</p></div>'
                    % (correct, bi((str(qi), fa(qi))), bi(q), ob, bi(why)))

    def pager_link(Lx, dirn):
        if not Lx:
            return '<span class="pager-empty"></span>'
        lab = {"prev": ("← Previous lesson", "→ درس قبلی"), "next": ("Next lesson →", "درس بعدی ←")}[dirn]
        n_en, n_fa = code_label(Lx)
        return ('<a class="pager-%s" href="/%s"><span class="pager-dir">%s</span><span class="pager-title">%s</span></a>'
                % (dirn, file_of(Lx), bi(lab), bi(("%s · %s" % (n_en, Lx["title"][0]), "%s · %s" % (n_fa, Lx["title"][1])))))

    crumbs = ('<nav class="crumbs" aria-label="Breadcrumb"><a href="/courses.html">%s</a><span aria-hidden="true">/</span>'
              '<a href="/courses.html#%s">%s</a><span aria-hidden="true">/</span><span>%s</span></nav>'
              % (bi(("Courses", "درس‌ها")), course["anchor"], bi(course["short"]), bi(("Lesson " + num_en, "درس " + num_fa))))

    meta_chips = '<div class="lmeta"><span class="chip-lite">%s</span><span class="chip-lite">%s</span><span class="chip-lite">%s</span></div>' % (
        bi(where), bi(("%d min read" % L["mins"], "%s دقیقه مطالعه" % fa(L["mins"]))), bi(("3-question quiz", "آزمونک ۳ پرسشی")))

    ld = {"@context": "https://schema.org", "@type": "LearningResource",
          "name": plain(en_t), "alternateName": plain(fa_t), "description": desc_en,
          "learningResourceType": "Lesson", "inLanguage": ["en", "fa"], "isAccessibleForFree": True,
          "educationalLevel": "Beginner" if L["course"] == "beginner" else "Advanced",
          "position": idx, "url": BASE + "/" + fn,
          "isPartOf": {"@type": "Course", "name": course["name"][0], "url": BASE + "/courses.html#" + course["anchor"]},
          "provider": {"@type": "EducationalOrganization", "name": "Forex School", "url": BASE}}

    remember = ""
    if L.get("remember"):
        remember = '<div class="lremember"><span class="eyebrow">%s</span><p>%s</p></div>' % (bi(("Remember", "یادتان باشد")), bi(L["remember"]))

    body = """
  <section class="page-head lesson-head">
    <div class="container">
      %(crumbs)s
      <span class="badge">%(badge)s</span>
      <h1>%(h1)s</h1>
      <p>%(sub)s</p>
      %(meta)s
    </div>
  </section>

  <section class="section lesson-main" data-lesson="%(id)s">
    <div class="container lesson-layout">
      <aside class="lesson-toc" aria-label="%(toc_label)s">
        <p class="toc-title">%(toc_title)s</p>
        <ol>%(toc)s</ol>
      </aside>
      <article class="lesson-article">
        <div class="card lkeys" id="keys">
          <h2 class="lkeys-title">%(keys_title)s</h2>
          <div class="prose">%(keys)s</div>
        </div>
        %(sections)s
        <section class="lsec card lhw" id="homework">
          <h2>%(hw_title)s</h2>
          <ol class="steps-list">%(hw)s</ol>
        </section>
        <section class="lsec card lquiz" id="quiz">
          <h2>%(quiz_title)s</h2>
          <p class="quiz-intro">%(quiz_intro)s</p>
          %(quiz)s
          <div class="quiz-result" hidden>
            <p class="quiz-score"></p>
            <button type="button" class="btn btn-outline quiz-reset">%(retry)s</button>
          </div>
        </section>
        %(remember)s
        <nav class="lesson-pager" aria-label="%(pager_label)s">%(prev)s%(next)s</nav>
        <p class="lesson-back"><a href="/courses.html#%(anchor)s">%(back)s</a></p>
      </article>
    </div>
  </section>
""" % {
        "crumbs": crumbs,
        "badge": bi((("Beginner · Lesson " + num_en) if L["course"] == "beginner" else ("Advanced · " + num_en),
                     ("دورهٔ پایه · درس " + num_fa) if L["course"] == "beginner" else ("دورهٔ پیشرفته · " + num_fa))),
        "h1": bi(L["title"]), "sub": bi(L["sub"]), "meta": meta_chips, "id": L["id"],
        "toc_label": "Lesson contents", "toc_title": bi(("In this lesson", "در این درس")),
        "toc": "".join('<li><a href="#%s">%s</a></li>' % (a, bi(t)) for a, t in toc),
        "keys_title": bi(("Key points", "نکات کلیدی")), "keys": keys,
        "sections": "\n        ".join(sec_html),
        "hw_title": bi(("Homework", "کارخانگی")), "hw": "".join(hw),
        "quiz_title": bi(("Quick quiz", "آزمونک")),
        "quiz_intro": bi(("Three questions to check what you learned. Pick an answer to see if you are right — get all three to mark this lesson as done.",
                          "سه پرسش برای سنجش آنچه آموختید. یک گزینه را انتخاب کنید تا ببینید درست است یا نه — با پاسخ درست به هر سه، این درس تکمیل‌شده علامت می‌خورد.")),
        "quiz": "\n          ".join(quiz), "retry": bi(("Try again", "دوباره امتحان کنید")),
        "remember": remember, "pager_label": "Lesson navigation",
        "prev": pager_link(prev, "prev"), "next": pager_link(nxt, "next"),
        "anchor": course["anchor"], "back": bi(("↑ All lessons of the " + course["short"][0].lower(), "↑ همهٔ درس‌های " + course["short"][1])),
    }

    if not PUBLISH_FULL:
        body = intro_body(L, crumbs, where, num_en, num_fa, pager_link(prev, "prev"), pager_link(nxt, "next"), course)

    head = shell["head"]
    head = head.replace("__TITLE_EN__", html.escape(title_en)).replace("__TITLE_FA__", html.escape(title_fa))
    head = head.replace("__DESC__", html.escape(desc_en)).replace("__DESC_FA__", html.escape(desc_fa))
    head = head.replace("__URL__", BASE + "/" + fn)
    head = head.replace("__JSONLD__", json.dumps(ld, ensure_ascii=False))

    page = head + shell["header"] + body + shell["after"]
    write(fn, page)
    return fn

def intro_body(L, crumbs, where, num_en, num_fa, prev_html, next_html, course):
    """The public lesson page: a short introduction and a call to join the online classes."""
    topics = "".join("<li>%s</li>" % bi(h) for h, _ in L["sections"])
    return """
  <section class="page-head lesson-head">
    <div class="container">
      %(crumbs)s
      <span class="badge">%(badge)s</span>
      <h1>%(h1)s</h1>
      <p>%(sub)s</p>
      <div class="lmeta"><span class="chip-lite">%(where)s</span><span class="chip-lite">%(live)s</span></div>
    </div>
  </section>

  <section class="section lesson-main" data-lesson="%(id)s">
    <div class="container lesson-intro">
      <div class="card lintro-card">
        <h2>%(about)s</h2>
        <p class="lintro-text">%(intro)s</p>
      </div>
      <div class="lintro-cta">
        <h2>%(cta_h)s</h2>
        <p>%(cta_p)s</p>
        <div class="lintro-btns">
          <a class="btn btn-gold" href="%(wa)s" target="_blank" rel="noopener">%(cta_join)s</a>
          <a class="btn btn-outline" href="/join.html">%(cta_how)s</a>
        </div>
      </div>
      <nav class="lesson-pager" aria-label="Lesson navigation">%(prev)s%(next)s</nav>
      <p class="lesson-back"><a href="/courses.html#%(anchor)s">%(back)s</a></p>
    </div>
  </section>
""" % {
        "crumbs": crumbs,
        "badge": bi((("Beginner · Lesson " + num_en) if L["course"] == "beginner" else ("Advanced · " + num_en),
                     ("دورهٔ پایه · درس " + num_fa) if L["course"] == "beginner" else ("دورهٔ پیشرفته · " + num_fa))),
        "h1": bi(L["title"]), "sub": bi(L["sub"]), "where": bi(where),
        "live": bi(("Taught in our online classes", "در کلاس‌های آنلاین تدریس می‌شود")), "id": L["id"],
        "about": bi(("About this lesson", "دربارهٔ این درس")), "intro": bi(intros.INTROS[L["id"]]),
        "cover": bi(("What we cover in class", "آنچه در کلاس می‌آموزید")), "topics": topics,
        "cta_h": bi(("Want the full lesson?", "درس کامل را می‌خواهید؟")),
        "cta_p": bi(("The complete lesson — with worked examples, charts, homework and answers to your questions — is taught in our free online classes. Join the Forex School WhatsApp channel to take part.",
                     "درس کامل — همراه با مثال‌های عملی، نمودارها، کارخانگی و پاسخ به پرسش‌های شما — در کلاس‌های آنلاین و رایگان ما تدریس می‌شود. برای شرکت، به کانال واتساپ مکتب فارکس بپیوندید.")),
        "wa": WA, "cta_join": bi(("Join the online classes", "پیوستن به کلاس‌های آنلاین")),
        "cta_how": bi(("How to join", "چگونه عضو شویم")),
        "prev": prev_html, "next": next_html, "anchor": course["anchor"],
        "back": bi(("↑ All lessons of the " + course["short"][0].lower(), "↑ همهٔ درس‌های " + course["short"][1])),
    }

def make_shell():
    src = read("courses.html")
    ver = re.search(r'global\.css\?v=([^"]+)"', src).group(1)
    head_scripts = re.findall(r"  <script>\(function\(\)\{.*?</script>\n", src)
    header = extract(src, '  <header class="nav">', '<div class="nav-backdrop"></div>\n')
    # the Courses nav link stays active on lesson pages (copied as-is)
    footer = extract(src, '  <!-- Disclaimer band -->', "</footer>\n")
    if PUBLISH_FULL:
        footer = footer.replace("Join the WhatsApp channel to get the lessons", "Questions about this lesson? Ask in the WhatsApp channel")
        footer = footer.replace("برای دریافت درس‌ها به کانال واتساپ بپیوند", "پرسشی دربارهٔ این درس دارید؟ در کانال واتساپ بپرسید")
    head = """<!DOCTYPE html>
<html lang="en" dir="ltr"
      data-title-en="__TITLE_EN__"
      data-title-fa="__TITLE_FA__"
      data-desc-fa="__DESC_FA__">
<head>
  <meta charset="UTF-8">
%(scripts)s  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#060C17">
  <title>__TITLE_EN__</title>
  <meta name="description" content="__DESC__">
  <meta property="og:title" content="__TITLE_EN__">
  <meta property="og:description" content="__DESC__">
  <meta property="og:image" content="https://forexschool.store/assets/img/og-image.jpg?v=%(ver)s">
  <meta property="og:url" content="__URL__">
  <meta property="og:type" content="article">
  <link rel="canonical" href="__URL__">
  <link rel="icon" href="/assets/img/favicon.ico" sizes="any">
  <link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/assets/img/favicon-16.png">
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preload" href="/assets/fonts/jakarta-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/assets/fonts/vazirmatn-arabic.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/css/global.css?v=%(ver)s">
  <script type="application/ld+json">__JSONLD__</script>
</head>
<body>

""" % {"scripts": "".join(head_scripts), "ver": ver}
    after = "\n" + footer + """
  <script src="/assets/vendor/gsap.min.js" defer></script>

  <script src="/assets/vendor/ScrollTrigger.min.js" defer></script>

%(lessons_js)s  <script src="/assets/js/site.js?v=%(ver)s" defer></script>
</body>
</html>
""" % {"ver": ver, "lessons_js": ('  <script src="/assets/js/lessons.js?v=%s" defer></script>\n' % ver) if PUBLISH_FULL else ""}
    return {"head": head, "header": header, "after": after}

# --------------------------------------------------------------------------- courses.html links
def link_courses(all_lessons):
    src = read("courses.html")
    n = 0
    for L in all_lessons:
        en_t = L.get("list_title", L["title"][0])
        # find the lesson row by its English title, then rewrite its button
        pat = re.compile(r'(<div class="lesson")(?: data-lesson="[^"]*")?(><div class="lesson-num">(?:(?!</div><a).)*?<span class="lang-en">%s</span>.*?</h4></div>)<a class="btn btn-gold" href="[^"]*"(?: target="_blank" rel="noopener")?><span class="lang-en">[^<]*</span><span class="lang-fa">[^<]*</span></a>'
                         % re.escape(en_t), re.S)
        rep = (r'\1 data-lesson="%s"\2<a class="btn btn-gold" href="/%s"><span class="lang-en">Lesson Overview</span><span class="lang-fa">معرفی درس</span></a>'
               % (L["id"], file_of(L)))
        src, k = pat.subn(rep, src, count=1)
        if not k:
            raise SystemExit("courses.html: no lesson row found for %r" % en_t)
        n += k
    write("courses.html", src)
    return n

# --------------------------------------------------------------------------- main
def main():
    os.makedirs("lessons", exist_ok=True)
    shell = make_shell()
    built = []
    seen = set()
    for key in ("beginner", "advanced"):
        ls = COURSES[key]["lessons"]
        for i, L in enumerate(ls):
            assert L["id"] not in seen, L["id"]; seen.add(L["id"])
            assert len(L["quiz"]) == 3, (L["id"], "needs 3 quiz questions")
            assert L["id"] in intros.INTROS, (L["id"], "needs an introduction in _lessons/intros.py")
            built.append(build_page(L, ls[i - 1] if i else None, ls[i + 1] if i + 1 < len(ls) else None, i + 1, len(ls), shell))
    # remove stale lesson pages
    for f in os.listdir("lessons"):
        if f.endswith(".html") and "lessons/" + f not in built:
            os.remove(os.path.join("lessons", f))
            print("removed stale lessons/" + f)
    n = link_courses(beginner.LESSONS + advanced.LESSONS)
    print("Built %d lesson pages; linked %d lesson rows on courses.html." % (len(built), n))

if __name__ == "__main__":
    main()
