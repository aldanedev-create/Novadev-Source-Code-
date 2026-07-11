# Roadmap

NovaDev is still a prototype. The goal is to grow it into a real programming
language ecosystem step by step.

## 0.1 Completed

- `let`
- `print`
- strings and numbers
- basic `+`
- simple HTML generator

## 0.2 Completed

- parser and AST
- table declarations
- auth declarations
- route declarations
- theme declarations
- declarative pages
- forms, tables, cards, charts, nav, sidebar, modals
- role-based generated UI
- generated HTML/CSS/JS dashboard
- tests
- docs

## 0.3 Completed

- real lexer token stream
- token-based recursive-descent parser
- richer expression parser
- `if` and `else`
- `while`
- functions and `return`
- runtime environments
- variable assignment
- missing-variable runtime errors
- app/table/page/route/theme/auth registries
- interactive shell with `.load` and full `nova.py` command equivalents
- `tokens` command
- `ast` command
- `build-ui` command that writes `dist/index.html`, `dist/style.css`, and `dist/app.js`
- `build-backend` command that writes Flask backend files
- `build-app` command that generates UI and Flask backend together
- beginner-focused docs and examples

## 0.4 Suggested Next

- formatter command
- semantic diagnostics for 0.3 AST nodes
- standard library functions
- arrays and object literals
- import files
- better route handlers
- SQLite persistence for the generated Flask backend
- generated validation on backend routes
- auth sessions
- password hashing

## 0.5 Suggested Next

- `nova new`
- `nova add`
- package file
- package registry prototype
- test generator
- security scanner expansion
- documentation generator command

## 1.0 Vision

NovaDev should become a full developer ecosystem:

- language
- lexer
- parser
- interpreter
- runtime
- package manager
- standard library
- web framework
- UI generator
- backend generator
- testing tool
- security scanner
- documentation generator
