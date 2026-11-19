#!/usr/bin/env python3
"""Baut die BWW-Lernbereiche (Entwurf 14.11.2026): je Kurs Hauptseite (indexierbar, ohne Loesungen), druckbares Arbeitsblatt (noindex, ohne Loesungen)
und die Loesungshinweis-Seite NUR ausserhalb des Repos (LOESUNGEN_DIR, ohne Adresse). Schale aus wissen/notruf-112 (aktuelle ?v-Token). Idempotent.
Inhalt: tools/lernbereich_inhalt.py. Zusaetzlich: Verweis auf der jeweiligen Kursseite (topic-links) und Sitemap-Eintrag je Hauptseite."""
import html as H, json, os, re, sys
ROOT = os.path.expanduser('~/Claude/bww-neu-wt'); os.chdir(ROOT); sys.path.insert(0, os.path.join(ROOT, 'tools'))
from lernbereich_inhalt import COURSES, ZP
ENTWURF = False   # Freigabe-Banner aus (Rubens Freigabe 19.11.2026); FREIGABE (Index/Sitemap) unveraendert
FREIGABE = False          # False: Hauptseiten noindex,follow und nicht in der Sitemap (bis Rubens Freigabe); True: indexierbar + Sitemap
LOESUNGEN_DIR = os.path.expanduser('~/Claude/Koordinator/ultracode-13-11/bww-loesungshinweise')   # ausserhalb des Repos, ohne Adresse
BASE = 'https://www.multiplikatorenstelle.de'; STAND = '14.11.2026'
shell = open('wissen/notruf-112/index.html', encoding='utf8').read()
head = shell[shell.index('<head>'):shell.index('<header class="site-header">')]
pre = shell[:shell.index('<head>')]
mid = shell[shell.index('<header class="site-header">'):shell.index('<main')]
tail = shell[shell.index('<section class="section home-final">'):]
def esc(t):
    t = t.replace(ZP, '§§ZP§§'); t = H.escape(t, quote=False); return t.replace('§§ZP§§', ZP)
