const NOVA_APP = {
  "name": "BusinessAdmin",
  "tables": {
    "User": {
      "endpoint": "/api/users",
      "primaryKey": "id",
      "fields": [
        {
          "name": "id",
          "type": "auto",
          "auto": true,
          "secure": false,
          "unique": false
        },
        {
          "name": "name",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "email",
          "type": "email",
          "auto": false,
          "secure": false,
          "unique": true
        },
        {
          "name": "role",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "password",
          "type": "secure",
          "auto": false,
          "secure": true,
          "unique": false
        }
      ]
    },
    "Product": {
      "endpoint": "/api/products",
      "primaryKey": "id",
      "fields": [
        {
          "name": "id",
          "type": "auto",
          "auto": true,
          "secure": false,
          "unique": false
        },
        {
          "name": "name",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "price",
          "type": "money",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "stock",
          "type": "int",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "active",
          "type": "boolean",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    },
    "Order": {
      "endpoint": "/api/orders",
      "primaryKey": "id",
      "fields": [
        {
          "name": "id",
          "type": "auto",
          "auto": true,
          "secure": false,
          "unique": false
        },
        {
          "name": "customer",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "total",
          "type": "money",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "status",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    }
  },
  "pages": [
    {
      "title": "Business Dashboard",
      "path": "/dashboard",
      "role": "Admin"
    },
    {
      "title": "Product Manager",
      "path": "/products",
      "role": "Admin"
    }
  ],
  "data": {
    "User": [
      {
        "id": 1,
        "name": "Name 1",
        "email": "email1@example.com",
        "role": "Role 1",
        "password": "Password 1"
      },
      {
        "id": 2,
        "name": "Name 2",
        "email": "email2@example.com",
        "role": "Role 2",
        "password": "Password 2"
      },
      {
        "id": 3,
        "name": "Name 3",
        "email": "email3@example.com",
        "role": "Role 3",
        "password": "Password 3"
      }
    ],
    "Product": [
      {
        "id": 1,
        "name": "Name 1",
        "price": 25,
        "stock": 25,
        "active": true
      },
      {
        "id": 2,
        "name": "Name 2",
        "price": 50,
        "stock": 50,
        "active": false
      },
      {
        "id": 3,
        "name": "Name 3",
        "price": 75,
        "stock": 75,
        "active": true
      }
    ],
    "Order": [
      {
        "id": 1,
        "customer": "Customer 1",
        "total": 25,
        "status": "Status 1"
      },
      {
        "id": 2,
        "customer": "Customer 2",
        "total": 50,
        "status": "Status 2"
      },
      {
        "id": 3,
        "customer": "Customer 3",
        "total": 75,
        "status": "Status 3"
      }
    ]
  }
};

const state = {
  role: localStorage.getItem("nova-role") || "Admin",
  light: localStorage.getItem("nova-light") === "true"
};

const $ = (selector, parent = document) => parent.querySelector(selector);
const $$ = (selector, parent = document) => Array.from(parent.querySelectorAll(selector));

function backendEnabled() {
  return location.protocol === "http:" || location.protocol === "https:";
}

function tableEndpoint(tableName) {
  return NOVA_APP.tables[tableName]?.endpoint || `/api/${String(tableName).toLowerCase()}s`;
}

function primaryKeyFor(tableName) {
  return NOVA_APP.tables[tableName]?.primaryKey || "id";
}

async function apiRequest(path, options = {}) {
  const headers = Object.assign({ "Content-Type": "application/json" }, options.headers || {});
  const response = await fetch(path, Object.assign({}, options, { headers }));
  const text = await response.text();
  const payload = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw new Error(payload.error || `Request failed: ${response.status}`);
  }
  return payload;
}

async function loadBackendData() {
  if (!backendEnabled()) return;
  const tableNames = Object.keys(NOVA_APP.tables || {});
  await Promise.all(tableNames.map(async (tableName) => {
    try {
      const payload = await apiRequest(tableEndpoint(tableName));
      NOVA_APP.data[tableName] = Array.isArray(payload) ? payload : (payload.rows || []);
    } catch (error) {
      console.warn(`Using local sample data for ${tableName}:`, error.message);
    }
  }));
}

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
    form.addEventListener("submit", async (event) => {
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
      try {
        if (backendEnabled()) {
          await apiRequest(tableEndpoint(tableName), {
            method: "POST",
            body: JSON.stringify(row)
          });
          await loadBackendData();
        } else {
          rows.push(row);
          NOVA_APP.data[tableName] = rows;
        }
        form.reset();
        renderAll();
      } catch (error) {
        alert(error.message);
      }
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

async function handleActions(event) {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const tableName = button.dataset.table;
  const rows = NOVA_APP.data[tableName] || [];
  const index = Number(button.dataset.index);
  const row = rows[index];
  if (!row) return;

  if (button.dataset.action === "delete") {
    try {
      if (backendEnabled()) {
        const key = primaryKeyFor(tableName);
        await apiRequest(`${tableEndpoint(tableName)}/${encodeURIComponent(row[key])}`, { method: "DELETE" });
        await loadBackendData();
      } else {
        rows.splice(index, 1);
      }
      renderAll();
    } catch (error) {
      alert(error.message);
    }
    return;
  }

  if (button.dataset.action === "edit") {
    const editable = visibleFields(tableName)[0];
    if (!editable) return;
    const next = prompt(`Edit ${editable.name}`, row[editable.name]);
    if (next == null) return;
    const updated = Object.assign({}, row, {
      [editable.name]: numericType(editable.type) ? Number(next || 0) : next
    });
    try {
      if (backendEnabled()) {
        const key = primaryKeyFor(tableName);
        await apiRequest(`${tableEndpoint(tableName)}/${encodeURIComponent(row[key])}`, {
          method: "PUT",
          body: JSON.stringify(updated)
        });
        await loadBackendData();
      } else {
        rows[index] = updated;
      }
      renderAll();
    } catch (error) {
      alert(error.message);
    }
    return;
  }

  alert(JSON.stringify(row, null, 2));
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

document.addEventListener("DOMContentLoaded", async () => {
  setupForms();
  setupModals();
  setupRoleAndTheme();
  document.addEventListener("click", handleActions);
  window.addEventListener("hashchange", activateRoute);
  window.addEventListener("resize", drawCharts);
  await loadBackendData();
  if (!location.hash && NOVA_APP.pages[0]) location.hash = NOVA_APP.pages[0].path;
  activateRoute();
});
