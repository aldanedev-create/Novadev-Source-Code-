from __future__ import annotations

"""Full project generator for NovaDev 1.0.

`ProjectGenerator` turns high-level NovaDev app declarations into a runnable
Flask + browser application under `generated/<app-name>/`.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

from .ast_nodes import (
    AppNode,
    ArchitectureNode,
    AssetNode,
    CustomCodeNode,
    FileNode,
    FilesystemNode,
    FolderNode,
    IgnoreNode,
    Program,
    PluginNode,
    ResourceNode,
    SourceFileNode,
    TemplateNode,
)
from .backend_targets import BackendTargetGenerator
from .frontend_generator import FrontendGenerator
from .vue_generator import VueGenerator


@dataclass
class ProjectBuild:
    app_name: str
    project_dir: Path
    frontend_dir: Path
    backend_dir: Path
    files: List[Path]
    frontend: str = ""
    backend: str = ""


class ProjectGenerator:
    def generate(self, program: Program, output_root: Path | str = "generated") -> ProjectBuild:
        app = self.find_app(program)
        self.collect_top_level_metadata(program, app)
        project_dir = Path(output_root) / slug_name(app.name)
        frontend_dir = project_dir / "frontend"
        backend_dir = project_dir / "backend"

        project_dir.mkdir(parents=True, exist_ok=True)
        self.apply_templates(app, project_dir)

        files: List[Path] = []
        frontend = frontend_target(app)
        backend = backend_target(app)
        if frontend == "Vue":
            files.extend(VueGenerator().generate(program, frontend_dir))
        else:
            files.extend(FrontendGenerator().generate(program, frontend_dir))
        files.extend(BackendTargetGenerator().generate(program, backend_dir, frontend_dir, backend))
        files.extend(self.apply_architecture(app.architecture, project_dir))
        files.extend(self.apply_filesystem(app.filesystem, project_dir))
        files.extend(self.write_project_files(app, project_dir, frontend_dir, backend_dir))
        files.extend(self.write_custom_code_files(app, project_dir, frontend_dir, backend_dir))

        return ProjectBuild(app.name, project_dir, frontend_dir, backend_dir, files, frontend, backend)

    def find_app(self, program: Program) -> AppNode:
        if program.app:
            return program.app
        for node in program.body:
            if isinstance(node, AppNode):
                return node
        return AppNode("NovaDevApp")

    def collect_top_level_metadata(self, program: Program, app: AppNode) -> None:
        for node in program.body:
            if node is app:
                continue
            if isinstance(node, (PluginNode, CustomCodeNode, ArchitectureNode, FilesystemNode)):
                app.add_member(node)

    def apply_templates(self, app: AppNode, project_dir: Path) -> None:
        template_name = (app.structure or app.stack).lower()
        if template_name == "jqueryflask":
            self.jquery_flask_template(project_dir)
        if template_name in {"vueflask", "vuefastapi", "vuenode", "vueexpress", "vuedjango"}:
            self.vue_template(project_dir)
        if app.filesystem:
            for entry in app.filesystem.entries:
                entry_name = entry.name.lower() if isinstance(entry, TemplateNode) else ""
                if entry_name == "jqueryflask":
                    self.jquery_flask_template(project_dir)
                elif entry_name in {"vueflask", "vuefastapi", "vuenode", "vueexpress", "vuedjango"}:
                    self.vue_template(project_dir)

    def jquery_flask_template(self, project_dir: Path) -> None:
        for folder in [
            project_dir / "backend",
            project_dir / "frontend",
            project_dir / "frontend" / "css",
            project_dir / "frontend" / "js",
            project_dir / "docs",
        ]:
            folder.mkdir(parents=True, exist_ok=True)

    def vue_template(self, project_dir: Path) -> None:
        for folder in [
            project_dir / "frontend" / "src" / "pages",
            project_dir / "frontend" / "src" / "components",
            project_dir / "frontend" / "src" / "router",
            project_dir / "frontend" / "src" / "stores",
            project_dir / "frontend" / "src" / "services",
            project_dir / "frontend" / "src" / "assets",
            project_dir / "frontend" / "src" / "layouts",
            project_dir / "frontend" / "public",
            project_dir / "backend",
            project_dir / "docs",
            project_dir / "uploads",
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
                elif entry.name.lower() in {"vueflask", "vuefastapi", "vuenode", "vueexpress", "vuedjango"}:
                    self.vue_template(project_dir)
            elif isinstance(entry, SourceFileNode):
                target = safe_join(base_dir, entry.name)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(entry.content, encoding="utf-8")
                written.append(target)
        return written

    def apply_architecture(self, architecture: ArchitectureNode | None, project_dir: Path) -> List[Path]:
        if not architecture:
            return []
        return self.apply_entries(architecture.entries, project_dir, project_dir)

    def write_project_files(
        self,
        app: AppNode,
        project_dir: Path,
        frontend_dir: Path,
        backend_dir: Path,
    ) -> List[Path]:
        files = {
            project_dir / "README.md": self.project_readme(app, frontend_dir, backend_dir),
            project_dir / "Nova.toml": self.nova_toml(app),
            project_dir / "docs" / "architecture.md": self.architecture_doc(app),
            project_dir / "docs" / "plugins.md": self.plugins_doc(app),
            project_dir / "docs" / "custom-code.md": self.custom_code_doc(app),
            project_dir / "novadev.project.json": self.project_manifest(app),
        }
        if app.database.lower() == "sqlite":
            database_path = backend_dir / "database.db"
            database_path.touch()
            files[database_path] = ""

        for path, content in files.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if content:
                path.write_text(content, encoding="utf-8")
        return list(files.keys())

    def write_custom_code_files(
        self,
        app: AppNode,
        project_dir: Path,
        frontend_dir: Path,
        backend_dir: Path,
    ) -> List[Path]:
        written: List[Path] = []
        for index, block in enumerate(app.custom_code, start=1):
            if block.language == "python" or block.target == "backend":
                suffix = "py" if block.language == "python" else "txt"
                target = backend_dir / "custom" / f"custom_{index}.{suffix}"
            elif block.language == "js" or block.target == "frontend":
                target = frontend_dir / "src" / "custom" / f"custom_{index}.js"
            elif block.language == "css" or block.target == "css":
                target = frontend_dir / "src" / "custom" / f"custom_{index}.css"
            elif block.language == "sql":
                target = project_dir / "database" / f"custom_{index}.sql"
            else:
                target = project_dir / "custom" / f"custom_{index}.{block.language or 'txt'}"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(block.code, encoding="utf-8")
            written.append(target)
        return written

    def project_readme(self, app: AppNode, frontend_dir: Path, backend_dir: Path) -> str:
        stack = app.stack or "JQueryFlask"
        frontend = frontend_target(app)
        backend = backend_target(app)
        database = app.database or "in-memory starter data"
        frontend_commands = self.frontend_commands(frontend, frontend_dir)
        backend_commands = self.backend_commands(backend, backend_dir)
        return f"""# {app.name}

