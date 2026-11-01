#!/usr/bin/env python3
"""Reihe F (GSC Position 8-20, 02.11.): Cluster RTW/KTW -> /wissen/fahrzeuge-rettungsdienst/, Bescheinigung/Nachweis -> /wissen/erste-hilfe-teilnahmebescheinigung/.
Title/Description/Antwort in 2 Sätzen/FAQ nur aus Seiteninhalt (Quellen auf der Seite) + je 3 interne Fließtext-Links. Idempotent."""
import re, json, html
def esc(s): return s.replace('&', '&amp;')
n = 0
def rd(p): return open(p + '/index.html', encoding='utf8').read()
def wr(p, h):
    global n
    open(p + '/index.html', 'w', encoding='utf8').write(h); n += 1
def meta(h, T, D, H1old=None, H1new=None):
    assert len(T) <= 60 and len(D) <= 155, (len(T), len(D))
    h = re.sub(r'<title>.*?</title>', '<title>' + esc(T) + '</title>', h, 1)
    h = re.sub(r'(<meta name="description" content=")[^"]*"', lambda m: m.group(1) + esc(D) + '"', h, 1)
    for a, v in (('og:description', D), ('twitter:description', D)): h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % a, lambda m: m.group(1) + esc(v) + '"', h, 1)
    for a in ('og:title', 'twitter:title'): h = re.sub(r'(<meta (?:property|name)="%s" content=")[^"]*"' % a, lambda m: m.group(1) + esc(T.replace(' | BWW', ' | BWW Wissensdatenbank')) + '"', h, 1)
    return h
def answer(h, text):
    a = '<p class="answer-lead"><strong>Direkt beantwortet:</strong> ' + text + '</p>'
    if 'class="answer-lead"' in h.split('<h2>')[0].split('article-body')[-1]: return h
    return h.replace('<section class="section article-body">', '<section class="section article-body">' + a, 1)
def add_faq(h, items):
    for q, a in items:
        if f'<h3>{esc(q)}</h3>' in h: continue
        k = h.find('<p class="article-related">'); assert k > 0
        h = h[:k] + f'<h3>{esc(q)}</h3><p>{esc(a)}</p>' + h[k:]
        m = [x for x in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S) if '"FAQPage"' in x.group(1)][0]
        j = json.loads(m.group(1)); j['mainEntity'].append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        h = h.replace(m.group(1), json.dumps(j, ensure_ascii=False, separators=(',', ':')), 1)
    return h
def link_in(page, anchor_html, marker_end):
    """haengt einen Satz mit Link an das Ende des ersten Fließtext-Absatzes an, der auf marker_end endet"""
    global n
    h = rd(page)
    if anchor_html in h: return
    if marker_end not in h: print('FEHLT', page, marker_end[:40]); return
    wr(page, h.replace(marker_end, marker_end[:-4] + ' ' + anchor_html + '</p>', 1))

# ---- Cluster 1: RTW/KTW
p = 'wissen/fahrzeuge-rettungsdienst'; h = rd(p); o = h
T = 'RTW-Abkürzung und Unterschied KTW/RTW erklärt | BWW'
D = 'RTW heißt Rettungswagen, KTW Krankentransportwagen: Der RTW fährt Notfälle, der KTW betreute Transporte. Dazu NEF, RTH und die Norm DIN EN 1789.'
h = meta(h, T, D)
h = h.replace('Fahrzeuge im Rettungsdienst: RTW, KTW, NEF und mehr', 'RTW, KTW, NEF: Abkürzungen und Fahrzeuge im Rettungsdienst')
h = answer(h, 'RTW steht für Rettungswagen, KTW für Krankentransportwagen. Der RTW versorgt Notfallpatienten und transportiert sie, der KTW befördert nicht akut lebensbedrohlich Erkrankte, die betreut werden müssen.')
h = add_faq(h, [('Was bedeutet die Abkürzung RTW?', 'RTW steht für Rettungswagen, das zentrale Fahrzeug der Notfallrettung. Die Anforderungen an Rettungs- und Krankenkraftwagen legt europaweit die Norm DIN EN 1789 fest.'),
                ('Was bedeutet KTW?', 'KTW steht für Krankentransportwagen. Er transportiert Personen, die nicht akut lebensbedrohlich erkrankt oder verletzt sind, aber betreut werden müssen; seine Ausstattung ist auf Betreuung und Transport ausgelegt, nicht auf die Notfallrettung.')])
for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
    j = json.loads(m.group(1))
    if j.get('@type') == 'Article':
        nj = dict(j); nj['headline'] = 'RTW, KTW, NEF: Abkürzungen und Fahrzeuge im Rettungsdienst'
        h = h.replace(m.group(1), json.dumps(nj, ensure_ascii=False, separators=(',', ':')), 1)
