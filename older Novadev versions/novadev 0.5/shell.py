from __future__ import annotations

"""Interactive shell and shell-side command runner for NovaDev 0.5."""

import json
import pprint
import shlex
import sys
from pathlib import Path
from typing import List, Optional, Tuple

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
from novadev.ui_generator import UIGenerator
from novadev.vue_generator import VueGenerator


SHELL_HELP = """NovaDev shell commands:
  .help
  .version
  .exit
  .load <file>
  .run <file>
  .tokens <file>
  .ast <file> [--json]
  .build-ui <file> [-o output_dir]
  .build-backend <file> [-o output_dir] [--frontend dist]
  .build-app <file> [--ui-output dist] [--backend-output generated_backend]
  .build <file> [-o generated]
  .build-vue <file> [-o output_dir]
  .build-fullstack <file> [-o generated]

You can also type NovaDev code directly:
  let name = "Aldane"
  print(name)

For multi-line if/while/function blocks, press a blank line after the closing
brace to run the block.
"""


def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_file(path: Path):
    return compile_file(path)


def split_shell_command(line: str) -> List[str]:
    """Split a shell command while preserving Windows backslashes."""
    parts = shlex.split(line, posix=False)
    return [strip_quotes(part) for part in parts]


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_output_args(args: List[str], default_output: str) -> Tuple[Path, Path]:
    file_path: Optional[Path] = None
    output_path = Path(default_output)
    index = 0

    while index < len(args):
        arg = args[index]
        if arg in {"-o", "--output"}:
            index += 1
            if index >= len(args):
                raise ValueError(f"{arg} needs an output folder")
            output_path = Path(args[index])
        elif arg.startswith("--output="):
            output_path = Path(arg.split("=", 1)[1])
        elif file_path is None:
            file_path = Path(arg)
        else:
            raise ValueError(f"Unexpected argument: {arg}")
        index += 1

    if file_path is None:
        raise ValueError("Expected a .nova file path")
    return file_path, output_path


def parse_backend_args(args: List[str]) -> Tuple[Path, Path, Path, Optional[str]]:
    file_path: Optional[Path] = None
    output_path = Path("generated_backend")
    frontend_path = Path("dist")
    target: Optional[str] = None
    index = 0

    while index < len(args):
        arg = args[index]
        if arg in {"-o", "--output"}:
            index += 1
            if index >= len(args):
                raise ValueError(f"{arg} needs an output folder")
            output_path = Path(args[index])
        elif arg.startswith("--output="):
            output_path = Path(arg.split("=", 1)[1])
        elif arg == "--frontend":
            index += 1
            if index >= len(args):
                raise ValueError("--frontend needs a frontend folder")
            frontend_path = Path(args[index])
        elif arg.startswith("--frontend="):
            frontend_path = Path(arg.split("=", 1)[1])
        elif arg == "--target":
            index += 1
            if index >= len(args):
                raise ValueError("--target needs Flask, FastAPI, Express, or Django")
            target = args[index]
        elif arg.startswith("--target="):
            target = arg.split("=", 1)[1]
        elif file_path is None:
            file_path = Path(arg)
        else:
            raise ValueError(f"Unexpected argument: {arg}")
        index += 1

    if file_path is None:
        raise ValueError("Expected a .nova file path")
    return file_path, output_path, frontend_path, target


def parse_build_app_args(args: List[str]) -> Tuple[Path, Path, Path]:
    file_path: Optional[Path] = None
    ui_output = Path("dist")
    backend_output = Path("generated_backend")
    index = 0

    while index < len(args):
        arg = args[index]
        if arg == "--ui-output":
            index += 1
            if index >= len(args):
                raise ValueError("--ui-output needs a folder")
            ui_output = Path(args[index])
        elif arg.startswith("--ui-output="):
            ui_output = Path(arg.split("=", 1)[1])
        elif arg == "--backend-output":
            index += 1
            if index >= len(args):
                raise ValueError("--backend-output needs a folder")
            backend_output = Path(args[index])
        elif arg.startswith("--backend-output="):
            backend_output = Path(arg.split("=", 1)[1])
        elif file_path is None:
            file_path = Path(arg)
        else:
            raise ValueError(f"Unexpected argument: {arg}")
        index += 1

    if file_path is None:
        raise ValueError("Expected a .nova file path")
    return file_path, ui_output, backend_output


