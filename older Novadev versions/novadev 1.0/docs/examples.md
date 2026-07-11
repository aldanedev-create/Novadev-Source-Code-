# NovaDev Examples

Use these files as starting points while learning NovaDev 1.0.

## Script Examples

```bash
python nova.py run examples/scripts/math_tool.nova
python nova.py run examples/scripts/file_tool.nova
python nova.py run examples/scripts/automation_tool.nova
python nova.py run examples/scripts/oop_demo.nova
```

What they show:

- `math_tool.nova`: `Nova.math`, `Nova.statistics`, lists, tuples, loops, and a
  safe Python block.
- `file_tool.nova`: `Nova.file.write` and `Nova.file.read`.
- `automation_tool.nova`: loops and `try/catch`.
- `oop_demo.nova`: classes, constructors, methods, and inheritance.

## Shell Examples

```bash
python shell.py
```

```txt
nova> let name = "Aldane"
nova> print(name)
Aldane
nova> .load examples/scripts/oop_demo.nova
Hello Aldane
admin
```

The shell also runs project commands:

```txt
nova> .tokens examples/apps/webshield
nova> .ast examples/apps/webshield --json
nova> .build-fullstack examples/apps/webshield
```

## App Example

WebShield is the main NovaDev 1.0 full-stack example:

```bash
python nova.py build-fullstack examples/apps/webshield
```

It shows:

- `Nova.toml`
- folder modules
- `import database.*`
- `import pages.*`
- tables, pages, routes, plugins, architecture, and custom code
- Vue frontend generation
- Flask backend generation

## Module Examples

```bash
python nova.py ast examples/modules/import_demo --json
python nova.py run examples/modules/python_bridge_demo/app.nova
python nova.py build-fullstack examples/modules/plugin_demo/app.nova
```

These examples show local imports, package-style imports, plugin metadata, and
Python bridge usage.

## Create Your Own App

```bash
python nova.py new examples/apps/my_store --frontend Vue --backend Flask --database SQLite
python nova.py build-fullstack examples/apps/my_store
```
