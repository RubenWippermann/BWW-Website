#!/usr/bin/env python3
"""Ratgeber-Artikel 'Betriebssanitäter werden' (idempotent). Basis: wissen/betriebssanitaeter-pflicht."""
import re, json, os, html
R = os.path.expanduser('~/Claude/bww-neu-wt'); os.chdir(R)
SLUG = 'wissen/betriebssanitaeter-werden-ablauf-voraussetzungen'
URL = 'https://www.multiplikatorenstelle.de/' + SLUG + '/'
TITLE = 'Betriebssanitäter werden: Ablauf und Voraussetzungen'
DESC = 'Betriebssanitäter werden: Grundlehrgang 63 UE, Aufbaulehrgang 32 UE, Fortbildung alle drei Jahre. Was die DGUV-Seiten zu Voraussetzungen sagen.'
H = '2026-11-02'
FAQ = [
 ('Wie lange dauert die Ausbildung zum Betriebssanitäter?',
  'Die DGUV nennt 63 Unterrichtseinheiten für den Grundlehrgang und 32 für den Aufbaulehrgang, zusammen 95. Rettungssanitäter steigen direkt mit dem Aufbaulehrgang ein.'),
 ('Wer darf Betriebssanitäter ausbilden?',
  'Die Ausbildung findet bei Stellen statt, die von den Unfallversicherungsträgern dafür als geeignet bewertet sind. Die öffentliche Liste führt die QSEH unter bg-qseh.de. Prüft dort den Eintrag, bevor ihr bucht.'),
 ('Wie oft muss ein Betriebssanitäter sich fortbilden?',
  'Spätestens alle drei Jahre. Die DGUV beschreibt dafür 16 Lerneinheiten.'),
]
BODY = f'''<p class="answer-lead"><strong>Direkt beantwortet:</strong> Wer Betriebssanitäter werden will, durchläuft zwei Lehrgänge: den Grundlehrgang mit 63 und den Aufbaulehrgang mit 32 Unterrichtseinheiten. Rettungssanitäter können nach den Angaben der DGUV direkt in den Aufbaulehrgang einsteigen. Danach ist alle drei Jahre eine Fortbildung fällig.</p>
<h2>Was Betriebssanitäter im Betrieb tun</h2>
<p>Betriebssanitäter leisten erweiterte Erste Hilfe. Sie gehen mit Geräten um, die über die Ausstattung eines Ersthelfers hinausgehen, etwa Beatmungsbeutel, Absaugpumpe und Sauerstoffgerät. Sie versorgen Verletzte und Erkrankte, bis der Rettungsdienst übernimmt, und sie ersetzen diesen nicht.</p>
<p>Ob ein Unternehmen überhaupt Betriebssanitäter stellen muss, regelt § 27 der DGUV Vorschrift 1. Die Schwellen und was dazwischen gilt, erklärt der Beitrag <a href="/wissen/betriebssanitaeter-pflicht/">Wann braucht ein Unternehmen Betriebssanitäter?</a>.</p>
<p>Die Zahl der Betriebssanitäter richtet sich nach der Betriebsgröße. Nach § 27 sind sie bei mehr als 1.500 anwesenden Versicherten vorgeschrieben. Bei mehr als 250 hängt es von Art, Schwere und Zahl der Unfälle ab, auf Baustellen gilt die Schwelle von mehr als 100 gleichzeitig Beschäftigten. Wer diese Schwellen erreicht, braucht also Personen, die den Weg unten gehen.</p>
<h2>Der Ablauf in drei Schritten</h2>
<h3>1. Grundlehrgang</h3>
<p>Der Grundlehrgang umfasst 63 Unterrichtseinheiten. Er steht am Anfang des Weges und wird bei einem Anbieter besucht, den die Unfallversicherungsträger als geeignet bewertet haben. Wer keine Vorbildung als Rettungssanitäter mitbringt, beginnt hier.</p>
<h3>2. Aufbaulehrgang</h3>
<p>Der Aufbaulehrgang schließt mit 32 Unterrichtseinheiten an. Rettungssanitäter können den Grundlehrgang überspringen und direkt hier beginnen. Das nennt die DGUV ausdrücklich.</p>
<h3>3. Fortbildung</h3>
<p>Die Fortbildung ist spätestens alle drei Jahre vorgesehen. Die DGUV beschreibt dafür 16 Lerneinheiten. Wer sie versäumt, sollte beim Anbieter und beim Unfallversicherungsträger klären, wie es weitergeht, bevor er wieder im betrieblichen Sanitätsdienst eingeteilt wird.</p>
<h2>Welche Voraussetzungen gibt es?</h2>
<p>Auf den Webseiten der DGUV zum Thema stehen keine formalen Zugangsvoraussetzungen für den Grundlehrgang. Genannt wird nur, dass sich zum Beispiel Sicherheitsbeauftragte für die Aufgabe bewerben können und dass der Betriebsarzt auf die besonderen Risiken des Betriebs vorbereitet. Mindestalter, Tauglichkeit oder bestimmte Vorqualifikationen nennen diese Seiten nicht.</p>
<p>Welche Nachweise ein Lehrgang verlangt, legt die Ausbildungsstelle fest. Lest dafür die Kursbeschreibung und fragt vor der Buchung nach. Das gilt auch, wenn ihr bereits eine Qualifikation aus dem Rettungsdienst habt und prüfen wollt, ob der Einstieg in den Aufbaulehrgang möglich ist.</p>
<h2>Wer sich dafür eignet</h2>
<p>Die DGUV beschreibt keinen festen Berufsweg zum Betriebssanitäter. Für Beschäftigte im Betrieb ist der Weg offen: Genannt werden etwa Sicherheitsbeauftragte, die sich für die Aufgabe bewerben können. Wer aus dem Rettungsdienst kommt, spart durch den direkten Einstieg in den Aufbaulehrgang den ersten Lehrgang. Auf die besonderen Risiken des eigenen Betriebs bereitet der Betriebsarzt vor.</p>
<h2>Wo die Ausbildung stattfindet</h2>
<p>Die Lehrgänge werden von Stellen durchgeführt, die von den Unfallversicherungsträgern als dafür geeignet bewertet sind. Eine Liste dieser Stellen führt die Qualitätssicherungsstelle Erste Hilfe (QSEH) auf bg-qseh.de. Prüft den Eintrag dort, bevor ihr bucht.</p>
<h2>Termine bei BWW</h2>
<p>Bei BWW sind die Betriebssanitäter-Lehrgänge in Leinefelde-Worbis angesetzt. Nach der Terminliste vom 02.11.2026 beginnt die <a href="/kurse/betriebssanitaeter-grundkurs/">Betriebssanitäter-Grundausbildung</a> am 13.07.2027 (450 € je Teilnehmer:in), der <a href="/kurse/betriebssanitaeter-aufbau/">Aufbaulehrgang</a> am 26.07.2027 (250 €). Weitere Termine im November 2027 stehen in der Terminliste. Für die <a href="/kurse/betriebssanitaeter-fortbildung/">Fortbildung</a> gelten die Termine auf der Kursseite. Ob ein Lehrgang für euer Unternehmen passt und was er im Einzelfall kostet, klären wir vor der Buchung mit euch.</p>
<p>Wer selbst andere für den betrieblichen Sanitätsdienst ausbilden will, findet die Wege unter <a href="/ausbilder-werden/betriebssanitaeter-lehrkraft/">Betriebssanitäter-Ausbilder werden</a>. Für Betriebe, die zwischen Ersthelfern und Sanitätern abwägen, hilft <a href="/wissen/ersthelfer-oder-betriebssanitaeter/">Ersthelfer oder Betriebssanitäter?</a>.</p>
<h2>Häufige Fragen</h2>
''' + ''.join(f'<h3>{q}</h3>\n<p>{a}</p>\n' for q, a in FAQ)
SRC = 'DGUV Fachbereich Erste Hilfe: Betriebssanitäter (dguv.de/fb-erstehilfe) · DGUV Arbeit &amp; Gesundheit: „Was machen Betriebssanitäter?“ (aug.dguv.de, 14.01.2022) · DGUV Vorschrift 1 § 27 · QSEH (bg-qseh.de). Abgerufen am 02.11.2026. Kein Ersatz für Rechtsberatung.'
RELATED = ('<p class="article-related"><a href="/wissen/betriebssanitaeter-pflicht/">Betriebssanitäter-Pflicht</a>'
 '<a href="/wissen/betriebssanitaeter-ausbildung/">Betriebssanitäter-Ausbildung</a>'
 '<a href="/kurse/betriebssanitaeter-grundkurs/">Grundausbildung</a><a href="/kurse/betriebssanitaeter-aufbau/">Aufbaulehrgang</a>'
 '<a href="/fuer-sanitaetsdienst/">Sanitätsdienst</a></p>\n')

