# Getting Started

This guide shows how to run NovaDev programs, use the shell, inspect language
internals, and generate app files.

## 1. Open The Project

From PowerShell:

```powershell
cd "C:\Users\aldan\Downloads\novadev 0.2"
```

## 2. Run Hello World

```powershell
python nova.py run examples\hello.nova
```

Expected output:

```txt
Hello Aldane
15
```

The source file:

```nova
let name = "Aldane"
print("Hello " + name)

let score = 10
print(score + 5)
```

## 3. Try The Interactive Shell

```powershell
python nova.py shell
```

or:

```powershell
python shell.py
```

You should see:

```txt
NovaDev 0.3 Interactive Shell
Type .exit to quit
nova>
```

Try:

```txt
nova> let name = "Aldane"
nova> print(name)
Aldane
nova> .exit
```

Load a file from the shell:

```txt
nova> .load examples/business_admin.nova
```

## 4. Run Control Flow

```powershell
python nova.py run examples\control_flow.nova
```

This demonstrates `while`, `if`, `else`, functions, and `return`.

## 5. Inspect Tokens

Tokens are the output of the lexer.

```powershell
python nova.py tokens examples\business_admin.nova
```

You will see rows like:

```txt
2:1    APP            app
2:5    IDENTIFIER     BusinessAdmin
2:19   LBRACE         {
```

## 6. Inspect The AST

The AST is the parser output.

```powershell
python nova.py ast examples\business_admin.nova
```

For JSON output:

```powershell
python nova.py ast examples\business_admin.nova --json
```

## 7. Build The UI

```powershell
python nova.py build-ui examples\business_admin.nova
```

NovaDev writes:

```txt
dist/index.html
dist/style.css
dist/app.js
```

Open `dist/index.html` in a browser.

## 8. Build Backend Starter Files

```powershell
python nova.py build-backend examples\business_admin.nova
```

NovaDev writes:

```txt
generated_backend/app.py
generated_backend/models.py
generated_backend/routes.py
```

Run the generated backend:

```powershell
cd generated_backend
python app.py
```

Then open a generated route such as:

```txt
http://127.0.0.1:8000/api/products
```

## 9. Create Your Own File

Create `examples\my_app.nova`:

```nova
app ProductDesk {
    table Product {
        id auto
        name text
        price money
        stock int
    }

    page Products {
        title "Products"

        card "Total Products" {
            value Product.count()
        }

        form Product {
            fields name, price, stock
            submit "Add Product"
        }

        table Product {
            columns name, price, stock
            actions view, delete
        }
    }

    route GET "/api/products" {
        return Product.all()
    }
}
```

Build it:

```powershell
python nova.py build-ui examples\my_app.nova
```
