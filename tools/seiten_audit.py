#!/usr/bin/env python3
"""Seiten-Audit der 10 wichtigsten BWW-Seiten (nur Quelltext): Titel/Desc/H1/Wörter/H2/interne Links/Schema/Keyword. Ausgabe Markdown-Tabelle + Funde."""
import re, html, json, sys
PAGES = {  # Seite: Hauptbegriff, Nebenbegriffe
 '': ('erste hilfe kurs inhouse', ['brandschutz', 'betrieb']), 'kurse/': ('erste hilfe kurs', ['brandschutzhelfer', 'betriebssanitäter']),
 'fuer-sanitaetsdienst/': ('betriebssanitäter', ['grundkurs', 'sanitätsdienst']), 'kurse/betriebssanitaeter-grundkurs/': ('betriebssanitäter grundkurs', ['63 ue', 'prüfung']),
 'kurse/brandschutzhelfer/': ('brandschutzhelfer', ['asr a2.2', 'ausbildung']), 'fuer-ausbilder/': ('ausbilder werden', ['lehrkraft', 'lehrbeauftragte']),
 'ausbilder-werden/lehrbeauftragter/': ('lehrbeauftragte', ['hospitation', '304-003']), 'kontakt/': ('kontakt', ['telefon', 'inhouse']),
 'kurse/erste-hilfe-ausbildung/': ('erste-hilfe-ausbildung', ['ersthelfer', 'inhouse']), 'inhouse-kurse/': ('inhouse', ['erste hilfe', 'brandschutz']),
}
res = []
for p, (kw, extra) in PAGES.items():
    h = open(p + 'index.html', encoding='utf8').read()
    t = html.unescape(re.search(r'<title>(.*?)</title>', h, re.S).group(1)); d = html.unescape((re.search(r'name="description" content="(.*?)"', h) or [0, ''])[1])
    m = re.search(r'<main.*?</main>', h, re.S); main = m.group(0) if m else h
    body = re.sub(r'<script.*?</script>|<style.*?</style>|<svg.*?</svg>', '', main, flags=re.S)
    text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', body))).strip()
    h1 = [re.sub('<[^>]+>', '', x) for x in re.findall(r'<h1[^>]*>(.*?)</h1>', main, re.S)]
    h2 = [re.sub('<[^>]+>', '', x) for x in re.findall(r'<h2[^>]*>(.*?)</h2>', main, re.S)]
    links = re.findall(r'<a\b[^>]*href="(/[^"#]*)', main)
    ld = []
    for x in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: j = json.loads(x.group(1)); ld.append(j.get('@type') if isinstance(j, dict) else 'list')
        except Exception: ld.append('PARSE-FEHLER')
    low = text.lower(); first = low[:600]
    k = kw.lower()
    res.append(dict(p=p or '/', tl=len(t), dl=len(d), h1=len(h1), h1t=h1[:1], words=len(text.split()), h2=len(h2), links=len(links), ulinks=len(set(links)), ld=[str(x) for x in ld], kw_t=k in t.lower(), kw_h1=any(k in x.lower() for x in h1), kw_first=k in first, kw_n=low.count(k),
                    extra=[(e, low.count(e)) for e in extra], rating='aggregateRating' in h.lower(), faq='FAQPage' in str(ld), title=t, desc=d))
print('| Seite | Title | Desc | H1 | Wörter | H2 | Links (eindeutig) | Schema | Keyword „Hauptbegriff“ in Title/H1/Anfang/gesamt | AggregateRating |')
print('|---|---|---|---|---|---|---|---|---|---|')
for r in res:
    print(f"| {r['p']} | {r['tl']} | {r['dl']} | {r['h1']} | {r['words']} | {r['h2']} | {r['links']} ({r['ulinks']}) | {','.join(sorted(set(r['ld'])))[:60]} | {'ja' if r['kw_t'] else 'nein'}/{'ja' if r['kw_h1'] else 'nein'}/{'ja' if r['kw_first'] else 'nein'}/{r['kw_n']} | {'JA' if r['rating'] else 'nein'} |")
print()
for r in res: print(r['p'], '|', r['title'], '|', r['h1t'])
