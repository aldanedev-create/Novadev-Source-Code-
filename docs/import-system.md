# Import System

NovaDev 1.0 supports local modules:

```nova
import database.*
import pages.Dashboard
import database.Product as ProductModel
```

Modules are resolved relative to the project root. A folder project should have
a `Nova.toml` file with an `entry` value:

```toml
entry = "app.nova"
```

The resolver records package-style imports separately and reports missing local
files or circular import chains with clear errors.