Generated by NovaDev 1.0.

## Stack

- Frontend: {frontend}
- Backend: {backend}
- Database setting: {database}
- NovaDev stack declaration: {stack}
- Mode: {app.mode or app.project_type or "app"}
- Plugins: {", ".join(plugin.name for plugin in app.plugins) or "none"}

## Run Frontend

```bash
{frontend_commands}
```

## Run Backend

```bash
{backend_commands}
```

For Vue projects, open the frontend at http://127.0.0.1:5173.

The generated code is intentionally normal editable frontend and backend code.
"""

    def nova_toml(self, app: AppNode) -> str:
        return f'''name = "{app.name}"
version = "1.0"
entry = "app.nova"
frontend = "{frontend_target(app)}"
backend = "{backend_target(app)}"
database = "{app.database or "SQLite"}"
'''

    def architecture_doc(self, app: AppNode) -> str:
        lines = ["# Project Architecture", "", "Generated by NovaDev 1.0.", ""]
        if app.architecture:
            lines.append("## Custom Architecture Entries")
            lines.append("")
            for entry in app.architecture.entries:
                lines.append(f"- `{entry.__class__.__name__}`: `{getattr(entry, 'name', '')}`")
        else:
            lines.append("No custom `project { architecture { ... } }` block was declared.")
        if app.filesystem:
            lines.extend(["", "## Filesystem Entries", ""])
            for entry in app.filesystem.entries:
                lines.append(f"- `{entry.__class__.__name__}`: `{getattr(entry, 'name', '')}`")
        return "\n".join(lines) + "\n"

    def plugins_doc(self, app: AppNode) -> str:
        lines = ["# Plugins", "", "NovaDev 1.0 records plugins as editable project metadata.", ""]
        if app.plugins:
            for plugin in app.plugins:
                lines.append(f"- `{plugin.name}`")
        else:
            lines.append("No plugins declared.")
        return "\n".join(lines) + "\n"

    def custom_code_doc(self, app: AppNode) -> str:
        lines = ["# Custom Code", "", "Custom code blocks copied from NovaDev source.", ""]
        if not app.custom_code:
            lines.append("No custom code blocks declared.")
        for index, block in enumerate(app.custom_code, start=1):
            lines.extend(
                [
                    f"## Block {index}: {block.language} -> {block.target or 'runtime'}",
                    "",
                    "```" + block.language,
                    block.code,
                    "```",
                    "",
                ]
            )
        return "\n".join(lines) + "\n"

    def project_manifest(self, app: AppNode) -> str:
        import json

        data = {
            "name": app.name,
            "version": "1.0",
            "frontend": frontend_target(app),
            "backend": backend_target(app),
            "database": app.database or "SQLite",
            "mode": app.mode or app.project_type or "app",
            "plugins": [plugin.name for plugin in app.plugins],
            "customCode": [
                {"language": block.language, "target": block.target, "bytes": len(block.code)}
                for block in app.custom_code
            ],
            "discoveries": app.discoveries,
        }
        return json.dumps(data, indent=2) + "\n"

    def frontend_commands(self, frontend: str, frontend_dir: Path) -> str:
        if frontend == "Vue":
            return f"cd {frontend_dir}\nnpm install\nnpm run dev"
        return f"open {frontend_dir / 'index.html'}"

    def backend_commands(self, backend: str, backend_dir: Path) -> str:
        if backend == "Express":
            return f"cd {backend_dir}\nnpm install\nnpm run dev"
        if backend == "FastAPI":
            return f"cd {backend_dir}\npython -m pip install -r requirements.txt\nuvicorn app:app --reload"
        if backend == "Django":
            return f"cd {backend_dir}\npython -m pip install -r requirements.txt\npython manage.py runserver"
        return f"cd {backend_dir}\npython -m pip install -r requirements.txt\npython app.py"


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


def frontend_target(app: AppNode) -> str:
    if app.frontend:
        return normalize_frontend(app.frontend)
    if app.stack.lower().startswith("vue"):
        return "Vue"
    return "StaticHTML"


def backend_target(app: AppNode) -> str:
    if app.backend:
        return normalize_backend(app.backend)
    stack = app.stack.lower()
    if stack == "vuefastapi":
        return "FastAPI"
    if stack in {"vuenode", "vueexpress"}:
        return "Express"
    if stack == "vuedjango":
        return "Django"
    return "Flask"


def normalize_frontend(value: str) -> str:
    return "Vue" if value.lower() in {"vue", "vue3"} else value


def normalize_backend(value: str) -> str:
    lowered = value.lower()
    if lowered in {"flask", "vueflask"}:
        return "Flask"
    if lowered in {"fastapi", "vuefastapi"}:
        return "FastAPI"
    if lowered in {"node", "express", "vuenode", "vueexpress"}:
        return "Express"
    if lowered in {"django", "vuedjango"}:
        return "Django"
    return value
