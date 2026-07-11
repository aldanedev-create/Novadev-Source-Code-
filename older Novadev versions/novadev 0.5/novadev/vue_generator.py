from __future__ import annotations

"""Vue 3 + Vite frontend generator for NovaDev 0.5."""

import json
import re
from pathlib import Path
from typing import Any, Dict, List

from .ast_nodes import ComponentNode, PageNode, Program, TableNode, expression_to_source
from .runtime import Runtime


class VueGenerator:
    def generate(self, program: Program, output_dir: Path | str) -> List[Path]:
        output_path = Path(output_dir)
        runtime = Runtime()
        runtime.load_declarations(program)
        app_name = next(iter(runtime.apps.keys()), "NovaDevApp")

        dirs = [
            output_path / "src" / "router",
            output_path / "src" / "stores",
            output_path / "src" / "services",
            output_path / "src" / "components",
            output_path / "src" / "pages",
            output_path / "src" / "assets",
            output_path / "src" / "layouts",
            output_path / "public",
        ]
        for folder in dirs:
            folder.mkdir(parents=True, exist_ok=True)

        pages = list(runtime.pages)
        if not any(page.name == "Dashboard" for page in pages):
            pages.insert(0, self.dashboard_page(runtime))

        files: Dict[Path, str] = {
            output_path / "package.json": self.package_json(app_name),
            output_path / "vite.config.js": self.vite_config(),
            output_path / "index.html": self.index_html(app_name),
            output_path / "README.md": self.readme(app_name),
            output_path / "src" / "main.js": self.main_js(),
            output_path / "src" / "App.vue": self.app_vue(app_name, pages),
            output_path / "src" / "router" / "index.js": self.router_js(pages),
            output_path / "src" / "stores" / "appStore.js": self.store_js(app_name, runtime, pages),
            output_path / "src" / "services" / "api.js": self.api_js(),
            output_path / "src" / "assets" / "main.css": self.css(),
            output_path / "src" / "components" / "Sidebar.vue": self.sidebar_vue(),
            output_path / "src" / "components" / "Navbar.vue": self.navbar_vue(),
            output_path / "src" / "components" / "DataTable.vue": self.data_table_vue(),
            output_path / "src" / "components" / "FormBuilder.vue": self.form_builder_vue(),
            output_path / "src" / "components" / "StatCard.vue": self.stat_card_vue(),
            output_path / "src" / "components" / "ChartBlock.vue": self.chart_block_vue(),
        }

        for page in pages:
            files[output_path / "src" / "pages" / f"{page.name}.vue"] = self.page_vue(page, runtime)

        for path, content in files.items():
            path.write_text(content, encoding="utf-8")
        return list(files.keys())

    def dashboard_page(self, runtime: Runtime) -> PageNode:
        components = [
            ComponentNode("card", name=f"{name} Records", props={"value": f"{name}.count()"})
            for name in runtime.tables
        ]
        return PageNode(name="Dashboard", title="Dashboard", components=components, body=components)

    def package_json(self, app_name: str) -> str:
        package_name = slug_name(app_name)
        data = {
            "name": package_name,
            "version": "0.5.0",
            "private": True,
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
            },
            "dependencies": {
                "vue": "latest",
                "vue-router": "latest",
                "pinia": "latest",
            },
            "devDependencies": {
                "vite": "latest",
                "@vitejs/plugin-vue": "latest",
            },
        }
        return json.dumps(data, indent=2) + "\n"

    def vite_config(self) -> str:
        return """import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:5000'
    }
  }
})
"""

    def index_html(self, app_name: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape_html(app_name)}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
"""

    def main_js(self) -> str:
        return """import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './assets/main.css'

createApp(App)
  .use(createPinia())
  .use(router)
  .mount('#app')
"""

    def app_vue(self, app_name: str, pages: List[PageNode]) -> str:
        pages_json = json.dumps([{"name": page.name, "title": page.display_title(), "path": page.route_path} for page in pages], indent=2)
        return f"""<script setup>
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'

const pages = {pages_json}
</script>

<template>
  <div class="app-shell">
    <Sidebar app-name="{escape_attr(app_name)}" :pages="pages" />
    <main class="workspace">
      <Navbar app-name="{escape_attr(app_name)}" :pages="pages" />
      <RouterView />
    </main>
  </div>
