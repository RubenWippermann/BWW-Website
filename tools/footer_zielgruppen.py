#!/usr/bin/env python3
"""Footer-Zeile 'Für wen' mit den Zielgruppenseiten auf allen Seiten (idempotent). Standard: Trockenlauf; --apply schreibt."""
import glob, hashlib, os, re, sys
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
APPLY = '--apply' in sys.argv
LINKS = [('fuer-schulen', 'Schulen'), ('fuer-behoerden', 'Behörden'), ('fuer-pflege', 'Pflege'), ('fuer-kitas', 'Kitas'),
         ('fuer-sanitaetsdienst', 'Sanitätsdienst'), ('fuer-ausbilder', 'Ausbilder'), ('inhouse-kurse', 'Inhouse')]
ROW = ('<nav class="footer-zielgruppen" aria-label="Für wen"><span aria-hidden="true">Für wen:</span>' +
       ''.join(f'<a href="/{p}/">{t}</a>' for p, t in LINKS) + '</nav>')
CSS = '''
/* Footer-Zeile "Für wen" */
.site-footer .footer-zielgruppen{grid-column:1/-1;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:0 4px;border-top:1px solid rgba(127,127,127,.28);padding-top:12px;margin-top:4px}
.site-footer .footer-zielgruppen span{font-size:.875rem;font-weight:600;padding:0 8px}
.site-footer .footer-zielgruppen a{display:inline-flex;align-items:center;min-height:44px;padding:0 8px;margin:0}
'''
css = open('assets/styles.css', encoding='utf8').read()
if 'footer-zielgruppen' not in css:
    css += CSS
    if APPLY: open('assets/styles.css', 'w', encoding='utf8').write(css)
new_tok = hashlib.sha1(css.encode('utf8')).hexdigest()[:8]
files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('tools/')]
n_foot = n_tok = n_skip = 0
for f in files:
    h = open(f, encoding='utf8').read(); o = h
    if 'footer-zielgruppen' not in h and '</footer>' in h and 'class="site-footer"' in h:
        h = h.replace('</footer>', ROW + '</footer>', 1); n_foot += 1
    elif 'class="site-footer"' not in h: n_skip += 1
    h2 = re.sub(r'(/assets/styles\.css\?v=)[0-9a-f]{8}', lambda m: m.group(1) + new_tok, h)
    if h2 != h: n_tok += 1
    if APPLY and h2 != o: open(f, 'w', encoding='utf8').write(h2)
print(('ANGEWENDET' if APPLY else 'TROCKENLAUF'), '| Seiten', len(files), '| Footer-Zeile neu', n_foot, '| Token geändert', n_tok, '| ohne Footer', n_skip, '| neuer Token', new_tok)
