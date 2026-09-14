# Handoff: PAIRS ML Mentorship Program Site

## Overview
A four-tab site for PAIRS (Program for Applied Independent Research in the Summer), a 10-week ML mentorship program. Tabs: Home (program pitch + curriculum), Members (mentor + student roster), Projects (filterable gallery of 12 real student projects, each with an in-site slideshow viewer), Awards (5 juried awards tied to specific projects/students). Clicking any member, project, or award card opens a detail modal.

## About the Design Files
The files in this bundle are **design references built as an HTML prototype** (using an internal design-component runtime, not a shippable web framework). They show intended layout, styling, copy, and interaction behavior — they are not production code to copy directly. The task is to **recreate this design in the target codebase's existing environment** (React, Vue, or whatever the receiving app already uses) using its own component patterns, routing, and state management — or, if no environment exists yet, to pick the most suitable framework and implement there.

## Fidelity
**High-fidelity.** Colors, type, spacing, and the wireframe/blueprint visual system are final. All content is final: real mentor and student names, photos, and bios; real project titles, abstracts, and teams pulled from the students' own presentation decks; real award winners.

## Design System
Built on an internal design system called "Industry": light steel-blue-on-paper wireframe aesthetic. Key characteristics to recreate:
- **Palette**: background #f2f2f3 (paper), text #1d1f20, accent #5980a6 (steel blue), accent-dark #416180 (used for labels/kickers, links), muted text #424244 / #5d5d60 / #7a7a7d, borders rgba(29,31,32,.16), dark band #1d2d3d, footer bg #e9e9ea.
- **Type**: Barlow Condensed (headings, semibold, tight letter-spacing on labels) + Barlow (body). Monospace (ui-monospace/SF Mono/Menlo) for all-caps kicker/label text with wide letter-spacing (0.12–0.22em).
- **"Blueprint" card pattern**: square corners (no border-radius), 1px hairline border, transparent/no fill, with four small "+" registration-mark glyphs in the corners (.corner.tl/.tr/.bl/.br). Used on every card, image frame, and modal.
- **Duotone image treatment**: photo slots are wrapped to receive a steel-blue duotone filter.
- No rounded corners anywhere; no drop shadows except a subtle hover lift on project/award cards.

## Screens / Views

### Header (persistent, all tabs)
- Sticky top bar, rgba(242,242,243,.92) background with blur, 1px bottom border.
- Left: PAIRS horizontal logo (42px height) + mono wrapped program name "PROGRAM FOR APPLIED INDEPENDENT RESEARCH IN THE SUMMER" (10px, max-width 150px).
- Center: 4 tab buttons — Home / Members / Projects / Awards. Barlow Condensed 600, 15px, uppercase, 0.14em spacing; inactive #5d5d60, active #1d1f20 with 2px accent bottom border.
- Right: mono date range "JUN 29 → SEP 04".

