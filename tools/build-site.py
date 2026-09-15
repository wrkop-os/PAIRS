#!/usr/bin/env python3
"""Rebuild index.html and js/app.js from the design-canvas source file.

The design was handed over as `PAIRS Site.dc.html`, a prototype that runs on a
proprietary editor runtime. This script mechanically converts it into the
standalone site: it lifts the markup into a <template>, lifts the component
logic into js/app.js, and applies the edits the shipping site needs (responsive
hooks, deck-backed slideshow, methodology reader).

Re-run it after replacing design/PAIRS_Site.dc.html with a newer export:

    python3 tools/build-site.py
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "design" / "PAIRS_Site.dc.html"

fail = []


def sub_once(text, old, new, label):
    """Replace exactly one occurrence, recording a failure if it isn't there."""
    if text.count(old) != 1:
        fail.append(f"{label}: expected 1 occurrence, found {text.count(old)}")
        return text
    return text.replace(old, new, 1)


def sub_many(text, old, new, label, expect):
    if text.count(old) != expect:
        fail.append(f"{label}: expected {expect} occurrences, found {text.count(old)}")
        return text
    return text.replace(old, new)


src = SOURCE.read_text()
markup = re.search(r"</helmet>\s*(.*?)\s*<script type=\"text/x-dc\"", src, re.S).group(1)
logic = re.search(r"<script type=\"text/x-dc\"[^>]*>\n(.*?)\n</script>", src, re.S).group(1)
markup = markup.replace("</x-dc>", "").strip()

# ---------------------------------------------------------------- markup ---
# Responsive hooks. The design file styles everything inline, so the mobile
# stylesheet needs attribute hooks to hang overrides on.
def hook_style(text, needle, name, expect):
    """Tag every element whose inline style contains `needle` with data-r."""
    pattern = re.compile(r'(<[a-zA-Z][\w-]*)((?:\s+[^>]*?)?style="[^"]*' + re.escape(needle) + r'[^"]*")')
    text, hits = pattern.subn(lambda m: f'{m.group(1)} data-r="{name}"{m.group(2)}', text)
    if hits != expect:
        fail.append(f"style hook {name}: expected {expect}, found {hits}")
    return text


def hook_tag(text, needle, name, expect):
    """Tag an element matched by an exact opening-tag prefix."""
    if text.count(needle) != expect:
        fail.append(f"tag hook {name}: expected {expect}, found {text.count(needle)}")
        return text
    head, _, rest = needle.partition(" ")
    return text.replace(needle, f'{head} data-r="{name}" {rest}'.rstrip(), expect)


# Layout containers, keyed by a distinctive fragment of their inline style.
markup = hook_style(markup, "grid-template-columns:repeat(7,1fr)", "stats", 1)
markup = hook_style(markup, "grid-template-columns:repeat(5,1fr);gap:1px", "pipeline", 1)
markup = hook_style(markup, "grid-template-columns:repeat(5,1fr);gap:22px", "grid5", 1)
markup = hook_style(markup, "grid-template-columns:repeat(4,1fr)", "grid4", 2)
markup = hook_style(markup, "grid-template-columns:repeat(3,1fr);gap:26px", "grid3", 1)
markup = hook_style(markup, "grid-template-columns:repeat(2,1fr);gap:26px", "grid2", 1)
markup = hook_style(markup, "grid-template-columns:1.05fr 1fr", "two", 2)
markup = hook_style(markup, "grid-template-columns:1fr 1fr;gap:26px", "two", 1)
markup = hook_style(markup, "grid-template-columns:300px 1fr;gap:34px", "modalbody", 1)
markup = hook_style(markup, "position:sticky", "header", 1)
markup = hook_style(markup, "position:relative;height:680px", "hero", 1)
markup = hook_style(markup, "height:260px;width:auto", "hero-logo", 1)
markup = hook_style(markup, "height:42px;width:auto", "logo", 1)
markup = hook_style(markup, "max-width:150px", "logo-name", 1)
markup = hook_style(markup, "font-size:48px", "h1", 1)
markup = hook_style(markup, "font-size:19px;line-height:1.5;max-width:520px", "hero-lede", 1)
markup = hook_style(markup, "font-size:46px", "h2", 7)
markup = hook_style(markup, "font-size:18px;line-height:1.6;color:#424244", "lede", 5)
markup = hook_style(markup, "padding:96px 40px", "section", 2)
markup = hook_style(markup, "padding:44px 40px", "section", 1)
markup = hook_style(markup, "background:#1d2d3d;color:#f2f2f3;padding:92px 40px", "band", 1)
markup = hook_style(markup, "padding:76px 40px 110px", "section-tall", 3)
markup = hook_style(markup, "border-top:1px solid rgba(29,31,32,.16);padding:26px 40px 46px", "footer", 1)
markup = hook_tag(markup, '<nav style="display:flex;gap:34px">', "nav", 1)
markup = hook_tag(markup, '<div id="pairs-hero-text"', "hero-text", 1)
markup = hook_tag(markup, '<span class="mono" style="font-size:10px;letter-spacing:.16em;color:#7a7a7d">JUN 29', "dates", 1)

