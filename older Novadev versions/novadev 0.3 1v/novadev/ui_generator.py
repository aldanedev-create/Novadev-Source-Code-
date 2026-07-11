from __future__ import annotations

"""Static admin-dashboard generator for NovaDev 0.3.

The generator reads registered app, table, page, and component declarations and
writes a small browser app to dist/index.html, dist/style.css, and dist/app.js.
"""

import html
import json
from pathlib import Path
from typing import Any, Dict, List

from .ast_nodes import ComponentNode, Program, TableNode, expression_to_source
from .runtime import Runtime


class UIGenerator:
    def generate(self, program: Program, output_dir: Path | str = "dist") -> List[Path]:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        runtime = Runtime()
        runtime.load_declarations(program)
        app_name = next(iter(runtime.apps.keys()), "NovaDevApp")

        files = {
            output_path / "index.html": self.html(app_name, runtime),
            output_path / "style.css": self.css(runtime),
            output_path / "app.js": self.javascript(app_name, runtime),
        }
        for path, content in files.items():
            path.write_text(content, encoding="utf-8")
        return list(files.keys())

    def html(self, app_name: str, runtime: Runtime) -> str:
        pages = runtime.pages
        first_title = pages[0].display_title() if pages else app_name
        nav = "\n".join(
            f'<a class="nav-link" href="#{escape(page.route_path)}">{escape(page.display_title())}</a>'
            for page in pages
        )
        page_html = "\n".join(self.page_html(page) for page in pages)
        roles = ["Admin", "Editor", "User"]
        for page in pages:
            if page.required_role and page.required_role not in roles:
                roles.insert(0, page.required_role)
        role_options = "\n".join(f'<option value="{escape(role)}">{escape(role)}</option>' for role in roles)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(first_title)}</title>
    <link rel="stylesheet" href="style.css">
    <script defer src="app.js"></script>
</head>
<body>
    <div class="app-shell">
        <aside class="sidebar">
            <div class="brand">
                <span class="brand-mark">N</span>
                <div>
                    <strong>{escape(app_name)}</strong>
                    <small>NovaDev 0.3</small>
                </div>
            </div>
            <nav class="nav-list">{nav}</nav>
        </aside>
        <main class="workspace">
            <header class="topbar">
                <div>
                    <p class="eyebrow">Generated admin workspace</p>
                    <h1 id="pageTitle">{escape(first_title)}</h1>
                </div>
                <div class="toolbar">
                    <label for="roleSelect">Role</label>
                    <select id="roleSelect">{role_options}</select>
                    <button id="themeToggle" type="button">Theme</button>
                </div>
            </header>
            <section class="access-warning" id="accessWarning">
                <strong>Access restricted.</strong>
                <span>This page requires <span id="requiredRole"></span>.</span>
            </section>
            {page_html}
        </main>
    </div>
</body>
</html>
"""

    def page_html(self, page) -> str:
        body = "\n".join(self.component_html(component) for component in page.components)
        if not body:
            body = '<section class="empty-state">No components declared for this page yet.</section>'
        role = f' data-required-role="{escape(page.required_role)}"' if page.required_role else ""
        return f"""<section class="page" data-route="{escape(page.route_path)}" data-title="{escape(page.display_title())}"{role}>
{body}
</section>"""

    def component_html(self, component: ComponentNode) -> str:
        if component.kind in {"sidebar", "navbar"}:
            links = "\n".join(
                f'<a href="#{escape(child.props.get("target", "#"))}">{escape(child.name)}</a>'
                for child in component.children
            )
            return f'<nav class="inline-links">{links}</nav>'
        if component.kind == "card":
            value = expression_to_source(component.props.get("value")) if component.props.get("value") is not None else ""
            return f"""<article class="metric-card">
    <span>{escape(component.name)}</span>
    <strong data-bind="{escape(value)}">{escape(value or "Ready")}</strong>
</article>"""
        if component.kind == "table":
            columns = ",".join(component.props.get("columns", []))
            actions = ",".join(component.props.get("actions", []))
            return f"""<section class="panel">
    <div class="panel-heading"><h2>{escape(component.name)}</h2><span>Table</span></div>
    <div class="table-scroll">
        <table data-table="{escape(component.name)}" data-columns="{escape(columns)}" data-actions="{escape(actions)}">
            <thead></thead>
            <tbody></tbody>
        </table>
    </div>
