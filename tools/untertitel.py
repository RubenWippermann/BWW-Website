#!/usr/bin/env python3
"""Header-Untertitel zentral umstellen (vorbereitet 01.11., NICHT ausgerollt; erst nach Rubens Antwort mit --apply).
Eine Stelle: UNTERTITEL_NEU. Ohne --apply nur Zählung (Trockenlauf). Idempotent."""
import glob, sys, os
UNTERTITEL_ALT = 'Multiplikatorenstelle · Bildungsstelle für Erste Hilfe und betrieblichen Sanitätsdienst'   # Stand Reihe A (live seit bcfbcbff)
UNTERTITEL_ALT_ROH = 'Multiplikatorenstelle &amp; Rettungsdienstbildungsstelle'   # Zwischenstand, falls noch vorhanden
UNTERTITEL_NEU = 'Bildungswerk für Wiederbelebung und Erste Hilfe'   # Rubens Entscheidung 01.11.: voller Name sichtbar im Kopf; Rechtsform im Logo-alt/Footer/Impressum
apply = '--apply' in sys.argv
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['index.html', '404.html']:
    if not os.path.exists(f): continue
    h = open(f, encoding='utf8').read(); o = h
    for a in (f'<small>{UNTERTITEL_ALT}</small>', f'<small>{UNTERTITEL_ALT_ROH}</small>', '<small>Multiplikatorenstelle & Rettungsdienstbildungsstelle</small>'):
        h = h.replace(a, f'<small>{UNTERTITEL_NEU}</small>')
    # Logo-alt im Kopf mit Rechtsform (Jurist Nachtrag 3)
    h = h.replace('<header class="site-header"><a class="brand" href="/"><img src="/media/bww-logo-transparent.webp" width="1744" height="738" alt="BWW Logo">', '<header class="site-header"><a class="brand" href="/"><img src="/media/bww-logo-transparent.webp" width="1744" height="738" alt="BWW UG (haftungsbeschränkt)">')
    if h != o:
        n += 1
        if apply: open(f, 'w', encoding='utf8').write(h)
print(('geändert: ' if apply else 'Trockenlauf, würde ändern: ') + str(n), 'Seiten')
