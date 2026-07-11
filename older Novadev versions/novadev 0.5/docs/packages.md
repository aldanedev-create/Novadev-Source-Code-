# Packages

NovaDev 0.5 parses package-style imports:

```nova
import "@nova/auth"
import "@nova/charts"
import "@nova/forms"
```

It also parses remote package URLs:

```nova
import "https://packages.novadev.dev/charts"
```

Prototype 0.5 does not download packages yet. The resolver records those imports
so a later package manager can create `packages/` and `nova.lock` safely.
