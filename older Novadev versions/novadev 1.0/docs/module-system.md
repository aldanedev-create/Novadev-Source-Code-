# Module System

NovaDev projects can be split across files with `import` and `export`.

```nova
import database.*
import pages.*
import database.Product as ProductModel

export Product
export default Dashboard
```

Common project layout:

```txt
my_app/
  Nova.toml
  app.nova
  database/
    Product.nova
  pages/
    Dashboard.nova
```

`Nova.toml` tells NovaDev which file starts the project:

```toml
name = "MyApp"
version = "1.0"
entry = "app.nova"
frontend = "Vue"
backend = "Flask"
database = "SQLite"
```

The resolver parses imported files once, merges declarations, reports missing
modules, and catches simple circular imports.