# Right-hand section labels ("ROSTER · 4 ENTRIES") are decoration with no room
# on a phone. The same styling is used for project-card IDs, which must stay —
# so match on the label text and skip the pure-binding cards.
META_LABEL = re.compile(
    r'<p class="mono" style="font-size:10px;letter-spacing:\.18em;color:#7a7a7d;margin:0">(?!\{\{)')
markup, meta_hits = META_LABEL.subn(
    '<p data-r="meta-right" class="mono" style="font-size:10px;letter-spacing:.18em;color:#7a7a7d;margin:0">', markup)
if meta_hits != 6:
    fail.append(f"meta right: expected 6 occurrences, found {meta_hits}")

# Modal chrome hooks.
markup = sub_once(markup,
    '<div style="position:fixed;inset:0;z-index:200;background:rgba(29,31,32,.55);display:flex;align-items:center;justify-content:center;padding:48px"',
    '<div data-r="modalwrap" style="position:fixed;inset:0;z-index:200;background:rgba(29,31,32,.55);display:flex;align-items:center;justify-content:center;padding:48px"',
    "modal wrap")
markup = sub_once(markup,
    '<div class="blueprint" style="background:#f2f2f3;max-width:900px;width:100%;max-height:84vh;overflow:auto"',
    '<div class="blueprint" data-r="modalpanel" style="background:#f2f2f3;max-width:900px;width:100%;max-height:84vh;overflow:auto"',
    "modal panel")
markup = sub_once(markup,
    '<div style="display:flex;justify-content:space-between;align-items:flex-start;padding:26px 30px 0">',
    '<div data-r="modalhead" style="display:flex;justify-content:space-between;align-items:flex-start;padding:26px 30px 0">',
    "modal head")
markup = sub_once(markup,
    '<div class="{{ modal.photoWrapClass }}" style="height:300px;background:{{ modal.photoBg }}">',
    '<div class="{{ modal.photoWrapClass }}" data-r="modalphoto" style="height:300px;background:{{ modal.photoBg }}">',
    "modal photo")
markup = sub_once(markup, '<h2 style="font-size:38px;line-height:1.05;margin:0 0 6px">{{ modal.title }}</h2>',
    '<h2 data-r="modaltitle" style="font-size:38px;line-height:1.05;margin:0 0 6px">{{ modal.title }}</h2>', "modal title")

