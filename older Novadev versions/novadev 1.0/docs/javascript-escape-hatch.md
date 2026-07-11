# JavaScript Escape Hatch

NovaDev can store JavaScript blocks for generated frontend projects. These
blocks are not executed by the NovaDev interpreter; they are copied into the
generated project as custom source files.

```nova
app Dashboard {
    custom frontend {
        js {
            export function formatCurrency(value) {
              return new Intl.NumberFormat("en-US", {
                style: "currency",
                currency: "USD"
              }).format(value)
            }
        }
    }
}
```

Use JavaScript custom code when a generated Vue app needs a small helper,
animation, browser API integration, or component-side behavior that should stay
as normal frontend code.
