#!/usr/bin/env python3
"""/wissen/rettungskette/: dreifach wiederholte FAQ-Antwort zu den Gliedern bereinigen (HTML + FAQPage-JSON-LD). Idempotent."""
import json, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'wissen/rettungskette/index.html'; h = open(f, encoding='utf8').read()
K = 'Das hängt von der Quelle ab: Die DGUV Information 204-022 beschreibt Laienhilfe, Rettungsdienst und Krankenhaus, das DRK nennt vier Glieder. In der Darstellung von BWW: '
def zaehle(t):
    faq = t[t.find('<h2>Häufige Fragen'):]; faq = faq[:faq.find('<p class="article-related">')]
    ld = [x for x in (json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S)) if x['@type'] == 'FAQPage'][0]
    return {'HTML-Fragen': faq.count('<h3>'), 'JSON-LD-Fragen': len(ld['mainEntity']), 'Wiederholungen HTML': t.count(K), 'Satz je Frage in JSON-LD': sum(q['acceptedAnswer']['text'].count(K) for q in ld['mainEntity'])}
print('vorher ', zaehle(h))
while K * 2 in h: h = h.replace(K * 2, K)
open(f, 'w', encoding='utf8').write(h); print('nachher', zaehle(h))