# --------------------------------------------------- slideshow + reader ---
# The prototype's lightbox paged through pre-rendered slide PNGs that were
# never handed over. Replace it with a viewer that renders each deck's real
# text content, and keep the image path for decks that do carry images.
OLD_LIGHTBOX = re.search(r'  <sc-if value="\{\{ hasLightbox \}\}".*?</sc-if>\n', markup, re.S).group(0)
NEW_LIGHTBOX = '''  <sc-if value="{{ hasLightbox }}">
  <div data-r="lbwrap" style="position:fixed;inset:0;z-index:300;background:rgba(29,31,32,.94);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:32px" onClick="{{ closeLightboxHandler }}">
    <div data-r="lbhead" style="display:flex;align-items:center;justify-content:space-between;gap:16px;width:100%;max-width:1100px;margin-bottom:14px" onClick="{{ stop }}">
      <p class="mono" style="font-size:11px;letter-spacing:.14em;color:#f2f2f3;margin:0;max-width:72%">{{ lightbox.title }}</p>
      <button onClick="{{ closeLightboxHandler }}" class="mono" style="border:1px solid rgba(242,242,243,.4);background:transparent;color:#f2f2f3;font-size:11px;letter-spacing:.1em;padding:8px 14px;cursor:pointer">CLOSE ✕</button>
    </div>
    <div data-r="lbstage" style="position:relative;width:100%;max-width:1100px;aspect-ratio:16/9;background:#f2f2f3" onClick="{{ stop }}">
      <sc-if value="{{ lightbox.hasImage }}">
      <image-slot id="lightbox-slide" shape="rect" fit="contain" placeholder="Slide" src="{{ lightbox.currentImage }}"></image-slot>
      </sc-if>
      <sc-if value="{{ lightbox.hasText }}">
      <article class="slide {{ lightbox.slideClass }}">
        <i class="corner tl"></i><i class="corner tr"></i><i class="corner bl"></i><i class="corner br"></i>
        <p class="mono slide-n">{{ lightbox.slideKicker }}</p>
        <h3 class="slide-title">{{ lightbox.slideTitle }}</h3>
        <ul class="slide-body">
          <sc-for list="{{ lightbox.slideBody }}" as="line">
            <li>{{ line }}</li>
          </sc-for>
        </ul>
        <p class="mono slide-foot">{{ lightbox.slideFoot }}</p>
      </article>
      </sc-if>
      <button class="lb-nav lb-prev" onClick="{{ lightboxPrevHandler }}" aria-label="Previous slide">‹</button>
      <button class="lb-nav lb-next" onClick="{{ lightboxNextHandler }}" aria-label="Next slide">›</button>
    </div>
    <p class="mono" style="font-size:10px;letter-spacing:.14em;color:rgba(242,242,243,.6);margin:14px 0 0">SLIDE {{ lightbox.position }} / {{ lightbox.total }}</p>
  </div>
  </sc-if>

  <sc-if value="{{ hasDoc }}">
  <div data-r="modalwrap" style="position:fixed;inset:0;z-index:320;background:rgba(29,31,32,.72);display:flex;align-items:center;justify-content:center;padding:40px" onClick="{{ closeDoc }}">
    <div class="blueprint doc-panel" onClick="{{ stop }}">
      <i class="corner tl"></i><i class="corner tr"></i><i class="corner bl"></i><i class="corner br"></i>
      <div class="doc-head">
        <p class="mono doc-kicker">{{ doc.kicker }}</p>
        <button class="mono btn-close" onClick="{{ closeDoc }}">CLOSE ✕</button>
      </div>
      <h2 class="doc-title">{{ doc.title }}</h2>
      <p class="mono doc-sub">{{ doc.subtitle }}</p>
      <sc-for list="{{ doc.sections }}" as="sec">
        <section class="doc-section">
          <sc-if value="{{ sec.heading }}">
          <h3>{{ sec.heading }}</h3>
          </sc-if>
          <sc-for list="{{ sec.paragraphs }}" as="para">
            <p>{{ para }}</p>
          </sc-for>
        </section>
      </sc-for>
    </div>
  </div>
  </sc-if>
'''
markup = markup.replace(OLD_LIGHTBOX, NEW_LIGHTBOX, 1)

# ----------------------------------------------------------------- logic ---
# Slide arrays pointed at 120 PNGs that were never delivered; slides now come
# from the extracted decks in js/decks.js.
before = len(re.findall(r"slides: \[R\(", logic))
logic = re.sub(r" slides: \[R\([^\]]*\],", "", logic)
if before != 12 or "slides: [R(" in logic:
    fail.append(f"slide arrays: stripped {before} (expected 12)")

