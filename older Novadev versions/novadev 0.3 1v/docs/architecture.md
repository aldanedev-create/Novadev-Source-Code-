# Architecture

NovaDev 0.3 is organized like a small compiler and interpreter pipeline.

## High-Level Flow

```txt
.nova source
  -> lexer
  -> tokens
  -> parser
  -> AST
  -> interpreter
  -> runtime
```

For generated apps:

```txt
.nova source
  -> lexer
  -> parser
  -> AST declarations
  -> runtime registries
  -> UI generator / backend generator
  -> generated files
```

## Modules

```txt
nova.py
```

CLI entry point. Handles `run`, `build-ui`, `build-backend`, `tokens`, `ast`,
and `shell`.

```txt
shell.py
```

Interactive NovaDev shell. It keeps one interpreter alive so variables persist
between prompts.

```txt
novadev/lexer.py
```

Turns source text into tokens. It tracks line and column numbers for clearer
errors and supports comments, strings, numbers, booleans, nil/null, operators,
punctuation, identifiers, and keywords.

```txt
novadev/parser.py
```

Turns tokens into AST nodes with a recursive-descent parser. It parses normal
programming syntax and full-stack declarations.

```txt
novadev/ast_nodes.py
```

Dataclasses for the AST:

- `Program`
- `AppNode`
- `ThemeNode`
- `TableNode`
- `FieldNode`
- `AuthNode`
- `RouteNode`
- `PageNode`
- `ComponentNode`
- `FunctionNode`
- `IfNode`
- `WhileNode`
- `LetNode`
- `PrintNode`
- `ReturnNode`
- `BinaryOpNode`
- `LiteralNode`
- `IdentifierNode`
- `CallNode`

```txt
novadev/runtime.py
```

Stores variables in environments, executes statements, calls functions, handles
control flow, and keeps registries for apps, tables, pages, routes, themes, and
auth models.

```txt
novadev/interpreter.py
```

Small facade that connects lexer, parser, and runtime.

```txt
novadev/ui_generator.py
```

Generates the static admin dashboard:

```txt
dist/index.html
dist/style.css
dist/app.js
```

```txt
novadev/codegen.py
```

Generates starter backend files:

```txt
generated_backend/app.py
generated_backend/models.py
generated_backend/routes.py
```

## Beginner Wrapper Files

The project root also has `lexer.py`, `parser.py`, `ast_nodes.py`, `runtime.py`,
`interpreter.py`, `ui_generator.py`, and `codegen.py`. These are thin wrappers
that re-export the package modules, so a beginner can find the requested files
without digging through package structure.

## Tests

The compatibility test suite is in:

```txt
tests/test_novadev_v02.py
```

Run:

```powershell
python -B -m unittest discover -s tests
```
