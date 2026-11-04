#!/usr/bin/env python3
"""/notruf-simulator/: Erklärtext zu den 5 W-Fragen mit Quellen, Hinweis für Lehrkräfte/Gruppen, interne Links, 3 weitere FAQ (HTML + FAQPage). Title/Description/H1 unberührt. Idempotent."""
import json, os, re, html
os.chdir(os.path.expanduser('~/Claude/bww-neu-wt'))
f = 'notruf-simulator/index.html'; h = open(f, encoding='utf8').read()
if 'notruf-erklaert' in h: print('bereits'); raise SystemExit
SEC = '''<section class="section article-body" id="notruf-erklaert"><h2>Die 5 W-Fragen beim Notruf erklärt</h2>
<p>Wer die 112 wählt, muss nicht perfekt formulieren: Die Leitstelle führt das Gespräch und gibt Anweisungen für die konkrete Lage. Eine feste Reihenfolge hilft trotzdem, nichts Wichtiges zu vergessen. Der Simulator fragt diese fünf Punkte ab und wertet am Ende aus, welche ihr genannt habt.</p>
<ol>
<li><strong>Wo ist der Notfallort?</strong> Die Adresse ist die wichtigste Angabe, denn die Einsatzkräfte müssen den Ort finden. Nennt Ort, Straße und Hausnummer, im Betrieb zusätzlich Gebäude, Stockwerk oder Eingang.</li>
<li><strong>Was ist passiert?</strong> Beschreibt in einem Satz, was geschehen ist: ein Sturz, ein Unfall, ein Brand oder eine plötzliche Erkrankung.</li>
<li><strong>Wie viele Betroffene gibt es?</strong> Die Zahl der verletzten oder erkrankten Personen hilft der Leitstelle, die Hilfe passend zu planen.</li>
<li><strong>Welche Verletzungen oder Symptome liegen vor?</strong> Zum Beispiel: ist bewusstlos, atmet nicht, blutet stark. Das hilft der Leitstelle einzuschätzen, wie dringend die Lage ist.</li>
<li><strong>Warten auf Rückfragen.</strong> Die Leitstelle fragt nach und leitet an. Legt nicht von euch aus auf, sondern bleibt am Telefon, bis sie das Gespräch beendet.</li>
</ol>
<p><strong>Quellen und Abweichungen:</strong> Die Formulierung der W-Fragen unterscheidet sich je nach Leitfaden. DGUV Arbeit &amp; Gesundheit nennt vier Angaben: Wo befindet sich die Unfallstelle, was ist passiert, wie viele Personen sind betroffen, welche Verletzungen liegen vor. Die BG ETEM führt fünf W-Fragen auf und fragt als fünfte „Wer meldet den Notfall?“. Der Simulator übt die fünf Punkte oben und ersetzt die fünfte Frage durch das Warten auf Rückfragen.</p>
<h2>Was vor und nach dem Anruf gilt</h2>
<p>Nach der Eigensicherung kommt der Notruf an erster Stelle. Das gilt auch bei einer Wiederbelebung: Zuerst wird die 112 gewählt, danach beginnt die Herzdruckmassage. Die Nummer 112 gilt europaweit und lässt sich von jedem Mobiltelefon wählen. Die Leitstelle kann am Telefon anleiten, etwa zur stabilen Seitenlage oder zur Herzdruckmassage. Wie der Notruf in die Abfolge der Hilfe passt, erklärt <a href="/wissen/rettungskette/">die Rettungskette</a>, den Ablauf des Gesprächs im Detail <a href="/wissen/notruf-112/">Notruf 112: die 5 W-Fragen</a>.</p>
<p><strong>Im echten Notfall wählt ihr sofort die 112.</strong> Der Simulator ist eine Übung und ersetzt weder einen Anruf noch einen <a href="/kurse/erste-hilfe-ausbildung/">Erste-Hilfe-Kurs</a>.</p>
<h2>Den Simulator mit Lehrkräften und Gruppen nutzen</h2>
<p>Der Simulator eignet sich für Unterricht und Unterweisung. Zeigt ihn mit dem Beamer, lasst eine Person den Notruf durchspielen und die Gruppe mitlesen. Im Kindermodus übt ein Kind den Anruf. Besprecht danach gemeinsam die Auswertung: Welche der fünf W-Fragen wurden zuerst genannt, welche fehlten? Für Schulen und Betreuungseinrichtungen gibt es dazu passende Angebote unter <a href="/fuer-schulen/">Erste Hilfe für Schulen</a> und <a href="/kurse/erste-hilfe-bildungseinrichtungen/">Erste Hilfe in Bildungs- und Betreuungseinrichtungen</a>.</p>
<p class="article-sources"><strong>Quellen:</strong> DGUV Arbeit &amp; Gesundheit: „Ersthelfende im Straßenverkehr: Sicher agieren“ (aug.dguv.de, 04.04.2025) · BG ETEM, profi: „Erste Hilfe“ (profi.bgetem.de, Seite ohne Datumsangabe). Abgerufen am 04.11.2026. Im Notfall immer 112.</p></section>
'''
FAQ = [
 ('Rufe ich bei einer Wiederbelebung zuerst die 112 an?', 'Ja. Nach der Eigensicherung steht der Notruf an erster Stelle, danach beginnt die Herzdruckmassage. Die Leitstelle kann dabei anleiten (Quelle: BG ETEM).'),
 ('Gehört „Wer meldet den Notfall?“ zu den W-Fragen?', 'Das hängt vom Leitfaden ab: Die BG ETEM nennt sie als fünfte W-Frage, DGUV Arbeit & Gesundheit führt vier Angaben auf. Der Simulator übt stattdessen das Warten auf Rückfragen der Leitstelle.'),
 ('Kann ich den Simulator mit einer Klasse oder Gruppe nutzen?', 'Ja. Eine Person spielt den Notruf durch, die Gruppe liest mit und bespricht danach die Auswertung der fünf W-Fragen. Im Kindermodus übt ein Kind den Anruf.'),
]
a = '<section class="section" id="simulator-faq">'; assert h.count(a) == 1
h = h.replace(a, SEC + a)
b = '<p class="small-note">Dies ist eine Übung.'; assert h.count(b) == 1
h = h.replace(b, ''.join(f'<h3>{q}</h3><p>{html.escape(an, quote=False)}</p>' for q, an in FAQ) + b)
def ld(m):
    j = json.loads(m.group(2))
    if j.get('@type') == 'FAQPage':
        j['mainEntity'] += [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": an}} for q, an in FAQ]
        return m.group(1) + json.dumps(j, ensure_ascii=False, separators=(',', ':')) + m.group(3)
    return m.group(0)
h = re.sub(r'(<script type="application/ld\+json">)(\{.*?\})(</script>)', ld, h, flags=re.S)
open(f, 'w', encoding='utf8').write(h)
i = h.find('<main'); j = h.find('<section class="section home-final"'); t = re.sub(r'<script.*?</script>', '', h[i:j], flags=re.S)
print('Wörter Hauptinhalt jetzt:', len(html.unescape(re.sub(r'<[^>]+>', ' ', t)).split()))
