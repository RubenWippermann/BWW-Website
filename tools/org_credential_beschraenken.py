#!/usr/bin/env python3
"""VARIANTE (nicht gebaut): hasCredential (Ermaechtigung EH/QSEH, 8.2122) im Organization-JSON-LD nur auf Start + EH-Ausbildungs-/Fortbildungsseiten behalten, sonst entfernen.
Standard: Trockenlauf (zaehlt und listet je Seitengruppe). Mit --write wird geschrieben. Arbeitet im Verzeichnis des Aufrufs. Idempotent."""
import collections, glob, json, os, re, sys
ROOT = os.getcwd(); WRITE = '--write' in sys.argv
AUSNAHME = {a.split('=',1)[1] for a in sys.argv if a.startswith('--ohne=')}   # Seiten, die NICHT angefasst werden (Messseite)
NUR = {a.split('=',1)[1] for a in sys.argv if a.startswith('--nur=')}       # nur diese Seiten
BEHALTEN = {'index.html', 'kurse/erste-hilfe-ausbildung/index.html', 'kurse/erste-hilfe-fortbildung/index.html'}
def ohne(o):
    """hasCredential rekursiv entfernen (auch verschachtelt, z. B. Course.provider)."""
    if isinstance(o, dict): return {k: ohne(v) for k, v in o.items() if k != 'hasCredential'}
    if isinstance(o, list): return [ohne(x) for x in o]
    return o
def hat(o):
    if isinstance(o, dict): return 'hasCredential' in o or any(hat(v) for v in o.values())
    if isinstance(o, list): return any(hat(x) for x in o)
    return False
SSTART, SEND = '<!-- BWW-FEED-COURSE:STATIC ', ' -->'
grp = collections.Counter(); n_bhl = 0; ents = []
for p in sorted(set(glob.glob('**/index.html', recursive=True) + ['index.html'])):
    if p.startswith('tools/') or p in AUSNAHME or (NUR and p not in NUR): continue
    h = open(os.path.join(ROOT, p), encoding='utf8').read(); h0 = h
    for m in list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)):
        j = json.loads(m.group(1))
        if hat(j):
            if p in BEHALTEN: n_bhl += 1; continue
            raw = m.group(1); indent = 1 if raw.lstrip().startswith('{\n') else None
            neu = json.dumps(ohne(j), ensure_ascii=False, **({'indent': 1} if indent else {'separators': (',', ':')}))
            h = h.replace(m.group(0), '<script type="application/ld+json">' + (('\n' + neu + '\n') if indent else neu) + '</script>', 1)
    mm = re.search(re.escape(SSTART) + r'(.*?)' + re.escape(SEND), h, re.S)   # gebackener STATIC-Marker des Generators
    if mm and p not in BEHALTEN:
        try:
            j = json.loads(mm.group(1))
            if hat(j): h = h.replace(mm.group(0), SSTART + json.dumps(ohne(j), ensure_ascii=False).replace('--', '\\u002d\\u002d') + SEND, 1)
        except Exception: pass
    if h != h0:
        ents.append(p); grp[p.split('/')[0] if '/' in p else '(Wurzel)'] += 1
        if WRITE: open(os.path.join(ROOT, p), 'w', encoding='utf8').write(h)
print(('GESCHRIEBEN' if WRITE else 'TROCKENLAUF'), '| Block entfällt auf', len(ents), 'Seiten | bleibt auf', n_bhl, 'Seiten')
for g, c in grp.most_common(): print(f'  {g}: {c}')
