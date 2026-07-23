/* BWW – Anbindung Kurs-/Buchungs-API (software-wippermann.de) */
(function () {
  var API = 'https://software-wippermann.de';
  var ORG = 'bww';
  var TEL = '+49 5527 748 7518';
  var MONTHS = ['Jan.', 'Feb.', 'März', 'Apr.', 'Mai', 'Juni', 'Juli', 'Aug.', 'Sep.', 'Okt.', 'Nov.', 'Dez.'];

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]; }); }
  function today() { var d = new Date(); function p(n){return (n<10?'0':'')+n;} return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()); }
  function fmtDate(d) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(d || '');
    if (!m) return esc(d);
    return parseInt(m[3], 10) + '. ' + MONTHS[parseInt(m[2], 10) - 1] + ' ' + m[1];
  }

  // Datum bzw. Datumsbereich (mehrtägige Kurse: datum_ende aus dem Feed)
  function fmtRange(k) {
    var a = /^(\d{4})-(\d{2})-(\d{2})$/.exec(k.datum || '');
    var b = /^(\d{4})-(\d{2})-(\d{2})$/.exec(k.datum_ende || '');
    if (!a) return esc(k.datum);
    if (!b || k.datum_ende === k.datum) return fmtDate(k.datum);
    var d1 = parseInt(a[3], 10), m1 = parseInt(a[2], 10), y1 = a[1];
    var d2 = parseInt(b[3], 10), m2 = parseInt(b[2], 10), y2 = b[1];
    if (y1 === y2 && m1 === m2) return d1 + '.–' + d2 + '. ' + MONTHS[m1 - 1] + ' ' + y1;
    if (y1 === y2) return d1 + '. ' + MONTHS[m1 - 1] + ' – ' + d2 + '. ' + MONTHS[m2 - 1] + ' ' + y1;
    return fmtDate(k.datum) + ' – ' + fmtDate(k.datum_ende);
  }

  /* ---------- Live-Termine ---------- */
  function cleanLabel(t) { return String(t == null ? '' : t).replace(/\s*\([^)]*\)/g, '').trim(); }

  function rowHTML(k) {
    var tags = [k.stadt];
    if (k.fuehrerschein_geeignet) tags.push('Führerschein');
    if (k.bg_uk_abrechenbar) tags.push('BG/UK abrechenbar');
    if (k.mehrtaegig) tags.push('mehrtägig');
    // org=bww nur anhängen, falls die API es nicht schon liefert (sonst Dublette)
    var burl = k.buchungs_url || '';
    if (burl.indexOf('org=') === -1) burl += (burl.indexOf('?') > -1 ? '&' : '?') + 'org=' + ORG;
    var voll = !!k.ausgebucht;
    var zeit = k.uhrzeit ? esc(k.uhrzeit) + (k.uhrzeit_ende ? '–' + esc(k.uhrzeit_ende) : '') + ' Uhr' : '';
    var preis = (k.preis != null && k.preis !== '') ? esc(k.preis) + ' €' : '';
    var inner =
      '<span class="termin-date"><b>' + fmtRange(k) + '</b>' + (zeit ? '<small>' + zeit + '</small>' : '') + '</span>' +
      '<span class="termin-info"><b>' + esc(k.titel) + '</b><small>' + tags.filter(Boolean).map(esc).join(' · ') + '</small></span>' +
      '<span class="termin-meta"><b>' + preis + '</b><small>' + (voll ? 'Ausgebucht' : 'Plätze frei') + '</small></span>';
    if (voll) {
      // Ausgebucht: echte Warteliste (POST /api/warteliste), kein Link zur Buchung
      return '<div class="termin-row is-full">' + inner +
        '<button type="button" class="termin-cta waitlist-toggle" data-termin="' + esc(k.id) + '" data-titel="' + esc(k.titel) + '" data-datum="' + esc(fmtRange(k)) + (k.stadt ? ' · ' + esc(k.stadt) : '') + '">Warteliste →</button></div>';
    }
    return '<a class="termin-row" href="' + esc(burl) + '" target="_blank" rel="noopener"' +
      ' data-termin-id="' + esc(k.id || '') + '" data-titel="' + esc(cleanLabel(k.titel) || '') + '">' + inner +
      '<span class="termin-cta">Buchen →</span></a>';
  }

  var EMPTY_MSG = '<p class="termine-empty">Aktuell sind hier keine offenen Termine gelistet. Fragt gern einen Wunschtermin oder <a href="/inhouse-kurse/">Inhouse-Kurs</a> an.</p>';

  function renderWithFilter(el, all) {
    // eindeutige Kursarten (Code -> lesbares Label aus dem Titel) und Städte
    var arten = {}, staedte = {};
    all.forEach(function (k) {
      if (k.kursart && !arten[k.kursart]) arten[k.kursart] = cleanLabel(k.titel);
      if (k.stadt) staedte[k.stadt] = 1;
    });
    var artKeys = Object.keys(arten).sort(function (a, b) { return arten[a].localeCompare(arten[b]); });
    var stadtKeys = Object.keys(staedte).sort();
    var showArt = artKeys.length > 1, showStadt = stadtKeys.length > 1, hasBg = all.some(function (k) { return k.bg_uk_abrechenbar; });
    var bar = '';
    if (showArt || showStadt || hasBg) {
      bar = '<div class="termine-filter">' +
        (showArt ? '<select class="tf-art" aria-label="Nach Kursart filtern"><option value="">Alle Kursarten</option>' + artKeys.map(function (c) { return '<option value="' + esc(c) + '">' + esc(arten[c]) + '</option>'; }).join('') + '</select>' : '') +
        (showStadt ? '<select class="tf-stadt" aria-label="Nach Ort filtern"><option value="">Alle Orte</option>' + stadtKeys.map(function (s) { return '<option value="' + esc(s) + '">' + esc(s) + '</option>'; }).join('') + '</select>' : '') +
        (hasBg ? '<label class="tf-bg"><input type="checkbox" class="tf-bgchk"> Nur BG/UK-abrechenbar</label>' : '') + '<span class="tf-count" aria-live="polite"></span></div>';
    }
    el.innerHTML = bar + '<div class="termine-rows"></div>';
    var artSel = el.querySelector('.tf-art'), stadtSel = el.querySelector('.tf-stadt');
    var rowsEl = el.querySelector('.termine-rows'), countEl = el.querySelector('.tf-count');
    function apply() {
      var a = artSel ? artSel.value : '', s = stadtSel ? stadtSel.value : '';
      var bgChk = el.querySelector('.tf-bgchk'), bg = bgChk && bgChk.checked;
      var f = all.filter(function (k) { return (!a || k.kursart === a) && (!s || k.stadt === s) && (!bg || k.bg_uk_abrechenbar); });
      rowsEl.innerHTML = f.length ? f.map(rowHTML).join('') : '<p class="termine-empty">Für diese Auswahl sind aktuell keine Termine frei. <a href="/inhouse-kurse/">Wunschtermin anfragen →</a></p>';
      if (countEl) countEl.textContent = f.length + (f.length === 1 ? ' Termin' : ' Termine');
    }
    if (artSel) artSel.addEventListener('change', apply);
    if (stadtSel) stadtSel.addEventListener('change', apply);
    var bgChk0 = el.querySelector('.tf-bgchk'); if (bgChk0) bgChk0.addEventListener('change', apply);
    apply();
  }

  function loadTermine() {
    var el = document.getElementById('live-termine');
    if (!el) return;
    var limitAttr = el.getAttribute('data-limit');
    // data-limit="all" (oder 0/leer) => alle Termine + Filter; sonst begrenzte Teaser-Liste
    var limit = (!limitAttr || limitAttr === 'all') ? 0 : parseInt(limitAttr, 10);
    var stadt = el.getAttribute('data-stadt') || '';
    // data-art="EHA" (oder mehrere per Komma) => nur diese Kursformate, ohne Filter-Dropdown (dedizierte Kursseite)
    var art = (el.getAttribute('data-art') || '').split(',').map(function (s) { return s.trim(); }).filter(Boolean);
    // ab_datum=heute IMMER mitgeben — sonst liefert der Feed auch vergangene Termine
    var url = API + '/api/kurse?org=' + ORG + '&ab_datum=' + today() + (stadt ? '&stadt=' + encodeURIComponent(stadt) : '');
    fetch(url).then(function (r) { return r.json(); }).then(function (data) {
      var all = (data && data.kurse) ? data.kurse : [];
      if (art.length) {
        all = all.filter(function (k) { return art.indexOf(String(k.kursart || '')) !== -1; });
        if (!all.length) { el.innerHTML = '<p class="termine-empty">Für dieses Format sind aktuell keine offenen Termine gelistet. Als Inhouse-Kurs jederzeit buchbar — <a href="#anfrage">Wunschtermin anfragen →</a></p>'; return; }
        el.innerHTML = (limit > 0 ? all.slice(0, limit) : all).map(rowHTML).join('');
        return;
      }
      if (!all.length) { el.innerHTML = EMPTY_MSG; return; }
      if (limit > 0) { el.innerHTML = all.slice(0, limit).map(rowHTML).join(''); return; }
      renderWithFilter(el, all);
    }).catch(function () {
      el.innerHTML = '<p class="termine-empty">Termine konnten gerade nicht geladen werden. Bitte später erneut versuchen oder <a href="/inhouse-kurse/">Wunschtermin anfragen →</a></p>';
    });
  }

  /* ---------- Formulare (Inhouse, Dozent, Kurs-Buchung) ---------- */
  function wireForms() {
    var forms = document.querySelectorAll('form[data-api]');
    Array.prototype.forEach.call(forms, function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var status = form.querySelector('.form-status');
        // Honeypot: ausgefülltes "website"-Feld => stiller Abbruch (Bot)
        var hp = form.querySelector('input[name="website"]');
        if (hp && hp.value) { if (status) status.textContent = 'Danke!'; return; }
        var payload = { org: ORG, website: '' };
        // Lead-Quelle für die Software (Büro trennt Inhouse-Website-Leads von Buchungen)
        if (form.getAttribute('data-api') === 'inhouse-anfrage') payload.quelle = 'inhouse-website';
        Array.prototype.forEach.call(form.querySelectorAll('[name]'), function (f) {
          var n = f.getAttribute('name');
          if (n === 'website' || n === 'consent') return; // Consent nur clientseitig erzwungen, nicht senden
          if (n === 'newsletter') return; // separat via POST /api/newsletter, nicht im Anfrage-Payload
          if (f.type === 'checkbox') {
            if (f.checked) { (payload[n] = payload[n] || []).push(f.value); }
          } else {
            payload[n] = f.value;
          }
        });
        var btn = form.querySelector('button[type="submit"]');
        var origTxt = btn ? btn.textContent : '';
        if (btn) { btn.disabled = true; btn.textContent = 'Wird gesendet …'; }
        if (status) { status.className = 'form-status'; status.textContent = ''; }
        // Newsletter (Opt-out) separat an eigenen Endpoint, fire-and-forget
        var nlEl = form.querySelector('input[name="newsletter"]');
        if (nlEl && nlEl.checked) {
          var nlMail = (form.querySelector('[name="email"]') || {}).value || '';
          if (nlMail) { try { fetch(API + '/api/newsletter', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ org: ORG, email: nlMail, quelle: form.getAttribute('data-api'), website: '' }) }); } catch (e) {} }
        }
        var httpStatus = 0;
        fetch(API + '/api/' + form.getAttribute('data-api'), {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
        }).then(function (r) { httpStatus = r.status; return r.json().catch(function () { return {}; }); }).then(function (res) {
          if (res && res.ok) {
            form.innerHTML = '<div class="form-success"><span class="form-success-ic">✓</span><h3>Danke – wir haben eure Anfrage erhalten!</h3><p>Wir melden uns zeitnah persönlich bei euch.' + (res.ticket_id ? ' Vorgangsnummer: <b>' + esc(res.ticket_id) + '</b>.' : '') + '</p></div>';
            return;
          }
          var msg;
          if (httpStatus === 429 || (res && res.error === 'too_many_requests')) {
            msg = 'Zu viele Anfragen in kurzer Zeit. Bitte in etwa einer Stunde erneut versuchen – oder ruft uns an: ' + TEL + '.';
          } else if (res && res.error === 'invalid_input') {
            msg = 'Bitte prüft eure Eingaben (Pflichtfelder, gültige E-Mail) und versucht es erneut.';
          } else {
            msg = 'Das hat leider nicht geklappt. Bitte versucht es erneut oder ruft uns an: ' + TEL + '.';
          }
          if (status) { status.className = 'form-status is-error'; status.textContent = msg; }
          if (btn) { btn.disabled = false; btn.textContent = origTxt; }
        }).catch(function () {
          if (status) { status.className = 'form-status is-error'; status.textContent = 'Verbindung fehlgeschlagen. Bitte später erneut versuchen oder anrufen: ' + TEL + '.'; }
          if (btn) { btn.disabled = false; btn.textContent = origTxt; }
        });
      });
    });
  }

  /* ---------- Warteliste (ausgebuchte Termine -> POST /api/warteliste) ---------- */
  function ensureWaitlistModal() {
    if (document.getElementById('wlModal')) return;
    var o = document.createElement('div');
    o.id = 'wlModal'; o.className = 'wl-overlay'; o.hidden = true;
    o.innerHTML =
      '<div class="wl-box" role="dialog" aria-modal="true" aria-labelledby="wlTitle">' +
        '<button type="button" class="wl-close" aria-label="Schließen">×</button>' +
        '<h3 id="wlTitle">Auf die Warteliste</h3>' +
        '<p class="wl-course"></p>' +
        '<form class="wl-form" novalidate>' +
          '<label for="wl-name">Name *</label><input id="wl-name" name="name" required>' +
          '<label for="wl-mail">E-Mail *</label><input id="wl-mail" name="email" type="email" required>' +
          '<label class="wl-consent"><input type="checkbox" name="consent" required><span>Ich habe die <a href="/datenschutz/" target="_blank" rel="noopener">Datenschutzerklärung</a> gelesen und stimme der Verarbeitung meiner Daten zu.</span></label>' +
          '<div class="hp"><label>Bitte frei lassen<input name="website" tabindex="-1" autocomplete="off"></label></div>' +
          '<button type="submit" class="btn primary">Eintragen</button>' +
          '<p class="wl-status" role="status"></p>' +
        '</form>' +
      '</div>';
    document.body.appendChild(o);
    function close() { o.hidden = true; document.body.classList.remove('wl-open'); }
    o.querySelector('.wl-close').addEventListener('click', close);
    o.addEventListener('click', function (e) { if (e.target === o) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !o.hidden) close(); });
    o.querySelector('.wl-form').addEventListener('submit', function (e) {
      e.preventDefault();
      var form = e.target, status = form.querySelector('.wl-status');
      var hp = form.querySelector('input[name="website"]');
      if (hp && hp.value) { close(); return; }
      var name = form.querySelector('input[name="name"]').value.trim();
      var email = form.querySelector('input[name="email"]').value.trim();
      var consent = form.querySelector('input[name="consent"]').checked;
      if (!name || !email || !consent) { status.className = 'wl-status is-error'; status.textContent = 'Bitte Name, E-Mail und Einwilligung ausfüllen.'; return; }
      var btn = form.querySelector('button[type="submit"]'); var orig = btn.textContent;
      btn.disabled = true; btn.textContent = 'Wird gesendet …'; status.textContent = ''; status.className = 'wl-status';
      var httpStatus = 0;
      fetch(API + '/api/warteliste', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ org: ORG, termin: o.dataset.termin || '', name: name, email: email, website: '' })
      }).then(function (r) { httpStatus = r.status; return r.json().catch(function () { return {}; }); }).then(function (res) {
        if (res && res.ok) {
          form.innerHTML = '<div class="form-success"><span class="form-success-ic">✓</span><h3>Du stehst auf der Warteliste!</h3><p>Wir melden uns, sobald ein Platz frei wird.' + (res.ticket_id ? ' Vorgang: <b>' + esc(res.ticket_id) + '</b>.' : '') + '</p></div>';
          return;
        }
        var msg = (httpStatus === 429 || (res && res.error === 'too_many_requests'))
          ? 'Zu viele Anfragen. Bitte später erneut versuchen oder anrufen: ' + TEL + '.'
          : 'Das hat nicht geklappt. Bitte erneut versuchen oder anrufen: ' + TEL + '.';
        status.className = 'wl-status is-error'; status.textContent = msg;
        btn.disabled = false; btn.textContent = orig;
      }).catch(function () {
        status.className = 'wl-status is-error'; status.textContent = 'Verbindung fehlgeschlagen. Bitte später erneut versuchen oder anrufen: ' + TEL + '.';
        btn.disabled = false; btn.textContent = orig;
      });
    });
  }
  function wireWaitlist() {
    document.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target.closest('.waitlist-toggle') : null;
      if (!t) return;
      e.preventDefault();
      ensureWaitlistModal();
      var o = document.getElementById('wlModal');
      o.dataset.termin = t.getAttribute('data-termin') || '';
      o.querySelector('.wl-course').textContent = (t.getAttribute('data-titel') || '') + (t.getAttribute('data-datum') ? ' – ' + t.getAttribute('data-datum') : '');
      // Formular zurücksetzen (falls zuvor abgeschickt)
      var f = o.querySelector('.wl-form'); if (f && f.querySelector('.form-success')) { o.remove(); ensureWaitlistModal(); o = document.getElementById('wlModal'); o.dataset.termin = t.getAttribute('data-termin') || ''; o.querySelector('.wl-course').textContent = (t.getAttribute('data-titel') || '') + (t.getAttribute('data-datum') ? ' – ' + t.getAttribute('data-datum') : ''); }
      o.hidden = false; document.body.classList.add('wl-open');
      var ni = o.querySelector('input[name="name"]'); if (ni) ni.focus();
    });
  }

  /* ---------- Kundenstimmen / Bewertungen (GET /api/bewertungen) ---------- */
  function stars(n) { n = Math.max(0, Math.min(5, parseInt(n, 10) || 0)); var s = ''; for (var i = 0; i < 5; i++) s += (i < n ? '★' : '☆'); return s; }
  function reviewHTML(b) {
    var meta = [b.quelle, b.datum].filter(Boolean).map(esc).join(' · ');
    var n = parseInt(b.sterne, 10) || 0;
    return '<figure class="review-card"><div class="review-stars" aria-label="' + n + ' von 5 Sternen">' + stars(n) + '</div>' +
      '<blockquote>' + esc(b.text || '') + '</blockquote>' +
      '<figcaption><b>' + esc(b.name || 'Anonym') + '</b>' + (meta ? '<small>' + meta + '</small>' : '') + '</figcaption></figure>';
  }
  function injectReviewSchema(list) {
    var rated = list.filter(function (b) { return parseInt(b.sterne, 10) > 0; });
    if (!rated.length) return;
    var sum = rated.reduce(function (a, b) { return a + (parseInt(b.sterne, 10) || 0); }, 0);
    var avg = Math.round((sum / rated.length) * 10) / 10;
    var node = {
      '@context': 'https://schema.org', '@type': 'EducationalOrganization', '@id': 'https://www.multiplikatorenstelle.de/#organization',
      name: 'BWW UG (haftungsbeschränkt)', url: 'https://www.multiplikatorenstelle.de/',
      aggregateRating: { '@type': 'AggregateRating', ratingValue: avg, reviewCount: rated.length, bestRating: 5, worstRating: 1 },
      review: rated.slice(0, 8).map(function (b) {
        return { '@type': 'Review', author: { '@type': 'Person', name: b.name || 'Anonym' }, reviewRating: { '@type': 'Rating', ratingValue: parseInt(b.sterne, 10), bestRating: 5, worstRating: 1 }, reviewBody: b.text || '' };
      })
    };
    var sc = document.createElement('script'); sc.type = 'application/ld+json'; sc.id = 'reviewSchema';
    sc.textContent = JSON.stringify(node); document.head.appendChild(sc);
  }
  function loadReviews() {
    var el = document.getElementById('reviews-list');
    if (!el) return;
    fetch(API + '/api/bewertungen?org=' + ORG).then(function (r) { return r.json(); }).then(function (data) {
      var list = (data && data.bewertungen) ? data.bewertungen : [];
      if (!list.length) return; // Fallback: Sektion bleibt mit Instagram/Google-CTA sichtbar
      el.innerHTML = list.slice(0, 12).map(reviewHTML).join('');
      el.hidden = false;
      injectReviewSchema(list);
    }).catch(function () { /* still: kein Bruch, Fallback-CTA bleibt */ });
  }

  /* ---------- Kurskarten anreichern: nächster Termin + Preis + Verfügbarkeit ---------- */
  function enrichCourseCards() {
    var cards = document.querySelectorAll('.course-card[data-art]');
    if (!cards.length) return;
    fetch(API + '/api/kurse?org=' + ORG + '&ab_datum=' + today()).then(function (r) { return r.json(); }).then(function (data) {
      var all = (data && data.kurse) ? data.kurse : [];
      var byArt = {};
      all.forEach(function (k) { var a = String(k.kursart || ''); (byArt[a] = byArt[a] || []).push(k); });
      Object.keys(byArt).forEach(function (a) { byArt[a].sort(function (x, y) { return String(x.datum || '').localeCompare(String(y.datum || '')); }); });
      Array.prototype.forEach.call(cards, function (card) {
        if (card.querySelector('.course-card-meta')) return;
        var list = byArt[card.getAttribute('data-art')] || [];
        var next = list.filter(function (k) { return !k.ausgebucht; })[0] || list[0];
        var meta = document.createElement('div'); meta.className = 'course-card-meta';
        if (next) {
          var voll = !!next.ausgebucht;
          var preis = (next.preis != null && next.preis !== '') ? esc(next.preis) + ' €' : '';
          meta.innerHTML = '<span class="ccm-date">' + fmtRange(next) + '</span>' +
            (preis ? '<span class="ccm-price">' + preis + '</span>' : '') +
            '<span class="ccm-status ' + (voll ? 'is-full' : 'is-free') + '">' + (voll ? 'Warteliste' : 'Plätze frei') + '</span>';
        } else {
          meta.innerHTML = '<span class="ccm-inhouse">Inhouse jederzeit buchbar</span>';
        }
        var link = card.querySelector('.text-link');
        if (link) card.insertBefore(meta, link); else card.appendChild(meta);
      });
    }).catch(function () { /* kein Bruch: Karten bleiben ohne Meta */ });
  }

  var UE_MAP = {
    'Erste-Hilfe-Ausbildung': 9, 'Erste-Hilfe-Fortbildung': 9,
    'Erste Hilfe am Kind (Baby/Kleinkind)': 4,
    'Erste Hilfe für Bildungs- & Betreuungseinrichtungen': 8,
    'Reanimation & AED-Training': 4, 'AED-Einweisung': 2,
    'Brandschutzhelfer': 4, 'Betriebssanitäter Grundausbildung': 72,
    'Betriebssanitäter Aufbaulehrgang': 40, 'Betriebssanitäter Fortbildung': 16,
    'Notfalltraining (Gesundheitswesen)': 4, 'Schulsanitäter-Ausbildung': 16,
    'Sanitätshelfer-Ausbildung': 24, 'Lehrkräfte-Ausbildung (Themenbereich I & II)': 24,
    'Lehrkräfte-Fortbildung': 8
  };
  // Uhrzeit-Dauer-Override in Zeitstunden für Formate, deren Zeitdauer von UE×45min abweicht (Feed/öffentliche Angabe maßgeblich)
  var DUR_H_OVERRIDE = { 'Notfalltraining (Gesundheitswesen)': 4 };
  function fmtDurMin(name) { if (DUR_H_OVERRIDE[name] != null) return DUR_H_OVERRIDE[name] * 60; var ue = UE_MAP[name]; if (ue == null) return 0; var m = ue * 45; if (ue >= 6) m += 45; return m; }
  function fmtHM(mins) { var h = Math.floor(mins / 60) % 24, m = mins % 60; return (h < 10 ? '0' : '') + h + ':' + (m < 10 ? '0' : '') + m; }
  function wireStartzeit() {
    var forms = document.querySelectorAll('form[data-api="inhouse-anfrage"]');
    Array.prototype.forEach.call(forms, function (form) {
      var timeEl = form.querySelector('input[name="wunsch_startzeit"]');
      var hint = form.querySelector('.startzeit-hint');
      if (!timeEl || !hint) return;
      function upd() {
        var v = timeEl.value;
        if (!v) { hint.textContent = ''; return; }
        var checked = Array.prototype.filter.call(form.querySelectorAll('input[name="kursart"]:checked'), function (c) { return fmtDurMin(c.value) > 0; });
        if (!checked.length) { hint.textContent = 'Endzeit richtet sich nach dem gewählten Kursformat.'; return; }
        var mins = Math.max.apply(null, checked.map(function (c) { return fmtDurMin(c.value); }));
        var multiDay = mins > 9 * 60;
        var daily = multiDay ? 8 * 60 : mins;
        var pp = v.split(':'); var start = (+pp[0]) * 60 + (+pp[1]);
        hint.textContent = 'ca. ' + v + '–' + fmtHM(start + daily) + ' Uhr' + (multiDay ? ' · pro Tag (mehrtägig)' : '') + ' – Richtwert';
      }
      timeEl.addEventListener('change', upd); timeEl.addEventListener('input', upd);
      Array.prototype.forEach.call(form.querySelectorAll('input[name="kursart"]'), function (c) { c.addEventListener('change', upd); });
    });
  }

  /* ---------- Testimonials (freigegebene Kundenstimmen mit Logo) — Sektion bleibt verborgen, bis Daten da sind ---------- */
  function testimonialHTML(t) {
    var logo = t.logo_url ? '<img class="tm-logo" src="' + esc(t.logo_url) + '" alt="' + esc(t.firma || 'Kundenlogo') + '" loading="lazy" decoding="async">' : '';
    var who = [t.person, t.rolle].filter(Boolean).map(esc).join(' · ');
    return '<figure class="testimonial-card">' + logo +
      '<blockquote>' + esc(t.text || '') + '</blockquote>' +
      '<figcaption>' + (t.firma ? '<b>' + esc(t.firma) + '</b>' : '') + (who ? '<span>' + who + '</span>' : '') + '</figcaption></figure>';
  }
  function loadTestimonials() {
    var el = document.getElementById('testimonials-list');
    if (!el) return;
    fetch(API + '/api/testimonials?org=' + ORG).then(function (r) { return r.json(); }).then(function (data) {
      var list = (data && data.testimonials) ? data.testimonials : [];
      if (!list.length) return;                       // keine Freigaben -> Sektion bleibt aus (nichts erfinden)
      el.innerHTML = list.slice(0, 9).map(testimonialHTML).join('');
      var sec = document.getElementById('testimonials');
      if (sec) sec.hidden = false;
    }).catch(function () { /* Endpoint noch nicht live -> Sektion bleibt aus */ });
  }

  /* ---------- Feature-Flags (schalten Online-Zahlung scharf, ohne Deploy) ---------- */
  var FEATURES = {};
  function loadFeatures() {
    return fetch(API + '/api/features?org=' + ORG).then(function (r) { return r.json(); })
      .then(function (f) { FEATURES = f || {}; }).catch(function () { FEATURES = {}; });
  }

  /* ---------- Online-Buchung + Bezahlung (gated: nur aktiv, wenn FEATURES.online_zahlung) ---------- */
  function ensureBookingModal() {
    if (document.getElementById('bkModal')) return;
    var o = document.createElement('div');
    o.id = 'bkModal'; o.className = 'wl-overlay'; o.hidden = true;
    o.innerHTML =
      '<div class="wl-box bk-box" role="dialog" aria-modal="true" aria-labelledby="bkTitle">' +
        '<button type="button" class="wl-close" aria-label="Schließen">×</button>' +
        '<h3 id="bkTitle">Kurs buchen &amp; bezahlen</h3><p class="wl-course"></p>' +
        '<form class="wl-form bk-form" novalidate>' +
          '<label for="bk-vorname">Vorname *</label><input id="bk-vorname" name="vorname" autocomplete="given-name" required>' +
          '<label for="bk-nachname">Nachname *</label><input id="bk-nachname" name="nachname" autocomplete="family-name" required>' +
          '<label for="bk-mail">E-Mail *</label><input id="bk-mail" name="email" type="email" autocomplete="email" required>' +
          '<label for="bk-firma">Firma (optional)</label><input id="bk-firma" name="firma" autocomplete="organization">' +
          '<label for="bk-strasse">Rechnungsadresse *</label><input id="bk-strasse" name="strasse" autocomplete="street-address" placeholder="Straße &amp; Hausnummer" required>' +
          '<div class="fgrid"><div><label for="bk-plz">PLZ *</label><input id="bk-plz" name="plz" autocomplete="postal-code" required></div>' +
          '<div><label for="bk-ort">Ort *</label><input id="bk-ort" name="ort" autocomplete="address-level2" required></div></div>' +
          '<div class="hp"><label>Bitte frei lassen<input name="website" tabindex="-1" autocomplete="off"></label></div>' +
          '<label class="consent"><input type="checkbox" name="consent" required><span>Ich habe die <a href="/datenschutz/" target="_blank" rel="noopener">Datenschutzerklärung</a> und die <a href="/agb/" target="_blank" rel="noopener">AGB</a> gelesen und akzeptiere sie.</span></label>' +
          '<button class="btn primary" type="submit">Weiter zur Zahlung</button>' +
          '<p class="wl-status" role="status" aria-live="polite"></p>' +
          '<p class="bk-note">Die Zahlung läuft über unseren Zahlungsdienstleister. Kartendaten werden nie auf dieser Website eingegeben.</p>' +
        '</form></div>';
    document.body.appendChild(o);
    function close() { o.hidden = true; }
    o.querySelector('.wl-close').addEventListener('click', close);
    o.addEventListener('click', function (e) { if (e.target === o) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    o.querySelector('form').addEventListener('submit', function (e) {
      e.preventDefault();
      var f = e.target, st = f.querySelector('.wl-status');
      if (f.querySelector('[name="website"]').value) return;                 // Honeypot
      if (!f.querySelector('[name="consent"]').checked) { st.textContent = 'Bitte Datenschutz und AGB bestätigen.'; return; }
      var btn = f.querySelector('button[type="submit"]');
      var payload = { org: ORG, termin: o.getAttribute('data-termin') || '', anzahl: 1, website: '',
        teilnehmer: [{ vorname: f.vorname.value.trim(), nachname: f.nachname.value.trim(), email: f.email.value.trim() }],
        rechnung: { firma: f.firma.value.trim(), strasse: f.strasse.value.trim(), plz: f.plz.value.trim(), ort: f.ort.value.trim(), email: f.email.value.trim() } };
      st.textContent = 'Buchung wird geprüft …'; btn.disabled = true;
      fetch(API + '/api/kurs-buchung', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, status: r.status, j: j }; }); })
        .then(function (res) {
          var d = res.j || {};
          if (res.ok && d.checkout_url) { st.textContent = 'Weiterleitung zur sicheren Zahlung …'; window.location.href = d.checkout_url; return; }
          btn.disabled = false;
          var msg = { course_full: 'Dieser Termin ist leider ausgebucht. Setzt euch gern auf die Warteliste.',
                      course_past: 'Dieser Termin liegt in der Vergangenheit. Bitte wählt einen aktuellen Termin.',
                      invalid_email: 'Bitte prüft die E-Mail-Adresse.',
                      already_booked: 'Für diese E-Mail liegt bereits eine Buchung zu diesem Termin vor.',
                      invalid_input: 'Bitte prüft eure Eingaben.' }[d.error];
          st.textContent = msg || 'Es ist ein Fehler aufgetreten. Bitte versucht es später erneut oder ruft uns an.';
        })
        .catch(function () { btn.disabled = false; st.textContent = 'Verbindung fehlgeschlagen. Bitte erneut versuchen.'; });
    });
  }
  function openBookingModal(id, titel) {
    ensureBookingModal();
    var o = document.getElementById('bkModal');
    o.setAttribute('data-termin', id || '');
    o.querySelector('.wl-course').textContent = titel || '';
    var s = o.querySelector('.wl-status'); if (s) s.textContent = '';
    o.hidden = false;
    var first = o.querySelector('input'); if (first) first.focus();
  }
  function wireBooking() {
    document.addEventListener('click', function (e) {
      if (FEATURES.online_zahlung !== true) return;                 // gated -> normaler buchungs_url-Link greift
      var a = e.target && e.target.closest ? e.target.closest('.termin-row[data-termin-id]') : null;
      if (!a || !a.getAttribute('data-termin-id')) return;
      e.preventDefault();
      openBookingModal(a.getAttribute('data-termin-id'), a.getAttribute('data-titel'));
    });
  }

  function init() { loadTermine(); wireForms(); wireWaitlist(); loadReviews(); enrichCourseCards(); wireStartzeit(); loadTestimonials(); loadFeatures(); wireBooking(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
