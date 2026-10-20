#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ergaenzt <meta name="theme-color" content="#25704e"> (BWW-Corporate-Design-Gruen, marken.ts) in allen Seiten
direkt hinter dem viewport-Meta. Idempotent. Aufruf im Wurzelverzeichnis: python3 tools/theme_color_ergaenzen.py [--pruefen]"""
import glob, sys
V = '<meta name="viewport" content="width=device-width,initial-scale=1">'
T = '<meta name="theme-color" content="#25704e">'
n = fehlt = 0
for f in sorted(glob.glob("**/*.html", recursive=True)):
    h = open(f, encoding="utf-8").read()
    if 'name="theme-color"' in h or V not in h:
        continue
    n += 1
    if "--pruefen" not in sys.argv:
        open(f, "w", encoding="utf-8").write(h.replace(V, V + T, 1))
print(n, "Seiten" + (" wuerden ergaenzt" if "--pruefen" in sys.argv else " ergaenzt"))