def words():
    t = re.sub(r'<[^>]+>', ' ', BODY); return len(html.unescape(t).split())

def build():
    h = open('wissen/betriebssanitaeter-pflicht/index.html', encoding='utf8').read()
    old = 'Wann braucht ein Unternehmen Betriebssanitäter?'
    head_end = h.find('</head>'); main_i = h.find('<main')
    head = h[:head_end]; tail = h[h.find('</section><section class="section home-final"'):]
    assert tail.startswith('</section>')
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{TITLE} | BWW</title>', head)
    head = head.replace('/wissen/betriebssanitaeter-pflicht/', '/' + SLUG + '/')
    head = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + DESC, head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + TITLE + ' | BWW Wissensdatenbank', head)
    head = re.sub(r'(<meta property="article:published_time" content=")[^"]*', lambda m: m.group(1) + H, head)
    head = re.sub(r'(<meta property="article:modified_time" content=")[^"]*', lambda m: m.group(1) + H, head)
    org = {"@type": "Organization", "name": "BWW UG (haftungsbeschränkt)", "url": "https://www.multiplikatorenstelle.de/"}
    ld = [
     {"@context": "https://schema.org", "@type": "Article", "headline": TITLE, "description": DESC,
      "image": "https://www.multiplikatorenstelle.de/media/og/betriebssanitaeter.png", "inLanguage": "de-DE",
      "datePublished": H, "dateModified": H, "author": org,
      "publisher": {"@type": "Organization", "name": "BWW UG (haftungsbeschränkt)", "logo": {"@type": "ImageObject", "url": "https://www.multiplikatorenstelle.de/media/bww-logo-transparent.png"}},
      "mainEntityOfPage": URL},
     {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
      {"@type": "ListItem", "position": 1, "name": "Start", "item": "https://www.multiplikatorenstelle.de/"},
      {"@type": "ListItem", "position": 2, "name": "Wissen", "item": "https://www.multiplikatorenstelle.de/wissen/"},
      {"@type": "ListItem", "position": 3, "name": TITLE, "item": URL}]},
     {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
      {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]
    head += ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)
    crumbs = re.search(r'<nav class="breadcrumbs".*?</nav>', h, re.S).group(0).replace(old, TITLE)
    lead = ('Betriebssanitäter werden: zwei Lehrgänge mit 63 und 32 Unterrichtseinheiten, danach Fortbildung alle drei Jahre. '
            'Was die DGUV zu Aufgaben, Ablauf und Voraussetzungen schreibt.')
    hero = (f'<section class="page-hero"><div><span class="eyebrow">Ratgeber · Betriebssanitäter</span><h1>{TITLE}</h1>'
            f'<p class="article-stand">Stand: 02.11.2026 · Redaktion BWW · Quellen: DGUV Fachbereich Erste Hilfe, DGUV Arbeit &amp; Gesundheit, DGUV Vorschrift 1 § 27</p>'
            f'<p>{lead}</p><div class="hero-actions"><a class="btn primary" href="/kurse/betriebssanitaeter-grundkurs/">Zum Grundlehrgang</a>'
            f'<a class="btn ghost" href="/wissen/">Zur Wissensdatenbank</a></div></div>'
            f'<img class="bww-ill" src="/media/illustrations/bww/betriebssanitaeter.webp" width="386" height="446" alt="Betriebssanitäter werden: Ablauf und Voraussetzungen" fetchpriority="high"></section>')
    main = (h[main_i:h.find('<nav class="breadcrumbs"')] + crumbs + hero + '<section class="section article-body">\n' + BODY + RELATED +
            f'<p class="article-sources"><strong>Quellen:</strong> {SRC}</p>\n')
    return head + h[head_end:main_i] + main + tail

