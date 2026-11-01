#!/usr/bin/env python3
"""Belegwortlaut nach QSEH-Nachweisen und Jurist-Gegenprüfung (01.11.): Ermächtigung (304-001) nur 'im Betrieb', Lehrkräfte/Sanitätsdienst als EIGNUNG mit Datum.
Gruppen: Karten Startseite/kurse/inhouse; FAQ 'Ist BWW ...?'; Einzelsätze. Idempotent."""
import re
EH = 'Für die Erste-Hilfe-Aus- und Fortbildung im Betrieb ist BWW ermächtigte Stelle der gesetzlichen Unfallversicherung (Kennziffer 8.2122, seit 28.10.2025).'
LK = 'BWW ist geeignete Stelle zur Aus- und Fortbildung von Lehrkräften der Ersten Hilfe (seit 28.10.2025, Kennziffer 8.2122).'
SAN = 'BWW ist geeignete Stelle zur Aus- und Fortbildung von Lehrkräften des betrieblichen Sanitätsdienstes (seit 29.10.2026, Kennziffer 8.2122).'
BS = 'BWW ist geeignete Stelle zur Aus- und Fortbildung von Betriebssanitätern (seit 29.10.2026, Kennziffer 8.2122).'
OLDQ = 'Ist BWW eine ermächtigte Stelle?'; OLDA = 'Ja. BWW ist ermächtigte Stelle der gesetzlichen Unfallversicherung (Kennziffer 8.2122).'
FAQ = {  # Seite -> (Frage, Antwort)
 'fuer-behoerden': (OLDQ, 'Ja. ' + EH), 'fuer-schulen': (OLDQ, 'Ja. ' + EH), 'kurse/erste-hilfe-fortbildung': (OLDQ, 'Ja. ' + EH),
 'kurse/erste-hilfe-bildungseinrichtungen': (OLDQ, 'Ja. Für die Erste-Hilfe-Aus- und Fortbildung im Betrieb und die Erste-Hilfe-Schulung in Bildungs- und Betreuungseinrichtungen ist BWW ermächtigte Stelle der gesetzlichen Unfallversicherung (Kennziffer 8.2122, seit 28.10.2025).'),
 'fuer-ausbilder': ('Ist BWW eine geeignete Stelle für Lehrkräfte-Ausbildung?', 'Ja. ' + LK),
 'kurse/lehrkraefte-ausbildung-lk1': ('Ist BWW eine geeignete Stelle für Lehrkräfte-Ausbildung?', 'Ja. ' + LK),
 'kurse/lehrkraefte-ausbildung-lk2': ('Ist BWW eine geeignete Stelle für Lehrkräfte-Ausbildung?', 'Ja. ' + LK),
 'kurse/lehrkraefte-fortbildung': ('Ist BWW eine geeignete Stelle für Lehrkräfte-Ausbildung?', 'Ja. ' + LK),
 'kurse/lehrkraefte-ausbildung-sanitaetsdienst': ('Ist BWW eine geeignete Stelle für diese Ausbildung?', 'Ja. ' + SAN),
 'kurse/betriebssanitaeter-aufbau': ('Ist BWW eine geeignete Stelle für die Betriebssanitäter-Ausbildung?', 'Ja. ' + BS),
 'kurse/betriebssanitaeter-fortbildung': ('Ist BWW eine geeignete Stelle für die Betriebssanitäter-Ausbildung?', 'Ja. ' + BS),
 'kurse/betriebssanitaeter-grundkurs': ('Ist BWW eine geeignete Stelle für die Betriebssanitäter-Ausbildung?', 'Ja. ' + BS)}
SATZ = {  # Seite -> [(alt, neu)]
 'kurse/lehrkraefte-ausbildung-lk1': [('BWW bildet als ermächtigte Stelle (Kennziffer 8.2122) auch Lehrkräfte aus.', LK)],
 'kurse/lehrkraefte-ausbildung-sanitaetsdienst': [('Die BWW UG (haftungsbeschränkt) ist nach DGUV Grundsatz 304-003 anerkannte und ermächtigte Stelle (Kennziffer 8.2122).', SAN),
                                                  ('BWW führt sie als ermächtigte Stelle (Kennziffer 8.2122) durch.', 'BWW ist dafür geeignete Stelle (Kennziffer 8.2122, seit 29.10.2026).')],
 'kurse/lehrbeauftragter-erste-hilfe': [('Die BWW UG (haftungsbeschränkt) ist nach DGUV Grundsatz 304-003 anerkannte und ermächtigte Stelle (Kennziffer 8.2122).', LK)],
 'kurse/lehrbeauftragten-fortbildung': [('Die BWW UG (haftungsbeschränkt) ist nach DGUV Grundsatz 304-003 anerkannte und ermächtigte Stelle (Kennziffer 8.2122).', LK)]}
KARTEN = ['index.html', 'kurse/index.html', 'inhouse-kurse/index.html']
K = [('Als betriebliche Erste-Hilfe-Ausbildung anerkannt – und über eure Berufsgenossenschaft oder Unfallkasse abrechenbar – sind nur Kurse einer <b>von der Berufsgenossenschaft anerkannten ermächtigten Stelle</b>. Genau das sind wir. Ohne diese Anerkennung tragt ihr die Kosten selbst.',
      'Als betriebliche Erste-Hilfe-Ausbildung gültig – und über eure Berufsgenossenschaft oder Unfallkasse abrechenbar – sind nur Kurse einer <b>ermächtigten Stelle</b>. ' + EH + ' Ohne diese Ermächtigung tragt ihr die Kosten selbst.'),
     ('<h3>Im vollen Umfang</h3><p>Unsere Ermächtigung umfasst <b>Erste Hilfe</b>, <b>Betriebssanitäter</b> und <b>Lehrkräfte</b> – wir bilden also auch Ausbilderinnen und Ausbilder aus. Diesen vollen Umfang haben längst nicht alle Anbieter.</p>',
      '<h3>Unsere Zulassungen</h3><p>Ermächtigt für die <b>Erste-Hilfe-Aus- und Fortbildung im Betrieb</b> (seit 28.10.2025). Geeignete Stelle für die Aus- und Fortbildung von <b>Lehrkräften der Ersten Hilfe</b> (seit 28.10.2025) sowie von <b>Lehrkräften des betrieblichen Sanitätsdienstes</b> und <b>Betriebssanitätern</b> (seit 29.10.2026).</p>')]
def rw(f, fn):
    h = open(f, encoding='utf8').read(); o = h; h = fn(h)
    if h != o: open(f, 'w', encoding='utf8').write(h); return 1
    return 0
n = 0
for f in KARTEN: n += rw(f, lambda h: h.replace(K[0][0], K[0][1]).replace(K[1][0], K[1][1]))
for p, (q, a) in FAQ.items(): n += rw(p + '/index.html', lambda h: h.replace(OLDA, a).replace(OLDQ, q))
for p, L in SATZ.items(): n += rw(p + '/index.html', lambda h: [h := h.replace(a, b) for a, b in L][-1])
# llms-full.txt: allgemeine Fassung
n += rw('llms-full.txt', lambda h: h.replace(OLDA, 'Ja. ' + EH + ' ' + LK.replace('BWW ist geeignete', 'Geeignete Stelle ist BWW') + ' Für Lehrkräfte des betrieblichen Sanitätsdienstes und Betriebssanitäter gilt dies seit 29.10.2026.'))
print('geändert:', n)
