#!/usr/bin/env python3
"""Stimmen-Block: Hinweissatz zur Auswahl (4 und 5 Sterne) entfernt (Auftrag BL/Ruben 04.11.2026). Auswahl der Bewertungen selbst unverändert. Idempotent."""
import os
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
UZ = 'Ausgewählte Rückmeldungen unserer Teilnehmenden. Wir veröffentlichen Rückmeldungen mit 4 und 5 Sternen; nicht alle Bewertungen werden veröffentlicht.'
n = 0
for f in ['index.html', 'inhouse-kurse/index.html', 'kurse/lehrkraefte-ausbildung-lk1/index.html', 'kurse/lehrkraefte-ausbildung-lk2/index.html']:
    h = open(f, encoding='utf8').read(); a = f'<p id="stimmen-agg">{UZ}</p>'
    if a in h: open(f, 'w', encoding='utf8').write(h.replace(a, '<p id="stimmen-agg"></p>')); n += 1
print('Seiten:', n)
p = 'tools/bewertung_darstellung.py'; s = open(p, encoding='utf8').read()
if UZ in s: open(p, 'w', encoding='utf8').write(s.replace("UZ = '" + UZ + "'", "UZ = ''  # Hinweissatz am 04.11.2026 entfernt (siehe bewertung_unterzeile_entfernen.py)"))
