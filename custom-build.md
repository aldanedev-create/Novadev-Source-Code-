# NovaDev 1.0 Mini Book: Building Custom Projects

This mini book teaches developers how to use NovaDev 1.0 to design and build
custom projects. It is written for beginners, but it uses the same workflow a
developer would use on a real application: model the data, design screens,
define backend routes, add custom code, generate the project, then keep editing
the generated files.

## Table Of Contents

1. What NovaDev Is
2. The NovaDev Mental Model
3. Starting A Project
4. Writing Normal Code
5. Designing Your App
6. Modeling Data With Tables
7. Building Pages And UI
8. Creating Backend Routes
9. Custom Project Architecture
10. Modules And Imports
11. Python, JavaScript, CSS, And SQL Custom Code
12. Plugins And Project Metadata
13. Building And Running Generated Projects
14. Recipes For Custom Projects
15. Developer Checklist
16. Troubleshooting

## 1. What NovaDev Is

NovaDev is both a programming language and a project builder.

You can use it as a scripting language:

```nova
let name = "Aldane"
print("Hello {name}")
```

You can also use it to describe a full-stack application:

```nova
app StoreAdmin {
    project {
        frontend Vue
        backend Flask
        database SQLite
    }

    table Product {
        id auto
        name text
        price money
        stock int
    }

    page Products {
        title "Products"
        table Product {
            columns name, price, stock
            actions view, edit, delete
        }
    }
}
```

NovaDev reads this source code, tokenizes it, parses it into AST nodes, and then
either runs it or generates project files.

## 2. The NovaDev Mental Model

Think of NovaDev in five layers:

```txt
source code -> lexer -> parser -> AST -> runtime/generators
```

The lexer turns text into tokens:

```txt
let name = "Aldane"
```

becomes tokens like:

```txt
LET IDENTIFIER EQUAL STRING
```

The parser turns tokens into AST nodes:

```txt
LetNode(name="name", expression=LiteralNode("Aldane"))
```

The runtime executes normal programming statements. The generators use app
declarations to create folders, frontend files, backend files, docs, and
metadata.

This means your NovaDev file can contain both:

- code that runs now
- declarations that generate a project

## 3. Starting A Project

Create a project folder:

```bash
python nova.py new examples/apps/my_custom_app --frontend Vue --backend Flask --database SQLite
```

This creates:

```txt
examples/apps/my_custom_app/
  Nova.toml
  app.nova
```

`Nova.toml` tells NovaDev where the entry file is:

```toml
name = "MyCustomApp"
version = "1.0"
entry = "app.nova"
frontend = "Vue"
backend = "Flask"
database = "SQLite"
```

Run commands directly:

```bash
python nova.py build-fullstack examples/apps/my_custom_app
```

Or use the interactive shell:

```bash
python shell.py
```

Inside the shell:

```txt
nova> .build-fullstack examples/apps/my_custom_app
nova> .tokens examples/apps/my_custom_app
nova> .ast examples/apps/my_custom_app --json
nova> .exit
```

## 4. Writing Normal Code

NovaDev can run general programming code.

Variables:

```nova
let product = "Keyboard"
let price = 49.99
let inStock = true
let missing = nil
```

Lists and objects:

```nova
let cart = [
    { name: "Keyboard", price: 49.99 },
    { name: "Mouse", price: 25 }
]
```

Loops:

```nova
for item in cart {
    print("{item.name}: {item.price}")
}
```

Functions:

```nova
function total(items) {
    let amount = 0
    for item in items {
        amount = amount + item.price
    }
    return amount
}

print(total(cart))
```

Classes:

```nova
class User {
    function init(name) {
        self.name = name
    }

    function label() {
        return "User: {self.name}"
    }
}

let user = User("Aldane")
print(user.label())
```

Use scripts for small tools, calculations, file helpers, and automation.

## 5. Designing Your App

Before writing a NovaDev app, answer five questions:

- What is the app called?
- What data does it store?
- What pages does the user need?
- What backend routes does the frontend need?
- What custom files or code should be generated?

Example planning table:

```txt
App: CampusStore
Data: Product, Customer, Order, OrderItem
Pages: Dashboard, Products, Orders, Customers
Routes: /api/products, /api/orders, /api/checkout
Custom code: currency helper, stock rules, dashboard styles
```

Then turn that plan into NovaDev declarations.

## 6. Modeling Data With Tables

Tables describe the main data in your app.

