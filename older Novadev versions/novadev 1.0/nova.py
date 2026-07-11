from __future__ import annotations

"""NovaDev 1.0 command-line interface."""

import argparse
import json
import pprint
import shutil
import sys
from pathlib import Path

from novadev import __version__
from novadev.ast_nodes import node_to_data
from novadev.backend_targets import BackendTargetGenerator
from novadev.codegen import BackendGenerator
from novadev.interpreter import Interpreter
from novadev.lexer import NovaLexerError, tokenize
from novadev.module_resolver import ModuleResolutionError, compile_file
from novadev.parser import NovaParser, NovaSyntaxError
from novadev.project_generator import ProjectGenerator, backend_target, slug_name
from novadev.runtime import NovaRuntimeError
from novadev.semantic_analyzer import SemanticAnalyzer
from novadev.ui_generator import UIGenerator
from novadev.vue_generator import VueGenerator


def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_file(path: Path):
    return compile_file(path)


def command_run(args) -> int:
    Interpreter().run_program(parse_file(args.file))
    return 0


def command_build_ui(args) -> int:
    program = parse_file(args.file)
    generated = UIGenerator().generate(program, args.output)
    print(f"NovaDev {__version__} UI generated in {args.output}")
    for path in generated:
        print(f"  {path}")
    return 0


def command_build_backend(args) -> int:
    program = parse_file(args.file)
    app = program.app
    target = args.target or (backend_target(app) if app else "Flask")
    generated = BackendTargetGenerator().generate(program, args.output, args.frontend, target)
    print(f"NovaDev {__version__} {target} backend generated in {args.output}")
    for path in generated:
        print(f"  {path}")
    return 0


def command_build_app(args) -> int:
    program = parse_file(args.file)
    ui_files = UIGenerator().generate(program, args.ui_output)
    backend_files = BackendGenerator().generate(program, args.backend_output, args.ui_output)
    print(f"NovaDev {__version__} app generated")
    print(f"  UI: {args.ui_output}")
    for path in ui_files:
        print(f"    {path}")
    print(f"  Flask backend: {args.backend_output}")
    for path in backend_files:
        print(f"    {path}")
    print("Run it with:")
    print(f"  cd {args.backend_output}")
    print("  python -m pip install -r requirements.txt")
    print("  python app.py")
    return 0


def command_build(args) -> int:
    program = parse_file(args.file)
    build = ProjectGenerator().generate(program, args.output)
    print(f"NovaDev {__version__} project generated")
    print(f"  App: {build.app_name}")
    print(f"  Project: {build.project_dir}")
    print(f"  Frontend: {build.frontend_dir}")
    print(f"  {build.backend} backend: {build.backend_dir}")
    print("Run it with:")
    print(f"  cd {build.backend_dir}")
    print("  python -m pip install -r requirements.txt")
    print("  python app.py")
    return 0


def command_build_vue(args) -> int:
    program = parse_file(args.file)
    app_name = program.app.name if program.app else args.file.stem
    output = args.output or (Path("generated") / slug_name(app_name) / "frontend")
    generated = VueGenerator().generate(program, output)
    print(f"NovaDev {__version__} Vue frontend generated in {output}")
    for path in generated:
        print(f"  {path}")
    return 0


def command_build_fullstack(args) -> int:
    args.output = args.output or Path("generated")
    return command_build(args)


def command_tokens(args) -> int:
    for token in tokenize(read_source(args.file)):
        print(f"{token.line}:{token.column}\t{token.type:<15}\t{token.display_value()}")
    return 0


def command_ast(args) -> int:
    program = parse_file(args.file)
    if args.json:
        print(json.dumps(node_to_data(program), indent=2))
    else:
        pprint.pp(program)
    return 0


def command_shell(args) -> int:
    import shell

    return shell.main()


