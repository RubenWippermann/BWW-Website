#!/usr/bin/env python3
"""Stimmen-Block: keine Gesamtnote/Anzahl mehr; offene Unterzeile (Jurist 03.11.2026, Mindestlösung). Idempotent. Kein AggregateRating im Markup (war nie vorhanden)."""
import hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
UZ = ''  # Hinweissatz am 04.11.2026 entfernt (siehe bewertung_unterzeile_entfernen.py)
js = open('assets/bewertungen.js', encoding='utf8').read()
a = js.find("    var a = d.aggregat, agg = document.getElementById('stimmen-agg');"); b = js.find("    sec.hidden = false;")
if 0 <= a < b:
    js = js[:a] + js[b:]
js = js.replace("Kein JSON-LD / AggregateRating: Bewertungen gelten fuer die Firma, nicht fuer eine einzelne Kursseite (Selbstbewertungs-Richtlinie). */",
                "Kein JSON-LD / AggregateRating: Bewertungen gelten fuer die Firma, nicht fuer eine einzelne Kursseite (Selbstbewertungs-Richtlinie).\n   Keine Gesamtnote/Anzahl (Jurist 03.11.2026): nur ausgewaehlte Stimmen mit offener Unterzeile (4 und 5 Sterne). */")
open('assets/bewertungen.js', 'w', encoding='utf8').write(js)
tok = hashlib.sha1(js.encode()).hexdigest()[:8]; n = 0
for f in ['index.html', 'inhouse-kurse/index.html', 'kurse/lehrkraefte-ausbildung-lk1/index.html', 'kurse/lehrkraefte-ausbildung-lk2/index.html']:
    h = o = open(f, encoding='utf8').read()
    h = h.replace('<p id="stimmen-agg"></p>', f'<p id="stimmen-agg">{UZ}</p>')
    h = re.sub(r'(bewertungen\.js\?v=)[^"\']*', lambda m: m.group(1) + tok, h)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
print('Seiten:', n, '| Token', tok)
