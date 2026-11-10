#!/usr/bin/env python3
"""Design 10.11. Teil C (BWW-12 bis 15), idempotent, nur Bewegung, Texte unveraendert.
12: Abschnitts-Reveal entfernt, Karten nur noch ueber fx-pre (a2-scroll entfernt, fx.js-Auswahl um course-card/tool-tile/anerkennung-card erweitert)
13: Keimen/Wald/Ranke/Triebe/Karteneinzug kuerzer, ohne Ueberschwingen
14: Lichtkegel als verschobene Flaeche (transform), Rechteck zwischengespeichert, requestAnimationFrame
15: Tilt/Glare/Magnet entfernt (durch !important der Design-Schicht ohnehin wirkungslos, gemessen)"""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
def sub(s, a, b, n=1):
    assert s.count(a) == n, (a[:60], s.count(a)); return s.replace(a, b)
# ---- styles.css
f = 'assets/styles.css'; s = open(f, encoding='utf8').read()
if 'html.reveal-on main .section,html.reveal-on main .section-soft{transform:translateY(18px)' in s:
    s = sub(s, 'html.reveal-on main .section,html.reveal-on main .section-soft{transform:translateY(18px);transition:transform .7s ease}\n', '')
    s = sub(s, 'html.reveal-on main .section.is-visible,html.reveal-on main .section-soft.is-visible{transform:none}\n', '')
    s = sub(s, '  @keyframes a2-scroll{from{transform:translateY(18px)}to{transform:none}}\n', '')
    s = re.sub(r'    html\.a3-ready main :is\(\.course-card,\.tool-tile,\.anerkennung-card\)(?::nth-child\(4n\+\d\))?\{animation(?:-range)?:[^}]*\}\n', '', s)
    assert 'a2-scroll' not in s
    open(f, 'w', encoding='utf8').write(s)
# BWW-16 Nachbesserung: :active muss die Spezifitaet der :hover-Regel (.btn.primary) erreichen, sonst bleibt hover (-1px) gewinnen
s = open('assets/styles.css', encoding='utf8').read()
a16 = 'html:root :is(.btn,.nav-cta,.sticky-book a,.text-link,.termin-cta):active{'
if a16 in s:
    open('assets/styles.css', 'w', encoding='utf8').write(s.replace(a16, 'html:root :is(.btn.primary,.btn,.nav-cta,.sticky-book a,.text-link,.termin-cta):active{'))
