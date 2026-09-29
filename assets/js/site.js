/* مکتب فارکس — Forex School | shared site behaviour.
   Core UI works without any library. Motion uses GSAP + ScrollTrigger when they are
   loaded (assets/vendor) and is skipped entirely for prefers-reduced-motion. */
(function () {
  'use strict';

  var root = document.documentElement;
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var gsap = window.gsap;
  var ScrollTrigger = window.ScrollTrigger;
  var canAnimate = !!(gsap && ScrollTrigger && !reduceMotion);
  if (canAnimate) gsap.registerPlugin(ScrollTrigger);
  else root.classList.remove('motion');           // show intro content immediately

  /* ---- Language switch (English primary, Farsi secondary) ---- */
  function applyLang(lang) {
    lang = (lang === 'fa') ? 'fa' : 'en';
    root.lang = lang;
    root.dir = (lang === 'fa') ? 'rtl' : 'ltr';
    var t = root.getAttribute('data-title-' + lang);
    if (t) document.title = t;
    document.querySelectorAll('.lang-toggle .lt-label').forEach(function (el) {
      el.textContent = (lang === 'fa') ? 'EN' : 'فارسی';
    });
    document.querySelectorAll('.lang-toggle').forEach(function (b) {
      b.setAttribute('aria-label', lang === 'fa' ? 'Switch to English' : 'تغییر به فارسی');
    });
    try { localStorage.setItem('mf-lang', lang); } catch (e) {}
    window.dispatchEvent(new Event('resize'));
  }

  // Language is determined by the URL: /fa/… is Farsi, everything else is English.
  var isFa = location.pathname.indexOf('/fa/') !== -1;
  applyLang(isFa ? 'fa' : 'en');

  document.querySelectorAll('.lang-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var p = location.pathname, target;
      if (isFa) target = p.replace('/fa/', '/');
      else target = '/fa' + ((p === '/' || p === '') ? '/index.html' : p);
      window.location.href = target + location.hash;
    });
  });

  var toFaDigits = function (s) { return String(s).replace(/\d/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }); };

  /* ---- Scroll progress bar + sticky nav state ---- */
  var progress = document.createElement('div');
  progress.className = 'scroll-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.appendChild(progress);

  var nav = document.querySelector('.nav');
  function onScroll() {
    var y = window.scrollY;
    if (nav) nav.classList.toggle('scrolled', y > 12);
    var max = document.documentElement.scrollHeight - window.innerHeight;
    progress.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
  }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- Mobile menu ---- */
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  var backdrop = document.querySelector('.nav-backdrop');

  function setMenu(open) {
    if (!links || !toggle) return;
    links.classList.toggle('open', open);
    if (backdrop) backdrop.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.classList.toggle('menu-open', open);
    if (open && canAnimate) {
      gsap.fromTo(links.querySelectorAll('a'), { y: 30, opacity: 0 },
        { y: 0, opacity: 1, duration: 0.6, stagger: 0.05, ease: 'power3.out', delay: 0.12, clearProps: 'transform,opacity' });
    }
  }
  if (toggle && links) {
    toggle.addEventListener('click', function () { setMenu(!links.classList.contains('open')); });
    if (backdrop) backdrop.addEventListener('click', function () { setMenu(false); });
    links.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  }

  /* ---- Accordion ---- */
  document.querySelectorAll('.acc-head').forEach(function (head) {
    head.addEventListener('click', function () {
      var panel = head.nextElementSibling;
      var open = head.getAttribute('aria-expanded') === 'true';
      head.setAttribute('aria-expanded', open ? 'false' : 'true');
      if (panel) panel.style.maxHeight = open ? null : panel.scrollHeight + 'px';
    });
  });

  /* ---- Back to top (footer) ---- */
  document.querySelectorAll('.to-top').forEach(function (b) {
    b.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' }); });
  });

  /* ---- Testimonials: avatar initials + "read more" for long quotes ---- */
  function updateAvatars() {
    var lang = root.lang === 'fa' ? 'fa' : 'en';
    document.querySelectorAll('.testimonial .who').forEach(function (who) {
      var av = who.querySelector('.t-avatar');
      if (!av) return;
      var name = who.querySelector('.lang-' + lang) || who.querySelector('.lang-en');
      av.textContent = name ? name.textContent.trim().charAt(0) : '★';
    });
  }
  document.querySelectorAll('.testimonial .who').forEach(function (who) {
    if (who.querySelector('.t-avatar')) return;
    var av = document.createElement('span');
    av.className = 't-avatar';
    av.setAttribute('aria-hidden', 'true');
    who.classList.add('has-avatar');
    who.insertBefore(av, who.firstChild);
  });
  updateAvatars();
  window.addEventListener('resize', updateAvatars);

  function setupReadMore() {
    document.querySelectorAll('.testimonial').forEach(function (card) {
      var q = card.querySelector('.quote');
      if (!q || card.querySelector('.more')) return;
      if (q.scrollHeight - q.clientHeight < 8) return;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'more';
      var label = function () {
        var open = card.classList.contains('expanded');
        b.textContent = root.lang === 'fa' ? (open ? 'کمتر' : 'ادامه…') : (open ? 'Show less' : 'Read more');
        b.setAttribute('aria-expanded', open ? 'true' : 'false');
      };
      b.addEventListener('click', function () {
        card.classList.toggle('expanded');
        label();
        window.dispatchEvent(new Event('resize'));
      });
      label();
      q.insertAdjacentElement('afterend', b);
    });
  }

  /* ---- Carousel — transform-based, arrows + dots + swipe, RTL-aware ---- */
  function initCarousel(rootEl) {
    var viewport = rootEl.querySelector('.carousel-viewport');
    var track = rootEl.querySelector('.carousel-track');
    if (!viewport || !track) return;
    var cards = Array.prototype.slice.call(track.children);
    if (!cards.length) return;
    var prev = rootEl.querySelector('.carousel-btn.prev');
    var next = rootEl.querySelector('.carousel-btn.next');
    var dotsWrap = rootEl.querySelector('.carousel-dots');
    var index = 0, dots = [], offsets = [];

    function rtl() { return getComputedStyle(track).direction === 'rtl'; }
    function startEdge(r) { return rtl() ? r.right : r.left; }
    function step() {
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      return cards[0].getBoundingClientRect().width + gap;
    }
    function perView() { return Math.max(1, Math.round(viewport.clientWidth / step())); }
    function maxIndex() { return Math.max(0, cards.length - perView()); }
    function measure() {
      var pt = track.style.transition, px = track.style.transform;
      track.style.transition = 'none';
      track.style.transform = 'translateX(0px)';
      var vs = startEdge(viewport.getBoundingClientRect());
      offsets = cards.map(function (c) { return startEdge(c.getBoundingClientRect()) - vs; });
      track.style.transform = px;
      void track.offsetWidth;
      track.style.transition = pt;
    }
    function buildDots() {
      if (!dotsWrap) return;
      dotsWrap.innerHTML = '';
      dots = [];
      for (var i = 0; i <= maxIndex(); i++) {
        (function (p) {
          var b = document.createElement('button');
          b.type = 'button';
          b.setAttribute('aria-label', 'Go to slide ' + (p + 1));
          b.addEventListener('click', function () { index = p; apply(); });
          dotsWrap.appendChild(b);
          dots.push(b);
        })(i);
      }
    }
    function apply() {
      index = Math.min(maxIndex(), Math.max(0, index));
      track.style.transform = 'translateX(' + (-offsets[index]) + 'px)';
      if (prev) prev.disabled = index <= 0;
      if (next) next.disabled = index >= maxIndex();
      dots.forEach(function (d, di) { d.classList.toggle('active', di === index); });
    }
    function go(delta) { index += delta; apply(); }
    if (prev) prev.addEventListener('click', function () { go(-perView()); });
    if (next) next.addEventListener('click', function () { go(perView()); });

    var x0 = null;
    track.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    track.addEventListener('touchend', function (e) {
      if (x0 == null) return;
      var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) < 40) return;
      go((rtl() ? dx > 0 : dx < 0) ? perView() : -perView());
    }, { passive: true });

    function refresh() { measure(); buildDots(); apply(); }
    var t;
    window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(refresh, 150); });
    window.addEventListener('load', refresh);
    refresh();
  }

  setupReadMore();
  document.querySelectorAll('[data-carousel]').forEach(initCarousel);
  window.addEventListener('load', setupReadMore);

  /* ---- Lesson dots (one per lesson) ---- */
  document.querySelectorAll('.lesson-dots[data-n]').forEach(function (el) {
    var n = parseInt(el.getAttribute('data-n'), 10) || 0;
    var html = '';
    for (var i = 0; i < n; i++) html += '<i></i>';
    el.innerHTML = html;
  });

  /* ---- Mini risk demo (home) ---- */
  var demo = document.getElementById('risk-demo');
  if (demo) {
    var range = demo.querySelector('input[type="range"]');
    var outPct = demo.querySelector('[data-out="pct"]');
    var outAmt = demo.querySelector('[data-out="amt"]');
    var verdict = demo.querySelector('.demo-verdict');
    var balance = parseFloat(demo.getAttribute('data-balance')) || 1000;
    var msgs = {
      ok:   { en: 'Healthy — within the 1–2% rule', fa: 'سالم — در محدودهٔ قانون ۱ تا ۲ درصد' },
      warn: { en: 'Aggressive — above 2% per trade', fa: 'پرریسک — بیش از ۲ درصد در هر معامله' },
      bad:  { en: 'Dangerous — one bad week can wipe you out', fa: 'خطرناک — یک هفتهٔ بد می‌تواند حساب را خالی کند' }
    };
    var updateDemo = function () {
      var v = parseFloat(range.value);
      var min = parseFloat(range.min), max = parseFloat(range.max);
      range.style.setProperty('--p', ((v - min) / (max - min) * 100) + '%');
      var fa = root.lang === 'fa';
      var pct = v.toFixed(1) + '%';
      var amt = '$' + (balance * v / 100).toFixed(0);
      outPct.textContent = fa ? toFaDigits(pct).replace('%', '٪') : pct;
      outAmt.textContent = fa ? toFaDigits(amt) : amt;
      var k = v <= 2 ? 'ok' : (v <= 4 ? 'warn' : 'bad');
      verdict.className = 'demo-verdict ' + k;
      verdict.textContent = msgs[k][fa ? 'fa' : 'en'];
    };
    range.addEventListener('input', updateDemo);
    updateDemo();
  }

  /* ---- Pointer effects: card spotlight + button light (fine pointers only) ---- */
  if (finePointer) {
    var spotSel = '.card, .lp-feature, .term, .step, .bento, .wa-inner';
    document.addEventListener('pointermove', function (e) {
      var el = e.target.closest && e.target.closest(spotSel);
      if (el) {
        var r = el.getBoundingClientRect();
        el.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        el.style.setProperty('--my', (e.clientY - r.top) + 'px');
      }
      var btn = e.target.closest && e.target.closest('.btn');
      if (btn) {
        var b = btn.getBoundingClientRect();
        btn.style.setProperty('--bx', (e.clientX - b.left) + 'px');
        btn.style.setProperty('--by', (e.clientY - b.top) + 'px');
      }
    }, { passive: true });
  }

  /* ---- Hero "live market" canvas (home) ---- */
  var canvas = document.querySelector('.hero-canvas');
  if (canvas && !reduceMotion && canvas.getContext) initMarket(canvas);

  function initMarket(cv) {
    var ctx = cv.getContext('2d');
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var W = 0, H = 0, candles = [], spacing = 22, bodyW = 10, offset = 0;
    var price = 0, running = true, last = 0;
    var mouse = { x: -1, y: -1, tx: 0, ty: 0, px: 0, py: 0 };
    var rtl = root.dir === 'rtl';

    function rand(a, b) { return a + Math.random() * (b - a); }
    function makeCandle(prevClose) {
      var drift = Math.sin(candles.length / 9) * 0.35 + 0.08;         // gentle up-trend with waves
      var o = prevClose;
      var c = o + rand(-1, 1) * 2.4 + drift;
      var h = Math.max(o, c) + rand(0.2, 1.6);
      var l = Math.min(o, c) - rand(0.2, 1.6);
      return { o: o, c: c, h: h, l: l, born: performance.now() };
    }
    function resize() {
      var r = cv.getBoundingClientRect();
      W = r.width; H = r.height;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      spacing = W < 640 ? 16 : 22; bodyW = W < 640 ? 7 : 10;
      var need = Math.ceil(W / spacing) + 4;
      while (candles.length < need) {
        price = candles.length ? candles[candles.length - 1].c : 0;
        var c = makeCandle(price); c.born = 0; candles.push(c);
      }
    }
    function range() {
      var lo = Infinity, hi = -Infinity;
      candles.forEach(function (c) { if (c.l < lo) lo = c.l; if (c.h > hi) hi = c.h; });
      return { lo: lo, hi: hi };
    }
    var smoothLo = null, smoothHi = null;

    function draw(now) {
      if (!running) return;
      var dt = Math.min(64, now - (last || now)); last = now;
      offset += dt * 0.012;                                   // scroll speed (px per ms)
      if (offset >= spacing) {
        offset -= spacing;
        candles.shift();
        candles.push(makeCandle(candles[candles.length - 1].c));
      }
      mouse.px += (mouse.tx - mouse.px) * 0.06;
      mouse.py += (mouse.ty - mouse.py) * 0.06;

      ctx.clearRect(0, 0, W, H);

      // grid
      ctx.save();
      ctx.translate(mouse.px * -8, mouse.py * -6);
      ctx.strokeStyle = 'rgba(148,170,210,0.06)';
      ctx.lineWidth = 1;
      for (var gx = -((offset * 2) % 64); gx < W + 64; gx += 64) { ctx.beginPath(); ctx.moveTo(gx, -20); ctx.lineTo(gx, H + 20); ctx.stroke(); }
      for (var gy = 0; gy < H + 64; gy += 64) { ctx.beginPath(); ctx.moveTo(-20, gy); ctx.lineTo(W + 20, gy); ctx.stroke(); }
      ctx.restore();

      var rg = range();
      if (smoothLo === null) { smoothLo = rg.lo; smoothHi = rg.hi; }
      smoothLo += (rg.lo - smoothLo) * 0.04; smoothHi += (rg.hi - smoothHi) * 0.04;
      var top = H * 0.18, bottom = H * 0.82;
      var y = function (v) { return bottom - (v - smoothLo) / (smoothHi - smoothLo || 1) * (bottom - top); };

      ctx.save();
      ctx.translate(mouse.px * -18, mouse.py * -12);
      var ma = [];
      for (var i = 0; i < candles.length; i++) {
        var c = candles[i];
        var x = i * spacing - offset;
        var fade = rtl ? 1 - x / W : x / W;                     // quieter behind the headline
        var a = Math.max(0.04, Math.min(1, fade * fade * 1.25));
        var grow = c.born ? Math.min(1, (now - c.born) / 600) : 1;
        var up = c.c >= c.o;
        var col = up ? '37,208,160' : '242,85,94';
        var yo = y(c.o), yc = y(c.o + (c.c - c.o) * grow);
        ctx.strokeStyle = 'rgba(' + col + ',' + (a * 0.55) + ')';
        ctx.beginPath(); ctx.moveTo(x, y(c.h)); ctx.lineTo(x, y(c.l)); ctx.stroke();
        ctx.fillStyle = 'rgba(' + col + ',' + (a * 0.5) + ')';
        var bh = Math.max(1.5, Math.abs(yc - yo));
        ctx.fillRect(x - bodyW / 2, Math.min(yo, yc), bodyW, bh);
        // moving average of closes
        var s = 0, n = 0;
        for (var k = Math.max(0, i - 7); k <= i; k++) { s += candles[k].c; n++; }
        ma.push([x, y(s / n)]);
      }
      // MA line with glow
      var grad = ctx.createLinearGradient(0, 0, W, 0);
      grad.addColorStop(rtl ? 1 : 0, 'rgba(250,153,57,0)');
      grad.addColorStop(rtl ? 0.55 : 0.45, 'rgba(250,153,57,0.12)');
      grad.addColorStop(rtl ? 0.2 : 0.8, 'rgba(255,190,92,0.9)');
      grad.addColorStop(rtl ? 0 : 1, 'rgba(250,153,57,1)');
      ctx.strokeStyle = grad;
      ctx.lineWidth = 2.2;
      ctx.shadowColor = 'rgba(250,153,57,0.7)';
      ctx.shadowBlur = 14;
      ctx.beginPath();
      ma.forEach(function (p, j) {
        if (!j) ctx.moveTo(p[0], p[1]);
        else {
          var q = ma[j - 1];
          ctx.quadraticCurveTo(q[0], q[1], (q[0] + p[0]) / 2, (q[1] + p[1]) / 2);
        }
      });
      ctx.stroke();
      ctx.shadowBlur = 0;

      // last-price pulse
      var lastP = ma[ma.length - 2];
      if (lastP) {
        var pulse = (now % 1600) / 1600;
        ctx.fillStyle = 'rgba(250,153,57,' + (0.35 * (1 - pulse)) + ')';
        ctx.beginPath(); ctx.arc(lastP[0], lastP[1], 4 + pulse * 14, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#FFBE5C';
        ctx.beginPath(); ctx.arc(lastP[0], lastP[1], 3.5, 0, Math.PI * 2); ctx.fill();
      }
      ctx.restore();

      // crosshair
      if (mouse.x >= 0) {
        ctx.strokeStyle = 'rgba(250,153,57,0.25)';
        ctx.setLineDash([4, 6]);
        ctx.beginPath(); ctx.moveTo(mouse.x, 0); ctx.lineTo(mouse.x, H); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(0, mouse.y); ctx.lineTo(W, mouse.y); ctx.stroke();
        ctx.setLineDash([]);
      }
      requestAnimationFrame(draw);
    }

    var hero = cv.parentElement;
    if (finePointer) {
      hero.addEventListener('pointermove', function (e) {
        var r = cv.getBoundingClientRect();
        mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
        mouse.tx = mouse.x / r.width - 0.5; mouse.ty = mouse.y / r.height - 0.5;
      }, { passive: true });
      hero.addEventListener('pointerleave', function () { mouse.x = -1; mouse.tx = 0; mouse.ty = 0; });
    }
    // Pause when off-screen or tab hidden
    var visible = true;
    function setRun(v) {
      if (v && !running) { running = true; last = 0; requestAnimationFrame(draw); }
      if (!v) running = false;
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (ents) { visible = ents[0].isIntersecting; setRun(visible && !document.hidden); }).observe(cv);
    }
    document.addEventListener('visibilitychange', function () { setRun(visible && !document.hidden); });
    var rt;
    window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(resize, 120); });
    resize();
    requestAnimationFrame(draw);
  }

  /* ---- Count-up numbers ---- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var suffix = el.getAttribute('data-suffix') || '';
    var en = el.querySelector('.lang-en'), fa = el.querySelector('.lang-fa');
    var write = function (v) {
      var s = Math.round(v) + suffix;
      if (en) en.textContent = s;
      if (fa) fa.textContent = toFaDigits(s).replace('%', '٪');
      if (!en && !fa) el.textContent = s;
    };
    if (!canAnimate) { write(target); return; }
    var o = { v: 0 };
    write(0);
    gsap.to(o, { v: target, duration: 1.8, ease: 'power2.out', onUpdate: function () { write(o.v); },
      scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
  }
  document.querySelectorAll('[data-count]').forEach(countUp);

  /* ======================================================================
     GSAP motion
     ====================================================================== */
  if (!canAnimate) {
    document.querySelectorAll('.lesson-dots').forEach(function (d) { d.classList.add('is-on'); });
    return;
  }

  // Split a heading into words (safe for Dari: never splits inside a word)
  function splitWords(el) {
    if (el.getAttribute('data-split-done')) return el.querySelectorAll('.split-word');
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/);
          var frag = document.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(p)); return; }
            var clip = document.createElement('span'); clip.className = 'reveal-clip';
            var w = document.createElement('span'); w.className = 'split-word'; w.textContent = p;
            clip.appendChild(w); frag.appendChild(clip);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && !/^(SVG|IMG|BR)$/i.test(n.tagName)) {
          walk(n);
        }
      });
    };
    walk(el);
    el.setAttribute('data-split-done', '1');
    return el.querySelectorAll('.split-word');
  }
  // Gradient text breaks when split into child boxes — move the gradient onto each word
  document.querySelectorAll('.hero h1 .accent, .page-head h1 .accent, .lp-hero h1 .grad').forEach(function (a) { a.classList.add('accent-split'); });

  /* Hero intro */
  var hero = document.querySelector('.hero');
  var intro = document.querySelectorAll('[data-intro]');
  if (intro.length) {
    var h1 = hero && hero.querySelector('h1');
    var tl = gsap.timeline({ defaults: { ease: 'power4.out' }, delay: 0.1 });
    tl.to(intro, { opacity: 1, y: 0, duration: 1, stagger: 0.09 });
    if (h1) {
      var hw = splitWords(h1);
      tl.from(hw, { yPercent: 110, duration: 1.1, stagger: 0.05 }, 0.05);
    }
    tl.from('.hero-card', { scale: 0.85, rotate: -6, opacity: 0, duration: 1.4, ease: 'expo.out' }, 0.2)
      .from('.chip', { scale: 0.6, opacity: 0, duration: 0.9, stagger: 0.12, ease: 'back.out(1.8)' }, 0.6);
    // Parallax out on scroll
    gsap.to('.hero-visual', { yPercent: 18, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
    gsap.to('.hero-copy', { yPercent: 10, opacity: 0.3, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
  }

  /* 3D tilt on the hero logo card */
  var tiltEl = document.querySelector('[data-tilt]');
  if (tiltEl && finePointer) {
    var area = tiltEl.closest('.hero') || tiltEl;
    var rx = gsap.quickTo(tiltEl, 'rotationX', { duration: 0.8, ease: 'power3.out' });
    var ry = gsap.quickTo(tiltEl, 'rotationY', { duration: 0.8, ease: 'power3.out' });
    area.addEventListener('pointermove', function (e) {
      var r = tiltEl.getBoundingClientRect();
      var dx = (e.clientX - (r.left + r.width / 2)) / window.innerWidth;
      var dy = (e.clientY - (r.top + r.height / 2)) / window.innerHeight;
      ry(dx * 28); rx(-dy * 22);
    });
    area.addEventListener('pointerleave', function () { rx(0); ry(0); });
  }

  /* Magnetic buttons */
  if (finePointer) {
    document.querySelectorAll('.btn-lg, .nav-cta').forEach(function (el) {
      var mx = gsap.quickTo(el, 'x', { duration: 0.5, ease: 'power3.out' });
      var my = gsap.quickTo(el, 'y', { duration: 0.5, ease: 'power3.out' });
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        mx((e.clientX - (r.left + r.width / 2)) * 0.25);
        my((e.clientY - (r.top + r.height / 2)) * 0.35);
      });
      el.addEventListener('pointerleave', function () { mx(0); my(0); });
    });
  }

  /* Interior page heads */
  document.querySelectorAll('.page-head h1, .lp-hero h1').forEach(function (h) {
    var words = splitWords(h);
    gsap.from(words, { yPercent: 110, duration: 1.1, ease: 'power4.out', stagger: 0.05, delay: 0.1 });
  });
  gsap.from('.page-head p, .lp-hero .lp-eyebrow, .lp-hero .lp-sub, .lp-hero .lp-cta-row, .lp-hero .lp-note', {
    y: 24, opacity: 0, duration: 1, ease: 'power3.out', stagger: 0.1, delay: 0.35
  });

  /* Section headings */
  document.querySelectorAll('.section-title, .wa-band h2, .empty-state h2').forEach(function (h) {
    if (h.closest('.page-head')) return;
    var words = splitWords(h);
    gsap.from(words, { yPercent: 110, duration: 1, ease: 'power4.out', stagger: 0.035,
      scrollTrigger: { trigger: h, start: 'top 88%', once: true } });
  });
  gsap.utils.toArray('.eyebrow:not([data-intro]), .section-head .lead, .band-islamic .lead').forEach(function (el) {
    gsap.from(el, { y: 20, opacity: 0, duration: 0.9, ease: 'power3.out', scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
  });

  /* Staggered reveals for repeating blocks */
  var batchSel = '.card:not(.testimonial), .bento, .lesson, .term, .step, .acc-item, .lp-feature, .stat, .path-step, .prose > *, .result-row, .calc-card, .founder, .table-wrap, .band-islamic, .article-card, .alert, .lp-stat, .embed-wrap';
  var batchEls = gsap.utils.toArray(batchSel).filter(function (el) { return !el.closest('.hero') && !el.closest('.carousel'); });
  gsap.set(batchEls, { y: 40, opacity: 0, transition: 'none' });
  ScrollTrigger.batch(batchEls, {
    start: 'top 92%',
    once: true,
    onEnter: function (els) {
      gsap.to(els, { y: 0, opacity: 1, duration: 0.9, ease: 'power3.out', stagger: 0.08, overwrite: true, clearProps: 'transform,opacity,transition' });
    }
  });
  gsap.from('.carousel', { y: 40, opacity: 0, duration: 1, ease: 'power3.out', scrollTrigger: { trigger: '.carousel', start: 'top 90%', once: true } });

  /* Lesson dots fill one by one */
  document.querySelectorAll('.lesson-dots').forEach(function (d) {
    var dots = d.querySelectorAll('i');
    ScrollTrigger.create({ trigger: d, start: 'top 94%', once: true, onEnter: function () {
      d.classList.add('is-on');
      gsap.fromTo(dots, { scale: 0.2, opacity: 0.2, transition: 'none' }, { scale: 1, opacity: 1, duration: 0.5, stagger: 0.035, ease: 'back.out(2)', clearProps: 'transform,opacity,transition' });
    } });
  });

  /* Learning path: line draws with scroll, nodes pop */
  var pathLine = document.querySelector('.path-line span');
  if (pathLine) {
    gsap.fromTo(pathLine, { scaleX: 0 }, { scaleX: 1, ease: 'none',
      scrollTrigger: { trigger: '.path', start: 'top 80%', end: 'bottom 60%', scrub: 0.6 } });
    gsap.fromTo('.path-node', { scale: 0, transition: 'none' }, { scale: 1, duration: 0.8, ease: 'back.out(2.2)', stagger: 0.15, clearProps: 'transform,transition',
      scrollTrigger: { trigger: '.path', start: 'top 85%', once: true } });
  }

  /* Mini calendar bars grow */
  var bars = document.querySelectorAll('.cal .bars i');
  if (bars.length) {
    gsap.from(bars, { scaleY: 0, duration: 0.8, ease: 'power3.out', stagger: 0.03,
      scrollTrigger: { trigger: '.cal', start: 'top 90%', once: true } });
  }

  /* Crescent rotates into place */
  gsap.from('.crescent svg', { rotate: -90, scale: 0.6, opacity: 0, duration: 1.4, ease: 'expo.out',
    scrollTrigger: { trigger: '.crescent', start: 'top 85%', once: true } });

  /* Footer wordmark rises */
  gsap.from('.footer-wordmark', { yPercent: 40, opacity: 0, ease: 'none',
    scrollTrigger: { trigger: '.footer', start: 'top bottom', end: 'bottom bottom', scrub: true } });

  window.addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
