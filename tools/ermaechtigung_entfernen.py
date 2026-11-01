#!/usr/bin/env python3
"""Ermächtigungs-Badge entfernen auf Kursseiten, für die die Erste-Hilfe-Ermächtigung nicht gilt (Betriebssanitäter, Lehrkräfte), Freigabe Betriebsleitung 01.11. Ohne --apply Trockenlauf. Idempotent."""
import re, sys
apply = '--apply' in sys.argv
SEITEN = ['kurse/betriebssanitaeter-aufbau', 'kurse/betriebssanitaeter-fortbildung', 'kurse/betriebssanitaeter-grundkurs',
          'kurse/lehrkraefte-ausbildung-lk1', 'kurse/lehrkraefte-ausbildung-lk2', 'kurse/lehrkraefte-ausbildung-sanitaetsdienst', 'kurse/lehrkraefte-fortbildung']
PAT = re.compile(r'<section class="badge-strip"><div class="trust-badges" aria-label="Vertrauensmerkmale"><span class="trust-badge trust-badge--seal"><svg class="ic"[^>]*><path d="[^"]*"/></svg> BG-anerkannte ermächtigte Stelle · Kennziffer 8\.2122</span></div></section>')
n = 0
for s in SEITEN:
    f = s + '/index.html'; h = open(f, encoding='utf8').read()
    nh, k = PAT.subn('', h)
    print(('entfernt ' if apply else 'würde entfernen ') + f, k)
    if k and apply: open(f, 'w', encoding='utf8').write(nh)
    n += k
print(n, 'Badges')
