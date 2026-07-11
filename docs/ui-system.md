# UI System

NovaDev pages describe admin-style UI screens with high-level components.

```nova
page Products {
    title "Products"
    navbar "Store Admin"
    sidebar "Catalog"
    card "Products" value "Product.count()"
    chart "Sales" type "line"
    form Product {
        fields name, price, stock
        submit "Save Product"
    }
    table Product {
        columns name, price, stock
        actions view, edit, delete
    }
    modal ProductDetails {
        title "Product Details"
    }
}
```

Build a static HTML/CSS/JS UI:

```bash
python nova.py build-ui examples/apps/webshield
```

Build a Vue frontend:

```bash
python nova.py build-vue examples/apps/webshield
```

Build frontend and backend together:

```bash
python nova.py build-fullstack examples/apps/webshield
```