</section>"""
        if component.kind == "form":
            fields = ",".join(component.props.get("fields", []))
            submit = component.props.get("submit", "Save")
            return f"""<form class="panel data-form" data-form="{escape(component.name)}" data-fields="{escape(fields)}">
    <div class="panel-heading"><h2>{escape(component.name)} Form</h2><span>Input</span></div>
    <div class="form-grid" data-form-fields></div>
    <div class="form-actions"><button type="submit">{escape(submit)}</button></div>
</form>"""
        if component.kind == "chart":
            return f"""<section class="panel">
    <div class="panel-heading"><h2>{escape(component.name)} Chart</h2><span>{escape(component.props.get("type", "line"))}</span></div>
    <canvas data-chart="{escape(component.name)}" data-chart-type="{escape(component.props.get("type", "line"))}" data-x="{escape(component.props.get("x", ""))}" data-y="{escape(component.props.get("y", ""))}"></canvas>
</section>"""
        if component.kind == "modal":
            modal_id = "modal-" + "".join(char.lower() if char.isalnum() else "-" for char in component.name).strip("-")
            return f"""<button class="primary-button" data-open-modal="{escape(modal_id)}" type="button">{escape(component.name)}</button>
<dialog id="{escape(modal_id)}">
    <div class="modal-panel">
        <h2>{escape(component.name)}</h2>
        <p>{escape(component.props.get("text", ""))}</p>
        <button data-close-modal type="button">{escape(component.props.get("button", "Close"))}</button>
    </div>
</dialog>"""
        if component.kind == "button":
            target = component.props.get("to")
            attr = f' data-target="{escape(target)}"' if target else ""
            return f'<button class="primary-button" type="button"{attr}>{escape(component.name)}</button>'
        return ""

    def css(self, runtime: Runtime) -> str:
        theme = self.theme(runtime)
        return f""":root {{
    --bg: {theme["background"]};
    --panel: {theme["panel"]};
    --panel-alt: {theme["panel_alt"]};
    --text: {theme["text"]};
    --muted: {theme["muted"]};
    --border: {theme["border"]};
    --accent: {theme["accent"]};
    --accent-alt: {theme["accent_alt"]};
    --danger: {theme["danger"]};
}}

body.light {{
    --bg: #f6f7f9;
    --panel: #ffffff;
    --panel-alt: #eef1f4;
    --text: #14161a;
    --muted: #667085;
    --border: #d9dee7;
}}

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    min-height: 100vh;
    background: var(--bg);
    color: var(--text);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    letter-spacing: 0;
}}

button,
input,
select {{
    font: inherit;
}}

button {{
    cursor: pointer;
}}

.app-shell {{
    display: grid;
    grid-template-columns: 260px minmax(0, 1fr);
    min-height: 100vh;
}}

.sidebar {{
    background: var(--panel);
    border-right: 1px solid var(--border);
    padding: 18px;
}}

.brand {{
    display: grid;
    grid-template-columns: 42px 1fr;
    gap: 10px;
    align-items: center;
    margin-bottom: 22px;
}}

.brand-mark {{
    width: 42px;
    height: 42px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    background: var(--accent);
    color: #061014;
    font-weight: 800;
}}

.brand strong,
.brand small {{
    display: block;
    overflow-wrap: anywhere;
}}

.brand small,
.eyebrow,
.panel-heading span,
.metric-card span,
.toolbar label {{
    color: var(--muted);
    font-size: 13px;
}}

.nav-list,
.inline-links {{
    display: grid;
    gap: 8px;
}}

.nav-link,
.inline-links a {{
    min-height: 38px;
    display: flex;
    align-items: center;
    padding: 8px 10px;
    border-radius: 8px;
    color: var(--text);
    text-decoration: none;
    border: 1px solid transparent;
    overflow-wrap: anywhere;
}}

.nav-link.active,
.nav-link:hover,
.inline-links a:hover {{
    background: var(--panel-alt);
    border-color: var(--border);
}}

.workspace {{
    min-width: 0;
    padding: 20px;
}}

.topbar {{
    max-width: 1180px;
    margin: 0 auto 16px;
    display: flex;
    justify-content: space-between;
    gap: 14px;
    align-items: center;
}}

.topbar h1 {{
    margin: 2px 0 0;
    font-size: 28px;
    line-height: 1.2;
    overflow-wrap: anywhere;
}}

.eyebrow {{
    margin: 0;
    text-transform: uppercase;
    font-weight: 700;
}}

.toolbar {{
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-wrap: wrap;
    gap: 8px;
}}

