#!/usr/bin/env python3
"""Kuerzt <title> (und gleichlautende og:title/twitter:title) auf <= 70 Zeichen.

Formel (Befund Web-A 26, 12.10.2026), nur bei Titeln > 70 Zeichen:
  1. Marke " | BWW Wissensdatenbank" -> " | BWW"
  2. immer noch > 70 und Doppelpunkt im Kern: Kern bis vor dem Doppelpunkt (Kernbegriff vorn)
  3. sonst unveraendert (kein Abschneiden mitten im Wort)
Marke bleibt am Ende. Aufruf im Wurzelverzeichnis: python3 tools/titel_kuerzen.py [--pruefen]
"""
import glob, html, re, sys

MAX = 70
LANG, KURZ = " | BWW Wissensdatenbank", " | BWW"


def kuerzen(t):
    if len(t) <= MAX:
        return t
    if t.endswith(LANG):
        t = t[: -len(LANG)] + KURZ
    if len(t) > MAX and " | " in t:
        kern, marke = t.rsplit(" | ", 1)
        if ":" in kern:
            kopf = kern.split(":", 1)[0].strip()
            if len(kopf) >= 20:
                t = f"{kopf} | {marke}"
    return t


def main(pruefen):
    n = 0
    for f in sorted(glob.glob("**/index.html", recursive=True)):
        s = open(f, encoding="utf-8").read()
        m = re.search(r"<title>(.*?)</title>", s, re.S)
        if not m:
            continue
        alt = html.unescape(m.group(1))
        neu = kuerzen(alt)
        if neu == alt:
            continue
        n += 1
        if pruefen:
            print(f"{len(alt):3d}->{len(neu):3d} {f}: {neu}")
            continue
        a, b = html.escape(alt, quote=False), html.escape(neu, quote=False)
        s = s.replace(f"<title>{m.group(1)}</title>", f"<title>{b}</title>")
        for prop in ('property="og:title"', 'name="twitter:title"'):
            s = s.replace(f'<meta {prop} content="{html.escape(alt)}"', f'<meta {prop} content="{html.escape(neu)}"')
            s = s.replace(f'<meta {prop} content="{a}"', f'<meta {prop} content="{b}"')
        open(f, "w", encoding="utf-8").write(s)
    print(n, "Titel angepasst" if not pruefen else "Titel wuerden angepasst")


main("--pruefen" in sys.argv)
