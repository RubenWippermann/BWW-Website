#!/usr/bin/env python3
"""/fuer-ausbilder/ (Jurist 16.11.): FAQPage- und Organization-JSON-LD entfernen; Badge und FAQ-Antwort zur Ausbildungsstelle nur mit Abgrenzung im selben Block (Text, kein Siegel),
'Lehrkraefte' ohne Bescheidbeleg auf 'Ausbildungsstelle Erste Hilfe' gekuerzt. Idempotent. Arbeitet im Verzeichnis des Aufrufs (nach den Neutralformel-Skripten)."""
import json, os, re
p = os.path.join(os.getcwd(), 'fuer-ausbilder', 'index.html'); h = open(p, encoding='utf8').read()
TXT = 'Ausbildungsstelle Erste Hilfe, seit 28.10.2025 (Kennziffer 8.2122). Gilt für Aus- und Fortbildung in Erster Hilfe. Anerkennungsstatus des Lehrbeauftragten-Formats: Auskunft vor Buchung auf Anfrage.'
for m in list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)):
    j = json.loads(m.group(1))
    if isinstance(j, dict) and j.get('@type') in ('FAQPage', 'EducationalOrganization'): h = h.replace(m.group(0), '', 1)
a = '<span class="trust-badge">Geeignete Stelle für Lehrkräfte Erste Hilfe (seit 28.10.2025) · Kennziffer 8.2122</span>'
if a in h: h = h.replace(a, '<span class="trust-badge">' + TXT + '</span>', 1)
q = '<summary>Ist BWW eine geeignete Stelle für Lehrkräfte-Ausbildung?</summary><div class="faq-a">Ja. BWW ist geeignete Stelle zur Aus- und Fortbildung von Lehrkräften der Ersten Hilfe (seit 28.10.2025, Kennziffer 8.2122). Die Kennziffer kannst du bei deinem Unfallversicherungsträger nachprüfen.</div>'
if q in h: h = h.replace(q, '<summary>Ist BWW eine Ausbildungsstelle Erste Hilfe?</summary><div class="faq-a">' + TXT + '</div>', 1)
open(p, 'w', encoding='utf8').write(h)
ld = [json.loads(x).get('@type') for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]
vis = re.sub(r'<script.*?</script>', '', h, flags=re.S)
print('JSON-LD übrig:', ld, '| sichtbar 8.2122:', len(re.findall(r'8\.2122', vis)), '| "Lehrkräften der Ersten Hilfe"/"geeignete Stelle für Lehrkräfte":', len(re.findall(r'Lehrkräften der Ersten Hilfe|Stelle für Lehrkräfte', vis)))
