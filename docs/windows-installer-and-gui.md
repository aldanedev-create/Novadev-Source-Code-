# NovaDev Windows Installer And GUI

NovaDev now has a first Windows desktop distribution layer.

## What It Adds

- `NovaDevSetup.exe` installer built with Inno Setup.
- `novadev_manager.py`, a Tkinter GUI for managing NovaDev.
- Windows launcher commands:
  - `nova`
  - `nova-shell`
  - `novapm`
  - `novadev-manager`
- User PATH registration.
- Start Menu shortcuts.
- Bundled starter packages.

## Build Requirements

Install Inno Setup 6:

```txt
https://jrsoftware.org/isinfo.php
```

NovaDev still requires Python 3 on the user's machine. This first installer
does not bundle a private Python runtime yet.

## Build Command

Run from the repo root:

```powershell
.\installer\windows\build-installer.ps1
```

Output:

```txt
nova website/downloads/NovaDevSetup.exe
```

## User Install Result

The installer places files here:

```txt
%LOCALAPPDATA%\NovaDev\
  bin\
    nova.cmd
    nova-shell.cmd
    novapm.cmd
    novadev-manager.cmd
    novadev-manager.vbs
  language\
  packages\
  cache\
  logs\
  config.json
  installed.json
```

The installer adds this folder to the current user's PATH:

```txt
%LOCALAPPDATA%\NovaDev\bin
```

After opening a new terminal, users can run:

```bash
nova shell
nova run examples/hello.nova
novapm doctor
novapm install auth-kit
```

## GUI

Run the GUI with:

```bash
novadev-manager
```

The Start Menu shortcut uses `novadev-manager.vbs` so the desktop manager opens
without flashing a terminal window. If the GUI cannot start, details are written
to:

```txt
%LOCALAPPDATA%\NovaDev\logs\manager.log
```

The GUI can:

- install or update NovaDev from the website zip
- install all bundled packages
- run `novapm doctor`
- open the Nova shell
- run the hello example
- search packages
- install packages
- remove packages
- list installed packages
- configure the registry URL

## Next Step

The next professional step would be to bundle a private Python runtime or build
small native `.exe` launchers, so users do not need Python installed first.
