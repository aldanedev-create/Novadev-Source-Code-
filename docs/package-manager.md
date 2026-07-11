# NovaDev Package Manager

`novapm.py` is NovaDev's local package manager.

It has two jobs:

- install the NovaDev language onto a developer's machine
- install NovaDev packages/modules locally

It uses Python 3 only. No external libraries are required.

## Local Layout

By default, NovaDev installs into:

```txt
~/.novadev/
  bin/
  language/
  packages/
  cache/
  registry.json
  installed.json
  config.json
```

Use `--home` to test or use a different location:

```bash
python novapm.py doctor --home .tmp-novadev
```

## Install NovaDev Language

From a downloaded NovaDev source folder:

```bash
python novapm.py install-language --source .
```

This copies the language into:

```txt
~/.novadev/language
```

and writes launcher scripts into:

```txt
~/.novadev/bin
```

Add that `bin` folder to PATH to run:

```bash
nova --version
novapm doctor
nova-shell
```

## Package Commands

```bash
python novapm.py init-registry
python novapm.py search ui
python novapm.py install packages/hello-ui
python novapm.py list
python novapm.py info hello-ui
python novapm.py remove hello-ui
python novapm.py pack packages/hello-ui
```

## Package Manifest

Packages use `nova-package.json`:

```json
{
  "name": "hello-ui",
  "version": "0.1.0",
  "description": "Example NovaDev UI helpers",
  "entry": "index.nova",
  "kind": "module",
  "files": ["index.nova"]
}
```

## Registry

The local registry lives at:

```txt
~/.novadev/registry.json
```

You can point it at a website-hosted registry:

```bash
python novapm.py configure-registry https://example.com/nova-packages.json
```

That is the path for a future public NovaDev package ecosystem: host a registry
JSON file and package zip files, then `novapm` downloads and installs them.

## Website Distribution Layout

The Vercel education site can host the installer, language zip, registry, and
package zips directly:

```txt
downloads/
  install-novadev.py
  NovaDevSetup.exe
  novadev.zip
  registry.json
  checksums.json
  packages/
    hello-ui.zip
    auth-kit.zip
    dashboard-kit.zip
```

After deployment, users run:

```bash
python install-novadev.py --zip-url https://novadev-org.vercel.app/downloads/novadev.zip --install-all-packages
```

The installer infers:

```txt
https://novadev-org.vercel.app/downloads/registry.json
```

and configures `~/.novadev/config.json` so `novapm install package-name`
downloads packages from the hosted registry.

## Windows Installer And GUI

NovaDev also has a first Windows installer setup in:

```txt
installer/windows/
```

Build it with:

```powershell
.\installer\windows\build-installer.ps1
```

The output is:

```txt
nova website/downloads/NovaDevSetup.exe
```

That installer copies NovaDev into `%LOCALAPPDATA%\NovaDev`, creates
`nova`, `nova-shell`, `novapm`, and `novadev-manager` launchers, adds the
launcher folder to the user's PATH, creates Start Menu shortcuts, and bundles
the starter packages.
