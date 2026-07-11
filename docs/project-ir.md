# ProjectIR

ProjectIR is NovaDev 1.1's internal project plan.

The AST answers:

```txt
What did the developer write?
```

ProjectIR answers:

```txt
What kind of project is this, and what code should exist?
```

It records:

- app name
- mode
- frontend/backend/database
- styling system and style profile
- entities/tables
- pages and page types
- workflows
- modules
- custom code
- routes
- plugins

For Vue projects, ProjectIR includes Tailwind styling data:

```json
{
  "styling": "Tailwind",
  "style": {
    "mode": "ecommerce",
    "primary": "#f59e0b",
    "accent": "#111827",
    "surface": "#fff7ed",
    "radius": "small",
    "density": "compact"
  }
}
```

The Vue generator uses this data to write `tailwind.config.js`, CSS variables,
and project-specific component classes.

Inspect it:

```bash
python nova.py ir examples/apps/construction_1_1
```