```nova
table Product {
    id auto
    name text
    description text
    category text
    price money
    stock int
}

table Customer {
    id auto
    name text
    email email unique
    phone text
}

table Order {
    id auto
    customerName text
    email email
    status text
    total money
}
```

Common field types:

```txt
auto, text, int, number, money, email, bool, date, secure
```

Use `secure` for sensitive fields:

```nova
table User {
    id auto
    email email unique
    password secure
    role text
}
```

Good table names are singular:

```txt
Product, Customer, Order, Invoice, Employee
```

The generated backend creates starter API resources from these tables.

## 7. Building Pages And UI

Pages describe what the user sees.

```nova
page Dashboard {
    title "Dashboard"
    card "Products" value "Product.count()"
    card "Orders" value "Order.count()"
    chart "Sales" type "line"
}
```

A table UI:

```nova
page Products {
    title "Products"

    form Product {
        fields name, description, category, price, stock
        submit "Save Product"
    }

    table Product {
        columns name, category, price, stock
        actions view, edit, delete
    }
}
```

Navigation:

```nova
page Dashboard {
    navbar "Campus Store"
    sidebar "Admin"
    link "Products" to "/products"
    link "Orders" to "/orders"
}
```

Modals:

```nova
page Products {
    modal ProductDetails {
        title "Product Details"
    }
}
```

Use pages to create a useful first version of the frontend. After generation,
you can edit the Vue files directly.

## 8. Creating Backend Routes

Routes describe custom backend endpoints.

```nova
route GET "/api/products" {
    return Product.all()
}

route GET "/api/products/first" {
    return Product.first()
}
```

Routes can use simple runtime expressions:

```nova
route GET "/api/stats" {
    return {
        products: Product.count(),
        orders: Order.count()
    }
}
```

Use routes when the generated table endpoints are not enough.

## 9. Custom Project Architecture

Use an `architecture` block when the generated project needs extra folders or
starter files.

```nova
app CampusStore {
    project {
        frontend Vue
        backend Flask
        database SQLite

        architecture {
            folder app/models
            folder app/pages
            folder app/services
            folder app/components
            file Dockerfile
            file docker-compose.yml
        }
    }
}
```

You can also create typed files:

```nova
architecture {
    python app/services/pricing.py {
        "def apply_discount(price, percent):\n    return price * (1 - percent / 100)\n"
    }

    css app/components/store.css {
        ".price { font-weight: 700; }\n"
    }
}
```

Architecture blocks are useful for projects that need a specific layout before
developers continue customizing by hand.

## 10. Modules And Imports

For bigger apps, split the source into modules.

Example:

```txt
campus_store/
  Nova.toml
  app.nova
  database/
    Product.nova
    Order.nova
  pages/
    Dashboard.nova
    Products.nova
```

`app.nova`:

```nova
import database.*
import pages.*

app CampusStore {
    project {
        frontend Vue
        backend Flask
        database SQLite
    }
}
```

`database/Product.nova`:

```nova
table Product {
    id auto
    name text
    price money
    stock int
}

export Product
```

`pages/Products.nova`:

```nova
page Products {
    title "Products"
    table Product {
        columns name, price, stock
        actions view, edit, delete
    }
}

export Products
```

Modules keep the project readable as it grows.

## 11. Python, JavaScript, CSS, And SQL Custom Code

NovaDev can call safe Python helpers:

```nova
use Nova.math
use Nova.file

print(Nova.math.sqrt(81))
Nova.file.write("generated_notes/store.txt", "Store generated")
```

You can run a guarded Python block:

```nova
python {
    import math
    print(math.sqrt(144))
}
```

Keep unsafe Python disabled unless you know why you need it:

```nova
allow unsafe_python false
```

For generated projects, use `custom` blocks:

```nova
custom backend {
    python {
        def normalize_email(value):
            return value.strip().lower()
    }
}

custom frontend {
    js {
        export function formatCurrency(value) {
          return "$" + Number(value).toFixed(2)
        }
    }

    css {
        ".highlight { border-color: #22c55e; }\n"
    }
}

custom database {
    sql {
        CREATE INDEX idx_product_category ON Product(category);
    }
}
```

Generated locations:

```txt
backend/custom/custom_1.py
frontend/src/custom/custom_2.js
frontend/src/custom/custom_3.css
database/custom_4.sql
```

## 12. Plugins And Project Metadata

Plugins are recorded as project metadata.

```nova
app CampusStore {
    plugin AuthKit
    plugin StripeCheckout
    plugin AdminCharts
}
```

