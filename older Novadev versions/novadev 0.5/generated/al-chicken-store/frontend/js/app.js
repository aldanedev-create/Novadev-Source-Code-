const NOVA_APP = {
  "name": "ALChickenStore",
  "tables": {
    "Customer": {
      "endpoint": "/api/customers",
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
          "name": "password",
          "type": "password",
          "auto": false,
          "secure": true,
          "unique": false
        },
        {
          "name": "role",
          "type": "text",
          "auto": false,
          "secure": false,
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
          "name": "description",
          "type": "text",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "category",
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
          "type": "number",
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
    "CartItem": {
      "endpoint": "/api/cart-items",
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
          "name": "productId",
          "type": "number",
          "auto": false,
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
          "name": "quantity",
          "type": "number",
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
          "name": "customerName",
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
          "unique": false
        },
        {
          "name": "address",
          "type": "text",
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
        },
        {
          "name": "total",
          "type": "money",
          "auto": false,
          "secure": false,
          "unique": false
        }
      ]
    },
    "OrderItem": {
      "endpoint": "/api/order-items",
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
          "name": "orderId",
          "type": "number",
          "auto": false,
          "secure": false,
          "unique": false
        },
        {
          "name": "productId",
          "type": "number",
          "auto": false,
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
          "name": "quantity",
          "type": "number",
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
        }
      ]
    }
  },
  "pages": [
    {
      "title": "ALChicken Store",
      "path": "/storefront",
      "role": null
    },
    {
      "title": "Shopping Cart",
      "path": "/cart",
      "role": null
    },
    {
      "title": "Checkout",
      "path": "/checkout",
      "role": null
    },
    {
      "title": "Store Admin",
      "path": "/admin",
      "role": "Admin"
    },
    {
      "title": "Orders",
      "path": "/orders",
      "role": "Admin"
    }
  ],
  "data": {
    "Customer": [
      {
        "id": 1,
        "name": "Name 1",
        "email": "email1@example.com",
        "password": "Password 1",
        "role": "Role 1"
      },
      {
        "id": 2,
        "name": "Name 2",
        "email": "email2@example.com",
        "password": "Password 2",
        "role": "Role 2"
      },
      {
        "id": 3,
        "name": "Name 3",
        "email": "email3@example.com",
        "password": "Password 3",
        "role": "Role 3"
      }
    ],
    "Product": [
      {
        "id": 1,
        "name": "Aurora Hoodie",
        "description": "Soft heavyweight fleece for everyday wear.",
        "category": "Apparel",
        "price": 68,
        "stock": 24,
        "active": true
      },
      {
        "id": 2,
        "name": "Orbit Desk Lamp",
        "description": "Adjustable LED lamp with warm and cool modes.",
        "category": "Home",
        "price": 89,
        "stock": 18,
        "active": true
      },
      {
        "id": 3,
        "name": "Nova Tote",
        "description": "Durable canvas tote for work, gym, and errands.",
        "category": "Accessories",
        "price": 32,
        "stock": 40,
        "active": true
      },
      {
        "id": 4,
        "name": "Focus Bottle",
        "description": "Insulated stainless bottle that keeps drinks cold.",
        "category": "Drinkware",
        "price": 28,
        "stock": 35,
        "active": true
      }
    ],
    "CartItem": [],
    "Order": [],
    "OrderItem": []
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

function tableByName(...names) {
  const tableNames = Object.keys(NOVA_APP.tables || {});
  for (const wanted of names) {
    const exact = tableNames.find((name) => name.toLowerCase() === String(wanted).toLowerCase());
    if (exact) return exact;
  }
  for (const wanted of names) {
    const fuzzy = tableNames.find((name) => name.toLowerCase().includes(String(wanted).toLowerCase()));
    if (fuzzy) return fuzzy;
  }
  return "";
}

function rowsFor(tableName) {
  return NOVA_APP.data[tableName] || [];
}

function fieldNames(tableName) {
  return fieldsFor(tableName).map((field) => field.name);
}

function fieldByCandidates(tableName, candidates) {
  const names = fieldNames(tableName);
  for (const candidate of candidates) {
    const exact = names.find((name) => name.toLowerCase() === candidate.toLowerCase());
    if (exact) return exact;
  }
  for (const candidate of candidates) {
    const fuzzy = names.find((name) => name.toLowerCase().includes(candidate.toLowerCase()));
    if (fuzzy) return fuzzy;
  }
  return "";
}

function money(value) {
  return new Intl.NumberFormat(undefined, { style: "currency", currency: "USD" }).format(Number(value || 0));
}

function productFields(tableName) {
  return {
    id: primaryKeyFor(tableName),
    name: fieldByCandidates(tableName, ["name", "title", "productName"]),
    price: fieldByCandidates(tableName, ["price", "amount", "cost"]),
    description: fieldByCandidates(tableName, ["description", "summary", "details"]),
    category: fieldByCandidates(tableName, ["category", "type"]),
    stock: fieldByCandidates(tableName, ["stock", "inventory", "quantity"]),
    active: fieldByCandidates(tableName, ["active", "enabled"]),
  };
}

function cartTableName() {
  return tableByName("CartItem", "CartLine", "Cart");
}

function orderTableName() {
  return tableByName("Order", "Purchase");
}

function cartFields(tableName) {
  return {
    id: primaryKeyFor(tableName),
    productId: fieldByCandidates(tableName, ["productId", "product_id", "product"]),
    productName: fieldByCandidates(tableName, ["productName", "product_name", "name"]),
    price: fieldByCandidates(tableName, ["price", "unitPrice", "amount"]),
    quantity: fieldByCandidates(tableName, ["quantity", "qty", "count"]),
  };
}

function rowId(tableName, row) {
  return row[primaryKeyFor(tableName)];
}

function renderCommerce() {
  renderCatalogs();
  renderCarts();
}

function renderCatalogs() {
  $$("[data-catalog]").forEach((section) => {
    const tableName = section.dataset.catalog;
    const grid = $("[data-product-grid]", section);
    const search = ($("[data-product-search]", section)?.value || "").toLowerCase();
    if (!grid) return;
    const fields = productFields(tableName);
    const rows = rowsFor(tableName).filter((row) => {
      const active = fields.active ? row[fields.active] !== false : true;
      const name = String(row[fields.name] || "");
      const category = String(row[fields.category] || "");
      return active && (!search || `${name} ${category}`.toLowerCase().includes(search));
    });

    if (!rows.length) {
      grid.innerHTML = '<div class="empty-state">No products found.</div>';
      return;
    }

    grid.replaceChildren(...rows.map((row) => productCard(tableName, row, fields)));
  });
}

function productCard(tableName, row, fields) {
  const card = document.createElement("article");
  card.className = "product-card";
  const id = row[fields.id];
  const name = row[fields.name] || `Product ${id}`;
  const description = row[fields.description] || "A useful product from this NovaDev store.";
  const price = Number(row[fields.price] || 0);
  const stock = fields.stock ? Number(row[fields.stock] || 0) : 99;
  const initials = String(name).split(/\s+/).map((part) => part[0]).join("").slice(0, 2).toUpperCase();
  card.innerHTML = `
    <div class="product-art">${initials || "N"}</div>
    <div class="product-card-body">
      <div>
        <h3>${escapeHtml(name)}</h3>
        <p>${escapeHtml(description)}</p>
      </div>
      <div class="product-card-footer">
        <span class="product-price">${money(price)}</span>
        <button class="primary-button" data-add-to-cart data-product-table="${tableName}" data-product-id="${id}" ${stock <= 0 ? "disabled" : ""}>
          ${stock <= 0 ? "Sold Out" : "Add"}
        </button>
      </div>
    </div>
  `;
  return card;
}

function renderCarts() {
  $$("[data-cart]").forEach((section) => {
    const tableName = section.dataset.cart || cartTableName();
    const list = $("[data-cart-items]", section);
    const totalNode = $("[data-cart-total]", section);
    if (!list) return;
    const fields = cartFields(tableName);
    const rows = rowsFor(tableName);
    let total = 0;

    if (!rows.length) {
      list.innerHTML = '<div class="empty-state">Your cart is empty.</div>';
      if (totalNode) totalNode.textContent = money(0);
      return;
    }

    list.replaceChildren(...rows.map((row, index) => {
      const quantity = Number(row[fields.quantity] || 1);
      const price = Number(row[fields.price] || 0);
      total += quantity * price;
      const item = document.createElement("article");
      item.className = "cart-item";
      item.innerHTML = `
        <div>
          <strong>${escapeHtml(row[fields.productName] || `Item ${index + 1}`)}</strong>
          <span>${quantity} x ${money(price)}</span>
        </div>
        <div class="cart-controls">
          <button data-cart-change="-1" data-cart-index="${index}" type="button">-</button>
          <span>${quantity}</span>
          <button data-cart-change="1" data-cart-index="${index}" type="button">+</button>
          <button data-cart-remove data-cart-index="${index}" type="button">Remove</button>
        </div>
      `;
      return item;
    }));

    if (totalNode) totalNode.textContent = money(total);
  });
}

function setupCommerceSearch() {
  $$("[data-product-search]").forEach((input) => {
    input.addEventListener("input", renderCatalogs);
  });
}

function setupCheckoutForms() {
  $$("form[data-checkout]").forEach((form) => {
    const tableName = form.dataset.checkout || orderTableName();
    const selected = form.dataset.fields ? form.dataset.fields.split(",").filter(Boolean) : [];
    const fields = selected.length
      ? selected
      : visibleFields(tableName).filter((field) => !["total", "status"].includes(field.name.toLowerCase())).map((field) => field.name);
    const container = $("[data-checkout-fields]", form);
    if (container) {
      container.replaceChildren(...fields.map((fieldName) => {
        const field = fieldsFor(tableName).find((item) => item.name === fieldName) || { name: fieldName, type: "text" };
        const label = document.createElement("label");
        label.className = "form-field";
        label.innerHTML = `<span>${field.name}</span><input name="${field.name}" type="${inputType(field.type)}" required>`;
        return label;
      }));
    }
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const data = {};
      fields.forEach((fieldName) => {
        const input = form.elements[fieldName];
        if (input) data[fieldName] = input.value;
      });
      try {
        let order = null;
        if (backendEnabled()) {
          const payload = await apiRequest("/api/checkout", {
            method: "POST",
            body: JSON.stringify(data)
          });
          order = payload.order;
          await loadBackendData();
        } else {
          order = localCheckout(tableName, data);
        }
        form.reset();
        renderAll();
        alert(`Order placed${order?.id ? ` #${order.id}` : ""}`);
      } catch (error) {
        alert(error.message);
      }
    });
  });
}

