# Deck and methodology content

Source content for the in-site slideshow and the methodology reader.
`tools/build-content.py` bundles everything here into `js/decks.js`.

## Slide decks — `P-01.json` … `P-13.json`

One file per project, keyed by the project ID used in `js/app.js`. Each holds the
deck's own text, slide by slide:

```json
{ "source": "<original file name>", "title": "<deck title>",
  "slides": [ { "n": 1, "title": "...", "body": ["...", "..."] } ] }
```

The text was extracted from the students' own `.pptx`/`.pdf` decks. Wording is
verbatim; only whitespace, slide-number artifacts and running headers were
dropped. **Presenter narration (speaker notes) is deliberately excluded** — it is
written to be spoken, names things the slide does not show, and is often in the
first person, so it does not belong on a public page. A slide that carries only a
title (its body was narration, or it holds just a diagram) renders as a centred
title card.

`P-13.json` came later than the rest: the deck was not in the shared folder
with the other twelve and was supplied separately, so its slide text was pulled
straight out of the `.pptx` rather than from the original extraction pass.

The original decks themselves are not in this repo. The design file references
them under `uploads/*.pptx`, but those files were never part of the handoff, and
the site does not link to them.

## Methodology write-ups

| File | Project | Basis for the mapping |
| --- | --- | --- |
| `method-pinn-cylinder-flow.json` | P-12 — PINNs for 2D Steady-State Flow Past a Cylinder | Document title matches the project title |
| `method-neural-ode-flight.json` | P-05 — Timescale-Aware Neural ODEs for 6-DOF Aircraft Dynamics | JSBSim F-15, 12-state 6-DOF, fast/slow timescale branching |
| `method-unnamed.json` | P-07 — Predicting Electromagnetic Interference in Circuit Boards | Subject matter: Fourier-enhanced domain-decomposed PINN for PCB EMI |

The two untitled PDFs carry no project ID or author line, so P-05 and P-07 are
matched on subject matter rather than a byline. If either is wrong, fix the entry
in `METHODOLOGY_OWNERS` in `tools/build-content.py` and re-run it.

`method-neural-ode-flight.json` is an unfinished draft: it ends mid-word and
contains the author's own placeholders (`[INSERT TABLE HERE …]`, `[Insert
Table]`). The JSON keeps them because they are what the document says; the build
filters them out of the published page.
