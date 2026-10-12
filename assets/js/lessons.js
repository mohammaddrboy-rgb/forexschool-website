/* Lesson pages: quiz, "done" progress (saved in this browser only), table-of-contents highlight.
   Also marks finished lessons on courses.html. Loaded on lesson pages and courses.html. */
(function () {
  'use strict';
  var KEY = 'mf-lessons-done';
  var isFa = location.pathname.indexOf('/fa/') !== -1;
  function faDigits(s) { return String(s).replace(/[0-9]/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }); }
  function loadDone() {
    try { var v = JSON.parse(localStorage.getItem(KEY) || '[]'); return Array.isArray(v) ? v : []; } catch (e) { return []; }
  }
  function saveDone(list) { try { localStorage.setItem(KEY, JSON.stringify(list)); } catch (e) { /* private mode */ } }

  /* ---------- Quiz ---------- */
  var main = document.querySelector('.lesson-main');
  var quiz = document.querySelector('.lquiz');
  if (main && quiz) {
    var id = main.getAttribute('data-lesson');
    var qs = Array.prototype.slice.call(quiz.querySelectorAll('.q'));
    var result = quiz.querySelector('.quiz-result');
    var score = quiz.querySelector('.quiz-score');

    var finish = function () {
      var answered = qs.filter(function (q) { return q.hasAttribute('data-answered'); });
      if (answered.length < qs.length) return;
      var right = qs.filter(function (q) { return q.getAttribute('data-answered') === 'right'; }).length;
      var pass = right === qs.length;
      if (pass) {
        var done = loadDone();
        if (done.indexOf(id) === -1) { done.push(id); saveDone(done); }
      }
      score.textContent = isFa
        ? (pass ? 'عالی! هر ' + faDigits(qs.length) + ' پرسش را درست جواب دادید — این درس تکمیل شد ✓'
                : faDigits(right) + ' از ' + faDigits(qs.length) + ' پاسخ درست. درس را مرور کنید و دوباره امتحان کنید.')
        : (pass ? 'Excellent! All ' + qs.length + ' correct — lesson marked as done ✓'
                : right + ' of ' + qs.length + ' correct. Review the lesson and try again.');
      result.classList.toggle('is-pass', pass);
      result.hidden = false;
    };

    qs.forEach(function (q) {
      var correct = +q.getAttribute('data-correct');
      var opts = Array.prototype.slice.call(q.querySelectorAll('.q-opt'));
      opts.forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (q.hasAttribute('data-answered')) return;
          var pick = +btn.getAttribute('data-i');
          q.setAttribute('data-answered', pick === correct ? 'right' : 'wrong');
          opts.forEach(function (b) { b.disabled = true; });
          opts[correct].classList.add('is-correct');
          if (pick !== correct) btn.classList.add('is-wrong');
          q.querySelector('.q-why').hidden = false;
          finish();
        });
      });
    });

    quiz.querySelector('.quiz-reset').addEventListener('click', function () {
      qs.forEach(function (q) {
        q.removeAttribute('data-answered');
        q.querySelector('.q-why').hidden = true;
        q.querySelectorAll('.q-opt').forEach(function (b) { b.disabled = false; b.classList.remove('is-correct', 'is-wrong'); });
      });
      result.hidden = true;
      result.classList.remove('is-pass');
      qs[0].querySelector('.q-opt').focus();
    });

    if (loadDone().indexOf(id) !== -1) {
      var badge = document.querySelector('.lesson-head .lmeta');
      if (badge) {
        var s = document.createElement('span');
        s.className = 'chip-lite';
        s.style.color = 'var(--bull)';
        s.textContent = isFa ? 'تکمیل‌شده ✓' : 'Completed ✓';
        badge.appendChild(s);
      }
    }
  }

  /* ---------- Table of contents: highlight the section in view ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.lesson-toc a'));
  if (links.length && 'IntersectionObserver' in window) {
    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible[e.target.id] = e.isIntersecting; });
      var firstId = null;
      links.some(function (a) { var k = a.getAttribute('href').slice(1); if (visible[k]) { firstId = k; return true; } return false; });
      if (firstId) links.forEach(function (a) { a.classList.toggle('is-active', a === map[firstId]); });
    }, { rootMargin: '-20% 0px -60% 0px' });
    Object.keys(map).forEach(function (k) { var el = document.getElementById(k); if (el) io.observe(el); });
  }

  /* ---------- courses.html: mark finished lessons ---------- */
  var rows = document.querySelectorAll('.lesson[data-lesson]');
  if (rows.length) {
    var done = loadDone();
    rows.forEach(function (r) { if (done.indexOf(r.getAttribute('data-lesson')) !== -1) r.classList.add('is-done'); });
    document.querySelectorAll('[data-progress]').forEach(function (el) {
      var ids = Array.prototype.map.call(document.querySelectorAll(el.getAttribute('data-progress') + ' .lesson[data-lesson]'), function (r) { return r.getAttribute('data-lesson'); });
      var n = ids.filter(function (x) { return done.indexOf(x) !== -1; }).length;
      if (!n) return;
      el.innerHTML = isFa
        ? 'پیشرفت شما: <b>' + faDigits(n) + ' از ' + faDigits(ids.length) + '</b> درس تکمیل شده (در همین مرورگر).'
        : 'Your progress: <b>' + n + ' of ' + ids.length + '</b> lessons done (saved in this browser).';
      el.hidden = false;
    });
  }
})();