</template>
"""

    def router_js(self, pages: List[PageNode]) -> str:
        imports = []
        routes = []
        for page in pages:
            imports.append(f"import {page.name} from '../pages/{page.name}.vue'")
            routes.append({"path": page.route_path, "name": page.name, "component": page.name})
        route_lines = ["  { path: '/', redirect: " + json.dumps(pages[0].route_path if pages else "/dashboard") + " }"]
        for route in routes:
            route_lines.append(f"  {{ path: {json.dumps(route['path'])}, name: {json.dumps(route['name'])}, component: {route['component']} }}")
        return "\n".join([
            "import { createRouter, createWebHistory } from 'vue-router'",
            *imports,
            "",
            "const router = createRouter({",
            "  history: createWebHistory(),",
            "  routes: [",
            ",\n".join(route_lines),
            "  ]",
            "})",
            "",
            "export default router",
            "",
        ])

    def store_js(self, app_name: str, runtime: Runtime, pages: List[PageNode]) -> str:
        tables = {
            name: {
                "resource": api_resource_name(name),
                "primaryKey": primary_key(table),
                "fields": [
                    {
                        "name": field.name,
                        "type": field.field_type,
                        "auto": field.auto,
                        "secure": field.secure,
                        "unique": field.unique,
                    }
                    for field in table.fields
                ],
            }
            for name, table in runtime.tables.items()
        }
        pages_data = [{"name": page.name, "title": page.display_title(), "path": page.route_path} for page in pages]
        config = {"name": app_name, "tables": tables, "pages": pages_data}
        return f"""import {{ defineStore }} from 'pinia'
import api from '../services/api'

const config = {json.dumps(config, indent=2)}

export const useAppStore = defineStore('app', {{
  state: () => ({{
    config,
    rows: {{}},
    loading: false,
    error: ''
  }}),
  getters: {{
    tableSchema: (state) => (tableName) => state.config.tables[tableName],
    tableRows: (state) => (tableName) => state.rows[tableName] || []
  }},
  actions: {{
    async loadTable(tableName) {{
      const schema = this.tableSchema(tableName)
      if (!schema) return
      this.loading = true
      this.error = ''
      try {{
        const data = await api.list(schema.resource)
        this.rows[tableName] = data.rows || []
      }} catch (error) {{
        this.error = error.message
      }} finally {{
        this.loading = false
      }}
    }},
    async createRow(tableName, payload) {{
      const schema = this.tableSchema(tableName)
      const row = await api.create(schema.resource, payload)
      await this.loadTable(tableName)
      return row
    }},
    async deleteRow(tableName, row) {{
      const schema = this.tableSchema(tableName)
      const id = row[schema.primaryKey]
      await api.remove(schema.resource, id)
      await this.loadTable(tableName)
    }}
  }}
}})
"""

    def api_js(self) -> str:
        return """const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}/api/${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options
  })
  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.error || `Request failed: ${response.status}`)
  }
  return data
}

