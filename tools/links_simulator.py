#!/usr/bin/env python3
"""Reihe C (Sichtsbarkeit, 01.11.): interne Verlinkung auf /notruf-simulator/ mit sprechendem Ankertext aus passenden Fließtext-Absätzen (6 Stellen, keine Linkblöcke). Idempotent."""
S = [  # (Datei, Absatz-Ende alt, neu)
 ('wissen/notruf-112/index.html', 'Dabei helfen die <strong>5 W-Fragen</strong>.</p>', 'Dabei helfen die <strong>5 W-Fragen</strong>. Den Ablauf könnt ihr kostenlos im <a href="/notruf-simulator/">Notruf-Simulator durchspielen</a>.</p>'),
 ('wissen/rettungskette/index.html', 'und auf Rückfragen zu warten.</p>', 'und auf Rückfragen zu warten. Das Gespräch mit der Leitstelle lässt sich im <a href="/notruf-simulator/">Notruf-Simulator üben</a>.</p>'),
 ('wissen/erste-hilfe-kurs-inhalte/index.html', 'sowie das Erkennen von Herzinfarkt und Schlaganfall.</p>', 'sowie das Erkennen von Herzinfarkt und Schlaganfall. Den Notruf könnt ihr vorab im <a href="/notruf-simulator/">Notruf-Simulator üben</a>.</p>'),
 ('wissen/reanimation/index.html', 'macht Handlungsschritte abrufbar.</p>', 'macht Handlungsschritte abrufbar. Den Anruf bei der 112 könnt ihr im <a href="/notruf-simulator/">Notruf-Simulator trainieren</a>.</p>'),
 ('wissen/kosten-rettungsdienst-krankenwagen/index.html', 'Niemand sollte den Notruf hinauszögern', 'Niemand sollte den Notruf hinauszögern'),  # Platzhalter, unten gezielt
 ('ausbilder-werden/fuer-betriebe/index.html', 'wie viele Ersthelfer ein Betrieb braucht, erklärt <a href="/wissen/ersthelfer-anzahl-dguv/">Wie viele Ersthelfer braucht ein Betrieb?</a></p>', 'wie viele Ersthelfer ein Betrieb braucht, erklärt <a href="/wissen/ersthelfer-anzahl-dguv/">Wie viele Ersthelfer braucht ein Betrieb?</a> Für die Praxis lässt sich der Notruf kostenlos im <a href="/notruf-simulator/">112-Notruf-Simulator üben</a>.</p>'),
]
n = 0
for f, a, b in S:
    if a == b: continue
    h = open(f, encoding='utf8').read()
    if b in h: continue
    if a not in h: print('FEHLT', f); continue
    open(f, 'w', encoding='utf8').write(h.replace(a, b, 1)); n += 1
# Kosten-Seite: Absatz zur 112 (FAQ-Antwort bleibt unverändert, nur Fließtext)
f = 'wissen/kosten-rettungsdienst-krankenwagen/index.html'; h = open(f, encoding='utf8').read()
a = 'Niemand sollte den Notruf hinauszögern, weil er Kosten fürchtet:'
if '/notruf-simulator/' not in h.split('<footer')[0].split('Häufige Fragen')[0] and a in h:
    i = h.find(a); j = h.find('</p>', i)
    seg = h[i:j]
    h = h[:j] + ' Den Anruf könnt ihr vorher im <a href="/notruf-simulator/">Notruf-Simulator üben</a>.' + h[j:]; open(f, 'w', encoding='utf8').write(h); n += 1
import glob
for f in glob.glob('**/index.html', recursive=True) + ['404.html']:
    try: h = open(f, encoding='utf8').read()
    except FileNotFoundError: continue
    if '>112-Simulator</a>' in h: open(f, 'w', encoding='utf8').write(h.replace('>112-Simulator</a>', '>Notruf-Simulator</a>')); n += 1   # Footer-Tools-Liste: sprechender Ankertext
print('geändert:', n)
