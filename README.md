# PAIRS — Program for Applied Independent Research in the Summer

Static site for the PAIRS summer AI/ML research and mentorship program: four tabs
(Home, Members, Projects, Awards), a detail panel for every mentor, student,
project and award, an in-site slideshow of each project's real presentation deck,
and a reader for the projects that have a written methodology.

No build step is needed to serve it — it is plain HTML, CSS and JS. Two scripts
regenerate the generated files when the source content changes (see below).

## Layout

```
index.html            # generated — page shell + the markup template
css/site.css          # design-system subset (blueprint frames, cards, overlays)
css/responsive.css    # tablet and phone layout
js/dc-runtime.js      # template runtime ({{ }}, <sc-if>, <sc-for>)
js/image-slot.js      # <image-slot> image frame with a missing-asset fallback
js/app.js             # generated — site data, state, hero animation, viewers
js/decks.js           # generated — slide decks + methodology text
content/decks/*.json  # source content for js/decks.js
design/               # the design handoff this site was built from
uploads/              # photos, project covers, award badges, logos
tools/                # the two generators
```

## Regenerating

```bash
python3 tools/build-content.py   # content/decks/*.json  -> js/decks.js
python3 tools/build-site.py      # design/PAIRS_Site.dc.html -> index.html + js/app.js
```

`index.html` and `js/app.js` are generated from `design/PAIRS_Site.dc.html`, the
design-canvas export in `design/`. Edit the design file (or the build script) and
re-run — hand edits to the generated files are overwritten. `tools/build-site.py`
fails loudly if the design file changes shape enough that one of its edits no
longer matches, so a silently half-applied build is not possible.

The design prototype ran on an internal editor runtime (`<sc-if>`, `<sc-for>`,
`{{ }}` bindings, a drag-and-drop `<image-slot>`, and an "Industry" design-system
bundle). None of that ships, so the build converts the markup and logic to run
against `js/dc-runtime.js`, `js/image-slot.js` and `css/site.css` instead.

## Content

Mentors, students, projects and awards are real, final content and live in the
design file's own data arrays (carried into `js/app.js` verbatim).

Slide decks and methodology write-ups live in `content/decks/` — see
[content/decks/README.md](content/decks/README.md) for where each came from and
how the text was extracted.

## Known gaps

- `uploads/Shahzeb Wali.jpg` and `uploads/Brandon Sweet.jpeg` are missing, so
  those two mentor cards show a placeholder frame. Drop the files in at those
  exact paths and they appear — no code change needed.
- `uploads/pairs-logo-horizontal.svg` and `uploads/pairs-logo-stacked.svg` are
  stand-ins drawn to match the palette. Replace them with the real logo files at
  the same paths.

## Deploying

`.github/workflows/deploy-pages.yml` publishes to the `gh-pages` branch on a push
to `claude/ml-mentorship-website-vo7qpq`. Any static host works too: serve the
folder as-is.
