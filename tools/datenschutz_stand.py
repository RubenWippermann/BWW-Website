#!/usr/bin/env python3
"""Datenschutzerklärung BWW: 'Stand' auf 09.11.2026 (inhaltliche Änderungen § 10 und § 14), nur in datenschutz/index.html; 'Seite k von 5' bleibt (5 Seitenmarken im Text). Idempotent."""
import os
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read(); n = h.count('Stand: 02.11.2026')
open(f, 'w', encoding='utf8').write(h.replace('Stand: 02.11.2026', 'Stand: 09.11.2026')); print('ersetzt:', n)