STYLE = '''<style>
.lern-toc{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.7rem;list-style:none;padding:0;margin:1.2rem 0 2rem}
.article-body .lern-toc a{display:block;padding:.8rem 1rem;border:1px solid var(--ad-line,#d9e5dd);border-radius:14px;background:var(--ad-card,#fff);color:inherit;text-decoration:none;min-height:44px}
.article-body .lern-toc a:hover b{text-decoration:underline}
.lern-toc b{display:block}.lern-toc span{font-size:.92rem;color:var(--ad-ink-3,#5b6e64)}
.lern-block{margin:2.6rem 0 0;padding-top:.4rem;border-top:1px solid var(--ad-line,#d9e5dd)}
.lern-block h3{margin:1.4rem 0 .4rem}
.lern-block .lead{color:var(--ad-ink-2,#3f5248);font-size:1.06rem}
.aufgabe{margin:.9rem 0;padding:1rem 1.1rem;border:1px solid var(--ad-line,#d9e5dd);border-radius:14px;background:var(--ad-card,#fff)}
.aufgabe p{margin:.2rem 0}
.zp{display:inline-block;background:#fff3cd;color:#5c4400;border-radius:6px;padding:0 .4rem;font-size:.78rem;font-weight:700;letter-spacing:.02em}
.entwurf{border:1px dashed #c9761f;border-radius:14px;padding:.8rem 1rem;background:#fff8ec;color:#5c4a33;font-size:.95rem;margin:0 0 1.4rem}
.lern-quellen li{margin:.25rem 0}
.ab-feld{display:flex;gap:1.2rem;flex-wrap:wrap;margin:1rem 0 1.6rem}.ab-feld span{flex:1 1 220px;border-bottom:1px solid currentColor;min-height:1.8rem;padding-bottom:.1rem}
.ab-linien{height:7.2rem;background:repeating-linear-gradient(to bottom,transparent 0,transparent 1.75rem,rgba(127,127,127,.55) 1.75rem,rgba(127,127,127,.55) calc(1.75rem + 1px));margin:.4rem 0 1rem}
.ab-block h2{margin-top:1.8rem}.ab-aufgabe{break-inside:avoid;margin:.8rem 0}
@media (prefers-color-scheme: dark){.zp{background:#4a3b0a;color:#ffe9a8}.entwurf{background:#2a2216;color:#e9d9b9;border-color:#c9761f}}
@media print{
 .site-header,.site-footer,.breadcrumbs,.home-final,.skip-link,.hero-actions,.privacy-note,.sticky-book,.no-print,nav[aria-label="Sprungnavigation"]{display:none!important}
 body{background:#fff!important;color:#000!important}main,.section,.page-hero{background:#fff!important;color:#000!important;padding:0!important;margin:0!important}
 .page-hero{display:block!important;border:0!important}.bww-ill{display:none!important}h1{font-size:1.5rem!important}h2{font-size:1.15rem!important;break-after:avoid}
 .zp,.entwurf{display:none!important}a{color:#000!important;text-decoration:none!important}
}
</style>'''
def make_head(c, url, title, desc, robots, og_title):
    h = head
    h = re.sub(r'<title>.*?</title>', '<title>' + H.escape(title, quote=False) + '</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="' + H.escape(desc) + '">', h, count=1)
    h = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="' + BASE + url + '">', h, count=1)
    h = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="' + robots + '">', h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="' + H.escape(og_title) + '">', h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="' + H.escape(desc) + '">', h, count=1)
    h = re.sub(r'<meta property="og:type" content="[^"]*">', '<meta property="og:type" content="website">', h, count=1)
    h = re.sub(r'<meta property="article:[a-z_]+" content="[^"]*">', '', h)
    h = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="' + BASE + url + '">', h, count=1)
    h = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="' + BASE + '/media/og/' + c['og'] + '">', h, count=1)
    h = re.sub(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="' + H.escape(og_title) + '">', h, count=1)
    h = re.sub(r'<meta name="twitter:description" content="[^"]*">', '<meta name="twitter:description" content="' + H.escape(desc) + '">', h, count=1)
    h = re.sub(r'<meta name="twitter:image" content="[^"]*">', '<meta name="twitter:image" content="' + BASE + '/media/og/' + c['og'] + '">', h, count=1)
    scripts = re.findall(r'<script type="application/ld\+json">.*?</script>', h, flags=re.S); org = scripts[0]
    for s in scripts: h = h.replace(s, '')
    name = title.split(' | ')[0]
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Start", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": c['kurs'][1], "item": BASE + c['kurs'][0]}, {"@type": "ListItem", "position": 3, "name": name, "item": BASE + url}]}
    lr = {"@context": "https://schema.org", "@type": "LearningResource", "name": name, "description": desc, "inLanguage": "de-DE", "url": BASE + url, "dateModified": "2026-11-14",
          "publisher": {"@type": "Organization", "name": "BWW UG (haftungsbeschränkt)"}}
    ld = ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False, separators=(',', ':')) + '</script>' for x in (bc, lr))
    return h.replace('<link rel="stylesheet" href="/assets/fx.css', org + ld + STYLE + '<link rel="stylesheet" href="/assets/fx.css', 1)
def crumbs(c, hub, cur):
    return ('<nav class="breadcrumbs" aria-label="Brotkrümel"><a href="/">Start</a><span class="sep" aria-hidden="true">›</span><a href="' + c['kurs'][0] + '">' + esc(c['kurs'][1]) + '</a>'
            + ('<span class="sep" aria-hidden="true">›</span><a href="' + hub + '">Lernbereich</a>' if cur != 'hub' else '') + '<span class="sep" aria-hidden="true">›</span><span class="current">'
            + {'hub': 'Lernbereich', 'ab': 'Arbeitsblatt', 'lo': 'Lösungshinweise'}[cur] + '</span></nav>')
def page(c, url, title, desc, robots, og_title, body):
    return pre + make_head(c, url, title, desc, robots, og_title) + '</head><body><nav aria-label="Sprungnavigation"><a class="skip-link" href="#hauptinhalt">Zum Inhalt springen</a></nav>' + mid + '<main id="hauptinhalt" tabindex="-1">' + body + tail
def hero(c, hub, cur, h1, eyebrow, intro, actions, bild=True):
    img = '<img class="bww-ill" src="' + c['bild'] + '" width="461" height="428" alt="' + esc(c['bild_alt']) + '" fetchpriority="high">' if bild else ''
    return ('<section class="page-hero"><div><span class="eyebrow">' + esc(eyebrow) + '</span><h1>' + esc(h1) + '</h1><p class="article-stand">Stand: ' + STAND + ' · Redaktion BWW</p><p>' + esc(intro) + '</p><div class="hero-actions">' + actions + '</div></div>' + img + '</section>')
