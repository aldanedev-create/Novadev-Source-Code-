# Custom Code

Custom code blocks let NovaDev projects keep hand-written source next to
high-level declarations.

```nova
app Store {
    custom backend {
        python {
            def discount(price, percent):
                return price * (1 - percent / 100)
        }
    }

    custom frontend {
        js {
            export function focusSearch() {
              document.querySelector("[data-search]")?.focus()
            }
        }

        css {
            ".featured { border-color: #22c55e; }\n"
        }
    }
}
```

Generated output locations:

- backend Python: `backend/custom/custom_1.py`
- frontend JavaScript: `frontend/src/custom/custom_2.js`
- frontend CSS: `frontend/src/custom/custom_3.css`
- SQL: `database/custom_4.sql`

At runtime, top-level `python { ... }` blocks can execute immediately. Project
custom code is mainly written into generated files.
