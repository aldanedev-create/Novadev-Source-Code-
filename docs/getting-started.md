# Getting Started

NovaDev 1.0 can be used as a scripting language, an interactive shell, and a
full-stack project generator.

## Run A Script

```bash
python nova.py run examples/scripts/math_tool.nova
```

## Use The Shell

```bash
python shell.py
```

```txt
nova> let name = "Aldane"
nova> print("Hello {name}")
Hello Aldane
nova> .load examples/scripts/oop_demo.nova
```

## Create A Project

```bash
python nova.py new examples/apps/my_store --frontend Vue --backend Flask --database SQLite
```

This creates:

```txt
examples/apps/my_store/
  Nova.toml
  app.nova
```

## Build A Full-Stack App

```bash
python nova.py build-fullstack examples/apps/webshield
```

Run the generated Flask backend:

```bash
cd generated/web-shield/backend
python -m pip install -r requirements.txt
python app.py
```

Run the generated Vue frontend:

```bash
cd generated/web-shield/frontend
npm install
npm run dev
```

## Inspect Source

```bash
python nova.py tokens examples/apps/webshield
python nova.py ast examples/apps/webshield --json
python nova.py lint examples/apps/webshield
python nova.py docs examples/apps/webshield
```
