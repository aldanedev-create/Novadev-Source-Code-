# Project-Specific Generation

NovaDev 1.1 generates from project intent instead of only copying generic
templates.

Pipeline:

```txt
.nova source -> lexer -> parser -> AST -> semantic analyzer -> ProjectIR -> generator
```

The generator uses `mode`, page types, workflows, tables, modules, and custom
code to decide what should be written. `mode custom` is strict: it does not add
e-commerce, construction, CRM, school, or other domain defaults.

## What Is Shared

NovaDev still writes normal framework foundation code:

- Vue app bootstrapping
- Vue Router setup
- Pinia store setup
- fetch-based API helpers
- Flask app setup
- generic CRUD routes for declared tables

That shared code is expected. It is the runtime foundation every generated app
needs.

## What Is Project-Specific

NovaDev now compiles project behavior from ProjectIR:

- `hero` declarations become generated hero blocks.
- `section Name from Table` becomes a record section for that table.
- `catalog Product` becomes a product catalog and only gets add-to-cart behavior
  when a cart table exists.
- `form Entity` submits through a matching workflow when one is declared.
- `estimator Module.function` calls the workflow that uses that Python module.
- `type pipeline` can render stage-based pipeline boards.
- workflow endpoints call generated backend Python modules from that project.
- ecommerce checkout routes are generated only for declared ecommerce checkout
  apps, not for every project.
- Vue styling is generated from ProjectIR style profiles, so `mode ecommerce`,
  `mode construction`, and `mode custom` do not need to share the same visual
  `main.css`.

## Tailwind Styling

For Vue projects, NovaDev prefers:

```nova
project {
    styling Tailwind
}
```

The compiler writes Tailwind config files and a generated `main.css` using
Tailwind directives, CSS variables, and mode-specific `@apply` rules. Tailwind is
the utility engine; ProjectIR decides which profile/classes/tokens to generate.

## Custom Mode Rule

With:

```nova
app ChurchMediaSystem {
    project {
        mode custom
    }
}
```

NovaDev does not infer carts, checkout, construction estimators, CRM pipelines,
or school attendance. If the developer declares sermons and prayer requests, the
generated project contains sermons and prayer requests.

## Workflow Example

```nova
workflow SubmitPrayer {
    input PrayerRequest
    uses PrayerTools.clean_message
    creates PrayerRequest
    notify Admin
}
```

This generates:

- `POST /api/workflows/submit-prayer`
- a backend module file under `backend/modules/`
- route code that loads the project-local module
- row creation for the declared `PrayerRequest` entity

Module results are mapped into useful generated fields such as `amount`, `total`,
`value`, `message`, `content`, or `text` when those fields exist.

Use:

```bash
python nova.py ir examples/apps/ecommerce_1_1
python nova.py explain examples/apps/ecommerce_1_1
python nova.py validate examples/apps/ecommerce_1_1
python nova.py build-fullstack examples/apps/ecommerce_1_1
```

Compare these generated files:

```txt
generated/ecommerce-one-one/backend/app.py
generated/construction-one-one/backend/app.py
generated/church-custom-one-one/backend/app.py
```

Only the ecommerce app should contain `/api/checkout`. The construction and
custom church apps should use their declared workflow endpoints instead.
