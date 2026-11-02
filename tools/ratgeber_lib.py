"""Gemeinsamer Aufbau für Ratgeber-Artikel (idempotent). Basis ist eine bestehende Wissensseite."""
import re, json, os, html
R = os.path.expanduser('~/Claude/bww-neu-wt'); SITE = 'https://www.multiplikatorenstelle.de/'

def words(body):
    return len(html.unescape(re.sub(r'<[^>]+>', ' ', body)).split())

def publish(c):
    os.chdir(R)
    slug, title, desc, day = c['slug'], c['title'], c['desc'], c['day']; url = SITE + slug + '/'
    base = open(c['base'] + '/index.html', encoding='utf8').read()
    old = re.search(r'<h1>(.*?)</h1>', base).group(1)
    he, mi = base.find('</head>'), base.find('<main')
    head = re.sub(r'<script type="application/ld\+json">.*?</script>', '', base[:he], flags=re.S)
    head = re.sub(r'<title>.*?</title>', f'<title>{title} | BWW</title>', head)
    head = head.replace('/' + c['base'] + '/', '/' + slug + '/')
    head = re.sub(r'(<meta (?:name="description"|property="og:description") content=")[^"]*', lambda m: m.group(1) + desc, head)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + title + ' | BWW Wissensdatenbank', head)
    head = re.sub(r'(<meta property="article:(?:published|modified)_time" content=")[^"]*', lambda m: m.group(1) + day, head)
    img = re.search(r'"image": ?"([^"]*)"', base[:he]).group(1)
    org = {"@type": "Organization", "name": "BWW UG (haftungsbeschränkt)", "url": SITE}
    ld = [{"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc, "image": img, "inLanguage": "de-DE",
           "datePublished": day, "dateModified": day, "author": org,
           "publisher": {"@type": "Organization", "name": "BWW UG (haftungsbeschränkt)", "logo": {"@type": "ImageObject", "url": SITE + "media/bww-logo-transparent.png"}},
           "mainEntityOfPage": url},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
           {"@type": "ListItem", "position": 1, "name": "Start", "item": SITE},
           {"@type": "ListItem", "position": 2, "name": "Wissen", "item": SITE + "wissen/"},
           {"@type": "ListItem", "position": 3, "name": title, "item": url}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
           {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in c['faq']]}]
    head += ''.join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + '</script>' for x in ld)
    crumbs = re.search(r'<nav class="breadcrumbs".*?</nav>', base, re.S).group(0).replace(old, title)
    ill = re.search(r'<img class="bww-ill"[^>]*>', base).group(0)
    ill = re.sub(r'alt="[^"]*"', 'alt="' + title + '"', ill)
    hero = (f'<section class="page-hero"><div><span class="eyebrow">{c["eyebrow"]}</span><h1>{title}</h1>'
            f'<p class="article-stand">Stand: {c["stand"]} · Redaktion BWW · Quellen: {c["stand_src"]}</p><p>{c["lead"]}</p>'
            f'<div class="hero-actions"><a class="btn primary" href="{c["cta"][0]}">{c["cta"][1]}</a>'
            f'<a class="btn ghost" href="/wissen/">Zur Wissensdatenbank</a></div></div>{ill}</section>')
    faq = ''.join(f'<h3>{q}</h3>\n<p>{a}</p>\n' for q, a in c['faq'])
    related = '<p class="article-related">' + ''.join(f'<a href="{h}">{t}</a>' for h, t in c['related']) + '</p>\n'
    main = (base[mi:base.find('<nav class="breadcrumbs"')] + crumbs + hero + '<section class="section article-body">\n' + c['body'] +
            '<h2>Häufige Fragen</h2>\n' + faq + related + f'<p class="article-sources"><strong>Quellen:</strong> {c["src"]}</p>\n')
    tail = base[base.find('</section><section class="section home-final"'):]
    assert tail.startswith('</section>')
    os.makedirs(slug, exist_ok=True)
    open(slug + '/index.html', 'w', encoding='utf8').write(head + base[he:mi] + main + tail)
    s = open('sitemap.xml', encoding='utf8').read()
    if slug not in s:
        m = re.search(r'<url><loc>[^<]*/' + re.escape(c['base']) + r'/</loc>.*?</url>', s)
        new = re.sub(r'<loc>[^<]*</loc>', '<loc>' + url + '</loc>', m.group(0)); new = re.sub(r'<lastmod>[^<]*', '<lastmod>' + day, new)
        open('sitemap.xml', 'w', encoding='utf8').write(s.replace(m.group(0), m.group(0) + new))
    l = open('llms.txt', encoding='utf8').read()
    if slug not in l:
        m = re.search(r'^- \[[^\]]*\]\([^)]*/' + re.escape(c['base']) + r'/\)$', l, re.M)
        open('llms.txt', 'w', encoding='utf8').write(l.replace(m.group(0), m.group(0) + f'\n- [{title}]({url})'))
    for p in c['backlinks']:
        f = p + '/index.html'; t = open(f, encoding='utf8').read()
        if slug not in t:
            k = t.find('<p class="article-related">'); e = t.find('</p>', k)
            open(f, 'w', encoding='utf8').write(t[:e] + f'<a href="/{slug}/">{c["backlink_text"]}</a>' + t[e:])
    print(slug, '| Wörter', words(c['body'] + faq), '| Title', len(title + ' | BWW'), '| Desc', len(desc))
