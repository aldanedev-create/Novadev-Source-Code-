# NovaDev 0.3 Language Spec

This document describes the syntax supported by the NovaDev 0.3 prototype.

## Comments

NovaDev supports line comments:

```nova
# comment
// comment
```

## Values

NovaDev has simple dynamic values:

```nova
"text"
123
12.5
true
false
nil
null
```

`nil` and `null` both mean no value.

## Variables

Declare a variable with `let`:

```nova
let name = "Aldane"
let count = 3
```

Assign to an existing variable:

```nova
count = count + 1
```

Reading a missing variable raises a clear runtime error.

## Print

```nova
print("Hello")
print(name)
print("Count: " + count)
```

When `+` touches a string, NovaDev joins values as text.

## Operators

Supported operators:

```txt
+ - * /
== != > >= < <=
&& ||
=
```

Examples:

```nova
let total = 10 + 5 * 2
let big = total > 20
let allowed = true && big
```

## If And Else

```nova
let score = 9

if score > 5 {
    print("Big")
} else {
    print("Small")
}
```

## While

```nova
let x = 0

while x < 3 {
    print(x)
    x = x + 1
}
```

Loops are stopped after 10000 iterations to protect the prototype from accidental
infinite loops.

## Functions

```nova
function greet(name) {
    return "Hello " + name
}

print(greet("Aldane"))
```

Functions can read outer variables through the runtime environment.

## App

An app groups tables, auth, routes, themes, and pages:

```nova
app BusinessAdmin {
    table Product {
        id auto
        name text
    }

    page Dashboard {
        title "Dashboard"
    }
}
```

Top-level declarations are also allowed. If a file has top-level `table`, `page`,
`route`, `theme`, or `auth` declarations, NovaDev registers them under a default
app named `NovaDevApp`.

## Tables

Tables describe data models:

```nova
table Product {
    id auto
    name text
    email email unique
    price money
    active boolean
}
```

Common field kinds:

```txt
auto
text
email
secure
password
int
number
money
currency
date
datetime
bool
boolean
markdown
```

Supported field attributes:

```txt
unique
auto
secure
```

## Auth

Auth points to a table:

```nova
auth User
```

Pages and routes can require auth or a role:

```nova
require auth
require role Admin
```

## Themes

Themes define visual tokens for generated CSS:

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

## Routes

Routes describe API behavior for backend generation:

```nova
route GET "/api/products" {
    require role Admin
    return Product.all()
}

route GET "/api/products/count" {
    require auth
    return Product.count()
}
```

Supported route methods:

```txt
GET
POST
PUT
PATCH
DELETE
```

The current backend generator understands `Table.all()` and `Table.count()`.
Other return expressions are emitted as starter placeholder results.

## Pages

Pages create generated UI routes:

```nova
page Dashboard {
    require role Admin
    title "Business Dashboard"
}
```

Page names become routes:

```txt
Dashboard -> /dashboard
AdminDashboard -> /admin-dashboard
```

## Sidebar And Navbar

```nova
sidebar {
    link "Dashboard" to "/dashboard"
    link "Products" to "/products"
}

navbar {
    link "Products" to "/products"
}
```

## Cards

```nova
card "Products" {
    value Product.count()
}
```

Supported generated card expressions:

```txt
Table.count()
Table.sum(field)
```

## Forms

```nova
form Product {
    fields name, price, stock
    submit "Add Product"
}
```

Forms are generated from table fields.

## Table Views

```nova
table Product {
    columns name, price, stock
    actions view, edit, delete
}
```

Inside a `page`, `table Product { ... }` creates a table UI. Inside an `app`,
`table Product { ... }` creates a data model. The parser knows which meaning to
use from context.

## Charts

```nova
chart Order {
    type bar
    x customer
    y total
}
```

The generated UI draws simple canvas charts.

## Buttons

```nova
button "Add Product"
button "Open Products" to "/products"
```

## Modals

```nova
modal "Product Help" {
    text "Use this page to add and inspect products."
    button "Got it"
}
```

## Punctuation

Supported punctuation:

```txt
( ) { } [ ] , . :
```

`[` and `]` are tokenized for language growth, but array literals are not
implemented yet.

## Simplified Grammar

```txt
program        = statement*
statement      = declaration | let | assignment | print | if | while | return | expression
declaration    = app | table | page | route | theme | auth | use_theme | function
app            = "app" identifier "{" statement* "}"
table          = "table" identifier "{" field* "}"
field          = identifier field_kind attribute*
page           = "page" identifier "{" page_item* "}"
route          = "route" method string "{" route_statement* "}"
theme          = "theme" identifier "{" theme_entry* "}"
function       = "function" identifier "(" params? ")" block
block          = "{" statement* "}"
expression     = logical_or
```
