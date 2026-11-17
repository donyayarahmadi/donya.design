/* Donya Design — interactions. Vanilla JS, no libraries. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };

  /* ---------- Letter-roll hover on nav links ---------- */
  $$("[data-roll]").forEach(function (el) {
    var t = el.textContent.trim();
    el.innerHTML = '<span class="roll"><span>' + t + "</span><span>" + t + "</span></span>";
  });

  /* ---------- Split the About paragraph into words ---------- */
  $$("[data-words]").forEach(function (el) {
    el.innerHTML = el.textContent.trim().split(/\s+/).map(function (w) {
      return '<span class="w">' + w + "</span>";
    }).join(" ");
  });

  /* ---------- Hash routing: #exam, #subjects, #books, #connecta ---------- */
  var views = { education: 1, exam: 1, subjects: 1, books: 1, connecta: 1 };
  function route() {
    var h = (location.hash || "").replace("#", "");
    var name = views[h] ? h : "home";
    $$(".view").forEach(function (v) { v.classList.toggle("on", v.id === "view-" + name); });
    document.body.classList.toggle("is-case", name !== "home");
    $$(".nav a").forEach(function (a) { a.classList.toggle("active", a.dataset.nav === (name === "home" ? (h === "work" ? "work" : "home") : "work")); });
    document.title = name === "home" ? "Donya Yarahmadi — Product Designer" : ($("#view-" + name + " h1").textContent + " — Donya Yarahmadi");
    if (h === "work") {
      var w = $("#work");
      if (w) setTimeout(function () { window.scrollTo({ top: w.getBoundingClientRect().top + window.scrollY - 70, behavior: reduce ? "auto" : "smooth" }); }, 30);
    } else {
      window.scrollTo(0, 0);
    }
    observe();
    onScroll();
  }
  window.addEventListener("hashchange", route);

  /* ---------- Reveal on view ---------- */
  var io = "IntersectionObserver" in window ? new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      el.classList.add("in");
      if (el.dataset.count) countUp(el);
      if (el.classList.contains("stat") || el.classList.contains("step")) lightDots(el);
      io.unobserve(el);
    });
  }, { rootMargin: "0px 0px -12% 0px", threshold: 0.05 }) : null;

  function observe() {
    $$(".view.on .reveal, .view.on .work, .view.on .cs-cover, .view.on .approach-title, .view.on [data-count], .view.on .stat, .view.on .step").forEach(function (el) {
      if (el.classList.contains("in")) return;
      if (io && !reduce) io.observe(el); else { el.classList.add("in"); if (el.dataset.count) el.textContent = el.dataset.count + (el.dataset.suffix || ""); lightDots(el); }
    });
  }

  function countUp(el) {
    var end = parseFloat(el.dataset.count), suffix = el.dataset.suffix || "", t0 = null, dur = 1400;
    function tick(t) {
      if (!t0) t0 = t;
      var p = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * e) + suffix;
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  function lightDots(el) {
    $$(".dots i", el).forEach(function (d, i) { setTimeout(function () { d.classList.add("on"); }, 180 * (i + 1)); });
  }

  /* ---------- Scroll-linked effects ---------- */
  var ticking = false;
  function progressOf(el) {
    var r = el.getBoundingClientRect(), h = window.innerHeight;
    return clamp(-r.top / Math.max(1, r.height - h), 0, 1);
  }

  function onScroll() {
    ticking = false;
    if (reduce) return;
    var home = $("#view-home");
    if (!home || !home.classList.contains("on")) return;

    // Hero: title drifts up and fades, portrait flips from black & white to colour and grows.
    var hero = $(".hero");
    if (hero) {
      var p = progressOf(hero);
      var title = $(".hero-title");
      title.style.transform = "translateY(" + (-p * 32) + "vh)";
      title.style.opacity = String(1 - clamp((p - 0.15) / 0.45, 0, 1));
      var portrait = $(".portrait");
      var stage = $(".portrait-stage");
      var e = 1 - Math.pow(1 - p, 2);
      var rotY = 180 - 180 * clamp(p / 0.6, 0, 1);
      var tilt = 18 * (1 - clamp(p / 0.6, 0, 1));
      var scale = 1 + e * 0.85;
      var base = window.innerWidth < 761 ? 46 : 66, lift = window.innerWidth < 761 ? 22 : 46;
      stage.style.top = (base - lift * e) + "vh";
      portrait.style.transform = "rotateY(" + rotY + "deg) rotateX(" + tilt * 0.4 + "deg) rotateZ(" + (-tilt * 0.25) + "deg) scale(" + scale + ")";
      $(".hero-hint").style.opacity = String(1 - clamp(p / 0.15, 0, 1));
    }

    // About: words light up as the paragraph passes through the viewport.
    var about = $(".about-text");
    if (about) {
      var r = about.getBoundingClientRect(), vh = window.innerHeight;
      var ap = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1);
      var words = $$(".w", about), n = Math.round(ap * words.length);
      words.forEach(function (w, i) { w.classList.toggle("lit", i < n); });
    }

    // "Case  studies": the two words slide in from the edges and meet in the middle.
    var split = $(".cs-split");
    if (split) {
      var sp = progressOf(split), k = 1 - Math.pow(1 - clamp(sp / 0.7, 0, 1), 3);
      var off = (1 - k) * 36;
      $(".cs-split .word.l").style.transform = "translateX(" + (-off) + "vw)";
      $(".cs-split .word.r").style.transform = "translateX(" + off + "vw)";
    }
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  window.addEventListener("resize", onScroll);

  /* ---------- Testimonials carousel ---------- */
  var slides = $$(".slide"), dots = $$(".carousel .dots i"), cur = 0, timer;
  function show(i) {
    cur = (i + slides.length) % slides.length;
    slides.forEach(function (s, k) { s.classList.toggle("on", k === cur); });
    dots.forEach(function (d, k) { d.classList.toggle("on", k <= cur); });
  }
  function auto() { clearInterval(timer); if (!reduce) timer = setInterval(function () { show(cur + 1); }, 7000); }
  if (slides.length) {
    $(".prev").addEventListener("click", function () { show(cur - 1); auto(); });
    $(".next-t").addEventListener("click", function () { show(cur + 1); auto(); });
    show(0); auto();
  }

  /* ---------- Lightbox for case-study screenshots ---------- */
  var lb = $(".lightbox");
  document.addEventListener("click", function (e) {
    var ph = e.target.closest && e.target.closest("figure .ph");
    if (ph) {
      var img = $("img", ph), cap = ph.parentElement.querySelector("figcaption");
      $("img", lb).src = img.src; $("img", lb).alt = img.alt;
      $("p", lb).textContent = cap ? cap.textContent : "";
      lb.classList.add("on");
      return;
    }
    if (lb.classList.contains("on") && e.target.closest(".lightbox")) lb.classList.remove("on");
  });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") lb.classList.remove("on"); });


  /* ---------- Prototype walkthroughs: auto-play when visible, click to step ---------- */
  $$(".flow").forEach(function (fl) {
    var steps = fl.dataset.steps.split("|").map(function (s) {
      var p = s.split("~"), hs = p[1] ? p[1].split(",").map(Number) : null;
      return { cap: p[0], hs: hs };
    });
    var imgs = $$(".flow-stage img", fl), segs = $$(".flow-bar i", fl), tap = $(".tap", fl);
    var cap = $(".flow-cap", fl), count = $(".flow-count", fl), ppBtn = $(".fpp", fl);
    var i = 0, playing = !reduce, visible = false, t0 = 0, raf = null, phase = "view";
    var VIEW = 2600, TAP = 900;
    function show(n) {
      i = (n + steps.length) % steps.length;
      imgs.forEach(function (im, k) { im.classList.toggle("on", k === i); if (k <= i + 1) im.loading = "eager"; });
      segs.forEach(function (sg, k) { sg.classList.toggle("done", k < i); $("b", sg).style.width = k < i ? "100%" : "0"; });
      cap.textContent = steps[i].cap; count.textContent = (i + 1) + " / " + steps.length;
      tap.classList.remove("show"); phase = "view"; t0 = performance.now();
    }
    function tick(now) {
      raf = null;
      if (!playing || !visible) return;
      var el = now - t0, total = VIEW + (steps[i].hs ? TAP : 0);
      $("b", segs[i]).style.width = Math.min(100, el / total * 100) + "%";
      if (phase === "view" && el > VIEW && steps[i].hs) {
        tap.style.left = steps[i].hs[0] + "%"; tap.style.top = steps[i].hs[1] + "%";
        tap.classList.add("show"); phase = "tap";
      }
      if (el > total + (steps[i].hs ? 0 : 800)) show(i + 1);
      raf = requestAnimationFrame(tick);
    }
    function run() { if (!raf && playing && visible) { t0 = performance.now() - 0; raf = requestAnimationFrame(tick); } }
    function setPlaying(p) { playing = p; ppBtn.textContent = p ? "PAUSE" : "PLAY"; ppBtn.setAttribute("aria-label", p ? "Pause" : "Play"); if (p) { t0 = performance.now(); run(); } }
    $(".flow-stage", fl).addEventListener("click", function () { setPlaying(false); show(i + 1); });
    $(".fn", fl).addEventListener("click", function () { setPlaying(false); show(i + 1); });
    $(".fp", fl).addEventListener("click", function () { setPlaying(false); show(i - 1); });
    ppBtn.addEventListener("click", function () { setPlaying(!playing); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) { t0 = performance.now(); run(); } }, { threshold: 0.4 }).observe(fl);
    }
    show(0); setPlaying(playing);
  });

  /* ---------- Start ---------- */
  route();
  requestAnimationFrame(function () { document.body.classList.add("loaded"); });
})();
