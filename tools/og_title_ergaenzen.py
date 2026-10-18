#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ergaenzt <meta property="og:title"> (Wert = vorhandener <title>) auf HTML-Seiten, die ihn nicht haben.
Idempotent: Seiten mit og:title bleiben unveraendert. Aufruf: python3 tools/og_title_ergaenzen.py [--pruefen]"""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
pruefen = "--pruefen" in sys.argv
n = 0
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if x not in (".git", "node_modules", "assets", "media")]
    for f in files:
        if not f.endswith(".html"):
            continue
        p = os.path.join(d, f)
        s = open(p, encoding="utf-8").read()
        if 'property="og:title"' in s or "property='og:title'" in s:
            continue
        m = re.search(r"<title>([^<]*)</title>", s)
        if not m or not m.group(1).strip():
            continue
        n += 1
        print(("fehlt: " if pruefen else "ergaenzt: ") + os.path.relpath(p, ROOT))
        if not pruefen:
            tag = '<meta property="og:title" content="%s">' % m.group(1).strip().replace('"', "&quot;")
            s = s[: m.end()] + tag + s[m.end():]
            open(p, "w", encoding="utf-8").write(s)
print(n, "Seiten", "ohne og:title" if pruefen else "ergaenzt")
