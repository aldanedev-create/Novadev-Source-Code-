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
```

Use a custom output folder:

```powershell
python nova.py build-backend examples\business_admin.nova -o my-backend
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

Starts:

```txt
NovaDev 0.3 Interactive Shell
Type .exit to quit
nova>
```

Shell commands:

```txt
.exit
.load examples/business_admin.nova
```

## Exit Codes

```txt
0 = success
1 = lexer error, syntax error, runtime error, or missing file
```

## Removed 0.2 Commands

NovaDev 0.3 does not use the old `lint`, `inspect`, or `build` alias commands.
Use `tokens`, `ast`, `run`, `build-ui`, and `build-backend` instead.
