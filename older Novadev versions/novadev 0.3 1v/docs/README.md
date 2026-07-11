# NovaDev 0.3 Documentation

NovaDev 0.3 is a Python-based toy programming language prototype. It can run
small programs and generate starter full-stack app files from readable `.nova`
source.

Start here:

- [Getting Started](getting-started.md)
- [Language Spec](language-spec.md)
- [Examples](examples.md)
- [CLI Reference](cli.md)
- [UI System](ui-system.md)
- [Architecture](architecture.md)
- [Roadmap](roadmap.md)

## What NovaDev 0.3 Can Do

- Tokenize source code with a real lexer
- Parse tokens into AST node objects
- Run variables, assignment, `print`, `if`, `else`, `while`, `function`, and `return`
- Store runtime variables in an environment
- Register apps, tables, pages, routes, themes, and auth models
- Generate a static admin dashboard into `dist/`
- Generate starter backend files into `generated_backend/`
- Run an interactive shell with `.load` support

## Learning Path

1. Read [Getting Started](getting-started.md).
2. Run `python nova.py run examples\hello.nova`.
3. Try the shell with `python nova.py shell`.
4. Read [Examples](examples.md) and copy snippets into `.nova` files.
5. Build the dashboard with `python nova.py build-ui examples\business_admin.nova`.
6. Inspect tokens and AST output when you want to understand how the language works.

## Prototype Limits

NovaDev 0.3 is still a toy language prototype. The generated UI is static and
uses local browser data. The generated backend is a starter Python standard
library app, not a production database-backed service.
