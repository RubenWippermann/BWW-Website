#!/usr/bin/env python3
"""Datenschutzerklärung BWW: 'Stand' 13.11.2026 -> 15.11.2026 (Pushtag laut BL), nur datenschutz/index.html. Idempotent."""
import os
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read(); n = h.count('Stand: 13.11.2026')
open(f, 'w', encoding='utf8').write(h.replace('Stand: 13.11.2026', 'Stand: 15.11.2026')); print('ersetzt:', n)
