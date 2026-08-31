# Single-Source-Header-Sync fuer die 332 statischen HTML-Seiten dieses Repos.
# Nutzung (aus dem Repo-Root):
#   python3 scripts/sync_headers.py            -> Dry-Run, zeigt was sich aendern wuerde
#   python3 scripts/sync_headers.py --apply    -> schreibt die Aenderungen
# Neue Seite hinzufuegen: Eintrag in header_map.json ergaenzen
#   ("/pfad/": {"active": "<nav-href, das aktiv markiert wird, oder null>",
#               "cta": "/inhouse-kurse/#anfrage"  <- oder "#anfrage", falls die Seite
#               selbst eine id="anfrage"-Sektion hat}), dann --apply laufen lassen.
import re, glob, json, sys

MAP_PATH = __file__.rsplit('/', 1)[0] + '/header_map.json'
mapping = json.load(open(MAP_PATH, encoding='utf-8'))

NAV_LINKS = [
    ('/kurse/', 'Kurse'),
    ('/inhouse-kurse/', 'Inhouse'),
    ('/kurse/offene-kurse-worbis/', 'Offene Kurse'),
    ('/standorte/', 'Standorte'),
    ('/arbeitsschutz-check/', 'Tools'),
    ('/wissen/', 'Wissen'),
    ('/dozent-werden/', 'Dozent werden'),
    ('/shop/', 'Shop'),
    ('https://software-wippermann.de/mein-bereich?org=bww', 'Login'),
]

def build_header(active_href, cta_href):
    parts = ['<header class="site-header"><a class="brand" href="/">'
             '<img src="/media/bww-logo-transparent.webp" alt="BWW Logo">'
             '<span><small>Multiplikatorenstelle & Rettungsdienstbildungsstelle</small></span></a>'
             '<button class="menu-toggle" aria-label="Menü öffnen" aria-expanded="false" '
             'onclick="var o=document.body.classList.toggle(\'menu-open\');'
             'this.setAttribute(\'aria-expanded\',o);'
             'this.setAttribute(\'aria-label\',o?\'Menü schließen\':\'Menü öffnen\')">'
             '☰</button><nav>']
    for href, label in NAV_LINKS:
        cls = 'active' if href == active_href else ''
        parts.append(f'<a class="{cls}" href="{href}">{label}</a>')
    parts.append(f'<a class="nav-cta" href="{cta_href}">Inhouse anfragen</a>')
    parts.append('</nav></header>')
    return ''.join(parts)

files = sorted(glob.glob('**/*.html', recursive=True))
changed = []
unmapped = []
no_header = []
for f in files:
    s = open(f, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<header class="site-header">.*?</header>', s, re.S)
    if not m:
        no_header.append(f)
        continue
    key = '/' + f[:-len('index.html')] if f.endswith('index.html') else '/' + f
    if f == 'index.html':
        key = '/'
    if key not in mapping:
        unmapped.append(f)
        continue
    entry = mapping[key]
    new_header = build_header(entry['active'], entry['cta'])
    if new_header != m.group(0):
        changed.append((f, m.group(0), new_header))

print('Dateien gesamt (ohne 404):', len(files) - (1 if '404.html' in files else 0))
print('ohne <header>:', len(no_header))
print('nicht in mapping:', len(unmapped), unmapped)
print('würden geändert:', len(changed))

# Kategorisiere die verbleibenden Diffs
real_concerns = []
for f, old, new in changed:
    old_norm = old.replace('&amp;', '&').replace('<a href=', '<a class="" href=')
    old_norm = re.sub(r'\s+', '', old_norm)
    new_norm = re.sub(r'\s+', '', new)
    if old_norm != new_norm:
        real_concerns.append((f, old, new))

print('davon NICHT durch class=""/whitespace/&-Normalisierung erklärbar:', len(real_concerns))
for f, old, new in real_concerns:
    print('---', f)
    print(' ALT:', old)
    print(' NEU:', new)

if '--apply' in sys.argv:
    applied = 0
    for f, old, new in changed:
        s = open(f, encoding='utf-8').read()
        s2 = s.replace(old, new, 1)
        open(f, 'w', encoding='utf-8').write(s2)
        applied += 1
    print('ANGEWENDET:', applied)
