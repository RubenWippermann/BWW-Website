#!/usr/bin/env python3
"""Zielgroesse (WCAG 2.2 SC 2.5.8): Checkboxen/Radios mindestens 24x24 px. Nur Groesse der Eingabe und die zugehoerige Grid-Spalte (22 -> 24 px); Texte, Farben, Abstaende sonst unveraendert. Idempotent, ?v-Token neu."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'assets/styles.css'; s = open(f, encoding='utf8').read(); M = '/* Zielgroesse 13.11. */'
if M not in s:
    s += '\n' + M + '\nhtml:root:root:root body input[type=checkbox],html:root:root:root body input[type=radio]{width:24px!important;height:24px!important;min-width:24px;min-height:24px;flex:0 0 24px}\nhtml:root:root:root body .bww-form .checks label{grid-template-columns:24px 1fr}\n'
    open(f, 'w', encoding='utf8').write(s)
c = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8]; m = 0
pat = re.compile(r'(assets/styles\.css\?v=)[0-9a-zA-Z]+')
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = pat.sub(lambda x: x.group(1) + c, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); m += 1
print('styles.css', c, m)