logic = sub_once(logic, """  openLightbox(project) {
    if (!project || !project.slides || !project.slides.length) return;
    this.setState({ lightbox: { title: project.title, images: project.slides, index: 0 } });
  }""", """  openLightbox(project) {
    const deck = DECKS[project.id];
    if (!deck || !deck.slides || !deck.slides.length) return;
    this.setState({ lightbox: { projectId: project.id, title: project.title, index: 0 } });
  }

  openDoc(project) {
    const doc = METHODOLOGIES[project.id];
    if (!doc) return;
    this.setState({ doc: { projectId: project.id } });
  }

  closeDoc() { this.setState({ doc: null }); }""", "openLightbox")

logic = sub_once(logic,
    "      hasLinks: !!(proj && proj.slides && proj.slides.length),\n"
    "      links: proj && proj.slides && proj.slides.length ? [{ label: \"View slideshow\", onClick: () => this.openLightbox(proj) }] : []",
    "      hasLinks: !!(proj && projectLinks(proj).length),\n"
    "      links: proj ? projectLinks(proj).map((l) => ({ label: l.label, onClick: () => l.kind === \"doc\" ? this.openDoc(proj) : this.openLightbox(proj) })) : []",
    "student links")

logic = sub_once(logic,
    "      hasLinks: !!(p.slides && p.slides.length),\n"
    "      links: p.slides && p.slides.length ? [{ label: \"View slideshow\", onClick: () => this.openLightbox(p) }] : []",
    "      hasLinks: !!projectLinks(p).length,\n"
    "      links: projectLinks(p).map((l) => ({ label: l.label, onClick: () => l.kind === \"doc\" ? this.openDoc(p) : this.openLightbox(p) }))",
    "project links")

logic = sub_once(logic, """      hasLightbox: !!this.state.lightbox,
      lightbox: this.state.lightbox ? {
        title: this.state.lightbox.title,
        currentImage: this.state.lightbox.images[this.state.lightbox.index],
        position: this.state.lightbox.index + 1,
        total: this.state.lightbox.images.length
      } : { title: "", currentImage: "", position: 1, total: 1 },""",
"""      hasLightbox: !!this.state.lightbox,
      lightbox: this.lightboxVals(),
      hasDoc: !!this.state.doc,
      doc: this.docVals(),
      closeDoc: () => this.closeDoc(),""", "lightbox vals")

# The lightbox now indexes a deck rather than an images array.
logic = sub_once(logic,
    "  lightboxNext() { this.setState((s) => s.lightbox ? { lightbox: { ...s.lightbox, index: (s.lightbox.index + 1) % s.lightbox.images.length } } : s); }\n"
    "  lightboxPrev() { this.setState((s) => s.lightbox ? { lightbox: { ...s.lightbox, index: (s.lightbox.index - 1 + s.lightbox.images.length) % s.lightbox.images.length } } : s); }",
    "  lightboxStep(delta) {\n"
    "    this.setState((s) => {\n"
    "      if (!s.lightbox) return s;\n"
    "      const total = deckSlides(s.lightbox.projectId).length || 1;\n"
    "      return { lightbox: { ...s.lightbox, index: (s.lightbox.index + delta + total) % total } };\n"
    "    });\n"
    "  }\n"
    "  lightboxNext() { this.lightboxStep(1); }\n"
    "  lightboxPrev() { this.lightboxStep(-1); }",
    "lightbox step")

logic = sub_once(logic, '  state = { tab: "home", modal: null, filter: "All", lightbox: null };',
                 '  state = { tab: "home", modal: null, filter: "All", lightbox: null, doc: null };', "state")

PRELUDE = '''/*
 * PAIRS site logic — generated by tools/build-site.py from
 * design/PAIRS_Site.dc.html. Edit the design file (or this script), not this
 * file: a rebuild overwrites it.
 *
 * Content (mentors, students, projects, awards) is the design file's own data,
 * kept verbatim. Slide decks and methodology write-ups live in js/decks.js,
 * built from content/ by tools/build-content.py.
 */
const DECKS = (window.PAIRS_DECKS || {});
const METHODOLOGIES = (window.PAIRS_METHODOLOGIES || {});

function deckSlides(projectId) {
  const deck = DECKS[projectId];
  return (deck && deck.slides) || [];
}

// Actions offered in a project's detail panel, in the order they appear.
function projectLinks(project) {
  const links = [];
  if (deckSlides(project.id).length) links.push({ kind: "slides", label: "View slideshow" });
  if (METHODOLOGIES[project.id]) links.push({ kind: "doc", label: "Read methodology" });
  return links;
}

'''

