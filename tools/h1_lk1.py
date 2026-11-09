#!/usr/bin/env python3
"""H1 der LK1-Seite um "Erste Hilfe" ergaenzen (idempotent). Nur die <h1>-Zeile, kein Titel."""
import pathlib, sys
p = pathlib.Path(__file__).resolve().parent.parent / "kurse/lehrkraefte-ausbildung-lk1/index.html"
s = p.read_text(encoding="utf-8")
alt, neu = "<h1>Lehrkräfte-Ausbildung LK1</h1>", "<h1>Lehrkräfte-Ausbildung LK1 für Erste Hilfe</h1>"
if neu in s:
    print("schon gesetzt"); sys.exit(0)
if s.count(alt) != 1:
    sys.exit(f"Erwartet genau 1 Treffer, gefunden {s.count(alt)}")
p.write_text(s.replace(alt, neu), encoding="utf-8")
print("H1 gesetzt")
