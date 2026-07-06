# PAIRS — Summer AI/ML Research & Mentorship Program

Static site for the PAIRS program ([original Google Site](https://sites.google.com/view/summermlairp/home)).

## Structure

```
index.html      # content/sections + Three.js importmap
css/style.css   # emerald theme, layout, UI animations
js/scene.js     # "Flow Wave" Three.js scene (ES module)
js/main.js      # UI interactions (reveals, counters, tilt, nav)
```

The background is a WebGL "Flow Wave" scene (Three.js r143 via unpkg importmap): a particle
sheet displaced by two octaves of simplex noise, rendered through three EffectComposers
(torus/bloom/final) with an UnrealBloom pipeline and a composite pass that adds the dark-emerald
background and corner-flame haze. Page scroll drives the camera dive from a high view down into
the field; the cursor parallaxes the camera and parts the particles where it points. Ambient
motes are camera-attached drifting points.

No build step — serve the folder with any static host (GitHub Pages, Netlify, Vercel).
Three.js loads from unpkg at runtime, so an internet connection is required.

## Program facts

Meeting days/times, program dates (June 29 – September 4), phases, curriculum, tools and
contact info come from official PAIRS program materials. Edit `index.html` to update copy.
