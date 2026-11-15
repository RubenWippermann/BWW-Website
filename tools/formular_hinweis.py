#!/usr/bin/env python3
"""Formulare: Pflicht-Einwilligungs-Haekchen (name=consent) der data-api-Formulare entfernt, Hinweistext (Wortlaut Jurist 13.11., Du-Fassung) unter dem Absenden-Button;
Widerruf: Nachricht optional (API verlangt nachricht, booking.js setzt bei leerem Feld technisch 'Widerruf'); Newsletter-Haekchen mit Firma konkret (Wortlaut Jurist). zertifikat-duplikat und Warteliste-Modal unveraendert. Idempotent."""
import glob, hashlib, os, re
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
A = '<a href="/datenschutz/" target="_blank" rel="noopener">Datenschutzerklärung</a>'
T = {
 'kontakt': 'Wir verwenden deine Angaben nur, um deine Anfrage zu beantworten (Art. 6 Abs. 1 lit. b, f DSGVO). Mehr dazu in der ' + A + '.',
 'inhouse-anfrage': 'Wir verwenden deine Angaben nur, um dein Angebot zu erstellen und deine Anfrage zu beantworten (Art. 6 Abs. 1 lit. b DSGVO). Mehr dazu in der ' + A + '.',
 'dozent-bewerbung': 'Wir verwenden deine Angaben nur zur Bearbeitung deiner Bewerbung (Art. 6 Abs. 1 lit. b DSGVO i.&nbsp;V.&nbsp;m. § 26 BDSG). Bei einer Absage löschen wir deine Unterlagen in der Regel nach sechs Monaten. Mehr dazu in der ' + A + '.',
 'widerruf': 'Wir verwenden deine Angaben nur, um deinen Widerruf zu bearbeiten und zu bestätigen (Art. 6 Abs. 1 lit. b, c DSGVO). Mehr dazu in der ' + A + '.',
}
NL_ALT = '<span>Ja, schickt mir gelegentlich Kurs-Infos &amp; Neuigkeiten per E-Mail (jederzeit abbestellbar).</span>'
NL_NEU = '<span>Ja, ich möchte per E-Mail Informationen und Neuigkeiten zu Kursen der BWW UG (haftungsbeschränkt) erhalten. Ich kann das jederzeit widerrufen, z.&nbsp;B. über den Abmeldelink in jeder Mail.</span>'
CONS = re.compile(r'<label class="consent full"><input type="checkbox" name="consent" required><span>Ich habe die <a [^>]*>Datenschutzerklärung</a> gelesen und stimme der Verarbeitung meiner Daten[^<]*</span></label>')
FORM = re.compile(r'(<form[^>]*data-api="([^"]+)"[^>]*>)(.*?)(</form>)', re.S)
n = 0
for p in glob.glob('**/*.html', recursive=True):
    if p.startswith('tools/'): continue
    h = open(p, encoding='utf8').read()
    def fix(m):
        api, body = m.group(2), m.group(3)
        if api not in T or 'form-note' in body: return m.group(0)
        body, k = CONS.subn('', body); assert k == 1, (p, api, k)
        ins = lambda x: x.group(1) + '<p class="form-note full">' + T[api] + '</p>' + x.group(2)
        body, k = re.subn(r'(<div class="form-actions">.*?</div>)(<div class="form-status">)', ins, body, count=1, flags=re.S)
        if k != 1: body, k = re.subn(r'(<button class="btn primary" type="submit">[^<]*</button>)(<div class="form-status">)', ins, body, count=1)
        assert k == 1, (p, 'actions')
        body = body.replace(NL_ALT, NL_NEU)
        if api == 'widerruf':
            a = '<label class="full" for="w-msg">Nachricht / Grund *</label><textarea id="w-msg" class="full" name="nachricht" required placeholder='
            assert a in body; body = body.replace(a, '<label class="full" for="w-msg">Nachricht (optional)</label><textarea id="w-msg" class="full" name="nachricht" placeholder=')
        return m.group(1) + body + m.group(4)
    h2 = FORM.sub(fix, h)
    if h2 != h: open(p, 'w', encoding='utf8').write(h2); n += 1
print('Seiten:', n)
f = 'assets/booking.js'; s = open(f, encoding='utf8').read()
if "payload.nachricht = 'Widerruf'" not in s:
    k = '        var dupKey = sentKey('; assert s.count(k) == 1
    s = s.replace(k, "        if (form.getAttribute('data-api') === 'widerruf' && !String(payload.nachricht || '').trim()) payload.nachricht = 'Widerruf';   // API verlangt eine Nachricht; Feld ist im Formular optional\n" + k)
    open(f, 'w', encoding='utf8').write(s)
f = 'assets/styles.css'; s = open(f, encoding='utf8').read()
if '.form-note' not in s:
    s += '\n/* Formular-Hinweis (Art. 13) */\n.form-note{font-size:.875rem;line-height:1.5;color:#5b6e64;margin:.8rem 0 0}.form-note a{color:inherit;text-decoration:underline}\n@media (prefers-color-scheme: dark){.form-note{color:var(--ad-ink-3)}}\n'
    open(f, 'w', encoding='utf8').write(s)
def tok(fn):
    c = hashlib.sha1(open(fn, 'rb').read()).hexdigest()[:8]; m = 0
    pat = re.compile(r'(assets/' + re.escape(os.path.basename(fn)) + r'\?v=)[0-9a-zA-Z]+')
    for p in glob.glob('**/*.html', recursive=True):
        if p.startswith('tools/'): continue
        h = open(p, encoding='utf8').read(); h2 = pat.sub(lambda x: x.group(1) + c, h)
        if h2 != h: open(p, 'w', encoding='utf8').write(h2); m += 1
    print(fn, c, m)
tok('assets/styles.css'); tok('assets/booking.js')