def command_new(args) -> int:
    root = Path(args.name)
    root.mkdir(parents=True, exist_ok=True)
    app_name = "".join(part.title() for part in root.name.replace("-", " ").replace("_", " ").split()) or "NovaApp"
    nova_toml = root / "Nova.toml"
    app_file = root / "app.nova"
    if not nova_toml.exists():
        nova_toml.write_text(
            f'''name = "{app_name}"
version = "1.0"
entry = "app.nova"
frontend = "{args.frontend}"
backend = "{args.backend}"
database = "{args.database}"
''',
            encoding="utf-8",
        )
    if not app_file.exists():
        app_file.write_text(
            f'''app {app_name} {{
    project {{
        frontend {args.frontend}
        backend {args.backend}
        database {args.database}
        structure {args.frontend}{args.backend}
        mode app

        architecture {{
            folder docs
            folder tests
            folder uploads
        }}
    }}

    page Dashboard {{
        title "{app_name} Dashboard"
    }}
}}
''',
            encoding="utf-8",
        )
    print(f"NovaDev {__version__} project created in {root}")
    return 0


def command_lint(args) -> int:
    program = parse_file(args.file)
    report = SemanticAnalyzer().analyze(program)
    if report.errors:
        for issue in report.errors:
            print(f"error: {issue}")
        return 1
    for issue in report.warnings:
        print(f"warning: {issue}")
    print(f"NovaDev lint ok: {args.file}")
    return 0


def command_format(args) -> int:
    source = read_source(args.file)
    formatted = "\n".join(line.rstrip() for line in source.splitlines()).strip() + "\n"
    parse_file(args.file)
    if args.check:
        if source != formatted:
            print(f"{args.file} needs formatting")
            return 1
        print(f"{args.file} is formatted")
        return 0
    args.file.write_text(formatted, encoding="utf-8")
    print(f"formatted {args.file}")
    return 0


def command_docs(args) -> int:
    program = parse_file(args.file)
    app = program.app
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    target = output / "project-summary.md"
    if app:
        content = f"""# {app.name}

Generated by NovaDev {__version__}.

- Frontend: {app.frontend or app.stack or 'not declared'}
- Backend: {app.backend or app.stack or 'not declared'}
- Database: {app.database or 'not declared'}
- Tables: {len(app.tables)}
- Pages: {len(app.pages)}
- Routes: {len(app.routes)}
- Plugins: {', '.join(plugin.name for plugin in app.plugins) or 'none'}
"""
    else:
        content = f"# NovaDev Program\n\nNo app declaration found in `{args.file}`.\n"
    target.write_text(content, encoding="utf-8")
    print(f"docs generated in {output}")
    return 0


def command_clean(args) -> int:
    program = parse_file(args.file)
    app_name = program.app.name if program.app else args.file.stem
    target = (args.output / slug_name(app_name)).resolve()
    output_root = args.output.resolve()
    if output_root != target and output_root not in target.parents:
        raise ValueError("Refusing to clean outside the generated output folder")
    if target.exists():
        shutil.rmtree(target)
        print(f"removed {target}")
    else:
        print(f"nothing to clean: {target}")
    return 0


def command_dev(args) -> int:
    command_build_fullstack(args)
    print("Dev project generated. Start frontend/backend using the README commands in the generated folder.")
    return 0


