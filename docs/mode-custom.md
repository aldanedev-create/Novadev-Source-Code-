# Mode Custom

`mode custom` means NovaDev does not assume a domain.

```nova
app ChurchMediaSystem {
    project {
        frontend Vue
        backend Flask
        database SQLite
        mode custom
    }
}
```

NovaDev generates only declared:

- tables/entities
- pages
- workflows
- routes
- modules
- custom code
- architecture files

It must not add carts, checkout, estimators, school grades, CRM deals, or any
other unrelated domain behavior.