# ---- fx.css
f = 'assets/fx.css'; s = open(f, encoding='utf8').read()
if '.fx-tilt' in s:
    s = sub(s, 'animation: fx-draw 2.4s cubic-bezier(.5,0,.2,1) .4s forwards;', 'animation: fx-draw 1.2s cubic-bezier(.5,0,.2,1) .3s forwards;')
    s = sub(s, 'animation: fx-leaf 700ms cubic-bezier(.3,1.5,.5,1) forwards; animation-delay: calc(900ms + var(--k) * 260ms);', 'animation: fx-leaf 400ms cubic-bezier(.16,1,.3,1) forwards; animation-delay: calc(500ms + var(--k) * 140ms);')
    s = sub(s, 'transition: transform 900ms cubic-bezier(.16,1,.3,1) 150ms; pointer-events: none; }', 'transition: transform 400ms cubic-bezier(.16,1,.3,1) 100ms; pointer-events: none; }')
    s = sub(s, '.fx-pre { transform: translate3d(0, 26px, 0) scale(.98); }', '.fx-pre { transform: translate3d(0, 14px, 0); }')
    s = sub(s, '.fx-pre.fx-in { transform: none; transition: transform 900ms cubic-bezier(.16,1,.3,1) var(--d, 0ms); }', '.fx-pre.fx-in { transform: none; transition: transform 400ms cubic-bezier(.16,1,.3,1) var(--d, 0ms); }')
    s = sub(s, '.fx-sprout.is-in svg { transform: none; transition: transform 900ms cubic-bezier(.3,1.6,.5,1) var(--d, 0ms); }', '.fx-sprout.is-in svg { transform: none; transition: transform 350ms cubic-bezier(.16,1,.3,1) var(--d, 0ms); }')
    s = sub(s, 'transition: transform 1000ms cubic-bezier(.3,1.4,.5,1) calc(var(--k) * 200ms); }', 'transition: transform 400ms cubic-bezier(.16,1,.3,1) calc(var(--k) * 100ms); }')
    # Lichtkegel als Flaeche
    s = re.sub(r'  \.fx-spot \{ position: absolute; inset: 0; pointer-events: none; opacity: 0; transition: opacity 500ms ease;\n    background: radial-gradient\(480px circle at var\(--sx, 60%\) var\(--sy, 40%\), rgba\(139,207,115,\.34\), rgba\(139,207,115,0\) 62%\); \}\n  \.page-hero\.fx-hero \.fx-spot \{ background: radial-gradient\(480px circle at var\(--sx, 60%\) var\(--sy, 40%\), rgba\(139,207,115,\.30\), rgba\(139,207,115,0\) 62%\); mix-blend-mode: screen; \}\n',
      '  .fx-spot { position: absolute; left: 0; top: 0; width: 960px; height: 960px; margin: -480px 0 0 -480px; pointer-events: none; opacity: 0; transition: opacity 400ms ease;\n    transform: translate3d(var(--sx, 0px), var(--sy, 0px), 0); will-change: transform;\n    background: radial-gradient(closest-side, rgba(139,207,115,.34), rgba(139,207,115,0) 62%); }\n  .page-hero.fx-hero .fx-spot { background: radial-gradient(closest-side, rgba(139,207,115,.30), rgba(139,207,115,0) 62%); mix-blend-mode: screen; }\n', s)
    assert 'closest-side, rgba(139,207,115,.34)' in s
    # Tilt/Glare/Magnet entfernen
    a = s.index('  /* Karten: Einzug gestaffelt, 3D-Neigung'); b = s.index('  .fx-pre { transform')
    s = s[:a] + '  /* Karten: Einzug gestaffelt */\n' + s[b:]
    a = s.index('  .fx-tilt { position: relative; }'); b = s.index('  /* Wachstum:')
    s = s[:a] + '\n' + s[b:]
    s = sub(s, '.fx-spot, .fx-glare { display: none !important; }', '.fx-spot { display: none !important; }')
    assert '.fx-tilt' not in s and '.fx-mag' not in s and '.fx-glare' not in s
    open(f, 'w', encoding='utf8').write(s)
# ---- fx.js
f = 'assets/fx.js'; s = open(f, encoding='utf8').read()
if 'fx-tilt' in s:
    s = sub(s, '"main .path-card, main .feature-card, main .sustain-card"', '"main .path-card, main .feature-card, main .sustain-card, main .course-card, main .tool-tile, main .anerkennung-card"')
    old = s[s.index('    if (spot) {\n      hero.addEventListener("pointermove"'):s.index('  /* Abschnittsköpfe: Trieb-Linie')]
    new = '''    if (spot) {
      var hr = null, ex = 0, ey = 0, pend = false;
      function inval() { hr = null; }
      window.addEventListener("scroll", inval, { passive: true });
      window.addEventListener("resize", inval);
      hero.addEventListener("pointermove", function (e) {
        ex = e.clientX; ey = e.clientY;
        hero.classList.add("fx-hot");
        if (pend) return;
        pend = true;
        raf(function () {
          pend = false;
          if (!hr) hr = hero.getBoundingClientRect();
          spot.style.setProperty("--sx", (ex - hr.left) + "px");
          spot.style.setProperty("--sy", (ey - hr.top) + "px");
        });
      }, { passive: true });
      hero.addEventListener("pointerleave", function () { hero.classList.remove("fx-hot"); });
    }
  }

'''
    s = s.replace(old, new, 1)
    a = s.index('  if (!fine) return;'); b = s.rindex('})();')
    s = s[:a].rstrip() + '\n' + s[b:]
    open(f, 'w', encoding='utf8').write(s)
def tok(fn):
    c = hashlib.sha1(open(fn, 'rb').read()).hexdigest()[:8]; n = 0
    pat = re.compile(r'(assets/' + re.escape(os.path.basename(fn)) + r'\?v=)[0-9a-zA-Z]+')
    for p in glob.glob('**/*.html', recursive=True):
        if p.startswith('tools/'): continue
        h = open(p, encoding='utf8').read(); h2 = pat.sub(lambda m: m.group(1) + c, h)
        if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
    print(fn, c, n)
for fn in ('assets/styles.css', 'assets/fx.css', 'assets/fx.js'): tok(fn)
