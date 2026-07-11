# NovaDev Windows Installer

This folder contains the first real Windows installer setup for NovaDev.

It uses Inno Setup to build:

```txt
nova website/downloads/NovaDevSetup.exe
```

## What The Installer Does

- Installs NovaDev to `%LOCALAPPDATA%\NovaDev`.
- Copies the NovaDev language into `%LOCALAPPDATA%\NovaDev\language`.
- Creates launchers in `%LOCALAPPDATA%\NovaDev\bin`:
  - `nova.cmd`
  - `nova-shell.cmd`
  - `novapm.cmd`
  - `novadev-manager.cmd`
- Adds `%LOCALAPPDATA%\NovaDev\bin` to the current user's PATH.
- Creates Start Menu shortcuts for NovaDev Manager, NovaDev Shell, and `novapm doctor`.
- Configures the package registry:

```txt
https://novadev-org.vercel.app/downloads/registry.json
```

- Bundles the starter packages:
  - `hello-ui`
  - `auth-kit`
  - `dashboard-kit`

## Requirement

This first installer requires Python 3 to already be installed on the user's computer.

If Python is not found, the launchers tell the user to install Python 3 from:

```txt
https://www.python.org/downloads/windows/
```

## Build The Installer

Install Inno Setup 6, then run:

```powershell
.\installer\windows\build-installer.ps1
```

The output will be:

```txt
nova website/downloads/NovaDevSetup.exe
```

After that, redeploy the `nova website` folder to Vercel so users can download the installer.