async function handleCommerceClick(event) {
  const addButton = event.target.closest("[data-add-to-cart]");
  if (addButton) {
    await addProductToCart(addButton.dataset.productTable, addButton.dataset.productId);
    return;
  }

  const changeButton = event.target.closest("[data-cart-change]");
  if (changeButton) {
    await changeCartQuantity(Number(changeButton.dataset.cartIndex), Number(changeButton.dataset.cartChange));
    return;
  }

  const removeButton = event.target.closest("[data-cart-remove]");
  if (removeButton) {
    await removeCartItem(Number(removeButton.dataset.cartIndex));
    return;
  }

  if (event.target.closest("[data-cart-clear]")) {
    await clearCart();
  }
}

async function addProductToCart(productTable, productId) {
  const product = rowsFor(productTable).find((row) => String(rowId(productTable, row)) === String(productId));
  const cartTable = cartTableName();
  if (!product || !cartTable) return;
  const p = productFields(productTable);
  const c = cartFields(cartTable);
  const rows = rowsFor(cartTable);
  const existing = rows.find((row) => String(row[c.productId]) === String(productId));
  const payload = {
    [c.productId || "productId"]: Number(productId),
    [c.productName || "productName"]: product[p.name] || `Product ${productId}`,
    [c.price || "price"]: Number(product[p.price] || 0),
    [c.quantity || "quantity"]: existing ? Number(existing[c.quantity] || 1) + 1 : 1
  };

  if (backendEnabled()) {
    if (existing) {
      await apiRequest(`${tableEndpoint(cartTable)}/${encodeURIComponent(rowId(cartTable, existing))}`, {
        method: "PUT",
        body: JSON.stringify(payload)
      });
    } else {
      await apiRequest(tableEndpoint(cartTable), { method: "POST", body: JSON.stringify(payload) });
    }
    await loadBackendData();
  } else if (existing) {
    existing[c.quantity] = payload[c.quantity || "quantity"];
  } else {
    payload[primaryKeyFor(cartTable)] = rows.length + 1;
    rows.push(payload);
  }
  renderAll();
}