### Home tab
1. **Hero** (full-bleed, overflow hidden, bottom border): absolute background grid layer (parallax-shifted on scroll), full-bleed canvas behind text rendering a rotating 3D node-graph (abstract feed-forward network, perspective-projected, cursor-reactive, pulsing edges/nodes in accent-dark). Decorative only — reimplement in the target stack's canvas/WebGL layer or swap for an equivalent looping graphic. Foreground: stacked PAIRS logo (150px), H1 "Program for Applied Independent Research in the Summer" (48px, normal case — no uppercase transform), body paragraph: "Ten weeks. Four mentors, thirty-plus students, twenty projects. You start at machine-learning fundamentals and finish with …" (19px, #424244, max-width 520px).
2. **Stats bar**: 7-column grid, each cell left-bordered hairline. Big number (Barlow Condensed 600, 44px, accent-dark) + mono unit label, then a muted description line. Values: 10 WEEKS · 4 MENTORS · 30+ STUDENTS · 20 PROJECTS · 3 SESS/WK · 1:1 · (7th stat per current source — check PROJECTS/stats array in file for the live wording).
3. **"Four definitions" section**: header row (kicker "01 / FUNDAMENTALS"). Two-column intro (46px H2 "What is machine learning?" + body). 4-column grid of blueprint cards (Model, Training data, Loss, Generalization).
4. **Pipeline band** (dark, full-bleed #1d2d3d, white text): kicker "02 / A PIPELINE", H2 "An ML system is five steps in a loop.", 5-column grid of steps (Frame, Data, Train, Evaluate, Iterate).
5. **Curriculum section**: kicker "03 / CURRICULUM", H2 "What we teach, and what you cross it with." Two blueprint cards: "A · ML SPECIALIZATIONS" and "B · APPLIED FIELDS" — **both tag lists are generated live from the actual PROJECTS array** (`Array.from(new Set(PROJECTS.map(p => p.method)))` / `.field`), not a hardcoded list. Recreate this as a derived/computed list from the real project data source, not a static array.

### Members tab
- H2 "Who you'll work with." + intro paragraph.
- **Mentors** (4, in this order): Kashfi Rehan (Program Director & Lead Mentor), Shahzeb Wali (Director of Agentic AI Systems & Web Development), Arian Akther (Applied Specializations & Fields Mentor), Brandon Sweet (Deep Learning Mentor). 4-column grid of blueprint cards, each with a real duotone photo, mono ID (M-01…), name, role, scope line, and a bio in its detail modal. All four have real photos and bios in-file.
- **Students** (14 real students with real photos/names/bios, no filler/placeholder entries): grid of cards, each with photo, mono ID (S-01…), name, and track. Click opens a modal with the student's bio and their project (title, abstract, awards, and a "View slideshow" action).

### Projects tab
- H2 "Everything built here." + intro paragraph.
- **Filter row**: tag buttons for method categories, derived from the real project data.
- **Grid**: 3-column, blueprint cards with hover lift. Each project has a **uniquely generated cover image** — 12 distinct hand-designed motifs (bit-stream columns, pivot-arm arcs, stepped discharge bars, voltage curves, flight trajectory, anomaly scatter, circuit traces, pitch-line diagram, retina rings, sunburst, graph network, flow streamlines past a cylinder), each in its own color treatment tied to the project's field — not a repeated template. Card shows mono ID + year, title, blurb, method+field tags, and an award line if the project won one.
- Clicking a card opens its modal with the full abstract, team, metadata, and a **"View slideshow" action that opens an in-site lightbox** (not an external link/download): a full-screen overlay with prev/next controls paging through images rendered from the project's actual presentation deck content (title + bullet text per slide, extracted from the source PPTX/PDF). Recreate this as a real embedded slide viewer over the actual deck asset (PDF pages or a slides API) rather than a file download link.

### Awards tab
- H2 "Certificates & awards." + intro paragraph ("Five awards juried by the mentors...").
- 2-column grid of blueprint cards, each showing: award badge icon (96px), award name, and the winning student(s)/project. Five awards, each with a fixed description (shown in the card and modal):
  - **PAIRS Distinguished Scholar Award** — strongest overall project, balancing originality, technical quality, execution, impact, and communication.
  - **Technical Excellence Award** — outstanding computational/theoretical rigor, ML sophistication, engineering, or analytical depth. Winner: Wilson Shao (Timescale-Aware Neural ODEs).
  - **Innovation Award** — most original idea, novel interdisciplinary connection, or creative contribution. Winners: Tirtha Saha & Alexander Soll (PICASO).
  - **Scientific Rigor Award** — exceptional experimental design, evaluation, reproducibility, methodology. Winners: Ethan Tan, Arthur Zin, Dennis Zhuo.
  - **Applied Impact Award** — strongest real-world significance, practical value, or societal relevance. Winner: Rishav Banik.
- Clicking a card opens a modal with the full description, winning team, and their project.

### Detail Modal (shared: mentor / student / project / award)
- Full-screen backdrop rgba(29,31,32,.55), click-outside to close.
- Blueprint-framed panel, max-width 900px, max-height 84vh scrollable, paper background.
- Top row: mono kicker (e.g. "MENTOR · M-01", "PROJECT · P-05") + "CLOSE ✕" button.
- Two-column body (image column + text column): left is a duotone+blueprint photo slot with a metadata key/value list below it; right is title, mono subtitle, body text, a "CERTIFICATES & AWARDS" mini-card section (award badge icons have their default grey placeholder background stripped via `image-slot::part(frame){background:transparent}` since real badge art is always present here), and link/action buttons (solid accent-blue, mono uppercase) — including "View slideshow" for projects, which triggers the in-site lightbox rather than navigating away.

### Lightbox (slideshow viewer)
- Separate full-screen overlay (z-index above the modal), dark background, title bar with a close button, a 16:9 image stage with prev/next arrow buttons, and a "SLIDE n / total" counter. Backed by per-project slide image arrays generated from each project's real deck content.

### Footer
- #e9e9ea background, top hairline border. Mono row: program full name (left), date range (center), "MON · WED · FRI · ET" (right).

## Interactions & Behavior
- **Tab switching**: click Home/Members/Projects/Awards — swaps the visible section, scrolls window to top. No URL routing was implemented; use real routes in the rebuild.
- **Hero animation**: canvas-based rotating node graph, auto-rotates, reacts to pointer position and scroll. Purely decorative.
- **Card hover**: project/award cards lift + soft shadow + accent border; member cards get a faint accent-tinted background on hover.
- **Modal**: opening any card sets modal content and shows the overlay; click backdrop or "CLOSE ✕" to dismiss.
- **Lightbox**: opened from a project's or award's "View slideshow" link; prev/next cycle through that project's slide images; close returns to the modal/page beneath.
- **Project filter**: clicking a filter chip narrows the projects grid (client-side, no network call).
- No form validation, no loading/error states — static content site with local UI state only (active tab, open modal, open lightbox, active filter).
- Not responsive in the original — built at a fixed ~1440px design width; add real breakpoints for the grid column counts in the rebuild.

## State Management
Minimal local UI state, no backend calls:
- `tab`: "home" | "members" | "projects" | "awards".
- `modal`: null | detail-panel object (kicker, title, subtitle, body, image slot id, metadata rows, awards list, links list).
- `filter`: selected project-category filter string (default "All").
- `lightbox`: null | { title, images: string[], index } — drives the slideshow overlay.

All mentor, student, project, and award data is a **hardcoded in-file array** (MENTORS, STUDENTS, PROJECTS, AWARD_DESCRIPTIONS in the script) — real, final content, not placeholder. In production this should come from a real data source (CMS/database/JSON); the shapes double as the content schema to replicate:
- Mentor: { id, name, title, scope, photo, bio }.
- Student: { id, name, track, photo, bio } tied to one project.
- Project: { id, year, title, blurb, method, field, team, award, awardIcon, slides[] } + a generated cover image.
- Award: { name, description, winner(s), project } — from a fixed 5-entry description map, joined against PROJECTS.

## Design Tokens
- **Colors**: bg #f2f2f3, text #1d1f20, text-muted #424244 / #5d5d60 / #7a7a7d, accent #5980a6, accent-dark #416180, border rgba(29,31,32,.16), dark-band bg #1d2d3d, dark-band text #f2f2f3, footer bg #e9e9ea, link color #416180 (hover #5980a6).
- **Typography**: Headings — Barlow Condensed, weight 600. Body — Barlow, 13.5–19px, line-height 1.4–1.6. Mono labels — ui-monospace/SF Mono/Menlo, 9.5–11.5px, letter-spacing 0.12–0.22em, uppercase.
- **Spacing**: section vertical padding 44–96px; horizontal gutters 40px; card padding 20–32px; grid gaps 22–64px.
- **Border radius**: 0 everywhere.
- **Borders/shadows**: 1px hairline rgba(29,31,32,.16) on all cards/dividers; hover shadow on project/award cards: 0 3px 10px rgba(43,43,45,.16).
- **Corner marks**: every blueprint-framed element carries 4 "+" registration-mark glyphs (.corner.tl/.tr/.bl/.br inside a .blueprint container).

## Assets
All included in `uploads/` in this bundle:
- **Logos**: pairs-logo-horizontal.svg (header, 42px), pairs-logo-stacked.svg (hero, 150px).
- **Mentor photos**: 4 real photos (Kashfi Rehan, Shahzeb Wali, Arian Akther, Brandon Sweet).
- **Student photos**: real photos for all 14 students.
- **Project cover images**: `uploads/covers/P-01.png` … `P-12.png` — generated, uniquely-composed cover art per project (not photography; each is a distinct diagram/motif tied to the project's method/field).
- **Slide images**: `uploads/slides/P-01/`…`P-12/` — per-project slide images rendered from each deck's real text content, used by the in-site lightbox viewer.
- **Award badges**: award-technical-excellence.png, award-innovation.png, award-scientific-rigor.png, award-applied-impact.png, award-distinguished-scholar-*.png.
- **Fonts**: Barlow and Barlow Condensed (Google Fonts), loaded via the bound Industry design-system stylesheet, not directly in this file.

## Files
- `PAIRS Site.dc.html` — the full prototype (all four tabs, modals, lightbox, and the canvas hero animation) in one file. Primary reference — view source for exact markup, inline styles, and the JS driving state/animation/data.
- `image-slot.js` — the drag-and-drop photo placeholder widget used throughout (a custom element; recreate as your framework's own image component, not to be ported verbatim).
- `uploads/` — every real image asset referenced above.
- The Industry design-system bundle (referenced from `_ds/`, not included in this handoff) supplies the shared card/button/blueprint CSS classes and corner-mark glyphs — ask if you need that bundle's raw CSS/JS as well.
