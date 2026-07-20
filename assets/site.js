
function escapeHtml(s){return String(s||'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
function asInt(id, fallback=0){const el=document.getElementById(id);const n=parseInt(el?.value||fallback,10);return Number.isFinite(n)?n:fallback;}

function calculateDguv(){
  const industry=document.getElementById('industry')?.value||'admin';
  const employees=Math.max(0,asInt('employees',0));
  const shifts=Math.max(1,asInt('shifts',1));
  const factor=industry==='admin'?0.05:0.10;
  let firstAid=employees<=0?0:(employees<=20?1:Math.ceil(employees*factor));
  firstAid=Math.max(firstAid, employees>0?shifts:0);
  let bsan=0;
  if(industry==='construction') bsan=employees>100?1:0;
  else bsan=employees>1500?1:0;
  const fire=employees>0?Math.max(1,Math.ceil(employees*0.05)):0;
  const evac=employees>0?Math.max(1,Math.ceil(employees*0.05)):0;
  const kits=employees<=0?0:employees<=50?1:employees<=300?2:Math.ceil(employees/150);
  const el=document.getElementById('calcResult');
  if(!el) return;
  el.innerHTML=`
    <div class="metric"><span>Betriebliche Ersthelfer</span><b>${firstAid}</b><small>inkl. Schichten/Abwesenheiten als praxisnahe Mindestplanung</small></div>
    <div class="metric"><span>Brandschutzhelfer</span><b>${fire}</b><small>Orientierung ca. 5 %, abhängig von Gefährdungsbeurteilung</small></div>
    <div class="metric"><span>Evakuierungshelfer</span><b>${evac}</b><small>für Räumung, Sammelstellen und Besucherströme einplanen</small></div>
    <div class="metric"><span>Betriebssanitäter</span><b>${bsan?bsan:'prüfen'}</b><small>${bsan?'Pflicht/Bedarf genauer prüfen':'meist nicht erforderlich, wenn keine besonderen Gefahren vorliegen'}</small></div>
    <div class="metric"><span>Verbandkästen</span><b>${kits}</b><small>Standorte müssen schnell erreichbar und regelmäßig geprüft sein</small></div>
    <div class="metric"><span>AED</span><b>${employees>=50||industry==='care'?'empfohlen':'prüfen'}</b><small>besonders bei Publikumsverkehr, Alleinarbeit oder erhöhtem Risiko</small></div>`;
}

const assistantAnswers={
  ersthelfer:['Wie viele Ersthelfer braucht mein Betrieb?','Bis 20 anwesende Versicherte mindestens eine Person. Danach wird je nach Branche häufig mit 5 % oder 10 % geplant. Schichten, Urlaube, Außenstellen und reale Erreichbarkeit zählen in der Praxis mit.','/dguv-rechner/'],
  brandschutz:['Wie viele Brandschutzhelfer sind sinnvoll?','Als praxisnahe Orientierung werden häufig etwa 5 % der Beschäftigten angesetzt. Entscheidend sind Gefährdungsbeurteilung, Brandlast, Publikumsverkehr, Schichtbetrieb und Evakuierungswege.','/arbeitsschutz-check/'],
  abrechnung:['Wie funktioniert die Kostenübernahme?','Viele Unfallversicherungsträger übernehmen erforderliche Erste-Hilfe-Kurse. Je nach BG/UK gibt es andere Wege: vorherige Kostenzusage, Abrechnungsformular, Online-Verfahren oder direkte Anmeldung.','/abrechnung/'],
  kind:['Was ist anders bei Erste Hilfe am Kind?','Kinder brauchen andere Dosierungen, andere Kommunikation und mehr Ruhe. Typische Themen sind Verschlucken, Fieberkrampf, Stürze, Atemprobleme und sichere Elternkommunikation.','/kurse/#erste-hilfe-kurs-baby--kind'],
  fahrschule:['Ist die Erste-Hilfe-Ausbildung für den Führerschein geeignet?','Ja. Die Erste-Hilfe-Ausbildung mit 9 Unterrichtseinheiten ist das passende Standardformat für Führerscheinanwärter und zugleich ein starker Einstieg in sichere Hilfe im Alltag.','/kurse/#live-termine'],
  dozent:['Wie bewerbe ich mich als Dozentin oder Dozent?','Das geht in unter einer Minute: Daten eintragen, Qualifikation auswählen, Zertifikate anhängen und absenden. Wir melden uns mit den nächsten Schritten.','/dozent-werden/']
};
function askAssistant(key){const a=assistantAnswers[key]||assistantAnswers.ersthelfer;const el=document.getElementById('assistantAnswer');if(!el)return;el.innerHTML=`<h2>${a[0]}</h2><p>${a[1]}</p><a class="btn primary" href="${a[2]}">Mehr dazu</a>`;}

const notrufPrompts={
 adult:[
  ['where','Notruf 112. Rettungsleitstelle Duderstadt. Wo genau ist der Notfallort?','Bitte nenne Ort, Straße, Hausnummer, Etage oder einen markanten Punkt.'],
  ['what','Was ist passiert?','Beschreibe kurz die Lage: Unfall, Sturz, Brand, Erkrankung oder Bewusstlosigkeit.'],
  ['howmany','Wie viele Personen sind betroffen?','Eine Person, mehrere Personen, Kinder oder Erwachsene?'],
  ['injuries','Welche Verletzungen oder Symptome sehen Sie?','Atmung, Bewusstsein, Blutung, Schmerzen oder andere Auffälligkeiten.'],
  ['wait','Bleiben Sie bitte am Telefon. Können Sie auf Rückfragen warten?','Nicht auflegen. Die Leitstelle führt dich weiter.']
 ],
 child:[
  ['where','Hallo. Du hast die 112 angerufen. Ich bin bei dir. Weißt du, wo du bist?','Zum Beispiel Zuhause, Schule, Straße, Ort oder ein Schild.'],
  ['what','Du machst das gut. Was ist passiert?','Sag einfach mit deinen Worten, was du gesehen hast.'],
  ['howmany','Ist eine Person verletzt oder sind es mehrere?','Eine, zwei oder mehrere Personen.'],
  ['injuries','Kann die Person sprechen oder atmen? Siehst du Blut?','Sag nur, was du sehen oder hören kannst.'],
  ['wait','Bleib bitte dran. Kannst du das Telefon bei dir behalten?','Du bist nicht allein. Hilfe ist unterwegs.']
 ]
};
let notruf={mode:'adult',step:0,answers:[],started:false,tries:{}};
function cleanSpeech(text){return String(text||'').replace(/[.,;:!?„“"()]/g,' ').replace(/\s+/g,' ').trim();}
function speakDE(text){try{speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(cleanSpeech(text));u.lang='de-DE';u.rate=notruf.mode==='child'?.92:1.02;u.pitch=notruf.mode==='child'?1.1:.95;speechSynthesis.speak(u);}catch(e){}}
function startNotrufSimulator(mode='adult'){notruf={mode,step:0,answers:[],started:true,tries:{}};renderNotruf();speakDE(notrufPrompts[mode][0][1]);setTimeout(()=>document.getElementById('notrufAnswer')?.focus(),100);}
function scoreAnswer(key,text){const t=(text||'').toLowerCase();if(key==='where')return /(straße|strasse|weg|platz|duderstadt|worbis|schule|kita|firma|haus|nummer|stock|etage|halle|büro|buero|[0-9])/.test(t)||t.length>22;if(key==='what')return /(unfall|sturz|brand|bewusstlos|ohnmacht|krank|verletzt|auto|fahrrad|atmet|blutet|schmerz|kippt|gefallen|verschluckt)/.test(t)||t.length>16;if(key==='howmany')return /(eine|einer|zwei|drei|vier|fünf|mehrere|person|kind|mann|frau|[0-9])/.test(t);if(key==='injuries')return /(atmet|atmung|blut|bewusst|schmerz|kopf|bein|arm|brust|verletz|spricht|nicht|krampf|verbrenn)/.test(t)||t.length>14;if(key==='wait')return /(ja|warte|bleibe|telefon|dran|nicht auflegen|rückfragen|ok|okay|kann)/.test(t)||t.length>4;return false;}
function notrufUseText(){const input=document.getElementById('notrufAnswer');if(!input||!notruf.started)return;const txt=input.value.trim();if(!txt)return;submitNotrufAnswer(txt);input.value='';}
function submitNotrufAnswer(txt){
  const prompt=notrufPrompts[notruf.mode][notruf.step]; if(!prompt)return;
  const ok=scoreAnswer(prompt[0],txt); notruf.tries[prompt[0]]=(notruf.tries[prompt[0]]||0)+1;
  notruf.answers.push({key:prompt[0],label:prompt[2],text:txt,ok});
  if(!ok && notruf.tries[prompt[0]]<2){
    renderNotruf(); const retry=notruf.mode==='child'?`Das ist okay. ${prompt[2]}`:`Ich frage noch einmal genauer: ${prompt[2]}`; speakDE(retry); return;
  }
  notruf.step++; renderNotruf();
  if(notruf.step<notrufPrompts[notruf.mode].length){speakDE(notrufPrompts[notruf.mode][notruf.step][1]);}
  else{speakDE('Danke. Das war die Simulation. Sie sehen jetzt die Auswertung.');}
}
function notrufStartVoice(){const Rec=window.SpeechRecognition||window.webkitSpeechRecognition;if(!Rec){alert('Spracherkennung wird in diesem Browser nicht unterstützt. Bitte nutze das Textfeld.');return;}const rec=new Rec();rec.lang='de-DE';rec.interimResults=false;rec.maxAlternatives=1;document.getElementById('notrufStatus').textContent='Ich höre zu…';rec.onresult=e=>submitNotrufAnswer(e.results[0][0].transcript);rec.onerror=()=>{document.getElementById('notrufStatus').textContent='Bitte Textfeld nutzen';};rec.onend=()=>{if(notruf.started&&notruf.step<notrufPrompts[notruf.mode].length)document.getElementById('notrufStatus').textContent='Bereit';};rec.start();}
function renderNotruf(){const title=document.getElementById('notrufTitle'),prompt=document.getElementById('notrufPrompt'),log=document.getElementById('notrufLog'),status=document.getElementById('notrufStatus'),score=document.getElementById('notrufScore');if(!log)return;const prompts=notrufPrompts[notruf.mode];if(title)title.textContent=notruf.mode==='child'?'Kinder-Notruftraining: freundlich, ruhig, sicher.':'Notruftraining: klar bleiben, wenn es zählt.';if(prompt)prompt.textContent=notruf.started?(notruf.step<prompts.length?prompts[notruf.step][1]:'Auswertung abgeschlossen. Starte gern eine neue Runde.'):'Wähle eine Simulation und starte den Notruf.';if(status)status.textContent=notruf.started?(notruf.step<prompts.length?`Frage ${notruf.step+1} von 5`:'Fertig'):'Bereit';let html=notruf.started?`<p><b>Leitstelle:</b> ${notruf.step<prompts.length?prompts[notruf.step][1]:'Simulation beendet.'}</p>`:'<p><b>Leitstelle:</b> Starte die Simulation. Du kannst sprechen oder tippen.</p>';notruf.answers.forEach(a=>{html+=`<p class="user ${a.ok?'':'soft-warn'}"><b>Du:</b> ${escapeHtml(a.text)} ${a.ok?'':'<small>— Leitstelle fragt genauer nach</small>'}</p>`});log.innerHTML=html;if(score){score.innerHTML=prompts.map(p=>{const a=notruf.answers.filter(x=>x.key===p[0]).pop();const label=p[0]==='where'?'Wo':p[0]==='what'?'Was':p[0]==='howmany'?'Wie viele':p[0]==='injuries'?'Verletzung':'Warten';return `<span class="${a?(a.ok?'ok':'miss'):''}">${label}</span>`}).join('');}}

document.addEventListener('keydown',e=>{if(e.key==='Enter'&&document.activeElement?.id==='notrufAnswer'){e.preventDefault();notrufUseText();}});

const complianceBase=['Sind ausreichend betriebliche Ersthelfer benannt?','Sind Ersthelfer-Schulungen aktuell?','Sind Erste-Hilfe-Leistungen dokumentiert?','Sind Verbandkästen vollständig und erreichbar?','Sind Notrufnummern sichtbar ausgehängt?','Ist der nächste AED-Standort bekannt?','Gibt es eine klare Alarmierungskette?','Sind Brandschutzhelfer benannt?','Wurden Evakuierungswege geprüft?','Gibt es Sammelstellen und Räumungsabläufe?','Sind neue Mitarbeitende unterwiesen?','Sind Schicht- und Außenbereiche berücksichtigt?','Sind Gefahrstoffe mit Sicherheitsdatenblatt erfasst?','Gibt es Augenspülung bei Augenrisiken?','Sind Maschinen- oder Schnittverletzungen bedacht?','Sind psychische Erste-Hilfe-Aspekte bekannt?','Gibt es regelmäßige Notfallübungen?','Sind Zuständigkeiten schriftlich geregelt?','Wurden Fremdfirmen/Besucher berücksichtigt?','Ist der Bedarf an Betriebssanitätern geprüft?','Sind Sicherheitsbeauftragte geprüft/benannt?','Sind Führungskräfte über Pflichten informiert?','Gibt es Inhouse-Trainings für reale Szenarien?','Sind Feuerlöscher passend platziert?','Sind Beschäftigte in Löschmitteln unterwiesen?','Ist die BG/UK für Abrechnung bekannt?','Sind Kursnachweise zentral abgelegt?','Wird nach Unfällen nachbereitet?','Gibt es einen Plan für Ausfälle/Urlaub?','Ist der Arbeitsschutz jährlich überprüft?'];
function initCompliance(){const wrap=document.getElementById('complianceQuestions'); if(!wrap||wrap.dataset.ready)return; wrap.dataset.ready='1'; wrap.innerHTML=complianceBase.map((q,i)=>`<label><input type="checkbox" data-compliance><span>${i+1}. ${q}</span></label>`).join('');}
function runSafetyCheck(){const f=document.getElementById('safetyCheckForm'); if(!f)return; const d=new FormData(f); const e=Math.max(1,parseInt(d.get('employees')||'1',10)); const sector=d.get('sector'); const shifts=Math.max(1,parseInt(d.get('shifts')||'1',10)); const risk=(d.get('chemicals')?1:0)+(d.get('machines')?1:0)+(d.get('remote')?1:0)+(d.get('public')?1:0); const first=e<=20?1:(sector==='office'?Math.ceil(e*.05):Math.ceil(e*.10)); const fire=Math.max(1,Math.ceil(e*.05)); const evac=Math.max(1,Math.ceil(e*.05)+(d.get('public')?1:0)); const kits=e<=50?1:e<=300?2:Math.ceil(e/150); const aug=d.get('chemicals')?'Ja – bei Augen-/Gefahrstoffrisiko einplanen':'Prüfen nach Gefährdungsbeurteilung'; const aed=(e>=50||sector==='care'||d.get('public'))?'Empfohlen':'Optional, Standort/Risiko prüfen'; const bsan=(sector==='construction'&&e>100)||(sector!=='construction'&&e>1500)?'Ja, Bedarf detailliert prüfen':'meist nicht erforderlich, Gefährdung prüfen'; const safety=e>20?'Sicherheitsbeauftragte prüfen/benennen':'bei Wachstum prüfen'; const trainings=['Erste-Hilfe-Ausbildung','Erste-Hilfe-Fortbildung','Brandschutzhelfer']; if(sector==='care')trainings.push('Notfalltraining Praxis/Pflege'); if(sector==='kita'||sector==='school')trainings.push('Erste Hilfe am Kind'); if(risk>=2)trainings.push('Szenario-Training / AED'); const el=document.getElementById('safetyCheckResult'); el.innerHTML=`<h2>Maßnahmenplan</h2><div class="result-list"><p>✅ Ersthelfer: <b>${Math.max(first,shifts)}</b></p><p>✅ Brandschutzhelfer: <b>${fire}</b></p><p>✅ Evakuierungshelfer: <b>${evac}</b></p><p>✅ Verbandkästen: <b>${kits}</b></p><p>✅ AED: <b>${aed}</b></p><p>✅ Augenduschen: <b>${aug}</b></p><p>✅ Betriebssanitäter: <b>${bsan}</b></p><p>✅ Sicherheitsbeauftragter: <b>${safety}</b></p></div><h3>Empfohlene Schulungen</h3><p>${trainings.join(' · ')}</p><a class="btn primary" href="/kurse/">Passende Kurse ansehen</a>`;}
function runComplianceScan(){const checks=[...document.querySelectorAll('[data-compliance]')]; const done=checks.filter(c=>c.checked).length; const pct=checks.length?Math.round(done/checks.length*100):0; const missing=checks.filter(c=>!c.checked).slice(0,8).map(c=>c.parentElement.textContent.trim()); const el=document.getElementById('complianceResult'); if(!el)return; el.innerHTML=`<h2>Compliance-Score: ${pct} %</h2><p>${pct>=85?'🟢 Sehr solide Basis. Jetzt Feinschliff und Nachweise pflegen.':pct>=60?'🟡 Gute Ansätze, aber mehrere Punkte sollten aktiv nachgezogen werden.':'🔴 Hier liegt deutliches Potenzial: bitte Verantwortlichkeiten, Schulungen und Ausstattung prüfen.'}</p><h3>Offene Punkte</h3><ul>${missing.map(m=>`<li>${m}</li>`).join('')}</ul><a class="btn primary" href="/inhouse-kurse/#anfrage">Schulungen planen</a>`;}
function generateIncidentReport(){const f=document.getElementById('incidentForm'); if(!f)return; const d=Object.fromEntries(new FormData(f).entries()); const report=document.getElementById('incidentReport'); const row=(k,v)=>`<p><b>${k}:</b><br>${escapeHtml(v||'—')}</p>`; report.innerHTML=`<div class="print-report"><h2>Arbeitsunfall-Dokumentation</h2>${row('Datum/Uhrzeit',d.time)}${row('Unternehmen/Standort',d.company)}${row('Verletzte Person',d.person)}${row('Unfallort',d.place)}${row('Unfallhergang',d.what)}${row('Verletzungen/Beschwerden',d.injury)}${row('Erste-Hilfe-Maßnahmen',d.measures)}${row('Zeugen',d.witnesses)}${row('Weitere Maßnahmen',d.followup)}<p class="small-note">Dokument bitte intern prüfen, ergänzen und gemäß den betrieblichen Vorgaben aufbewahren.</p><button class="btn primary" onclick="window.print()">PDF speichern / drucken</button></div>`;}

const ill='/media/illustrations/bww/';
const gameSteps={start:{img:ill+'office-emergency.png',title:'Ein Mitarbeiter kippt plötzlich um.',text:'Er liegt am Boden und reagiert nicht sofort. Was machst du zuerst?',choices:[['ansprechen','Ansprechen und vorsichtig rütteln',10,'breathing'],['cpr','Sofort drücken',0,'warn1'],['water','Wasser holen',-5,'warn1']]},warn1:{img:ill+'notruf-practice.png',title:'Kurz sortieren.',text:'Erst prüfen: Eigenschutz, Bewusstsein, normale Atmung. Dann wird entschieden.',choices:[['check','Bewusstsein und Atmung prüfen',10,'breathing'],['call','Direkt Notruf',5,'call']]},breathing:{img:ill+'cpr-clean.png',title:'Keine normale Atmung.',text:'Jetzt zählt jede Sekunde. Was ist der nächste starke Schritt?',choices:[['call','112 rufen / rufen lassen',10,'cpr'],['side','Stabile Seitenlage',-5,'warn2'],['wait','Abwarten',-10,'warn2']]},warn2:{img:ill+'stable-position.png',title:'Achtung: stabile Seitenlage passt hier nicht.',text:'Bei fehlender normaler Atmung: Notruf, Herzdruckmassage, AED.',choices:[['cpr','Herzdruckmassage starten',10,'aed'],['call','112 rufen',8,'cpr']]},call:{img:ill+'school-call-training.png',title:'Notruf läuft.',text:'Die Leitstelle fragt nach Ort, Lage, Betroffenen und Atmung. Was parallel?',choices:[['cpr','Herzdruckmassage starten',10,'aed'],['search','AED holen lassen',8,'aed']]},cpr:{img:ill+'cpr-clean.png',title:'Du beginnst mit Herzdruckmassage.',text:'Sehr gut. Drücke fest und schnell in der Mitte des Brustkorbs. Was hilft zusätzlich?',choices:[['aed','AED holen und Anweisungen folgen',10,'finish'],['stop','Pausieren bis Rettungsdienst kommt',-10,'warn2']]},aed:{img:ill+'aed-training.png',title:'AED ist da.',text:'Du klebst die Elektroden und folgst den Sprachansagen. Was ist wichtig?',choices:[['continue','Nach Analyse weiter drücken, bis Hilfe übernimmt',10,'finish'],['remove','Elektroden wieder entfernen',-10,'warn2']]},finish:{img:ill+'inclusive-inhouse.png',title:'Simulation geschafft.',text:'Du hast die wichtigsten Schritte trainiert: prüfen, Notruf, Reanimation, AED, weitermachen.',choices:[['restart','Neu starten',0,'start']]}};
let game={step:'start',score:0};
function renderGame(){const s=gameSteps[game.step]; const img=document.getElementById('gameImage'); if(!img||!s)return; img.src=s.img; document.getElementById('gameTitle').textContent=s.title; document.getElementById('gameText').textContent=s.text; document.getElementById('gameScore').textContent='Score: '+game.score; document.getElementById('gameChoices').innerHTML=s.choices.map(c=>`<button onclick="chooseGame('${c[3]}',${c[2]})">${c[1]}</button>`).join('');}
function chooseGame(next,points){if(next==='start')game.score=0;else game.score=Math.max(0,game.score+points);game.step=next;renderGame();}

const hazards=[
 ['chlorreiniger','Reizend/ätzend','GHS05 / GHS07','Dämpfe meiden, Frischluft, Augen/Haut lange spülen, bei Atemnot 112. Niemals mit Säure oder Essig mischen.','Handschuhe, Schutzbrille, Lüftung, kindersichere Lagerung.'],
 ['essigreiniger','Reizend','GHS07','Bei Augenkontakt mehrere Minuten spülen. Bei Verschlucken Mund ausspülen, kein Erbrechen auslösen, Giftnotruf/112 je nach Lage.','Nicht mit Chlor mischen, gut lüften.'],
 ['rohrreiniger','Ätzend','GHS05','Sofort lange mit Wasser spülen, kontaminierte Kleidung entfernen, ärztliche Hilfe. Bei Verschlucken sofort Giftnotruf/112.','Schutzbrille, Chemikalienschutzhandschuhe, kindersicher aufbewahren.'],
 ['lauge','Ätzend','GHS05','Wie bei Rohrreiniger: lange spülen, keine Neutralisation versuchen, medizinisch abklären.','PSA, Augendusche, Sicherheitsdatenblatt.'],
 ['säure','Ätzend','GHS05','Augen/Haut sofort mit viel Wasser spülen, kontaminierte Kleidung entfernen, ärztliche Abklärung.','Schutzbrille, Handschuhe, Augendusche, Sicherheitsdatenblatt.'],
 ['spülmaschinen-tab','Reizend/ätzend möglich','GHS07 / GHS05','Mund ausspülen, nicht erbrechen lassen, bei Kindern Giftnotruf/112. Haut/Augen mit Wasser spülen.','Originalverpackung, kindersicherer Schrank.'],
 ['waschmittel','Reizend','GHS07','Bei Augenkontakt spülen, bei Verschlucken Mund ausspülen, Packung bereithalten, Giftnotruf kontaktieren.','Außer Reichweite von Kindern, Dosierhilfen sicher lagern.'],
 ['desinfektionsmittel','Entzündbar/Reizend','GHS02 / GHS07','Frischluft bei Dämpfen, Augen spülen, bei Verschlucken Giftnotruf/112. Zündquellen vermeiden.','Lüftung, kein offenes Feuer, Hautschutz.'],
 ['alkohol','Entzündbar','GHS02','Frischluft, Zündquellen vermeiden, bei Bewusstseinsstörung 112.','Dicht verschließen, Mengen begrenzen.'],
 ['benzin','Hoch entzündbar/Gesundheitsgefahr','GHS02 / GHS08','Frischluft, kontaminierte Kleidung entfernen, bei Einatmen/Verschlucken sofort Hilfe. Kein Erbrechen auslösen.','Explosionsschutz, keine Zündquellen, geeignete Lagerung.'],
 ['lackverdünnung','Entzündbar/gesundheitsschädlich','GHS02 / GHS07 / GHS08','Frischluft, Haut reinigen, Augen spülen, bei Benommenheit oder Verschlucken 112/Giftnotruf.','Atemschutz/Lüftung, Handschuhe, Brandschutz.'],
 ['backofenreiniger','Ätzend/Reizend','GHS05 / GHS07','Haut/Augen lange spülen, Dämpfe meiden, bei Beschwerden ärztlich abklären.','Handschuhe, Schutzbrille, nicht einatmen.'],
 ['kalkreiniger','Reizend/ätzend möglich','GHS07 / GHS05','Augen spülen, Haut reinigen, nicht mit Chlor mischen.','Lüftung, Handschuhe, getrennte Lagerung.'],
 ['glasreiniger','Reizend/entzündbar möglich','GHS07 / GHS02','Augen spülen, Frischluft bei Sprühnebel, bei Beschwerden Giftnotruf.','Nicht in Kinderhände, Sprühnebel vermeiden.'],
 ['ätherische öle','Gefahr für Kinder/Haustiere möglich','GHS07','Bei Verschlucken oder Atembeschwerden Giftnotruf/112; nicht eigenständig Erbrechen auslösen.','Kindersicher, sparsam dosieren, nicht unverdünnt anwenden.']
];
function runHazardCheck(){const q=(document.getElementById('hazardInput')?.value||'').toLowerCase(); let row=hazards.find(h=>q.includes(h[0])); if(!row) row=['Unbekannter Stoff','Sicherheitsdatenblatt prüfen','SDB','Stoff eindeutig identifizieren, Exposition beenden, bei akuter Gefahr 112 oder Giftnotruf.','Kennzeichnung, Betriebsanweisung, PSA und Erste-Hilfe-Ausstattung prüfen.']; const el=document.getElementById('hazardResult'); if(el) el.innerHTML=`<h2>${row[1]}</h2><div class="hazard-picto">${row[2]}</div><h3>Erste Hilfe</h3><p>${row[3]}</p><h3>Schutzmaßnahmen</h3><p>${row[4]}</p><p class="small-note">Orientierung: Maßgeblich sind Kennzeichnung, Betriebsanweisung und aktuelles Sicherheitsdatenblatt.</p>`;}
var _kbCat='all';
function filterKnowledge(cat){_kbCat=cat;document.querySelectorAll('.filter-bar button').forEach(b=>{var oc=b.getAttribute('onclick')||'';b.classList.toggle('is-active',oc.indexOf("('"+cat+"')")>-1);});applyKnowledgeFilter();}
function applyKnowledgeFilter(){var si=document.getElementById('kbSearch');var q=si?si.value.trim().toLowerCase():'';var n=0;document.querySelectorAll('.knowledge-card').forEach(c=>{var okC=(_kbCat==='all'||c.dataset.cat===_kbCat);var okQ=!q||c.textContent.toLowerCase().indexOf(q)>-1;var show=okC&&okQ;c.style.display=show?'':'none';if(show)n++;});var e=document.getElementById('kbEmpty');if(e)e.style.display=n?'none':'';var cnt=document.getElementById('kbCount');if(cnt)cnt.textContent=n+(n===1?' Artikel':' Artikel');}

document.addEventListener('DOMContentLoaded',()=>{if(document.getElementById('calcResult'))calculateDguv();initCompliance();renderGame();renderNotruf();if(document.querySelector('.filter-bar')){try{var _q=new URLSearchParams(location.search).get('q');var _si=document.getElementById('kbSearch');if(_q&&_si)_si.value=_q;}catch(e){}filterKnowledge('all');}});

/* Dezenter Datenschutz-Hinweis (keine Tracking-Cookies; merkt Dismiss via localStorage) */
(function(){try{if(localStorage.getItem('bww-privacy-ok'))return;}catch(e){}
var b=document.createElement('div');b.className='privacy-note';
b.innerHTML='<span>Diese Website nutzt <b>keine Tracking-Cookies</b>. Mehr in der <a href="/datenschutz/">Datenschutzerklärung</a>.</span><button type="button">Verstanden</button>';
b.querySelector('button').addEventListener('click',function(){b.remove();try{localStorage.setItem('bww-privacy-ok','1');}catch(e){}});
if(document.body)document.body.appendChild(b);})();

/* Dezente Scroll-Reveals (progressive Enhancement, respektiert reduce-motion, Sicherheits-Fallback) */
(function(){
  var root=document.documentElement;
  if(!('IntersectionObserver' in window))return;                 // ohne Support: Inhalt bleibt sichtbar
  try{if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;}catch(e){}
  function start(){
    var targets=document.querySelectorAll('main .section, main .section-soft');
    if(!targets.length)return;
    root.classList.add('reveal-on');
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-visible');io.unobserve(e.target);}});
    },{rootMargin:'0px 0px -8% 0px',threshold:0.04});
    targets.forEach(function(t){io.observe(t);});
    setTimeout(function(){targets.forEach(function(t){t.classList.add('is-visible');});},3500); // Fallback: nie dauerhaft ausgeblendet
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();
