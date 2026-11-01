#!/usr/bin/env python3
"""Statisches Qualitäts-Audit der BWW-Ausgabe (nur Quelltext, kein Browser). Schreibt Markdown-Bericht (Pfad als Argument)."""
import re, glob, json, html, os, sys, collections, urllib.parse
ROOT = '.'; HOST = 'https://www.multiplikatorenstelle.de'
files = sorted(f for f in glob.glob('**/*.html', recursive=True) if not f.startswith(('node_modules', '.git')))
txt = {f: open(f, encoding='utf8', errors='replace').read() for f in files}
def url_of(f):
    if f == 'index.html': return HOST + '/'
    if f.endswith('/index.html'): return HOST + '/' + f[:-10]
    return HOST + '/' + f
def main_of(h): return h
out = []; P = out.append
def sec(t): P(f'\n## {t}')
def lim(lst, n=15): return lst[:n] + ([f'… (+{len(lst)-n})'] if len(lst) > n else [])
P(f'# Statisches Audit BWW, {len(files)} HTML-Dateien (Skript tools/audit_statisch.py)')
ids = {f: set(re.findall(r'\bid="([^"]+)"', h)) | set(re.findall(r'<a[^>]+\bname="([^"]+)"', h)) for f, h in txt.items()}
# --- 1 Links/Bilder
sec('1. Interne Links, Anker, Bilder')
def resolve(p):
    p = p.split('?')[0]
    if p.endswith('/'): return p.strip('/') + '/index.html' if p != '/' else 'index.html'
    return p.strip('/') if os.path.exists(p.strip('/')) else (p.strip('/') + '/index.html' if os.path.exists(p.strip('/') + '/index.html') else p.strip('/'))
dead = collections.defaultdict(set); deadanchor = collections.defaultdict(set); deadimg = collections.defaultdict(set)
for f, h in txt.items():
    body = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    for m in re.finditer(r'<a\b[^>]*\bhref="([^"]*)"', body):
        u = html.unescape(m.group(1))
        if not u.startswith('/') or u.startswith('//'): 
            if u.startswith('#') and len(u) > 1 and u[1:] not in ids[f]: deadanchor[f].add(u)
            continue
        path, _, frag = u.partition('#'); t = resolve(path or '/')
        if not os.path.exists(t): dead[f].add(u); continue
        if frag and t.endswith('.html') and frag not in ids.get(t, set()) and t in ids: deadanchor[f].add(u)
    for m in re.finditer(r'<img\b[^>]*\bsrc="([^"]+)"', body):
        u = html.unescape(m.group(1))
        if u.startswith('/') and not os.path.exists(u.split('?')[0].strip('/')): deadimg[f].add(u)
allfiles = sorted(set(u for s in dead.values() for u in s)); P(f'- Tote interne Links: {sum(len(s) for s in dead.values())} Stellen in {len(dead)} Dateien, {len(allfiles)} verschiedene Ziele')
for u in lim(allfiles): P(f'  - `{u}` (z. B. in `{next(f for f,s in dead.items() if u in s)}`)')
P(f'- Tote Anker (#id ohne Ziel): {sum(len(s) for s in deadanchor.values())} in {len(deadanchor)} Dateien'); 
for f in lim(sorted(deadanchor)): P(f'  - `{f}`: {sorted(deadanchor[f])[:4]}')
P(f'- Fehlende Bilder: {sum(len(s) for s in deadimg.values())} in {len(deadimg)} Dateien')
for f in lim(sorted(deadimg)): P(f'  - `{f}`: {sorted(deadimg[f])[:3]}')
# --- 2 JSON-LD
sec('2. JSON-LD')
perr = []; dupid = []; missing = []; faqmis = []; counts = collections.Counter()
def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values(): yield from walk(v)
    elif isinstance(o, list):
        for v in o: yield from walk(v)
