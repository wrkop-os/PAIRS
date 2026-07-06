# PAIRS — Summer AI/ML Research & Mentorship Program

A complete redesign of the PAIRS program website ([original Google Site](https://sites.google.com/view/summermlairp/home)) as a fast, dependency-free static site.

## Features

- **3D parallax hero** — mouse-driven depth layers (`rotateX`/`rotateY`/`translate3d`), an animated perspective grid floor, floating code chips, and a live neural-network particle canvas that reacts to the cursor
- **Full animation suite** — scroll-reveal sections, animated stat counters, 3D tilt cards with spotlight hover, magnetic buttons, gradient-shift text, glitch hover on the headline, typewriter ticker, scroll-progress bar, animated timeline fill, marquee strip, cursor glow
- **Responsive** — mobile nav, stacked layouts, touch devices skip pointer-only effects
- **Accessible** — respects `prefers-reduced-motion`, semantic HTML, keyboard-friendly FAQ accordions

## Structure

```
index.html      # all content/sections
css/style.css   # design system + animations
js/main.js      # canvas, parallax, reveals, interactions
```

No build step — open `index.html` in a browser, or serve the folder with any static host (GitHub Pages, Netlify, Vercel).

## Program facts on the site

Meeting days/times, program dates (June 29 – September 4), phases, curriculum, tools and contact info are drawn from official PAIRS program materials. Edit `index.html` to update copy.
