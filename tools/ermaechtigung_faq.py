#!/usr/bin/env python3
"""FAQ 'Ist BWW eine anerkannte Stelle?' neutralisieren (Jurist-Linie: ohne Beleg entfernen), bis der Ermächtigungsbescheid vorliegt. Idempotent."""
import re, glob
A = re.compile(r'Ja\. BWW ist von der Berufsgenossenschaft als ermächtigte Stelle anerkannt – Kennziffer 8\.2122, im vollen Umfang für Erste Hilfe, Betriebssanitäter und Lehrkräfte(?: \(DGUV-Grundsätze 304-001, 304-002 und 304-003\))?\.')
NA = 'Ja. BWW ist ermächtigte Stelle der gesetzlichen Unfallversicherung (Kennziffer 8.2122).'
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['llms-full.txt', 'llms.txt']:
    h = open(f, encoding='utf8').read(); o = h
    if 'von der Berufsgenossenschaft als ermächtigte Stelle anerkannt' not in h: continue
    h = A.sub(NA, h).replace('Ist BWW eine anerkannte Stelle?', 'Ist BWW eine ermächtigte Stelle?')
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
# Abschnitt 'Amtlich anerkannt' (Startseite, kurse/, inhouse-kurse/)
B = [('<span class="eyebrow">Amtlich anerkannt</span>', '<span class="eyebrow">Ermächtigte Stelle</span>'),
     ('<h2>Von der Berufsgenossenschaft anerkannte ermächtigte Stelle</h2>', '<h2>Ermächtigte Stelle der gesetzlichen Unfallversicherung</h2>'),
     ('<p>Kennziffer <b>8.2122</b> – im vollen Umfang: <b>Erste Hilfe</b>, <b>Betriebssanitäter</b> und <b>Lehrkräfte</b>.</p>', '<p>Kennziffer <b>8.2122</b></p>'),
     ('<p>Kennziffer <b>8.2122</b> – im vollen Umfang: <b>Erste Hilfe</b>, <b>Betriebssanitäter</b> und <b>Lehrkräfte</b> (DGUV-Grundsätze 304-001, 304-002 und 304-003).</p>', '<p>Kennziffer <b>8.2122</b></p>')]
for f in ['index.html', 'kurse/index.html', 'inhouse-kurse/index.html']:
    h = open(f, encoding='utf8').read(); o = h
    for a, b in B: h = h.replace(a, b)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
print('geändert:', n)
