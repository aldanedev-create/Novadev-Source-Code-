# Stack Targets

NovaDev can generate starter projects for several targets.

Frontend targets:

- `HTML` through `build-ui`.
- `Vue` through `build-vue` or `build-fullstack`.

Backend targets:

- `Flask`
- `FastAPI`
- `Express`
- `Django`

Database metadata:

- `SQLite`
- `Postgres`
- `MySQL`
- `MongoDB`

Example:

```nova
project {
    frontend Vue
    backend Flask
    database SQLite
    structure VueFlask
}
```

Flask is the most complete backend target and is the default for full-stack
builds. The other backend targets generate editable starter APIs.
