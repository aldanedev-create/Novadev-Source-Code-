# Packages

Package-style imports can be written in NovaDev source:

```nova
import auth.login
import ui.charts as Charts
```

In NovaDev 1.0, package commands manage local registry metadata:

```bash
python nova.py install auth.login
python nova.py update auth.login
python nova.py remove auth.login
```

The package registry lives in `nova.packages.json`. This keeps the command flow
ready for a real package manager while avoiding external dependencies.
