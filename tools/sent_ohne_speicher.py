#!/usr/bin/env python3
"""Doppelsende-Schutz nur im Arbeitsspeicher (kein localStorage, kein Payload im Schlüssel); alte 'bww_sent_*'-Einträge werden einmalig entfernt. Idempotent."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'assets/booking.js'; s = open(f, encoding='utf8').read()
if 'SENT_MEM' in s: print('bereits'); raise SystemExit
a = s.index("  var SENT_PREFIX = 'bww_sent_';"); b = s.index("  function wireForms() {")
NEU = """  var SENT_PREFIX = 'bww_sent_';
  var SENT_TTL_MS = 24 * 60 * 60 * 1000;
  var SENT_MEM = {};   // nur Arbeitsspeicher dieser Seite: kein Browser-Speicher, kein Klartext-Payload (§ 25 TDDDG, Datenminimierung)
  // Alte Einträge früherer Fassungen (Schlüssel enthielt den Anfrage-Inhalt) einmalig vom Gerät entfernen
  try {
    var alt = [];
    for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k && k.indexOf(SENT_PREFIX) === 0) alt.push(k); }
    alt.forEach(function (k) { localStorage.removeItem(k); });
  } catch (e) {}
  function sentKey(apiName, payload) {
    var str = JSON.stringify(payload), h = 5381;
    for (var i = 0; i < str.length; i++) h = ((h << 5) + h + str.charCodeAt(i)) | 0;
    return SENT_PREFIX + apiName + '_' + (h >>> 0).toString(36);
  }
  function readSent(key) {
    var c = SENT_MEM[key];
    if (!c || Date.now() - c.t > SENT_TTL_MS) return null;
    return c;
  }
  function writeSent(key, ticketId) { SENT_MEM[key] = { t: Date.now(), ticket_id: ticketId || '' }; }
"""
s = s[:a] + NEU + s[b:]; open(f, 'w', encoding='utf8').write(s)
tok = hashlib.sha1(s.encode()).hexdigest()[:8]; n = 0
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = re.sub(r'(assets/booking\.js\?v=)[0-9a-f]+', lambda m: m.group(1) + tok, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
print('angewendet; Token', tok, 'Seiten', n)
