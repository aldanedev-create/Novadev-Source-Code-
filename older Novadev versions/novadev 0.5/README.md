# NovaDev Prototype 0.5

NovaDev is a Python 3 toy programming language prototype that can run simple
programs and generate editable full-stack projects.

Prototype 0.5 adds:

- Vue 3 + Vite project generation.
- Vue Router, Pinia, reusable Vue components, and fetch API services.
- Backend target selectors for Flask, FastAPI, Express, and Django.
- Project metadata blocks such as `project { frontend Vue backend Flask }`.
- Local module imports and exports across multiple `.nova` files.

## Quick Start

Run NovaDev code:

```bash
python nova.py run examples/python_features.nova
```

Build a Vue + Flask app:

```bash
python nova.py build-fullstack examples/vue_alchicken.nova
```

Run frontend:

```bash
cd generated/al-chicken/frontend
npm install
npm run dev
```

Run backend:

```bash
cd generated/al-chicken/backend
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5173.

## NovaDev 0.5 Syntax

```nova
app ALChicken {
    project {
        frontend Vue
        backend Flask
        database SQLite
        structure VueFlask
    }

    table Product {
        id auto
        name text
        price money
        stock int
    }

    page Products {
        title "Products"
        form Product {
            fields name, price, stock
            submit "Add Product"
        }
        table Product {
            columns name, price, stock
            actions view, edit, delete
        }
    }
}
```

## CLI

```bash
python nova.py run examples/python_features.nova
python nova.py shell
python nova.py tokens examples/vue_alchicken.nova
python nova.py ast examples/vue_alchicken.nova --json
python nova.py build-vue examples/vue_alchicken.nova
python nova.py build-backend examples/vue_alchicken.nova --target Flask
python nova.py build-fullstack examples/vue_alchicken.nova
python nova.py build examples/vue_alchicken.nova
```

## Shell

```bash
python shell.py
```

Inside the shell:

```txt
nova> let name = "Aldane"
nova> print("Hello {name}")
Hello Aldane
nova> .build-fullstack examples/vue_alchicken.nova
```

## Modules

NovaDev can split projects into files:

```nova
import database.*
import pages.*
import database.Product as ProductModel

export Product
export default Dashboard
```

Build a folder project with `Nova.toml`:

```bash
python nova.py build-fullstack examples/hello_modules
```

## Docs

- `docs/vue-generation.md`
- `docs/backend-targets.md`
- `docs/fullstack-projects.md`
- `docs/project-structure.md`
- `docs/import-system.md`
- `docs/modules.md`
- `docs/packages.md`

NovaDev is still a learning prototype, but the generated Vue, Flask, FastAPI,
Express, and Django starter code is normal editable project code.