async function changeCartQuantity(index, delta) {
  const cartTable = cartTableName();
  const rows = rowsFor(cartTable);
  const row = rows[index];
  if (!row) return;
  const c = cartFields(cartTable);
  const next = Number(row[c.quantity] || 1) + delta;
  if (next <= 0) {
    await removeCartItem(index);
    return;
  }
  const payload = Object.assign({}, row, { [c.quantity || "quantity"]: next });
  if (backendEnabled()) {
    await apiRequest(`${tableEndpoint(cartTable)}/${encodeURIComponent(rowId(cartTable, row))}`, {
      method: "PUT",
      body: JSON.stringify(payload)
    });
    await loadBackendData();
  } else {
    row[c.quantity] = next;
  }
  renderAll();
}

async function removeCartItem(index) {
  const cartTable = cartTableName();
  const rows = rowsFor(cartTable);
  const row = rows[index];
  if (!row) return;
  if (backendEnabled()) {
    await apiRequest(`${tableEndpoint(cartTable)}/${encodeURIComponent(rowId(cartTable, row))}`, { method: "DELETE" });
    await loadBackendData();
  } else {
    rows.splice(index, 1);
  }
  renderAll();
}

async function clearCart() {
  const cartTable = cartTableName();
  const rows = [...rowsFor(cartTable)];
  if (backendEnabled()) {
    await Promise.all(rows.map((row) => apiRequest(`${tableEndpoint(cartTable)}/${encodeURIComponent(rowId(cartTable, row))}`, { method: "DELETE" })));
    await loadBackendData();
  } else {
    rowsFor(cartTable).splice(0);
  }
  renderAll();
}

function localCheckout(orderTable, customer) {
  const cartTable = cartTableName();
  const cartRows = rowsFor(cartTable);
  const c = cartFields(cartTable);
  const total = cartRows.reduce((sum, row) => sum + Number(row[c.price] || 0) * Number(row[c.quantity] || 1), 0);
  const order = Object.assign({}, customer, {
    id: rowsFor(orderTable).length + 1,
    total,
    status: "Paid"
  });
  NOVA_APP.data[orderTable] = rowsFor(orderTable).concat(order);
  NOVA_APP.data[cartTable] = [];
  return order;
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value == null ? "" : String(value);
  return div.innerHTML;
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
  renderCommerce();
  drawCharts();
}

document.addEventListener("DOMContentLoaded", async () => {
  setupForms();
  setupCommerceSearch();
  setupCheckoutForms();
  setupModals();
  setupRoleAndTheme();
  document.addEventListener("click", handleActions);
  document.addEventListener("click", handleCommerceClick);
  window.addEventListener("hashchange", activateRoute);
  window.addEventListener("resize", drawCharts);
  await loadBackendData();
  if (!location.hash && NOVA_APP.pages[0]) location.hash = NOVA_APP.pages[0].path;
  activateRoute();
});
