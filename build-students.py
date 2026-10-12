#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync the Student Stories page (students.html) from the homepage testimonials.

The homepage carousel in index.html is the single source of truth for testimonials.
This script:
  1. copies every <article class="card testimonial"> from index.html into students.html,
     tagging each with its city (data-city) for the city filter;
  2. builds the city filter buttons (All + one per city, with counts);
  3. updates every count marked data-sync="students" / data-sync="cities"
     in index.html and students.html.

Run it after adding or editing a testimonial, BEFORE build-fa.py:

    python build-students.py && python build-fa.py && python build-geo.py
"""
import io, re

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

def read(p): return io.open(p, encoding="utf-8").read()
def write(p, s): io.open(p, "w", encoding="utf-8").write(s)

idx = read("index.html")
track = re.search(r'<div class="carousel-track">(.*?)\n        </div>\n        </div>', idx, re.S).group(1)
cards = re.findall(r'<article class="card testimonial">\s*<p class="quote">.*?</article>', track, re.S)
assert cards, "no testimonials found in index.html"

cities = {}          # slug -> [en, fa, count]  (insertion order = first appearance)
out = []
for c in cards:
    m = re.search(r'<span><span class="lang-en">([^<]+)</span><span class="lang-fa">([^<]+)</span></span></div>', c)
    en, fa = (m.group(1).strip(), m.group(2).strip()) if m else ("Other", "دیگر")
    slug = re.sub(r"[^a-z0-9]+", "-", en.lower()).strip("-")
    cities.setdefault(slug, [en, fa, 0])[2] += 1
    body = re.sub(r"\n\s*", "\n            ", c.strip())
    body = body.replace('<article class="card testimonial">', '<article class="card testimonial" data-city="%s">' % slug, 1)
    body = re.sub(r"\n\s*</article>$", "\n          </article>", body)
    out.append("          " + body)

total, ncity = len(cards), len(cities)
order = sorted(cities.items(), key=lambda kv: -kv[1][2])
btn = '<button type="button" class="filter-chip%s" data-filter="%s" aria-pressed="%s"><span class="lang-en">%s</span><span class="lang-fa">%s</span> <span class="fc-n"><span class="lang-en">%d</span><span class="lang-fa">%s</span></span></button>'
chips = [btn % (" active", "all", "true", "All", "همه", total, str(total).translate(FA_DIGITS))]
chips += [btn % ("", s, "false", en, fa, n, str(n).translate(FA_DIGITS)) for s, (en, fa, n) in order]

st = read("students.html")
st = re.sub(r"<!-- students:list -->.*?<!-- /students:list -->",
            lambda m: "<!-- students:list -->\n" + "\n".join(out) + "\n        <!-- /students:list -->", st, flags=re.S)
st = re.sub(r"<!-- students:filters -->.*?<!-- /students:filters -->",
            lambda m: "<!-- students:filters -->\n        " + "\n        ".join(chips) + "\n        <!-- /students:filters -->", st, flags=re.S)

def sync(s, key, n):
    pat = re.compile(r'(<(\w+)[^>]*data-sync="%s"[^>]*>)<span class="lang-en">[^<]*</span><span class="lang-fa">[^<]*</span>' % key)
    def rep(m):
        tag = re.sub(r'data-count="\d+"', 'data-count="%d"' % n, m.group(1))
        return '%s<span class="lang-en">%d</span><span class="lang-fa">%s</span>' % (tag, n, str(n).translate(FA_DIGITS))
    return pat.sub(rep, s)

for path, s in (("students.html", st), ("index.html", idx)):
    s = sync(sync(s, "students", total), "cities", ncity)
    write(path, s)

print("Synced %d testimonials from %d cities into students.html." % (total, ncity))