.toolbar select,
.toolbar button,
.primary-button,
.data-form button,
.modal-panel button {{
    min-height: 38px;
    border-radius: 8px;
    border: 1px solid var(--border);
    padding: 8px 11px;
    color: var(--text);
    background: var(--panel-alt);
}}

.primary-button,
.data-form button {{
    color: #061014;
    background: var(--accent);
    border-color: var(--accent);
    font-weight: 700;
}}

.page {{
    display: none;
    max-width: 1180px;
    margin: 0 auto;
}}

.page.active {{
    display: grid;
    gap: 14px;
}}

.metric-card,
.panel,
.empty-state,
.access-warning {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
}}

.metric-card {{
    min-height: 124px;
    padding: 18px;
    display: grid;
    align-content: space-between;
}}

.metric-card strong {{
    font-size: 30px;
    line-height: 1.1;
    overflow-wrap: anywhere;
}}

.panel {{
    overflow: hidden;
}}

.panel-heading {{
    display: flex;
    justify-content: space-between;
    gap: 12px;
    align-items: center;
    border-bottom: 1px solid var(--border);
    padding: 14px 16px;
}}

.panel-heading h2 {{
    margin: 0;
    font-size: 18px;
}}

.table-scroll {{
    overflow-x: auto;
}}

table {{
    width: 100%;
    min-width: 620px;
    border-collapse: collapse;
}}

th,
td {{
    padding: 12px 14px;
    border-bottom: 1px solid var(--border);
    text-align: left;
    overflow-wrap: anywhere;
}}

th {{
    color: var(--muted);
    font-size: 13px;
}}

.row-actions {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}

.row-actions button {{
    min-height: 32px;
    border-radius: 8px;
    border: 1px solid var(--border);
    background: var(--panel-alt);
    color: var(--text);
}}

.form-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    padding: 16px;
}}

.form-field {{
    display: grid;
    gap: 6px;
}}

.form-field label {{
    color: var(--muted);
    font-size: 13px;
}}

.form-field input {{
    min-height: 40px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: var(--bg);
    color: var(--text);
    padding: 8px 10px;
    width: 100%;
}}

.form-actions {{
    padding: 0 16px 16px;
    display: flex;
    justify-content: flex-end;
}}

canvas {{
    width: 100%;
    height: 260px;
    display: block;
    padding: 12px;
}}

.access-warning {{
    display: none;
    max-width: 1180px;
    margin: 0 auto 14px;
    padding: 14px;
    color: var(--danger);
}}

.access-warning.active {{
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}}

.empty-state {{
    padding: 18px;
    color: var(--muted);
}}

dialog {{
    border: 0;
    padding: 0;
    background: transparent;
    color: var(--text);
}}

dialog::backdrop {{
    background: rgba(0, 0, 0, 0.55);
}}

.modal-panel {{
    width: min(520px, calc(100vw - 32px));
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 18px;
}}

