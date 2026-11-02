#!/usr/bin/env python3
"""Sanitätshelfer-Kursseite ohne Ermächtigungs-/Anerkennungs-/QSEH-/VBG-Bezug (BL-Entscheidung 02.11.): hasCredential (Kennziffer, QSEH, VBG) aus dem Organization-JSON-LD dieser Seite entfernen. Idempotent."""
import re, json
f = 'kurse/sanitaetshelfer-ausbildung/index.html'
h = open(f, encoding='utf8').read(); o = h
def fix(m):
    j = json.loads(m.group(1))
    if isinstance(j, dict) and 'hasCredential' in j:
        j.pop('hasCredential'); return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + '</script>'
    return m.group(0)
h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', fix, h, flags=re.S)
if h != o: open(f, 'w', encoding='utf8').write(h); print('geändert')
else: print('keine Änderung')
