/*
 * <image-slot> — read-only image frame.
 *
 * The design prototype used an editor-only custom element with drag-and-drop,
 * reframing and a JSON sidecar. None of that belongs on a public site, so this
 * is the shipping equivalent: it fills its container, honours the same
 * attributes the markup already sets (shape / fit / src / placeholder), and
 * degrades to a blueprint placeholder when an image is missing or fails to
 * load — which is what keeps the page intact while a photo is still missing.
 *
 * Attributes: src, fit ("cover" | "contain"), shape ("rect" | "rounded" |
 * "circle" | "pill"), radius, placeholder, alt.
 * Exposes part="frame" and part="image" for outside styling.
 */
(function () {
  const STYLE = `
    :host{display:block;position:relative;width:100%;height:100%}
    .frame{position:absolute;inset:0;overflow:hidden;background:rgba(127,127,127,.08)}
    img{width:100%;height:100%;display:block;object-fit:cover}
    :host([fit="contain"]) img{object-fit:contain}
    .empty{position:absolute;inset:0;display:none;flex-direction:column;align-items:center;
      justify-content:center;gap:8px;text-align:center;padding:12px;box-sizing:border-box;
      color:#7a7a7d;font:11px/1.4 ui-monospace,"SF Mono",Menlo,monospace;
      letter-spacing:.14em;text-transform:uppercase}
    .empty svg{opacity:.5}
    :host([data-empty]) .empty{display:flex}
    :host([data-empty]) img{display:none}
    .ring{position:absolute;inset:0;pointer-events:none;border:1px dashed rgba(29,31,32,.22);display:none}
    :host([data-empty]) .ring{display:block}
  `;

  const ICON = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">' +
    '<rect x="3" y="3" width="18" height="18"/><circle cx="8.5" cy="8.5" r="1.5"/>' +
    '<path d="m21 15-5-5L5 21"/></svg>';

  class ImageSlot extends HTMLElement {
    static get observedAttributes() { return ['src', 'shape', 'radius', 'placeholder', 'alt']; }

    constructor() {
      super();
      const root = this.shadowRoot || this.attachShadow({ mode: 'open' });
      root.innerHTML =
        '<style>' + STYLE + '</style>' +
        '<div class="frame" part="frame">' +
        '  <img part="image" alt="" draggable="false">' +
        '  <div class="empty" part="empty">' + ICON + '<span class="label"></span></div>' +
        '  <div class="ring"></div>' +
        '</div>';
      this._frame = root.querySelector('.frame');
      this._img = root.querySelector('img');
      this._label = root.querySelector('.label');
      // A missing file is the expected case for assets that have not landed
      // yet — fall back to the placeholder instead of a broken-image icon.
      this._img.addEventListener('error', () => this.setAttribute('data-empty', ''));
      this._img.addEventListener('load', () => this.removeAttribute('data-empty'));
    }

    connectedCallback() { this._render(); }
    attributeChangedCallback() { if (this.shadowRoot) this._render(); }

    _render() {
      const shape = (this.getAttribute('shape') || 'rounded').toLowerCase();
      let radius = '';
      if (shape === 'circle') radius = '50%';
      else if (shape === 'pill') radius = '9999px';
      else if (shape === 'rounded') {
        const n = parseFloat(this.getAttribute('radius'));
        radius = (Number.isFinite(n) ? n : 12) + 'px';
      }
      this._frame.style.borderRadius = radius;

      // "Drop photo" and friends are editor prompts; on the live site the
      // placeholder should read as a caption, not an instruction.
      const hint = (this.getAttribute('placeholder') || 'Image').replace(/^drop\s+/i, '');
      this._label.textContent = hint;

      const src = this.getAttribute('src') || '';
      if (src) {
        if (this._img.getAttribute('src') !== src) this._img.setAttribute('src', src);
        this._img.alt = this.getAttribute('alt') || hint;
        if (this._img.complete && this._img.naturalWidth === 0) this.setAttribute('data-empty', '');
      } else {
        this._img.removeAttribute('src');
        this.setAttribute('data-empty', '');
      }
    }
  }

  if (!customElements.get('image-slot')) customElements.define('image-slot', ImageSlot);
})();
