#!/usr/bin/env python3
"""Schema hasCredential.recognizedBy: QSEH bei der VBG statt DGUV (Jurist 01.11.). Idempotent."""
import glob
OLD = '"recognizedBy":{"@type":"Organization","name":"Deutsche Gesetzliche Unfallversicherung (DGUV)","url":"https://www.dguv.de/"}'
NEW = '"recognizedBy":{"@type":"Organization","name":"Qualitätssicherungsstelle Erste Hilfe (QSEH) der gesetzlichen Unfallversicherungsträger bei der VBG"}'
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['404.html']:
    try: h = open(f, encoding='utf8').read()
    except FileNotFoundError: continue
    if OLD in h: open(f, 'w', encoding='utf8').write(h.replace(OLD, NEW)); n += 1
print('geändert:', n)
