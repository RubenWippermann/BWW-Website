#!/usr/bin/env python3
"""Neutralformel-Seiten: Organization-JSON-LD ohne hasCredential (Ermaechtigung/QSEH/8.2122): Kennziffer 8.2122 nie auf Lehrbeauftragten-/Fachseiten (Jurist). Idempotent. Arbeitet im Verzeichnis des Aufrufs."""
import json, os, re
ROOT = os.getcwd()
PAGES = ['ausbilder-werden/lehrbeauftragter', 'ausbilder-werden/preise', 'fuer-ausbilder', 'kurse/lehrbeauftragten-fortbildung', 'kurse/lehrbeauftragter-erste-hilfe']
n = 0
for page in PAGES:
    p = os.path.join(ROOT, page, 'index.html'); h = open(p, encoding='utf8').read(); h0 = h
    for m in list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)):
        j = json.loads(m.group(1))
        if isinstance(j, dict) and 'hasCredential' in j:
            del j['hasCredential']
            h = h.replace(m.group(0), '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + '</script>', 1)
    if h != h0: open(p, 'w', encoding='utf8').write(h); n += 1
print('Seiten:', n)
for page in PAGES:
    h = open(os.path.join(ROOT, page, 'index.html'), encoding='utf8').read()
    ld = ' '.join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S))
    vis = re.sub(r'<script.*?</script>', '', h, flags=re.S)
    print(page, '| JSON-LD 8.2122/QSEH/hasCredential:', bool(re.search(r'8\.2122|QSEH|hasCredential', ld)), '| sichtbar 8.2122:', len(re.findall(r'8\.2122', vis)))
