/*
 * Minimal template runtime for the PAIRS site.
 *
 * The site's markup comes from a design-canvas prototype that used a
 * proprietary editor runtime (<sc-if>, <sc-for>, "{{ expr }}" bindings and a
 * DCLogic base class). That runtime is not shippable, so this file implements
 * the same, much smaller contract against plain DOM:
 *
 *   <sc-if value="{{ expr }}">      render children when expr is truthy
 *   <sc-for list="{{ expr }}" as="x">  render children once per item, x in scope
 *   {{ expr }}                      interpolate in text nodes and attributes
 *   onClick="{{ handler }}"         bind a click listener (never an inline handler)
 *
 * Expressions are deliberately limited to what the markup actually uses:
 * literals and dotted property paths. Anything else resolves to undefined
 * rather than being eval'd, so template text can never become executable code.
 */
(function () {
  const BINDING = /\{\{\s*([^}]*?)\s*\}\}/g;
  const ONLY_BINDING = /^\{\{\s*([^}]*?)\s*\}\}$/;

  // Resolve "a.b.c", "true", "false", "42", "'text'" against a scope object.
  function resolve(expr, scope) {
    expr = String(expr).trim();
    if (expr === '') return undefined;
    if (expr === 'true') return true;
    if (expr === 'false') return false;
    if (expr === 'null') return null;
    if (/^-?\d+(\.\d+)?$/.test(expr)) return Number(expr);
    const quoted = /^'([^']*)'$/.exec(expr) || /^"([^"]*)"$/.exec(expr);
    if (quoted) return quoted[1];
    if (!/^[A-Za-z_$][\w$]*(\.[A-Za-z_$][\w$]*)*$/.test(expr)) return undefined;
    let value = scope;
    for (const part of expr.split('.')) {
      if (value === null || value === undefined) return undefined;
      value = value[part];
    }
    return value;
  }

  // Whole-attribute binding keeps the raw value (functions, booleans);
  // an embedded one stringifies, so "1px solid {{ f.border }}" still works.
  function interpolate(text, scope) {
    const whole = ONLY_BINDING.exec(text);
    if (whole) return resolve(whole[1], scope);
    return text.replace(BINDING, (_, expr) => {
      const value = resolve(expr, scope);
      return value === undefined || value === null ? '' : String(value);
    });
  }

  function renderChildren(source, scope, out) {
    for (const child of Array.from(source.childNodes)) renderNode(child, scope, out);
  }

  function renderNode(node, scope, out) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.nodeValue;
      if (!BINDING.test(text)) {
        out.appendChild(node.cloneNode(false));
        return;
      }
      BINDING.lastIndex = 0;
      const value = interpolate(text, scope);
      out.appendChild(document.createTextNode(value === undefined || value === null ? '' : String(value)));
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return;

    const tag = node.tagName.toLowerCase();

    if (tag === 'sc-if') {
      if (resolve(stripBinding(node.getAttribute('value')), scope)) renderChildren(node, scope, out);
      return;
    }

    if (tag === 'sc-for') {
      const list = resolve(stripBinding(node.getAttribute('list')), scope);
      const name = node.getAttribute('as') || 'item';
      if (!Array.isArray(list)) return;
      list.forEach((item, index) => {
        const inner = Object.create(scope);
        inner[name] = item;
        inner[name + 'Index'] = index;
        renderChildren(node, inner, out);
      });
      return;
    }

    const el = document.createElement(tag);
    for (const attr of Array.from(node.attributes)) {
      const name = attr.name;
      // The HTML parser lowercases attribute names, so onClick arrives as
      // onclick. Bind it as a listener — never as an inline handler string.
      if (name.startsWith('on')) {
        const handler = interpolate(attr.value, scope);
        if (typeof handler === 'function') el.addEventListener(name.slice(2), handler);
        continue;
      }
      if (name.startsWith('hint-placeholder')) continue;
      const value = interpolate(attr.value, scope);
      if (value === undefined || value === null || value === false) continue;
      el.setAttribute(name, String(value));
    }
    renderChildren(node, scope, el);
    out.appendChild(el);
  }

  function stripBinding(raw) {
    if (!raw) return '';
    const whole = ONLY_BINDING.exec(raw.trim());
    return whole ? whole[1] : raw;
  }

  class DCLogic {
    constructor(root, template) {
      this.root = root;
      this.template = template;
      this.state = {};
      this._queued = false;
    }

    setState(update) {
      const next = typeof update === 'function' ? update(this.state) : update;
      this.state = Object.assign({}, this.state, next);
      this.scheduleRender();
    }

    scheduleRender() {
      if (this._queued) return;
      this._queued = true;
      window.requestAnimationFrame(() => {
        this._queued = false;
        this.render();
      });
    }

    render() {
      const scope = this.renderVals();
      const fragment = document.createDocumentFragment();
      renderChildren(this.template.content, scope, fragment);
      this.root.replaceChildren(fragment);
    }

    mount() {
      this.render();
      return this;
    }
  }

  window.DCLogic = DCLogic;
})();