export default {
  list(resource) {
    return request(resource)
  },
  create(resource, payload) {
    return request(resource, {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  },
  remove(resource, id) {
    return request(`${resource}/${id}`, { method: 'DELETE' })
  }
}
"""

    def page_vue(self, page: PageNode, runtime: Runtime) -> str:
        components = "\n".join(self.component_vue(component, runtime) for component in page.components)
        load_tables = sorted({component.name for component in page.components if component.kind in {"table", "form", "catalog", "cart", "checkout"} and component.name in runtime.tables})
        on_mounted = "\n".join(f"  store.loadTable({json.dumps(table_name)})" for table_name in load_tables)
        return f"""<script setup>
import {{ computed, onMounted }} from 'vue'
import {{ useAppStore }} from '../stores/appStore'
import DataTable from '../components/DataTable.vue'
import FormBuilder from '../components/FormBuilder.vue'
import StatCard from '../components/StatCard.vue'
import ChartBlock from '../components/ChartBlock.vue'

const store = useAppStore()

function schema(tableName) {{
  return store.tableSchema(tableName)
}}

function rows(tableName) {{
  return computed(() => store.tableRows(tableName))
}}

async function createRow(tableName, payload) {{
  await store.createRow(tableName, payload)
}}

async function deleteRow(tableName, row) {{
  await store.deleteRow(tableName, row)
}}

onMounted(() => {{
{on_mounted or "  // This page does not need initial table data."}
}})
</script>

<template>
  <section class="page">
    <div class="page-heading">
      <p class="eyebrow">NovaDev 0.5 Vue Page</p>
      <h1>{escape_html(page.display_title())}</h1>
    </div>
{components or '    <p class="empty">Add page components in NovaDev to fill this page.</p>'}
  </section>
</template>
"""

    def component_vue(self, component: ComponentNode, runtime: Runtime) -> str:
        if component.kind == "card":
            value = expression_to_source(component.props.get("value")) if component.props.get("value") is not None else ""
            table_name = table_name_from_expression(value)
            if table_name in runtime.tables:
                return f"""    <StatCard title="{escape_attr(component.name)}" :value="rows('{table_name}').value.length" />"""
            return f"""    <StatCard title="{escape_attr(component.name)}" value="{escape_attr(value or 'Ready')}" />"""

        if component.kind in {"table", "catalog", "cart"}:
            columns = component.props.get("columns") or component.props.get("fields") or default_columns(runtime.tables.get(component.name))
            return f"""    <DataTable
      title="{escape_attr(component.name)}"
      table-name="{escape_attr(component.name)}"
      :columns="{vue_expr(columns)}"
      :rows="rows('{component.name}').value"
      :primary-key="schema('{component.name}')?.primaryKey || 'id'"
      @delete="deleteRow('{component.name}', $event)"
    />"""

        if component.kind == "form" or component.kind == "checkout":
            fields = component.props.get("fields") or default_columns(runtime.tables.get(component.name), include_auto=False)
            submit = component.props.get("submit", "Save")
            return f"""    <FormBuilder
      title="{escape_attr(component.name)} Form"
      :fields="{vue_expr(fields)}"
      submit-label="{escape_attr(submit)}"
      @submit="createRow('{component.name}', $event)"
    />"""

        if component.kind == "chart":
            chart_type = component.props.get("type", "bar")
            return f"""    <ChartBlock title="{escape_attr(component.name)} Chart" type="{escape_attr(chart_type)}" />"""

        if component.kind in {"navbar", "sidebar"}:
            return ""

        return f"""    <p class="empty">Unsupported component: {escape_html(component.kind)}</p>"""

    def sidebar_vue(self) -> str:
        return """<script setup>
defineProps({
  appName: { type: String, required: true },
  pages: { type: Array, required: true }
})
</script>

<template>
  <aside class="sidebar">
    <RouterLink class="brand" to="/">
      <span class="brand-mark">N</span>
      <strong>{{ appName }}</strong>
    </RouterLink>
    <nav class="nav-list">
      <RouterLink v-for="page in pages" :key="page.path" :to="page.path" class="nav-link">
        {{ page.title }}
      </RouterLink>
    </nav>
  </aside>
</template>
"""

    def navbar_vue(self) -> str:
        return """<script setup>
defineProps({
  appName: { type: String, required: true },
  pages: { type: Array, required: true }
})
</script>

<template>
  <header class="topbar">
    <strong>{{ appName }}</strong>
    <div class="topbar-actions">
      <span>{{ pages.length }} pages</span>
      <a href="/api/health" target="_blank" rel="noreferrer">API Health</a>
    </div>
  </header>
</template>
"""

    def data_table_vue(self) -> str:
        return """<script setup>
defineProps({
  title: { type: String, default: 'Table' },
  tableName: { type: String, required: true },
  columns: { type: Array, default: () => [] },
  rows: { type: Array, default: () => [] },
  primaryKey: { type: String, default: 'id' }
})

const emit = defineEmits(['delete'])
</script>

<template>
  <section class="panel">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ rows.length }} records</span>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th v-for="column in columns" :key="column">{{ column }}</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row[primaryKey]">
            <td v-for="column in columns" :key="column">{{ row[column] }}</td>
            <td>
              <button class="ghost-button" @click="emit('delete', row)">Delete</button>
            </td>
          </tr>
          <tr v-if="rows.length === 0">
            <td :colspan="columns.length + 1" class="empty">No rows yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
"""

    def form_builder_vue(self) -> str:
        return """<script setup>
import { reactive, watchEffect } from 'vue'

const props = defineProps({
  title: { type: String, default: 'Form' },
  fields: { type: Array, default: () => [] },
  submitLabel: { type: String, default: 'Save' }
})
const emit = defineEmits(['submit'])
const form = reactive({})

watchEffect(() => {
  props.fields.forEach((field) => {
    if (!(field in form)) form[field] = ''
  })
})

function submit() {
  emit('submit', { ...form })
  Object.keys(form).forEach((key) => {
    form[key] = ''
  })
}
</script>

<template>
  <form class="panel form-grid" @submit.prevent="submit">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ fields.length }} fields</span>
    </div>
    <label v-for="field in fields" :key="field">
      <span>{{ field }}</span>
      <input v-model="form[field]" :name="field" />
    </label>
    <button class="primary-button" type="submit">{{ submitLabel }}</button>
  </form>
</template>
"""

    def stat_card_vue(self) -> str:
        return """<script setup>
defineProps({
  title: { type: String, required: true },
  value: { type: [String, Number], default: 'Ready' }
})
</script>

<template>
  <article class="stat-card">
    <span>{{ title }}</span>
    <strong>{{ value }}</strong>
  </article>
</template>
"""

    def chart_block_vue(self) -> str:
        return """<script setup>
defineProps({
  title: { type: String, required: true },
  type: { type: String, default: 'bar' }
})
</script>

<template>
  <section class="panel chart-block">
    <div class="panel-heading">
      <h2>{{ title }}</h2>
      <span>{{ type }}</span>
    </div>
    <div class="chart-placeholder">
      <span>Chart component placeholder</span>
    </div>
  </section>
