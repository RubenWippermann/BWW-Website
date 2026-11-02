#!/usr/bin/env python3
"""Seiten-Audit Rest (BL-Entscheidung 02.11.): Startseiten-H1 mit Themenwort, /kontakt/ ausbauen (nur belegte Angaben), /inhouse-kurse/ H1. Rechtsseiten 0. Idempotent."""
n = 0
def rw(f, fn):
    global n
    h = open(f, encoding='utf8').read(); o = h; h = fn(h)
    if h != o: open(f, 'w', encoding='utf8').write(h); n += 1
rw('index.html', lambda h: h.replace('<h1>Erste-Hilfe-Kurse inhouse: Leben retten – <span class="hl-green">leicht gemacht.</span></h1>', '<h1>Leben retten – <span class="hl-green">leicht gemacht.</span></h1>').replace('<h1>Leben retten – <span class="hl-green">leicht gemacht.</span></h1>', '<h1><span class="h1-kw">Erste-Hilfe-Kurse inhouse</span> Leben retten – <span class="hl-green">leicht gemacht.</span></h1>'))
rw('inhouse-kurse/index.html', lambda h: h.replace('<h1>Inhouse-Kurse für Erste Hilfe und Brandschutz: Wir kommen zu euch — mit Kursen, die zu eurem Alltag passen.</h1>', '<h1>Wir kommen zu euch — mit Kursen, die zu eurem Alltag passen.</h1>').replace('<h1>Wir kommen zu euch — mit Kursen, die zu eurem Alltag passen.</h1>', '<h1>Inhouse-Kurse für Erste Hilfe und Brandschutz: Wir kommen zu euch.</h1>'))
SEC = ('<section class="section" id="anfrageweg"><div class="section-head"><span class="eyebrow">Ablauf</span><h2>So läuft eure Anfrage</h2></div>'
 '<ul class="check-list"><li><strong>Anfrage senden:</strong> über das Kontaktformular, die <a href="/inhouse-kurse/#anfrage">Inhouse-Anfrage</a> oder telefonisch unter <a href="tel:+4955277487518">+49 5527 748 7518</a>.</li>'
  '<li><strong>Für Inhouse-Kurse</strong> helfen uns Kursart, Teilnehmerzahl, Wunschzeitraum und Ort.</li>'
 '<li><strong>Offene Kurse</strong> bucht ihr direkt online bei den <a href="/kurse/#live-termine">freien Terminen</a>.</li></ul>'
 '<h2>Wobei wir helfen</h2>'
 '<ul class="check-list"><li><a href="/kurse/">Kursauswahl</a> für Betrieb, Führerschein, Brandschutz und Sanitätsdienst</li>'
 '<li><a href="/inhouse-kurse/">Inhouse-Kurse</a> direkt bei euch vor Ort</li>'
 '<li><a href="/abrechnung/">Abrechnung über die Berufsgenossenschaft</a> für betriebliche Ersthelfer</li>'
 '<li>Teilnahmebescheinigung <a href="/zertifikat-pruefen/">prüfen</a> oder <a href="/zertifikat-duplikat/">Duplikat anfordern</a></li>'
 '<li><a href="/fuer-ausbilder/">Ausbilder werden</a>: Lehrkräfte-Ausbildung und Fortbildung</li>'
 '<li><a href="/anfrage-status/">Status einer Anfrage</a></li></ul>'
 '<h2>Anschrift</h2><p>BWW UG (haftungsbeschränkt), Worbiser Straße 2, 37115 Duderstadt. Telefon <a href="tel:+4955277487518">+49 5527 748 7518</a>, E-Mail <a href="mailto:info@multiplikatorenstelle.de">info@multiplikatorenstelle.de</a>. Kursorte stehen bei jedem Termin.</p></section>')
def kontakt(h):
    if 'id="anfrageweg"' in h: return h
    k = h.find('<section class="section home-final">'); assert k > 0
    return h[:k] + SEC + h[k:]
rw('kontakt/index.html', kontakt)
rw('index.html', lambda h: h.replace('Aus dem Rettungsdienst', 'Dozenten aus der Praxis'))   # Rettungsdienst-Herkunft der Dozenten nicht belegt
css = open('assets/styles.css', encoding='utf8').read()
if '.h1-kw' not in css:
    css += '\n/* Startseite: Themenwort als Zeile über der H1, 02.11.2026 */\nhtml:root:root:root .hero h1 .h1-kw{display:block!important;font-size:max(.3em,13px)!important;line-height:1.25!important;font-weight:800!important;letter-spacing:.03em!important;color:#426d58!important;margin:0 0 .5em!important}\n'
    open('assets/styles.css', 'w', encoding='utf8').write(css); n += 1
    import hashlib, glob
    old = __import__('re').search(r'styles\.css\?v=([0-9a-f]{8})', open('index.html', encoding='utf8').read()).group(1); new = hashlib.sha1(css.encode('utf8')).hexdigest()[:8]
    for f in glob.glob('**/*.html', recursive=True):
        t = open(f, encoding='utf8').read()
        if 'styles.css?v=' + old in t: open(f, 'w', encoding='utf8').write(t.replace('styles.css?v=' + old, 'styles.css?v=' + new))
print('geändert:', n)