@media (max-width: 860px) {{
    .app-shell {{
        grid-template-columns: 1fr;
    }}

    .sidebar {{
        border-right: 0;
        border-bottom: 1px solid var(--border);
    }}

    .nav-list {{
        grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    }}

    .topbar {{
        align-items: flex-start;
        flex-direction: column;
    }}

    .toolbar {{
        justify-content: flex-start;
    }}
}}
"""

    def javascript(self, app_name: str, runtime: Runtime) -> str:
        payload = {
            "name": app_name,
            "tables": {name: self.table_data(table) for name, table in runtime.tables.items()},
            "pages": [
                {"title": page.display_title(), "path": page.route_path, "role": page.required_role}
                for page in runtime.pages
            ],
            "data": {name: self.sample_rows(table) for name, table in runtime.tables.items()},
        }
        return "const NOVA_APP = " + json.dumps(payload, indent=2) + ";\n" + JS_RUNTIME

    def table_data(self, table: TableNode) -> Dict[str, Any]:
        return {
            "fields": [
                {"name": field.name, "type": field.field_type, "auto": field.auto, "secure": field.secure, "unique": field.unique}
                for field in table.fields
            ]
        }

    def sample_rows(self, table: TableNode) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for index in range(1, 4):
            row: Dict[str, Any] = {}
            for field in table.fields:
                row[field.name] = self.sample_value(field, index)
            rows.append(row)
        return rows

    def sample_value(self, field, index: int) -> Any:
        kind = field.field_type.lower()
        if field.auto:
            return index
        if kind in {"int", "number", "money", "currency"}:
            return index * 25
        if kind in {"bool", "boolean"}:
            return index % 2 == 1
        if kind in {"email"}:
            return f"{field.name}{index}@example.com"
        return f"{field.name.title()} {index}"

    def theme(self, runtime: Runtime) -> Dict[str, str]:
        base = {
            "background": "#101114",
            "panel": "#181b20",
            "panel_alt": "#22262d",
            "text": "#f4f6f8",
            "muted": "#9aa4b2",
            "border": "#303640",
            "accent": "#45d6b5",
            "accent_alt": "#f4b860",
            "danger": "#ff6b6b",
        }
        theme = runtime.themes.get(runtime.active_theme or "")
        if theme:
            for key, value in theme.values.items():
                base[key] = str(value)
        return base


JS_RUNTIME = r'''
const state = {
  role: localStorage.getItem("nova-role") || "Admin",
  light: localStorage.getItem("nova-light") === "true"
};

const $ = (selector, parent = document) => parent.querySelector(selector);
const $$ = (selector, parent = document) => Array.from(parent.querySelectorAll(selector));

function fieldsFor(tableName) {
  return NOVA_APP.tables[tableName]?.fields || [];
}

function visibleFields(tableName) {
  return fieldsFor(tableName).filter((field) => !field.auto && !field.secure);
}

function selectedColumns(tableName, raw) {
  const selected = raw ? raw.split(",").filter(Boolean) : [];
  return selected.length ? selected : visibleFields(tableName).map((field) => field.name);
}

function formatValue(value) {
  if (value === true) return "Yes";
  if (value === false) return "No";
  if (value == null) return "";
  return String(value);
}

function bindExpression(expression) {
  const count = expression.match(/^([A-Za-z_][A-Za-z0-9_]*)\.count\(\)$/);
  if (count) return String((NOVA_APP.data[count[1]] || []).length);
  const sum = expression.match(/^([A-Za-z_][A-Za-z0-9_]*)\.sum\(([A-Za-z_][A-Za-z0-9_]*)\)$/);
  if (sum) {
    const total = (NOVA_APP.data[sum[1]] || []).reduce((acc, row) => acc + Number(row[sum[2]] || 0), 0);
    return new Intl.NumberFormat().format(total);
  }
  return expression || "Ready";
}

function renderBindings() {
  $$("[data-bind]").forEach((node) => {
    node.textContent = bindExpression(node.dataset.bind || "");
  });
}

function renderTables() {
  $$("table[data-table]").forEach((table) => {
    const tableName = table.dataset.table;
    const columns = selectedColumns(tableName, table.dataset.columns);
    const actions = table.dataset.actions ? table.dataset.actions.split(",").filter(Boolean) : [];
    const rows = NOVA_APP.data[tableName] || [];
    const head = $("thead", table);
    const body = $("tbody", table);
    head.innerHTML = `<tr>${columns.map((column) => `<th>${column}</th>`).join("")}${actions.length ? "<th>Actions</th>" : ""}</tr>`;
    body.replaceChildren();
    rows.forEach((row, index) => {
      const tr = document.createElement("tr");
      columns.forEach((column) => {
        const td = document.createElement("td");
        td.textContent = formatValue(row[column]);
        tr.appendChild(td);
      });
      if (actions.length) {
        const td = document.createElement("td");
        const wrap = document.createElement("div");
        wrap.className = "row-actions";
        actions.forEach((action) => {
          const button = document.createElement("button");
          button.type = "button";
          button.textContent = action;
          button.dataset.action = action;
          button.dataset.table = tableName;
          button.dataset.index = String(index);
          wrap.appendChild(button);
        });
        td.appendChild(wrap);
        tr.appendChild(td);
      }
      body.appendChild(tr);
    });
  });
}

function setupForms() {
  $$("form[data-form]").forEach((form) => {
    const tableName = form.dataset.form;
    const selected = form.dataset.fields ? form.dataset.fields.split(",").filter(Boolean) : [];
    const fields = selected.length
      ? visibleFields(tableName).filter((field) => selected.includes(field.name))
      : visibleFields(tableName);
    const container = $("[data-form-fields]", form);
    container.replaceChildren();
    fields.forEach((field) => {
      const wrapper = document.createElement("label");
      wrapper.className = "form-field";
      wrapper.innerHTML = `<span>${field.name}</span><input name="${field.name}" type="${inputType(field.type)}">`;
      container.appendChild(wrapper);
    });
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const rows = NOVA_APP.data[tableName] || [];
      const row = {};
      fieldsFor(tableName).forEach((field) => {
        if (field.auto) {
          row[field.name] = rows.length + 1;
          return;
        }
        const input = form.elements[field.name];
        if (!input) return;
        row[field.name] = numericType(field.type) ? Number(input.value || 0) : input.value;
      });
      rows.push(row);
      NOVA_APP.data[tableName] = rows;
      form.reset();
      renderAll();
    });
  });
}

function inputType(type) {
  const lowered = String(type).toLowerCase();
  if (["int", "number", "money", "currency"].includes(lowered)) return "number";
  if (lowered === "email") return "email";
  if (["password", "secure"].includes(lowered)) return "password";
  return "text";
}

function numericType(type) {
  return ["int", "number", "money", "currency"].includes(String(type).toLowerCase());
}

function handleActions(event) {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const rows = NOVA_APP.data[button.dataset.table] || [];
  const index = Number(button.dataset.index);
  if (button.dataset.action === "delete") {
    rows.splice(index, 1);
    renderAll();
    return;
  }
  alert(JSON.stringify(rows[index], null, 2));
}

function drawCharts() {
  $$("canvas[data-chart]").forEach((canvas) => {
    const rows = NOVA_APP.data[canvas.dataset.chart] || [];
    const yField = canvas.dataset.y || "";
    const rect = canvas.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, rect.width, rect.height);
    const values = rows.map((row, index) => Number(row[yField] ?? row.price ?? row.total ?? index + 1));
    const max = Math.max(...values, 1);
    const pad = 32;
    const width = rect.width - pad * 2;
    const height = rect.height - pad * 2;
    ctx.strokeStyle = getComputedStyle(document.body).getPropertyValue("--border");
    ctx.beginPath();
    ctx.moveTo(pad, pad);
    ctx.lineTo(pad, pad + height);
    ctx.lineTo(pad + width, pad + height);
    ctx.stroke();
    values.forEach((value, index) => {
      const x = pad + (index + 0.25) * (width / Math.max(values.length, 1));
      const barWidth = Math.max(18, width / Math.max(values.length * 2, 1));
      const barHeight = (value / max) * height;
      ctx.fillStyle = index % 2 ? getCss("--accent-alt") : getCss("--accent");
      ctx.fillRect(x, pad + height - barHeight, barWidth, barHeight);
    });
  });
}

function getCss(name) {
  return getComputedStyle(document.body).getPropertyValue(name).trim();
}

function setupModals() {
  $$("[data-open-modal]").forEach((button) => {
    button.addEventListener("click", () => document.getElementById(button.dataset.openModal)?.showModal());
  });
  $$("[data-close-modal]").forEach((button) => {
    button.addEventListener("click", () => button.closest("dialog")?.close());
  });
}

function routeFromHash() {
  const path = location.hash.replace(/^#/, "") || NOVA_APP.pages[0]?.path || "/";
  return NOVA_APP.pages.find((page) => page.path === path) || NOVA_APP.pages[0];
}

function activateRoute() {
  const route = routeFromHash();
  if (!route) return;
  const allowed = !route.role || route.role === state.role;
  $("#pageTitle").textContent = route.title;
  $$(".nav-link").forEach((link) => link.classList.toggle("active", link.getAttribute("href") === `#${route.path}`));
  $$(".page").forEach((page) => page.classList.toggle("active", allowed && page.dataset.route === route.path));
  $("#accessWarning").classList.toggle("active", !allowed);
  $("#requiredRole").textContent = route.role || "";
  requestAnimationFrame(renderAll);
}

function setupRoleAndTheme() {
  const role = $("#roleSelect");
  role.value = state.role;
  role.addEventListener("change", () => {
    state.role = role.value;
    localStorage.setItem("nova-role", state.role);
    activateRoute();
  });
  document.body.classList.toggle("light", state.light);
  $("#themeToggle").addEventListener("click", () => {
    state.light = !state.light;
    localStorage.setItem("nova-light", String(state.light));
    document.body.classList.toggle("light", state.light);
    drawCharts();
  });
}

function renderAll() {
  renderBindings();
  renderTables();
  drawCharts();
}

document.addEventListener("DOMContentLoaded", () => {
  setupForms();
  setupModals();
  setupRoleAndTheme();
  document.addEventListener("click", handleActions);
  window.addEventListener("hashchange", activateRoute);
  window.addEventListener("resize", drawCharts);
  if (!location.hash && NOVA_APP.pages[0]) location.hash = NOVA_APP.pages[0].path;
  activateRoute();
});
'''


def escape(value: Any) -> str:
    return html.escape(str(value), quote=True)
