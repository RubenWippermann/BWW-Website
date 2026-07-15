"use client";

import Image from "next/image";
import { useState } from "react";

const BOOKING_URL = "https://bww.kurse-verwalten.de";

const courses = [
  {
    title: "Erste Hilfe im Betrieb",
    label: "DGUV",
    image: "/media/course-first-aid.jpg",
    text: "Aus- und Fortbildung betrieblicher Ersthelfender - praxisnah und auf Ihre Organisation abgestimmt.",
    facts: ["9 Unterrichtseinheiten", "Für Betriebe & Teams", "BG-Abrechnung möglich"],
  },
  {
    title: "Erste Hilfe am Kind",
    label: "Kita & Schule",
    image: "/media/course-rescue.jpg",
    text: "Sicher handeln bei Notfällen mit Säuglingen und Kindern - für Bildungs- und Betreuungseinrichtungen.",
    facts: ["Praxisorientiert", "Inhouse möglich", "Bescheinigung inklusive"],
  },
  {
    title: "Erste Hilfe für den Führerschein",
    label: "§ 19 FeV",
    image: "/media/course-driving.jpg",
    text: "Der kompakte Erste-Hilfe-Kurs für Führerscheinbewerberinnen und Führerscheinbewerber.",
    facts: ["1 Kurstag", "Amtliche Bescheinigung", "Direkt online anfragen"],
  },
  {
    title: "Rettungsdienst & Notfallmedizin",
    label: "Fachfortbildung",
    image: "/media/course-medical.jpg",
    text: "Fort- und Weiterbildung für medizinisches Fachpersonal, Einsatzkräfte und Organisationen.",
    facts: ["Fachlich fundiert", "Individuelle Module", "Für Teams & Einrichtungen"],
  },
];

const standards = [
  ["304-001", "Ermächtigung von Stellen für die Aus- und Fortbildung in der Ersten Hilfe"],
  ["304-002", "Aus- und Fortbildung für den betrieblichen Sanitätsdienst"],
  ["304-003", "Aus- und Fortbildung von Lehrkräften und Multiplikatorenstellen"],
];

