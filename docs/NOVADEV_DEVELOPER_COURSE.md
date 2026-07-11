# NovaDev Developer Course

This course is the source direction for the NovaDev IDE lessons. It teaches NovaDev the way beginner-friendly programming sites teach Python: start with small runnable code, then move into real project structure, APIs, backend work, frontend generation, packages, and deployment.

## Course Path

1. Getting Started
   Learn what NovaDev is, how source code becomes tokens, how tokens become AST output, and how runtime execution differs from project generation.

2. Beginner Programming
   Learn `print`, `let`, strings, interpolation, numbers, booleans, `nil`, lists, objects, operators, and indexing.

3. Core Programming
   Learn `if`, `else`, `while`, functions, debugging, errors, and multi-file project organization with `use`.

4. Object-Oriented Programming
   Learn classes, objects, constructors, methods, `this`, inheritance, composition, and domain modeling.

5. App Building
   Learn `app`, `project`, modes, tables, fields, pages, components, workflows, routes, auth, SQLite, SQLAlchemy, Vue, Tailwind, and project architecture.

6. Standard Library
   Learn Nova math, dates/time, JSON-style data exchange, HTTP/API clients, file operations, SQLite, and safe local/backend runtime patterns.

7. Automations
   Learn scheduled tasks for reports, reminders, cleanup, imports, alerts, and recurring workflow jobs.

8. Custom Code
   Learn custom frontend blocks, custom backend Python modules, triple-quoted strings, API-key handling, environment variables, and third-party API integration.

9. Packages
   Learn how NovaDev packages can provide reusable features such as `auth-kit`, `dashboard-kit`, UI kits, payment helpers, and project templates.

10. Professional Development
   Learn project-specific code generation, testing, deployment planning, and how to avoid generic generated projects.

11. Capstones
   Build an e-commerce store and a custom business system using NovaDev declarations plus custom code.

## API Keys

API keys must not be hardcoded in frontend code. The recommended NovaDev pattern is:

- declare a backend route in `.nova`
- add custom backend Python code
- read the secret from an environment variable
- call the third-party API from the backend
- let the frontend call your backend route

Example environment variable names:

- `OPENAI_API_KEY`
- `STRIPE_SECRET_KEY`
- `RESEND_API_KEY`
- `WEATHER_API_KEY`

## General-Purpose Side of NovaDev

NovaDev is not only a project generator. It also has normal programming features:

- variables
- strings
- numbers
- booleans
- lists
- objects
- indexing
- arithmetic
- comparisons
- logical expressions
- conditionals
- loops
- functions
- classes
- objects
- methods
- OOP design
- shell execution
- runtime errors

## Standard Library Topics

The NovaDev learning path should also teach standard-library style capabilities:

- Nova Math: arithmetic, totals, percentages, averages, rounding, min/max, random values, finance calculations
- Nova Date/Time: dates, scheduled jobs, booking times, report ranges, reminders
- Nova JSON: objects, lists, API responses, package manifests, config data
- Nova HTTP: backend API clients, GET/POST requests, headers, service modules
- Nova Files: read, write, append, create, and safe delete patterns
- Nova SQLite: local database files, CRUD routes, SQLAlchemy models, generated persistence
- Nova Security: environment variables, secrets, safe paths, validation, auth roles

Browser lessons should explain when a feature is local/backend-only. File deletion, raw file access, API secrets, and SQLite writes should be taught as installed NovaDev or generated backend features, not unsafe browser actions.

That general-purpose side matters because real applications need calculations, validation, formatting, business rules, workflows, and integration logic.

## Full-Stack Side of NovaDev

NovaDev app declarations describe the software that should be generated:

- frontend: Vue
- backend: Flask
- database: SQLite
- model layer: SQLAlchemy
- styling: Tailwind
- project structure: VueFlask
- generated pages
- generated routes
- generated models
- generated workflows
- custom frontend files
- custom backend files
- scheduled automations
- package-manager modules
- API-key-backed service modules
- file and database utilities

## File Operations

NovaDev should teach file operations with safety boundaries:

- `read`: load trusted local files or backend-managed files
- `write`: create or replace generated reports, exports, logs, or project files
- `append`: add log lines or export rows
- `delete`: remove only files inside approved folders such as uploads, cache, or temp

Generated backend code should validate paths before deleting or writing. User-provided paths should not be trusted.

## Automations

Automations describe background jobs:

- daily reports
- appointment reminders
- billing checks
- inventory alerts
- package update checks
- upload cleanup
- external API sync

Automations can connect to workflows and custom backend modules.

## OOP

NovaDev should teach OOP as a design tool:

- classes are blueprints
- objects are live values
- constructors initialize state
- methods define behavior
- inheritance models is-a relationships
- composition models has-a relationships

For generated projects, OOP may appear as Python classes, SQLAlchemy models, service objects, or frontend component objects.

## Teaching Rule

Every lesson should answer four questions:

1. What does this syntax do?
2. Why does a developer need it?
3. Can the learner run a small example?
4. Where does this appear in a real project?
