#!/usr/bin/env python3
"""Design 10.11. Teil B (BWW-01, 03, 04, 05, 08): Raster ohne Waisenkarte, einheitliche Breite/Kante/Abstand, Abschnittskopf, Brotkrumen/Nav-Hoehe. Idempotent, Texte unveraendert. ?v-Token styles.css neu."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
MARK = '/* Design 10.11. Teil B */'
f = 'assets/styles.css'; s = open(f, encoding='utf8').read()
if MARK not in s:
    s += '''
''' + MARK + '''
/* BWW-04/05: alle Raster auf eine Breite (--wrap) und einen Abstand */
:root{--wrap:min(1120px,100%);--grid-gap:18px}
html:root:root:root body main :is(.pathway-grid,.path-grid,.feature-grid,.tools-grid,.course-grid,.knowledge-grid,.stimmen-grid,.format-chips,.anerkennung-grid){width:var(--wrap)!important;max-width:none!important;margin-left:auto!important;margin-right:auto!important;gap:var(--grid-gap)!important}
/* BWW-01: fuenf Karten 3+2 mittig, vier Karten 2x2 (ab 1000 px), 16 Chips 4x4 */
@media(min-width:1181px){
html:root:root:root body main .pathway-grid.five{grid-template-columns:repeat(6,minmax(0,1fr))!important;overflow:visible!important}
html:root:root:root body main .pathway-grid.five>*{grid-column:span 2!important;min-width:0}
html:root:root:root body main .pathway-grid.five>:nth-child(4){grid-column:2/span 2!important}
html:root:root:root body main .pathway-grid.five>:nth-child(5){grid-column:4/span 2!important}}
@media(min-width:1000px){html:root:root:root body main .pathway-grid:not(.five):has(>:nth-child(4):last-child){grid-template-columns:repeat(2,minmax(0,1fr))!important}
html:root:root:root body main .format-chips:has(>:nth-child(16):last-child){grid-template-columns:repeat(4,minmax(0,1fr))!important}}
@media(min-width:480px) and (max-width:999px){html:root:root:root body main .format-chips:has(>:nth-child(16):last-child){grid-template-columns:repeat(2,minmax(0,1fr))!important}}
@media(min-width:901px){html:root:root:root body main .stimmen-grid:has(>:nth-child(4):last-child){grid-template-columns:repeat(2,minmax(0,1fr))!important}}
/* BWW-03: linksbuendige Abschnittskoepfe, Absatz an der Kante der Ueberschrift; zentrierte Koepfe bleiben zentriert */
html:root:root:root body main .section-head:not(.center):not(.section.compact .section-head):not(.tools-highlight .section-head):not(.sustainability .section-head){text-align:left!important}
html:root:root:root body main .section-head:not(.center):not(.section.compact .section-head):not(.tools-highlight .section-head):not(.sustainability .section-head)>:is(.eyebrow,h2,p){margin-left:0!important;margin-right:auto!important;text-align:left!important}
/* BWW-03: zentrierte Koepfe (Werkzeuge, Nachhaltigkeit, kompakt): Absatz zentriert wie die Ueberschrift */
html:root:root:root body main :is(.tools-highlight,.sustainability,.section.compact,.center) .section-head p{margin-left:auto!important;margin-right:auto!important;text-align:center!important}
/* BWW-04: Heroes (Start und Kursseiten) beginnen an derselben Kante wie Abschnittskoepfe und Raster */
html:root:root:root body main :is(.hero.apple-hero,.page-hero){padding-left:max(18px,calc((100% - 1120px)/2))!important;padding-right:max(18px,calc((100% - 1120px)/2))!important}
/* BWW-08: Brotkrumen und Navigation mindestens 44 px, Navigation einheitlich hoch, Tagline lesbar */
html:root:root:root body .crumb a{display:inline-flex;align-items:center;min-height:44px;min-width:44px;padding:0 .35rem}
html:root:root:root body .site-header nav a{display:inline-flex;align-items:center;min-height:46px}
@media(max-width:480px){html:root:root:root body .site-header .brand small{font-size:.75rem!important}}
'''
    open(f, 'w', encoding='utf8').write(s)
# Teil A: max-width 760 des 2x2-Stimmenrasters entfaellt (Kante = --wrap)
b = 'assets/bewertungen.css'; t = open(b, encoding='utf8').read()
t2 = t.replace('grid-template-columns:repeat(2,minmax(0,1fr));max-width:760px}', 'grid-template-columns:repeat(2,minmax(0,1fr))}')
if t2 != t: open(b, 'w', encoding='utf8').write(t2)
def tok(fn):
    c = hashlib.sha1(open(fn, 'rb').read()).hexdigest()[:8]; n = 0
    pat = re.compile(r'(assets/' + re.escape(os.path.basename(fn)) + r'\?v=)[0-9a-zA-Z]+')
    for p in glob.glob('**/*.html', recursive=True):
        if p.startswith('tools/'): continue
        h = open(p, encoding='utf8').read(); h2 = pat.sub(lambda m: m.group(1) + c, h)
        if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
    print(fn, c, n)
tok('assets/styles.css'); tok('assets/bewertungen.css')
