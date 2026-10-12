# -*- coding: utf-8 -*-
"""Inline SVG diagrams for the lesson pages — one (or more) per lesson.

Every label is bilingual: T() writes an English and a Dari <text>; CSS shows the one for the
page language. Colours come from CSS classes (.dg …) so the diagrams follow the site theme.
Charts are always drawn left-to-right (dir="ltr"), also on Dari pages, like real trading charts.
"""
import re

FA = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

def fa(s):
    """Persian digits, with Persian decimal (٫), thousands (٬) and percent (٪) signs."""
    s = str(s).translate(FA)
    s = re.sub(r"(?<=[۰-۹])\.(?=[۰-۹])", "٫", s)
    s = re.sub(r"(?<=[۰-۹]),(?=[۰-۹])", "٬", s)
    return s.replace("%", "٪")

def T(x, y, en, fa_=None, cls="", anchor="middle", size=None, weight=None):
    """Bilingual label. fa_=None -> same text (digits converted) for Dari."""
    if fa_ is None:
        fa_ = fa(en)
    st = []
    if size: st.append("font-size:%spx" % size)
    if weight: st.append("font-weight:%s" % weight)
    style = ' style="%s"' % ";".join(st) if st else ""
    # Dari labels are laid out right-to-left, where "start" means the right edge — so swap the
    # anchor to keep both languages in the same place on the chart.
    a_en = ' direction="ltr" text-anchor="%s"' % anchor
    a_fa = ' direction="rtl" text-anchor="%s"' % {"start": "end", "end": "start"}.get(anchor, anchor)
    c = (" " + cls) if cls else ""
    return ('<text x="%s" y="%s"%s class="lang-en%s"%s>%s</text><text x="%s" y="%s"%s class="lang-fa%s"%s>%s</text>'
            % (x, y, a_en, c, style, en, x, y, a_fa, c, style, fa_))

def L(x1, y1, x2, y2, cls="ln", extra=""):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" class="%s"%s/>' % (x1, y1, x2, y2, cls, extra)

def R(x, y, w, h, cls="", rx=6, extra=""):
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" class="%s"%s/>' % (x, y, w, h, rx, cls, extra)

def P(d, cls="", extra=""):
    return '<path d="%s" class="%s"%s/>' % (d, cls, extra)

def C(x, y, r, cls=""):
    return '<circle cx="%s" cy="%s" r="%s" class="%s"/>' % (x, y, r, cls)

def poly(pts, cls="pl"):
    return '<polyline points="%s" class="%s"/>' % (" ".join("%s,%s" % p for p in pts), cls)

def candle(x, o, h, l, c, w=14, cls=None):
    """Screen coords: smaller y = higher price. Bull if close is above open."""
    bull = c < o
    k = cls or ("bull" if bull else "bear")
    top, bot = min(o, c), max(o, c)
    return ('<g class="cdl %s">' % k + L(x, h, x, l, "wick") +
            R(x - w / 2, top, w, max(bot - top, 2), "body", 2) + "</g>")

