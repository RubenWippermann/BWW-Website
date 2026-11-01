#!/usr/bin/env python3
"""VORBEREITET (nicht ausgerollt): 'Von Rettungsdienst-Profis' ersetzen (Jurist Nachtrag 2; Dozentennamen nirgends). Trockenlauf ohne --apply."""
import glob, sys, re, html
apply = '--apply' in sys.argv
R = [('von Rettungsdienst-Profis', 'mit erfahrenen Dozenten'),            # Beschreibungen Standortseiten, Startseiten-Fließtext
     ('>Von Rettungsdienst-Profis<', '>Erfahrene Dozenten aus der Praxis<')]  # Trust-Badge
n = 0
for f in sorted(glob.glob('**/index.html', recursive=True)):
    h = open(f, encoding='utf8').read(); o = h
    for a, b in R: h = h.replace(a, b)
    if h != o:
        for m in re.finditer(r'<meta name="description" content="(.*?)"', h):
            if len(html.unescape(m.group(1))) > 155: print('ZU LANG', f)
        n += 1; print(('geändert ' if apply else 'würde ändern ') + f)
        if apply: open(f, 'w', encoding='utf8').write(h)
print(n, 'Seiten')
