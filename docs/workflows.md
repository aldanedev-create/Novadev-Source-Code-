# Workflows

Workflows describe project-specific backend behavior.

```nova
workflow Checkout {
    input CartItem
    uses CartMath.calculate_total
    creates Order
    clears CartItem
    validates stock
}
```

When a workflow uses a Python module, NovaDev writes the module to the generated
backend and appends a workflow route hook:

```txt
POST /api/workflows/checkout
```

The generated route imports and calls the exported Python function.