if h != o: wr(p, h)
LK = '<a href="/wissen/fahrzeuge-rettungsdienst/">RTW, KTW und NEF im Überblick</a>'
link_in('wissen/kosten-rettungsdienst-krankenwagen', 'Welche Fahrzeuge es gibt, zeigt ' + LK + '.', 'Bei einem <strong>Arbeits- oder Wegeunfall</strong> zahlt die</p>') if False else None
# Links per Absatzende (aus den Seiten gelesen)
def link_after(page, needle, sentence):
    h = rd(page)
    if '/wissen/fahrzeuge-rettungsdienst/' in h[h.find('<main'):h.find('<h2>Häufige Fragen')]: return
    i = h.find(needle, h.find('<main'))
    if i < 0: print('FEHLT', page, needle[:40]); return
    j = h.find('</p>', i); wr(page, h[:j] + ' ' + sentence + h[j:])
link_after('wissen/rettungskette', 'Der <strong>Notruf 112</strong> bringt professionelle Hilfe in Gang.', 'Welche Fahrzeuge dann ausrücken, erklärt ' + LK + '.')
link_after('wissen/notruf-112', 'Die Leitstelle stellt gezielt Rückfragen', 'Welches Fahrzeug alarmiert wird, zeigt ' + LK + '.')
link_after('wissen/kosten-rettungsdienst-krankenwagen', 'Der Notruf 112 ist immer kostenlos', 'Mehr zu den Fahrzeugen: ' + LK + '.') if False else link_after('wissen/kosten-rettungsdienst-krankenwagen', 'übernimmt in aller Regel die <strong>Krankenkasse</strong>', 'Welche Fahrzeuge es gibt, erklärt ' + LK + '.')

# ---- Cluster 2: Bescheinigung/Nachweis
p = 'wissen/erste-hilfe-teilnahmebescheinigung'; h = rd(p); o = h
T = 'Erste-Hilfe-Bescheinigung & Nachweis: Pflichtangaben | BWW'
D = 'Erste-Hilfe-Bescheinigung und Nachweis: Was nach DGUV Grundsatz 304-001 draufstehen muss, wem sie gehört und woran ihr eine ermächtigte Stelle erkennt.'
h = meta(h, T, D)
h = answer(h, 'Nach jedem Erste-Hilfe-Kurs erhalten Teilnehmende eine Teilnahmebescheinigung; sie ist der Nachweis gegenüber der Berufsgenossenschaft und gehört der Person, auf deren Namen sie ausgestellt ist. Pflichtangaben nach DGUV Grundsatz 304-001 (Abschnitt 2.4.5) sind unter anderem Name, Datum, Unterrichtseinheiten sowie Name und Kennziffer der ermächtigten Stelle.')
h = h.replace('Woran erkenne ich, dass die Bescheinigung von einer anerkannten Stelle stammt?', 'Woran erkenne ich, dass die Bescheinigung von einer ermächtigten Stelle stammt?')
h = add_faq(h, [('Wie bekomme ich eine Erste-Hilfe-Bescheinigung?', 'Nach regelmäßigem Besuch des Kurses. Die Bescheinigung darf nur erteilt werden, wenn die Lehrkraft die Überzeugung gewonnen hat, dass die teilnehmende Person die erforderlichen Kenntnisse und Fähigkeiten besitzt; reine Anwesenheit genügt nicht (DGUV Grundsatz 304-001).'),
                ('Ist die Bescheinigung der Erste-Hilfe-Nachweis für den Betrieb?', 'Ja, für die Berufsgenossenschaft ist sie der Beleg, dass Ersthelfende ausgebildet sind. Das Original gehört der Person; der Betrieb kann eine Kopie für seine Unterlagen nehmen.')])
if h != o: wr(p, h)
LB = '<a href="/wissen/erste-hilfe-teilnahmebescheinigung/">Was auf der Erste-Hilfe-Bescheinigung stehen muss</a>'
link_after2 = lambda page, needle, sentence: None
def link_after_b(page, needle, sentence):
    h = rd(page)
    if '/wissen/erste-hilfe-teilnahmebescheinigung/' in h[h.find('<main'):h.find('<h2>Häufige Fragen')]: return
    i = h.find(needle, h.find('<main'))
    if i < 0: print('FEHLT', page, needle[:40]); return
    j = h.find('</p>', i); wr(page, h[:j] + ' ' + sentence + h[j:])
link_after_b('wissen/erste-hilfe-kurs-inhalte', 'Der Erste-Hilfe-Kurs macht in einem Tag handlungssicher', 'Nach dem Kurs gibt es eine Bescheinigung als Nachweis: ' + LB + '.')
link_after_b('wissen/erste-hilfe-fuehrerschein', 'Notruf, Absichern, Seitenlage', 'Den Nachweis dafür erklärt ' + LB + '.')
link_after_b('wissen/erste-hilfe-kurs-gueltigkeit', 'Kurze Antwort:', 'Welche Angaben der Nachweis enthalten muss, zeigt ' + LB + '.')
print('geändert:', n)
