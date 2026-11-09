#!/usr/bin/env python3
"""Google-Anzeigen-Kennung: ?quelle=ads-[wdpb] (Allowlist) beim Laden lesen und als Feld 'kennung' an Formular-/Newsletter-/Wartelisten-Anfragen und an Buchungslinks zur Software anhängen. Kein Speicher (kein localStorage/sessionStorage/Cookie), keine Dekoration interner Links. Idempotent."""
import hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'assets/booking.js'; s = open(f, encoding='utf8').read()
if 'KENNUNG' in s: print('bereits'); raise SystemExit
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
rep("  var QUELLE = 'multiplikatorenstelle';",
    "  // Anzeigen-Kennung aus der Adresse (?quelle=ads-w|d|p|b), nur Allowlist, nur im Arbeitsspeicher dieser Seite (kein Speicher, keine Weitergabe an andere Seiten)\n"
    "  var KENNUNG = (function () { var m = /[?&]quelle=(ads-[wdpb])(?:&|$)/.exec(location.search); return m ? m[1] : ''; })();\n"
    "  function mitKennung(u) { return (KENNUNG && u && u.indexOf('kennung=') === -1) ? u + (u.indexOf('?') > -1 ? '&' : '?') + 'kennung=' + KENNUNG : u; }\n"
    "  var QUELLE = 'multiplikatorenstelle';")
rep("    if (window.bwwHerkunft) burl = window.bwwHerkunft(burl);",
    "    burl = mitKennung(burl);\n    if (window.bwwHerkunft) burl = window.bwwHerkunft(burl);")
rep("    if (window.bwwHerkunft) hurl = window.bwwHerkunft(hurl);",
    "    hurl = mitKennung(hurl);\n    if (window.bwwHerkunft) hurl = window.bwwHerkunft(hurl);")
rep("        var payload = { org: ORG, website: '' };",
    "        var payload = { org: ORG, website: '' };\n        if (KENNUNG) payload.kennung = KENNUNG;")
rep("JSON.stringify({ org: ORG, email: nlMail, quelle: QUELLE, website: '' })",
    "JSON.stringify(KENNUNG ? { org: ORG, email: nlMail, quelle: QUELLE, kennung: KENNUNG, website: '' } : { org: ORG, email: nlMail, quelle: QUELLE, website: '' })")
rep("body: JSON.stringify({ org: ORG, quelle: QUELLE, termin: o.dataset.termin || '', name: name, email: email, website: '' })",
    "body: JSON.stringify(KENNUNG ? { org: ORG, quelle: QUELLE, kennung: KENNUNG, termin: o.dataset.termin || '', name: name, email: email, website: '' } : { org: ORG, quelle: QUELLE, termin: o.dataset.termin || '', name: name, email: email, website: '' })")
# feste Buchungslinks im HTML (software-wippermann.de/buchen) beim Laden ergänzen
rep("  var KENNUNG = (function () {", "  var KENNUNG = (function () {")
s = s.rstrip('\n') + "\n// Feste Buchungslinks zur Software ergänzen (nur mit gültiger Kennung)\n(function () { if (!/[?&]quelle=ads-[wdpb](?:&|$)/.test(location.search)) return; function run() { var k = /[?&]quelle=(ads-[wdpb])(?:&|$)/.exec(location.search)[1]; Array.prototype.forEach.call(document.querySelectorAll('a[href*=\"software-wippermann.de/buchen\"]'), function (a) { var u = a.getAttribute('href'); if (u.indexOf('kennung=') === -1) a.setAttribute('href', u + (u.indexOf('?') > -1 ? '&' : '?') + 'kennung=' + k); }); } if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run(); })();\n"
open(f, 'w', encoding='utf8').write(s)
tok = hashlib.sha1(s.encode()).hexdigest()[:8]; n = 0
import glob
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = re.sub(r'(assets/booking\.js\?v=)[0-9a-f]+', lambda m: m.group(1) + tok, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
print('angewendet; Token', tok, 'Seiten', n)
