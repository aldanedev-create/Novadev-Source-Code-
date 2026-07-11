# Vue Generation

NovaDev 1.0 can generate a Vue 3 + Vite frontend from page, table, form, card,
chart, navbar, sidebar, and modal declarations.

```nova
project {
    frontend Vue
}

page Products {
    title "Products"
    card "Inventory" value "Product.count()"
    form Product {
        fields name, price, stock
        submit "Save Product"
    }
    table Product {
        columns name, price, stock
        actions view, edit, delete
    }
}
```

Build:

```bash
python nova.py build-vue examples/apps/webshield
```

Run:

```bash
cd generated/web-shield/frontend
npm install
npm run dev
```