EPILOGUE = '''
// ---------------------------------------------------------------- viewer ---
Component.prototype.lightboxVals = function () {
  const empty = { title: "", hasText: false, hasImage: false, slideKicker: "", slideTitle: "", slideBody: [], slideClass: "", slideFoot: "", currentImage: "", position: 1, total: 1 };
  if (!this.state.lightbox) return empty;
  const { projectId, title, index } = this.state.lightbox;
  const slides = deckSlides(projectId);
  const slide = slides[index];
  if (!slide) return Object.assign({}, empty, { title });
  const body = (slide.body || []).filter(Boolean);
  return {
    title: title,
    hasImage: !!slide.image,
    hasText: !slide.image,
    currentImage: slide.image || "",
    slideKicker: projectId + " · " + (DECKS[projectId] ? DECKS[projectId].slides.length : 0) + " SLIDES",
    slideTitle: slide.title || title,
    slideBody: body,
    slideClass: body.length ? "" : "slide-cover",
    slideFoot: String(index + 1).padStart(2, "0") + " / " + String(slides.length).padStart(2, "0"),
    position: index + 1,
    total: slides.length
  };
};

Component.prototype.docVals = function () {
  if (!this.state.doc) return { kicker: "", title: "", subtitle: "", sections: [] };
  const doc = METHODOLOGIES[this.state.doc.projectId] || {};
  const project = PROJECTS.find((p) => p.id === this.state.doc.projectId);
  return {
    kicker: "METHODOLOGY · " + this.state.doc.projectId,
    title: doc.title || "Methodology",
    // The source filename is provenance, not a subtitle — name the project.
    subtitle: doc.authors || (project ? project.title : ""),
    sections: doc.sections || []
  };
};

// Keyboard: arrows page the slideshow, Escape closes the topmost overlay.
document.addEventListener("keydown", (e) => {
  const app = window.PAIRS_APP;
  if (!app) return;
  if (e.key === "Escape") {
    if (app.state.doc) return app.closeDoc();
    if (app.state.lightbox) return app.closeLightbox();
    if (app.state.modal) return app.setState({ modal: null });
    return;
  }
  if (!app.state.lightbox) return;
  if (e.key === "ArrowRight") { e.preventDefault(); app.lightboxNext(); }
  if (e.key === "ArrowLeft") { e.preventDefault(); app.lightboxPrev(); }
});

const root = document.getElementById("app");
const template = document.getElementById("app-template");
const app = new Component(root, template);
window.PAIRS_APP = app;

// Background scroll under a full-screen overlay is disorienting on touch.
const baseRender = app.render.bind(app);
app.render = function () {
  baseRender();
  const locked = !!(this.state.modal || this.state.lightbox || this.state.doc);
  document.body.classList.toggle("is-locked", locked);
};
app.mount();
'''

logic = PRELUDE + logic + EPILOGUE

# ------------------------------------------------------------------ write ---
INDEX = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PAIRS — Program for Applied Independent Research in the Summer</title>
<meta name="description" content="PAIRS is a ten-week summer AI/ML research and mentorship program: four mentors, thirty-plus students, and independent projects from fundamentals to final presentation.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500;600&family=Barlow:wght@400;500;600&display=swap">
<link rel="stylesheet" href="css/site.css">
<link rel="stylesheet" href="css/responsive.css">
</head>
<body>
<div id="app"></div>

<template id="app-template">
__MARKUP__
</template>

<script src="js/decks.js"></script>
<script src="js/image-slot.js"></script>
<script src="js/dc-runtime.js"></script>
<script src="js/app.js"></script>
</body>
</html>
'''

if fail:
    print("BUILD FAILED:", file=sys.stderr)
    for f in fail:
        print("  -", f, file=sys.stderr)
    sys.exit(1)

(ROOT / "index.html").write_text(INDEX.replace("__MARKUP__", markup))
(ROOT / "js" / "app.js").write_text(logic)
print(f"wrote index.html ({len(markup)} bytes of markup) and js/app.js ({len(logic)} bytes)")
