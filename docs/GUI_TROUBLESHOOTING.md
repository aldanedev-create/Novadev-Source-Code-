# NovaDev GUI Troubleshooting

NovaDev Manager is a Tkinter desktop GUI for running common NovaDev commands.

## If the Icon Opens Then Disappears

The Windows launcher now writes a log file and shows a message box when startup fails.

Log path:

```text
Windows installer:
C:\Users\<you>\AppData\Local\NovaDev\logs\manager.log

Website Python installer:
C:\Users\<you>\.novadev\logs\manager.log
```

Common causes:

- Python is not installed or not visible to the launcher.
- Tkinter is missing from the Python installation.
- `nova.py` is missing from the installed NovaDev language folder.
- The install package was not rebuilt after source changes.

## What the Buttons Do

- `Open Shell` opens NovaDev shell in a new console window.
- `Run Example` runs `nova run <file>`.
- `Build UI` runs `nova build-ui <file>`.
- `Show Tokens` runs `nova tokens <file>`.
- `Show AST` runs `nova ast <file>`.
- `Doctor`, `Search`, and `List Installed` run `novapm` package-manager commands.

If a command fails, the GUI output box shows stdout, stderr, and the exit code.

## Rebuilding the Windows Installer

After editing GUI or launcher files, rebuild the installer package before uploading it to the website. Otherwise users will still download the older GUI.