def command_package(args) -> int:
    package_file = Path("nova.packages.json")
    data = {"packages": []}
    if package_file.exists():
        data = json.loads(package_file.read_text(encoding="utf-8"))
    packages = set(data.get("packages", []))
    if args.package:
        if args.action == "install":
            packages.add(args.package)
        elif args.action == "remove":
            packages.discard(args.package)
    data["packages"] = sorted(packages)
    package_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"package registry updated: {package_file}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nova", description="NovaDev 1.0 language CLI")
    parser.add_argument("--version", action="version", version=f"NovaDev {__version__}")
    subparsers = parser.add_subparsers(dest="command")

    new_parser = subparsers.add_parser("new", help="Create a NovaDev project folder")
    new_parser.add_argument("name")
    new_parser.add_argument("--frontend", default="Vue")
    new_parser.add_argument("--backend", default="Flask")
    new_parser.add_argument("--database", default="SQLite")
    new_parser.set_defaults(func=command_new)

    run_parser = subparsers.add_parser("run", help="Run a NovaDev file")
    run_parser.add_argument("file", type=Path)
    run_parser.set_defaults(func=command_run)

    ui_parser = subparsers.add_parser("build-ui", help="Generate dist/index.html, dist/style.css, dist/app.js")
    ui_parser.add_argument("file", type=Path)
    ui_parser.add_argument("-o", "--output", type=Path, default=Path("dist"))
    ui_parser.set_defaults(func=command_build_ui)

    backend_parser = subparsers.add_parser("build-backend", help="Generate Flask backend files")
    backend_parser.add_argument("file", type=Path)
    backend_parser.add_argument("-o", "--output", type=Path, default=Path("generated_backend"))
    backend_parser.add_argument("--frontend", type=Path, default=Path("dist"), help="Frontend folder the Flask app should serve")
    backend_parser.add_argument("--target", choices=["Flask", "FastAPI", "Express", "Django"], help="Backend target override")
    backend_parser.set_defaults(func=command_build_backend)

    app_parser = subparsers.add_parser("build-app", help="Generate UI and Flask backend together")
    app_parser.add_argument("file", type=Path)
    app_parser.add_argument("--ui-output", type=Path, default=Path("dist"))
    app_parser.add_argument("--backend-output", type=Path, default=Path("generated_backend"))
    app_parser.set_defaults(func=command_build_app)

    project_parser = subparsers.add_parser("build", help="Generate a full Flask + frontend project")
    project_parser.add_argument("file", type=Path)
    project_parser.add_argument("-o", "--output", type=Path, default=Path("generated"))
    project_parser.set_defaults(func=command_build)

    vue_parser = subparsers.add_parser("build-vue", help="Generate only the Vue frontend")
    vue_parser.add_argument("file", type=Path)
    vue_parser.add_argument("-o", "--output", type=Path)
    vue_parser.set_defaults(func=command_build_vue)

    fullstack_parser = subparsers.add_parser("build-fullstack", help="Generate frontend and backend from project targets")
    fullstack_parser.add_argument("file", type=Path)
    fullstack_parser.add_argument("-o", "--output", type=Path)
    fullstack_parser.set_defaults(func=command_build_fullstack)

    tokens_parser = subparsers.add_parser("tokens", help="Print lexer tokens")
    tokens_parser.add_argument("file", type=Path)
    tokens_parser.set_defaults(func=command_tokens)

    ast_parser = subparsers.add_parser("ast", help="Print parsed AST")
    ast_parser.add_argument("file", type=Path)
    ast_parser.add_argument("--json", action="store_true", help="Print JSON-friendly AST")
    ast_parser.set_defaults(func=command_ast)

    shell_parser = subparsers.add_parser("shell", help="Start the interactive shell")
    shell_parser.set_defaults(func=command_shell)

    lint_parser = subparsers.add_parser("lint", help="Parse and lint a NovaDev file or project")
    lint_parser.add_argument("file", type=Path)
    lint_parser.set_defaults(func=command_lint)

    format_parser = subparsers.add_parser("format", help="Format a NovaDev file")
    format_parser.add_argument("file", type=Path)
    format_parser.add_argument("--check", action="store_true")
    format_parser.set_defaults(func=command_format)

    docs_parser = subparsers.add_parser("docs", help="Generate NovaDev project docs")
    docs_parser.add_argument("file", type=Path)
    docs_parser.add_argument("-o", "--output", type=Path, default=Path("generated_docs"))
    docs_parser.set_defaults(func=command_docs)

    clean_parser = subparsers.add_parser("clean", help="Remove generated output for a project")
    clean_parser.add_argument("file", type=Path)
    clean_parser.add_argument("-o", "--output", type=Path, default=Path("generated"))
    clean_parser.set_defaults(func=command_clean)

    dev_parser = subparsers.add_parser("dev", help="Generate a dev project and print run instructions")
    dev_parser.add_argument("file", type=Path)
    dev_parser.add_argument("-o", "--output", type=Path)
    dev_parser.set_defaults(func=command_dev)

    for name in ["install", "update", "remove", "package", "deploy"]:
        package_parser = subparsers.add_parser(name, help=f"{name} package/deployment metadata")
        package_parser.add_argument("package", nargs="?")
        package_parser.set_defaults(func=command_package, action=name)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0

    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(f"file not found: {exc.filename}", file=sys.stderr)
        return 1
    except (NovaLexerError, NovaSyntaxError, NovaRuntimeError, ModuleResolutionError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
