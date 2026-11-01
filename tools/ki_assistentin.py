#!/usr/bin/env python3
"""'digitale Assistentin' -> 'KI-Assistentin' (Jurist 01.11.: Transparenz, es ist ein KI-Telefonassistent). Idempotent."""
import glob
n = 0
for f in glob.glob('**/index.html', recursive=True) + ['404.html', 'llms.txt', 'llms-full.txt']:
    try: h = open(f, encoding='utf8').read()
    except FileNotFoundError: continue
    if 'digitale Assistentin' in h:
        open(f, 'w', encoding='utf8').write(h.replace('digitale Assistentin', 'KI-Assistentin')); n += 1
print('geändert:', n)