def parse_project_build_args(args: List[str]) -> Tuple[Path, Path]:
    file_path: Optional[Path] = None
    output_path = Path("generated")
    index = 0

    while index < len(args):
        arg = args[index]
        if arg in {"-o", "--output"}:
            index += 1
            if index >= len(args):
                raise ValueError(f"{arg} needs an output folder")
            output_path = Path(args[index])
        elif arg.startswith("--output="):
            output_path = Path(arg.split("=", 1)[1])
        elif file_path is None:
            file_path = Path(arg)
        else:
            raise ValueError(f"Unexpected argument: {arg}")
        index += 1

    if file_path is None:
        raise ValueError("Expected a .nova file path")
    return file_path, output_path


def parse_ast_args(args: List[str]) -> Tuple[Path, bool]:
    file_path: Optional[Path] = None
    as_json = False
    for arg in args:
        if arg == "--json":
            as_json = True
        elif file_path is None:
            file_path = Path(arg)
        else:
            raise ValueError(f"Unexpected argument: {arg}")
    if file_path is None:
        raise ValueError("Expected a .nova file path")
    return file_path, as_json


def one_file_arg(args: List[str]) -> Path:
    if len(args) != 1:
        raise ValueError("Expected exactly one .nova file path")
    return Path(args[0])


def execute_command(command: str, args: List[str], interpreter: Optional[Interpreter] = None) -> int:
    command = command.lower()

    if command in {"help", "-h", "--help"}:
        print(SHELL_HELP)
        return 0

    if command in {"version", "--version"}:
        print(f"NovaDev {__version__}")
        return 0

    if command == "shell":
        return interactive_main()

    if command in {"load", "run"}:
        path = one_file_arg(args)
        active_interpreter = interpreter or Interpreter()
        active_interpreter.run_program(parse_file(path))
        return 0

    if command == "tokens":
        path = one_file_arg(args)
        for token in tokenize(read_source(path)):
            print(f"{token.line}:{token.column}\t{token.type:<15}\t{token.display_value()}")
        return 0

    if command == "ast":
        path, as_json = parse_ast_args(args)
        program = parse_file(path)
        if as_json:
            print(json.dumps(node_to_data(program), indent=2))
        else:
            pprint.pp(program)
        return 0

    if command == "build-ui":
        path, output = parse_output_args(args, "dist")
        generated = UIGenerator().generate(parse_file(path), output)
        print(f"NovaDev {__version__} UI generated in {output}")
        for item in generated:
            print(f"  {item}")
        return 0

    if command == "build-backend":
        path, output, frontend, target = parse_backend_args(args)
        program = parse_file(path)
        app = program.app
        selected = target or (backend_target(app) if app else "Flask")
        generated = BackendTargetGenerator().generate(program, output, frontend, selected)
        print(f"NovaDev {__version__} {selected} backend generated in {output}")
        for item in generated:
            print(f"  {item}")
        return 0

    if command == "build-app":
        path, ui_output, backend_output = parse_build_app_args(args)
        program = parse_file(path)
        ui_files = UIGenerator().generate(program, ui_output)
        backend_files = BackendGenerator().generate(program, backend_output, ui_output)
        print(f"NovaDev {__version__} app generated")
        print(f"  UI: {ui_output}")
        for item in ui_files:
            print(f"    {item}")
        print(f"  Flask backend: {backend_output}")
        for item in backend_files:
            print(f"    {item}")
        print("Run it with:")
        print(f"  cd {backend_output}")
        print("  python -m pip install -r requirements.txt")
        print("  python app.py")
        return 0

    if command == "build":
        path, output = parse_project_build_args(args)
        build = ProjectGenerator().generate(parse_file(path), output)
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

    if command == "build-vue":
        path, output = parse_project_build_args(args)
        program = parse_file(path)
        app_name = program.app.name if program.app else path.stem
        if str(output) == "generated":
            output = Path("generated") / slug_name(app_name) / "frontend"
        generated = VueGenerator().generate(program, output)
        print(f"NovaDev {__version__} Vue frontend generated in {output}")
        for item in generated:
            print(f"  {item}")
        return 0

    if command == "build-fullstack":
        path, output = parse_project_build_args(args)
        build = ProjectGenerator().generate(parse_file(path), output)
        print(f"NovaDev {__version__} fullstack project generated")
        print(f"  App: {build.app_name}")
        print(f"  Frontend: {build.frontend_dir}")
        print(f"  Backend: {build.backend_dir}")
        return 0

    raise ValueError(f"Unknown shell command: {command}")


