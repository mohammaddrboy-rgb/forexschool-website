# -*- coding: utf-8 -*-
"""Podcast episodes for podcast.html (built by build-podcast.py). Newest episode first.

To add an episode: put the mastered MP3 and its cover (1400x1400 JPG) in assets/podcast/, copy the dict
below, fill it in (text pairs are (English, Dari)), then run:
    python build-podcast.py && python build-fa.py && python build-geo.py
`seconds` and `bytes` come from the MP3 (ffprobe / file size).
"""

SHOW = {
    "title": ("Forex School Podcast", "پادکست مکتب فارکس"),
    "host": ("Mohammad Akhondzadeh", "محمد آخوندزاده"),
    "cover": "/assets/podcast/show-cover.jpg",
}

EPISODES = [
dict(
    num=2, date="2026-11-13", seconds=417, bytes=5127858,
    audio="/assets/podcast/forex-school-podcast-e02.mp3",
    cover="/assets/podcast/e02-cover.jpg",
    title=("The 1–2% risk rule", "قانون ریسک ۱ تا ۲ درصد"),
    sub=("Why this rule can save your trading account", "چرا این قانون نجات‌دهنده هست"),
    desc=("At the start, your goal isn't growth — it's survival. If you survive, there will always be a chance to grow. In this episode of the Forex School Podcast, Mohammad Akhondzadeh explains the 1–2% risk rule and why it can save your trading account.",
          "هدف شما در ابتدا، رشد نیست — بقا است. اگر زنده بمانید، فرصت رشد همیشه هست. در این قسمت از پادکست مکتب فارکس، محمد آخوندزاده قانون ریسک ۱ تا ۲ درصد را توضیح می‌دهد و اینکه چرا این قانون می‌تواند حساب معاملاتی شما را نجات دهد."),
),
dict(
    num=1, date="2026-11-01", seconds=1125, bytes=13634775,
    audio="/assets/podcast/forex-school-podcast-e01.mp3",
    cover="/assets/podcast/e01-cover.jpg",
    title=("Why do most beginner traders lose money?", "چرا اکثر معامله‌گران تازه‌کار ضرر می‌کنند؟"),
    sub=("The three main reasons new traders lose in the forex market", "سه علت اصلی ضرر‌ده بودن تریدرهای تازه‌کار در بازار فارکس"),
    desc=("Most people who start trading forex lose money in their first months. In this first episode of the Forex School Podcast, Mohammad Akhondzadeh explains the three main reasons beginner traders lose — so you can recognise them early and avoid them.",
          "بیشتر کسانی که معامله در فارکس را شروع می‌کنند، در ماه‌های اول ضرر می‌کنند. در نخستین قسمت پادکست مکتب فارکس، محمد آخوندزاده سه علت اصلی ضرر‌ده بودن تریدرهای تازه‌کار را توضیح می‌دهد — تا بتوانید آن‌ها را زود بشناسید و از آن‌ها دوری کنید."),
),
]
