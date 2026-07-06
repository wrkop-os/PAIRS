/* ============================================================
   PAIRS — interactions & animations
   ============================================================ */
(() => {
  "use strict";

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const isTouch = window.matchMedia("(pointer: coarse)").matches;

  /* ---------- neural network particle canvas ---------- */
  const canvas = document.getElementById("neural-canvas");
  if (canvas && !prefersReduced) {
    const ctx = canvas.getContext("2d");
    let w, h, nodes = [], raf;
    const mouse = { x: -9999, y: -9999 };
    const DENSITY = 1 / 16000; // nodes per px²
    const LINK_DIST = 150;

    const resize = () => {
      w = canvas.width = canvas.offsetWidth * devicePixelRatio;
      h = canvas.height = canvas.offsetHeight * devicePixelRatio;
      const count = Math.min(130, Math.floor((canvas.offsetWidth * canvas.offsetHeight) * DENSITY));
      nodes = Array.from({ length: count }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.35 * devicePixelRatio,
        vy: (Math.random() - 0.5) * 0.35 * devicePixelRatio,
        r: (Math.random() * 1.6 + 0.8) * devicePixelRatio,
      }));
    };

    const step = () => {
      ctx.clearRect(0, 0, w, h);
      const linkDist = LINK_DIST * devicePixelRatio;

      for (const n of nodes) {
        n.x += n.vx; n.y += n.vy;
        if (n.x < 0 || n.x > w) n.vx *= -1;
        if (n.y < 0 || n.y > h) n.vy *= -1;

        // gentle attraction to cursor
        const dxm = mouse.x - n.x, dym = mouse.y - n.y;
        const dm = Math.hypot(dxm, dym);
        if (dm < 220 * devicePixelRatio && dm > 1) {
          n.x += (dxm / dm) * 0.25;
          n.y += (dym / dm) * 0.25;
        }
      }

      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i], b = nodes[j];
          const d = Math.hypot(a.x - b.x, a.y - b.y);
          if (d < linkDist) {
            const alpha = (1 - d / linkDist) * 0.34;
            ctx.strokeStyle = `rgba(139, 92, 246, ${alpha})`;
            ctx.lineWidth = devicePixelRatio * 0.6;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.stroke();
          }
        }
      }

      for (const n of nodes) {
        ctx.fillStyle = "rgba(34, 211, 238, 0.85)";
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fill();
      }
      raf = requestAnimationFrame(step);
    };

    resize();
    step();
    addEventListener("resize", resize);
    canvas.parentElement.addEventListener("pointermove", (e) => {
      const rect = canvas.getBoundingClientRect();
      mouse.x = (e.clientX - rect.left) * devicePixelRatio;
      mouse.y = (e.clientY - rect.top) * devicePixelRatio;
    });
    canvas.parentElement.addEventListener("pointerleave", () => {
      mouse.x = mouse.y = -9999;
    });
    // pause when hero is offscreen
    new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) { cancelAnimationFrame(raf); step(); }
      else cancelAnimationFrame(raf);
    }).observe(canvas);
  }

  /* ---------- hero 3D mouse parallax ---------- */
  const scene = document.getElementById("heroScene");
  if (scene && !prefersReduced && !isTouch) {
    const layers = scene.querySelectorAll(".hero__layer");
    let targetX = 0, targetY = 0, curX = 0, curY = 0, rafP;

    const animate = () => {
      curX += (targetX - curX) * 0.06;
      curY += (targetY - curY) * 0.06;
      layers.forEach((layer) => {
        const depth = parseFloat(layer.dataset.depth || 0.2);
        const rx = curY * -7 * depth;
        const ry = curX * 10 * depth;
        const tx = curX * 34 * depth;
        const ty = curY * 26 * depth;
        layer.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg) translate3d(${tx}px, ${ty}px, 0)`;
      });
      rafP = requestAnimationFrame(animate);
    };
    animate();

    document.querySelector(".hero").addEventListener("pointermove", (e) => {
      targetX = (e.clientX / innerWidth - 0.5) * 2;
      targetY = (e.clientY / innerHeight - 0.5) * 2;
    });
    document.querySelector(".hero").addEventListener("pointerleave", () => {
      targetX = targetY = 0;
    });
  }

  /* ---------- scroll parallax on hero + progress bar ---------- */
  const progress = document.querySelector(".scroll-progress span");
  const heroContent = document.querySelector(".hero__content");
  addEventListener("scroll", () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (progress) progress.style.width = `${(scrollY / max) * 100}%`;
    if (heroContent && !prefersReduced && scrollY < innerHeight) {
      heroContent.style.opacity = 1 - (scrollY / innerHeight) * 1.3;
      heroContent.style.translate = `0 ${scrollY * 0.35}px`;
    }
    // nav state
    document.getElementById("nav").classList.toggle("scrolled", scrollY > 30);
    // timeline fill
    const tl = document.querySelector(".timeline");
    const fill = document.getElementById("timelineFill");
    if (tl && fill) {
      const rect = tl.getBoundingClientRect();
      const pct = Math.min(1, Math.max(0, (innerHeight * 0.75 - rect.top) / rect.height));
      fill.style.height = `${pct * 100}%`;
    }
  }, { passive: true });

  /* ---------- cursor glow ---------- */
  const glow = document.querySelector(".cursor-glow");
  if (glow && !isTouch) {
    addEventListener("pointermove", (e) => {
      glow.style.left = `${e.clientX}px`;
      glow.style.top = `${e.clientY}px`;
    });
  }

  /* ---------- scroll reveal ---------- */
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.transitionDelay = `${(i % 4) * 80}ms`;
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
      const dur = 1400;
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

  /* ---------- 3D tilt cards ---------- */
  if (!isTouch && !prefersReduced) {
    document.querySelectorAll(".tilt").forEach((card) => {
      card.addEventListener("pointermove", (e) => {
        const rect = card.getBoundingClientRect();
        const px = (e.clientX - rect.left) / rect.width;
        const py = (e.clientY - rect.top) / rect.height;
        card.style.transform = `perspective(800px) rotateX(${(0.5 - py) * 10}deg) rotateY(${(px - 0.5) * 12}deg) translateY(-4px)`;
        card.style.setProperty("--mx", `${px * 100}%`);
        card.style.setProperty("--my", `${py * 100}%`);
      });
      card.addEventListener("pointerleave", () => {
        card.style.transform = "perspective(800px) rotateX(0) rotateY(0) translateY(0)";
      });
    });
  }

  /* ---------- magnetic buttons ---------- */
  if (!isTouch && !prefersReduced) {
    document.querySelectorAll(".magnetic").forEach((btn) => {
      btn.addEventListener("pointermove", (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x * 0.22}px, ${y * 0.3}px)`;
      });
      btn.addEventListener("pointerleave", () => {
        btn.style.transform = "translate(0, 0)";
      });
    });
  }

  /* ---------- typewriter ---------- */
  const tw = document.getElementById("typewriter");
  if (tw) {
    const phrases = [
      "> pairing students with mentors since day one",
      "> explore applied fields × ML specializations",
      "> read the papers. build the project. own the research.",
      "> Mon / Wed / Fri · 8:30 PM — live",
    ];
    let pi = 0, ci = 0, deleting = false;
    const type = () => {
      const phrase = phrases[pi];
      tw.textContent = phrase.slice(0, ci);
      if (!deleting && ci < phrase.length) { ci++; setTimeout(type, 42); }
      else if (!deleting) { deleting = true; setTimeout(type, 2200); }
      else if (ci > 0) { ci--; setTimeout(type, 16); }
      else { deleting = false; pi = (pi + 1) % phrases.length; setTimeout(type, 400); }
    };
    if (prefersReduced) tw.textContent = phrases[0].slice(2);
    else setTimeout(type, 1200);
  }

  /* ---------- mobile menu ---------- */
  const burger = document.getElementById("burger");
  const nav = document.getElementById("nav");
  if (burger) {
    burger.addEventListener("click", () => nav.classList.toggle("menu-open"));
    document.querySelectorAll(".nav__links a").forEach((a) =>
      a.addEventListener("click", () => nav.classList.remove("menu-open"))
    );
  }
})();
