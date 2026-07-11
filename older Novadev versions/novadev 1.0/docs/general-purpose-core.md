# General-Purpose Core

NovaDev 1.0 has a small dynamic runtime for scripts and tools. The core language
is interpreted directly from the AST.

Supported basics:

- `let` variables and reassignment.
- Numbers, strings, booleans, nil/null, lists, objects, and tuples.
- Arithmetic and comparison operators: `+`, `-`, `*`, `/`, `==`, `!=`, `>`,
  `>=`, `<`, `<=`, `&&`, and `||`.
- `if`, `elif`, `else`, `while`, and `for`.
- `break`, `continue`, `return`, `try`, and `catch`.
- Functions, classes, methods, constructors, and inheritance.
- Built-in `print`.
- Standard helpers through `Nova.*`.

Example:

```nova
function subtotal(items) {
    let total = 0
    for item in items {
        total = total + item.price
    }
    return total
}

let cart = [
    { name: "Keyboard", price: 50 },
    { name: "Mouse", price: 25 }
]

print("Total: {subtotal(cart)}")
```

NovaDev is dynamically typed. A variable can hold any value, and clear runtime
errors are raised when a program reads a missing variable or calls something
that is not callable.
