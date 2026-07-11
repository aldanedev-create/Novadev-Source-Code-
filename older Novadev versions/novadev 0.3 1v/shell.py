from __future__ import annotations

"""Interactive shell for NovaDev 0.3."""

from pathlib import Path

from novadev.interpreter import Interpreter
from novadev.lexer import NovaLexerError
from novadev.parser import NovaSyntaxError
from novadev.runtime import NovaRuntimeError


def main() -> int:
    interpreter = Interpreter()
    print("NovaDev 0.3 Interactive Shell")
    print("Type .exit to quit")

    buffer: list[str] = []
    prompt = "nova> "

    while True:
        try:
            line = input(prompt)
        except EOFError:
            print()
            return 0

        stripped = line.strip()
        if not buffer and not stripped:
            continue
        if not buffer and stripped == ".exit":
            return 0
        if not buffer and stripped.startswith(".load "):
            path = Path(stripped[len(".load ") :].strip())
            try:
                interpreter.run(path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                print(f"error: file not found: {path}")
            except (NovaLexerError, NovaSyntaxError, NovaRuntimeError) as exc:
                print(f"error: {exc}")
            continue

        buffer.append(line)
        source = "\n".join(buffer)
        if source.count("{") > source.count("}"):
            prompt = "... "
            continue

        try:
            interpreter.run(source)
        except (NovaLexerError, NovaSyntaxError, NovaRuntimeError) as exc:
            print(f"error: {exc}")
        finally:
            buffer.clear()
            prompt = "nova> "


if __name__ == "__main__":
    raise SystemExit(main())
