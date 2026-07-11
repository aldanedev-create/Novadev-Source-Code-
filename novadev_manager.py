"""NovaDev Manager GUI.

This file is intentionally small and dependency-free. The Windows installer
launches it from the installed language folder, and the local source tree can
launch it directly with Python.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk


ROOT = Path(__file__).resolve().parent
NOVA = ROOT / "nova.py"
NOVAPM = ROOT / "novapm.py"
EXAMPLES = ROOT / "examples"


class NovaDevManager(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("NovaDev Manager")
        self.geometry("980x650")
        self.minsize(820, 560)

        self.output_var = tk.StringVar(value="Ready")
        self.example_var = tk.StringVar(value=str(EXAMPLES / "hello.nova"))

        self.configure(bg="#181818")
        self.build_style()
        self.build_ui()

    def build_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background="#181818")
        style.configure("Panel.TFrame", background="#202020")
        style.configure("TLabel", background="#181818", foreground="#f3f4f6")
        style.configure("Muted.TLabel", background="#181818", foreground="#a1a1aa")
        style.configure("TButton", padding=8)
        style.configure("Accent.TButton", padding=8)
        style.configure("TNotebook", background="#181818", borderwidth=0)
        style.configure("TNotebook.Tab", padding=(12, 7))

    def build_ui(self) -> None:
        header = ttk.Frame(self, padding=(18, 14))
        header.pack(fill="x")

        mark = tk.Label(header, text="ND", width=4, height=2, bg="#22c55e", fg="#052e16", font=("Segoe UI", 11, "bold"))
        mark.pack(side="left")

        title_box = ttk.Frame(header)
        title_box.pack(side="left", padx=12)
        ttk.Label(title_box, text="NovaDev Manager", font=("Segoe UI", 16, "bold")).pack(anchor="w")
        ttk.Label(title_box, text="Run NovaDev, open the shell, build UI, and manage packages.", style="Muted.TLabel").pack(anchor="w")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.build_run_tab()
        self.build_packages_tab()
        self.build_help_tab()

        status = ttk.Label(self, textvariable=self.output_var, anchor="w", padding=(10, 4))
        status.pack(fill="x")

    def build_run_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Panel.TFrame", padding=16)
        self.notebook.add(frame, text="Run")

        ttk.Label(frame, text="NovaDev Commands", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        ttk.Label(frame, text="These buttons run the same commands available in nova.py and shell.py.", style="Muted.TLabel").pack(anchor="w", pady=(0, 12))

        buttons = ttk.Frame(frame, style="Panel.TFrame")
        buttons.pack(fill="x", pady=(0, 12))

        ttk.Button(buttons, text="Open Shell", command=self.open_shell).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Run Example", command=self.run_selected_example).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Build UI", command=self.build_selected_ui).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Show Tokens", command=lambda: self.run_command([sys.executable, str(NOVA), "tokens", self.example_var.get()])).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Show AST", command=lambda: self.run_command([sys.executable, str(NOVA), "ast", self.example_var.get()])).pack(side="left")

        ttk.Label(frame, text="Example file").pack(anchor="w")
        entry = ttk.Entry(frame, textvariable=self.example_var)
        entry.pack(fill="x", pady=(4, 12))

        self.output = scrolledtext.ScrolledText(frame, height=20, bg="#0f1115", fg="#f8fafc", insertbackground="#f8fafc", font=("Consolas", 10))
        self.output.pack(fill="both", expand=True)

    def build_packages_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Panel.TFrame", padding=16)
        self.notebook.add(frame, text="Packages")

        ttk.Label(frame, text="NovaDev Package Manager", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Install and inspect local NovaDev packages.", style="Muted.TLabel").pack(anchor="w", pady=(0, 12))

        buttons = ttk.Frame(frame, style="Panel.TFrame")
        buttons.pack(fill="x", pady=(0, 12))
        ttk.Button(buttons, text="Doctor", command=lambda: self.run_command([sys.executable, str(NOVAPM), "doctor"])).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="Search", command=lambda: self.run_command([sys.executable, str(NOVAPM), "search"])).pack(side="left", padx=(0, 8))
        ttk.Button(buttons, text="List Installed", command=lambda: self.run_command([sys.executable, str(NOVAPM), "list"])).pack(side="left")

    def build_help_tab(self) -> None:
        frame = ttk.Frame(self.notebook, style="Panel.TFrame", padding=16)
        self.notebook.add(frame, text="Help")

        text = (
            "Common commands:\n\n"
            "nova shell\n"
            "nova run examples/hello.nova\n"
            "nova build-ui examples/business_admin.nova\n"
            "nova tokens examples/hello.nova\n"
            "nova ast examples/hello.nova\n"
            "novapm doctor\n\n"
            "If a command fails, the output box shows the error."
        )
        help_box = scrolledtext.ScrolledText(frame, bg="#0f1115", fg="#f8fafc", font=("Consolas", 10))
        help_box.pack(fill="both", expand=True)
        help_box.insert("1.0", text)
        help_box.configure(state="disabled")

    def run_selected_example(self) -> None:
        self.run_command([sys.executable, str(NOVA), "run", self.example_var.get()])

    def build_selected_ui(self) -> None:
        self.run_command([sys.executable, str(NOVA), "build-ui", self.example_var.get()])

    def open_shell(self) -> None:
        command = [sys.executable, str(NOVA), "shell"]
        try:
            kwargs = {"cwd": str(ROOT)}
            if os.name == "nt":
                kwargs["creationflags"] = subprocess.CREATE_NEW_CONSOLE
            subprocess.Popen(command, **kwargs)
            self.output_var.set("Opened NovaDev shell")
            self.write_output("\nOpened NovaDev shell in a new console window.\n")
        except Exception as error:
            self.output_var.set("Could not open shell")
            self.write_output(f"error: {error}\n")
            messagebox.showerror("NovaDev Manager", str(error))

    def run_command(self, command: list[str]) -> None:
        self.output_var.set("Running: " + " ".join(command))
        self.write_output("\n$ " + " ".join(command) + "\n")
        try:
            completed = subprocess.run(
                command,
                cwd=str(ROOT),
                text=True,
                capture_output=True,
                timeout=60,
            )
            if completed.stdout:
                self.write_output(completed.stdout)
            if completed.stderr:
                self.write_output(completed.stderr)
            if completed.returncode == 0:
                self.output_var.set("Command finished")
            else:
                self.output_var.set(f"Command failed with exit code {completed.returncode}")
        except Exception as error:
            self.output_var.set("Command failed")
            self.write_output(f"error: {error}\n")
            messagebox.showerror("NovaDev Manager", str(error))

    def write_output(self, text: str) -> None:
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.see("end")


def main() -> int:
    if "--self-test" in sys.argv:
        missing = [path for path in (NOVA, NOVAPM) if not path.exists()]
        if missing:
            for path in missing:
                print(f"missing: {path}")
            return 1
        import tkinter  # noqa: F401

        print("NovaDev Manager self-test passed")
        return 0

    if not NOVA.exists():
        messagebox.showerror("NovaDev Manager", f"Could not find nova.py at:\n{NOVA}")
        return 1
    app = NovaDevManager()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
