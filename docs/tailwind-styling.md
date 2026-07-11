# Tailwind Styling

NovaDev can generate Vue projects with Tailwind CSS.

Use:

```nova
app FreshCart {
    project {
        frontend Vue
        backend Flask
        database SQLite
        structure VueFlask
        styling Tailwind
        mode ecommerce
    }
}
```

For Vue projects, Tailwind is the preferred styling system. You can still use
plain generated CSS with:

```nova
project {
    styling CSS
}
```

## Why Tailwind Helps

Tailwind gives NovaDev a large UI vocabulary:

- layout utilities
- spacing utilities
- responsive design
- color utilities
- typography utilities
- borders, radius, shadows, and states
- reusable `@apply` component classes

That makes it easier for NovaDev to generate different apps without inventing a
large custom CSS framework.

## What ProjectIR Controls

Tailwind is the tool. ProjectIR is the decision-maker.

ProjectIR decides:

- app mode
- styling system
- theme colors
- density
- radius
- page types
- component choices
- workflow-driven UI behavior

Then the Vue generator writes:

```txt
frontend/vite.config.js
frontend/tailwind.config.js
frontend/src/assets/main.css
frontend/src/**/*.vue
```

`main.css` is no longer one fixed visual identity. It contains Tailwind setup,
CSS variables, `@theme` tokens, and generated `@apply` rules based on the app's
ProjectIR style profile.

## Mode Profiles

NovaDev includes Tailwind profiles for:

```txt
custom, ecommerce, construction, crm, school, portfolio, restaurant, booking,
dashboard, blog, cms, church, gym, inventory, delivery, realestate, healthcare,
finance, trading, security, nonprofit, event, hotel, salon, learning,
marketplace, social, forum, projectmanagement, invoice, pos, supportdesk,
logistics
```

Each profile can change:

- primary color
- accent color
- surface color
- sidebar treatment
- hero treatment
- panel/card treatment
- button treatment
- density
- radius

## Theme Overrides

Themes can override the mode profile:

```nova
theme FreshStore {
    primary "#f59e0b"
    accent "#111827"
    surface "#fff7ed"
    radius "small"
    density "compact"
}

app FreshCart {
    use theme FreshStore

    project {
        frontend Vue
        backend Flask
        styling Tailwind
        mode ecommerce
    }
}
```

## Commands

Inspect style in ProjectIR:

```bash
python nova.py ir examples/apps/ecommerce_1_1
python nova.py explain examples/apps/ecommerce_1_1
```

Build a Tailwind Vue + Flask project:

```bash
python nova.py build-fullstack examples/apps/ecommerce_1_1
```

Run the frontend:

```bash
cd generated/ecommerce-one-one/frontend
npm install
npm run dev
```

## General-Purpose Example

NovaDev is not only a project DSL. It also has normal programming features.

Run:

```bash
python nova.py run examples/scripts/project_planner.nova
```

That script uses variables, lists, objects, functions, `if/elif/else`, loops,
and `print` to generate starter `.nova` app declarations with Tailwind enabled.
