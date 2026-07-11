# Project Structure

NovaDev 0.5 treats project structure as part of the language.

```nova
app BusinessAdmin {
    project {
        frontend Vue
        backend Flask
        database SQLite
        structure VueFlask
        docs Standard
    }
}
```

You can still add explicit filesystem entries:

```nova
filesystem {
    use template VueFlask
    folder uploads
    folder reports
}
```

Templates create the expected folders. Explicit folders and files are appended
after the template.

Module projects can also use `Nova.toml`:

```toml
name = "BusinessAdmin"
version = "0.5"
frontend = "Vue"
backend = "Flask"
database = "SQLite"
entry = "app.nova"
```
