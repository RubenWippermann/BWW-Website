#!/usr/bin/env python3
"""T-259: statischer Platzhalter im Terminblock (#live-termine) 'Termine werden geladen …' -> 'Termine auf Anfrage.' (ohne JavaScript und fuer Crawler sichtbar; mit JavaScript ersetzt booking.js den Inhalt). Idempotent."""
import glob, os, sys
OHNE = {a.split('=',1)[1] for a in sys.argv if a.startswith('--ohne=')}; NUR = {a.split('=',1)[1] for a in sys.argv if a.startswith('--nur=')}
A = 'Termine werden geladen … <a href="/kurse/offene-kurse-worbis/">'; B = 'Termine auf Anfrage. <a href="/kurse/offene-kurse-worbis/">'
n = 0
for p in glob.glob('**/index.html', recursive=True):
    if p.startswith('tools/') or p in OHNE or (NUR and p not in NUR): continue
    h = open(p, encoding='utf8').read()
    if A in h: open(p, 'w', encoding='utf8').write(h.replace(A, B)); n += 1
print('Seiten:', n)
