# -*- coding: utf-8 -*-
"""ARCHIVE (October 2026) — the first 8 broker profiles, taken off the live site on 2026-10-29 at the
owner's request. NOT used by build-brokers.py. To reuse a broker, copy its dict(...) into
BROKERS in brokers.py (and add register_url if the owner gives one).

Originally: broker profiles for brokers.html (built by build-brokers.py). Text pairs are (English, Dari).

Facts are from the brokers' public information as of October 2026 and are written as
"from / about / up to" on purpose: brokers change conditions often, and the entity a
client is opened under (and therefore leverage, protection and payment methods) depends
on the client's country. Update CHECKED when you re-verify.
"""

CHECKED = ("October 2026", "اکتوبر ۲۰۲۶")

# Regulation tiers used for the coloured badge on each broker.
TIERS = {
    "t1": ("Top-tier regulated", "نظارت سطح یک"),
    "mix": ("Top-tier + offshore", "نظارت سطح یک + آفشور"),
    "off": ("Offshore regulation only", "فقط نظارت آفشور"),
}

BROKERS = [
dict(
    id="exness", name="Exness", url="https://www.exness.com", color="#FFDE02", ink="#1A1A1A", tier="mix",
    tagline=("Very low minimum deposit and fast, often instant, withdrawals.", "حداقل واریز بسیار کم و برداشت سریع، اغلب فوری."),
    chips=[("From $10", "از ۱۰ دلار"), ("MT4 · MT5", "MT4 · MT5")],
    clusters=[
        (("Company & regulation", "شرکت و نظارت"), "shield", [
            (("Founded", "تأسیس"), ("2008", "۲۰۰۸")),
            (("Headquarters", "مقر اصلی"), ("Limassol, Cyprus", "لیماسول، قبرس")),
            (("Regulators", "نهادهای ناظر"), ("CySEC (EU), FCA (UK), FSCA (South Africa), FSA (Seychelles), FSC (Mauritius) and others", "CySEC (اروپا)، FCA (بریتانیا)، FSCA (افریقای جنوبی)، FSA (سیشل)، FSC (موریس) و دیگران")),
        ]),
        (("Accounts & costs", "حساب‌ها و هزینه‌ها"), "coins", [
            (("Minimum deposit", "حداقل واریز"), ("From about $10 (Standard); higher for Raw Spread / Zero / Pro", "از حدود ۱۰ دلار (Standard)؛ برای Raw Spread / Zero / Pro بیشتر")),
            (("EUR/USD cost", "هزینهٔ EUR/USD"), ("Standard: about 1 pip, no commission · Raw/Zero: from 0.0 pips + commission", "Standard: حدود ۱ پیپ، بدون کمیسیون · Raw/Zero: از ۰٫۰ پیپ + کمیسیون")),
            (("Maximum leverage", "حداکثر لیوریج"), ("Very high on offshore accounts (conditions apply); much lower in the EU/UK", "در حساب‌های آفشور بسیار بالا (با شرایط)؛ در اروپا/بریتانیا بسیار کمتر")),
            (("Swap-free (Islamic) account", "حساب بدون سواپ (اسلامی)"), ("Yes — automatic for many Muslim-majority countries", "بله — برای بسیاری از کشورهای مسلمان‌نشین به‌صورت خودکار")),
        ]),
        (("Platforms", "پلتفرم‌ها"), "screen", [
            (("Trading platforms", "پلتفرم معاملاتی"), ("MetaTrader 4, MetaTrader 5, Exness Terminal (web), Exness Trade app", "متاتریدر ۴، متاتریدر ۵، Exness Terminal (وب)، اپ Exness Trade")),
            (("Demo account", "حساب دمو"), ("Yes, free", "بله، رایگان")),
        ]),
        (("Deposits & withdrawals", "واریز و برداشت"), "wallet", [
            (("Methods", "روش‌ها"), ("Bank cards, e-wallets, local payment options and crypto (e.g. USDT) — depends on your country", "کارت بانکی، کیف پول الکترونیکی، روش‌های پرداخت محلی و رمزارز (مثلاً USDT) — بسته به کشور شما")),
            (("Speed", "سرعت"), ("Many withdrawals are processed automatically within minutes", "بسیاری از برداشت‌ها در چند دقیقه به‌صورت خودکار انجام می‌شوند")),
        ]),
    ],
    pros=[("Start with a very small amount", "شروع با مبلغ بسیار کم"), ("Fast withdrawals, including crypto", "برداشت سریع، از جمله با رمزارز"), ("Swap-free accounts widely available", "حساب بدون سواپ به‌طور گسترده")],
    cons=[("Very high leverage is tempting — dangerous for beginners", "لیوریج بسیار بالا وسوسه‌انگیز است — برای مبتدیان خطرناک"), ("Non-EU clients are usually opened under an offshore entity", "مشتریان غیراروپایی معمولاً زیر نهاد آفشور ثبت می‌شوند")],
    best=("Beginners who want to start small and value fast withdrawals.", "تازه‌کارانی که می‌خواهند با مبلغ کم شروع کنند و برداشت سریع برایشان مهم است."),
),
dict(
    id="xm", name="XM", url="https://www.xm.com", color="#E02020", ink="#FFFFFF", tier="mix",
    tagline=("A well-known global broker with micro accounts and lots of free education.", "بروکر شناخته‌شدهٔ جهانی با حساب میکرو و آموزش رایگان فراوان."),
    chips=[("From $5", "از ۵ دلار"), ("MT4 · MT5", "MT4 · MT5")],
    clusters=[
        (("Company & regulation", "شرکت و نظارت"), "shield", [
            (("Founded", "تأسیس"), ("2009 (Trading Point group)", "۲۰۰۹ (گروه Trading Point)")),
            (("Headquarters", "مقر اصلی"), ("Limassol, Cyprus", "لیماسول، قبرس")),
            (("Regulators", "نهادهای ناظر"), ("CySEC (EU), ASIC (Australia), DFSA (Dubai), FSCA (South Africa), FSC (Belize)", "CySEC (اروپا)، ASIC (آسترالیا)، DFSA (دبی)، FSCA (افریقای جنوبی)، FSC (بلیز)")),
        ]),
        (("Accounts & costs", "حساب‌ها و هزینه‌ها"), "coins", [
            (("Minimum deposit", "حداقل واریز"), ("From about $5", "از حدود ۵ دلار")),
            (("Account types", "انواع حساب"), ("Micro, Standard, Ultra Low, Shares", "Micro، Standard، Ultra Low، Shares")),
            (("EUR/USD cost", "هزینهٔ EUR/USD"), ("Standard: about 1.6 pips · Ultra Low: from about 0.6 pips, no commission", "Standard: حدود ۱٫۶ پیپ · Ultra Low: از حدود ۰٫۶ پیپ، بدون کمیسیون")),
            (("Maximum leverage", "حداکثر لیوریج"), ("Up to 1:1000 on the international entity; lower elsewhere", "تا ۱:۱۰۰۰ در نهاد بین‌المللی؛ در جاهای دیگر کمتر")),
            (("Swap-free (Islamic) account", "حساب بدون سواپ (اسلامی)"), ("Yes, on request", "بله، با درخواست")),
        ]),
        (("Platforms", "پلتفرم‌ها"), "screen", [
            (("Trading platforms", "پلتفرم معاملاتی"), ("MetaTrader 4, MetaTrader 5, XM app", "متاتریدر ۴، متاتریدر ۵، اپ XM")),
            (("Demo account", "حساب دمو"), ("Yes, free", "بله، رایگان")),
        ]),
        (("Deposits & withdrawals", "واریز و برداشت"), "wallet", [
            (("Methods", "روش‌ها"), ("Bank cards, bank transfer, e-wallets and local options — depends on your country", "کارت بانکی، انتقال بانکی، کیف پول الکترونیکی و روش‌های محلی — بسته به کشور شما")),
            (("Speed", "سرعت"), ("E-wallets usually within a day; bank transfers take longer", "کیف پول الکترونیکی معمولاً تا یک روز؛ انتقال بانکی بیشتر طول می‌کشد")),
        ]),
    ],
    pros=[("Micro account — trade very small sizes", "حساب میکرو — معامله با حجم بسیار کوچک"), ("Lots of free webinars and education", "وبینار و آموزش رایگان فراوان"), ("Long track record", "سابقهٔ طولانی")],
    cons=[("Standard account spreads are higher than raw-spread brokers", "اسپرد حساب Standard از بروکرهای Raw Spread بیشتر است"), ("Deposit bonuses on offshore accounts come with conditions — read them", "بونوس واریز در حساب‌های آفشور شرط دارد — آن را بخوانید")],
    best=("New traders who want tiny position sizes and education.", "معامله‌گران تازه‌کاری که حجم بسیار کوچک و آموزش می‌خواهند."),
),
dict(
    id="icmarkets", name="IC Markets", url="https://www.icmarkets.com", color="#0B2E5B", ink="#FFFFFF", tier="mix",
    tagline=("A favourite of active traders for very tight raw spreads.", "محبوب معامله‌گران فعال به خاطر اسپرد خام بسیار پایین."),
    chips=[("From $200", "از ۲۰۰ دلار"), ("MT4 · MT5 · cTrader", "MT4 · MT5 · cTrader")],
    clusters=[
        (("Company & regulation", "شرکت و نظارت"), "shield", [
            (("Founded", "تأسیس"), ("2007", "۲۰۰۷")),
            (("Headquarters", "مقر اصلی"), ("Sydney, Australia", "سیدنی، آسترالیا")),
            (("Regulators", "نهادهای ناظر"), ("ASIC (Australia), CySEC (EU), FSA (Seychelles), SCB (Bahamas)", "ASIC (آسترالیا)، CySEC (اروپا)، FSA (سیشل)، SCB (باهاما)")),
        ]),
        (("Accounts & costs", "حساب‌ها و هزینه‌ها"), "coins", [
            (("Minimum deposit", "حداقل واریز"), ("About $200", "حدود ۲۰۰ دلار")),
            (("EUR/USD cost", "هزینهٔ EUR/USD"), ("Raw: from 0.0 pips + about $7 commission per lot round-turn · Standard: from about 0.8 pips", "Raw: از ۰٫۰ پیپ + حدود ۷ دلار کمیسیون برای هر لات (رفت و برگشت) · Standard: از حدود ۰٫۸ پیپ")),
            (("Maximum leverage", "حداکثر لیوریج"), ("Up to 1:500 or more on the offshore entity; 1:30 in Australia/EU", "تا ۱:۵۰۰ یا بیشتر در نهاد آفشور؛ ۱:۳۰ در آسترالیا/اروپا")),
            (("Swap-free (Islamic) account", "حساب بدون سواپ (اسلامی)"), ("Yes, on request", "بله، با درخواست")),
        ]),
        (("Platforms", "پلتفرم‌ها"), "screen", [
            (("Trading platforms", "پلتفرم معاملاتی"), ("MetaTrader 4, MetaTrader 5, cTrader, TradingView", "متاتریدر ۴، متاتریدر ۵، cTrader، TradingView")),
            (("Demo account", "حساب دمو"), ("Yes, free", "بله، رایگان")),
        ]),
        (("Deposits & withdrawals", "واریز و برداشت"), "wallet", [
            (("Methods", "روش‌ها"), ("Bank cards, bank transfer and e-wallets — depends on your country", "کارت بانکی، انتقال بانکی و کیف پول الکترونیکی — بسته به کشور شما")),
            (("Fees", "کارمزد"), ("Usually no broker fee; bank fees may apply", "معمولاً بدون کارمزد بروکر؛ ممکن است بانک کارمزد بگیرد")),
        ]),
    ],
    pros=[("Very low trading costs on Raw accounts", "هزینهٔ معامله بسیار پایین در حساب Raw"), ("Choice of MT4, MT5, cTrader and TradingView", "انتخاب میان MT4، MT5، cTrader و TradingView"), ("Fast order execution", "اجرای سریع سفارش")],
    cons=[("Higher minimum deposit than some others", "حداقل واریز بیشتر از برخی دیگر"), ("Built for active traders — less beginner education", "برای معامله‌گران فعال ساخته شده — آموزش مبتدی کمتر")],
    best=("Traders with a tested plan who care most about low costs.", "معامله‌گرانی با پلان آزموده که هزینهٔ کم برایشان مهم‌ترین است."),
),
dict(
    id="pepperstone", name="Pepperstone", url="https://pepperstone.com", color="#0B1F3A", ink="#4BD3FF", tier="t1",
    tagline=("Strongly regulated, with low costs and excellent platforms.", "نظارت قوی، هزینهٔ کم و پلتفرم‌های عالی."),
    chips=[("No minimum", "بدون حداقل"), ("MT4 · MT5 · cTrader · TV", "MT4 · MT5 · cTrader · TV")],
    clusters=[
        (("Company & regulation", "شرکت و نظارت"), "shield", [
            (("Founded", "تأسیس"), ("2010", "۲۰۱۰")),
            (("Headquarters", "مقر اصلی"), ("Melbourne, Australia", "ملبورن، آسترالیا")),
            (("Regulators", "نهادهای ناظر"), ("ASIC (Australia), FCA (UK), CySEC (EU), BaFin (Germany), DFSA (Dubai), CMA (Kenya), SCB (Bahamas)", "ASIC (آسترالیا)، FCA (بریتانیا)، CySEC (اروپا)، BaFin (آلمان)، DFSA (دبی)، CMA (کنیا)، SCB (باهاما)")),
        ]),
        (("Accounts & costs", "حساب‌ها و هزینه‌ها"), "coins", [
            (("Minimum deposit", "حداقل واریز"), ("No fixed minimum (about $200 is a sensible start)", "حداقل ثابت ندارد (حدود ۲۰۰ دلار شروع منطقی است)")),
            (("EUR/USD cost", "هزینهٔ EUR/USD"), ("Razor: from 0.0 pips + commission · Standard: from about 1 pip", "Razor: از ۰٫۰ پیپ + کمیسیون · Standard: از حدود ۱ پیپ")),
            (("Maximum leverage", "حداکثر لیوریج"), ("Up to about 1:200–1:500 depending on the entity; 1:30 in the UK/EU/Australia", "بسته به نهاد تا حدود ۱:۲۰۰ تا ۱:۵۰۰؛ ۱:۳۰ در بریتانیا/اروپا/آسترالیا")),
            (("Swap-free (Islamic) account", "حساب بدون سواپ (اسلامی)"), ("Yes, for eligible clients", "بله، برای مشتریان واجد شرایط")),
        ]),
        (("Platforms", "پلتفرم‌ها"), "screen", [
            (("Trading platforms", "پلتفرم معاملاتی"), ("MetaTrader 4, MetaTrader 5, cTrader, TradingView, Pepperstone app", "متاتریدر ۴، متاتریدر ۵، cTrader، TradingView، اپ Pepperstone")),
            (("Demo account", "حساب دمو"), ("Yes, free", "بله، رایگان")),
        ]),
        (("Deposits & withdrawals", "واریز و برداشت"), "wallet", [
            (("Methods", "روش‌ها"), ("Bank cards, bank transfer and e-wallets — depends on your country", "کارت بانکی، انتقال بانکی و کیف پول الکترونیکی — بسته به کشور شما")),
            (("Fees", "کارمزد"), ("Usually no broker fee; bank fees may apply", "معمولاً بدون کارمزد بروکر؛ ممکن است بانک کارمزد بگیرد")),
        ]),
    ],
    pros=[("Among the most strongly regulated brokers", "از بروکرهای دارای قوی‌ترین نظارت"), ("Low costs and great TradingView integration", "هزینهٔ کم و اتصال عالی به TradingView"), ("Highly rated customer service", "پشتیبانی بسیار خوب")],
    cons=[("Account opening can be stricter (more documents)", "افتتاح حساب ممکن است سخت‌گیرانه‌تر باشد (مدارک بیشتر)"), ("Not every country is accepted", "همهٔ کشورها پذیرفته نمی‌شوند")],
    best=("Traders who put safety of funds and quality first.", "معامله‌گرانی که امنیت سرمایه و کیفیت را در اولویت می‌گذارند."),
),
dict(
    id="tickmill", name="Tickmill", url="https://www.tickmill.com", color="#0E2A47", ink="#26C2E6", tier="mix",
    tagline=("Low commissions and a clean, no-nonsense offering.", "کمیسیون پایین و خدمات ساده و بی‌حاشیه."),
    chips=[("From $100", "از ۱۰۰ دلار"), ("MT4 · MT5", "MT4 · MT5")],
    clusters=[
        (("Company & regulation", "شرکت و نظارت"), "shield", [
            (("Founded", "تأسیس"), ("2014", "۲۰۱۴")),
            (("Headquarters", "مقر اصلی"), ("London, UK", "لندن، بریتانیا")),
            (("Regulators", "نهادهای ناظر"), ("FCA (UK), CySEC (EU), FSCA (South Africa), DFSA (Dubai), FSA (Seychelles), Labuan FSA (Malaysia)", "FCA (بریتانیا)، CySEC (اروپا)، FSCA (افریقای جنوبی)، DFSA (دبی)، FSA (سیشل)، Labuan FSA (مالزی)")),
        ]),
        (("Accounts & costs", "حساب‌ها و هزینه‌ها"), "coins", [
            (("Minimum deposit", "حداقل واریز"), ("About $100", "حدود ۱۰۰ دلار")),
            (("EUR/USD cost", "هزینهٔ EUR/USD"), ("Raw: from 0.0 pips + about $6 commission per lot round-turn · Classic: from about 1.6 pips", "Raw: از ۰٫۰ پیپ + حدود ۶ دلار کمیسیون برای هر لات (رفت و برگشت) · Classic: از حدود ۱٫۶ پیپ")),
            (("Maximum leverage", "حداکثر لیوریج"), ("Up to about 1:500 or more on the offshore entity; 1:30 in the UK/EU", "تا حدود ۱:۵۰۰ یا بیشتر در نهاد آفشور؛ ۱:۳۰ در بریتانیا/اروپا")),
            (("Swap-free (Islamic) account", "حساب بدون سواپ (اسلامی)"), ("Yes, on request", "بله، با درخواست")),
        ]),
        (("Platforms", "پلتفرم‌ها"), "screen", [
            (("Trading platforms", "پلتفرم معاملاتی"), ("MetaTrader 4, MetaTrader 5, TradingView, Tickmill app", "متاتریدر ۴، متاتریدر ۵، TradingView، اپ Tickmill")),
            (("Demo account", "حساب دمو"), ("Yes, free", "بله، رایگان")),
        ]),
        (("Deposits & withdrawals", "واریز و برداشت"), "wallet", [
            (("Methods", "روش‌ها"), ("Bank cards, bank transfer, e-wallets and some crypto options — depends on your country", "کارت بانکی، انتقال بانکی، کیف پول الکترونیکی و برخی گزینه‌های رمزارز — بسته به کشور شما")),
            (("Fees", "کارمزد"), ("Usually no broker fee; bank fees may apply", "معمولاً بدون کارمزد بروکر؛ ممکن است بانک کارمزد بگیرد")),
        ]),
    ],
    pros=[("Low commission on Raw accounts", "کمیسیون پایین در حساب Raw"), ("Top-tier regulation in the group", "نظارت سطح یک در گروه"), ("Simple account choice", "انتخاب ساده میان حساب‌ها")],
    cons=[("Fewer instruments than the biggest brokers", "ابزارهای معاملاتی کمتر از بزرگ‌ترین بروکرها"), ("Limited beginner education", "آموزش مبتدی محدود")],
    best=("Cost-conscious traders who want a straightforward broker.", "معامله‌گرانی که به هزینه حساس‌اند و بروکری ساده می‌خواهند."),
),
dict(
    id="avatrade", name="AvaTrade", url="https://www.avatrade.com", color="#1C3B8C", ink="#FFFFFF", tier="t1",
    tagline=("Heavily regulated with fixed-cost pricing and a beginner-friendly app.", "نظارت گسترده، هزینهٔ ثابت و اپ مناسب مبتدیان."),
    chips=[("From $100", "از ۱۰۰ دلار"), ("MT4 · MT5 · AvaTradeGO", "MT4 · MT5 · AvaTradeGO")],
    clusters=[
        (("Company & regulation", "شرکت و نظارت"), "shield", [
            (("Founded", "تأسیس"), ("2006", "۲۰۰۶")),
            (("Headquarters", "مقر اصلی"), ("Dublin, Ireland", "دوبلین، ایرلند")),
            (("Regulators", "نهادهای ناظر"), ("Central Bank of Ireland (EU), ASIC (Australia), FSA (Japan), FSCA (South Africa), ADGM (Abu Dhabi), FSC (BVI)", "بانک مرکزی ایرلند (اروپا)، ASIC (آسترالیا)، FSA (جاپان)، FSCA (افریقای جنوبی)، ADGM (ابوظبی)، FSC (جزایر ویرجین بریتانیا)")),
        ]),
        (("Accounts & costs", "حساب‌ها و هزینه‌ها"), "coins", [
            (("Minimum deposit", "حداقل واریز"), ("About $100", "حدود ۱۰۰ دلار")),
            (("EUR/USD cost", "هزینهٔ EUR/USD"), ("About 0.9 pips, no commission", "حدود ۰٫۹ پیپ، بدون کمیسیون")),
            (("Maximum leverage", "حداکثر لیوریج"), ("Up to about 1:400 on the international entity; lower elsewhere", "تا حدود ۱:۴۰۰ در نهاد بین‌المللی؛ در جاهای دیگر کمتر")),
            (("Swap-free (Islamic) account", "حساب بدون سواپ (اسلامی)"), ("Yes, on request", "بله، با درخواست")),
            (("Watch out", "توجه"), ("An inactivity fee is charged after a few months without trading", "پس از چند ماه بدون معامله، کارمزد عدم فعالیت گرفته می‌شود")),
        ]),
        (("Platforms", "پلتفرم‌ها"), "screen", [
            (("Trading platforms", "پلتفرم معاملاتی"), ("MetaTrader 4, MetaTrader 5, AvaTradeGO app, WebTrader, AvaOptions", "متاتریدر ۴، متاتریدر ۵، اپ AvaTradeGO، WebTrader، AvaOptions")),
            (("Demo account", "حساب دمو"), ("Yes, free", "بله، رایگان")),
        ]),
        (("Deposits & withdrawals", "واریز و برداشت"), "wallet", [
            (("Methods", "روش‌ها"), ("Bank cards, bank transfer and e-wallets — depends on your country", "کارت بانکی، انتقال بانکی و کیف پول الکترونیکی — بسته به کشور شما")),
            (("Speed", "سرعت"), ("Usually 1–3 business days after approval", "معمولاً ۱ تا ۳ روز کاری پس از تأیید")),
        ]),
    ],
    pros=[("Regulated in many top jurisdictions", "دارای مجوز در حوزه‌های قضایی معتبر متعدد"), ("Simple, commission-free pricing", "قیمت‌گذاری ساده و بدون کمیسیون"), ("Easy mobile app for beginners", "اپ موبایل ساده برای مبتدیان")],
    cons=[("Inactivity fee", "کارمزد عدم فعالیت"), ("Costs a little higher than raw-spread brokers", "هزینه کمی بیشتر از بروکرهای Raw Spread")],
    best=("Beginners who want a heavily regulated broker and a simple app.", "تازه‌کارانی که بروکری با نظارت گسترده و اپی ساده می‌خواهند."),
),
dict(
    id="admirals", name="Admirals", url="https://admiralmarkets.com", color="#0C2340", ink="#F5B335", tier="mix",
    tagline=("Long-running European broker with strong MetaTrader tools.", "بروکر قدیمی اروپایی با ابزارهای قوی متاتریدر."),
    chips=[("From about $25", "از حدود ۲۵ دلار"), ("MT4 · MT5", "MT4 · MT5")],
    clusters=[
        (("Company & regulation", "شرکت و نظارت"), "shield", [
            (("Founded", "تأسیس"), ("2001 (formerly Admiral Markets)", "۲۰۰۱ (نام قبلی Admiral Markets)")),
            (("Headquarters", "مقر اصلی"), ("Tallinn, Estonia", "تالین، استونی")),
            (("Regulators", "نهادهای ناظر"), ("FCA (UK), CySEC (EU), ASIC (Australia), FSCA (South Africa), FSA (Seychelles) and others", "FCA (بریتانیا)، CySEC (اروپا)، ASIC (آسترالیا)، FSCA (افریقای جنوبی)، FSA (سیشل) و دیگران")),
        ]),
        (("Accounts & costs", "حساب‌ها و هزینه‌ها"), "coins", [
            (("Minimum deposit", "حداقل واریز"), ("From about $25", "از حدود ۲۵ دلار")),
            (("EUR/USD cost", "هزینهٔ EUR/USD"), ("Trade.MT5: from about 0.6 pips · Zero.MT5: from 0.0 pips + commission", "Trade.MT5: از حدود ۰٫۶ پیپ · Zero.MT5: از ۰٫۰ پیپ + کمیسیون")),
            (("Maximum leverage", "حداکثر لیوریج"), ("Up to about 1:500 or more on the offshore entity; 1:30 in the UK/EU", "تا حدود ۱:۵۰۰ یا بیشتر در نهاد آفشور؛ ۱:۳۰ در بریتانیا/اروپا")),
            (("Swap-free (Islamic) account", "حساب بدون سواپ (اسلامی)"), ("Yes, on request", "بله، با درخواست")),
        ]),
        (("Platforms", "پلتفرم‌ها"), "screen", [
            (("Trading platforms", "پلتفرم معاملاتی"), ("MetaTrader 4, MetaTrader 5 (with the free “Supreme Edition” add-on), Admirals app", "متاتریدر ۴، متاتریدر ۵ (با افزونهٔ رایگان Supreme Edition)، اپ Admirals")),
            (("Demo account", "حساب دمو"), ("Yes, free", "بله، رایگان")),
        ]),
        (("Deposits & withdrawals", "واریز و برداشت"), "wallet", [
            (("Methods", "روش‌ها"), ("Bank cards, bank transfer and e-wallets — depends on your country", "کارت بانکی، انتقال بانکی و کیف پول الکترونیکی — بسته به کشور شما")),
            (("Fees", "کارمزد"), ("Some free withdrawals per month, then a small fee", "چند برداشت رایگان در ماه، سپس کارمزد کم")),
        ]),
    ],
    pros=[("Over 20 years in business", "بیش از ۲۰ سال فعالیت"), ("Useful free MetaTrader add-ons", "افزونه‌های رایگان و مفید متاتریدر"), ("Good educational material", "مطالب آموزشی خوب")],
    cons=[("Limited withdrawals before fees apply", "تعداد برداشت رایگان محدود"), ("Product range differs by entity", "محصولات بسته به نهاد متفاوت است")],
    best=("MetaTrader users who want extra tools and a long track record.", "کاربران متاتریدر که ابزار بیشتر و سابقهٔ طولانی می‌خواهند."),
),
dict(
    id="roboforex", name="RoboForex", url="https://roboforex.com", color="#1F6FEB", ink="#FFFFFF", tier="off",
    tagline=("Very low entry and many platforms — but offshore regulation only.", "ورود با مبلغ بسیار کم و پلتفرم‌های متنوع — اما فقط با نظارت آفشور."),
    chips=[("From $10", "از ۱۰ دلار"), ("MT4 · MT5 · cTrader", "MT4 · MT5 · cTrader")],
    clusters=[
        (("Company & regulation", "شرکت و نظارت"), "shield", [
            (("Founded", "تأسیس"), ("2009", "۲۰۰۹")),
            (("Headquarters", "مقر اصلی"), ("Belize", "بلیز")),
            (("Regulators", "نهادهای ناظر"), ("FSC (Belize) — offshore", "FSC (بلیز) — آفشور")),
        ]),
        (("Accounts & costs", "حساب‌ها و هزینه‌ها"), "coins", [
            (("Minimum deposit", "حداقل واریز"), ("From about $10", "از حدود ۱۰ دلار")),
            (("EUR/USD cost", "هزینهٔ EUR/USD"), ("ECN / Prime: from 0.0 pips + commission · Pro: from about 1.3 pips", "ECN / Prime: از ۰٫۰ پیپ + کمیسیون · Pro: از حدود ۱٫۳ پیپ")),
            (("Maximum leverage", "حداکثر لیوریج"), ("Very high (up to 1:2000) — use with great care", "بسیار بالا (تا ۱:۲۰۰۰) — با احتیاط بسیار")),
            (("Swap-free (Islamic) account", "حساب بدون سواپ (اسلامی)"), ("Yes, on request", "بله، با درخواست")),
        ]),
        (("Platforms", "پلتفرم‌ها"), "screen", [
            (("Trading platforms", "پلتفرم معاملاتی"), ("MetaTrader 4, MetaTrader 5, cTrader, R StocksTrader", "متاتریدر ۴، متاتریدر ۵، cTrader، R StocksTrader")),
            (("Demo account", "حساب دمو"), ("Yes, free", "بله، رایگان")),
        ]),
        (("Deposits & withdrawals", "واریز و برداشت"), "wallet", [
            (("Methods", "روش‌ها"), ("Bank cards, e-wallets, local options and crypto — depends on your country", "کارت بانکی، کیف پول الکترونیکی، روش‌های محلی و رمزارز — بسته به کشور شما")),
            (("Fees", "کارمزد"), ("Varies by method", "بسته به روش متفاوت است")),
        ]),
    ],
    pros=[("Start with a very small amount", "شروع با مبلغ بسیار کم"), ("Many platforms, including cTrader", "پلتفرم‌های متنوع، از جمله cTrader")],
    cons=[("Offshore regulation only — less protection for your money", "فقط نظارت آفشور — حمایت کمتر از سرمایهٔ شما"), ("Extreme leverage is easy to misuse", "لیوریج بسیار بالا به‌آسانی مورد سوءاستفاده قرار می‌گیرد")],
    best=("Experienced traders who understand the extra risk of offshore brokers.", "معامله‌گران باتجربه‌ای که ریسک بیشتر بروکرهای آفشور را می‌فهمند."),
),
]
