#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build brokers.html (the "Brokers" section) from _brokers/brokers.py.

Each broker is an accordion row (name + plus sign); opening it shows its details grouped
into boxes (company & regulation, accounts & costs, platforms, deposits & withdrawals),
pros/cons and a link to the official website. The page shell (head, nav, footer) is copied
from courses.html so it always matches the rest of the site.

Run after editing _brokers/brokers.py (or the nav/footer), BEFORE build-fa.py:

    python build-brokers.py && python build-fa.py && python build-geo.py
"""
import io, os, re, sys, json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_brokers"))
import brokers as B  # noqa: E402

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
WA_CHAT_EN = "https://wa.me/989057230266?text=" + "Hello%20Forex%20School%21%20I%20have%20a%20question%20about%20choosing%20a%20broker."
WA_CHAT_FA = "https://wa.me/989057230266?text=" + "%D8%B3%D9%84%D8%A7%D9%85%20%D9%85%DA%A9%D8%AA%D8%A8%20%D9%81%D8%A7%D8%B1%DA%A9%D8%B3%21%20%D8%AF%D8%B1%D8%A8%D8%A7%D8%B1%D9%87%D9%94%20%D8%A7%D9%86%D8%AA%D8%AE%D8%A7%D8%A8%20%D8%A8%D8%B1%D9%88%DA%A9%D8%B1%20%D8%B3%D8%A4%D8%A7%D9%84%DB%8C%20%D8%AF%D8%A7%D8%B1%D9%85."

def read(p): return io.open(p, encoding="utf-8").read()
def write(p, s): io.open(p, "w", encoding="utf-8").write(s)

def bi(pair):
    if isinstance(pair, str):
        pair = (pair, pair)
    return '<span class="lang-en">%s</span><span class="lang-fa">%s</span>' % pair

ICONS = {
    "shield": '<path d="M12 2 4 5v6c0 5 3.4 9.6 8 11 4.6-1.4 8-6 8-11V5l-8-3zm-1 14-4-4 1.4-1.4L11 13.2l4.6-4.6L17 10l-6 6z"/>',
    "coins": '<path d="M9 4C5.1 4 2 5.3 2 7v10c0 1.7 3.1 3 7 3 1.2 0 2.3-.1 3.3-.4A6 6 0 0 0 22 14c0-2.6-1.7-4.8-4-5.6V7c0-1.7-3.1-3-7-3H9zm0 2c3 0 5 .9 5 1s-2 1-5 1-5-.9-5-1 2-1 5-1zM4 9.6C5.4 10.2 7.1 10.5 9 10.5s3.6-.3 5-.9V8.6c-2 .9-3 2.9-3 5.4v.1c-.6.1-1.3.1-2 .1-3 0-5-.9-5-1V9.6zM16 10a4 4 0 1 1 0 8 4 4 0 0 1 0-8zM4 14.6c1.4.6 3.1.9 5 .9.6 0 1.3 0 1.9-.1.1.7.4 1.4.7 2-.8.1-1.7.2-2.6.2-3 0-5-.9-5-1v-2z"/>',
    "screen": '<path d="M3 4h18a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1h-7v2h3v2H7v-2h3v-2H3a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm1 2v9h16V6H4zm2 7 3-3 2 2 4-4 2 2-6 6-2-2-1 1-2-2z"/>',
    "wallet": '<path d="M4 5h14a2 2 0 0 1 2 2v1h1a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2zm0 2v12h14v-1h-4a3 3 0 0 1-3-3v-2a3 3 0 0 1 3-3h4V7H4zm10 3a1 1 0 0 0-1 1v2a1 1 0 0 0 1 1h6v-4h-6zm1 1.2a.8.8 0 1 1 0 1.6.8.8 0 0 1 0-1.6z"/>',
}
def icon(name):
    return '<svg class="bk-ic" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % ICONS[name]

def broker_item(b, i):
    tier_en, tier_fa = B.TIERS[b["tier"]]
    initials = "".join(w[0] for w in b["name"].split())[:2].upper()
    chips = "".join('<span class="bk-chip">%s</span>' % bi(c) for c in b["chips"])
    boxes = []
    for title, ic, rows in b["clusters"]:
        dl = "".join('<div class="bk-row"><dt>%s</dt><dd>%s</dd></div>' % (bi(k), bi(v)) for k, v in rows)
        boxes.append('<section class="bk-box"><h4>%s%s</h4><dl>%s</dl></section>' % (icon(ic), bi(title), dl))
    pros = "".join("<li>%s</li>" % bi(p) for p in b["pros"])
    cons = "".join("<li>%s</li>" % bi(c) for c in b["cons"])
    return """
        <div class="acc-item bk-item" id="%(id)s">
          <button class="acc-head bk-head" aria-expanded="false" aria-controls="bk-%(id)s">
            <span class="bk-title">
              <span class="bk-logo" style="--bk-bg:%(color)s;--bk-ink:%(ink)s" aria-hidden="true">%(initials)s</span>
              <span class="bk-name-wrap"><span class="bk-name latin">%(name)s</span><span class="bk-tag">%(tagline)s</span></span>
            </span>
            <span class="bk-meta"><span class="bk-tier bk-tier-%(tier)s">%(tierlabel)s</span>%(chips)s</span>
            <span class="acc-icon" aria-hidden="true">+</span>
          </button>
          <div class="acc-panel" id="bk-%(id)s" role="region">
            <div class="acc-panel-inner bk-panel">
              <div class="bk-grid">%(boxes)s</div>
              <div class="cmp bk-cmp">
                <div class="cmp-col cmp-good"><h4>%(pros_t)s</h4><ul>%(pros)s</ul></div>
                <div class="cmp-col cmp-bad"><h4>%(cons_t)s</h4><ul>%(cons)s</ul></div>
              </div>
              <div class="bk-foot">
                <p class="bk-best"><strong>%(best_t)s</strong> %(best)s</p>
                <a class="btn btn-outline bk-site" href="%(url)s" target="_blank" rel="nofollow noopener">%(visit)s <span aria-hidden="true">↗</span></a>
              </div>
            </div>
          </div>
        </div>""" % {
        "id": b["id"], "color": b["color"], "ink": b["ink"], "initials": initials, "name": b["name"],
        "tagline": bi(b["tagline"]), "tier": b["tier"], "tierlabel": bi((tier_en, tier_fa)), "chips": chips,
        "boxes": "".join(boxes), "pros_t": bi(("Strengths", "نقاط قوت")), "cons_t": bi(("Watch out for", "نکات قابل توجه")),
        "pros": pros, "cons": cons, "best_t": bi(("Best for:", "مناسب برای:")), "best": bi(b["best"]),
        "url": b["url"], "visit": bi(("Official website", "وب‌سایت رسمی")),
    }

TIPS = [
    ("shield", ("Check the regulator", "ناظر را بررسی کنید"),
     ("Prefer brokers licensed by top regulators (FCA, ASIC, CySEC…). Offshore licences protect you much less.", "بروکرهای دارای مجوز از ناظران معتبر (FCA، ASIC، CySEC…) را ترجیح دهید. مجوزهای آفشور حمایت بسیار کمتری دارند.")),
    ("wallet", ("Test the withdrawal first", "اول برداشت را آزمایش کنید"),
     ("Deposit a small amount, then withdraw it. A good broker pays out quickly and without excuses.", "مبلغ کمی واریز کنید و سپس برداشت کنید. بروکر خوب سریع و بدون بهانه پرداخت می‌کند.")),
    ("coins", ("Compare the real cost", "هزینهٔ واقعی را مقایسه کنید"),
     ("Look at spread + commission together, and check swap and inactivity fees.", "اسپرد و کمیسیون را با هم ببینید و کارمزد سواپ و عدم فعالیت را بررسی کنید.")),
    ("screen", ("Practise on demo", "روی دمو تمرین کنید"),
     ("Every broker here offers a free demo. Try the platform before you send real money.", "همهٔ این بروکرها حساب دموی رایگان دارند. پیش از واریز پول واقعی، پلتفرم را امتحان کنید.")),
]

def build():
    src = read("courses.html")
    head_end = src.index('<div class="nav-backdrop"></div>\n') + len('<div class="nav-backdrop"></div>\n')
    foot_start = src.index('  <!-- Disclaimer band -->')
    top, bottom = src[:head_end], src[foot_start:]

    # head: titles, descriptions, URLs; drop course JSON-LD and hreflang (build-fa re-adds hreflang)
    top = top.replace('data-title-en="Courses | Forex School"', 'data-title-en="Forex Brokers | Forex School"')
    top = top.replace('data-title-fa="درس‌ها | مکتب فارکس"', 'data-title-fa="بروکرهای فارکس | مکتب فارکس"')
    top = re.sub(r"<title>.*?</title>", "<title>Forex Brokers | Forex School</title>", top, count=1)
    desc = "A guide for Afghan traders to well-known forex brokers: regulation, minimum deposit, costs, platforms and withdrawals — compared in Dari and English."
    top = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + desc, top, count=1)
    top = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + "Forex Brokers | Forex School", top, count=1)
    top = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + "Compare well-known forex brokers — guidance for Afghan traders", top, count=1)
    top = top.replace("https://forexschool.store/courses.html", "https://forexschool.store/brokers.html")
    top = re.sub(r'  <link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', "", top)
    top = re.sub(r'  <script type="application/ld\+json">.*?</script>\n', "", top, flags=re.S)
    # nav: Brokers is the active page
    top = top.replace('<a href="/courses.html" class="active">', '<a href="/courses.html">')
    top = top.replace('<a href="/brokers.html">', '<a href="/brokers.html" class="active">')
    # page scripts: no lesson progress script on this page
    bottom = re.sub(r'  <script src="/assets/js/lessons\.js[^"]*" defer></script>\n', "", bottom)
    bottom = bottom.replace("Join the WhatsApp channel to get the lessons", "Join the Forex School WhatsApp channel")
    bottom = bottom.replace("برای دریافت درس‌ها به کانال واتساپ بپیوند", "به کانال واتساپ مکتب فارکس بپیوندید")

    tips = "".join('<div class="bk-tip">%s<h3>%s</h3><p>%s</p></div>' % (icon(ic), bi(t), bi(d)) for ic, t, d in TIPS)
    items = "".join(broker_item(b, i) for i, b in enumerate(B.BROKERS))
    n = len(B.BROKERS)

    body = """
  <section class="page-head">
    <div class="container">
      <h1>%(h1)s</h1>
      <p>%(intro)s</p>
    </div>
  </section>

  <section class="section section-tight">
    <div class="container">
      <div class="bk-tips">%(tips)s</div>
    </div>
  </section>

  <section class="section band" id="brokers">
    <div class="container bk-wrap">
      <div class="bk-listhead">
        <h2 class="section-title">%(list_h)s</h2>
        <button type="button" class="btn btn-outline bk-toggle-all" aria-pressed="false">%(expand)s</button>
      </div>
      <p class="bk-hint">%(hint)s</p>
      <div class="accordion bk-list">%(items)s
      </div>
      <div class="alert alert-warn bk-note"><span class="a-icon" aria-hidden="true">⚠️</span><p>%(note)s</p></div>
      <div class="bk-ask">
        <p>%(ask)s</p>
        <a class="btn btn-gold lang-en" href="%(wa_en)s" target="_blank" rel="noopener">Ask us on WhatsApp</a>
        <a class="btn btn-gold lang-fa" href="%(wa_fa)s" target="_blank" rel="noopener">در واتساپ از ما بپرسید</a>
      </div>
    </div>
  </section>

