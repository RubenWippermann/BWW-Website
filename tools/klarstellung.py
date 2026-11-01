#!/usr/bin/env python3
"""Jurist-Auflagen 'Rettungsdienstbildungsstelle' (01.11.): Klarstellungssatz im Footer (nicht auf Rechtstexten) und im Unternehmensprofil;
Langform 'Bildungswerk ...' nur mit Rechtsform als Geschäftsbezeichnung. Idempotent."""
import glob, os
S = 'BWW UG (haftungsbeschränkt) ist ein gewerblicher Bildungsanbieter und keine Schule im Sinne der Schulgesetze.'
LEGAL = ()   # Footer-Satz auf JEDER Seite (Jurist 01.11., Bedingung zum Namen im Kopf); nur der Footer, nie der Rechtstext
n = 0
OLDF = 'BWW UG (haftungsbeschränkt). Praxisnahe'
NEWF = S + ' Praxisnahe'
for f in glob.glob('**/index.html', recursive=True) + ['404.html']:
    if f.startswith(LEGAL): continue
    h = open(f, encoding='utf8').read(); o = h
    h = h.replace(OLDF, NEWF)
    if f == 'unternehmensprofil/index.html':
        h = h.replace('<h1>BWW – Bildungswerk für Wiederbelebung und Erste Hilfe</h1>', '<h1>BWW UG (haftungsbeschränkt) – Bildungswerk für Wiederbelebung und Erste Hilfe</h1>')
        h = h.replace('"alternateName":"BWW – Bildungswerk für Wiederbelebung und Erste Hilfe"', '"alternateName":"BWW UG (haftungsbeschränkt) – Bildungswerk für Wiederbelebung und Erste Hilfe"')
        a = '<p><strong>BWW (Bildungswerk für Wiederbelebung und Erste Hilfe)</strong> ist eine'
        h = h.replace(a, '<p><strong>BWW UG (haftungsbeschränkt)</strong> (Geschäftsbezeichnung: Bildungswerk für Wiederbelebung und Erste Hilfe) ist eine', 1)
        if S not in h.split('<footer')[0]:
            i = h.find('<h2>Über BWW</h2>'); j = h.find('</p>', i) + 4
            h = h[:j] + '\n<p>' + S + '</p>' + h[j:]
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
f = 'llms-full.txt'; h = open(f, encoding='utf8').read(); o = h
h = h.replace('Hauptüberschrift: BWW – Bildungswerk für Wiederbelebung und Erste Hilfe', 'Hauptüberschrift: BWW UG (haftungsbeschränkt) – Bildungswerk für Wiederbelebung und Erste Hilfe')
if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
print('geändert:', n)
