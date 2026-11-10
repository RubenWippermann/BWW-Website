#!/usr/bin/env python3
"""Datenschutzerklärung BWW: 'Stand' 09.11.2026 -> 10.11.2026 (Ergänzung § 16), nur datenschutz/index.html. Idempotent."""
import os
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read(); n = h.count('Stand: 09.11.2026')
open(f, 'w', encoding='utf8').write(h.replace('Stand: 09.11.2026', 'Stand: 10.11.2026')); print('ersetzt:', n)
