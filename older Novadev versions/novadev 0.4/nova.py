from __future__ import annotations

"""NovaDev 0.4 command-line interface."""

import argparse
import json
import pprint
import sys
from pathlib import Path

from novadev import __version__
from novadev.ast_nodes import node_to_data
from novadev.codegen import BackendGenerator
from novadev.interpreter import Interpreter
from novadev.lexer import NovaLexerError, tokenize
from novadev.parser import NovaParser, NovaSyntaxError
from novadev.project_generator import ProjectGenerator
from novadev.runtime import NovaRuntimeError
from novadev.ui_generator import UIGenerator


def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_file(path: Path):
    return NovaParser(read_source(path)).parse()


def command_run(args) -> int:
    Interpreter().run(read_source(args.file))
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
    generated = BackendGenerator().generate(program, args.output, args.frontend)
    print(f"NovaDev {__version__} backend generated in {args.output}")
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
    print(f"  Flask backend: {build.backend_dir}")
    print("Run it with:")
    print(f"  cd {build.backend_dir}")
    print("  python -m pip install -r requirements.txt")
    print("  python app.py")
    return 0


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nova", description="NovaDev 0.4 prototype CLI")
    parser.add_argument("--version", action="version", version=f"NovaDev {__version__}")
    subparsers = parser.add_subparsers(dest="command")

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

    tokens_parser = subparsers.add_parser("tokens", help="Print lexer tokens")
    tokens_parser.add_argument("file", type=Path)
    tokens_parser.set_defaults(func=command_tokens)

    ast_parser = subparsers.add_parser("ast", help="Print parsed AST")
    ast_parser.add_argument("file", type=Path)
    ast_parser.add_argument("--json", action="store_true", help="Print JSON-friendly AST")
    ast_parser.set_defaults(func=command_ast)

    shell_parser = subparsers.add_parser("shell", help="Start the interactive shell")
    shell_parser.set_defaults(func=command_shell)

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
    except (NovaLexerError, NovaSyntaxError, NovaRuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
