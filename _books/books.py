# -*- coding: utf-8 -*-
"""Trading books for books.html (built by build-books.py). Text pairs are (English, Dari). Newest first.

The list is EMPTY until the owner sends the first book — the page then shows a "coming soon" box.

To add a book:
  1. Put the book file in assets/books/ (e.g. assets/books/trading-in-the-zone.pdf) and its cover image
     (portrait JPG, about 600x900) as assets/books/trading-in-the-zone.jpg.
  2. Copy the template below into BOOKS, fill it in, then run:
         python build-books.py && python build-fa.py && python build-geo.py
  Only publish books Forex School is allowed to share (public domain, the author's permission, or our own).
  If a book can't be shared as a file, leave `file` empty and set `link` to the official page instead.

Template:

dict(
    id="trading-in-the-zone",                 # used for the direct link /books.html#trading-in-the-zone
    title=("Trading in the Zone", "معامله در منطقه"),
    author=("Mark Douglas", "مارک داگلاس"),
    year="2000",                              # optional
    level=("Beginner–intermediate", "مبتدی تا متوسط"),   # optional
    pages="216",                              # optional
    focus=("Trading psychology", "روانشناسی معامله"),   # main focus — shown as a chip
    cover="/assets/books/trading-in-the-zone.jpg",
    intro=("One short paragraph introducing the book: what it is about, who the author is, who it is for.",
           "یک پاراگراف کوتاه برای معرفی کتاب: موضوع اصلی، نویسنده و اینکه برای چه کسی مناسب است."),
    summary=[                                 # a couple of paragraphs
        ("First summary paragraph…", "پاراگراف اول خلاصه…"),
        ("Second summary paragraph…", "پاراگراف دوم خلاصه…"),
    ],
    file="/assets/books/trading-in-the-zone.pdf",   # download (leave "" if not shared as a file)
    size="2.4 MB",                                  # shown on the download button (optional)
    lang=("English", "انگلیسی"),                    # language of the book file (optional)
    link="",                                        # optional official page (used when there is no file)
),
"""

BOOKS = [
]
