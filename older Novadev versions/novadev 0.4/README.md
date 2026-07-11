# NovaDev Prototype 0.4

NovaDev is a toy programming language prototype written in Python 3. It teaches
how languages work while also generating small Flask web apps from high-level
NovaDev source files.

The language pipeline is:

```txt
source code -> lexer -> tokens -> parser -> AST -> runtime/interpreter
```

Prototype 0.4 adds Python-like programming features, a safe `Nova.*` bridge to
use selected Python standard-library modules, and a full project builder for
Flask + browser apps.

## Quick Start

Run NovaDev code:

```bash
python nova.py run examples/python_features.nova
```

Start the interactive shell:

```bash
python shell.py
```

Build the e-commerce app:

```bash
python nova.py build examples/alchicken_app.nova
cd generated/al-chicken-store/backend
python -m pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

## Shell

The shell can run normal NovaDev code and every command from `nova.py`.

```txt
NovaDev 0.4 Interactive Shell
Type .help for commands
Type .exit to quit
nova> let name = "Aldane"
nova> print("Hello {name}")
Hello Aldane
```

Shell commands:

```txt
nova> .run examples/python_features.nova
nova> .load examples/alchicken_app.nova
nova> .tokens examples/alchicken_app.nova
nova> .ast examples/alchicken_app.nova --json
nova> .build examples/alchicken_app.nova
nova> .build-ui examples/business_admin.nova
nova> .build-backend examples/business_admin.nova
nova> .build-app examples/business_admin.nova
```

Multi-line code works too. Press a blank line after the closing brace:

```txt
nova> let x = 10
nova> if x > 5 {
...     print("big")
... } else {
...     print("small")
... }
...
big
```

## Language Examples

Variables, strings, and interpolation:

```nova
let name = "Aldane"
print("Hello {name}")
```

Lists:

```nova
let items = ["keyboard", "mouse"]
items.add("monitor")
print(items.length())

for item in items {
    print(item)
}
```

Objects and dot access:

```nova
let user = {
    name: "Mira",
    role: "Admin"
}
user.email = "mira@example.com"
print(user.email)
```

Control flow:

```nova
if score >= 90 {
    print("excellent")
} elif score >= 80 {
    print("good")
} else {
    print("keep practicing")
}

while count < 10 {
    count = count + 1
}
```

Functions and classes:

```nova
function discount(price) {
    return price * 0.9
}

class Customer {
    function init(name) {
        self.name = name
    }

    function label() {
        return "Customer {self.name}"
    }
}
```

Safe Python bridge:

```nova
let root = Nova.math.sqrt(81)
let id = Nova.uuid.uuid4()
Nova.files.write("generated_notes/id.txt", id)
```

## Full-Stack App Example

NovaDev can describe a small e-commerce app:

```nova
app ALChickenStore {
    stack JQueryFlask
    database sqlite

    table Product {
        id auto
        name text
        description text
        price money
        stock number
    }

    page Storefront {
        title "ALChicken Store"
        catalog Product {
            fields name description price stock
            actions add_to_cart
        }
    }
}
```

Build it:

```bash
python nova.py build examples/alchicken_app.nova
```

Output:

```txt
generated/al-chicken-store/frontend/index.html
generated/al-chicken-store/frontend/css/style.css
generated/al-chicken-store/frontend/js/app.js
generated/al-chicken-store/backend/app.py
generated/al-chicken-store/backend/models.py
generated/al-chicken-store/backend/routes.py
generated/al-chicken-store/backend/requirements.txt
```

The Flask backend serves the generated frontend and exposes API endpoints for the
declared tables.

## CLI Commands

```bash
python nova.py run examples/python_features.nova
python nova.py shell
python nova.py tokens examples/alchicken_app.nova
python nova.py ast examples/alchicken_app.nova --json
python nova.py build examples/alchicken_app.nova
python nova.py build-ui examples/business_admin.nova
python nova.py build-backend examples/business_admin.nova
python nova.py build-app examples/business_admin.nova
```

## Project Files

```txt
nova.py                       command-line interface
shell.py                      interactive shell
novadev/lexer.py              source code -> tokens
novadev/parser.py             tokens -> AST nodes
novadev/ast_nodes.py          AST dataclasses
novadev/runtime.py            variables, functions, classes, control flow
novadev/interpreter.py        lexer + parser + runtime facade
novadev/nova_modules.py       safe Nova.* Python bridge
novadev/frontend_generator.py frontend project generator
novadev/backend_generator.py  Flask backend generator wrapper
novadev/project_generator.py  full app generator
novadev/errors.py             beginner-friendly error classes
examples/                     runnable NovaDev examples
novadev/docs/                 0.4 language docs
```

## How It Works

The lexer creates tokens such as `LET`, `IDENTIFIER`, `STRING`, and `LBRACE`.
The parser turns those tokens into AST nodes such as `LetNode`, `IfNode`, and
`AppNode`. The runtime walks the AST, stores variables in an environment, calls
functions, handles loops, and registers app/table/page declarations for the
generators.

NovaDev is a learning prototype, not production-ready, but its pieces are shaped
like a real language implementation.