def arrow(x1, y1, x2, y2, cls="arw"):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" class="%s" marker-end="url(#ah)"/>' % (x1, y1, x2, y2, cls)

DEFS = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>')

def svg(w, h, body, label=""):
    return ('<svg class="dg" viewBox="0 0 %d %d" role="img" aria-label="%s" dir="ltr" preserveAspectRatio="xMidYMid meet">%s%s</svg>'
            % (w, h, label, DEFS, body))

# =========================================================================== beginner

def pyramid():
    b = []
    rows = [(270, 40, 100, ("Founder", "بنیان‌گذار"), "brand"),
            (215, 100, 210, ("First members", "نفرات اول"), "warn"),
            (150, 160, 340, ("New investors — the biggest losses", "سرمایه‌گذاران جدید — بیشترین ضرر"), "bad")]
    for x, y, w, lab, k in rows:
        b.append(R(x, y, w, 46, "box-" + k, 8))
        b.append(T(x + w / 2, y + 28, lab[0], lab[1], "t-strong"))
    b.append(arrow(560, 196, 560, 70, "arw arw-brand"))
    b.append(T(575, 130, "money", "پول", "t-brand", "start"))
    b.append(T(575, 148, "flows up", "به بالا", "t-brand", "start"))
    b.append(T(320, 238, "Profits are paid from new members' money — not from real business.",
               "سود نفرات بالا از جیب اعضای جدید پرداخت می‌شود — نه از یک تجارت واقعی.", "t-muted", size=13))
    return svg(640, 252, "".join(b), "Pyramid scheme")

def sessions():
    # Kabul time, 0..24h -> x 120..610
    x0, x1 = 120, 610
    def X(h): return x0 + (x1 - x0) * h / 24.0
    b = []
    for h in range(0, 25, 3):
        b.append(L(X(h), 30, X(h), 190, "grid"))
        b.append(T(X(h), 210, "%02d:00" % (h % 24), None, "t-dim", size=11))
    rows = [(("Asia / Sydney", "آسیا و آسترالیا"), [(2.5, 13.5)], "ses-asia"),
            (("London", "لندن"), [(12.5, 21.5)], "ses-london"),
            (("New York", "نیویورک"), [(17.5, 24), (0, 2.5)], "ses-ny")]
    for i, (lab, segs, k) in enumerate(rows):
        y = 44 + i * 44
        b.append(T(108, y + 18, lab[0], lab[1], "t-strong", "end", size=13))
        for a, z in segs:
            b.append(R(X(a), y, X(z) - X(a), 26, k, 6))
    b.append(R(X(17.5), 34, X(21.5) - X(17.5), 150, "overlap", 4))
    b.append(T(X(19.5), 26, "Busiest: 17:30–21:30", "شلوغ‌ترین: ۱۷:۳۰ تا ۲۱:۳۰", "t-brand", size=12, weight=700))
    return svg(640, 222, "".join(b), "Forex sessions in Kabul time")

def spread():
    b = []
    b.append(L(140, 30, 140, 210, "axis"))
    b.append(R(170, 52, 300, 44, "box-bear", 8))
    b.append(T(320, 79, "Ask (buy price)  1.0852", "قیمت خرید (Ask)  ۱٫۰۸۵۲", "t-strong"))
    b.append(R(170, 144, 300, 44, "box-bull", 8))
    b.append(T(320, 171, "Bid (sell price)  1.0850", "قیمت فروش (Bid)  ۱٫۰۸۵۰", "t-strong"))
    b.append(arrow(510, 100, 510, 140, "arw arw-brand"))
    b.append(arrow(510, 140, 510, 100, "arw arw-brand"))
    b.append(T(530, 116, "Spread", "سپرید", "t-brand", "start", weight=700))
    b.append(T(530, 134, "= 2 pips", "= ۲ پیپ", "t-brand", "start"))
    b.append(T(120, 79, "you buy", "خرید شما", "t-muted", "end", size=12))
    b.append(T(120, 171, "you sell", "فروش شما", "t-muted", "end", size=12))
    return svg(640, 230, "".join(b), "Bid, ask and spread")

def bars(items, maxv, title_en, title_fa, unit="%", h=230, fmt=None):
    """Horizontal bar chart. items: (label_en, label_fa, value, cls)."""
    b = [T(20, 24, title_en, title_fa, "t-muted", "start", size=13)]
    n = len(items)
    row = (h - 50) / n
    for i, (le, lf, v, k) in enumerate(items):
        y = 40 + i * row
        b.append(T(196, y + row / 2 + 4, le, lf, "t-strong", "end", size=13))
        w = max(4, 380 * v / maxv)
        b.append(R(210, y + row * 0.18, w, row * 0.64, "bar-" + k, 5))
        val = fmt(v) if fmt else ("%s%s" % (v, unit))
        b.append(T(218 + w, y + row / 2 + 4, val, None, "t-strong", "start", size=13, weight=700))
    return svg(640, h, "".join(b))

def leverage_bars():
    return bars([("1 standard lot", "۱ لات ستندرد", 50, "bad"), ("1 mini lot", "۱ مینی لات", 5, "warn"), ("1 micro lot", "۱ مایکرو لات", 0.5, "good")],
                50, "A 50-pip move against a $1,000 account — % of the account lost",
                "حرکت ۵۰ پیپی مخالف روی حساب ۱٬۰۰۰ دلاری — درصد حسابی که از دست می‌رود")

def ten_losses():
    # equity after k losses at 2% vs 10%
    b = []
    x0, x1, y0, y1 = 80, 600, 30, 200
    def X(k): return x0 + (x1 - x0) * k / 10.0
    def Y(v): return y1 - (y1 - y0) * v / 100.0
    for v in (0, 25, 50, 75, 100):
        b.append(L(x0, Y(v), x1, Y(v), "grid"))
        b.append(T(x0 - 10, Y(v) + 4, "$%d" % (v * 10), None, "t-dim", "end", size=11))
    for k in range(0, 11, 2):
        b.append(T(X(k), y1 + 18, str(k), None, "t-dim", size=11))
    a = [(X(k), Y(100 * 0.98 ** k)) for k in range(11)]
    c = [(X(k), Y(100 * 0.90 ** k)) for k in range(11)]
    b.append(poly(a, "pl pl-bull"))
    b.append(poly(c, "pl pl-bear"))
    b.append(T(X(10) - 4, Y(82) - 10, "2% risk: $817 left", "ریسک ۲٪: ۸۱۷ دلار می‌ماند", "t-bull", "end", size=12, weight=700))
    b.append(T(X(10) - 4, Y(35) + 22, "10% risk: $349 left", "ریسک ۱۰٪: ۳۴۹ دلار می‌ماند", "t-bear", "end", size=12, weight=700))
    b.append(T(340, 236, "Losing trades in a row (account starts at $1,000)", "تعداد ضررهای پشت سر هم (حساب ۱٬۰۰۰ دلاری)", "t-muted", size=12))
    return svg(640, 248, "".join(b), "Ten losses in a row")

def candle_anatomy():
    b = []
    # bullish
    b.append(L(170, 30, 170, 210, "wick-bull"))
    b.append(R(140, 70, 60, 100, "body-bull", 4))
    # bearish
    b.append(L(450, 30, 450, 210, "wick-bear"))
    b.append(R(420, 70, 60, 100, "body-bear", 4))
    for x, top, bot in ((170, ("Close", "بسته"), ("Open", "باز")), (450, ("Open", "باز"), ("Close", "بسته"))):
        b.append(L(x + 34, 70, x + 70, 70, "ln-dim")); b.append(T(x + 76, 74, top[0], top[1], "t-strong", "start", size=12))
        b.append(L(x + 34, 170, x + 70, 170, "ln-dim")); b.append(T(x + 76, 174, bot[0], bot[1], "t-strong", "start", size=12))
        b.append(L(x + 4, 30, x + 70, 30, "ln-dim")); b.append(T(x + 76, 34, "High", "بالاترین", "t-muted", "start", size=12))
        b.append(L(x + 4, 210, x + 70, 210, "ln-dim")); b.append(T(x + 76, 214, "Low", "پایین‌ترین", "t-muted", "start", size=12))
    b.append(T(100, 124, "body", "بدنه", "t-muted", "end", size=12))
    b.append(T(100, 54, "wick", "سایه", "t-muted", "end", size=12))
    b.append(T(170, 238, "Bullish (price rose)", "صعودی (قیمت بالا رفت)", "t-bull", weight=700))
    b.append(T(450, 238, "Bearish (price fell)", "نزولی (قیمت پایین آمد)", "t-bear", weight=700))
    return svg(640, 252, "".join(b), "Candlestick anatomy")

def uptrend():
    pts = [(40, 190), (120, 120), (170, 160), (260, 80), (310, 125), (410, 45), (460, 92), (560, 20)]
    b = [poly(pts, "pl pl-price")]
    b.append(L(40, 190.5, 600, 59.2, "trendline"))
    b.append(L(40, 131.6, 600, 0.3, "trendline dashed"))
    labs = [(120, 120, "HH", "سقف بالاتر", -12), (170, 160, "HL", "کف بالاتر", 22), (260, 80, "HH", "سقف بالاتر", -12),
            (310, 125, "HL", "کف بالاتر", 22), (410, 45, "HH", "سقف بالاتر", -12), (460, 92, "HL", "کف بالاتر", 22)]
    for x, y, en, f, dy in labs:
        b.append(C(x, y, 4, "dot"))
        b.append(T(x, y + dy, en, f, "t-bull" if "H" == en[0] else "t-bull", size=12, weight=700))
    b.append(T(560, 196, "trendline (connect the lows)", "خط روند (اتصال کف‌ها)", "t-brand", "end", size=12))
    b.append(T(120, 24, "channel top", "سقف کانال", "t-dim", "start", size=12))
    return svg(640, 232, "".join(b), "Uptrend, trendline and channel")

def patterns():
    b = []
    def lab(x, en, f, k): b.append(T(x, 204, en, f, k, size=12, weight=700))
    # doji
    b.append(candle(60, 110, 60, 160, 111, 18, "neutral")); lab(60, "Doji", "دوجی", "t-strong")
    # hammer
    b.append(candle(170, 80, 72, 170, 70, 18)); lab(170, "Hammer", "چکش", "t-bull")
    # shooting star
    b.append(candle(280, 150, 60, 158, 160, 18)); lab(280, "Shooting star", "ستاره دنباله‌دار", "t-bear")
    # bullish engulfing
    b.append(candle(375, 100, 92, 150, 140, 16)); b.append(candle(400, 150, 70, 156, 84, 20)); lab(388, "Bullish engulfing", "پوششی صعودی", "t-bull")
    # morning star
    b.append(candle(495, 60, 54, 140, 130, 16)); b.append(candle(520, 150, 140, 168, 152, 12, "neutral")); b.append(candle(545, 140, 66, 146, 76, 16))
    lab(520, "Morning star", "ستاره صبحگاهی", "t-bull")
    b.append(T(320, 238, "Location matters most: a pattern on support or resistance is far more reliable.",
               "محل ظاهر شدن الگو مهم‌تر است: الگو روی حمایت یا مقاومت بسیار معتبرتر است.", "t-muted", size=12))
    return svg(640, 252, "".join(b), "Candlestick patterns")

def indicators():
    b = []
    price = [(40, 120), (80, 110), (120, 128), (160, 98), (200, 86), (240, 96), (280, 70), (320, 60), (360, 74), (400, 52), (440, 40), (480, 58), (520, 48), (560, 30), (600, 36)]
    ma = [(40, 128), (120, 118), (200, 104), (280, 88), (360, 74), (440, 60), (520, 52), (600, 44)]
    b.append(poly(price, "pl pl-price")); b.append(poly(ma, "pl pl-ma"))
    b.append(T(600, 70, "MA 50", None, "t-brand", "end", size=12, weight=700))
    b.append(T(40, 22, "Price above a rising MA = uptrend", "قیمت بالای میانگین صعودی = روند صعودی", "t-muted", "start", size=12))
    # RSI panel
    b.append(R(40, 150, 560, 80, "panel", 6))
    for v, k in ((70, "bear"), (30, "bull")):
        y = 150 + 80 * (100 - v) / 100.0
        b.append(L(40, y, 600, y, "lvl-" + k)); b.append(T(608, y + 4, str(v), None, "t-" + k, "start", size=11))
    rsi = [(40, 196), (100, 188), (160, 176), (220, 172), (280, 160), (320, 168), (380, 158), (440, 170), (500, 184), (560, 198), (600, 206)]
    b.append(poly(rsi, "pl pl-rsi"))
    b.append(T(50, 223, "RSI: above 70 overbought · below 30 oversold", "RSI: بالای ۷۰ خرید بیش از حد · زیر ۳۰ فروش بیش از حد", "t-dim", "start", size=11))
    return svg(640, 244, "".join(b), "Moving average and RSI")

def flow(nodes, w=640, h=150, title=None, cls="box-brand"):
    """Left-to-right flow of boxes with arrows. nodes: (en, fa)."""
    b = []
    n = len(nodes)
    gap = 26
    bw = (w - 40 - gap * (n - 1)) / n
    y = 50 if title else 36
    if title:
        b.append(T(w / 2, 26, title[0], title[1], "t-muted", size=13))
    for i, (en, f) in enumerate(nodes):
        x = 20 + i * (bw + gap)
        b.append(R(x, y, bw, 62, cls if i < n - 1 else "box-bull", 10))
        parts_en, parts_fa = en.split("|"), f.split("|")
        for j in range(max(len(parts_en), len(parts_fa))):
            pe = parts_en[j] if j < len(parts_en) else ""
            pf = parts_fa[j] if j < len(parts_fa) else ""
            yy = y + 31 - 9 * (max(len(parts_en), len(parts_fa)) - 1) + 18 * j + 4
            b.append(T(x + bw / 2, yy, pe, pf, "t-strong", size=12.5))
        if i < n - 1:
            b.append(arrow(x + bw + 3, y + 31, x + bw + gap - 3, y + 31, "arw arw-brand"))
    return svg(w, h, "".join(b))

def rate_flow():
    return flow([("Central bank|raises rates", "بانک مرکزی|نرخ بهره را بالا می‌برد"),
                 ("Higher return|on that currency", "بازده بیشتر|برای آن ارز"),
                 ("Investors buy|the currency", "سرمایه‌گذاران|ارز را می‌خرند"),
                 ("Currency|gets stronger", "ارز|قوی‌تر می‌شود")], title=("Why interest rates move currencies", "چرا نرخ بهره ارزها را حرکت می‌دهد"))

def cycle(nodes, title=None, bad=False):
    """Four nodes around a loop (clockwise)."""
    b = []
    pos = [(320, 52), (540, 135), (320, 218), (100, 135)]
    if title:
        b.append(T(320, 270, title[0], title[1], "t-muted", size=12.5))
    for i, ((x, y), (en, f)) in enumerate(zip(pos, nodes)):
        b.append(R(x - 95, y - 26, 190, 52, "box-bad" if bad else "box-brand", 10))
        pe, pf = en.split("|"), f.split("|")
        for j in range(max(len(pe), len(pf))):
            yy = y + 5 - 9 * (max(len(pe), len(pf)) - 1) + 18 * j
            b.append(T(x, yy, pe[j] if j < len(pe) else "", pf[j] if j < len(pf) else "", "t-strong", size=12.5))
    arr = [((420, 62), (500, 105)), ((500, 165), (420, 208)), ((220, 208), (140, 165)), ((140, 105), (220, 62))]
    for (a, c) in arr:
        b.append(arrow(a[0], a[1], c[0], c[1], "arw " + ("arw-bear" if bad else "arw-brand")))
    return svg(640, 284 if title else 260, "".join(b))

def revenge():
    return cycle([("A loss", "یک ضرر"), ("Anger: “win it|back now!”", "خشم: «همین حالا|جبران کنم!»"),
                  ("Bigger size,|no stop-loss", "حجم بزرگ‌تر،|بدون استاپ لاس"), ("A bigger loss", "ضرر بزرگ‌تر")],
                 ("The revenge-trading spiral — break it: stop for the day after two losses in a row.",
                  "چرخهٔ معاملهٔ انتقامی — آن را بشکنید: پس از دو ضرر پیاپی، برای همان روز متوقف شوید."), bad=True)

def plan_loop():
    return cycle([("1. Write the plan", "۱. پلان بنویسید"), ("2. Trade only|by the plan", "۲. فقط طبق|پلان معامله کنید"),
                  ("3. Record it|in the journal", "۳. در ژورنال|ثبت کنید"), ("4. Review weekly|(change after 50 trades)", "۴. هفتگی مرور کنید|(تغییر پس از ۵۰ معامله)")],
                 ("Plan → trade → journal → review: the loop that turns mistakes into lessons.",
                  "پلان ← معامله ← ژورنال ← مرور: چرخه‌ای که اشتباه را به درس تبدیل می‌کند."))

def stairs(steps, title):
    b = [T(320, 22, title[0], title[1], "t-muted", size=12.5)]
    n = len(steps)
    w = 560 / n
    for i, (en, f, sub_en, sub_fa) in enumerate(steps):
        x = 40 + i * w
        hgt = 60 + i * 45
        y = 230 - hgt
        b.append(R(x + 4, y, w - 8, hgt, "box-brand" if i < n - 1 else "box-bull", 8))
        b.append(T(x + w / 2, y + 24, en, f, "t-strong", size=13, weight=700))
        b.append(T(x + w / 2, y + 44, sub_en, sub_fa, "t-muted", size=11.5))
    return svg(640, 244, "".join(b))

def demo_live():
    return stairs([("Demo", "دمو", "3+ months, real size", "حداقل ۳ ماه، حجم واقعی"),
                   ("Micro live", "مایکرو واقعی", "same plan, tiny size", "همان پلان، حجم کوچک"),
                   ("Standard", "استاندارد", "after steady profits", "پس از سود پایدار")],
                  ("From demo to live — one careful step at a time", "از دمو تا حساب واقعی — قدم‌به‌قدم و با احتیاط"))

# =========================================================================== advanced F

def regime_matrix():
    b = []
    b.append(T(250, 28, "Floating", "شناور", "t-strong", weight=700))
    b.append(T(500, 28, "Pegged / fixed", "ثابت / پگ", "t-strong", weight=700))
    b.append(T(70, 100, "No commodity", "بدون کامودیتی", "t-strong", weight=700, size=12.5))
    b.append(T(70, 118, "dependence", "وابستگی کالایی", "t-dim", size=11))
    b.append(T(70, 205, "Commodity", "کامودیتی‌محور", "t-strong", weight=700, size=12.5))
    b.append(T(70, 223, "driven", "", "t-dim", size=11))
    cells = [(140, 44, "box-bull", ("USD · EUR · JPY · GBP", "USD · EUR · JPY · GBP"), ("CHF · SEK · CZK · PLN", "CHF · SEK · CZK · PLN"), ("most opportunity", "بیشترین فرصت")),
             (390, 44, "box-dim", ("HKD · SGD · DKK", "HKD · SGD · DKK"), ("", ""), ("little movement", "نوسان کم")),
             (140, 150, "box-bull", ("AUD · NZD · CAD · NOK", "AUD · NZD · CAD · NOK"), ("ZAR · BRL · MXN · RUB", "ZAR · BRL · MXN · RUB"), ("commodity prices add moves", "قیمت کالاها نوسان می‌افزاید")),
             (390, 150, "box-dim", ("SAR · AED · QAR · KWD", "SAR · AED · QAR · KWD"), ("CNH", "CNH"), ("mostly GCC oil exporters", "بیشتر صادرکنندگان نفت خلیج"))]
    for x, y, k, a, c, note in cells:
        b.append(R(x, y, 220, 96, k, 10))
        b.append(T(x + 110, y + 30, a[0], a[1], "t-strong", size=12.5))
        b.append(T(x + 110, y + 50, c[0], c[1], "t-strong", size=12.5))
        b.append(T(x + 110, y + 78, note[0], note[1], "t-muted", size=11.5))
    return svg(640, 260, "".join(b), "Four currency groups")

def bretton_timeline():
    b = [L(40, 110, 600, 110, "axis")]
    ev = [(80, "1944", ("Bretton Woods:", "برتون وودز:"), ("USD pegged to gold", "دلار به طلا پگ شد")),
          (230, "1950–69", ("US share of world", "سهم امریکا از تولید"), ("output 35% → 27%", "جهانی ۳۵٪ ← ۲۷٪")),
          (380, "1971", ("Nixon shock: gold", "شوک نیکسون: تعلیق"), ("convertibility ends", "تبدیل دلار به طلا")),
          (540, "1973", ("Major currencies", "ارزهای بزرگ"), ("float freely", "آزادانه شناور شدند"))]
    for i, (x, yr, a, c) in enumerate(ev):
        b.append(C(x, 110, 7, "dot-brand"))
        up = i % 2 == 0
        b.append(T(x, 92 if up else 140, yr, None, "t-brand", size=14, weight=700))
        b.append(T(x, 52 if up else 166, a[0], a[1], "t-strong", size=12))
        b.append(T(x, 70 if up else 184, c[0], c[1], "t-muted", size=12))
    return svg(640, 200, "".join(b), "From Bretton Woods to floating currencies")

def peg_band():
    b = []
    def Y(v): return 40 + (7.87 - v) / (7.87 - 7.73) * 160
    for v, k, en, f in ((7.85, "lvl-bear", "Upper band 7.85", "باند بالا ۷٫۸۵"),
                        (7.80, "lvl-mid", "Peg 7.80", "نرخ مرکزی ۷٫۸۰"),
                        (7.75, "lvl-bull", "Lower band 7.75", "باند پایین ۷٫۷۵")):
        b.append(L(40, Y(v), 440, Y(v), k))
        b.append(T(450, Y(v) + 4, en, f, "t-muted", "start", size=11))
    import math
    pts = []
    for i in range(0, 41):
        x = 40 + i * 10
        v = 7.80 + 0.042 * math.sin(i / 4.0) + 0.006 * math.sin(i * 1.7)
        pts.append((x, round(Y(v), 1)))
    b.append(poly(pts, "pl pl-price"))
    b.append(T(40, 226, "USD/HKD stays inside its band — little room to trade unless the peg itself breaks.",
               "USD/HKD درون باند می‌ماند — فرصت معامله کم است، مگر اینکه خود پگ بشکند.", "t-muted", "start", size=12))
    return svg(640, 240, "".join(b), "Currency peg band")

# =========================================================================== advanced A

def mtf_funnel():
    b = []
    rows = [(60, 520, ("HTF — Weekly / Daily", "HTF — هفتگی / روزانه"), ("Bias: buy or sell today?", "بایاس: امروز خرید یا فروش؟")),
            (130, 380, ("MTF — 4H / 1H", "MTF — ۴ ساعته / ۱ ساعته"), ("Structure and the zone to watch", "ساختار و منطقهٔ مورد توجه")),
            (200, 240, ("LTF — 15m / 5m", "LTF — ۱۵ / ۵ دقیقه"), ("Exact entry and stop", "ورود دقیق و حد ضرر"))]
    for i, (y, w, a, c) in enumerate(rows):
        x = 320 - w / 2
        b.append(R(x, y - 40, w, 58, ["box-brand", "box-warn", "box-bull"][i], 10))
        b.append(T(320, y - 15, a[0], a[1], "t-strong", size=13, weight=700))
        b.append(T(320, y + 4, c[0], c[1], "t-muted", size=12))
    b.append(T(320, 240, "Top-down: never trade against the higher timeframe.", "از بالا به پایین: هرگز خلاف تایم‌فریم بالاتر معامله نکنید.", "t-brand", size=12.5, weight=700))
    return svg(640, 254, "".join(b), "Multi-timeframe funnel")

def structure():
    pts = [(30, 190), (90, 120), (130, 150), (200, 80), (240, 112), (310, 50), (360, 96), (400, 70), (440, 140), (500, 110), (560, 180), (610, 165)]
    b = [poly(pts, "pl pl-price")]
    # BOS lines
    b.append(L(90, 120, 190, 120, "lvl-bull dashed")); b.append(T(160, 114, "BOS", None, "t-bull", size=12, weight=700))
    b.append(L(200, 80, 300, 80, "lvl-bull dashed")); b.append(T(270, 74, "BOS", None, "t-bull", size=12, weight=700))
    # CHoCH: break of last HL (360,96)
    b.append(L(360, 96, 430, 96, "lvl-bear dashed")); b.append(T(436, 100, "CHoCH", None, "t-bear", "start", size=13, weight=700))
    for x, y, t, d, k in ((90, 120, "HH", -10, "t-bull"), (130, 150, "HL", 20, "t-bull"), (200, 80, "HH", -10, "t-bull"), (240, 112, "HL", 20, "t-bull"),
                          (310, 50, "HH", -10, "t-bull"), (360, 96, "HL", 20, "t-bull"), (400, 70, "LH", -10, "t-bear"), (440, 140, "LL", 20, "t-bear"),
                          (500, 110, "LH", -10, "t-bear"), (560, 180, "LL", 20, "t-bear")):
        b.append(C(x, y, 3.5, "dot")); b.append(T(x, y + d, t, None, k, size=11, weight=700))
    b.append(T(170, 222, "BOS = trend continues", "BOS = ادامهٔ روند", "t-bull", size=12.5, weight=700))
    b.append(T(470, 222, "CHoCH = first warning of reversal", "CHoCH = اولین هشدار برگشت", "t-bear", size=12.5, weight=700))
    return svg(640, 236, "".join(b), "Break of structure and change of character")

def demand_zone():
    b = [R(60, 150, 560, 36, "zone-bull", 4)]
    b.append(T(70, 202, "Demand zone (drawn as an area, not a line)", "منطقهٔ تقاضا (به‌صورت ناحیه، نه خط)", "t-bull", "start", size=12, weight=700))
    cs = [(80, 120, 112, 160, 150), (100, 150, 140, 176, 160), (120, 162, 150, 180, 156), (140, 156, 150, 178, 170),
          (162, 168, 110, 172, 116), (184, 116, 70, 120, 76), (206, 76, 36, 82, 42),
          (260, 50, 44, 90, 84), (290, 84, 78, 120, 112), (320, 112, 100, 150, 140), (350, 140, 132, 168, 152),
          (380, 152, 120, 160, 126), (410, 126, 80, 130, 86), (440, 86, 40, 90, 46)]
    for x, o, h, l, c in cs:
        b.append(candle(x, o, h, l, c, 14))
    b.append(T(195, 26, "impulsive move", "حرکت انفجاری", "t-brand", size=12, weight=700))
    b.append(T(470, 173, "first return (fresh)", "اولین بازگشت (تازه)", "t-muted", "start", size=11.5))
    b.append(arrow(470, 60, 560, 30, "arw arw-bull"))
    return svg(640, 220, "".join(b), "Supply and demand zone")

# =========================================================================== advanced AS

def order_block():
    b = [R(150, 128, 460, 46, "zone-bull", 4)]
    cs = [(60, 60, 54, 96, 90), (90, 90, 84, 124, 118), (120, 118, 112, 150, 144), (150, 132, 128, 174, 168),
          (180, 166, 110, 170, 114), (210, 114, 64, 118, 70), (240, 70, 30, 74, 36),
          (300, 50, 44, 90, 84), (330, 84, 78, 120, 112), (360, 112, 104, 140, 134), (390, 134, 116, 138, 120), (420, 120, 76, 124, 82), (450, 82, 40, 86, 46)]
    for x, o, h, l, c in cs:
        b.append(candle(x, o, h, l, c, 14))
    b.append(R(141, 124, 18, 54, "hl-box", 3))
    b.append(T(150, 200, "Bullish order block = last bearish candle before the impulse", "بلاک سفارش صعودی = آخرین کندل نزولی پیش از حرکت انفجاری",
               "t-bull", "start", size=12, weight=700))
    b.append(T(500, 120, "price returns → reaction", "بازگشت قیمت ← واکنش", "t-muted", "start", size=11.5))
    return svg(640, 214, "".join(b), "Order block")

def fvg():
    b = []
    # candle 1 high at 120, candle 3 low at 80 -> gap 80..120
    b.append(R(150, 80, 440, 40, "zone-brand", 4))
    b.append(candle(140, 150, 120, 176, 128, 22))
    b.append(candle(190, 130, 40, 136, 46, 22))
    b.append(candle(240, 50, 26, 80, 34, 22))
    b.append(L(120, 120, 600, 120, "ln-dim dashed")); b.append(L(120, 80, 600, 80, "ln-dim dashed"))
    b.append(T(480, 104, "Fair Value Gap", "شکاف ارزش منصفانه", "t-brand", size=13, weight=700))
    b.append(T(124, 116, "candle 1 high", "سایهٔ بالای کندل ۱", "t-dim", "end", size=11))
    b.append(T(262, 76, "candle 3 low", "سایهٔ پایین کندل ۳", "t-dim", "start", size=11))
    pts = [(260, 30), (320, 40), (380, 70), (420, 98), (460, 60), (520, 30), (590, 16)]
    b.append(poly(pts, "pl pl-price dashed"))
    b.append(T(320, 206, "Three candles — the gap between candle 1 and candle 3 is often revisited.",
               "سه کندل — شکاف میان کندل ۱ و ۳ اغلب دوباره لمس می‌شود.", "t-muted", size=12))
    return svg(640, 220, "".join(b), "Fair value gap")

def liquidity():
    b = []
    b.append(L(60, 60, 470, 60, "lvl-bear dashed"))
    b.append(T(70, 50, "Equal highs — buy-side liquidity (stops sit above)", "سقف‌های برابر — نقدینگی سمت خرید (حد ضررها بالای آن)", "t-bear", "start", size=12, weight=700))
    pts = [(40, 160), (100, 62), (150, 120), (220, 61), (270, 125), (340, 62), (390, 120), (440, 90), (470, 32), (500, 96), (550, 150), (610, 190)]
    b.append(poly(pts, "pl pl-price"))
    b.append(C(470, 32, 5, "dot-bear"))
    b.append(T(486, 30, "sweep", "سوییپ", "t-brand", "start", size=12, weight=700))
    b.append(T(630, 80, "reversal + CHoCH", "برگشت + CHoCH", "t-muted", "end", size=11.5))
    b.append(T(320, 214, "A quick spike through the level and straight back = a liquidity sweep, not a real breakout.",
               "نفوذ سریع از سطح و بازگشت فوری = سوییپ نقدینگی، نه شکست واقعی.", "t-muted", size=12))
    return svg(640, 228, "".join(b), "Liquidity sweep")

def killzones():
    x0, x1 = 110, 610
    def X(h): return x0 + (x1 - x0) * h / 24.0
    b = []
    for h in range(0, 25, 3):
        b.append(L(X(h), 34, X(h), 170, "grid"))
        b.append(T(X(h), 186, "%02d" % h, None, "t-dim", size=11))
        kh = (h + 4.5) % 24
        b.append(T(X(h), 204, "%02d:%02d" % (int(kh), 30 if kh % 1 else 0), None, "t-brand", size=10.5))
    b.append(T(84, 186, "GMT", "GMT", "t-dim", "end", size=11))
    b.append(T(84, 204, "Kabul", "کابل", "t-brand", "end", size=11))
    zones = [(0, 6, ("Asia (Tokyo)", "سشن آسیا"), "ses-asia"), (7, 10, ("London open", "باز شدن لندن"), "ses-london"),
             (12, 15, ("New York open", "باز شدن نیویورک"), "ses-ny"), (15, 17, ("NY/London close", "بستن لندن/نیویورک"), "ses-dim")]
    for i, (a, z, lab, k) in enumerate(zones):
        y = 44 + i * 30
        b.append(R(X(a), y, X(z) - X(a), 22, k, 5))
        b.append(T(X(z) + 6, y + 16, lab[0], lab[1], "t-strong", "start", size=11.5))
    b.append(T(360, 226, "Best window: the London–New York overlap, ~12:00–15:00 GMT (16:30–19:30 Kabul).",
               "بهترین بازه: هم‌پوشانی لندن و نیویورک، حدود ۱۲ تا ۱۵ GMT (۱۶:۳۰ تا ۱۹:۳۰ کابل).", "t-muted", size=12))
    return svg(640, 240, "".join(b), "Killzones")

def amd():
    b = [R(40, 96, 190, 50, "zone-dim", 4), R(230, 40, 150, 170, "zone-bear", 0), R(380, 30, 230, 180, "zone-bull", 0)]
    pts = [(40, 120), (60, 108), (80, 130), (100, 112), (120, 134), (140, 106), (160, 128), (180, 114), (200, 132), (230, 120),
           (260, 150), (290, 182), (310, 160), (340, 130), (380, 110), (420, 90), (460, 72), (500, 80), (540, 52), (600, 40)]
    b.append(poly(pts, "pl pl-price"))
    b.append(T(135, 86, "1. Accumulation", "۱. تجمیع", "t-strong", size=12.5, weight=700))
    b.append(T(135, 166, "Asia: tight range", "آسیا: محدودهٔ باریک", "t-muted", size=11.5))
    b.append(T(305, 30, "2. Manipulation", "۲. دستکاری", "t-bear", size=12.5, weight=700))
    b.append(T(305, 200, "London: fake move (Judas)", "لندن: حرکت نمایشی (یهودا)", "t-muted", size=11.5))
    b.append(T(495, 22, "3. Distribution", "۳. توزیع", "t-bull", size=12.5, weight=700))
    b.append(T(495, 200, "New York: the real move", "نیویورک: حرکت واقعی", "t-muted", size=11.5))
    return svg(640, 218, "".join(b), "Power of three")

def ote():
    b = []
    # swing low (80,200) to high (300,40); retracement levels measured from high down
    lo, hi = 200, 40
    def lvl(p): return hi + (lo - hi) * p
    b.append(R(300, lvl(0.62), 300, lvl(0.79) - lvl(0.62), "zone-bull", 3))
    for p, k in ((0.5, "ln-dim dashed"), (0.62, "lvl-bull"), (0.705, "lvl-bull dashed"), (0.79, "lvl-bull"), (1.0, "ln-dim")):
        b.append(L(80, lvl(p), 600, lvl(p), k))
        b.append(T(606, lvl(p) + 4, "%g%%" % (p * 100) if p not in (1.0,) else "100%", None, "t-dim", "start", size=11))
    b.append(L(80, hi, 600, hi, "ln-dim")); b.append(T(606, hi + 4, "0%", None, "t-dim", "start", size=11))
    pts = [(40, 150), (80, 200), (130, 150), (160, 165), (210, 100), (250, 115), (300, 40), (360, 90), (410, 125), (440, 150), (470, 120), (530, 60), (590, 20)]
    b.append(poly(pts, "pl pl-price"))
    b.append(T(160, 186, "CHoCH / MSS", None, "t-bull", size=11.5, weight=700))
    b.append(T(335, lvl(0.705) + 4, "OTE zone 62–79%", "ناحیهٔ OTE ۶۲ تا ۷۹٪", "t-bull", size=12.5, weight=700))
    b.append(T(320, 226, "Draw the Fibonacci on the new swing after the structure shift; enter in the 62–79% zone.",
               "فیبوناچی را روی موج جدید پس از تغییر ساختار رسم کنید؛ ورود در ناحیهٔ ۶۲ تا ۷۹٪.", "t-muted", size=12))
    return svg(640, 240, "".join(b), "Optimal trade entry")

# =========================================================================== advanced B

def carry():
    return flow([("Borrow a low-rate|currency (JPY)", "قرض گرفتن ارز|کم‌بهره (ین)"),
                 ("Invest in a|high-rate currency", "سرمایه‌گذاری در|ارز پربهره"),
                 ("Earn the|rate difference", "کسب تفاوت|نرخ بهره"),
                 ("Risk-off: trades|unwind fast", "ریسک‌گریزی: بسته|شدن سریع کری‌ترید")],
                title=("The carry trade", "کری‌ترید"))

def intermarket():
    b = [C(320, 130, 56, "hub")]
    b.append(T(320, 126, "Forex", "فارکس", "t-strong", size=15, weight=700))
    b.append(T(320, 146, "your pair", "جفت‌ارز شما", "t-muted", size=11.5))
    nodes = [(110, 46, ("DXY ↑", "DXY ↑"), ("pressure on non-USD pairs", "فشار بر جفت‌های غیردلاری")),
             (530, 46, ("US 10Y yield ↑", "بازده ۱۰ سالهٔ امریکا ↑"), ("supports the dollar", "حمایت از دلار")),
             (110, 214, ("Gold ↑", "طلا ↑"), ("helps AUD, ZAR", "کمک به AUD و ZAR")),
             (530, 214, ("Oil ↑", "نفت ↑"), ("helps CAD, NOK", "کمک به CAD و NOK")),
             (320, 250, ("COT extremes", "موقعیت افراطی COT"), ("possible reversal", "احتمال برگشت"))]
    for x, y, a, c in nodes:
        b.append(L(320, 130, x, y, "ln-dim"))
        b.append(R(x - 92, y - 24, 184, 48, "box-brand", 10))
        b.append(T(x, y - 4, a[0], a[1], "t-strong", size=12.5, weight=700))
        b.append(T(x, y + 14, c[0], c[1], "t-muted", size=11))
    return svg(640, 280, "".join(b), "Intermarket signals")

# =========================================================================== advanced C / D

def plan_parts():
    parts = [("Entry rules", "معیار ورود"), ("Invalidation", "معیار ابطال"), ("Stop & targets", "حد ضرر و حد سود"),
             ("Position size", "اندازهٔ موقعیت"), ("No-trade rules", "شرایط عدم معامله")]
    b = []
    for i, (en, f) in enumerate(parts):
        x = 20 + i * 122
        b.append(R(x, 40, 110, 110, "box-brand", 12))
        b.append(T(x + 55, 84, str(i + 1), None, "t-brand", size=26, weight=800))
        b.append(T(x + 55, 120, en, f, "t-strong", size=12.5, weight=700))
    b.append(T(320, 186, "Test of a good rule: someone else could follow it without asking you.",
               "محک یک قانون خوب: فرد دیگری بتواند بدون پرسیدن از شما آن را اجرا کند.", "t-muted", size=12.5))
    return svg(640, 200, "".join(b), "Five parts of a trading plan")

def expectancy():
    return bars([("System A — 60% wins, 1R : 1R", "سیستم الف — ۶۰٪ برد، ۱R : ۱R", 0.2, "warn"),
                 ("System B — 35% wins, 3R : 1R", "سیستم ب — ۳۵٪ برد، ۳R : ۱R", 0.4, "good")],
                0.5, "Expectancy per trade (average R) — higher is better",
                "Expectancy هر معامله (میانگین R) — هر چه بیشتر، بهتر", h=160, fmt=lambda v: "+%.1fR" % v)

def random_streaks():
    # deterministic pseudo-random W/L sequence with positive edge
    seq = "WLLWLWWLLLWLWWLWLLWWLWLLLWWLWWLWLWWLLWWLW"
    b = []
    eq = 0
    pts = [(40, 130)]
    for i, ch in enumerate(seq[:40]):
        x = 40 + i * 14
        b.append(R(x - 5, 186, 10, 16, "bar-good" if ch == "W" else "bar-bad", 2))
        eq += 1.6 if ch == "W" else -1
        pts.append((x + 7, 130 - eq * 6))
    b.append(poly(pts, "pl pl-price"))
    b.append(L(40, 130, 610, 130, "ln-dim dashed"))
    b.append(T(40, 24, "40 trades of a profitable system: wins and losses come in random clusters",
               "۴۰ معاملهٔ یک سیستم سودده: بردها و باخت‌ها به‌صورت تصادفی پشت سر هم می‌آیند", "t-muted", "start", size=12))
    b.append(T(40, 222, "each block = one trade (green win, red loss) · line = account", "هر مربع = یک معامله (سبز برد، سرخ باخت) · خط = حساب",
               "t-dim", "start", size=11))
    return svg(640, 236, "".join(b), "Random distribution of wins and losses")

def recovery():
    return bars([("Lose 10%", "۱۰٪ افت", 11.1, "good"), ("Lose 25%", "۲۵٪ افت", 33.3, "warn"),
                 ("Lose 50%", "۵۰٪ افت", 100, "bad"), ("Lose 75%", "۷۵٪ افت", 300, "bad")],
                300, "Gain needed to get back to where you started", "سود لازم برای بازگشت به نقطهٔ شروع",
                fmt=lambda v: "+%s%%" % ("%g" % v))

def oos():
    b = []
    import math
    pts = []
    for i in range(0, 61):
        x = 40 + i * 9
        if i <= 48:
            v = 160 - i * 2.2 + 8 * math.sin(i / 2.3)
        else:
            v = 160 - 48 * 2.2 + 8 * math.sin(48 / 2.3) + (i - 48) * 2.6 + 4 * math.sin(i)
        pts.append((x, round(v, 1)))
    b.append(R(40, 30, 432, 160, "zone-dim", 0))
    b.append(R(472, 30, 140, 160, "zone-bear", 0))
    b.append(poly(pts, "pl pl-price"))
    b.append(T(256, 50, "In-sample (80%): looks great", "داخل نمونه (۸۰٪): عالی به نظر می‌رسد", "t-strong", size=12.5, weight=700))
    b.append(T(542, 50, "Out-of-sample", "خارج از نمونه", "t-bear", size=12, weight=700))
    b.append(T(542, 68, "(20%) fails", "(۲۰٪) شکست", "t-bear", size=12))
    b.append(T(320, 214, "If results collapse on the data you kept aside, the plan is curve-fitted.",
               "اگر نتیجه روی داده‌های کنارگذاشته فرو بریزد، پلان بیش‌برازش شده است.", "t-muted", size=12))
    return svg(640, 228, "".join(b), "Out-of-sample test")

def style_choice():
    b = []
    b.append(R(220, 20, 200, 52, "box-brand", 10))
    b.append(T(320, 42, "How much time can you", "چقدر وقت پیوسته", "t-strong", size=12.5))
    b.append(T(320, 60, "watch charts each day?", "در روز دارید؟", "t-strong", size=12.5))
    b.append(arrow(260, 74, 160, 120, "arw arw-brand")); b.append(arrow(380, 74, 480, 120, "arw arw-brand"))
    b.append(T(178, 98, "a few short checks", "چند بررسی کوتاه", "t-muted", "end", size=11.5))
    b.append(T(462, 98, "hours, focused", "چند ساعت پیوسته", "t-muted", "start", size=11.5))
    b.append(R(60, 124, 200, 78, "box-bull", 10))
    b.append(T(160, 150, "Swing trading", "سوئینگ", "t-strong", size=13.5, weight=700))
    b.append(T(160, 170, "Weekly/Daily → 4H → 1H", "هفتگی/روزانه ← ۴ ساعته ← ۱ ساعته", "t-muted", size=11.5))
    b.append(T(160, 188, "fits a full-time job", "سازگار با شغل تمام‌وقت", "t-muted", size=11.5))
    b.append(R(380, 124, 200, 78, "box-warn", 10))
    b.append(T(480, 150, "Day trading", "معامله‌گری روزانه", "t-strong", size=13.5, weight=700))
    b.append(T(480, 170, "Daily/4H → 1H → 15m/5m", "روزانه/۴ ساعته ← ۱ ساعته ← ۱۵/۵ دقیقه", "t-muted", size=11.5))
    b.append(T(480, 188, "needs speed, more stress", "تصمیم سریع، استرس بیشتر", "t-muted", size=11.5))
    return svg(640, 214, "".join(b), "Choosing a trading style")

def capstone():
    parts = [("My trading world", "دنیای معاملاتی من", "F3"), ("Technical framework", "چارچوب تکنیکال", "A"), ("Macro routine", "روتین کلان", "B"),
             ("Entry & exit rules", "قوانین ورود و خروج", "C1"), ("Risk rules", "قوانین ریسک", "C2"), ("Stops & discipline", "توقف و انضباط", "C3–C4"),
             ("Style & backtest", "سبک و بک‌تست", "D1–D2")]
    b = []
    for i, (en, f, mod) in enumerate(parts):
        col, row = i % 4, i // 4
        x = 20 + col * 152 + (76 if row else 0)
        y = 20 + row * 92
        b.append(R(x, y, 140, 76, "box-brand" if i < 6 else "box-bull", 10))
        b.append(T(x + 22, y + 30, str(i + 1), None, "t-brand", size=20, weight=800))
        b.append(T(x + 76, y + 30, mod, mod, "t-dim", size=11))
        b.append(T(x + 70, y + 56, en, f, "t-strong", size=12, weight=700))
    b.append(T(320, 212, "Seven sections — one written plan you will actually trade with.", "هفت بخش — یک پلان مکتوب که واقعاً با آن معامله می‌کنید.", "t-muted", size=12.5))
    return svg(640, 226, "".join(b), "Capstone plan sections")

REG = {k: v for k, v in globals().items() if callable(v) and not k.startswith("_") and k not in
       ("fa", "T", "L", "R", "P", "C", "poly", "candle", "arrow", "svg", "bars", "flow", "cycle", "stairs", "render")}

def render(name):
    return REG[name]()
