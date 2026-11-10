#!/usr/bin/env python3
"""Design 10.11. Teil A (BL-Auftrag BWWChat.md), nur Quelltext, idempotent, Texte unveraendert:
BWW-02 (Waisenkarten: stimmen-grid 4 -> 2x2, course-grid.large mit 5 Karten 3+2 mittig), BWW-06 (Kartentitel ohne Silbentrennung, fluide Groesse),
BWW-09 (Pfeil mit geschuetztem Leerzeichen), BWW-16 (:active mit Eindrueckung), BWW-17 (Kill-Switch Reduced Motion entfernt, .01ms-Netz bleibt),
BWW-18 (ein Fokusring 2 px). ?v-Token fuer styles.css / bewertungen.css neu."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
def rw(f, fn):
    s = open(f, encoding='utf8').read(); t = fn(s)
    if t != s: open(f, 'w', encoding='utf8').write(t)
    return t
MARK = '/* Design 10.11. Teil A */'
def css(s):
    if MARK in s: return s
    # BWW-17: Kill-Switch entfernen
    k = '@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}'
    assert s.count(k) == 1; s = s.replace(k, '')
    # BWW-16: :active mit Eindrueckung
    a = 'html:root :is(.btn.primary,.sticky-book a,.text-link,.termin-cta):active{transform:none!important}'
    assert s.count(a) == 1
    s = s.replace(a, 'html:root :is(.btn,.nav-cta,.sticky-book a,.text-link,.termin-cta):active{transform:scale(.97)!important;transition-duration:90ms!important}')
    # BWW-18: ein Fokusring (2 px)
    f = 'input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid var(--ad-accent,#25704e);outline-offset:2px;border-radius:8px}'
    assert s.count(f) == 1; s = s.replace(f, f.replace('outline:3px', 'outline:2px'))
    s += '''
''' + MARK + '''
/* BWW-02: fuenf Kurskarten 3+2 mittig statt 4+1 (ab 1181 px), zwei Spalten: letzte Karte mittig */
@media(min-width:1181px){html:root:root:root .course-grid.large:has(>:nth-child(5):last-child){grid-template-columns:repeat(6,minmax(0,1fr))}
html:root:root:root .course-grid.large:has(>:nth-child(5):last-child)>*{grid-column:span 2}
html:root:root:root .course-grid.large:has(>:nth-child(5):last-child)>:nth-child(4){grid-column:2/span 2}
html:root:root:root .course-grid.large:has(>:nth-child(5):last-child)>:nth-child(5){grid-column:4/span 2}}
@media(min-width:601px) and (max-width:1180px){html:root:root:root .course-grid.large>:last-child:nth-child(odd){grid-column:1/-1;justify-self:center;width:calc(50% - .55rem)}}
/* BWW-06: Kartentitel ohne automatische Silbentrennung, fluide Groesse */
html:root:root:root body main .course-card h3{hyphens:manual;font-size:clamp(1.05rem,1.6vw,1.25rem);overflow-wrap:normal}
'''
    return s
rw('assets/styles.css', css)
def stimmen(s):
    if '4 Stimmen' in s: return s
    return s + '''/* 4 Stimmen: 2x2 statt 3+1 (Design 10.11., BWW-02) */
@media(min-width:901px){.stimmen-grid:has(>:nth-child(4):last-child){grid-template-columns:repeat(2,minmax(0,1fr));max-width:760px}}
'''
rw('assets/bewertungen.css', stimmen)
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    rw(p, lambda s: s.replace('freie Termine ansehen →', 'freie Termine ansehen&nbsp;→'))
def tok(f):
    t = hashlib.sha1(open(f, 'rb').read()).hexdigest()[:8]; n = 0
    pat = re.compile(r'(assets/' + re.escape(os.path.basename(f)) + r'\?v=)[0-9a-zA-Z]+')
    for p in glob.glob('**/*.html', recursive=True):
        if p.startswith('tools/'): continue
        h = open(p, encoding='utf8').read(); h2 = pat.sub(lambda m: m.group(1) + t, h)
        if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
    print(f, t, n)
tok('assets/styles.css'); tok('assets/bewertungen.css')
