#!/usr/bin/env python3
"""Keine Frist-Zusage ('innerhalb eines Werktags', § 5 UWG, BL 02.11.): sitewide neutral 'Wir melden uns bei dir.' bzw. entfernt. Rechtsseiten werden nicht angefasst. Idempotent."""
import glob, re, json
R = [('Wir melden uns i.&nbsp;d.&nbsp;R. innerhalb eines Werktags.', 'Wir melden uns bei dir.'),
     ('wir melden uns in der Regel innerhalb eines Werktags.', 'wir melden uns bei dir.'),
     ('Wir melden uns in der Regel innerhalb eines Werktags mit Terminvorschlag und Angebot.', 'Wir melden uns mit Terminvorschlag und Angebot.'),
     ('Wir bestätigen dir den Eingang – i.&nbsp;d.&nbsp;R. innerhalb eines Werktags.', 'Wir bestätigen dir den Eingang.')]
KONTAKT = [(' Wir melden uns in der Regel innerhalb eines Werktags.</p></div><img', '</p></div><img'),
           ('<span class="form-hint">Wir melden uns i.&nbsp;d.&nbsp;R. innerhalb eines Werktags.</span>', '')]   # /kontakt/: Zusage gestrichen (BL-Auflage)
FAQQ = 'Wie schnell melden wir uns nach einer Anfrage?'
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['404.html']:
    if f.startswith(('agb/', 'datenschutz/', 'impressum/', 'widerruf/')): continue
    h = open(f, encoding='utf8').read(); o = h
    if f == 'kontakt/index.html':
        for a, b in KONTAKT: h = h.replace(a, b)
    for a, b in R: h = h.replace(a, b)
    if f == 'inhouse-kurse/index.html' and FAQQ in h:
        h = re.sub(r'<h3>' + re.escape(FAQQ) + r'</h3><p>.*?</p>', '', h, count=1, flags=re.S)
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            if '"FAQPage"' in m.group(1):
                j = json.loads(m.group(1)); j['mainEntity'] = [q for q in j['mainEntity'] if q['name'] != FAQQ]
                h = h.replace(m.group(1), json.dumps(j, ensure_ascii=False, separators=(',', ':')), 1)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
print('geändert:', n)
