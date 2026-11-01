#!/usr/bin/env python3
"""VORBEREITET (nicht ausgerollt): Ermächtigungs-Aussage nach Jurist Nachtrag 2. Trockenlauf ohne --apply.
'BG-anerkannte ermächtigte Stelle · Kennziffer 8.2122' (Trust-Badge) -> 'Ermächtigte Stelle der gesetzlichen Unfallversicherung für die Erste-Hilfe-Ausbildung (Kennziffer 8.2122)'.
Ermächtigungsaussage nur an Erste-Hilfe-Kursen; Betriebssanitäter-/Lehrkräfte-Seiten werden NICHT angefasst, sondern gelistet (Entscheidung Jurist). Keine DGUV/BG-Logos."""
import glob, sys
apply = '--apply' in sys.argv
BADGE_ALT = 'BG-anerkannte ermächtigte Stelle · Kennziffer 8.2122'
BADGE_NEU = 'Ermächtigte Stelle der gesetzlichen Unfallversicherung für die Erste-Hilfe-Ausbildung (Kennziffer 8.2122)'
SATZ_ALT = 'bei einer BG-anerkannten Stelle wie BWW (Kennziffer 8.2122)'
SATZ_NEU = 'bei einer ermächtigten Stelle wie BWW (Kennziffer 8.2122)'
NICHT = ('kurse/betriebssanitaeter-', 'kurse/lehrkraefte-')   # Jurist entscheidet: Ermächtigung gilt hier evtl. nicht
n = 0; offen = []
for f in sorted(glob.glob('**/index.html', recursive=True)):
    h = open(f, encoding='utf8').read(); o = h
    if BADGE_ALT not in h and SATZ_ALT not in h: continue
    if f.startswith(NICHT): offen.append(f); continue
    h = h.replace(BADGE_ALT, BADGE_NEU).replace(SATZ_ALT, SATZ_NEU)
    if h != o:
        n += 1; print(('geändert ' if apply else 'würde ändern ') + f)
        if apply: open(f, 'w', encoding='utf8').write(h)
print(f'{n} Seiten; unberührt (Jurist-Entscheidung): {len(offen)}', offen)
