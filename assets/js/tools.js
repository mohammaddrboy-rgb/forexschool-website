/* مکتب فارکس — Forex School | trading tools (pip value, margin & leverage, market hours).
   Loaded only on the tool pages. Vanilla JS, no dependencies. Account currency: USD. */
(function () {
  'use strict';

  var root = document.documentElement;
  var isFa = function () { return root.lang === 'fa'; };
  var $ = function (id) { return document.getElementById(id); };
  var FA = '۰۱۲۳۴۵۶۷۸۹';
  var faDigits = function (s) { return String(s).replace(/\d/g, function (d) { return FA[d]; }); };
  var num = function (el) { var v = parseFloat(String(el.value).replace(',', '.')); return isFinite(v) ? v : NaN; };
  var money = function (n, d) {
    if (!isFinite(n)) return '—';
    d = d == null ? 2 : d;
    return '$' + n.toLocaleString('en-US', { minimumFractionDigits: d, maximumFractionDigits: d });
  };
  function show(el, text) {
    if (!el || el.textContent === text) return;
    el.textContent = text;
    el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
  }

  /* ---------- Currency pairs ---------- */
  // p = an example price only (the user should type today's price)
  var PAIRS = {
    EURUSD: { b: 'EUR', q: 'USD', p: 1.08 }, GBPUSD: { b: 'GBP', q: 'USD', p: 1.27 },
    AUDUSD: { b: 'AUD', q: 'USD', p: 0.66 }, NZDUSD: { b: 'NZD', q: 'USD', p: 0.60 },
    USDJPY: { b: 'USD', q: 'JPY', p: 150 },  USDCHF: { b: 'USD', q: 'CHF', p: 0.88 },
    USDCAD: { b: 'USD', q: 'CAD', p: 1.36 }, EURGBP: { b: 'EUR', q: 'GBP', p: 0.85 },
    EURJPY: { b: 'EUR', q: 'JPY', p: 162 },  GBPJPY: { b: 'GBP', q: 'JPY', p: 190 }
  };
  // For cross pairs we need the quote currency's rate against USD.
  // USD-first currencies are quoted as USD/XXX, the rest as XXX/USD.
  var USD_FIRST = { JPY: 150, CHF: 0.88, CAD: 1.36 };
  var USD_SECOND = { GBP: 1.27, EUR: 1.08, AUD: 0.66, NZD: 0.60 };

  function crossInfo(pair) {
    var q = PAIRS[pair].q;
    if (pair.indexOf('USD') !== -1) return null;
    return q in USD_FIRST ? { label: 'USD/' + q, def: USD_FIRST[q], usdFirst: true }
                          : { label: q + '/USD', def: USD_SECOND[q], usdFirst: false };
  }
  // value in USD of 1 unit of the quote currency
  function quoteToUSD(pair, price, xrate) {
    var d = PAIRS[pair];
    if (d.q === 'USD') return 1;
    if (d.b === 'USD') return 1 / price;
    var c = crossInfo(pair);
    return c.usdFirst ? 1 / xrate : xrate;
  }
  // value in USD of 1 unit of the base currency
  function baseToUSD(pair, price, xrate) {
    var d = PAIRS[pair];
    if (d.b === 'USD') return 1;
    return price * quoteToUSD(pair, price, xrate);
  }
  var pipSize = function (pair) { return PAIRS[pair].q === 'JPY' ? 0.01 : 0.0001; };

  // Shared wiring: pair select drives the example price and the cross-rate field
  function wirePair(prefix, recalc) {
    var sel = $(prefix + '-pair'), price = $(prefix + '-price'), xf = $(prefix + '-xfield'), x = $(prefix + '-xrate');
    function onPair() {
      var pair = sel.value, c = crossInfo(pair);
      price.value = PAIRS[pair].p;
      if (c) {
        xf.hidden = false;
        x.value = c.def;
        xf.querySelectorAll('.x-pair').forEach(function (s) { s.textContent = c.label; });
      } else {
        xf.hidden = true;
      }
      recalc();
    }
    sel.addEventListener('change', onPair);
    onPair();
  }

  /* ---------- Pip value calculator ---------- */
  if ($('pip-pair')) {
    var pipCalc = function () {
      var pair = $('pip-pair').value, lots = num($('pip-lots')), price = num($('pip-price')), x = num($('pip-xrate'));
      var size = pipSize(pair);
      var perLot = 100000 * size * quoteToUSD(pair, price, x);
      var perPip = perLot * lots;
      var ok = lots > 0 && price > 0 && (!crossInfo(pair) || x > 0);
      show($('pip-out-value'), ok ? money(perPip, perPip < 1 ? 3 : 2) : '—');
      show($('pip-out-10'), ok ? money(perPip * 10) : '—');
      show($('pip-out-50'), ok ? money(perPip * 50) : '—');
      show($('pip-out-lot'), ok ? money(perLot) : '—');
      show($('pip-out-size'), String(size));
    };
    ['pip-lots', 'pip-price', 'pip-xrate'].forEach(function (id) { $(id).addEventListener('input', pipCalc); });
    wirePair('pip', pipCalc);
  }

  /* ---------- Margin & leverage calculator ---------- */
  if ($('mg-pair')) {
    var msgs = {
      ok:   { en: 'Low effective leverage — the account can absorb normal market moves.', fa: 'اهرم مؤثر پایین — حساب می‌تواند نوسانات عادی بازار را تحمل کند.' },
      warn: { en: 'High effective leverage — a small move against you will hurt the account.', fa: 'اهرم مؤثر بالا — یک حرکت کوچک خلاف شما به حساب آسیب می‌زند.' },
      bad:  { en: 'Dangerous — a normal daily move could wipe out a large part of the account.', fa: 'خطرناک — یک نوسان عادی روزانه می‌تواند بخش بزرگی از حساب را از بین ببرد.' }
    };
    var mgCalc = function () {
      var pair = $('mg-pair').value, lots = num($('mg-lots')), price = num($('mg-price')),
          x = num($('mg-xrate')), lev = num($('mg-lev')), bal = num($('mg-balance'));
      var ok = lots > 0 && price > 0 && lev > 0 && bal > 0 && (!crossInfo(pair) || x > 0);
      var notional = 100000 * lots * baseToUSD(pair, price, x);
      var margin = notional / lev;
      var marginPct = margin / bal * 100;
      var move1 = notional * 0.01;
      var eff = notional / bal;
      show($('mg-out-notional'), ok ? money(notional, 0) : '—');
      show($('mg-out-margin'), ok ? money(margin) : '—');
      show($('mg-out-pct'), ok ? marginPct.toFixed(1) + '%' : '—');
      show($('mg-out-eff'), ok ? eff.toFixed(1) + 'x' : '—');
      show($('mg-out-move'), ok ? money(move1) + ' (' + (move1 / bal * 100).toFixed(1) + '%)' : '—');
      var v = $('mg-verdict');
      if (!ok) { v.className = 'demo-verdict'; v.textContent = ''; return; }
      var k = eff <= 5 ? 'ok' : (eff <= 10 ? 'warn' : 'bad');
      v.className = 'demo-verdict ' + k;
      v.textContent = msgs[k][isFa() ? 'fa' : 'en'];
      var bar = $('mg-bar');
      if (bar) { bar.style.setProperty('--w', Math.min(100, eff / 20 * 100) + '%'); bar.className = 'lev-bar ' + k; }
    };
    ['mg-lots', 'mg-price', 'mg-xrate', 'mg-lev', 'mg-balance'].forEach(function (id) {
      $(id).addEventListener('input', mgCalc); $(id).addEventListener('change', mgCalc);
    });
    wirePair('mg', mgCalc);
  }

  /* ---------- Market hours (shown in Kabul time) ---------- */
  var mh = $('mh-app');
  if (mh && window.Intl) {
    var KABUL = 'Asia/Kabul';
    var SESSIONS = [
      { id: 'sydney',  tz: 'Australia/Sydney',  o: 7, c: 16, en: 'Sydney',   fa: 'سیدنی' },
      { id: 'tokyo',   tz: 'Asia/Tokyo',        o: 9, c: 18, en: 'Tokyo',    fa: 'توکیو' },
      { id: 'london',  tz: 'Europe/London',     o: 8, c: 17, en: 'London',   fa: 'لندن' },
      { id: 'newyork', tz: 'America/New_York',  o: 8, c: 17, en: 'New York', fa: 'نیویورک' }
    ];
    var fmtCache = {};
    function partsIn(tz, t) {
      var f = fmtCache[tz] || (fmtCache[tz] = new Intl.DateTimeFormat('en-US', {
        timeZone: tz, hourCycle: 'h23', year: 'numeric', month: 'numeric', day: 'numeric',
        hour: 'numeric', minute: 'numeric', second: 'numeric', weekday: 'short' }));
      var o = {};
      f.formatToParts(new Date(t)).forEach(function (p) { o[p.type] = p.value; });
      return { y: +o.year, m: +o.month - 1, d: +o.day, h: +o.hour % 24, mi: +o.minute, s: +o.second, wd: o.weekday };
    }
    function offsetMin(tz, t) {
      var p = partsIn(tz, t);
      return Math.round((Date.UTC(p.y, p.m, p.d, p.h, p.mi, p.s) - Math.floor(t / 1000) * 1000) / 60000);
    }
    function zonedToUTC(tz, y, m, d, h) {
      var guess = Date.UTC(y, m, d, h, 0, 0);
      var t = guess - offsetMin(tz, guess) * 60000;
      var t2 = guess - offsetMin(tz, t) * 60000;
      return t2;
    }
    // Session occurrences around time t (yesterday, today, tomorrow in the city's own calendar), weekdays only
    function occurrences(s, t) {
      var p = partsIn(s.tz, t), out = [];
      for (var k = -1; k <= 1; k++) {
        var day = new Date(Date.UTC(p.y, p.m, p.d + k));
        var wd = day.getUTCDay();
        if (wd === 0 || wd === 6) continue;
        var open = zonedToUTC(s.tz, day.getUTCFullYear(), day.getUTCMonth(), day.getUTCDate(), s.o);
        out.push({ open: open, close: open + (s.c - s.o) * 3600000 });
      }
      return out;
    }
    // Forex week: Sunday 17:00 to Friday 17:00 New York time
    function marketOpen(t) {
      var p = partsIn('America/New_York', t);
      var wd = new Date(Date.UTC(p.y, p.m, p.d)).getUTCDay();
      if (wd === 6) return false;
      if (wd === 5) return p.h < 17;
      if (wd === 0) return p.h >= 17;
      return true;
    }
    function nextMarketOpen(t) {
      var p = partsIn('America/New_York', t);
      var d = new Date(Date.UTC(p.y, p.m, p.d));
      while (d.getUTCDay() !== 0) d.setUTCDate(d.getUTCDate() + 1);
      return zonedToUTC('America/New_York', d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate(), 17);
    }
    var pad = function (n) { return (n < 10 ? '0' : '') + n; };
    function hhmm(tz, t) { var p = partsIn(tz, t); return pad(p.h) + ':' + pad(p.mi); }
    function dur(ms) {
      var m = Math.max(0, Math.round(ms / 60000)), h = Math.floor(m / 60); m = m % 60;
      if (isFa()) return h ? faDigits(h) + ' ساعت' + (m ? ' و ' + faDigits(m) + ' دقیقه' : '') : faDigits(m) + ' دقیقه';
      return h ? h + 'h' + (m ? ' ' + m + 'm' : '') : m + 'm';
    }
    var L = function (en, fa) { return isFa() ? fa : en; };
    var loc = function (s) { return isFa() ? faDigits(s) : s; };

    var clockEl = $('mh-clock'), dateEl = $('mh-date'), statusEl = $('mh-status'), youEl = $('mh-you');
    var cards = {}, bars = $('mh-bars'), nowLine = $('mh-now');
    SESSIONS.forEach(function (s) { cards[s.id] = mh.querySelector('[data-session="' + s.id + '"]'); });
    var userTz = (Intl.DateTimeFormat().resolvedOptions().timeZone) || KABUL;

    function render() {
      var now = Date.now();
      var kp = partsIn(KABUL, now);
      clockEl.textContent = loc(pad(kp.h) + ':' + pad(kp.mi) + ':' + pad(kp.s));
      dateEl.textContent = new Intl.DateTimeFormat(isFa() ? 'fa-AF' : 'en-GB', { timeZone: KABUL, weekday: 'long', day: 'numeric', month: 'long' }).format(new Date(now));
      if (youEl) {
        var sameAsKabul = offsetMin(userTz, now) === offsetMin(KABUL, now);
        youEl.hidden = sameAsKabul;
        if (!sameAsKabul) youEl.textContent = L('Your time: ', 'وقت شما: ') + loc(hhmm(userTz, now));
      }
      var open = marketOpen(now);
      statusEl.className = 'mh-status ' + (open ? 'is-open' : 'is-closed');
      statusEl.textContent = open ? L('The forex market is open', 'بازار فارکس باز است')
                                  : L('Closed for the weekend — opens in ', 'تعطیل آخر هفته — تا باز شدن: ') + dur(nextMarketOpen(now) - now);

      var kabulMidnight = zonedToUTC(KABUL, kp.y, kp.m, kp.d, 0);
      var dayLen = 24 * 3600000;
      var segsHtml = '';
      var spans = {};
      SESSIONS.forEach(function (s, i) {
        var occ = occurrences(s, now);
        var cur = null, next = null;
        occ.forEach(function (o) {
          if (now >= o.open && now < o.close) cur = o;
          else if (o.open > now && (!next || o.open < next.open)) next = o;
        });
        var card = cards[s.id];
        if (card) {
          var ref = cur || next || occ[occ.length - 1];
          card.querySelector('.ses-hours').textContent = ref ? loc(hhmm(KABUL, ref.open) + ' – ' + hhmm(KABUL, ref.close)) : '—';
          card.classList.toggle('is-open', !!cur && open);
          var st = card.querySelector('.ses-state');
          if (cur && open) st.textContent = L('Open · closes in ', 'باز · تا بسته شدن: ') + dur(cur.close - now);
          else if (next) st.textContent = L('Closed · opens in ', 'بسته · تا باز شدن: ') + dur(next.open - now);
          else st.textContent = L('Closed', 'بسته');
          var prog = card.querySelector('.ses-progress');
          if (prog) prog.style.setProperty('--p', cur && open ? ((now - cur.open) / (cur.close - cur.open) * 100) + '%' : '0%');
        }
        // timeline segments for the current Kabul day
        spans[s.id] = [];
        occ.forEach(function (o) {
          var a = Math.max(0, (o.open - kabulMidnight) / dayLen), b = Math.min(1, (o.close - kabulMidnight) / dayLen);
          if (b > a) {
            spans[s.id].push([a, b]);
            segsHtml += '<span class="tl-seg tl-' + s.id + '" style="--row:' + i + ';--a:' + (a * 100) + '%;--b:' + (b * 100) + '%"></span>';
          }
        });
      });
      // London + New York overlap
      (spans.london || []).forEach(function (l) {
        (spans.newyork || []).forEach(function (n) {
          var a = Math.max(l[0], n[0]), b = Math.min(l[1], n[1]);
          if (b > a) segsHtml += '<span class="tl-overlap" style="--a:' + (a * 100) + '%;--b:' + (b * 100) + '%"></span>';
        });
      });
      if (bars.getAttribute('data-html') !== segsHtml) { bars.innerHTML = segsHtml; bars.setAttribute('data-html', segsHtml); }
      nowLine.style.setProperty('--x', ((now - kabulMidnight) / dayLen * 100) + '%');
    }
    render();
    setInterval(render, 1000);
    mh.classList.add('is-live');
  }
})();
