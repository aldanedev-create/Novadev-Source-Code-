# Language Spec

NovaDev 1.0 source files are tokenized, parsed into AST nodes, and executed by a
dynamic runtime.

Core declarations:

- `app`, `project`, `theme`, `table`, `page`, `route`, and `auth`.
- `plugin`, `architecture`, `custom`, `python`, `js`, `css`, and `sql`.
- `import`, `export`, and `use`.

Core statements:

- `let name = value`
- `name = value`
- `print(value)`
- `return value`
- `if condition { ... } elif condition { ... } else { ... }`
- `while condition { ... }`
- `for item in items { ... }`
- `try { ... } catch error { ... }`
- `function name(args) { ... }`
- `class Name extends Parent { ... }`

Expressions support literals, identifiers, calls, lists, objects, tuples, unary
operators, binary operators, member access, and interpolation inside strings.

Strings support:

- double quotes: `"hello"`
- single quotes: `'hello'`
- triple double quotes for multi-line text: `"""..."""`
- triple single quotes for multi-line text: `'''...'''`

To protect accidental infinite loops, `while` loops are capped by the runtime.
