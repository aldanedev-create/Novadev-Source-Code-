# Full-Stack Projects

Build a full Vue + backend project:

```bash
python nova.py build-fullstack examples/vue_alchicken.nova
```

`python nova.py build ...` does the same target-aware generation.

Generated structure:

```txt
generated/al-chicken/
  README.md
  frontend/
    package.json
    vite.config.js
    src/
  backend/
    app.py
    models.py
    routes.py
    config.py
    requirements.txt
```

The source controls the target:

```nova
app ALChicken {
    project {
        frontend Vue
        backend Flask
        database SQLite
        structure VueFlask
    }
}
```

The compiler reads one `.nova` file, resolves imports, builds an AST, and sends
the result into the project, frontend, backend, documentation, and filesystem
generators.