def hub_page(c, slug):
    hub = '/lernbereich/' + slug + '/'; ab = hub + 'arbeitsblatt/'; BL = c['bloecke']
    b = [crumbs(c, hub, 'hub'), hero(c, hub, 'hub', c['h1'], c['eyebrow'], c['intro'], '<a class="btn primary" href="' + ab + '">Arbeitsblatt öffnen und drucken</a><a class="btn ghost" href="' + c['kurs'][0] + '">Zum Kurs</a>')]
    b.append('<section class="section article-body">')
    if ENTWURF: b.append('<p class="entwurf"><strong>Entwurf.</strong> Fachliche Freigabe durch Ruben steht aus; markierte Stellen („ZU PRÜFEN DURCH RUBEN“) sind in den vorhandenen Wissensbeiträgen nicht belegt.</p>')
    b.append('<p>Der Lernbereich folgt ' + c['anzahl'] + ' Themenblöcken. Jeder Block ist in sich abgeschlossen: lesen, die Aufgaben schriftlich bearbeiten und die Ergebnisse im Kurs besprechen. Ausführliche Hintergründe stehen in den verlinkten Beiträgen der Wissensdatenbank. Der Lernbereich ersetzt keine praktische Ausbildung: Handgriffe werden im Kurs geübt.</p>')
    b.append('<ol class="lern-toc">' + ''.join('<li><a href="#' + x['id'] + '"><b>Block ' + str(i) + ': ' + esc(x['titel']) + '</b><span>' + esc(x['kurz']) + '</span></a></li>' for i, x in enumerate(BL, 1)) + '</ol>')
    for i, x in enumerate(BL, 1):
        b.append('<section class="lern-block" id="' + x['id'] + '"><h2>Block ' + str(i) + ': ' + esc(x['titel']) + '</h2><p class="lead">' + esc(x['kurz']) + '</p>')
        b.append('<h3>Lernziele</h3><p>Nach diesem Block kannst du:</p><ul>' + ''.join('<li>' + esc(z) + '</li>' for z in x['ziele']) + '</ul>')
        b.append('<h3>Erklärung</h3>' + ''.join('<p>' + esc(p) + '</p>' for p in x['text']))
        b.append('<div class="key-facts"><h3>Merksätze</h3><ul>' + ''.join('<li>' + esc(m) + '</li>' for m in x['merk']) + '</ul></div>')
        b.append('<h3>Typische Fehler</h3><ul>' + ''.join('<li>' + esc(f) + '</li>' for f in x['fehler']) + '</ul><h3>Aufgaben zum Ausarbeiten</h3>')
        for j, (typ, frage, _l) in enumerate(x['aufgaben'], 1):
            b.append('<div class="aufgabe"><p><strong>Aufgabe ' + str(i) + '.' + str(j) + ' · ' + esc(typ) + '</strong></p><p>' + esc(frage) + '</p></div>')
        b.append('<p class="article-related">' + ''.join('<a href="' + u + '">' + esc(n) + '</a>' for u, n in x['weiter']) + '</p></section>')
    b.append('<section class="lern-block"><h2>Arbeitsblatt zum Ausdrucken</h2><p>Alle Aufgaben dieses Lernbereichs stehen auf einem Arbeitsblatt mit Schreibfeldern, gedacht für den Ausdruck oder als PDF aus dem Druckdialog deines Browsers.</p><p class="article-related"><a href="' + ab + '">Arbeitsblatt öffnen</a><a href="' + c['kurs'][0] + '">Zum Kurs</a></p></section>')
    b.append('<section class="lern-block lern-quellen"><h2>Fachliche Grundlagen</h2><ul>' + ''.join('<li>' + esc(q) + '</li>' for q in c['quellen']) + '</ul><div class="article-note"><strong>Hinweis:</strong> Dieser Lernbereich ersetzt keine Ausbildung. Im Notfall gelten die Anweisungen der Leitstelle.</div></section></section>')
    return page(c, hub, c['titel_seo'], c['desc'], 'index,follow,max-image-preview:large' if FREIGABE else 'noindex,follow', c['titel_seo'].replace(' | BWW', '') + ' | BWW', ''.join(b))
