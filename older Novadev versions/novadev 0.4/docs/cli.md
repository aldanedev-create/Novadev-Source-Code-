# CLI Reference

The CLI entry point is:

```powershell
python nova.py
```

Use `python3` instead of `python` if your system uses that command.

## Version

```powershell
python nova.py --version
```

Prints:

```txt
NovaDev 0.3.0
```

## Run

```powershell
python nova.py run examples\hello.nova
```

Runs a NovaDev file through the lexer, parser, interpreter, and runtime.

Useful for:

- `let`
- assignment
- `print`
- `if`
- `else`
- `while`
- `function`
- `return`

## Build UI

```powershell
python nova.py build-ui examples\business_admin.nova
```

Generates:

```txt
dist/index.html
dist/style.css
dist/app.js
```

Use a custom output folder:

```powershell
python nova.py build-ui examples\business_admin.nova -o my-dist
```

## Build Backend

```powershell
python nova.py build-backend examples\business_admin.nova
```

Generates:

```txt
generated_backend/app.py
generated_backend/models.py
generated_backend/routes.py
generated_backend/requirements.txt
```

Use a custom output folder:

```powershell
python nova.py build-backend examples\business_admin.nova -o my-backend
```

Point the Flask app at a custom frontend folder:

```powershell
python nova.py build-backend examples\business_admin.nova -o my-backend --frontend my-dist
```

## Build App

```powershell
python nova.py build-app examples\business_admin.nova
```

Generates the UI and Flask backend together:

```txt
dist/
generated_backend/
```

Run it:

```powershell
cd generated_backend
python -m pip install -r requirements.txt
python app.py
```

Open:

```txt
http://127.0.0.1:5000
```

Use custom output folders:

```powershell
python nova.py build-app examples\business_admin.nova --ui-output my-dist --backend-output my-backend
```

## Tokens

```powershell
python nova.py tokens examples\business_admin.nova
```

Prints lexer tokens with line and column numbers:

```txt
2:1    APP            app
2:5    IDENTIFIER     BusinessAdmin
2:19   LBRACE         {
```

## AST

```powershell
python nova.py ast examples\business_admin.nova
```

Prints the parsed AST as Python dataclasses.

JSON-friendly output:

```powershell
python nova.py ast examples\business_admin.nova --json
```

## Shell

```powershell
python nova.py shell
```

or:

```powershell
python shell.py
```

Starts:

```txt
NovaDev 0.3 Interactive Shell
Type .help for commands
Type .exit to quit
Finish multi-line blocks with a blank line
nova>
```

Shell commands:

```txt
.help
.version
.exit
.load examples/business_admin.nova
.run examples/hello.nova
.tokens examples/business_admin.nova
.ast examples/business_admin.nova --json
.build-ui examples/business_admin.nova
.build-backend examples/business_admin.nova
.build-app examples/business_admin.nova
```

`shell.py` can also run the same commands directly:

```powershell
python shell.py --version
python shell.py run examples\hello.nova
python shell.py tokens examples\business_admin.nova
python shell.py ast examples\business_admin.nova --json
python shell.py build-ui examples\business_admin.nova
python shell.py build-backend examples\business_admin.nova
python shell.py build-app examples\business_admin.nova
```

In other words, `nova.py` is the normal CLI, and `shell.py` can do the same work
either interactively or as a direct command runner.

You can also write programming code directly in the shell:

```txt
nova> let score = 8
nova> if score > 5 {
...     print("passed")
... } else {
...     print("try again")
... }
...
passed
```

The shell runs multi-line `if`, `while`, `function`, `app`, `page`, and other
brace blocks after you press a blank line with balanced braces.

## Exit Codes

```txt
0 = success
1 = lexer error, syntax error, runtime error, or missing file
```

## Removed 0.2 Commands

NovaDev 0.3 does not use the old `lint`, `inspect`, or `build` alias commands.
Use `tokens`, `ast`, `run`, `build-ui`, `build-backend`, and `build-app` instead.
