# -*- coding: utf-8 -*-
"""Articles for the Articles page (built by build-articles.py into articles/*.html + the list on articles.html).

Every text is a pair (English, Dari). Newest article first. Body blocks are the same as the lesson
blocks in build-lessons.py: ("p", en, fa), ("ul"/"check"/"ol", [pairs]), ("note"/"tip"/"warn", title|None, body),
("table", head, rows), ("formula", "text" or pair, explanation), ("cmp", [(tone, title, items)]),
("stats", [(big, label)]). Articles are short, practical and evergreen; the full topics are taught in the classes.
"""

# Gregorian date -> shown as "1 November 2026" / «۱ نومبر ۲۰۲۶»
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MONTHS_FA = ["جنوری", "فبروری", "مارچ", "اپریل", "می", "جون", "جولای", "اگست", "سپتمبر", "اکتوبر", "نومبر", "دسمبر"]

NW = '<span class="nw">%s</span>'   # keep a number/time range on one line

CATEGORIES = {
    "basics": ("Forex basics", "مبانی فارکس"),
    "risk": ("Risk management", "مدیریت ریسک"),
    "timing": ("Market timing", "زمان‌بندی بازار"),
    "news": ("News & fundamentals", "اخبار و تحلیل بنیادی"),
}

ARTICLES = [
# ---------------------------------------------------------------------------------------------
dict(
    slug="5-beginner-mistakes", cat="risk", date="2026-11-01", mins=6, icon="⚠️",
    title=("5 Beginner Mistakes That Empty Trading Accounts", "۵ اشتباه تازه‌کاران که حساب معاملاتی را خالی می‌کند"),
    sub=("Most new traders don't lose because forex is impossible — they lose because of the same five avoidable mistakes.",
         "بیشتر معامله‌گران تازه‌کار به این دلیل ضرر نمی‌کنند که فارکس ناممکن است؛ آن‌ها به‌خاطر همین پنج اشتباهِ قابل‌پرهیز ضرر می‌کنند."),
    desc=("The five most common beginner forex mistakes — no stop-loss, too much leverage, revenge trading, no plan, and trusting 'guaranteed profit' signals — and how to avoid each one.",
          "پنج اشتباه رایج تازه‌کاران در فارکس — نگذاشتن حد ضرر، لیوریج زیاد، معاملهٔ انتقامی، نداشتن برنامه و اعتماد به سیگنال‌های «سود تضمینی» — و راه پرهیز از هر کدام."),
    summary=("No stop-loss, oversized lots, revenge trading, no plan and 'guaranteed' signals — and how to avoid all five.",
             "بدون حد ضرر، لات بزرگ، معاملهٔ انتقامی، بی‌برنامگی و سیگنال‌های «تضمینی» — و راه پرهیز از هر پنج."),
    key=[("Every trade needs a stop-loss before you enter.", "هر معامله پیش از ورود به حد ضرر نیاز دارد."),
         ("Risk a small, fixed part of your account — about 1% per trade.", "بخش کوچک و ثابتی از حساب را ریسک کنید — حدود ۱٪ در هر معامله."),
         ("After a loss, stop and review — don't try to win it back.", "پس از ضرر، دست نگه دارید و بررسی کنید — برای جبران عجله نکنید."),
         ("Nobody can guarantee profit. A promise of it is a warning sign.", "هیچ‌کس نمی‌تواند سود را تضمین کند. وعدهٔ آن یک علامت خطر است.")],
    sections=[
        (("Mistake 1: Trading without a stop-loss", "اشتباه ۱: معامله بدون حد ضرر"), [
            ("p", "A stop-loss is an order that closes your trade automatically at a price you choose in advance. Without one, a normal losing trade can turn into a disaster — because \"it will come back\" is what every trader says just before a big loss.",
                  "حد ضرر دستوری است که معامله را در قیمتی که از قبل انتخاب کرده‌اید به‌طور خودکار می‌بندد. بدون آن، یک معاملهٔ زیان‌دهِ عادی می‌تواند به فاجعه تبدیل شود؛ چون «قیمت برمی‌گردد» جمله‌ای است که هر معامله‌گر درست پیش از یک ضرر بزرگ به خودش می‌گوید."),
            ("tip", ("The fix", "راه‌حل"), ("Decide where you are wrong before you enter, and place the stop-loss with the order. Never move it further away once the trade is open.",
                                          "پیش از ورود تصمیم بگیرید در کجا اشتباه کرده‌اید و حد ضرر را همراه با دستور بگذارید. وقتی معامله باز شد، هرگز آن را دورتر نبرید.")),
        ]),
        (("Mistake 2: Too much leverage and lots that are too big", "اشتباه ۲: لیوریج زیاد و لات‌های بیش از حد بزرگ"), [
            ("p", "High leverage lets you open a big position with little money — but your profit and loss are calculated on the full position. On a $200 account, a 0.5-lot trade on EUR/USD moves $5 per pip: just 40 pips against you and the whole account is gone.",
                  "لیوریج بالا به شما اجازه می‌دهد با پول کم یک معاملهٔ بزرگ باز کنید؛ اما سود و ضرر شما بر اساس کل حجم معامله حساب می‌شود. در یک حساب ۲۰۰ دلاری، معاملهٔ ۰٫۵ لات روی EUR/USD با هر پیپ ۵ دلار تغییر می‌کند: فقط ۴۰ پیپ حرکت خلاف شما، و کل حساب از بین رفته است."),
            ("tip", ("The fix", "راه‌حل"), ("Choose your lot size from your stop-loss and a fixed risk (about 1% of the account), not from how much the broker lets you open.",
                                          "حجم لات را بر اساس حد ضرر و یک ریسک ثابت (حدود ۱٪ حساب) انتخاب کنید، نه بر اساس اینکه بروکر اجازهٔ باز کردن چه حجمی را می‌دهد.")),
        ]),
        (("Mistake 3: Revenge trading and overtrading", "اشتباه ۳: معاملهٔ انتقامی و بیش‌معامله‌گری"), [
            ("p", "After a loss, it is natural to want the money back immediately. So traders jump into the next trade — bigger, faster and without a real setup. One bad day becomes a destroyed account. Trading too often out of boredom does the same damage more slowly.",
                  "پس از ضرر، طبیعی است که بخواهید پول را فوراً پس بگیرید. پس معامله‌گر به معاملهٔ بعدی می‌پرد — بزرگ‌تر، سریع‌تر و بدون موقعیت واقعی. یک روز بد به یک حساب نابودشده تبدیل می‌شود. معاملهٔ زیاد از روی بی‌حوصلگی هم همین آسیب را آهسته‌تر می‌زند."),
            ("tip", ("The fix", "راه‌حل"), ("Set a daily limit — for example, stop for the day after 2 losing trades or a 2% loss. Close the platform and review the trades in your journal instead.",
                                          "یک سقف روزانه بگذارید — مثلاً پس از ۲ معاملهٔ زیان‌ده یا ۲٪ ضرر، آن روز را تمام کنید. پلتفرم را ببندید و به‌جای آن معاملات را در ژورنال خود بررسی کنید.")),
        ]),
        (("Mistake 4: Going live without a plan (or a demo)", "اشتباه ۴: رفتن به حساب واقعی بدون برنامه (یا دمو)"), [
            ("p", "Many beginners open a real account in their first week, trading on feelings and other people's opinions. Without written rules there is nothing to follow when the market gets emotional — and nothing to improve afterwards.",
                  "بسیاری از تازه‌کاران در هفتهٔ اول حساب واقعی باز می‌کنند و بر اساس احساس و نظر دیگران معامله می‌کنند. بدون قوانین نوشته‌شده، وقتی بازار هیجانی می‌شود چیزی برای پیروی وجود ندارد — و بعداً هم چیزی برای بهتر کردن."),
            ("check", [("Write a simple plan: which pairs, which setups, risk per trade, when you don't trade.", "یک برنامهٔ ساده بنویسید: کدام جفت‌ارزها، کدام موقعیت‌ها، ریسک هر معامله، و چه زمانی معامله نمی‌کنید."),
                       ("Follow it on a demo account for at least a month.", "دست‌کم یک ماه آن را روی حساب دمو اجرا کنید."),
                       ("Record every trade in a journal — entry, stop, result and why you took it.", "هر معامله را در ژورنال ثبت کنید — ورود، حد ضرر، نتیجه و دلیل ورود.")]),
        ]),
        (("Mistake 5: Trusting 'guaranteed profit' signals and schemes", "اشتباه ۵: اعتماد به سیگنال‌ها و طرح‌های «سود تضمینی»"), [
            ("p", "Groups that promise fixed monthly returns, \"account management\" where you send money to a person, or VIP signals with a perfect record are the fastest way to lose money in forex. Real trading always includes losing trades — nobody can guarantee profit.",
                  "گروه‌هایی که سود ماهانهٔ ثابت وعده می‌دهند، «مدیریت حساب» که در آن پول را برای یک شخص می‌فرستید، یا سیگنال‌های VIP با کارنامهٔ بی‌نقص، سریع‌ترین راه از دست دادن پول در فارکس‌اند. معاملهٔ واقعی همیشه معاملات زیان‌ده هم دارد — هیچ‌کس نمی‌تواند سود را تضمین کند."),
            ("warn", ("Warning signs", "علامت‌های خطر"), ("Guaranteed or fixed profits · pressure to deposit quickly · sending money to a personal account or wallet · a broker you cannot find on any regulator's website.",
                                                          "سود تضمینی یا ثابت · فشار برای واریز سریع · فرستادن پول به حساب یا کیف پول شخصی · بروکری که در وب‌سایت هیچ نهاد ناظری پیدا نمی‌شود.")),
        ]),
    ],
    tool=("/risk-calculator.html", ("Risk Calculator", "ماشین‌حساب ریسک"), ("Find the right lot size for your stop-loss and risk in seconds.", "حجم مناسب لات را برای حد ضرر و ریسک خود در چند ثانیه پیدا کنید.")),
),
# ---------------------------------------------------------------------------------------------
dict(
    slug="what-is-a-pip", cat="basics", date="2026-11-01", mins=5, icon="📏",
    title=("What Is a Pip? A Simple Guide With Examples", "پیپ چیست؟ راهنمای ساده با مثال"),
    sub=("Pips are how traders measure price moves, profits and losses. Here is how to count them — and what one pip is worth.",
         "پیپ واحدی است که معامله‌گران با آن حرکت قیمت، سود و ضرر را اندازه می‌گیرند. در اینجا روش شمردن آن — و ارزش هر پیپ — را می‌بینید."),
    desc=("What a pip is in forex, how to count pips on EUR/USD and USD/JPY, what a pipette is, and how much one pip is worth for standard, mini and micro lots.",
          "پیپ در فارکس چیست، چگونه پیپ‌ها را روی EUR/USD و USD/JPY بشماریم، پیپت چیست و ارزش هر پیپ برای لات استاندارد، مینی و میکرو چقدر است."),
    summary=("How to count pips on any pair, what a pipette is, and how much one pip is worth for each lot size.",
             "شمردن پیپ روی هر جفت‌ارز، پیپت چیست و ارزش هر پیپ برای هر اندازهٔ لات."),
    key=[("For most pairs, 1 pip = 0.0001 (the 4th decimal).", "برای بیشتر جفت‌ارزها، ۱ پیپ = ۰٫۰۰۰۱ (رقم چهارم اعشار)."),
         ("For pairs with the Japanese yen, 1 pip = 0.01 (the 2nd decimal).", "برای جفت‌ارزهای دارای ین ژاپن، ۱ پیپ = ۰٫۰۱ (رقم دوم اعشار)."),
         ("On EUR/USD, 1 standard lot = $10 per pip, 0.1 lot = $1, 0.01 lot = $0.10.", "روی EUR/USD، ۱ لات استاندارد = ۱۰ دلار برای هر پیپ، ۰٫۱ لات = ۱ دلار، ۰٫۰۱ لات = ۰٫۱۰ دلار.")],
    sections=[
        (("What a pip is", "پیپ چیست"), [
            ("p", "A pip (\"percentage in point\") is the standard unit for measuring how much an exchange rate moves. For most currency pairs it is the fourth digit after the decimal point. If EUR/USD moves from 1.0850 to 1.0851, it has moved 1 pip.",
                  "پیپ (Percentage in Point) واحد استاندارد برای اندازه‌گیری میزان حرکت نرخ ارز است. برای بیشتر جفت‌ارزها، پیپ رقم چهارم پس از ممیز است. اگر EUR/USD از ۱٫۰۸۵۰ به ۱٫۰۸۵۱ برود، ۱ پیپ حرکت کرده است."),
            ("table", [("Pair", "جفت‌ارز"), ("1 pip", "۱ پیپ"), ("Price moves", "حرکت قیمت"), ("Pips", "پیپ")], [
                ["EUR/USD", ("0.0001", "۰٫۰۰۰۱"), (NW % "1.0850 → 1.0880", "از %s تا %s" % (NW % "۱٫۰۸۵۰", NW % "۱٫۰۸۸۰")), ("30", "۳۰")],
                ["GBP/USD", ("0.0001", "۰٫۰۰۰۱"), (NW % "1.2700 → 1.2650", "از %s تا %s" % (NW % "۱٫۲۷۰۰", NW % "۱٫۲۶۵۰")), ("50", "۵۰")],
                ["USD/JPY", ("0.01", "۰٫۰۱"), (NW % "150.20 → 150.95", "از %s تا %s" % (NW % "۱۵۰٫۲۰", NW % "۱۵۰٫۹۵")), ("75", "۷۵")],
            ]),
            ("note", ("What about the 5th digit?", "رقم پنجم چیست؟"), ("Most brokers show one extra digit — 1.08512 instead of 1.0851. That last digit is a pipette, one tenth of a pip. So a move of 15 pipettes is 1.5 pips.",
                                                                       "بیشتر بروکرها یک رقم اضافه نشان می‌دهند — ۱٫۰۸۵۱۲ به‌جای ۱٫۰۸۵۱. آن رقم آخر «پیپت» است، یعنی یک‌دهم پیپ. پس حرکت ۱۵ پیپت برابر ۱٫۵ پیپ است.")),
        ]),
        (("How much is one pip worth?", "ارزش هر پیپ چقدر است؟"), [
            ("p", "The value of a pip depends on your position size (lot). When the US dollar is the second currency of the pair (EUR/USD, GBP/USD, AUD/USD…), the value is easy to remember:",
                  "ارزش هر پیپ به حجم معاملهٔ شما (لات) بستگی دارد. وقتی دلار امریکا ارز دوم جفت باشد (EUR/USD، GBP/USD، AUD/USD…)، ارزش آن به‌آسانی به یاد می‌ماند:"),
            ("table", [("Lot", "لات"), ("Units", "واحد"), ("Value of 1 pip", "ارزش ۱ پیپ")], [
                [("1.00 (standard)", "۱٫۰۰ (استاندارد)"), ("100,000", "۱۰۰٬۰۰۰"), ("$10", "۱۰ دلار")],
                [("0.10 (mini)", "۰٫۱۰ (مینی)"), ("10,000", "۱۰٬۰۰۰"), ("$1", "۱ دلار")],
                [("0.01 (micro)", "۰٫۰۱ (میکرو)"), ("1,000", "۱٬۰۰۰"), ("$0.10", "۰٫۱۰ دلار")],
            ]),
            ("formula", ("Profit or loss = pips × value of 1 pip", "سود یا ضرر = تعداد پیپ × ارزش ۱ پیپ"),
                        ("Example: you buy 0.10 lot of EUR/USD at 1.0850 and close at 1.0880. That is 30 pips × $1 = $30 profit.",
                         "مثال: ۰٫۱۰ لات EUR/USD را در ۱٫۰۸۵۰ می‌خرید و در ۱٫۰۸۸۰ می‌بندید. یعنی ۳۰ پیپ × ۱ دلار = ۳۰ دلار سود.")),
            ("p", "For other pairs the pip value changes a little with the exchange rate. For example, on USD/JPY at 150.00 one standard lot is worth about $6.67 per pip. You don't need to calculate this by hand — the Pip Calculator does it for you.",
                  "برای جفت‌ارزهای دیگر، ارزش پیپ کمی با نرخ ارز تغییر می‌کند. مثلاً روی USD/JPY در نرخ ۱۵۰٫۰۰، هر لات استاندارد برای هر پیپ حدود ۶٫۶۷ دلار ارزش دارد. لازم نیست این را با دست حساب کنید — ماشین‌حساب پیپ این کار را برای شما انجام می‌دهد."),
        ]),
        (("Why pips matter for every trade", "چرا پیپ در هر معامله مهم است"), [
            ("ul", [("Spread: the difference between buy and sell price is measured in pips — it is the cost of opening a trade.", "اسپرد: فاصلهٔ قیمت خرید و فروش به پیپ اندازه‌گیری می‌شود — این هزینهٔ باز کردن معامله است."),
                    ("Stop-loss and take-profit: you plan them in pips, e.g. a 25-pip stop and a 50-pip target.", "حد ضرر و حد سود: آن‌ها را به پیپ برنامه‌ریزی می‌کنید، مثلاً حد ضرر ۲۵ پیپ و هدف ۵۰ پیپ."),
                    ("Risk: pips × pip value tells you exactly how many dollars you can lose before you enter.", "ریسک: تعداد پیپ × ارزش پیپ دقیقاً به شما می‌گوید پیش از ورود چند دلار ممکن است از دست بدهید.")]),
            ("note", ("Gold and indices", "طلا و شاخص‌ها"), ("For gold (XAU/USD), oil and indices, brokers define a \"pip\" differently. Always check the contract details on your broker's platform before you trade them.",
                                                         "برای طلا (XAU/USD)، نفت و شاخص‌ها، بروکرها «پیپ» را متفاوت تعریف می‌کنند. پیش از معامله، همیشه مشخصات قرارداد را در پلتفرم بروکر خود بررسی کنید.")),
        ]),
    ],
    tool=("/pip-calculator.html", ("Pip Calculator", "ماشین‌حساب پیپ"), ("See the value of one pip for any pair and lot size.", "ارزش یک پیپ را برای هر جفت‌ارز و هر حجم لات ببینید.")),
),
# ---------------------------------------------------------------------------------------------
dict(
    slug="position-size-1-percent-rule", cat="risk", date="2026-11-01", mins=5, icon="🎯",
    title=("How Much Should You Risk? Position Size and the 1% Rule", "چقدر ریسک کنیم؟ حجم معامله و قانون ۱٪"),
    sub=("The size of your trade — not your strategy — decides whether a losing streak is a small setback or the end of your account.",
         "اندازهٔ معاملهٔ شما — نه استراتژی‌تان — تعیین می‌کند که یک سلسله ضرر، یک عقب‌نشینی کوچک باشد یا پایان حساب شما."),
    desc=("How to calculate forex position size with the 1% rule: a simple formula, worked examples, and why small risk per trade protects your account from losing streaks.",
          "چگونه حجم معامله را با قانون ۱٪ حساب کنیم: یک فرمول ساده، مثال‌های عملی و اینکه چرا ریسک کم در هر معامله حساب را در برابر ضررهای پیاپی حفظ می‌کند."),
    summary=("A simple formula for lot size, worked examples, and why 1% per trade survives a losing streak.",
             "فرمول سادهٔ حجم لات، مثال‌های عملی، و اینکه چرا ۱٪ در هر معامله از سلسلهٔ ضررها جان سالم به در می‌برد."),
    key=[("Decide your risk in money first: about 1% of the account per trade.", "اول ریسک را به پول مشخص کنید: حدود ۱٪ حساب در هر معامله."),
         ("Lot size = risk ÷ (stop-loss in pips × pip value of 1 lot).", "حجم لات = ریسک ÷ (حد ضرر به پیپ × ارزش پیپ برای ۱ لات)."),
         ("A wider stop means a smaller lot — the risk in dollars stays the same.", "حد ضرر بازتر یعنی لات کوچک‌تر — ریسک به دلار ثابت می‌ماند.")],
    sections=[
        (("Start with the money you are willing to lose", "از پولی شروع کنید که حاضرید از دست بدهید"), [
            ("p", "Professional traders don't ask \"how much can I make?\" first. They ask \"how much will I lose if I'm wrong?\" A common rule is to risk no more than 1% of your account on one trade (2% at most). On a $1,000 account, 1% is $10.",
                  "معامله‌گران حرفه‌ای اول نمی‌پرسند «چقدر می‌توانم سود کنم؟». آن‌ها می‌پرسند «اگر اشتباه کنم چقدر ضرر می‌کنم؟». یک قانون رایج این است که در هر معامله بیش از ۱٪ حساب را ریسک نکنید (حداکثر ۲٪). در یک حساب ۱٬۰۰۰ دلاری، ۱٪ یعنی ۱۰ دلار."),
            ("p", "Why so small? Because every trader has losing streaks. Look at what 10 losses in a row do to an account at different risk levels:",
                  "چرا این‌قدر کم؟ چون هر معامله‌گری دوره‌های ضرر پیاپی دارد. ببینید ۱۰ ضرر پشت سر هم با سطوح مختلف ریسک با حساب چه می‌کند:"),
            ("table", [("Risk per trade", "ریسک هر معامله"), ("Account left after 10 losses", "باقی‌ماندهٔ حساب پس از ۱۰ ضرر")], [
                [("1%", "۱٪"), ("about 90%", "حدود ۹۰٪")],
                [("5%", "۵٪"), ("about 60%", "حدود ۶۰٪")],
                [("10%", "۱۰٪"), ("about 35%", "حدود ۳۵٪")],
            ]),
            ("note", None, ("And losses are harder to recover than they look: after losing 50% of an account, you need +100% just to get back to where you started.",
                            "و جبران ضرر سخت‌تر از آن است که به نظر می‌رسد: پس از از دست دادن ۵۰٪ حساب، فقط برای برگشتن به نقطهٔ شروع به ۱۰۰٪ سود نیاز دارید.")),
        ]),
        (("The position size formula", "فرمول حجم معامله"), [
            ("formula", ("Lot size = Risk in $ ÷ (Stop-loss in pips × pip value for 1 lot)", "حجم لات = ریسک به دلار ÷ (حد ضرر به پیپ × ارزش پیپ برای ۱ لات)"),
                        ("For EUR/USD and other …/USD pairs, the pip value for 1 lot is $10.", "برای EUR/USD و دیگر جفت‌های …/USD، ارزش پیپ برای ۱ لات ۱۰ دلار است.")),
            ("ol", [("Account $1,000, risk 1% = $10.", "حساب ۱٬۰۰۰ دلار، ریسک ۱٪ = ۱۰ دلار."),
                    ("Your stop-loss is 25 pips away on EUR/USD.", "حد ضرر شما روی EUR/USD در فاصلهٔ ۲۵ پیپ است."),
                    ("$10 ÷ (25 × $10) = 0.04 lot.", "۱۰ ÷ (۲۵ × ۱۰) = ۰٫۰۴ لات."),
                    ("Check: 0.04 lot = $0.40 per pip × 25 pips = $10. ✓", "بررسی: ۰٫۰۴ لات = ۰٫۴۰ دلار برای هر پیپ × ۲۵ پیپ = ۱۰ دلار. ✓")]),
            ("tip", ("Same risk, different stop", "ریسک یکسان، حد ضرر متفاوت"), ("If the chart needs a 50-pip stop instead, the lot becomes 0.02. You still risk $10 — the stop goes where the chart says, and the lot size adjusts.",
                                                                               "اگر نمودار به‌جای آن حد ضرر ۵۰ پیپی لازم داشته باشد، لات ۰٫۰۲ می‌شود. شما همچنان ۱۰ دلار ریسک می‌کنید — حد ضرر جایی می‌رود که نمودار می‌گوید، و حجم لات خودش را تنظیم می‌کند.")),
        ]),
        (("Common questions", "پرسش‌های رایج"), [
            ("cmp", [("good", ("Do", "انجام دهید"), [("Calculate the lot size before every trade", "پیش از هر معامله حجم لات را حساب کنید"),
                                                       ("Keep the same % risk on every trade", "در همهٔ معاملات درصد ریسک یکسان نگه دارید"),
                                                       ("Round the lot size down, not up", "حجم لات را به پایین گرد کنید، نه به بالا")]),
                     ("bad", ("Don't", "انجام ندهید"), [("Pick a lot size because it \"feels right\"", "حجم لات را به این دلیل انتخاب نکنید که «حس خوبی دارد»"),
                                                         ("Increase risk to win back a loss", "برای جبران ضرر ریسک را بالا نبرید"),
                                                         ("Move the stop to fit a bigger lot", "حد ضرر را برای جا دادن لات بزرگ‌تر جابه‌جا نکنید")])]),
            ("p", "If your account is very small, even 0.01 lot may be more than 1% risk with a wide stop. In that case, choose setups with tighter stops — or keep practising on demo while you build the account.",
                  "اگر حساب شما خیلی کوچک است، حتی ۰٫۰۱ لات با یک حد ضرر باز ممکن است بیش از ۱٪ ریسک باشد. در این صورت، موقعیت‌هایی با حد ضرر نزدیک‌تر انتخاب کنید — یا تا بزرگ شدن حساب، روی دمو تمرین را ادامه دهید."),
        ]),
    ],
    tool=("/risk-calculator.html", ("Risk Calculator", "ماشین‌حساب ریسک"), ("Enter your balance, risk % and stop-loss — get the lot size instantly.", "موجودی، درصد ریسک و حد ضرر را وارد کنید — حجم لات را فوراً بگیرید.")),
),
# ---------------------------------------------------------------------------------------------
dict(
    slug="leverage-and-margin-explained", cat="basics", date="2026-11-01", mins=6, icon="⚖️",
    title=("Leverage and Margin Explained Simply", "لیوریج و مارجین به زبان ساده"),
    sub=("Leverage is a tool, not free money. Understand margin, free margin and margin call before they surprise you.",
         "لیوریج یک ابزار است، نه پول رایگان. مارجین، مارجین آزاد و مارجین کال را پیش از آنکه غافلگیرتان کنند بشناسید."),
    desc=("Forex leverage and margin explained with simple examples: how much margin a trade needs, what free margin and margin level are, and how margin call and stop-out work.",
          "توضیح لیوریج و مارجین در فارکس با مثال‌های ساده: هر معامله چقدر مارجین لازم دارد، مارجین آزاد و سطح مارجین چیست، و مارجین کال و استاپ‌اوت چگونه کار می‌کنند."),
    summary=("How much margin a trade needs, what free margin and margin level mean, and how margin call works.",
             "هر معامله چقدر مارجین لازم دارد، مارجین آزاد و سطح مارجین یعنی چه، و مارجین کال چگونه کار می‌کند."),
    key=[("Leverage decides how big a position you CAN open — not how big you SHOULD open.", "لیوریج تعیین می‌کند چه معامله‌ای را «می‌توانید» باز کنید — نه اینکه «باید» باز کنید."),
         ("Margin is a deposit the broker holds while your trade is open.", "مارجین ودیعه‌ای است که بروکر تا باز بودن معامله نگه می‌دارد."),
         ("Your profit and loss always depend on the full position size.", "سود و ضرر شما همیشه به کل حجم معامله بستگی دارد.")],
    sections=[
        (("What leverage does", "لیوریج چه می‌کند"), [
            ("p", "One standard lot of EUR/USD is 100,000 euros — about $108,500. Almost nobody has that, so brokers lend you the difference. With 1:100 leverage, you need only 1/100 of the position as a deposit (margin).",
                  "یک لات استاندارد EUR/USD برابر ۱۰۰٬۰۰۰ یورو است — حدود ۱۰۸٬۵۰۰ دلار. تقریباً هیچ‌کس چنین پولی ندارد، پس بروکر مابه‌التفاوت را به شما قرض می‌دهد. با لیوریج ۱:۱۰۰، فقط به ۱/۱۰۰ حجم معامله به‌عنوان ودیعه (مارجین) نیاز دارید."),
            ("formula", ("Required margin = (lots × 100,000 × price) ÷ leverage", "مارجین لازم = (لات × ۱۰۰٬۰۰۰ × قیمت) ÷ لیوریج"),
                        ("For EUR/USD at 1.0850, 0.10 lot = $10,850 position.", "برای EUR/USD با قیمت ۱٫۰۸۵۰، معاملهٔ ۰٫۱۰ لات ارزشی برابر ۱۰٬۸۵۰ دلار دارد.")),
            ("table", [("Leverage", "لیوریج"), ("Margin for 0.10 lot EUR/USD", "مارجین برای ۰٫۱۰ لات EUR/USD"), ("Value of 1 pip", "ارزش ۱ پیپ")], [
                [("1:30", "۱:۳۰"), ("about $362", "حدود ۳۶۲ دلار"), ("$1", "۱ دلار")],
                [("1:100", "۱:۱۰۰"), ("about $109", "حدود ۱۰۹ دلار"), ("$1", "۱ دلار")],
                [("1:500", "۱:۵۰۰"), ("about $22", "حدود ۲۲ دلار"), ("$1", "۱ دلار")],
            ]),
            ("note", ("Notice the last column", "به ستون آخر دقت کنید"), ("Leverage changes the deposit, not the risk. The same trade makes or loses $1 per pip whatever your leverage is.",
                                                                        "لیوریج ودیعه را تغییر می‌دهد، نه ریسک را. همین معامله با هر لیوریجی، برای هر پیپ ۱ دلار سود یا ضرر می‌کند.")),
        ]),
        (("Balance, equity, free margin and margin level", "موجودی، اکوئیتی، مارجین آزاد و سطح مارجین"), [
            ("table", [("Term", "اصطلاح"), ("Meaning", "معنی")], [
                [("Balance", "موجودی (Balance)"), ("Your money without counting open trades.", "پول شما بدون حساب کردن معاملات باز.")],
                [("Equity", "اکوئیتی (Equity)"), ("Balance + profit/loss of open trades — what your account is worth right now.", "موجودی + سود/ضرر معاملات باز — ارزش همین لحظهٔ حساب شما.")],
                [("Used margin", "مارجین استفاده‌شده"), ("The deposits held for your open trades.", "ودیعه‌هایی که برای معاملات باز شما نگه داشته شده است.")],
                [("Free margin", "مارجین آزاد"), ("Equity − used margin: what is left to absorb losses or open new trades.", "اکوئیتی − مارجین استفاده‌شده: آنچه برای تحمل ضرر یا باز کردن معاملهٔ جدید باقی مانده است.")],
                [("Margin level", "سطح مارجین"), ("Equity ÷ used margin × 100%.", "اکوئیتی ÷ مارجین استفاده‌شده × ۱۰۰٪.")],
            ]),
        ]),
        (("Margin call and stop-out", "مارجین کال و استاپ‌اوت"), [
            ("p", "When losses shrink your equity, the margin level falls. At the broker's margin call level (often 100%) you cannot open new trades. If it keeps falling to the stop-out level (often 20–50%), the broker starts closing your trades automatically — at the worst possible moment.",
                  "وقتی ضررها اکوئیتی را کم می‌کنند، سطح مارجین پایین می‌آید. در سطح مارجین کالِ بروکر (اغلب ۱۰۰٪) دیگر نمی‌توانید معاملهٔ جدید باز کنید. اگر باز هم پایین بیاید و به سطح استاپ‌اوت برسد (اغلب ۲۰ تا ۵۰٪)، بروکر شروع به بستن خودکار معاملات شما می‌کند — در بدترین لحظهٔ ممکن."),
            ("warn", ("A real example", "یک مثال واقعی"), ("$200 account, 1:500 leverage. The trader opens 0.5 lot of EUR/USD — margin is only about $108, so it looks fine. But every pip is now $5: a 40-pip move against the trade wipes out the entire account.",
                                                         "حساب ۲۰۰ دلاری، لیوریج ۱:۵۰۰. معامله‌گر ۰٫۵ لات EUR/USD باز می‌کند — مارجین فقط حدود ۱۰۸ دلار است، پس به نظر مشکلی نیست. اما حالا هر پیپ ۵ دلار است: یک حرکت ۴۰ پیپی خلاف او کل حساب را از بین می‌برد.")),
            ("tip", ("The safe way", "روش امن"), ("Size every trade with the 1% rule and a stop-loss. Then leverage simply means less of your money is locked as margin — and margin call never becomes a worry.",
                                                  "هر معامله را با قانون ۱٪ و حد ضرر اندازه بگیرید. آن‌وقت لیوریج فقط یعنی پول کمتری از شما به‌عنوان مارجین قفل می‌شود — و مارجین کال هرگز نگرانی نمی‌شود.")),
        ]),
    ],
    tool=("/margin-calculator.html", ("Margin & Leverage Calculator", "ماشین‌حساب مارجین و لیوریج"), ("See the margin any trade needs before you open it.", "پیش از باز کردن هر معامله، مارجین لازم آن را ببینید.")),
),
# ---------------------------------------------------------------------------------------------
dict(
    slug="best-time-to-trade-forex-kabul", cat="timing", date="2026-11-01", mins=5, icon="🕐",
    title=("The Best Time to Trade Forex From Afghanistan (Kabul Time)", "بهترین زمان معامله در فارکس از افغانستان (به وقت کابل)"),
    sub=("The forex market is open 24 hours on weekdays — but not every hour is worth trading. Here are the sessions in Kabul time.",
         "بازار فارکس در روزهای کاری ۲۴ ساعته باز است — اما هر ساعتی ارزش معامله ندارد. در اینجا جلسه‌های معاملاتی را به وقت کابل می‌بینید."),
    desc=("Forex trading sessions in Kabul time: when Sydney, Tokyo, London and New York open and close, the London–New York overlap, and the best hours to trade from Afghanistan.",
          "جلسه‌های معاملاتی فارکس به وقت کابل: زمان باز و بسته شدن سیدنی، توکیو، لندن و نیویورک، هم‌پوشانی لندن و نیویورک، و بهترین ساعات معامله از افغانستان."),
    summary=("Sydney, Tokyo, London and New York sessions in Kabul time — and why the evening is the busiest time to trade.",
             "جلسه‌های سیدنی، توکیو، لندن و نیویورک به وقت کابل — و اینکه چرا شب پرتحرک‌ترین زمان معامله است."),
    key=[("The market opens Monday after midnight and closes early Saturday morning, Kabul time.", "بازار دوشنبه پس از نیمه‌شب باز می‌شود و صبح زود شنبه به وقت کابل بسته می‌شود."),
         ("The busiest hours are the London–New York overlap: about 17:30–21:30 Kabul time in winter.", "پرتحرک‌ترین ساعات، هم‌پوشانی لندن و نیویورک است: در زمستان حدود ۱۷:۳۰ تا ۲۱:۳۰ به وقت کابل."),
         ("Europe and the US change their clocks; Kabul doesn't — so session times shift by one hour twice a year.", "اروپا و امریکا ساعت‌های خود را تغییر می‌دهند؛ کابل نه — پس زمان جلسه‌ها سالی دو بار یک ساعت جابه‌جا می‌شود.")],
    sections=[
        (("Four sessions, one market", "چهار جلسه، یک بازار"), [
            ("p", "Forex has no single exchange. Trading moves around the world with the banks' working day: from Sydney and Tokyo, to London, then New York. Afghanistan sits in the middle, which makes the busiest sessions fall in the afternoon and evening — convenient if you work or study during the day.",
                  "فارکس بورس واحدی ندارد. معامله با روز کاری بانک‌ها دور دنیا می‌چرخد: از سیدنی و توکیو، به لندن، و سپس نیویورک. افغانستان در میانه قرار دارد؛ به همین دلیل پرتحرک‌ترین جلسه‌ها در بعدازظهر و شب می‌افتند — که برای کسی که روزها کار می‌کند یا درس می‌خواند مناسب است."),
            ("table", [("Session (Kabul time)", "جلسه (وقت کابل)"), ("Winter", "زمستان"), ("Summer", "تابستان")], [
                [("Sydney", "سیدنی"), (NW % "00:30 – 09:30", NW % "۰۰:۳۰ – ۰۹:۳۰"), (NW % "01:30 – 10:30", NW % "۰۱:۳۰ – ۱۰:۳۰")],
                [("Tokyo", "توکیو"), (NW % "04:30 – 13:30", NW % "۰۴:۳۰ – ۱۳:۳۰"), (NW % "04:30 – 13:30", NW % "۰۴:۳۰ – ۱۳:۳۰")],
                [("London", "لندن"), (NW % "12:30 – 21:30", NW % "۱۲:۳۰ – ۲۱:۳۰"), (NW % "11:30 – 20:30", NW % "۱۱:۳۰ – ۲۰:۳۰")],
                [("New York", "نیویورک"), (NW % "17:30 – 02:30", NW % "۱۷:۳۰ – ۰۲:۳۰"), (NW % "16:30 – 01:30", NW % "۱۶:۳۰ – ۰۱:۳۰")],
            ]),
            ("note", ("Winter and summer", "زمستان و تابستان"), ("\"Winter\" here means early November to mid-March, when the US and UK are on standard time. Sydney is the other way round: its summer time runs October to April. The Market Hours tool always shows the live times.",
                                                              "«زمستان» در اینجا یعنی از اوایل نومبر تا اواسط مارچ، وقتی امریکا و بریتانیا در ساعت استاندارد هستند. سیدنی برعکس است: ساعت تابستانی آن از اکتوبر تا اپریل است. ابزار ساعات بازار همیشه زمان‌های لحظه‌ای را نشان می‌دهد.")),
        ]),
        (("When to trade — and when to wait", "چه زمانی معامله کنیم — و چه زمانی صبر کنیم"), [
            ("cmp", [("good", ("Good times", "زمان‌های خوب"), [("London session — the biggest session; EUR, GBP and CHF pairs move most", "جلسهٔ لندن — بزرگ‌ترین جلسه؛ جفت‌ارزهای EUR، GBP و CHF بیشترین حرکت را دارند"),
                                                                  ("London–New York overlap — highest volume and tightest spreads", "هم‌پوشانی لندن و نیویورک — بیشترین حجم و کمترین اسپرد"),
                                                                  ("Tokyo session for JPY, AUD and NZD pairs (Kabul morning)", "جلسهٔ توکیو برای جفت‌ارزهای JPY، AUD و NZD (صبح کابل)")]),
                     ("bad", ("Be careful", "احتیاط کنید"), [("Late night after New York closes — thin market, wide spreads", "نیمه‌شب پس از بسته شدن نیویورک — بازار کم‌حجم، اسپرد بالا"),
                                                             ("Monday's first hours — prices can open with a gap", "ساعات اول دوشنبه — قیمت ممکن است با گپ باز شود"),
                                                             ("Minutes before and after high-impact news", "چند دقیقه پیش و پس از اخبار پراهمیت")])]),
            ("p", "Note for Afghan traders: Friday is a full trading day for the market, even though it is our weekend — and US jobs data (NFP), one of the most volatile releases of the month, usually comes out on the first Friday evening. The market is closed on Saturday and Sunday.",
                  "نکته برای معامله‌گران افغان: جمعه برای بازار یک روز کامل معاملاتی است، با اینکه تعطیلی آخر هفتهٔ ماست — و گزارش اشتغال امریکا (NFP)، یکی از پرنوسان‌ترین اخبار ماه، معمولاً شام اولین جمعهٔ هر ماه منتشر می‌شود. بازار شنبه و یکشنبه بسته است."),
            ("tip", ("Pick your hours", "ساعت‌های خود را انتخاب کنید"), ("You don't need to watch the market all day. Choose one session that fits your life — for most of our students that is the London–New York overlap in the evening — and trade only then.",
                                                                     "لازم نیست تمام روز بازار را تماشا کنید. یک جلسه را که با زندگی شما سازگار است انتخاب کنید — برای بیشتر شاگردان ما این همان هم‌پوشانی لندن و نیویورک در شب است — و فقط در همان زمان معامله کنید.")),
        ]),
    ],
    tool=("/market-hours.html", ("Market Hours (Kabul time)", "ساعات بازار (به وقت کابل)"), ("A live clock showing which sessions are open right now.", "ساعتی زنده که نشان می‌دهد همین حالا کدام جلسه‌ها باز هستند.")),
),
# ---------------------------------------------------------------------------------------------
dict(
    slug="how-to-read-the-economic-calendar", cat="news", date="2026-11-01", mins=6, icon="📅",
    title=("How to Read the Economic Calendar", "چگونه تقویم اقتصادی را بخوانیم"),
    sub=("Big news moves the market in seconds. Learn what the calendar columns mean and which events every forex trader should know.",
         "اخبار مهم بازار را در چند ثانیه حرکت می‌دهد. یاد بگیرید ستون‌های تقویم اقتصادی چه معنایی دارند و هر معامله‌گر فارکس کدام رویدادها را باید بشناسد."),
    desc=("How to read a forex economic calendar: impact levels, actual vs forecast vs previous, the most important events (interest rates, CPI, NFP) and how to trade safely around news.",
          "چگونه تقویم اقتصادی فارکس را بخوانیم: سطح اهمیت، مقدار واقعی در برابر پیش‌بینی و قبلی، مهم‌ترین رویدادها (نرخ بهره، CPI، NFP) و معاملهٔ امن در زمان اخبار."),
    summary=("Impact levels, actual vs forecast, the events that matter most — and a simple weekly routine.",
             "سطح اهمیت، مقدار واقعی در برابر پیش‌بینی، رویدادهای مهم — و یک روال سادهٔ هفتگی."),
    key=[("Check the calendar before the week starts and before every trade.", "پیش از شروع هفته و پیش از هر معامله تقویم را بررسی کنید."),
         ("The market reacts to the surprise: the difference between actual and forecast.", "بازار به غافلگیری واکنش نشان می‌دهد: فاصلهٔ مقدار واقعی و پیش‌بینی."),
         ("Around high-impact news, spreads widen and prices can jump past your stop.", "در زمان اخبار پراهمیت، اسپرد بالا می‌رود و قیمت ممکن است از حد ضرر شما بپرد.")],
    sections=[
        (("The columns, one by one", "ستون‌ها، یکی‌یکی"), [
            ("table", [("Column", "ستون"), ("What it tells you", "چه چیزی به شما می‌گوید")], [
                [("Time", "زمان"), ("When the number is released — set the calendar to Kabul time (GMT+4:30).", "زمان انتشار عدد — تقویم را روی وقت کابل (GMT+4:30) تنظیم کنید.")],
                [("Currency", "ارز"), ("Which currency is most likely to move (USD, EUR, GBP…).", "کدام ارز به احتمال زیاد حرکت می‌کند (USD، EUR، GBP…).")],
                [("Impact", "اهمیت"), ("Low, medium or high. High-impact events can move a pair 50–100 pips in minutes.", "کم، متوسط یا زیاد. رویدادهای پراهمیت می‌توانند یک جفت‌ارز را در چند دقیقه ۵۰ تا ۱۰۰ پیپ حرکت دهند.")],
                [("Actual", "واقعی"), ("The real number, shown at release time.", "عدد واقعی که در زمان انتشار نشان داده می‌شود.")],
                [("Forecast", "پیش‌بینی"), ("What economists expected. Prices usually already reflect it.", "آنچه اقتصاددانان انتظار داشتند. قیمت‌ها معمولاً از قبل آن را در خود دارند.")],
                [("Previous", "قبلی"), ("The last release — useful to see the trend.", "انتشار قبلی — برای دیدن روند مفید است.")],
            ]),
            ("note", ("It's the surprise that moves price", "این غافلگیری است که قیمت را حرکت می‌دهد"), ("If US inflation was forecast at 3.0% and comes out at 3.4%, the dollar often jumps — not because 3.4% is high, but because it was not expected.",
                                                                                                         "اگر تورم امریکا ۳٫۰٪ پیش‌بینی شده باشد و ۳٫۴٪ اعلام شود، دلار اغلب جهش می‌کند — نه به این دلیل که ۳٫۴٪ زیاد است، بلکه چون انتظارش نمی‌رفت.")),
        ]),
        (("The events every trader should know", "رویدادهایی که هر معامله‌گر باید بشناسد"), [
            ("ul", [("Interest rate decisions (US Fed, ECB, Bank of England…) — the most important events of all. Higher rates usually strengthen a currency.", "تصمیم‌های نرخ بهره (فدرال رزرو امریکا، بانک مرکزی اروپا، بانک انگلستان…) — مهم‌ترین رویدادها. نرخ بهرهٔ بالاتر معمولاً ارز را تقویت می‌کند."),
                    ("Inflation (CPI) — central banks watch it to decide interest rates.", "تورم (CPI) — بانک‌های مرکزی برای تصمیم‌گیری دربارهٔ نرخ بهره آن را زیر نظر دارند."),
                    ("US jobs report (Non-Farm Payrolls, NFP) — usually the first Friday of the month, around 17:00–18:00 Kabul time.", "گزارش اشتغال امریکا (NFP) — معمولاً اولین جمعهٔ ماه، حدود ساعت ۱۷:۰۰ تا ۱۸:۰۰ به وقت کابل."),
                    ("GDP, retail sales and PMI — how fast an economy is growing.", "تولید ناخالص داخلی (GDP)، خرده‌فروشی و PMI — سرعت رشد اقتصاد."),
                    ("Central bank speeches — a few words can move markets as much as the data.", "سخنرانی رؤسای بانک‌های مرکزی — چند کلمه می‌تواند به اندازهٔ داده‌ها بازار را حرکت دهد.")]),
        ]),
        (("A simple weekly routine", "یک روال سادهٔ هفتگی"), [
            ("ol", [("Sunday or Monday: open the calendar, filter to high impact, and note this week's big events for the pairs you trade.", "یکشنبه یا دوشنبه: تقویم را باز کنید، روی «اهمیت زیاد» فیلتر کنید و رویدادهای بزرگ این هفته را برای جفت‌ارزهای خود یادداشت کنید."),
                    ("Before every trade: check whether high-impact news is due in the next hour or two.", "پیش از هر معامله: بررسی کنید که آیا در یکی دو ساعت آینده خبر پراهمیتی در راه است."),
                    ("If it is, wait — or reduce your position size. Don't open a new trade just minutes before the release.", "اگر هست، صبر کنید — یا حجم معامله را کم کنید. چند دقیقه پیش از انتشار خبر معاملهٔ جدید باز نکنید."),
                    ("After the release: let the first wild minutes pass, then look for your normal setups.", "پس از انتشار: بگذارید دقایق پرنوسان اول بگذرد، سپس دنبال موقعیت‌های معمول خود باشید.")]),
            ("warn", None, ("During big news, spreads can widen several times over and price can jump past your stop-loss (slippage). Trading the news itself is for experienced traders only.",
                            "در زمان اخبار مهم، اسپرد می‌تواند چند برابر شود و قیمت ممکن است از روی حد ضرر شما بپرد (اسلیپیج). معامله روی خودِ خبر فقط برای معامله‌گران باتجربه است.")),
            ("tip", ("Go deeper", "عمیق‌تر شوید"), ("Our Advanced students analyse the week's key events together in the Weekly Economic News Analysis session — see Services.",
                                                   "شاگردان دورهٔ پیشرفتهٔ ما رویدادهای مهم هر هفته را در جلسهٔ «تحلیل هفتگی اخبار اقتصادی» با هم بررسی می‌کنند — بخش خدمات را ببینید.")),
        ]),
    ],
    tool=("/economic-calendar.html", ("Economic Calendar", "تقویم اقتصادی"), ("This week's events, with impact level, forecast and actual numbers.", "رویدادهای این هفته، با سطح اهمیت، پیش‌بینی و اعداد واقعی.")),
),
]
