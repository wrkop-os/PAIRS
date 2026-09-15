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

## Slide images

All twelve projects show their deck's real slides — 222 images, rendered from
the source files to `uploads/slides/P-XX/NN.webp`. `tools/build-content.py`
picks those up automatically and the viewer switches from text slides to image
slides; a project with no images falls back to rendering its deck's text.

Two of the decks (P-04, P-10) are ~10.2 MB, and the Drive connector drops its
session partway through a download that size rather than refusing cleanly —
`get_file_metadata` on the same file answers instantly, so it is the payload,
not access. Those two were supplied directly instead. Either route below
re-renders any deck.

### Rendering from the Drive connector (how ten of them were done)

An agent session with the Google Drive connector can pull decks under roughly
10 MB directly. Oversized tool results are spilled to a JSON file rather than
returned inline, so the deck's bytes never have to pass through a context
window — read `content` out of that file, base64-decode it, and hand the
result to `tools/render_slides.py`'s `to_pdf()` and `rasterise()`.

### Rendering on a GitHub runner (no size limit)

1. Share the Drive folder holding the decks as **Anyone with the link → Viewer**:
   <https://drive.google.com/drive/folders/1L_wC6d70zFuG8VAIq9j6E1BeBQ4GFfWY>
2. Re-run the **Render deck slides** workflow
   (`.github/workflows/render-slides.yml`). It installs LibreOffice, downloads
   each deck anonymously, converts it and rasterises every page, then commits
   the result. While the folder is private it exits clean, having rendered
   nothing, and says so.

## Content

Mentors, students, projects and awards are real, final content and live in the
design file's own data arrays (carried into `js/app.js` verbatim).

Slide decks and methodology write-ups live in `content/decks/` — see
[content/decks/README.md](content/decks/README.md) for where each came from and
how the text was extracted.

## Logo

`uploads/pairs-logo-horizontal.svg` and `uploads/pairs-logo-stacked.svg` both
carry the real program seal. If the horizontal and stacked lockups (the seal set
beside or above the wordmark) are wanted instead, replace those two files at the
same paths — the header sizes the mark by height alone, so either shape fits.

## Deploying

Live at <https://pairs-ml.vercel.app>. Vercel builds that project from this
repository's default branch, `claude/ml-mentorship-website-vo7qpq`, so a merge
to it deploys to production on its own; other branches get a preview URL.
`.github/workflows/deploy-pages.yml` also publishes to `gh-pages` on the same
push. Any static host works too: serve the folder as-is.
