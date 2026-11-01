#!/usr/bin/env python3
"""Schritt B (SEO 01.11.): Anfragen auf Position 8-20 gezielt ausbauen. Idempotent; nur Fakten, die auf BWW-Wissensseiten stehen."""
import re, json, os, sys
root = sys.argv[1] if len(sys.argv) > 1 else '.'
def rd(p): return open(os.path.join(root, p, 'index.html'), encoding='utf8').read()
def wr(p, h): open(os.path.join(root, p, 'index.html'), 'w', encoding='utf8').write(h)
def esc(s): return s.replace('&', '&amp;')
n = 0

def add_faq(h, items, anchor_html):
    """items=[(frage,antwort)]; sichtbar vor anchor_html und im FAQPage-JSON-LD."""
    for q, a in items:
        if f'<h3>{esc(q)}</h3>' in h: continue
        h = h.replace(anchor_html, f'<h3>{esc(q)}</h3><p>{esc(a)}</p>' + anchor_html, 1)
        m = [x for x in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S) if '"FAQPage"' in x.group(1)][0]
        j = json.loads(m.group(1)); j['mainEntity'].append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        h = h.replace(m.group(1), json.dumps(j, ensure_ascii=False, separators=(',', ':')), 1)
    return h

# 1) Rettungskette: Anfrage "rettungskette 5 schritte"
p = 'wissen/rettungskette/'; h = rd(p); o = h
h = add_faq(h, [("Wie lauten die 5 Schritte der Rettungskette?",
   "Die Rettungskette besteht aus fünf Gliedern: 1. Sofortmaßnahmen und Eigenschutz, 2. Notruf 112, 3. Erste Hilfe durch Anwesende, 4. Rettungsdienst, 5. Krankenhaus. Die ersten drei Glieder liegen in den Händen von Laien."),
   ("Wer gehört zur Rettungskette?",
   "Ersthelfende und Anwesende am Notfallort, die Leitstelle über den Notruf 112, der Rettungsdienst und das Krankenhaus.")],
   '<p class="article-related">')
if h != o: wr(p, h); n += 1

# 2) Notruf-Simulator: Inhalt + FAQ + FAQPage-Schema (Anfrage "notruf simulator")
p = 'notruf-simulator/'; h = rd(p); o = h
if 'id="simulator-faq"' not in h:
    faq = [("Was ist der Notruf-Simulator?", "Eine kostenlose Übung ohne Anmeldung: Ihr spielt einen Notruf an die Leitstelle durch, könnt sprechen oder tippen und bekommt am Ende eine Auswertung der 5 W-Fragen."),
           ("Was sind die 5 W-Fragen beim Notruf?", "Wo ist der Notfallort, was ist passiert, wie viele Betroffene gibt es, welche Verletzungen oder Symptome liegen vor, und warten auf Rückfragen der Leitstelle."),
           ("Ist der Simulator ein echter Notruf?", "Nein, es ist eine Übung. Im echten Notfall wählt ihr sofort die 112. Der Notruf ist immer kostenlos."),
           ("Für wen gibt es den Kindermodus?", "Im Kindermodus übt ein Kind den Notruf. Erwachsene starten den Modus für Erwachsene.")]
    qa = ''.join(f'<h3>{esc(q)}</h3><p>{esc(a)}</p>' for q, a in faq)
    sec = ('<section class="section" id="simulator-faq"><h2>Häufige Fragen zum Notruf-Simulator</h2>' + qa +
           '<p class="small-note">Dies ist eine Übung. Im echten Notfall: Notruf 112.</p>'
           '<p class="article-related"><a href="/wissen/notruf-112/">Notruf 112: die 5 W-Fragen</a><a href="/wissen/rettungskette/">Rettungskette</a>'
           '<a href="/wissen/reanimation/">Reanimation</a><a href="/kurse/erste-hilfe-ausbildung/">Erste-Hilfe-Ausbildung</a></p></section>')
    h = h.replace('</main>', sec + '</main>', 1)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    h = h.replace('</head>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + '</script></head>', 1)
    wr(p, h); n += 1

# 3) interne Links (>= 3 thematisch passende Seiten je Zielseite)
LINKS = {
 'wissen/kosten-rettungsdienst-krankenwagen': ('Kosten Rettungsdienst', ['wissen/notruf-112', 'wissen/rettungskette', 'wissen/fahrzeuge-rettungsdienst', 'wissen/reanimation']),
 'wissen/erste-hilfe-teilnahmebescheinigung': ('Erste-Hilfe-Bescheinigung', ['wissen/erste-hilfe-kurs-gueltigkeit', 'wissen/erste-hilfe-fuehrerschein', 'wissen/erste-hilfe-kurs-inhalte', 'wissen/erste-hilfe-bescheinigung-verloren-duplikat']),
 'wissen/erste-hilfe-kurs-inhalte': ('Erste-Hilfe-Kurs: Inhalte', ['wissen/erste-hilfe-fuehrerschein', 'wissen/erste-hilfe-kurs-gueltigkeit', 'wissen/erste-hilfe-teilnahmebescheinigung']),
 'notruf-simulator': ('Notruf-Simulator', ['wissen/notruf-112', 'wissen/rettungskette', 'wissen/reanimation']),
}
for tgt, (label, srcs) in LINKS.items():
    a = f'<a href="/{tgt}/">{esc(label)}</a>'
    for s in srcs:
        if s == tgt: continue
        h = rd(s + '/'); 
        if f'href="/{tgt}/"' in h.split('<footer')[0]: continue
        m = re.search(r'<p class="article-related">(.*?)</p>', h, re.S)
        if not m: print('KEIN article-related:', s); continue
        h = h.replace(m.group(0), m.group(0).replace('</p>', a + '</p>'), 1); wr(s + '/', h); n += 1
print('geändert:', n)