</template>
"""

    def css(self) -> str:
        return """:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #17202a;
  background: #f4f7fb;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  min-width: 320px;
}

a {
  color: inherit;
  text-decoration: none;
}

button,
input {
  font: inherit;
}

.app-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 260px 1fr;
}

.sidebar {
  background: #101828;
  color: white;
  padding: 18px;
  display: grid;
  align-content: start;
  gap: 18px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 44px;
}

.brand-mark {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 8px;
  background: #2dd4bf;
  color: #042f2e;
  font-weight: 900;
}

.nav-list {
  display: grid;
  gap: 8px;
}

.nav-link {
  padding: 10px 12px;
  border-radius: 8px;
  color: #d0d5dd;
}

.nav-link.router-link-active,
.nav-link:hover {
  background: #1d2939;
  color: white;
}

.workspace {
  min-width: 0;
  display: grid;
  grid-template-rows: auto 1fr;
}

.topbar {
  min-height: 62px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  background: white;
  border-bottom: 1px solid #d9e2ec;
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  color: #52616b;
  font-size: 14px;
}

.page {
  padding: 24px;
  display: grid;
  gap: 16px;
  align-content: start;
}

.page-heading h1,
.panel h2 {
  margin: 0;
}

.eyebrow,
.panel-heading span,
.stat-card span {
  color: #697386;
  font-size: 13px;
}

.stat-card,
.panel {
  background: white;
  border: 1px solid #d9e2ec;
  border-radius: 8px;
}

.stat-card {
  min-height: 118px;
  padding: 18px;
  display: grid;
  align-content: space-between;
}

.stat-card strong {
  font-size: 32px;
}

.panel {
  overflow: hidden;
}

.panel-heading {
  padding: 14px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  border-bottom: 1px solid #d9e2ec;
}

.table-wrap {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  text-align: left;
  padding: 12px 14px;
  border-bottom: 1px solid #edf2f7;
  white-space: nowrap;
}

th {
  color: #52616b;
  font-size: 13px;
}

.form-grid {
  padding-bottom: 16px;
  display: grid;
  gap: 14px;
}

.form-grid label {
  padding: 0 16px;
  display: grid;
  gap: 6px;
}

.form-grid input {
  min-height: 40px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 8px 10px;
}

.primary-button,
.ghost-button {
  min-height: 38px;
  border: 0;
  border-radius: 8px;
  padding: 8px 12px;
  cursor: pointer;
}

.primary-button {
  justify-self: start;
  margin-left: 16px;
  background: #0f766e;
  color: white;
}

.ghost-button {
  background: #eef2f7;
  color: #344054;
}

.chart-placeholder {
  min-height: 220px;
  display: grid;
  place-items: center;
  color: #697386;
  background: linear-gradient(135deg, #f8fafc, #ecfeff);
}

.empty {
  padding: 16px;
  color: #697386;
}

@media (max-width: 820px) {
  .app-shell {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
  }
}
"""

    def readme(self, app_name: str) -> str:
        return f"""# {app_name} Vue Frontend

Generated by NovaDev 0.5.

## Run

```bash
npm install
npm run dev
```

The Vite dev server proxies `/api` requests to `http://127.0.0.1:5000`.

## Build

```bash
npm run build
```

This project uses Vue 3, Vite, Vue Router, Pinia, fetch-based API services, and
custom CSS. The generated code is normal editable Vue code.
"""


def api_resource_name(table_name: str) -> str:
    words = re.sub(r"(?<!^)(?=[A-Z])", "-", table_name).replace("_", "-").lower()
    base = re.sub(r"[^a-z0-9-]+", "-", words).strip("-") or "rows"
    if base.endswith("y") and not base.endswith(("ay", "ey", "iy", "oy", "uy")):
        return base[:-1] + "ies"
    if base.endswith("s"):
        return base + "es"
    return base + "s"


def primary_key(table: TableNode) -> str:
    for field in table.fields:
        if field.auto:
            return field.name
    for field in table.fields:
        if field.name == "id":
            return field.name
    return table.fields[0].name if table.fields else "id"


def default_columns(table: TableNode | None, include_auto: bool = True) -> List[str]:
    if not table:
        return []
    return [field.name for field in table.fields if include_auto or not field.auto and not field.secure]


def table_name_from_expression(source: str) -> str:
    match = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\.count\(\)", source or "")
    return match.group(1) if match else ""


def slug_name(name: str) -> str:
    separated = re.sub(r"(.)([A-Z][a-z]+)", r"\1-\2", name)
    separated = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", separated)
    return re.sub(r"[^a-zA-Z0-9-]+", "-", separated).strip("-").lower() or "novadev-app"


def escape_html(value: Any) -> str:
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def escape_attr(value: Any) -> str:
    return escape_html(value).replace('"', "&quot;")


def vue_expr(value: Any) -> str:
    return escape_attr(json.dumps(value))
