#!/usr/bin/env python3
"""Neutralisiert 'deutschlandweit'/'bundesweit' im Inhouse-Bezug (Jurist Nr. 116/2, BL 23.11.2026):
Einsatzgebiet nur mit Beleg im Bescheid -> 'Orte nach Absprache'. Idempotent; Drittaussagen (Traeger, QSEH, Warntag)
bleiben. Aufruf: python3 tools/deutschlandweit_neutralisieren.py [--dry]"""
import os, re, sys
DRY = '--dry' in sys.argv
O = 'Orte nach Absprache'
R = [
 (r'vor Ort – deutschlandweit', 'vor Ort (%s)' % O),
 (r'Wir kommen deutschlandweit direkt zu euch', 'Wir kommen direkt zu euch (%s)' % O),
 (r'Wir kommen deutschlandweit zu euch', 'Wir kommen zu euch (%s)' % O),
 (r'als Inhouse-Kurs, deutschlandweit', 'als Inhouse-Kurs (%s)' % O),
 (r'Vereine, deutschlandweit', 'Vereine (%s)' % O),
 (r'bei euch vor Ort, deutschlandweit, ermächtigt', 'bei euch vor Ort (%s), ermächtigt' % O),
 (r'Deutschlandweit &amp; inhouse vor Ort', 'Inhouse vor Ort (%s)' % O),
 (r'Deutschlandweit & inhouse vor Ort', 'Inhouse vor Ort (%s)' % O),
 (r'Inhouse Erste-Hilfe-Kurse deutschlandweit', 'Inhouse Erste-Hilfe-Kurse (%s)' % O),
 (r'Inhouse-Erste-Hilfe-Kurse deutschlandweit', 'Inhouse-Erste-Hilfe-Kurse (%s)' % O),
 (r'Erste-Hilfe-Kurse als Inhouse-Schulung deutschlandweit', 'Erste-Hilfe-Kurse als Inhouse-Schulung (%s)' % O),
 (r'Inhouse-Kurse deutschlandweit', 'Inhouse-Kurse (%s)' % O),
 (r'Inhouse deutschlandweit', 'Inhouse (%s)' % O),
 (r'abrechenbar, deutschlandweit', 'abrechenbar, %s' % O),
 (r'inhouse bundesweit', 'inhouse (%s)' % O),
 (r'Inhouse bundesweit', 'Inhouse (%s)' % O),
 (r'bundesweit als Inhouse-Schulung tätig', 'als Inhouse-Schulung tätig (%s)' % O),
 (r'bundesweit als Inhouse-Schulung', 'als Inhouse-Schulung (%s)' % O),
 (r'Bundesweit inhouse:', 'Inhouse (%s):' % O),
 (r'Inhouse-Kurse in (\d+) Städten deutschlandweit', r'Inhouse-Kurse in \1 Städten (%s)' % O),
 (r'deutschlandweit und inhouse', 'inhouse (%s)' % O),
 (r'praxisnah und deutschlandweit', 'praxisnah (%s)' % O),
 (r'deutschlandweit als Inhouse-Kurs', 'als Inhouse-Kurs (%s)' % O),
 (r'inhouse deutschlandweit oder', 'inhouse (%s) oder' % O),
 (r'Wir bilden betriebliche Ersthelfer deutschlandweit bei euch', 'Wir bilden betriebliche Ersthelfer bei euch (%s)' % O),
 (r'Wir arbeiten bundesweit und kommen zu euch', 'Wir kommen zu euch (%s)' % O),
 (r'Wir sind bundesweit im Einsatz und kommen zu euch', 'Wir kommen zu euch (%s)' % O),
 (r'durch – bundesweit und damit auch bei euch in', 'durch – bei euch vor Ort (%s), auch in' % O),
 (r'deutschlandweit – BWW führt', '%s – BWW führt' % O),
 (r'\(im Betrieb, deutschlandweit\)', '(im Betrieb, %s)' % O),
 (r'für Unternehmen, Schulen, Kitas und Vereine, deutschlandweit', 'für Unternehmen, Schulen, Kitas und Vereine (%s)' % O),
 (r'BWW: Erste Hilfe & Brandschutz inhouse, deutschlandweit', 'BWW: Erste Hilfe & Brandschutz inhouse (%s)' % O),
 (r'Kitas deutschlandweit in Erster Hilfe', 'Kitas in Erster Hilfe'),
 (r'Kommt ihr wirklich deutschlandweit zu uns\?', 'Kommt ihr auch zu uns vor Ort?'),
 (r'Wohin kommt BWW für Inhouse-Kurse\?', 'Wohin kommt BWW für Inhouse-Kurse?'),
 (r'– deutschlandweit, zum Wunschtermin', '– %s, zum Wunschtermin' % O),
 (r'Verwaltungen und Vereine – deutschlandweit', 'Verwaltungen und Vereine (%s)' % O),
 (r'Inhouse-Kurse: deutschlandweit direkt beim Kunden', 'Inhouse-Kurse: direkt beim Kunden (%s)' % O),
 (r'Schulungen direkt bei euch vor Ort, deutschlandweit\.', 'Schulungen direkt bei euch vor Ort (%s).' % O),
 (r'\(8\.2122\), bundesweit Inhouse\.', '(8.2122), Inhouse vor Ort (%s).' % O),
 (r'über BG/UK abrechenbar, deutschlandweit', 'über BG/UK abrechenbar, %s' % O),
]
EXC = re.compile(r'zuständige Branchen|führt bundesweit 11|bundesweite Warntag|SVLFG|svlfg|Bundesweit einziger|Bundesweit: |bundesweit: |bundesweit bei der|nicht nach Bundesland|unfallkassen/bundesweit|bundesweit zuständige', re.I)
n = 0; files = 0
for dp, dn, fs in os.walk('.'):
    if '.git' in dp or dp.startswith('./tools'): continue
    for f in fs:
        if not f.endswith(('.html', '.txt')): continue
        p = os.path.join(dp, f)
        try: t = open(p, encoding='utf-8').read()
        except Exception: continue
        u = t
        for a, b in R: u = re.sub(a, b, u)
        if u != t:
            files += 1; n += sum(1 for _ in re.finditer('|'.join(a for a, _ in R), t))
            if not DRY: open(p, 'w', encoding='utf-8').write(u)
print('Dateien', files, 'Ersetzungen', n)
rest = []
for dp, dn, fs in os.walk('.'):
    if '.git' in dp or dp.startswith('./tools'): continue
    for f in fs:
        if f.endswith(('.html', '.txt')):
            p = os.path.join(dp, f)
            try: t = open(p, encoding='utf-8').read()
            except Exception: continue
            for m in re.finditer(r'(?i)deutschlandweit\w*|bundesweit\w*', t):
                ctx = t[max(0, m.start()-60):m.end()+60].replace('\n', ' ')
                if not EXC.search(ctx): rest.append((p, ctx))
print('Rest ohne Ausnahme:', len(rest))
for p, c in rest[:40]: print(' ', p, '|', c)