def run_command_safely(command: str, args: List[str], interpreter: Optional[Interpreter] = None) -> int:
    try:
        return execute_command(command, args, interpreter)
    except FileNotFoundError as exc:
        print(f"error: file not found: {exc.filename}")
    except ValueError as exc:
        print(f"error: {exc}")
    except (NovaLexerError, NovaSyntaxError, NovaRuntimeError, ModuleResolutionError) as exc:
        print(f"error: {exc}")
    return 1


def brace_balance(source: str) -> int:
    """Count braces using lexer tokens so braces inside strings are ignored."""
    try:
        tokens = tokenize(source)
    except NovaLexerError:
        return source.count("{") - source.count("}")
    opens = sum(1 for token in tokens if token.type == "LBRACE")
    closes = sum(1 for token in tokens if token.type == "RBRACE")
    return opens - closes


def run_buffer(buffer: List[str], interpreter: Interpreter) -> None:
    source = "\n".join(buffer).strip()
    if not source:
        return
    try:
        interpreter.run(source)
    except (NovaLexerError, NovaSyntaxError, NovaRuntimeError) as exc:
        print(f"error: {exc}")


def handle_dot_command(line: str, interpreter: Interpreter) -> bool:
    try:
        parts = split_shell_command(line)
    except ValueError as exc:
        print(f"error: {exc}")
        return True

    if not parts:
        return True

    command = parts[0][1:].lower()
    args = parts[1:]

    if command == "exit":
        raise EOFError

    if command == "":
        print("error: empty shell command")
        return True

    run_command_safely(command, args, interpreter)
    return True


def interactive_main() -> int:
    interpreter = Interpreter()
    print("NovaDev 0.5 Interactive Shell")
    print("Type .help for commands")
    print("Type .exit to quit")
    print("Finish multi-line blocks with a blank line")

    buffer: list[str] = []
    prompt = "nova> "

    while True:
        try:
            line = input(prompt)
        except EOFError:
            print()
            return 0

        stripped = line.strip()

        if buffer and not stripped:
            source = "\n".join(buffer)
            if brace_balance(source) == 0:
                run_buffer(buffer, interpreter)
                buffer.clear()
                prompt = "nova> "
            else:
                prompt = "... "
            continue

        if not buffer and not stripped:
            continue

        if not buffer and stripped.startswith("."):
            try:
                handle_dot_command(stripped, interpreter)
            except EOFError:
                return 0
            continue

        buffer.append(line)
        source = "\n".join(buffer)

        balance = brace_balance(source)
        if balance > 0:
            prompt = "... "
            continue

        if balance < 0:
            run_buffer(buffer, interpreter)
            buffer.clear()
            prompt = "nova> "
            continue

        if len(buffer) > 1 and "{" in source:
            prompt = "... "
            continue

        run_buffer(buffer, interpreter)
        buffer.clear()
        prompt = "nova> "


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args:
        command = args[0]
        if command in {"-h", "--help"}:
            print(SHELL_HELP)
            return 0
        return run_command_safely(command, args[1:])
    return interactive_main()


if __name__ == "__main__":
    raise SystemExit(main())
