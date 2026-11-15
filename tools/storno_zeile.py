#!/usr/bin/env python3
"""T-291 (BL/Jurist Nr. 79, 16.11.): Stornozeile mit Widerrufshinweis unter den Hero-Aktionen, NUR auf Kursseiten mit direktem Buchungsbutton (mind. ein <a class="termin-row"> im statischen HTML).
Wortlaut woertlich: Kostenfrei stornieren bis 14 Kalendertage vor Veranstaltungsbeginn, in Textform (AGB § 6.2). Verbraucher haben zusaetzlich ein gesetzliches Widerrufsrecht (Widerrufsbelehrung).
Links: AGB § 6.2 -> /agb/, Widerrufsbelehrung -> /widerruf/. --ohne=<Seite> (Messseite lk1 erst nach Freeze). Idempotent; nach neuen Terminen erneut laufen lassen. Arbeitet im Verzeichnis des Aufrufs."""
import glob, re, sys
OHNE = {a.split('=',1)[1] for a in sys.argv if a.startswith('--ohne=')}
Z = ('<p class="hero-note">Kostenfrei stornieren bis 14 Kalendertage vor Veranstaltungsbeginn, in Textform (<a href="/agb/">AGB § 6.2</a>). '
     'Verbraucher haben zusätzlich ein gesetzliches Widerrufsrecht (<a href="/widerruf/">Widerrufsbelehrung</a>).</p>')
mit, ohne = [], []
for p in sorted(glob.glob('kurse/*/index.html')):
    if p in OHNE: continue
    h = open(p, encoding='utf8').read(); body = re.sub(r'<script.*?</script>', '', h, flags=re.S)
    if '<a class="termin-row"' not in body or h.count('<div class="hero-actions">') != 1: ohne.append(p); continue
    mit.append(p)
    if Z in h: continue
    i = h.index('<div class="hero-actions">'); j = h.index('</div>', i) + 6
    open(p, 'w', encoding='utf8').write(h[:j] + Z + h[j:])
print('mit Zeile:', len(mit)); print('ohne (kein Buchungsbutton):', ', '.join(x.split('/')[1] for x in ohne))
