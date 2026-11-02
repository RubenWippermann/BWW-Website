#!/usr/bin/env python3
"""/kurse/offene-kurse-worbis/: Mischanrede du/ihr auf ihr/euch vereinheitlichen (idempotent)."""
import os
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'kurse/offene-kurse-worbis/index.html'; h = open(f, encoding='utf8').read(); n = 0
for a, b in (('freie Termine findest du direkt', 'freie Termine findet ihr direkt'), ('in deiner Buchungsbestätigung', 'in eurer Buchungsbestätigung')):
    n += h.count(a); h = h.replace(a, b)
open(f, 'w', encoding='utf8').write(h); print('Ersetzungen:', n)
