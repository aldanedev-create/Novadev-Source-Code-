from __future__ import annotations

"""Full project generator for NovaDev 0.4.

`ProjectGenerator` turns high-level NovaDev app declarations into a runnable
Flask + browser application under `generated/<app-name>/`.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from .ast_nodes import (
    AppNode,
    AssetNode,
    FileNode,
    FilesystemNode,
    FolderNode,
    IgnoreNode,
    Program,
    ResourceNode,
    TemplateNode,
)
from .backend_generator import BackendGenerator
from .frontend_generator import FrontendGenerator


@dataclass
class ProjectBuild:
    app_name: str
    project_dir: Path
    frontend_dir: Path
    backend_dir: Path
    files: List[Path]


class ProjectGenerator:
    def generate(self, program: Program, output_root: Path | str = "generated") -> ProjectBuild:
        app = self.find_app(program)
        project_dir = Path(output_root) / slug_name(app.name)
        frontend_dir = project_dir / "frontend"
        backend_dir = project_dir / "backend"

        project_dir.mkdir(parents=True, exist_ok=True)
        self.apply_templates(app, project_dir)

        files: List[Path] = []
        files.extend(FrontendGenerator().generate(program, frontend_dir))
        files.extend(BackendGenerator().generate(program, backend_dir, frontend_dir))
        files.extend(self.apply_filesystem(app.filesystem, project_dir))
        files.extend(self.write_project_files(app, project_dir, frontend_dir, backend_dir))

        return ProjectBuild(app.name, project_dir, frontend_dir, backend_dir, files)

    def find_app(self, program: Program) -> AppNode:
        if program.app:
            return program.app
        for node in program.body:
            if isinstance(node, AppNode):
                return node
        return AppNode("NovaDevApp")

    def apply_templates(self, app: AppNode, project_dir: Path) -> None:
        if app.stack.lower() == "jqueryflask":
            self.jquery_flask_template(project_dir)
        if app.filesystem:
            for entry in app.filesystem.entries:
                if isinstance(entry, TemplateNode) and entry.name.lower() == "jqueryflask":
                    self.jquery_flask_template(project_dir)

    def jquery_flask_template(self, project_dir: Path) -> None:
        for folder in [
            project_dir / "backend",
            project_dir / "frontend",
            project_dir / "frontend" / "css",
            project_dir / "frontend" / "js",
            project_dir / "docs",
        ]:
            folder.mkdir(parents=True, exist_ok=True)

    def apply_filesystem(self, filesystem: FilesystemNode | None, project_dir: Path) -> List[Path]:
        if not filesystem:
            return []
        return self.apply_entries(filesystem.entries, project_dir, project_dir)

    def apply_entries(self, entries: Iterable[object], base_dir: Path, project_dir: Path) -> List[Path]:
        written: List[Path] = []
        base_dir.mkdir(parents=True, exist_ok=True)

        for entry in entries:
            if isinstance(entry, FolderNode):
                folder = safe_join(base_dir, entry.name)
                folder.mkdir(parents=True, exist_ok=True)
                written.extend(self.apply_entries(entry.entries, folder, project_dir))
            elif isinstance(entry, FileNode):
                target_name = entry.generate or entry.name
                target = safe_join(project_dir if entry.generate else base_dir, target_name)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(entry.content, encoding="utf-8")
                written.append(target)
            elif isinstance(entry, IgnoreNode):
                target = project_dir / ".gitignore"
                text = "\n".join(entry.patterns).strip() + "\n"
                target.write_text(text, encoding="utf-8")
                written.append(target)
            elif isinstance(entry, AssetNode):
                written.extend(self.apply_entries(entry.entries, project_dir / "frontend" / "assets", project_dir))
            elif isinstance(entry, ResourceNode):
                written.extend(self.apply_entries(entry.entries, project_dir / "resources", project_dir))
            elif isinstance(entry, TemplateNode):
                if entry.name.lower() == "jqueryflask":
                    self.jquery_flask_template(project_dir)
        return written

    def write_project_files(
        self,
        app: AppNode,
        project_dir: Path,
        frontend_dir: Path,
        backend_dir: Path,
    ) -> List[Path]:
        files = {
            project_dir / "README.md": self.project_readme(app, frontend_dir, backend_dir),
        }
        if app.database.lower() == "sqlite":
            database_path = backend_dir / "database.db"
            database_path.touch()
            files[database_path] = ""

        for path, content in files.items():
            if content:
                path.write_text(content, encoding="utf-8")
        return list(files.keys())

    def project_readme(self, app: AppNode, frontend_dir: Path, backend_dir: Path) -> str:
        stack = app.stack or "JQueryFlask"
        database = app.database or "in-memory starter data"
        return f"""# {app.name}

Generated by NovaDev 0.4.

## Stack

- Frontend: HTML, CSS, JavaScript, and jQuery-style browser behavior
- Backend: Flask
- Database setting: {database}
- NovaDev stack declaration: {stack}

## Run

```bash
cd {backend_dir}
python -m pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000.

The Flask server serves `{frontend_dir}` and exposes JSON API routes for the
tables declared in the NovaDev source file.
"""


def slug_name(name: str) -> str:
    separated = re.sub(r"(.)([A-Z][a-z]+)", r"\1-\2", name)
    separated = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", separated)
    separated = separated.replace("_", "-")
    return re.sub(r"[^a-zA-Z0-9-]+", "-", separated).strip("-").lower() or "novadev-app"


def safe_join(root: Path, relative: str) -> Path:
    root_resolved = root.resolve()
    target = (root / relative).resolve()
    if root_resolved != target and root_resolved not in target.parents:
        raise ValueError(f"Refusing to write outside generated project: {relative}")
    return target
