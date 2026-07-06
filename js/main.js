/* ============================================================
   PAIRS — UI interactions & HUD (the Flow Wave scene lives in scene.js)
   ============================================================ */
(() => {
  "use strict";

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- scroll: progress bar, nav state, timeline fill ---------- */
  const progress = document.getElementById("scrollFill");
  const nav = document.getElementById("nav");
  const timeline = document.querySelector(".timeline");
  const timelineFill = document.getElementById("timelineFill");

  addEventListener("scroll", () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (progress && max > 0) progress.style.width = `${(scrollY / max) * 100}%`;
    nav.classList.toggle("scrolled", scrollY > 30);
    if (timeline && timelineFill) {
      const rect = timeline.getBoundingClientRect();
      const pct = Math.min(1, Math.max(0, (innerHeight * 0.75 - rect.top) / rect.height));
      timelineFill.style.height = `${pct * 100}%`;
    }
  }, { passive: true });

  /* ---------- scroll reveal ---------- */
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.transitionDelay = `${(i % 4) * 70}ms`;
        entry.target.classList.add("visible");
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

  /* ---------- animated counters ---------- */
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const end = parseInt(el.dataset.count, 10);
      const dur = 1200;
      const t0 = performance.now();
      const tick = (t) => {
        const p = Math.min(1, (t - t0) / dur);
        el.textContent = Math.round(end * (1 - Math.pow(1 - p, 3)));
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
      counterObserver.unobserve(el);
    });
  }, { threshold: 0.6 });
  document.querySelectorAll(".stat__num").forEach((el) => counterObserver.observe(el));

  /* ---------- mobile menu ---------- */
  const burger = document.getElementById("burger");
  if (burger) {
    burger.addEventListener("click", () => nav.classList.toggle("menu-open"));
    document.querySelectorAll(".nav__links a").forEach((a) =>
      a.addEventListener("click", () => nav.classList.remove("menu-open"))
    );
  }

  /* ============================================================
     HUD: clock, section tracker, live scene telemetry
     ============================================================ */
  const hudClock = document.getElementById("hudClock");
  const hudSection = document.getElementById("hudSection");
  const hudTelemetry = document.getElementById("hudTelemetry");

  /* UTC clock */
  const pad = (n) => String(n).padStart(2, "0");
  const updateClock = () => {
    const d = new Date();
    hudClock.textContent =
      `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())} ` +
      `${pad(d.getUTCHours())}:${pad(d.getUTCMinutes())}:${pad(d.getUTCSeconds())} UTC`;
  };
  updateClock();
  setInterval(updateClock, 1000);

  /* section tracker */
  const sections = [...document.querySelectorAll("[data-sec]")];
  const TOTAL = sections.length;
  const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const el = entry.target;
        hudSection.textContent = `SEC ${el.dataset.sec}/${pad(TOTAL)} · ${el.dataset.name}`;
      }
    });
  }, { rootMargin: "-45% 0px -45% 0px" });
  sections.forEach((s) => sectionObserver.observe(s));

  /* live telemetry from the Flow Wave scene */
  let frames = 0, fps = 0, fpsT0 = performance.now();
  const countFrame = (t) => {
    frames++;
    if (t - fpsT0 >= 1000) { fps = frames; frames = 0; fpsT0 = t; }
    requestAnimationFrame(countFrame);
  };
  if (!prefersReduced) requestAnimationFrame(countFrame);

  const signed = (v) => `${v < 0 ? "-" : "+"}${Math.abs(v).toFixed(2).padStart(5, "0")}`;
  const updateTelemetry = () => {
    const w = window.__flowWave;
    if (w && hudTelemetry) {
      const max = document.documentElement.scrollHeight - innerHeight;
      const sc = max > 0 ? Math.round((scrollY / max) * 100) : 0;
      const swell = (w.uniforms.uWaveHeight.value / 3).toFixed(2);
      hudTelemetry.textContent =
        `SCROLL ${String(sc).padStart(3, "0")}% · ` +
        `CAM ${signed(w.camera.position.y)}/${signed(w.camera.position.z)} · ` +
        `SWELL ${swell}x · ${fps || "--"} FPS`;
    }
  };
  setInterval(updateTelemetry, 150);
})();
