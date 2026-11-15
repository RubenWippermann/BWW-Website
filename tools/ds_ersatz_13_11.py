#!/usr/bin/env python3
"""Jurist-Ersatztexte BWW 13.11. (wortlaut-ds-ersatztexte-…-13-11.md, Abschnitt BWW; Entwurf, Vorbehalt Anwalt), idempotent:
(1) DSE § 4.2 Rechtsgrundlage lit. b/f statt lit. a; neuer Absatz 'Duplikat der Teilnahmebescheinigung' am Ende von § 16; Stand 13.11.2026
(2) Warteliste-Modal (booking.js): Pflicht-Haekchen -> Hinweis (Du-Fassung), Meldung 'Bitte Name und E-Mail ausfuellen.'
(3) /zertifikat-duplikat/: Datenschutz-Haekchen entfaellt + Hinweis; Erlöschens-Häkchen mit Wortlaut der Datei (bleibt Pflicht); Button 'Zahlungspflichtig bestellen'.
Nicht eingebaut: Speicherdauer Warteliste (30 Tage) bis BL bestaetigt."""
import glob, hashlib, os, re, textwrap
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
A = '<a href="/datenschutz/" target="_blank" rel="noopener">Datenschutzerklärung</a>'
# ---- (1) DSE
f = 'datenschutz/index.html'; h = open(f, encoding='utf8').read()
alt42 = re.search(r'4\.2 Die Rechtsgrundlage für die Verarbeitung dieser Daten ist bei Vorliegen einer Einwilligung Art\. 6 Abs\. 1\n.*?Abs\. 1 lit\. b DSGVO\.\n', h, re.S)
NEU42 = ('4.2 Die Rechtsgrundlage für die Verarbeitung dieser Daten ist Art. 6 Abs. 1 lit. b DSGVO, wenn die Kontaktaufnahme auf den Abschluss oder die Durchführung eines Vertrages abzielt '
         '(z. B. Anfrage zu einer Strukturberatung oder einer Inhouse-Schulung), im Übrigen Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Beantwortung von Anfragen). '
         'Eine Einwilligung ist dafür nicht erforderlich.')
if alt42:
    h = h.replace(alt42.group(0), '\n'.join(textwrap.wrap(NEU42, 108, break_long_words=False, break_on_hyphens=False)) + '\n', 1)
DUP = ('<b>Duplikat der Teilnahmebescheinigung.</b> Wenn Sie ein Duplikat anfordern, verarbeiten wir Ihren Namen, Ihr Geburtsdatum, Ihre Kursdaten und Ihre Kontaktdaten, um die Bescheinigung zuzuordnen, '
       'auszustellen und zuzusenden, sowie die Zahlungsdaten über unseren Zahlungsdienstleister (Art. 6 Abs. 1 lit. b DSGVO). Die Angaben bewahren wir entsprechend den Aufbewahrungsfristen auf (siehe § 16).')
if 'Duplikat der Teilnahmebescheinigung.</b>' not in h:
    K = '§ 16 Kursabwicklung und Teilnahmebescheinigung\n'; a = h.index(K) + len(K); b = h.index('BWW UG (haftungsbeschränkt) — Datenschutzerklärung (Stand:', a)
    z = textwrap.wrap(DUP.replace('<b>Duplikat der Teilnahmebescheinigung.</b>', 'KOPFXX', 1), 108, break_long_words=False, break_on_hyphens=False)
    h = h[:b] + '\n'.join(z).replace('KOPFXX', '<b>Duplikat der Teilnahmebescheinigung.</b>', 1) + '\n' + h[b:]
