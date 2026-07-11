# UI System

NovaDev UI is declarative. You describe pages and components in `.nova` source,
and NovaDev generates browser files.

## Build Command

```powershell
python nova.py build-ui examples\business_admin.nova
```

Generated files:

```txt
dist/index.html
dist/style.css
dist/app.js
```

For a connected frontend/backend app, use:

```powershell
python nova.py build-app examples\business_admin.nova
cd generated_backend
python -m pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`. The Flask app serves the UI and the JSON API.

## UI Pipeline

```txt
NovaDev source
  -> lexer
  -> parser
  -> page/table/component AST
  -> runtime registries
  -> HTML/CSS/JS generator
  -> Flask backend generator
  -> working dashboard backed by API routes
```

## Pages

```nova
page Products {
    title "Product Manager"
}
```

Generated pages become hash routes:

```txt
Products -> /products
AdminDashboard -> /admin-dashboard
```

## Role-Based Pages

```nova
page Dashboard {
    require role Admin
    title "Business Dashboard"
}
```

The generated dashboard includes a role selector. If the selected role does not
match the page requirement, the UI hides the page and shows an access warning.

## Tables And Forms

Source:

```nova
table Product {
    id auto
    name text
    price money
    stock int
}

page Products {
    form Product {
        fields name, price, stock
        submit "Add Product"
    }
}
```

Generated UI:

```txt
Name input
Price number input
Stock number input
Add Product button
```

If the UI is opened directly from `dist/index.html`, submitted rows are stored in
local browser data. If the UI is served by Flask, submitted rows are sent to the
backend with POST requests.

## Table Views And Actions

Source:

```nova
table Product {
    columns name, price, stock
    actions view, edit, delete
}
```

Generated UI:

- table headers
- demo data rows
- action buttons
- backend-backed delete behavior when served by Flask
- backend-backed edit behavior when served by Flask

## Cards

Source:

```nova
card "Products" {
    value Product.count()
}
```

Generated UI binds the card value to local table data.

Supported card expressions:

```txt
Table.count()
Table.sum(field)
```

## Charts

Source:

```nova
chart Order {
    type bar
    x customer
    y total
}
```

Generated UI uses an HTML canvas chart.

## Navigation

```nova
navbar {
    link "Dashboard" to "/dashboard"
    link "Products" to "/products"
}

sidebar {
    link "Dashboard" to "/dashboard"
    link "Products" to "/products"
}
```

## Modals

```nova
modal "Product Help" {
    text "Use this page to add, inspect, and remove product rows."
    button "Got it"
}
```

## Themes

Source:

```nova
theme CyberDark {
    background "#101114"
    panel "#181b20"
    panel_alt "#22262d"
    accent "#45d6b5"
    accent_alt "#f4b860"
    text "#f4f6f8"
    muted "#9aa4b2"
    border "#303640"
    danger "#ff6b6b"
}

use theme CyberDark
```

Generated CSS uses theme values as CSS variables.
