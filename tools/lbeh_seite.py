#!/usr/bin/env python3
"""LBEH-Kursseite nach Jurist (jurist/bww-qseh-liste-lbeh-01-11.md): private Qualifizierung, Hinweis oben, keine Kennziffer/'ermächtigte Stelle'. Idempotent.
Auf /kurse/lehrbeauftragten-fortbildung/ nur der Kennziffer-Satz entfernt (gleiche Logik, Lehrgang außerhalb der Eignung)."""
import re, json
def esc(s): return s.replace('&', '&amp;')
T = 'Lehrbeauftragten-Qualifizierung Erste Hilfe, 120 UE | BWW'
D = 'Qualifizierung für Erste-Hilfe-Lehrkräfte nach Orientierungsrahmen: 120 UE an 14 Tagen, 700 €. Keine QSEH-registrierte Maßnahme, keine DGUV-Anerkennung.'
assert len(T) <= 60 and len(D) <= 155, (len(T), len(D))
P = 'kurse/lehrbeauftragter-erste-hilfe/index.html'
h = open(P, encoding='utf8').read(); o = h
h = re.sub(r'<title>.*?</title>', f'<title>{T}</title>', h, 1)
h = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + D + '"', h, 1)
for a, v in (('og:title', T), ('og:description', D), ('twitter:title', T), ('twitter:description', D)):
    h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % a, lambda m: m.group(1) + v + '"', h, 1)
h = h.replace('<h1>Lehrbeauftragter Erste Hilfe</h1><p>Pädagogische Qualifizierung zum Lehrbeauftragten Erste Hilfe: Lehrbeauftragte bilden Lehrkräfte aus und fort. Die Qualifizierung umfasst mindestens 120 Unterrichtseinheiten an 14 Tagen in Präsenz.</p>',
 '<h1>Lehrbeauftragten-Qualifizierung Erste Hilfe (nach Orientierungsrahmen)</h1><p><strong>Wichtig: Dieser Lehrgang ist keine bei der QSEH registrierte oder von der DGUV anerkannte Maßnahme.</strong> Er richtet sich an erfahrene Lehrkräfte Erste Hilfe, die sich für die Aus- und Fortbildung von Lehrkräften qualifizieren möchten, und orientiert sich am Orientierungsrahmen (Anhang 3) der DGUV Grundsatz 304-003. Die Bescheinigung ist eine Teilnahmebescheinigung der BWW UG (haftungsbeschränkt). Ob ihr als Lehrbeauftragte oder Lehrbeauftragter tätig werden dürft, entscheidet die Ausbildungsstelle, die euch benennt, und die QSEH; die Lehrberechtigung ist befristet. 120 Unterrichtseinheiten an 14 Tagen in Präsenz.</p>')
h = h.replace('<span class="fact-v">Erste-Hilfe-Lehrkräfte, die künftig Lehrkräfte aus- und fortbilden', '<span class="fact-v">Erfahrene Lehrkräfte Erste Hilfe, die sich für die Aus- und Fortbildung von Lehrkräften qualifizieren möchten')
h = h.replace('<span class="fact-k">Abschluss</span><span class="fact-v">Teilnahmebescheinigung<', '<span class="fact-k">Abschluss</span><span class="fact-v">Teilnahmebescheinigung (Qualifizierung nach Orientierungsrahmen)<')
h = h.replace('<li>Pädagogische Schulung für Lehrbeauftragte im Umfang von mindestens 120 UE insgesamt</li>', '<li>Pädagogische Schulung im Umfang von mindestens 120 UE insgesamt</li>')
# Kennziffer-Satz raus (beide Seiten)
KS = 'BWW ist geeignete Stelle zur Aus- und Fortbildung von Lehrkräften der Ersten Hilfe (seit 28.10.2025, Kennziffer 8.2122). '
h = h.replace(KS, '')
# Course-Schema
h = h.replace('"name":"Lehrbeauftragter Erste Hilfe","description":"Pädagogische Qualifizierung zum Lehrbeauftragten Erste Hilfe: Lehrbeauftragte bilden Lehrkräfte aus und fort. Die Qualifizierung umfasst mindestens 120 Unterrichtseinheiten an 14 Tagen in Präsenz."',
              '"name":"Lehrbeauftragten-Qualifizierung Erste Hilfe (nach Orientierungsrahmen)","description":"Qualifizierung für erfahrene Lehrkräfte Erste Hilfe nach dem Orientierungsrahmen der DGUV Grundsatz 304-003, mindestens 120 Unterrichtseinheiten an 14 Tagen in Präsenz. Keine QSEH-registrierte Maßnahme, keine DGUV-Anerkennung."')
n = 0
if h != o: open(P, 'w', encoding='utf8').write(h); n += 1
P2 = 'kurse/lehrbeauftragten-fortbildung/index.html'; g = open(P2, encoding='utf8').read()
if KS in g: open(P2, 'w', encoding='utf8').write(g.replace(KS, '')); n += 1
print('geändert:', n)
