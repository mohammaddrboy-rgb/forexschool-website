# -*- coding: utf-8 -*-
"""Broker profiles for brokers.html (built by build-brokers.py). Text pairs are (English, Dari).

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

# Live broker profiles. Empty for now (owner's request, 2026-10-29): the page shows a
# "coming soon" box until the owner sends broker details. The previous 8 profiles (Exness, XM,
# IC Markets, Pepperstone, Tickmill, AvaTrade, Admirals, RoboForex) are kept in archive_2026-10.py
# and on the git branch archive/brokers-v1.
#
# Template for one broker (copy into the list and fill in; every text is (English, Dari)):
#
# dict(
#     id="exness",                          # used for the direct link /brokers.html#exness
#     name="Exness",
#     url="https://www.exness.com",         # official website
#     register_url="https://...",           # OPTIONAL: registration / sign-up link from the owner —
#                                           # shows an "Open an account" button (row + details).
#     color="#FFDE02", ink="#1A1A1A",       # logo-badge background / letter colour
#     tier="mix",                           # one of TIERS above
#     tagline=("One-line summary.", "خلاصهٔ یک‌خطی."),
#     chips=[("From $10", "از ۱۰ دلار"), ("MT4 · MT5", "MT4 · MT5")],
#     clusters=[                            # boxes; icons: shield, coins, screen, wallet
#         (("Company & regulation", "شرکت و نظارت"), "shield", [
#             (("Founded", "تأسیس"), ("2008", "۲۰۰۸")),
#         ]),
#     ],
#     pros=[("…", "…")],
#     cons=[("…", "…")],
#     best=("Who it suits.", "مناسب چه کسی است."),
# ),
BROKERS = [
]
