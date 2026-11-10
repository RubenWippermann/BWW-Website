#!/usr/bin/env python3
"""BWW-11: Dunkelmodus: Negativ-Logo (marken.ts logoNegativ = /brands/negativ/bww.png) statt weissem Kasten um das dunkelgruene Logo.
Header- und Footer-Logo werden in <picture> mit prefers-color-scheme:dark-Quelle gesetzt; weisser Traeger im Dunkelmodus entfaellt. Idempotent."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
SRC = '/Users/rubenwippermannn/Claude/kn-wt/public/brands/negativ/bww.png'
if not os.path.exists('media/bww-logo-negativ.webp'):
    from PIL import Image
    im = Image.open(SRC).convert('RGBA'); im = im.resize((640, round(640 * im.height / im.width)), Image.LANCZOS)
    im.save('media/bww-logo-negativ.webp', 'WEBP', quality=90, method=6)
SRCSET = '<source media="(prefers-color-scheme: dark)" srcset="/media/bww-logo-negativ.webp">'
IMGS = ['<img src="/media/bww-logo-transparent.webp" width="1744" height="738" alt="BWW UG (haftungsbeschränkt)">',
        '<img class="footer-logo" src="/media/bww-logo-transparent.webp" width="1744" height="738" alt="BWW Logo">']
n = 0
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = h
    for i in IMGS:
        if '<picture>' + SRCSET + i in h2: continue
        h2 = h2.replace(i, '<picture>' + SRCSET + i + '</picture>')
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
print('Seiten mit Logo-Picture:', n)
f = 'assets/styles.css'; s = open(f, encoding='utf8').read()
MARK = '/* BWW-11 */'
if MARK not in s:
    s += '\n' + MARK + '\n@media (prefers-color-scheme: dark){html:root:root:root body .site-header .brand img,html:root:root:root body .site-footer .footer-logo{background:transparent;border-radius:0;padding:0}}\n'
    open(f, 'w', encoding='utf8').write(s)
c = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8]; m = 0
pat = re.compile(r'(assets/styles\.css\?v=)[0-9a-zA-Z]+')
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = pat.sub(lambda x: x.group(1) + c, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); m += 1
print('styles.css', c, m)