""" % {
        "h1": bi(('Forex <span class="accent">Brokers</span>', 'بروکرهای <span class="accent">فارکس</span>')),
        "intro": bi(("The broker you choose holds your money, so choosing well matters as much as learning to trade. This section is here to help and guide Afghan traders choose a reliable broker: below you can compare well-known brokers side by side — how they are regulated, what it costs to trade, which platforms they offer and how deposits and withdrawals work.",
                     "بروکری که انتخاب می‌کنید نگهدارندهٔ پول شماست؛ پس انتخاب درست به اندازهٔ یادگیری معامله‌گری اهمیت دارد. هدف این بخش، کمک و راهنمایی معامله‌گران افغان برای انتخاب یک بروکر معتبر است: در پایین می‌توانید بروکرهای شناخته‌شده را کنار هم مقایسه کنید — نحوهٔ نظارت بر آن‌ها، هزینهٔ معامله، پلتفرم‌هایی که ارائه می‌دهند و نحوهٔ واریز و برداشت.")),
        "tips": tips,
        "list_h": bi(("Compare %d brokers" % n, "مقایسهٔ %s بروکر" % str(n).translate(FA_DIGITS))),
        "expand": bi(("Expand all", "باز کردن همه")),
        "hint": bi(("Tap a broker's name (or the + sign) to see its full details.", "روی نام هر بروکر (یا علامت +) بزنید تا جزئیات کامل آن را ببینید.")),
        "items": items,
        "note": bi(("<strong>Please read:</strong> this information is for education only and is not a recommendation or financial advice; Forex School is not paid by these brokers. Details were checked in %s, but brokers change their conditions often, and leverage, protection and payment methods depend on which of the broker's companies you are opened under — that depends on your country. Not every broker accepts clients from every country: always confirm on the official website before you deposit. Forex trading carries a high risk of losing money." % B.CHECKED[0],
                     "<strong>لطفاً بخوانید:</strong> این اطلاعات فقط جنبهٔ آموزشی دارد و توصیه یا مشاورهٔ مالی نیست؛ مکتب فارکس از این بروکرها پولی دریافت نمی‌کند. جزئیات در %s بررسی شده‌اند، اما بروکرها شرایط خود را زیاد تغییر می‌دهند و لیوریج، میزان حمایت و روش‌های پرداخت بستگی دارد که زیر کدام شرکتِ بروکر ثبت شوید — که آن هم به کشور شما بستگی دارد. همهٔ بروکرها مشتریان همهٔ کشورها را نمی‌پذیرند: پیش از واریز، همیشه در وب‌سایت رسمی بررسی کنید. معامله در فارکس با ریسک بالای از دست دادن پول همراه است." % B.CHECKED[1])),
        "ask": bi(("Not sure which broker suits you? Ask us — we are happy to help.", "مطمئن نیستید کدام بروکر برای شما مناسب است؟ از ما بپرسید — با کمال میل کمک می‌کنیم.")),
        "wa_en": WA_CHAT_EN, "wa_fa": WA_CHAT_FA,
    }

    script = """  <script>
    /* Brokers: "Expand all / Collapse all" for the accordion (single rows use site.js). */
    (function () {
      var btn = document.querySelector('.bk-toggle-all');
      if (!btn) return;
      var en = btn.querySelector('.lang-en'), fa = btn.querySelector('.lang-fa');
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-pressed') !== 'true';
        document.querySelectorAll('.bk-list .acc-head').forEach(function (h) {
          h.setAttribute('aria-expanded', open ? 'true' : 'false');
          var p = h.nextElementSibling;
          if (p) p.style.maxHeight = open ? p.scrollHeight + 'px' : null;
        });
        btn.setAttribute('aria-pressed', open ? 'true' : 'false');
        en.textContent = open ? 'Collapse all' : 'Expand all';
        fa.textContent = open ? 'بستن همه' : 'باز کردن همه';
      });
      /* keep open panels the right height when the screen size changes */
      window.addEventListener('resize', function () {
        document.querySelectorAll('.bk-list .acc-head[aria-expanded="true"]').forEach(function (h) {
          var p = h.nextElementSibling; if (p) p.style.maxHeight = p.scrollHeight + 'px';
        });
      });
      /* open a broker linked directly, e.g. /brokers.html#exness */
      var target = null;
      try { target = location.hash && document.querySelector('.bk-list ' + location.hash + ' .acc-head'); } catch (e) {}
      if (target) setTimeout(function () { target.click(); target.scrollIntoView({ block: 'start' }); }, 300);
    })();
  </script>
</body>"""
    bottom = bottom.replace("</body>", script, 1)
    write("brokers.html", top + body + bottom)
    print("Built brokers.html with %d brokers." % n)

if __name__ == "__main__":
    build()
