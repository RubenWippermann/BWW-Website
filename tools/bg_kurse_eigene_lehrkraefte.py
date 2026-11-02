#!/usr/bin/env python3
"""Sachlicher Satz: BG-Kurse der BWW UG halten ausschließlich BWW-eigene Lehrkräfte (Beleg: Bescheid-Auswertung, Beauftragung Dritter unzulässig). Idempotent."""
import os
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
S = ' BG-Kurse der BWW UG werden ausschließlich von BWW-eigenen Lehrkräften durchgeführt.'
R = {
 'abrechnung': 'über den zuständigen Unfallversicherungsträger abrechnen.</p><div class="hero-actions">',
 'kurse/erste-hilfe-ausbildung': 'über die zuständige BG oder Unfallkasse abrechenbar; die Entscheidung trifft der Träger.</p>',
 'kurse/erste-hilfe-fortbildung': 'an realistischen Fallbeispielen aus eurem Arbeitsumfeld.</p>',
}
n = 0
for p, a in R.items():
    f = p + '/index.html'; h = open(f, encoding='utf8').read()
    if 'ausschließlich von BWW-eigenen Lehrkräften' in h: continue
    assert h.count(a) == 1, (p, h.count(a))
    b = a.replace('</p>', S + '</p>', 1); open(f, 'w', encoding='utf8').write(h.replace(a, b)); n += 1
print('geändert:', n)
