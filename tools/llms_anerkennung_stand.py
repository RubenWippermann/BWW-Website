#!/usr/bin/env python3
"""llms-full.txt: die drei Frage/Antwort-Paare zur DGUV-Anerkennung der Lehrbeauftragten-Kurse durch die neutrale Auskunft ersetzen (Jurist); llms.txt/llms-full.txt: Stand-Zeile maschinell auf das Datum des Laufs setzen
(llms.txt ISO, llms-full.txt TT.MM.JJJJ). Idempotent. Arbeitet im Verzeichnis des Aufrufs; Datum per Argument (YYYY-MM-DD) oder heute."""
import datetime, os, re, sys
ROOT = os.getcwd()
d = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
fp = os.path.join(ROOT, 'llms-full.txt'); t = open(fp, encoding='utf8').read()
t, n = re.subn(r'- Frage: Ist der Kurs (?:für Lehrbeauftragte )?eine von der DGUV anerkannte Maßnahme\?\n  Antwort: Nein\.[^\n]*\n',
               lambda m: '- Frage: Wie steht es um die Anerkennung des Kurses' + (' für Lehrbeauftragte' if 'für Lehrbeauftragte' in m.group(0).split('\n')[0] else '') + '?\n  Antwort: Anerkennungsstatus: Auskunft vor Buchung auf Anfrage.\n', t)
t, n2 = re.subn(r'(?m)^Stand: \d{2}\.\d{2}\.\d{4}$', 'Stand: ' + d.strftime('%d.%m.%Y'), t, count=1)
open(fp, 'w', encoding='utf8').write(t)
lp = os.path.join(ROOT, 'llms.txt'); u = open(lp, encoding='utf8').read()
u, n3 = re.subn(r'(?m)^Stand: \d{4}-\d{2}-\d{2}$', 'Stand: ' + d.isoformat(), u, count=1)
open(lp, 'w', encoding='utf8').write(u)
print('Q&A ersetzt:', n, '| Stand llms-full:', n2, '| Stand llms:', n3)
rest = [l for l in t.split('\n') + u.split('\n') if re.search(r'QSEH-Portal registrierte|keine DGUV-Anerkennung|von der DGUV anerkannte', l)]
print('Reste Verneinung:', len(rest))