for f, h in txt.items():
    vis = html.unescape(re.sub(r'<[^>]+>', ' ', re.sub(r'<script.*?</script>', '', h, flags=re.S)))
    vis = re.sub(r'\s+', ' ', vis); seen = collections.Counter()
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: j = json.loads(m.group(1))
        except Exception as e: perr.append((f, str(e)[:60])); continue
        for o in walk(j):
            t = o.get('@type'); ts = t if isinstance(t, list) else [t]
            for x in ts: counts[x] += 1
            if '@id' in o and isinstance(o['@id'], str) and ('@type' in o): seen[o['@id']] += 1
            if 'FAQPage' in ts:
                me = o.get('mainEntity') or []
                if not me: missing.append((f, 'FAQPage ohne mainEntity'))
                for q in me:
                    nm = q.get('name'); a = (q.get('acceptedAnswer') or {}).get('text')
                    if not nm or not a: missing.append((f, 'FAQ Frage/Antwort fehlt'))
                    elif re.sub(r'\s+', ' ', html.unescape(nm)).strip() not in vis: faqmis.append((f, nm[:60]))
            if 'Course' in ts:
                for k in ('name', 'description', 'provider'):
                    if not o.get(k): missing.append((f, f'Course ohne {k}'))
            if any(x in ('Organization', 'EducationalOrganization', 'LocalBusiness') for x in ts if x) and (o is j or (isinstance(j, dict) and o in (j.get('@graph') or []))):
                for k in ('name', 'url'):
                    if not o.get(k) and not o.get('@id'): missing.append((f, f'Organization ohne {k}'))
            if 'BreadcrumbList' in ts:
                for it in o.get('itemListElement') or []:
                    if not (it.get('name') and it.get('item') and it.get('position')): missing.append((f, 'Breadcrumb-Item unvollständig'))
    for i, c in seen.items():
        if c > 1: dupid.append((f, i))
P(f'- Typen: {dict(counts.most_common(12))}')
P(f'- Parse-Fehler: {len(perr)} {lim(perr, 5)}'); P(f'- Doppelte @id (mit @type) je Seite: {len(dupid)} {lim(dupid, 5)}')
P(f'- Fehlende Pflichtfelder: {len(missing)} {lim(sorted(set(missing)), 8)}'); P(f'- FAQ-Frage im Schema, aber nicht sichtbar: {len(faqmis)} {lim(faqmis, 8)}')
# --- 3 Title/Description/H1
sec('3. Title, Description, Überschriften')
T = {}; D = {}; h1bad = []; skip = []; long_t = []; long_d = []
for f, h in txt.items():
    if 'http-equiv="refresh"' in h: continue
    t = re.search(r'<title>(.*?)</title>', h, re.S); d = re.search(r'<meta name="description" content="(.*?)"', h)
    t = html.unescape(t.group(1)).strip() if t else ''; d = html.unescape(d.group(1)).strip() if d else ''
    T[f] = t; D[f] = d
    if len(t) > 60 or not t: long_t.append((f, len(t)))
    if len(d) > 155 or not d: long_d.append((f, len(d)))
    body = re.sub(r'<script.*?</script>|<!--.*?-->', '', h, flags=re.S); hs = [int(x) for x in re.findall(r'<h([1-6])\b', body)]
    if hs.count(1) != 1: h1bad.append((f, hs.count(1)))
    for a, b in zip(hs, hs[1:]):
        if b > a + 1: skip.append((f, f'h{a}->h{b}')); break
P(f'- Title > 60 oder leer: {len(long_t)} {lim(long_t, 6)}'); P(f'- Description > 155 oder leer: {len(long_d)} {lim(long_d, 6)}')
for name, dd in (('Title', T), ('Description', D)):
    c = collections.Counter(v for v in dd.values() if v); dup = {k: [f for f, v in dd.items() if v == k] for k, n in c.items() if n > 1}
    P(f'- Doppelte {name}: {len(dup)}'); 
    for k, fs in list(dup.items())[:5]: P(f'  - „{k[:70]}“: {lim(fs, 4)}')
