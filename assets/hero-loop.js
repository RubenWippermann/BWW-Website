/* Hero-Loop (Startseite): Video erst nach window load, nur Desktop (min-width 1024px, hover:hover),
   nicht bei prefers-reduced-motion / Datensparmodus / 2g. Das Poster steht sofort im HTML. */
(function () {
  var wrap = document.querySelector(".hero-scene[data-loop]");
  if (!wrap || !window.matchMedia) return;
  var mm = window.matchMedia;
  if (!mm("(min-width: 1024px) and (hover: hover)").matches) return;
  if (mm("(prefers-reduced-motion: reduce)").matches) return;
  var c = navigator.connection;
  if (c && (c.saveData || /(^|-)2g$/.test(c.effectiveType || ""))) return;
  function start() {
    var v = document.createElement("video");
    v.className = "hero-loop";
    v.muted = true; v.loop = true; v.playsInline = true; v.preload = "metadata";
    v.setAttribute("aria-hidden", "true"); v.tabIndex = -1;
    v.setAttribute("muted", ""); v.setAttribute("playsinline", "");
    v.addEventListener("canplay", function () {
      var p = v.play();
      if (p && p.then) p.then(function () { v.classList.add("is-playing"); }, function () { v.remove(); });
      else v.classList.add("is-playing");
    }, { once: true });
    v.addEventListener("error", function () { v.remove(); });
    v.src = wrap.getAttribute("data-loop");
    wrap.appendChild(v);
  }
  if (document.readyState === "complete") setTimeout(start, 300);
  else window.addEventListener("load", function () { setTimeout(start, 300); }, { once: true });
})();
