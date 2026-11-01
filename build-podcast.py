#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the episode list (with audio players) on podcast.html from _podcast/episodes.py.

The list sits between <!-- podcast:list --> and <!-- /podcast:list --> in podcast.html; the page's
description and share image are updated to the newest episode. Run after adding an episode, BEFORE build-fa.py:

    python build-podcast.py && python build-fa.py && python build-geo.py
"""
import io, json, os, re, sys, html

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "_podcast"))
import episodes as E  # noqa: E402

BASE = "https://forexschool.store"
FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MONTHS_FA = ["جنوری", "فبروری", "مارچ", "اپریل", "می", "جون", "جولای", "اگست", "سپتمبر", "اکتوبر", "نومبر", "دسمبر"]
ORD_FA = {1: "اول", 2: "دوم", 3: "سوم", 4: "چهارم", 5: "پنجم", 6: "ششم", 7: "هفتم", 8: "هشتم", 9: "نهم", 10: "دهم"}

def read(p): return io.open(p, encoding="utf-8").read()
def write(p, s): io.open(p, "w", encoding="utf-8").write(s)
def fa(n): return str(n).translate(FA_DIGITS)
def bi(pair): return '<span class="lang-en">%s</span><span class="lang-fa">%s</span>' % pair

def date_pair(d):
    y, m, day = (int(x) for x in d.split("-"))
    return ("%d %s %d" % (day, MONTHS[m - 1], y), "%s %s %s" % (fa(day), MONTHS_FA[m - 1], fa(y)))

def clock(s): return "%d:%02d" % (s // 60, s % 60)

ICON = {
    "play": '<svg class="pp-i-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>'
            '<svg class="pp-i-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z"/></svg>',
    "back": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2L7 6l5 4V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z"/><text x="12" y="16.2" text-anchor="middle" font-size="6.5" font-weight="700" font-family="sans-serif">15</text></svg>',
    "fwd": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5V2l5 4-5 4V7a6 6 0 1 0 6 6h2a8 8 0 1 1-8-8z"/><text x="12" y="16.2" text-anchor="middle" font-size="6.5" font-weight="700" font-family="sans-serif">15</text></svg>',
    "dl": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M11 4h2v8.2l3.3-3.3 1.4 1.4L12 16l-5.7-5.7 1.4-1.4 3.3 3.3zM5 18h14v2H5z"/></svg>',
}

def episode(ep, latest):
    n = ep["num"]
    mins = round(ep["seconds"] / 60)
    mb = ep["bytes"] / 1e6
    label = ("Episode %d" % n, "قسمت %s" % ORD_FA.get(n, fa(n)))
    return """
      <article class="pod-ep card%(latest_cls)s" id="episode-%(n)d">
        <div class="pod-art">
          <img src="%(cover)s" width="1400" height="1400" alt="%(alt)s" loading="%(loading)s">
        </div>
        <div class="pod-body">
          <div class="pod-meta">%(new)s<span class="badge">%(label)s</span><span class="chip-lite">%(date)s</span><span class="chip-lite">%(len)s</span></div>
          <h2 class="pod-title">%(title)s</h2>
          <p class="pod-sub">%(sub)s</p>
          <p class="pod-desc">%(desc)s</p>
          <div class="pod-player" dir="ltr" data-seconds="%(secs)d">
            <audio preload="metadata" src="%(audio)s"></audio>
            <button type="button" class="pp-play" aria-label="Play / pause">%(i_play)s</button>
            <div class="pp-main">
              <input type="range" class="pp-seek" min="0" max="1000" value="0" step="1" aria-label="Seek">
              <div class="pp-row">
                <span class="pp-time"><span class="pp-cur">0:00</span> / <span class="pp-dur">%(dur)s</span></span>
                <span class="pp-ctrls">
                  <button type="button" class="pp-btn pp-back" aria-label="Back 15 seconds">%(i_back)s</button>
                  <button type="button" class="pp-btn pp-fwd" aria-label="Forward 15 seconds">%(i_fwd)s</button>
                  <button type="button" class="pp-btn pp-speed" aria-label="Playback speed">1×</button>
                  <a class="pp-btn pp-dl" href="%(audio)s" download aria-label="Download MP3 (%(mb).0f MB)" title="Download MP3 (%(mb).0f MB)">%(i_dl)s</a>
                </span>
              </div>
            </div>
          </div>
        </div>
      </article>""" % {
        "n": n, "latest_cls": " pod-latest" if latest else "", "cover": ep["cover"], "loading": "eager" if latest else "lazy",
        "alt": html.escape("%s — %s" % (label[0], ep["title"][0])),
        "new": ('<span class="pod-new">%s</span>' % bi(("New", "تازه"))) if latest else "",
        "label": bi(label), "date": bi(date_pair(ep["date"])), "len": bi(("%d min" % mins, "%s دقیقه" % fa(mins))),
        "title": bi(ep["title"]), "sub": bi(ep["sub"]), "desc": bi(ep["desc"]),
        "secs": ep["seconds"], "audio": ep["audio"], "dur": clock(ep["seconds"]), "mb": mb,
        "i_play": ICON["play"], "i_back": ICON["back"], "i_fwd": ICON["fwd"], "i_dl": ICON["dl"],
    }

PLAYER_JS = r"""
      <script>
        /* Podcast players: play/pause, seek, ±15 s, speed, one episode at a time; Dari digits on /fa/. */
        (function () {
          var fa = document.documentElement.lang === 'fa';
          function num(s) { return fa ? s.replace(/\d/g, function (d) { return '۰۱۲۳۴۵۶۷۸۹'[d]; }).replace('.', '٫') : s; }
          function clock(t) { t = Math.max(0, Math.floor(t || 0)); var h = Math.floor(t / 3600), m = Math.floor(t % 3600 / 60), s = t % 60;
            return num((h ? h + ':' + (m < 10 ? '0' : '') : '') + m + ':' + (s < 10 ? '0' : '') + s); }
          var players = [].slice.call(document.querySelectorAll('.pod-player'));
          var SPEEDS = [1, 1.25, 1.5, 2];
          players.forEach(function (box) {
            var a = box.querySelector('audio'), play = box.querySelector('.pp-play'), seek = box.querySelector('.pp-seek'),
                cur = box.querySelector('.pp-cur'), dur = box.querySelector('.pp-dur'), sp = box.querySelector('.pp-speed');
            var total = +box.getAttribute('data-seconds') || 0, dragging = false;
            dur.textContent = clock(total); sp.textContent = num('1×');
            function paint() {
              var d = a.duration || total, p = d ? a.currentTime / d : 0;
              if (!dragging) seek.value = Math.round(p * 1000);
              seek.style.setProperty('--p', (p * 100).toFixed(2) + '%');
              cur.textContent = clock(a.currentTime);
            }
            a.addEventListener('loadedmetadata', function () { if (a.duration) dur.textContent = clock(a.duration); });
            a.addEventListener('timeupdate', paint);
            a.addEventListener('play', function () { box.classList.add('is-playing');
              players.forEach(function (o) { if (o !== box) { var x = o.querySelector('audio'); if (!x.paused) x.pause(); } }); });
            a.addEventListener('pause', function () { box.classList.remove('is-playing'); });
            a.addEventListener('ended', function () { box.classList.remove('is-playing'); });
            play.addEventListener('click', function () { if (a.paused) { a.play(); } else { a.pause(); } });
            seek.addEventListener('input', function () { dragging = true; var d = a.duration || total;
              seek.style.setProperty('--p', (seek.value / 10) + '%'); cur.textContent = clock(seek.value / 1000 * d); });
            seek.addEventListener('change', function () { var d = a.duration || total; a.currentTime = seek.value / 1000 * d; dragging = false; paint(); });
            box.querySelector('.pp-back').addEventListener('click', function () { a.currentTime = Math.max(0, a.currentTime - 15); paint(); });
            box.querySelector('.pp-fwd').addEventListener('click', function () { a.currentTime = Math.min((a.duration || total), a.currentTime + 15); paint(); });
            sp.addEventListener('click', function () { var i = (SPEEDS.indexOf(a.playbackRate) + 1) % SPEEDS.length;
              a.playbackRate = SPEEDS[i]; sp.textContent = num(SPEEDS[i] + '×'); });
          });
        })();
      </script>"""

def build():
    eps = E.EPISODES
    latest = eps[0]
    ld = {"@context": "https://schema.org", "@type": "PodcastSeries", "name": E.SHOW["title"][0], "alternateName": E.SHOW["title"][1],
          "url": BASE + "/podcast.html", "image": BASE + E.SHOW["cover"], "inLanguage": "fa",
          "author": {"@type": "Person", "name": E.SHOW["host"][0]},
          "publisher": {"@type": "EducationalOrganization", "name": "Forex School", "url": BASE},
          "hasPart": [{"@type": "PodcastEpisode", "episodeNumber": e["num"], "name": e["title"][1], "alternateName": e["title"][0],
                       "description": e["desc"][0], "datePublished": e["date"], "timeRequired": "PT%dM%dS" % (e["seconds"] // 60, e["seconds"] % 60),
                       "url": BASE + "/podcast.html#episode-%d" % e["num"], "image": BASE + e["cover"],
                       "associatedMedia": {"@type": "MediaObject", "contentUrl": BASE + e["audio"], "encodingFormat": "audio/mpeg"}}
                      for e in eps]}
    block = """<!-- podcast:list (generated by build-podcast.py from _podcast/episodes.py — do not edit by hand) -->
      <div class="pod-list">%(eps)s
      </div>
      <p class="pod-follow">%(follow)s</p>
      <script type="application/ld+json">%(ld)s</script>%(js)s
      <!-- /podcast:list -->""" % {
        "eps": "".join(episode(e, i == 0) for i, e in enumerate(eps)),
        "follow": bi(('Also on <a href="https://www.instagram.com/forexmaktab/" target="_blank" rel="noopener">Instagram</a> and in our <a href="https://www.facebook.com/groups/1009705208203191" target="_blank" rel="noopener">Facebook group</a> — new episodes are announced on the WhatsApp channel first.',
                      'همچنین در <a href="https://www.instagram.com/forexmaktab/" target="_blank" rel="noopener">اینستاگرام</a> و <a href="https://www.facebook.com/groups/1009705208203191" target="_blank" rel="noopener">گروه فیسبوک</a> ما — قسمت‌های تازه ابتدا در کانال واتساپ اعلام می‌شوند.')),
        "ld": json.dumps(ld, ensure_ascii=False), "js": PLAYER_JS,
    }
    src = read("podcast.html")
    src, n = re.subn(r"<!-- podcast:list.*?<!-- /podcast:list -->", lambda m: block, src, count=1, flags=re.S)
    if not n:
        raise SystemExit("podcast.html: markers <!-- podcast:list --> ... <!-- /podcast:list --> not found")
    # page description + share image follow the newest episode
    desc = "Forex School Podcast in Dari — latest episode: %s %s" % (latest["title"][0], latest["sub"][0].lower() + ".")
    src = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(desc), src, count=1)
    src = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape("Episode %d: %s" % (latest["num"], latest["title"][0])), src, count=1)
    src = re.sub(r'(<meta property="og:image" content=")[^"]*', lambda m: m.group(1) + BASE + latest["cover"], src, count=1)
    write("podcast.html", src)
    print("Built %d podcast episode(s) on podcast.html." % len(eps))

if __name__ == "__main__":
    build()