Generated docs include plugin information so developers know which capabilities
the app expects.

Local package metadata commands:

```bash
python nova.py install AuthKit
python nova.py update AuthKit
python nova.py remove AuthKit
```

The shell can run them too:

```txt
nova> .install AuthKit
nova> .remove AuthKit
```

## 13. Building And Running Generated Projects

Build everything:

```bash
python nova.py build-fullstack examples/apps/campus_store
```

Build only the frontend:

```bash
python nova.py build-vue examples/apps/campus_store
```

Build only the backend:

```bash
python nova.py build-backend examples/apps/campus_store --target Flask
```

Run generated Flask:

```bash
cd generated/campus-store/backend
python -m pip install -r requirements.txt
python app.py
```

Run generated Vue:

```bash
cd generated/campus-store/frontend
npm install
npm run dev
```

Inspect your language file:

```bash
python nova.py tokens examples/apps/campus_store
python nova.py ast examples/apps/campus_store --json
python nova.py lint examples/apps/campus_store
python nova.py docs examples/apps/campus_store
```

## 14. Recipes For Custom Projects

### E-Commerce Store

```nova
app StoreFront {
    project {
        frontend Vue
        backend Flask
        database SQLite
    }

    table Product {
        id auto
        name text
        description text
        category text
        price money
        stock int
    }

    table CartItem {
        id auto
        productName text
        price money
        quantity int
    }

    table Order {
        id auto
        customerName text
        email email
        address text
        total money
        status text
    }

    page Shop {
        title "Shop"
        card "Products" value "Product.count()"
        table Product {
            columns name, category, price, stock
            actions view, edit, delete
        }
    }

    page Checkout {
        title "Checkout"
        form Order {
            fields customerName, email, address
            submit "Place Order"
        }
    }
}
```

### CRM

```nova
app ClientDesk {
    project {
        frontend Vue
        backend Flask
        database SQLite
    }

    table Client {
        id auto
        name text
        email email
        company text
        status text
    }

    table Deal {
        id auto
        clientName text
        value money
        stage text
    }

    page Pipeline {
        title "Pipeline"
        card "Clients" value "Client.count()"
        card "Deals" value "Deal.count()"
        table Deal {
            columns clientName, value, stage
            actions view, edit
        }
    }
}
```

### School Dashboard

```nova
app SchoolHub {
    project {
        frontend Vue
        backend Flask
        database SQLite
    }

    table Student {
        id auto
        name text
        email email
        grade text
    }

    table Course {
        id auto
        title text
        teacher text
        room text
    }

    page Dashboard {
        title "School Dashboard"
        card "Students" value "Student.count()"
        card "Courses" value "Course.count()"
    }
}
```

### Security Scanner

```nova
app WebShield {
    project {
        frontend Vue
        backend Flask
        database SQLite
    }

    table Scan {
        id auto
        target text
        status text
        score int
        risk text
    }

    page Dashboard {
        title "WebShield Dashboard"
        card "Scans" value "Scan.count()"
        table Scan {
            columns target, status, score, risk
            actions view, delete
        }
    }
}
```

## 15. Developer Checklist

Before building:

- Choose `frontend`, `backend`, and `database` targets.
- Write tables for the real data.
- Write pages for the main user workflows.
- Add routes for custom backend behavior.
- Add architecture folders and files if your project needs a special layout.
- Add custom Python, JS, CSS, or SQL only when declarations are not enough.
- Run `lint`.
- Run `ast --json` if parsing looks wrong.

After building:

- Open the generated project folder.
- Run the backend.
- Run the frontend.
- Test the generated API endpoints.
- Edit generated files like normal project code.
- Keep the NovaDev source as your high-level project blueprint.

## 16. Troubleshooting

If a file does not parse, run:

```bash
python nova.py tokens path/to/project
python nova.py ast path/to/project --json
```

If a variable is missing:

```txt
Variable 'name' is not defined
```

Check that you declared it with `let`, imported the right module, or spelled the
name correctly.

If a generated app has no pages, run:

```bash
python nova.py lint path/to/project
```

If a module is missing, check `Nova.toml` and your import paths:

```nova
import database.*
import pages.*
```

If npm is not available, the backend can still be generated and run, but the Vue
frontend needs Node.js and npm installed.

## Final Idea

NovaDev is best used as a project blueprint language. Write the high-level shape
in `.nova`, generate the app, then continue customizing the real frontend and
backend files. That gives developers both speed and control.
