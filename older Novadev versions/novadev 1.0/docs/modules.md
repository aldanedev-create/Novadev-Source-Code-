# Modules

A NovaDev module is a `.nova` file containing tables, pages, routes, functions,
classes, components, themes, or services.

Example project:

```txt
hello_modules/
  Nova.toml
  app.nova
  database/Product.nova
  pages/Products.nova
```

`app.nova`:

```nova
import database.*
import pages.*

app HelloModules {
    project {
        frontend Vue
        backend Flask
        database SQLite
        structure VueFlask
    }
}
```

The compiler combines all imported modules into one AST before execution or
generation.
