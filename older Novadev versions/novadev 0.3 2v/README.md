# NovaDev Prototype 0.3

NovaDev is a toy programming language prototype written in Python 3. It is built
to show the same core pipeline used by bigger languages:

```txt
source code -> lexer -> tokens -> parser -> AST -> interpreter/runtime
```

NovaDev 0.3 can run small programs and describe a simple full-stack admin app in
one `.nova` file. It is beginner-friendly and intentionally not production-ready,
but the pieces are organized like a real language project.

## Project Files

```txt
lexer.py                  beginner wrapper for novadev/lexer.py
parser.py                 beginner wrapper for novadev/parser.py
ast_nodes.py              beginner wrapper for novadev/ast_nodes.py
runtime.py                beginner wrapper for novadev/runtime.py
interpreter.py            beginner wrapper for novadev/interpreter.py
ui_generator.py           beginner wrapper for novadev/ui_generator.py
codegen.py                beginner wrapper for the Flask backend generator
shell.py                  interactive shell plus command runner
nova.py                   command-line tool
examples/                 sample NovaDev programs
novadev/                  main Python package
```

## How The Lexer Works

The lexer reads raw NovaDev text one character at a time and creates tokens.

Example:

```nova
let name = "Aldane"
```

becomes tokens like:

```txt
LET IDENTIFIER EQUAL STRING
```

The lexer supports identifiers, strings, numbers, booleans, nil/null, operators,
punctuation, comments, and NovaDev keywords such as `app`, `table`, `page`,
`if`, `while`, `function`, `let`, and `print`.

Inspect tokens with:

```bash
python3 nova.py tokens examples/business_admin.nova
```

## How The Parser Works

The parser reads tokens and builds AST nodes. It supports full-stack declarations:

```nova
app BusinessAdmin {
    table Product {
        id auto
        name text
        price money
    }

    page Dashboard {
        card "Products" {
            value Product.count()
        }
    }

    route GET "/api/products" {
        return Product.all()
    }
}
```

It also supports normal programming syntax:

```nova
let x = 10
print("Hello")
if x > 5 { print("Big") }
while x < 10 { x = x + 1 }
```

Inspect the AST with:

```bash
python3 nova.py ast examples/business_admin.nova
```

## How The AST Works

The AST is a tree of Python dataclasses. Important nodes include:

`Program`, `AppNode`, `ThemeNode`, `TableNode`, `FieldNode`, `AuthNode`,
`RouteNode`, `PageNode`, `ComponentNode`, `FunctionNode`, `IfNode`, `WhileNode`,
`LetNode`, `PrintNode`, `ReturnNode`, `BinaryOpNode`, `LiteralNode`,
`IdentifierNode`, and `CallNode`.

This means the interpreter does not execute text directly. It walks structured
objects that describe the program.

## How The Interpreter Works

`interpreter.py` connects the lexer, parser, and runtime:

```txt
source -> Lexer -> Parser -> Runtime
```

Run a file with:

```bash
python3 nova.py run examples/hello.nova
```

## How The Runtime Works

The runtime stores variables in an environment and executes:

- `let`
- assignment
- `print`
- `if`
- `while`
- `function`
- `return`
- function calls

It also keeps registries for apps, tables, pages, routes, themes, and auth
models. Generators use those registries to create frontend and backend starter
files.

## Interactive Shell

Start the shell with:

```bash
python3 shell.py
```

or:

```bash
python3 nova.py shell
```

You will see:

```txt
NovaDev 0.3 Interactive Shell
Type .help for commands
Type .exit to quit
Finish multi-line blocks with a blank line
nova>
```

Example:

```txt
nova> let name = "Aldane"
nova> print(name)
Aldane
```

Load a file:

```txt
nova> .load examples/business_admin.nova
```

Multi-line programming works too. Press a blank line after the closing brace to
run the block:

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

Functions work the same way:

```txt
nova> function greet(name) {
...     return "Hello " + name
... }
...
nova> print(greet("Aldane"))
Hello Aldane
```

Everything available in `nova.py` is also available from `shell.py`.

Interactive shell commands:

```txt
nova> .version
nova> .run examples/hello.nova
nova> .tokens examples/business_admin.nova
nova> .ast examples/business_admin.nova --json
nova> .build-ui examples/business_admin.nova
nova> .build-backend examples/business_admin.nova
```

Direct `shell.py` commands:

```bash
python3 shell.py run examples/hello.nova
python3 shell.py tokens examples/business_admin.nova
python3 shell.py ast examples/business_admin.nova --json
python3 shell.py build-ui examples/business_admin.nova
python3 shell.py build-backend examples/business_admin.nova
```

## How The UI Generator Works

`ui_generator.py` reads page, table, card, chart, form, sidebar, navbar, and modal
declarations. It creates a browser dashboard:

```bash
python3 nova.py build-ui examples/business_admin.nova
```

Output:

```txt
dist/index.html
dist/style.css
dist/app.js
```

Open `dist/index.html` in a browser to try the dashboard.

## Flask App Generation

Build the UI and Flask backend together:

```bash
python3 nova.py build-app examples/business_admin.nova
```

Output:

```txt
dist/index.html
dist/style.css
dist/app.js
generated_backend/app.py
generated_backend/models.py
generated_backend/routes.py
generated_backend/requirements.txt
```

Run the app:

```bash
cd generated_backend
python3 -m pip install -r requirements.txt
python3 app.py
```

Open:

```txt
http://127.0.0.1:5000
```

The Flask app serves the UI and APIs together. Forms POST to `/api/products`,
tables load rows from `/api/products`, and actions like edit/delete call the
backend.

An e-commerce example is included:

```bash
python3 nova.py build-app examples/ecommerce_store.nova --ui-output dist_ecommerce --backend-output generated_backend_ecommerce
cd generated_backend_ecommerce
python3 -m pip install -r requirements.txt
python3 app.py
```

It includes product catalog, cart, checkout, orders, order items, inventory
stock decrementing, and admin product management.

You can still generate only the backend:

```bash
python3 nova.py build-backend examples/business_admin.nova
```

Output:

```txt
generated_backend/app.py
generated_backend/models.py
generated_backend/routes.py
generated_backend/requirements.txt
```

## Prototype 0.3 Checklist

NovaDev 0.3 includes:

- token-based lexer
- recursive-descent parser
- AST node classes
- runtime environment
- interpreter
- interactive shell
- CLI and shell commands for run, build-ui, build-backend, build-app, tokens, ast, and shell
- generated admin dashboard files
- Flask backend generator
- beginner-friendly examples

This is still a toy language prototype, but it now follows the same core shape
as production language tools: lexing, parsing, AST construction, interpretation,
runtime state, and code generation.
