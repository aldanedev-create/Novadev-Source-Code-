# Import System

NovaDev 0.5 supports local module imports.

```nova
import Product
import database.Product
import database.*
import pages.*
import database.Product as ProductModel
```

Package and remote imports parse too:

```nova
import "@nova/auth"
import "https://packages.novadev.dev/charts"
```

Prototype 0.5 records package imports but does not download remote code. The
compiler core stays Python-only and beginner-friendly.

Exports:

```nova
export Product
export default Dashboard
```

The resolver:

- Reads imported `.nova` files once.
- Merges imported AST nodes before run/build.
- Detects missing imports.
- Detects circular imports.
- Supports `Nova.toml` entry files when the CLI receives a folder path.

Example:

```bash
python nova.py build-fullstack examples/hello_modules
```