os.makedirs(SLUG, exist_ok=True)
open(SLUG + '/index.html', 'w', encoding='utf8').write(build())

# Sitemap, llms.txt, Rückverlinkung (idempotent)
s = open('sitemap.xml', encoding='utf8').read()
if SLUG not in s:
    m = re.search(r'<url><loc>[^<]*betriebssanitaeter-pflicht/</loc>.*?</url>', s)
    new = re.sub(r'<loc>[^<]*</loc>', '<loc>' + URL + '</loc>', m.group(0)); new = re.sub(r'<lastmod>[^<]*', '<lastmod>' + H, new)
    s = s.replace(m.group(0), m.group(0) + new); open('sitemap.xml', 'w', encoding='utf8').write(s)
l = open('llms.txt', encoding='utf8').read()
if SLUG not in l:
    line = '- [Betriebssanitäter werden: Ablauf und Voraussetzungen](' + URL + ')'
    anchor = '- [Wann braucht ein Betrieb Betriebssanitäter?](https://www.multiplikatorenstelle.de/wissen/betriebssanitaeter-pflicht/)'
    assert anchor in l; open('llms.txt', 'w', encoding='utf8').write(l.replace(anchor, anchor + '\n' + line))
for p in ('wissen/betriebssanitaeter-pflicht', 'wissen/betriebssanitaeter-ausbildung'):
    f = p + '/index.html'; t = open(f, encoding='utf8').read()
    if SLUG not in t:
        k = t.find('<p class="article-related">'); e = t.find('</p>', k)
        t = t[:e] + f'<a href="/{SLUG}/">Betriebssanitäter werden</a>' + t[e:]; open(f, 'w', encoding='utf8').write(t)
print('Wörter Body:', words(), '| Title', len(TITLE + ' | BWW'), '| Desc', len(DESC))
