#!/usr/bin/env python3
"""Fixes aus dem statischen Audit 02.11. (Reihe D). Rechtsseiten werden nicht angefasst. Idempotent."""
import re, glob
n = 0
def rw(f, pairs):
    global n
    h = open(f, encoding='utf8').read(); o = h
    for a, b in pairs: h = h.replace(a, b)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
rw('kurse/offene-kurse-worbis/index.html', [('sind über die ermächtigte Stelle (Kennziffer 8.2122, DGUV-Grundsatz 304-001) anerkannt.',
   'werden von der BWW UG (haftungsbeschränkt) durchgeführt, ermächtigte Stelle der gesetzlichen Unfallversicherung für die Erste-Hilfe-Aus- und Fortbildung im Betrieb (Kennziffer 8.2122).')])
for f in ('fuer-kitas/index.html', 'kurse/erste-hilfe-bildungseinrichtungen/index.html', 'llms-full.txt'):
    rw(f, [('ist er der anerkannte Nachweis für Beschäftigte in diesem Bereich', 'ist er der maßgebliche Nachweis für Beschäftigte in diesem Bereich')])
rw('llms-full.txt', [('- Anerkennung: von der Berufsgenossenschaft ermächtigte Stelle, Kennziffer 8.2122', '- Ermächtigung: ermächtigte Stelle der gesetzlichen Unfallversicherung für die Erste-Hilfe-Aus- und Fortbildung im Betrieb, Kennziffer 8.2122')])
rw('abrechnung/index.html', [('<input id="trSearch" type="search"', '<input id="trSearch" aria-label="Träger oder Branche suchen" type="search"')])
rw('notruf-simulator/index.html', [('<input id="notrufAnswer" placeholder', '<input id="notrufAnswer" aria-label="Antwort im Notruf-Simulator" placeholder')])
rw('404.html', [('<h3>Alle Kurse', '<h2>Alle Kurse'), ('<h3>Inhouse-Kurse', '<h2>Inhouse-Kurse')])
h = open('404.html', encoding='utf8').read()
h2 = re.sub(r'<h2>(Alle Kurse.*?)</h3>', r'<h2>\1</h2>', h, flags=re.S); h2 = re.sub(r'<h2>(Inhouse-Kurse.*?)</h3>', r'<h2>\1</h2>', h2, flags=re.S)
if h2 != h: open('404.html', 'w', encoding='utf8').write(h2); n += 1
print('geändert:', n)