P(f'- Seiten mit ≠ 1 H1: {len(h1bad)} {lim(h1bad, 8)}'); P(f'- Überschrift-Sprünge (h2→h4 usw.): {len(skip)} {lim(skip, 8)}')
# --- 4 canonical, noindex, sitemap, robots
sec('4. Canonical, noindex, Sitemap, robots.txt')
canbad = []; noindex = []; hreflang = []
for f, h in txt.items():
    if 'http-equiv="refresh"' in h: continue
    c = re.search(r'<link rel="canonical" href="([^"]*)"', h)
    if not c: canbad.append((f, 'fehlt')); 
    elif f != '404.html' and c.group(1) != url_of(f): canbad.append((f, c.group(1)[-50:]))
    if re.search(r'<meta name="robots" content="[^"]*noindex', h): noindex.append(f)
    if 'hreflang' in h: hreflang.append(f)
P(f'- Canonical fehlt/abweichend: {len(canbad)} {lim(canbad, 8)}'); P(f'- noindex-Seiten: {len(noindex)}; hreflang: {len(hreflang)}')
sm = open('sitemap.xml', encoding='utf8').read(); smurls = re.findall(r'<loc>(.*?)</loc>', sm)
fileurls = {url_of(f): f for f in files if 'http-equiv="refresh"' not in txt[f] and f != '404.html'}
miss_file = [u for u in smurls if u not in fileurls]; not_in_sm = [f for u, f in fileurls.items() if u not in set(smurls) and f not in noindex]
noidx_in_sm = [fileurls[u] for u in smurls if u in fileurls and fileurls[u] in noindex]
P(f'- Sitemap: {len(smurls)} URLs; ohne Datei: {len(miss_file)} {lim(miss_file, 5)}; indexierbare Dateien nicht in der Sitemap: {len(not_in_sm)} {lim(not_in_sm, 8)}; noindex-Seiten in der Sitemap: {len(noidx_in_sm)} {lim(noidx_in_sm, 5)}')
P(f'- Doppelte Sitemap-URLs: {len(smurls) - len(set(smurls))}')
rb = open('robots.txt', encoding='utf8').read() if os.path.exists('robots.txt') else ''
nd = len(re.findall(r'(?im)^disallow:\s*\S', rb))
P(f'- robots.txt: {"vorhanden" if rb else "FEHLT"}; Sitemap-Zeile: {"ja" if "Sitemap:" in rb else "nein"}; Disallow-Zeilen: {nd}')
# --- 5 Alt, Labels, Kontrast
sec('5. Alt-Texte, Formularlabels, Kontrast-Tokens')
noalt = collections.Counter(); nolabel = []; emptybtn = []
for f, h in txt.items():
    body = re.sub(r'<script.*?</script>|<!--.*?-->', '', h, flags=re.S)
    for m in re.finditer(r'<img\b([^>]*)>', body):
        if not re.search(r'\balt=', m.group(1)): noalt[f] += 1
    for m in re.finditer(r'<(input|select|textarea)\b([^>]*)>', body):
        a = m.group(2)
        if re.search(r'type="(hidden|submit|button|checkbox|radio)"', a) and 'checkbox' not in a and 'radio' not in a: continue
        if 'aria-hidden="true"' in a: continue   # Honeypot-Felder
        idm = re.search(r'\bid="([^"]+)"', a)
        pre = body[:m.start()]; wrapped = pre.rfind('<label') > pre.rfind('</label>')
        ok = wrapped or bool(re.search(r'aria-label=|aria-labelledby=|title=', a)) or (idm and re.search(r'<label[^>]*\bfor="%s"' % re.escape(idm.group(1)), body))
        if not ok: nolabel.append((f, (idm.group(1) if idm else re.search(r'name="([^"]*)"', a).group(1) if re.search(r'name="([^"]*)"', a) else '?')))
    for m in re.finditer(r'<button\b[^>]*>(.*?)</button>', body, re.S):
        if not re.sub(r'<[^>]+>', '', m.group(1)).strip() and 'aria-label' not in m.group(0): emptybtn.append(f)
