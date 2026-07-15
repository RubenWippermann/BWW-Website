const bookingUrl = "https://bww.kurse-verwalten.de";

function toggleMenu(){
  document.querySelector(".nav-links")?.classList.toggle("open");
}

function calculateDguv(){
  const employees = Math.max(0, parseInt(document.getElementById("employees")?.value || "0", 10));
  const branch = document.getElementById("branch")?.value || "office";
  const result = document.getElementById("calcResult");
  const note = document.getElementById("calcNote");
  if(!result || !note) return;

  let firstAiders = 0;
  if(employees >= 2 && employees <= 20) firstAiders = 1;
  if(employees > 20){
    const rate = branch === "office" ? 0.05 : 0.10;
    firstAiders = Math.ceil(employees * rate);
  }

  let paramedics = 0;
  let paramedicText = "In der Regel nicht automatisch erforderlich.";
  if(branch === "construction" && employees > 100){
    paramedics = 1;
    paramedicText = "Auf Baustellen greift die Schwelle ab mehr als 100 anwesenden Versicherten.";
  } else if(branch === "highrisk" && employees > 250){
    paramedics = 1;
    paramedicText = "Bei besonderer Art, Schwere und Zahl der Unfälle kann die Schwelle ab mehr als 250 anwesenden Versicherten greifen.";
  } else if(employees > 1500){
    paramedics = 1;
    paramedicText = "Ab mehr als 1.500 anwesenden Versicherten ist mindestens ein Betriebssanitäter zu berücksichtigen.";
  }

  result.innerHTML = `
    <div class="metric"><span>Ersthelfer mindestens</span><b>${firstAiders}</b><small>Orientierung nach DGUV Vorschrift 1 § 26</small></div>
    <div class="metric"><span>Betriebssanitäter mindestens</span><b>${paramedics}</b><small>${paramedicText}</small></div>
  `;
  note.innerHTML = employees < 2
    ? "Bitte geben Sie mindestens 2 anwesende Versicherte ein. Der Rechner arbeitet mit der typischen Anzahl anwesender Personen, nicht zwingend mit der gesamten Kopfzahl."
    : "Hinweis: Der Rechner ersetzt keine Gefährdungsbeurteilung. Schichtbetrieb, Außenstellen, erhöhte Gefahren, räumliche Verteilung und Unfallgeschehen können den Bedarf verändern.";
}

function askAssistant(topic){
  const answer = document.getElementById("assistantAnswer");
  if(!answer) return;
  const answers = {
    ersthelfer: "Für Betriebe ist entscheidend, wie viele Versicherte typischerweise gleichzeitig anwesend sind. Bei 2 bis 20 Personen wird mindestens ein Ersthelfer benötigt. Bei mehr als 20 Personen gelten Richtwerte von 5 % in Verwaltungs- und Handelsbetrieben sowie 10 % in sonstigen Betrieben. BWW unterstützt mit Aus- und Fortbildung sowie Inhouse-Terminen.",
    sanitaeter: "Betriebssanitäter werden insbesondere bei großen Betrieben, Baustellen oder erhöhtem Unfallrisiko relevant. Die Schwellen nach DGUV Vorschrift 1 § 27 sind ein guter Startpunkt; die konkrete Bewertung erfolgt über Gefährdungsbeurteilung und Organisationsstruktur.",
    brandschutz: "Brandschutzhelfer werden nach ASR A2.2 in der Regel in ausreichender Anzahl benötigt; häufig wird eine Quote von etwa 5 % der Beschäftigten als Orientierung genutzt. Je nach Brandgefährdung, Schichtbetrieb und Besucheraufkommen kann mehr sinnvoll sein.",
    inhouse: "Inhouse-Schulungen lohnen sich, wenn mehrere Mitarbeitende geschult werden sollen, Prozesse erklärt werden müssen oder die Ausbildung direkt an Ihren Räumlichkeiten stattfinden soll. Wir klären Teilnehmerzahl, Raum, Material, Abrechnung und passende Termine.",
    dozent: "Wer fachlich stark ist und Freude an verständlicher Ausbildung hat, kann sich als Dozent oder Honorarkraft bewerben. Besonders spannend sind Erste Hilfe, Brandschutz, Notfallmedizin, Sanitätsdienst und pädagogische Kursformate."
  };
  answer.textContent = answers[topic] || answers.ersthelfer;
}

document.addEventListener("DOMContentLoaded", () => {
  calculateDguv();
  document.getElementById("employees")?.addEventListener("input", calculateDguv);
  document.getElementById("branch")?.addEventListener("change", calculateDguv);
});