export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);

  function chooseCourse(title: string) {
    window.location.href = `${BOOKING_URL}?kurs=${encodeURIComponent(title)}`;
  }

  return (
    <main>
      <div className="topbar">
        <div className="shell topbar-inner">
          <span>Multiplikatorenstelle · Rettungsdienstbildungsstelle</span>
          <div><a href="tel:+4955277487518">+49 (0) 5527 748 7518</a><a href="mailto:info@multiplikatorenstelle.de">info@multiplikatorenstelle.de</a></div>
        </div>
      </div>

      <header className="site-header">
        <div className="shell nav-wrap">
          <a className="brand" href="#start" aria-label="BWW Startseite">
            <Image src="/media/bww-logo.jpeg" alt="BWW - Leben retten leicht gemacht" width={420} height={198} priority />
          </a>
          <button className="menu-button" onClick={() => setMenuOpen(!menuOpen)} aria-expanded={menuOpen} aria-label="Navigation öffnen">
            <span /> <span /> <span />
          </button>
          <nav className={menuOpen ? "open" : ""} aria-label="Hauptnavigation">
            <a href="#kurse" onClick={() => setMenuOpen(false)}>Kurse</a>
            <a href="#leistungen" onClick={() => setMenuOpen(false)}>Leistungen</a>
            <a href="#ueber-uns" onClick={() => setMenuOpen(false)}>Über uns</a>
            <a href="#kontakt" onClick={() => setMenuOpen(false)}>Kontakt</a>
            <a className="nav-cta" href={BOOKING_URL} onClick={() => setMenuOpen(false)}>Kurs buchen</a>
          </nav>
        </div>
      </header>

      <section className="hero" id="start">
        <video className="hero-video" autoPlay muted loop playsInline preload="metadata" poster="/media/reanimation-poster.jpg" aria-label="Reanimationstraining mit Herzdruckmassage und Beatmung">
          <source src="/media/reanimation.m4v" type="video/mp4" />
        </video>
        <div className="hero-overlay" />
        <div className="shell hero-content">
          <p className="eyebrow light">Multiplikatorenstelle &amp; Rettungsdienstbildungsstelle</p>
          <h1>Leben retten.<br /><em>Leicht gemacht.</em></h1>
          <p className="hero-lead"><strong>Schwerpunkt des Unternehmens: Erste Hilfe &amp; Notfallmedizin.</strong> Professionelle Aus- und Fortbildung - verständlich, praxisnah und digital organisiert.</p>
          <div className="hero-actions">
            <a className="button button-primary" href="#kurse">Passenden Kurs finden <span>→</span></a>
            <a className="button button-ghost" href="#leistungen">BWW kennenlernen</a>
          </div>
          <div className="hero-trust">
            <span><b>DGUV-orientiert</b> nach 304-001/-002/-003</span>
            <span><b>Praxisnah</b> für echte Handlungssicherheit</span>
            <span><b>Digital</b> von Anfrage bis Verwaltung</span>
          </div>
        </div>
      </section>

      <section className="audience-strip" aria-label="Zielgruppen">
        <div className="shell audience-grid">
          <span>Für Unternehmen</span><i />
          <span>Für Bildungsstätten</span><i />
          <span>Für Fahrschulen</span><i />
          <span>Für Rettungsdienste</span>
        </div>
      </section>

      <section className="section shell" id="kurse">
        <div className="section-heading split-heading">
          <div><p className="eyebrow">Unser Kursangebot</p><h2>Wissen, das zu <em>Handeln</em> wird.</h2></div>
          <p>Vom ersten sicheren Handgriff bis zur spezialisierten medizinischen Fortbildung: Unsere Angebote verbinden klare Didaktik mit realitätsnaher Praxis.</p>
        </div>
        <div className="course-grid">
          {courses.map((course) => (
            <article className="course-card" key={course.title}>
              <div className="course-image"><Image src={course.image} alt="" fill sizes="(max-width: 800px) 100vw, 50vw" /><span>{course.label}</span></div>
              <div className="course-body">
                <h3>{course.title}</h3><p>{course.text}</p>
                <ul>{course.facts.map((fact) => <li key={fact}>{fact}</li>)}</ul>
                <button onClick={() => chooseCourse(course.title)}>Kurs anfragen <span>→</span></button>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="standards" id="leistungen">
        <div className="shell standards-grid">
          <div className="standards-copy">
            <p className="eyebrow light">Qualität mit System</p>
            <h2>Ausbildung nach <em>klaren Grundsätzen.</em></h2>
            <p>Als Multiplikatorenstelle und Partner für Bildungsorganisationen orientieren wir unsere Leistungen an den einschlägigen DGUV-Grundsätzen und entwickeln daraus praxistaugliche Bildungsprozesse.</p>
            <a className="text-link light-link" href="https://www.dguv.de/fb-erstehilfe/vorschriften-und-fachinformationen/vorschriften-regeln-grundsaetze/index.jsp" target="_blank" rel="noreferrer">DGUV-Grundsätze ansehen ↗</a>
          </div>
          <div className="standard-list">
            {standards.map(([number, title]) => <div className="standard-row" key={number}><b>{number}</b><span>{title}</span></div>)}
          </div>
        </div>
      </section>

      <section className="section shell" id="ueber-uns">
        <div className="feature-grid">
          <div className="feature-photo"><Image src="/media/course-medical.jpg" alt="Medizinische Fortbildung im Hörsaal" fill sizes="(max-width: 800px) 100vw, 50vw" /></div>
          <div className="feature-copy">
            <p className="eyebrow">Mehr als ein Kursanbieter</p>
            <h2>Bildung. Beratung. <em>Entwicklung.</em></h2>
            <p>BWW steht für das Bildungswerk für Wiederbelebung und Erste Hilfe. Unser Schwerpunkt liegt auf medizinischer Breitenbildung, notfallmedizinischer Fortbildung und dem professionellen Aufbau von Schulungsstrukturen.</p>
            <div className="service-list">
              <div><b>01</b><span><strong>Aus- und Fortbildung</strong>Erste Hilfe, Sanitätsdienst und Notfallmedizin</span></div>
              <div><b>02</b><span><strong>Multiplikatorenstelle</strong>Qualifizierung von Lehrkräften und Begleitung von Anerkennungsverfahren</span></div>
              <div><b>03</b><span><strong>Strukturberatung</strong>Curricula, QM-Handbücher und digitale Bildungsorganisation</span></div>
            </div>
            <a className="text-link" href="#kontakt">Individuelle Leistung besprechen →</a>
          </div>
        </div>
      </section>

      <section className="booking-section" id="buchen">
        <div className="shell booking-grid">
          <div className="booking-intro">
            <p className="eyebrow light">Online anfragen</p>
            <h2>Ihr Kurs beginnt <em>hier.</em></h2>
            <p>Bis zur vollständigen Anbindung unserer neuen Software laufen Kursbuchungen über die bestehende Kursverwaltung.</p>
            <div className="selected-course"><span>Aktuelle Buchungsstrecke</span><strong>bww.kurse-verwalten.de</strong><small>Direkte Weiterleitung zur Kursauswahl und Anmeldung</small></div>
            <p className="software-note">Die neue Schnittstelle zu <a href="https://www.software-wippermann.de" target="_blank" rel="noreferrer">software-wippermann.de</a> ist vorbereitet. Bis dahin nutzen Sie bitte die bestehende Kursverwaltung.</p>
          </div>
          <div className="booking-card">
            <div className="success-message booking-redirect" role="status">
              <div className="success-mark">→</div>
              <p className="eyebrow">Online buchen</p>
              <h3>Kurse direkt auswählen</h3>
              <p>Sie werden zur bestehenden BWW-Kursverwaltung weitergeleitet. Dort können Sie verfügbare Termine einsehen und Kurse online buchen.</p>
              <a className="submit-button full" href={BOOKING_URL}>Zur Kursbuchung<span>→</span></a>
              <p className="form-hint full">Die Buchung erfolgt bis zur neuen Software-Schnittstelle über bww.kurse-verwalten.de.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="contact-section" id="kontakt">
        <div className="shell contact-grid">
          <div><p className="eyebrow">Direkter Draht</p><h2>Was können wir für Sie <em>möglich machen?</em></h2></div>
          <div className="contact-links"><a href="tel:+4955277487518"><span>Telefon</span><strong>+49 (0) 5527 748 7518</strong></a><a href="mailto:info@multiplikatorenstelle.de"><span>E-Mail</span><strong>info@multiplikatorenstelle.de</strong></a></div>
        </div>
      </section>

      <footer>
        <div className="shell footer-grid">
          <div className="footer-brand"><Image src="/media/bww-logo.jpeg" alt="BWW" width={330} height={156} /><p>Bildungswerk für Wiederbelebung und Erste Hilfe<br />Multiplikatorenstelle · Rettungsdienstbildungsstelle<br />Schwerpunkt: Erste Hilfe &amp; Notfallmedizin</p></div>
          <div><h3>Kontakt</h3><p>BWW UG (haftungsbeschränkt)<br />Worbiser Straße 2<br />37115 Duderstadt<br />Deutschland</p><p><a href="mailto:info@multiplikatorenstelle.de">info@multiplikatorenstelle.de</a><br /><a href="tel:+4955277487518">+49 (0) 5527 748 7518</a></p></div>
          <div><h3>Rechtliches</h3><a href="#impressum">Impressum</a><a href="/legal/Datenschutz_BWW.pdf" target="_blank">Datenschutz (PDF)</a><a href="/legal/AGB_BWW.pdf" target="_blank">AGB & Widerruf (PDF)</a><a href="#streitbeilegung">Verbraucherschlichtung</a></div>
          <div><h3>Partner & Standards</h3><a href="https://www.software-wippermann.de" target="_blank" rel="noreferrer">Software Wippermann ↗</a><a href="https://www.dguv.de/fb-erstehilfe/" target="_blank" rel="noreferrer">DGUV Fachbereich Erste Hilfe ↗</a></div>
        </div>
        <div className="shell legal-panel" id="impressum">
          <details><summary>Impressum anzeigen</summary><div className="legal-content"><h3>Angaben gemäß § 5 DDG</h3><p><strong>BWW UG (haftungsbeschränkt)</strong><br />Geschäftsführer: Ruben Wippermann<br />Worbiser Straße 2, 37115 Duderstadt, Deutschland</p><p>E-Mail: info@multiplikatorenstelle.de<br />Telefon: +49 (0) 5527 748 7518</p><p>Registergericht: Amtsgericht Göttingen<br />Handelsregister: HRB 207725<br />Steuernummer: 35/200/03084<br />USt-IdNr.: DE458801252</p><h3>Verantwortlich für journalistisch-redaktionelle Inhalte gemäß § 18 Abs. 2 MStV</h3><p>Ruben Wippermann, Worbiser Straße 2, 37115 Duderstadt</p></div></details>
          <details id="streitbeilegung"><summary>Verbraucherschlichtung</summary><div className="legal-content"><p>Die BWW UG (haftungsbeschränkt) ist nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p><p>Hinweis: Die frühere europäische OS-Plattform wurde zum 20. Juli 2025 eingestellt. Ein entsprechender Link wird daher nicht mehr als aktive Streitbeilegungsplattform ausgewiesen.</p></div></details>
        </div>
        <div className="shell footer-bottom"><span>© {new Date().getFullYear()} BWW UG (haftungsbeschränkt)</span><span>Digitale Kursorganisation in Verbindung mit Software Wippermann</span></div>
      </footer>
    </main>
  );
}
