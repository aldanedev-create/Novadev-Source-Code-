# NovaDev Examples

This page is a quick copy-paste guide for learning NovaDev syntax.

## Hello World

```nova
print("Hello NovaDev")
```

Run it:

```powershell
python nova.py run examples\hello.nova
```

## Variables

```nova
let name = "Aldane"
let age = 20

print(name)
print(age + 5)
```

## Strings And Numbers

```nova
let product = "Keyboard"
let price = 99

print(product + " costs " + price)
```

Output:

```txt
Keyboard costs 99
```

## Booleans And Nil

```nova
let active = true
let missing = nil

print(active)
print(missing)
```

## If And Else

```nova
let stock = 8

if stock > 0 {
    print("In stock")
} else {
    print("Sold out")
}
```

## While Loop

```nova
let x = 0

while x < 3 {
    print("loop " + x)
    x = x + 1
}
```

## Functions

```nova
function greet(name) {
    return "Hello " + name
}

print(greet("Aldane"))
```

## Interactive Shell Programming

Start the shell:

```powershell
python shell.py
```

Variables and print run immediately:

```txt
nova> let name = "Aldane"
nova> print(name)
Aldane
```

For multi-line blocks, press a blank line after the closing brace:

```txt
nova> let stock = 8
nova> if stock > 0 {
...     print("In stock")
... } else {
...     print("Sold out")
... }
...
In stock
```

Loops:

```txt
nova> let x = 0
nova> while x < 3 {
...     print("loop " + x)
...     x = x + 1
... }
...
loop 0
loop 1
loop 2
```

Functions:

```txt
nova> function greet(name) {
...     return "Hello " + name
... }
...
nova> print(greet("Aldane"))
Hello Aldane
```

## Table Model

```nova
table Product {
    id auto
    name text
    price money
    stock int
}
```

## App With A Page

Save this as `examples\my_app.nova`:

```nova
app ProductDesk {
    table Product {
        id auto
        name text
        price money
        stock int
    }

    page Products {
        title "Products"

        card "Total Products" {
            value Product.count()
        }

        form Product {
            fields name, price, stock
            submit "Add Product"
        }

        table Product {
            columns name, price, stock
            actions view, delete
        }
    }
}
```

Build the UI:

```powershell
python nova.py build-app examples\my_app.nova
```

## Theme

```nova
theme CyberDark {
    background "#101114"
    panel "#181b20"
    accent "#45d6b5"
    text "#f4f6f8"
}

use theme CyberDark
```

## Auth And Roles

```nova
table User {
    id auto
    name text
    email email unique
    role text
    password secure
}

auth User

page AdminDashboard {
    require role Admin
    title "Admin Dashboard"
}
```

## Route

```nova
route GET "/api/products" {
    require role Admin
    return Product.all()
}
```

Generate backend starter files:

```powershell
python nova.py build-app examples\business_admin.nova
```

## Full Example

See:

```txt
examples/business_admin.nova
```

Useful commands:

```powershell
python nova.py tokens examples\business_admin.nova
python nova.py ast examples\business_admin.nova --json
python nova.py build-ui examples\business_admin.nova
python nova.py build-backend examples\business_admin.nova
python nova.py build-app examples\business_admin.nova
```

## E-Commerce Store Example

See:

```txt
examples/ecommerce_store.nova
```

Build and run it:

```powershell
python nova.py build-app examples\ecommerce_store.nova --ui-output dist_ecommerce --backend-output generated_backend_ecommerce
cd generated_backend_ecommerce
python -m pip install -r requirements.txt
python app.py
```

Open:

```txt
http://127.0.0.1:5000
```

The e-commerce example uses these NovaDev components:

```nova
catalog Product {
    fields name, description, category, price, stock
    actions add_to_cart
}

cart CartItem {
    fields productName, price, quantity
}

checkout Order {
    fields customerName, email, address
    submit "Place Order"
}
```

The generated Flask app supports product browsing, add to cart, quantity changes,
checkout, order creation, order items, cart clearing, and stock decrementing.
