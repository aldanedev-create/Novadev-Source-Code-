# Generated Projects

`build-fullstack` turns a NovaDev app into an editable project under
`generated/<app-slug>`.

Typical output:

```txt
generated/web-shield/
  Nova.toml
  README.md
  novadev.project.json
  docs/
  frontend/
  backend/
  app/
```

The generated backend has route files, model/data helpers, requirements, and a
run-ready app for the selected backend target. The generated frontend contains a
Vue/Vite project when `frontend Vue` is selected.

Run a generated Flask app:

```bash
cd generated/web-shield/backend
python -m pip install -r requirements.txt
python app.py
```

Run a generated Vue frontend:

```bash
cd generated/web-shield/frontend
npm install
npm run dev
```
