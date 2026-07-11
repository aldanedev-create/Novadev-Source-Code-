# Getting Started

This guide shows how to run NovaDev programs, use the shell, inspect language
internals, and generate app files.

## 1. Open The Project

From PowerShell:

```powershell
cd "C:\Users\aldan\Downloads\novadev 0.2"
```

The folder name still says `0.2`, but the code inside is NovaDev 0.3.

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
Type .help for commands
Type .exit to quit
Finish multi-line blocks with a blank line
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

Run `if/else` directly in the shell:

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

The blank line after the closing brace tells the shell to run the completed
block.

Run a loop:

```txt
nova> let x = 0
nova> while x < 3 {
...     print("loop " + x)
...     x = x + 1
... }
...
loop 0
loop 1
loop 2
```

Define and call a function:

```txt
nova> function greet(name) {
...     return "Hello " + name
... }
...
nova> print(greet("Aldane"))
Hello Aldane
```

The shell can also do the same jobs as `nova.py`:

```txt
nova> .version
nova> .run examples/hello.nova
nova> .tokens examples/business_admin.nova
nova> .ast examples/business_admin.nova --json
nova> .build-ui examples/business_admin.nova
nova> .build-backend examples/business_admin.nova
```

You can also call those commands directly through `shell.py`:

```powershell
python shell.py run examples\hello.nova
python shell.py tokens examples\business_admin.nova
python shell.py ast examples\business_admin.nova --json
python shell.py build-ui examples\business_admin.nova
python shell.py build-backend examples\business_admin.nova
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

When opened directly from disk, the UI uses local sample data. When served by
the generated Flask app, it calls the backend API.

## 8. Build UI And Flask Backend Together

```powershell
python nova.py build-app examples\business_admin.nova
```

NovaDev writes:

```txt
dist/index.html
dist/style.css
dist/app.js
generated_backend/app.py
generated_backend/models.py
generated_backend/routes.py
generated_backend/requirements.txt
```

Run the Flask app:

```powershell
cd generated_backend
python -m pip install -r requirements.txt
python app.py
```

Open:

```txt
http://127.0.0.1:5000
```

The browser UI and backend now work together:

- tables load rows from Flask API endpoints
- forms create rows with POST requests
- edit and delete actions call backend endpoints
- the Flask app serves `index.html`, `style.css`, and `app.js`

## 9. Build Only Backend Files

```powershell
python nova.py build-backend examples\business_admin.nova
```

NovaDev writes:

```txt
generated_backend/app.py
generated_backend/models.py
generated_backend/routes.py
generated_backend/requirements.txt
```

Run the generated backend after building the UI:

```powershell
cd generated_backend
python -m pip install -r requirements.txt
python app.py
```

Then open a generated route such as:

```txt
http://127.0.0.1:5000/api/products
```

## 10. Create Your Own File

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
python nova.py build-app examples\my_app.nova
```
