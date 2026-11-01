#!/usr/bin/env python3
"""Header-Untertitel zentral umstellen (vorbereitet 01.11., NICHT ausgerollt; erst nach Rubens Antwort mit --apply).
Eine Stelle: UNTERTITEL_NEU. Ohne --apply nur Zählung (Trockenlauf). Idempotent."""
import glob, sys, os
UNTERTITEL_ALT = 'Multiplikatorenstelle &amp; Rettungsdienstbildungsstelle'   # so steht es im HTML
UNTERTITEL_ALT_ROH = 'Multiplikatorenstelle & Rettungsdienstbildungsstelle'
UNTERTITEL_NEU = 'Multiplikatorenstelle · Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst'   # Jurist Nachtrag 2, 01.11. (kurz: '… Erste Hilfe und Sanitätsdienst'); erst nach Rubens Bestätigung --apply
apply = '--apply' in sys.argv
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['index.html', '404.html']:
    if not os.path.exists(f): continue
    h = open(f, encoding='utf8').read(); o = h
    for a in (f'<small>{UNTERTITEL_ALT}</small>', f'<small>{UNTERTITEL_ALT_ROH}</small>'):
        h = h.replace(a, f'<small>{UNTERTITEL_NEU}</small>')
    if h != o:
        n += 1
        if apply: open(f, 'w', encoding='utf8').write(h)
print(('geändert: ' if apply else 'Trockenlauf, würde ändern: ') + str(n), 'Seiten')
