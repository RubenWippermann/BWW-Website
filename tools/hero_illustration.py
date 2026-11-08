#!/usr/bin/env python3
"""Startseite: Foto-/Video-Hero (KI-Foto, Loop-Video) durch Illustration im Zeichenstil der Seite ersetzen (Ruben 08.11.2026). Idempotent."""
import os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'index.html'; h = open(f, encoding='utf8').read()
m = re.search(r'<div class="hero-visual">.*?</p></div>(?=</section>)', h, re.S)
if 'hero-uebungsraum' in h: print('bereits'); raise SystemExit
assert m, 'hero-visual nicht gefunden'
NEU = ('<div class="hero-visual"><img class="bww-ill hero-illu" src="/media/illustrations/bww/hero-uebungsraum-1024.webp" '
       'srcset="/media/illustrations/bww/hero-uebungsraum-750.webp 750w, /media/illustrations/bww/hero-uebungsraum-1024.webp 1024w" '
       'sizes="(min-width:1024px) 46vw, 92vw" width="1024" height="630" style="height:auto!important;aspect-ratio:1024/630;padding:clamp(12px,2vw,28px)!important" '
       'alt="Illustration: Eine Ausbilderin zeigt zwei Kursteilnehmenden an einer Übungspuppe die Herzdruckmassage" fetchpriority="high">'
       '<p class="bildnachweis">Illustration, KI-gestützt erstellt</p></div>')
h = h.replace(m.group(0), NEU)
h = re.sub(r'<script src="/assets/hero-loop\.js[^"]*"[^>]*></script>', '', h)
open(f, 'w', encoding='utf8').write(h); print('ersetzt')

# Preload auf das neue Bild und Aufräumen der alten Hero-Dateien (Foto-Poster, Loop-Video, Loop-Skript)
h = open(f, encoding='utf8').read()
h = re.sub(r'<link rel="preload" as="image" href="/media/hero/lehrsituation-poster-1440\.webp"[^>]*>',
           '<link rel="preload" as="image" href="/media/illustrations/bww/hero-uebungsraum-1024.webp" imagesrcset="/media/illustrations/bww/hero-uebungsraum-750.webp 750w, /media/illustrations/bww/hero-uebungsraum-1024.webp 1024w" imagesizes="(min-width:1024px) 46vw, 92vw" fetchpriority="high">', h)
open(f, 'w', encoding='utf8').write(h)
for p in ('media/hero/lehrsituation-loop.mp4', 'media/hero/lehrsituation-poster-1440.webp', 'media/hero/lehrsituation-poster-750.webp', 'assets/hero-loop.js'):
    if os.path.exists(p): os.remove(p)
