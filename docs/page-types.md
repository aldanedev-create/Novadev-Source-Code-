# Page Types

Page types give pages meaning.

```nova
page Home {
    type marketing
    hero {
        title "Reliable construction services"
        subtitle "Homes, commercial spaces, roofing, and repairs"
        action "Request Quote" to "/quote"
    }
    section Services from Service
}
```

Useful types:

```txt
landing, marketing, catalog, product_detail, checkout, dashboard, admin, form,
portfolio, profile, settings, report, calendar, booking, pipeline, table,
custom
```
