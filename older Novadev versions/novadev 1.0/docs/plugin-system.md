# Plugin System

NovaDev 1.0 records plugin declarations as project metadata.

```nova
app Store {
    plugin AuthKit
    plugin StripeCheckout
    plugin AdminCharts
}
```

Generated projects include plugin documentation so a developer can see which
plugin-style capabilities the NovaDev source asked for. Current plugins are
metadata hooks; future versions can attach parser extensions, generator hooks,
and validation rules.

Package-style CLI commands currently maintain local metadata:

```bash
python nova.py install AuthKit
python nova.py update AuthKit
python nova.py remove AuthKit
```
