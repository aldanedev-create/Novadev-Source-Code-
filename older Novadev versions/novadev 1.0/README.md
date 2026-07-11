# NovaDev 1.0

NovaDev is a Python 3 programming language and project builder. It can run
normal programming code, load modules, call safe Python helpers, and generate
editable full-stack applications from high-level app declarations.

NovaDev 1.0 is intentionally small and beginner-friendly, but the core is
organized like a real language:
source code becomes tokens, tokens become AST nodes, and the runtime executes
or generates project files from the AST.

## Quick Start

Run a NovaDev script:

```bash
python nova.py run examples/scripts/math_tool.nova
```

Open the interactive shell:

```bash
python shell.py
```

Inside the shell:

```txt
NovaDev 1.0 Interactive Shell
Type .exit to quit
nova> let name = "Aldane"
nova> print("Hello {name}")
Hello Aldane
nova> .load examples/scripts/math_tool.nova
```

Build the WebShield full-stack app:

```bash
python nova.py build-fullstack examples/apps/webshield
```

Run the generated Flask backend:

```bash
cd generated/web-shield/backend
python -m pip install -r requirements.txt
python app.py
```

The backend serves APIs and the generated frontend project can be run with npm
from `generated/web-shield/frontend`.

## Language Example

```nova
use Nova.math

let numbers = [4, 9, 16]

for number in numbers {
    let root = Nova.math.sqrt(number)
    print("sqrt({number}) = {root}")
}

function total(items) {
    let result = 0
    for item in items {
        result = result + item
    }
    return result
}

if total(numbers) > 20 {
    print("Large cart")
} else {
    print("Small cart")
}
```

## Full-Stack App Example

```nova
import database.*
import pages.*

app WebShield {
    project {
        frontend Vue
        backend Flask
        database SQLite
        structure VueFlask

        architecture {
            folder app/models
            folder app/pages
            file Dockerfile
            python app/utils/FileTools.py {
                "def normalize_name(value):\n    return value.strip().lower()\n"
            }
        }
    }

    plugin AuthKit
    allow unsafe_python false

    table Scan {
        id auto
        target text
        risk text
        score number
    }

    page Dashboard {
        title "Security Dashboard"
        card "Open Scans" value "Scan.count()"
        table Scan {
            columns target, risk, score
            actions view, edit, delete
        }
    }
}
```

## CLI

```bash
python nova.py new my_app --frontend Vue --backend Flask --database SQLite
python nova.py run examples/scripts/math_tool.nova
python nova.py shell
python nova.py tokens examples/apps/webshield
python nova.py ast examples/apps/webshield --json
python nova.py lint examples/apps/webshield
python nova.py format examples/apps/webshield --check
python nova.py docs examples/apps/webshield
python nova.py build-ui examples/apps/webshield
python nova.py build-backend examples/apps/webshield
python nova.py build-fullstack examples/apps/webshield
python nova.py dev examples/apps/webshield
python nova.py clean generated/web-shield
```

The shell supports the same project commands with dot commands, such as
`.build-fullstack examples/apps/webshield`, `.tokens ...`, `.ast ...`,
`.lint ...`, and `.docs ...`.

## What NovaDev 1.0 Supports

- Variables with `let`, assignment, strings, numbers, booleans, nil, lists,
  objects, tuples, and interpolation.
- `if`, `elif`, `else`, `while`, `for`, `break`, `continue`, `try`, and `catch`.
- Functions, returns, classes, constructors, methods, and inheritance.
- Modules with `import`, `import folder.*`, aliases, exports, and `Nova.toml`.
- Safe Python bridge through `Nova.*` and `python { ... }` blocks.
- JavaScript/CSS/SQL/custom code blocks for generated projects.
- App declarations for tables, pages, routes, auth, themes, plugins, and
  project architecture.
- Vue frontend generation and Flask/FastAPI/Express/Django backend targets.

## Documentation

Start here:

- [Mini Book: Building Custom Projects](docs/mini-book-custom-projects.md)
- [Language Guide](docs/language-guide.md)
- [General-Purpose Core](docs/general-purpose-core.md)
- [Project Layer](docs/project-layer.md)
- [Python Bridge](docs/python-bridge.md)
- [JavaScript Escape Hatch](docs/javascript-escape-hatch.md)
- [Module System](docs/module-system.md)
- [Plugin System](docs/plugin-system.md)
- [File Structure System](docs/file-structure-system.md)
- [Stack Targets](docs/stack-targets.md)
- [Generated Projects](docs/generated-projects.md)
- [Custom Code](docs/custom-code.md)
- [CLI](docs/cli.md)
- [Examples](docs/examples.md)

NovaDev is designed for learning and for generating real editable starter apps.
Treat generated projects like normal application code: inspect them, run them,
and keep editing after generation.
