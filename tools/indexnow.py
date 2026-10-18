#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IndexNow-Meldung nur fuer GEAENDERTE URLs (Bing, Yandex u. a.).

Standard ist --dry-run: es wird nur angezeigt, was gemeldet wuerde. Gesendet wird ausschliesslich
mit --senden. Dieses Skript ist NICHT in den Build/Deploy eingehaengt; Aufruf nur von Hand.

Welche URLs gelten als geaendert?
  * Stand-Datei tools/indexnow-stand.txt (wird nach erfolgreichem Senden geschrieben) oder --seit WERT.
  * WERT = Datum JJJJ-MM-TT  -> alle Sitemap-URLs mit lastmod >= Datum.
  * WERT = Git-Revision      -> Dateien aus `git diff --name-only WERT..HEAD`, auf Sitemap-URLs abgebildet
                                (Seiten ausserhalb der Sitemap, z. B. noindex, werden nie gemeldet).
Ohne Stand und ohne --seit bricht das Skript ab (kein stilles "alles senden").

Sicherungen: Host-Pruefung (alle URLs muessen zu HOST gehoeren), Obergrenze 10000 URLs,
Schluesseldatei muss im Wurzelverzeichnis der Site liegen und ihr Inhalt dem Schluessel entsprechen.

    python3 tools/indexnow.py                  # Trockenlauf mit Stand-Datei
    python3 tools/indexnow.py --seit 2026-10-18
    python3 tools/indexnow.py --seit <commit>  # Git-Modus
    python3 tools/indexnow.py --senden         # echt senden (nur nach Deploy!)
"""
import argparse, datetime, json, os, re, subprocess, sys, urllib.error, urllib.request

HOST = "www.multiplikatorenstelle.de"
KEY = "a3417f9234310f7574d865bbeddb85ac"
ENDPUNKT = "https://api.indexnow.org/indexnow"
MAX_URLS = 10000
SITE_IM_GIT = True          # True: Site-Dateien liegen in diesem Repo (Git-Modus moeglich)

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
STAND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "indexnow-stand.txt")


def sitemap_eintraege(sitemap):
    with open(sitemap, encoding="utf-8") as fh:
        xml = fh.read()
    out = []
    for blk in re.findall(r"<url>(.*?)</url>", xml, re.S):
        loc = re.search(r"<loc>\s*([^<\s]+)\s*</loc>", blk)
        lm = re.search(r"<lastmod>\s*([^<\s]+)\s*</lastmod>", blk)
        if loc:
            out.append((loc.group(1), lm.group(1)[:10] if lm else ""))
    return out


def datei_zu_url(pfad):
    if pfad.endswith("index.html"):
        pfad = pfad[: -len("index.html")]
    return f"https://{HOST}/{pfad}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--senden", action="store_true", help="echt senden (sonst Trockenlauf)")
    ap.add_argument("--dry-run", action="store_true", help="Trockenlauf (Standard)")
    ap.add_argument("--seit", help="Datum JJJJ-MM-TT oder Git-Revision")
    ap.add_argument("--site", default=os.path.join(REPO, "."), help="Wurzel der ausgelieferten Site")
    a = ap.parse_args()
    if a.senden and a.dry_run:
        print("! --senden und --dry-run schliessen sich aus"); return 2

    seit = a.seit
    if not seit and os.path.exists(STAND):
        seit = open(STAND, encoding="utf-8").read().strip()
    if not seit:
        print("! Kein Stand (tools/indexnow-stand.txt fehlt) und kein --seit angegeben. Nichts gemeldet.")
        return 2

    sm = os.path.join(a.site, "sitemap.xml")
    if not os.path.exists(sm):
        print(f"! Keine sitemap.xml unter {a.site} (mit --site angeben)"); return 2
    eintraege = sitemap_eintraege(sm)
    in_sitemap = {u for u, _ in eintraege}

    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", seit):
        urls = [u for u, lm in eintraege if lm and lm >= seit]
        modus = f"lastmod >= {seit}"
        neuer_stand = datetime.date.today().isoformat()
    else:
        if not SITE_IM_GIT:
            print("! Git-Modus nicht verfuegbar (Site liegt nicht in diesem Repo); --seit JJJJ-MM-TT nutzen."); return 2
        r = subprocess.run(["git", "-C", REPO, "diff", "--name-only", f"{seit}..HEAD"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("! git diff fehlgeschlagen:", r.stderr.strip()[:200]); return 2
        urls = sorted({datei_zu_url(p) for p in r.stdout.split("\n") if p.endswith(".html")} & in_sitemap)
        modus = f"git diff {seit[:12]}..HEAD"
        neuer_stand = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"],
                                     capture_output=True, text=True).stdout.strip()

    fremd = [u for u in urls if re.sub(r"^https?://([^/]+).*", r"\1", u) != HOST]
    if fremd:
        print(f"! Host-Pruefung: {len(fremd)} URL(s) nicht auf {HOST}, z. B. {fremd[0]} -- Abbruch"); return 2
    if len(urls) > MAX_URLS:
        print(f"! {len(urls)} URLs > Obergrenze {MAX_URLS} -- Abbruch"); return 2

    kf = os.path.join(a.site, KEY + ".txt")
    if os.path.exists(kf):
        if open(kf, encoding="utf-8").read().strip() != KEY:
            print(f"! Inhalt von {KEY}.txt passt nicht zum Schluessel -- Abbruch"); return 2
    else:
        print(f"  (Hinweis: {KEY}.txt nicht unter {a.site} gefunden, Pruefung uebersprungen)")

    print(f"Modus: {modus} | Host: {HOST} | URLs: {len(urls)} | {'SENDEN' if a.senden else 'TROCKENLAUF'}")
    for u in urls[:50]:
        print("  ", u)
    if len(urls) > 50:
        print(f"   ... und {len(urls) - 50} weitere")
    if not urls:
        print("Nichts zu melden."); return 0
    if not a.senden:
        print("Trockenlauf: nichts gesendet. Mit --senden echt senden."); return 0

    rumpf = {"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}
    req = urllib.request.Request(ENDPUNKT, data=json.dumps(rumpf).encode("utf-8"),
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            gut = r.status in (200, 202)
            print(f"IndexNow: HTTP {r.status} -- {len(urls)} URLs gemeldet")
    except urllib.error.HTTPError as e:
        print(f"! IndexNow: HTTP {e.code} -- nicht angenommen"); return 1
    except Exception as e:
        print(f"! IndexNow nicht erreichbar: {e}"); return 1
    if gut:
        with open(STAND, "w", encoding="utf-8") as fh:
            fh.write(neuer_stand + "\n")
    return 0 if gut else 1


if __name__ == "__main__":
    sys.exit(main())