P(f'- <img> ohne alt: {sum(noalt.values())} in {len(noalt)} Dateien {lim(list(noalt.items()), 5)}'); P(f'- Formularfelder ohne Label/aria-label: {len(nolabel)} {lim(nolabel, 8)}'); P(f'- Buttons ohne Text/aria-label: {len(emptybtn)} {lim(emptybtn, 5)}')
css = open('assets/styles.css', encoding='utf8').read()
def lum(hx):
    hx = hx.lstrip('#'); hx = ''.join(c * 2 for c in hx) if len(hx) == 3 else hx
    r, g, b = [int(hx[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)
pairs = [('#426d58', '#ffffff', 'Kopf-Name'), ('#65766d', '#ffffff', 'small-note (alt)'), ('#25704e', '#ffffff', 'Grün/Weiß (Button)'), ('#2c3a33', '#f4f8f5', 'Badge')]
mm = re.search(r'--bww-muted:\s*(#[0-9a-fA-F]{3,6})', css)
if mm: pairs.append((mm.group(1), '#ffffff', '--bww-muted/Weiß'))
P('- Kontrast (Soll ≥ 4,5 : 1): ' + '; '.join(f'{n} {cr(a, b):.2f}' for a, b, n in pairs))
# --- 6 Claims
sec('6. Alte Aussagen (sichtbarer Text, Meta, Schema, llms)')
PH = ['anerkannt', 'Rettungsdienstbildungsstelle', 'eine von 14', 'langjährig', 'einzige', 'günstigste', 'Marktführer', 'im vollen Umfang', 'DGUV-ermächtigt', 'amtlich', 'staatlich']
srcs = dict(txt); 
for g in ('llms.txt', 'llms-full.txt'): 
    if os.path.exists(g): srcs[g] = open(g, encoding='utf8').read()
res = {p: collections.defaultdict(int) for p in PH}
for f, h in srcs.items():
    t = html.unescape(re.sub(r'<script(?! type="application/ld\+json").*?</script>|<style.*?</style>|<!--.*?-->', '', h, flags=re.S))
    for p in PH:
        n = len(re.findall(re.escape(p), t, re.I))
        if n: res[p][f] = n
for p in PH:
    fs = res[p]; legal = [f for f in fs if f.startswith(('agb/', 'datenschutz/', 'impressum/', 'widerruf/'))]
    P(f'- „{p}“: {sum(fs.values())} Treffer in {len(fs)} Dateien' + (f' (davon Rechtsseiten: {legal})' if legal else '') + f'; Beispiele {lim(sorted(fs), 4)}')
P('- „anerkannt“/„Anerkennung“ mit Selbstbezug (BWW/wir/unsere/Kennziffer im Umkreis von 90 Zeichen):')
selb = []
for f, h in srcs.items():
    t = html.unescape(re.sub(r'<script(?! type="application/ld\+json").*?</script>|<style.*?</style>|<!--.*?-->', '', h, flags=re.S)); t = re.sub(r'<[^>]+>', ' ', t); t = re.sub(r'\s+', ' ', t)
    for m in re.finditer(r'[Aa]nerkannt\w*|[Aa]nerkennung', t):
        ctx = t[max(0, m.start() - 90):m.end() + 90]
        if re.search(r'BWW|\bwir\b|\bunser|Kennziffer|8\.2122', ctx): selb.append((f, ctx))
P(f'  - {len(selb)} Stellen in {len(set(x[0] for x in selb))} Dateien')
for f, c in selb[:25]: P(f'  - `{f}`: …{c}…')
# --- 7 externe Skripte, Schlüssel
sec('7. Externe Skripte und Schlüssel im Frontend')
ext = collections.Counter(); keyhits = []
for f, h in list(txt.items()):
    for m in re.finditer(r'<script[^>]+src="(https?://[^"]+)"', h): ext[urllib.parse.urlparse(m.group(1)).netloc] += 1
for f in glob.glob('assets/*.js') + list(txt):
    t = open(f, encoding='utf8', errors='replace').read()
    for m in re.finditer(r'(?i)(api[_-]?key|secret|bearer\s+[a-z0-9]|sk_(live|test)_|AIza[0-9A-Za-z_-]{20,}|password\s*[:=]\s*["\'][^"\']+)', t):
        keyhits.append((f, m.group(0)[:30]))
P(f'- Externe Script-Hosts: {dict(ext)}'); P(f'- Muster für Schlüssel/Secrets: {len(keyhits)} {lim(sorted(set(keyhits)), 8)}')
open(sys.argv[1], 'w', encoding='utf8').write('\n'.join(out) + '\n'); print('Bericht:', sys.argv[1], len(out), 'Zeilen')