h = h.replace('Stand: 10.11.2026', 'Stand: 13.11.2026')
open(f, 'w', encoding='utf8').write(h)
# ---- (2) Warteliste-Modal
f = 'assets/booking.js'; s = open(f, encoding='utf8').read()
if 'wl-note' not in s:
    c = """          '<label class="wl-consent"><input type="checkbox" name="consent" required><span>Ich habe die <a href="/datenschutz/" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen und stimme der Verarbeitung meiner Daten zu.</span></label>' +\n"""
    assert s.count(c) == 1; s = s.replace(c, '')
    b = """          '<button type="submit" class="btn primary">Eintragen</button>' +\n"""
    assert s.count(b) == 1
    s = s.replace(b, b + """          '<p class="wl-note">Wir verwenden deine Angaben nur, um dich zu benachrichtigen, wenn ein Platz frei wird (Art. 6 Abs. 1 lit. b DSGVO). Mehr dazu in der <a href="/datenschutz/" target="_blank" rel="noopener">Datenschutzerklärung</a>.</p>' +\n""")
    v = "      var consent = form.querySelector('input[name=\"consent\"]').checked;\n"
    assert s.count(v) == 1; s = s.replace(v, '')
    m = "      if (!name || !email || !consent) { status.className = 'wl-status is-error'; status.textContent = 'Bitte Name, E-Mail und Einwilligung ausfüllen.'; return; }"
    assert s.count(m) == 1; s = s.replace(m, "      if (!name || !email) { status.className = 'wl-status is-error'; status.textContent = 'Bitte Name und E-Mail ausfüllen.'; return; }")
    open(f, 'w', encoding='utf8').write(s)
# ---- (3) Zertifikat-Duplikat
f = 'zertifikat-duplikat/index.html'; h = open(f, encoding='utf8').read()
if 'form-note' not in h:
    c = re.search(r'<label class="consent full"><input type="checkbox" name="consent" required>.*?</label>', h, re.S); assert c; h = h.replace(c.group(0), '', 1)
    w = re.search(r'(<label class="consent full"><input type="checkbox" name="widerruf_verzicht" required><span>).*?(</span></label>)', h, re.S); assert w
    h = h.replace(w.group(0), w.group(1) + 'Ich verlange ausdrücklich, dass vor Ablauf der Widerrufsfrist mit der Ausstellung des Duplikats begonnen wird. Mir ist bekannt, dass ein etwaiges Widerrufsrecht erlischt, sobald die Leistung vollständig erbracht ist (§ 356 Abs. 4 BGB), und dass ich bei einem Widerruf vor Vollerbringung den Wert der bis dahin erbrachten Leistung zu bezahlen habe (§ 357a BGB).' + w.group(2), 1)
    bt = 'id="zd-submit" disabled>Duplikat kostenpflichtig anfordern</button>'; assert h.count(bt) == 1; h = h.replace(bt, 'id="zd-submit" disabled>Zahlungspflichtig bestellen</button>')
    st = '<p class="form-status" id="zd-status"'; assert h.count(st) == 1
    h = h.replace(st, '<p class="form-note full">Zur Ausstellung des Duplikats verwenden wir deinen Namen, dein Geburtsdatum und die Kursdaten nur, um die Bescheinigung zu finden, auszustellen und zuzusenden (Art. 6 Abs. 1 lit. b DSGVO). Mehr dazu in der ' + A + '.</p>' + st)
    open(f, 'w', encoding='utf8').write(h)
# ---- CSS + Token
f = 'assets/styles.css'; s = open(f, encoding='utf8').read()
if '.wl-note' not in s:
    s += '.wl-note{font-size:.875rem;line-height:1.5;color:#5b6e64;margin:.8rem 0 0}.wl-note a{color:inherit;text-decoration:underline}\n@media (prefers-color-scheme: dark){.wl-note{color:var(--ad-ink-3)}}\n'
    open(f, 'w', encoding='utf8').write(s)
def tok(fn):
    c = hashlib.sha1(open(fn, 'rb').read()).hexdigest()[:8]; m = 0
    pat = re.compile(r'(assets/' + re.escape(os.path.basename(fn)) + r'\?v=)[0-9a-zA-Z]+')
    for p in glob.glob('**/*.html', recursive=True):
        if p.startswith('tools/'): continue
        t = open(p, encoding='utf8').read(); t2 = pat.sub(lambda x: x.group(1) + c, t)
        if t2 != t: open(p, 'w', encoding='utf8').write(t2); m += 1
    print(fn, c, m)
tok('assets/styles.css'); tok('assets/booking.js')
