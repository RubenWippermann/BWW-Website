#!/usr/bin/env python3
"""booking.js: Zeitgrenze (30 s) fuer die Formular-POSTs (Anfrage/Kontakt/Widerruf/Dozent und Warteliste). Ohne Grenze bleibt der Knopf bei haengender Verbindung dauerhaft auf "Wird gesendet ...". Bei Abbruch durch die Zeitgrenze (AbortError) erscheint ein Text, der NICHT zum erneuten Senden auffordert (Entscheid BL 10.11.); andere Netzfehler behalten die bisherige Meldung. Idempotent; setzt ?v-Token neu."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'assets/booking.js'; s = open(f, encoding='utf8').read()
if 'function mitZeit' in s: print('bereits'); raise SystemExit
anker = "  function mitKennung(u)"
assert s.count(anker) == 1
helfer = "  function mitZeit(o) { if (window.AbortController) { var c = new AbortController(); setTimeout(function () { c.abort(); }, 30000); o.signal = c.signal; } return o; }   // Zeitgrenze 30 s, danach greift die Fehlermeldung mit Telefonnummer\n"
s = s.replace(anker, helfer + anker, 1)
a1 = "fetch(API + '/api/' + form.getAttribute('data-api'), {\n          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)\n        })"
b1 = "fetch(API + '/api/' + form.getAttribute('data-api'), mitZeit({\n          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)\n        }))"
assert s.count(a1) == 1; s = s.replace(a1, b1)
i = s.index("fetch(API + '/api/warteliste', {"); j = s.index("}).then(", i)
s = s[:i] + "fetch(API + '/api/warteliste', mitZeit({" + s[i+len("fetch(API + '/api/warteliste', {"):j] + "})).then(" + s[j+len("}).then("):]
ABBR = "(e && e.name === 'AbortError') ? 'Wir haben keine Antwort erhalten. Ihre Anfrage ist möglicherweise angekommen. Bitte prüfen Sie Ihr Postfach oder rufen Sie uns an, bevor Sie erneut senden. Telefon: ' + TEL : "
for kopf, cls in (("}).catch(function () {\n          if (status) { status.className = 'form-status is-error'; status.textContent = ", None), ("}).catch(function () {\n        status.className = 'wl-status is-error'; status.textContent = ", None)):
    assert s.count(kopf) == 1, kopf
    s = s.replace(kopf, kopf.replace("catch(function ()", "catch(function (e)") + ABBR)
open(f, 'w', encoding='utf8').write(s)
tok = hashlib.sha1(s.encode()).hexdigest()[:8]; n = 0
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read(); h2 = re.sub(r'(assets/booking\.js\?v=)[0-9a-f]+', lambda m: m.group(1) + tok, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
print('angewendet; Token', tok, 'Seiten', n)
