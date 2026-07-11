# Project Layer

The project layer lets NovaDev describe application structure at a higher level
than normal code. The compiler reads declarations and generators turn them into
frontend, backend, database, and documentation files.

```nova
app BusinessAdmin {
    project {
        frontend Vue
        backend Flask
        database SQLite
        structure VueFlask
    }

    plugin AuthKit
    theme CyberDark { primary "#38bdf8" }

    table Product {
        id auto
        name text
        price money
    }

    route GET "/api/products" {
        return Product.all()
    }

    page Dashboard {
        title "Dashboard"
        card "Products" value "Product.count()"
        chart "Sales" type "line"
    }
}
```

Project declarations are metadata at runtime and input for generators at build
time. They do not replace real code; they create a starting application that can
be edited like any other generated project.
