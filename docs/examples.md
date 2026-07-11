# NovaDev Examples

Use these files as starting points while learning NovaDev 1.1.

## NovaDev 1.1 ProjectIR Examples

These examples use multiple `.nova` files, imports, modes, workflows, page
types, and Nova-wrapped Python modules:

```bash
python nova.py validate examples/apps/ecommerce_1_1
python nova.py validate examples/apps/construction_1_1
python nova.py validate examples/apps/crm_1_1
python nova.py validate examples/apps/school_1_1
python nova.py validate examples/apps/church_custom_1_1
python nova.py validate examples/apps/gym_custom_1_1
python nova.py validate examples/apps/security_1_1
python nova.py validate examples/apps/booking_1_1
```

Inspect intent:

```bash
python nova.py ir examples/apps/ecommerce_1_1
python nova.py explain examples/apps/church_custom_1_1
```

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

Amazon Clone is the custom storefront example:

```bash
python nova.py build-fullstack "examples/apps/amazon clone"
```

It shows:

- an Amazon-style e-commerce storefront
- a custom Vue page written through NovaDev architecture
- imported custom frontend JavaScript
- imported custom CSS
- backend Python custom code
- SQL custom code

Construction Website is the larger multi-file website example:

```bash
python nova.py build-fullstack "examples/apps/construction website"
```

It shows:

- splitting a project across many `.nova` files
- importing models, pages, routes, modules, and website customizations
- backend Python modules wrapped inside NovaDev
- a custom generated Vue homepage
- custom frontend CSS and JavaScript
- generated Flask APIs for public website data

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
