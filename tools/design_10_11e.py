#!/usr/bin/env python3
"""Design 10.11. Teil E: BWW-10 (Hero-Illustration der Kursseiten mit festem Seitenverhaeltnis 419:284) und BWW-21 (Teil: doppelte, ueberlagerte .pathway-grid-Altregeln Z.188 und Z.219 entfernt). Idempotent; ?v-Token neu."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'assets/styles.css'; s = open(f, encoding='utf8').read()
A = '.pathway-grid{width:min(1180px,calc(100% - 36px));margin:auto;display:grid;grid-template-columns:1.15fr 1fr 1fr;gap:18px}\n'
B = '  .pathway-grid{grid-template-columns:1fr}\n  .path-card.big{grid-row:auto;min-height:360px}'
if A in s:
    assert s.count(A) == 1 and s.count(B) == 1
    s = s.replace(A, '').replace(B, '  .path-card.big{grid-row:auto;min-height:360px}')
M = '/* BWW-10 */'
if M not in s:
    s += '\n' + M + '\nhtml:root:root:root body main .page-hero>.bww-ill{height:auto!important;aspect-ratio:419/284;object-fit:contain}\n'
open(f, 'w', encoding='utf8').write(s)
c = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8]; m = 0
pat = re.compile(r'(assets/styles\.css\?v=)[0-9a-zA-Z]+')
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = pat.sub(lambda x: x.group(1) + c, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); m += 1
print('styles.css', c, m)
