#!/usr/bin/env python3
"""/zertifikat-duplikat/: Layout (kein Text): Haekchen neben seinem Text statt darueber (.tool-card label = Spalte ueberschrieb die Zeile), Button-Zeile wie .bww-form (Hinweis umfliesst den Button nicht). Idempotent, ?v-Token neu."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'assets/styles.css'; s = open(f, encoding='utf8').read(); M = '/* zd-Layout 13.11. */'
if M not in s:
    s += '\n' + M + '\nhtml:root:root:root body #zd-form .consent{flex-direction:row;align-items:flex-start;gap:.7rem}\nhtml:root:root:root body #zd-form .consent input{margin-top:.1rem}\nhtml:root:root:root body #zd-form .form-actions{margin-top:1.4rem;display:flex;align-items:center;gap:1rem;flex-wrap:wrap}\n'
    open(f, 'w', encoding='utf8').write(s)
c = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8]; m = 0
pat = re.compile(r'(assets/styles\.css\?v=)[0-9a-zA-Z]+')
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = pat.sub(lambda x: x.group(1) + c, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); m += 1
print('styles.css', c, m)