def ab_page(c, slug):
    hub = '/lernbereich/' + slug + '/'; BL = c['bloecke']; short = c['kurs'][1]
    b = [crumbs(c, hub, 'ab'), hero(c, hub, 'ab', 'Arbeitsblatt: ' + short, 'Arbeitsblatt · ' + short, 'Bearbeite die Aufgaben schriftlich. Die Erklärungen findest du im Lernbereich.',
                                    '<button class="btn primary no-print" type="button" onclick="window.print()">Drucken oder als PDF speichern</button><a class="btn ghost" href="' + hub + '">Zum Lernbereich</a>', bild=False), '<section class="section article-body">']
    if ENTWURF: b.append('<p class="entwurf"><strong>Entwurf.</strong> Fachliche Freigabe durch Ruben steht aus.</p>')
    b.append('<div class="ab-feld"><span>Name:</span><span>Datum:</span><span>Kurs:</span></div>')
    for i, x in enumerate(BL, 1):
        b.append('<div class="ab-block"><h2>Block ' + str(i) + ': ' + esc(x['titel']) + '</h2>')
        for j, (typ, frage, _l) in enumerate(x['aufgaben'], 1):
            b.append('<div class="ab-aufgabe"><p><strong>Aufgabe ' + str(i) + '.' + str(j) + ' · ' + esc(typ) + '</strong><br>' + esc(frage) + '</p><div class="ab-linien" aria-hidden="true"></div></div>')
        b.append('</div>')
    b.append('<p class="article-related no-print"><a href="' + hub + '">Zurück zum Lernbereich</a></p></section>')
    t = 'Arbeitsblatt ' + short + ' zum Drucken | BWW'
    return page(c, hub + 'arbeitsblatt/', t[:60] if len(t) <= 60 else 'Arbeitsblatt zum Drucken | BWW', 'Druckbares Arbeitsblatt: ' + short + ', alle Aufgaben mit Schreibfeldern, ohne Lösungen.', 'noindex,follow', 'Arbeitsblatt: ' + short + ' | BWW', ''.join(b))
def lo_page(c, slug):
    hub = '/lernbereich/' + slug + '/'; BL = c['bloecke']; short = c['kurs'][1]
    b = [crumbs(c, hub, 'lo'), hero(c, hub, 'lo', 'Lösungshinweise: ' + short, 'Nur für die Kursleitung', 'Kurze Lösungshinweise zu den Aufgaben des Lernbereichs, für die Besprechung im oder nach dem Kurs. Diese Seite ist nicht verlinkt und nicht für Suchmaschinen vorgesehen.', '', bild=False), '<section class="section article-body">']
    if ENTWURF: b.append('<p class="entwurf"><strong>Entwurf.</strong> Fachliche Freigabe durch Ruben steht aus.</p>')
    for i, x in enumerate(BL, 1):
        b.append('<h2>Block ' + str(i) + ': ' + esc(x['titel']) + '</h2>')
        for j, (typ, frage, loes) in enumerate(x['aufgaben'], 1):
            b.append('<div class="aufgabe"><p><strong>Aufgabe ' + str(i) + '.' + str(j) + ' · ' + esc(typ) + '</strong></p><p>' + esc(frage) + '</p><p><em>Lösungshinweis:</em> ' + esc(loes) + '</p></div>')
    b.append('</section>')
    return page(c, hub + 'loesungshinweise/', 'Lösungshinweise (Kursleitung) | BWW', 'Lösungshinweise zu den Aufgaben des Lernbereichs, nur für die Kursleitung.', 'noindex,nofollow', 'Lösungshinweise | BWW', ''.join(b))
sm = open('sitemap.xml', encoding='utf8').read()
for slug, c in COURSES.items():
    d = 'lernbereich/' + slug; os.makedirs(d + '/arbeitsblatt', exist_ok=True)
    open(d + '/index.html', 'w', encoding='utf8').write(hub_page(c, slug))
    open(d + '/arbeitsblatt/index.html', 'w', encoding='utf8').write(ab_page(c, slug))
    os.makedirs(LOESUNGEN_DIR, exist_ok=True); open(LOESUNGEN_DIR + '/' + slug + '.html', 'w', encoding='utf8').write(lo_page(c, slug))
    hubu = '/lernbereich/' + slug + '/'
    f = c['kurs_datei']; s = open(f, encoding='utf8').read()
    if hubu not in s:
        m = re.search(r'<p class="topic-links">.*?</p>', s, re.S); assert m, f
        s = s[:m.end() - 4] + ' ' + c['verweis_text'] + s[m.end() - 4:]; open(f, 'w', encoding='utf8').write(s)
    if not FREIGABE: sm = re.sub(r'<url><loc>' + re.escape(BASE + hubu) + r'</loc>.*?</url>', '', sm)
    elif hubu not in sm: sm = sm.replace('</urlset>', '<url><loc>' + BASE + hubu + '</loc><lastmod>2026-11-14</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url></urlset>', 1)
open('sitemap.xml', 'w', encoding='utf8').write(sm)
print('ok', len(COURSES), 'Kurse')
