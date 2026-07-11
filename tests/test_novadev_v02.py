from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from novadev.parser import NovaParser
from novadev.runtime import run_code
from novadev.interpreter import Interpreter
from novadev.lexer import tokenize
from novadev.codegen import BackendGenerator
from novadev.semantic import SemanticAnalyzer
from novadev.ui.html_generator import UIGenerator


class NovaDevV02Tests(unittest.TestCase):
    def test_parser_builds_app_ast(self):
        source = (ROOT / "examples" / "dashboard.nova").read_text(encoding="utf-8")
        program = NovaParser(source).parse()

        self.assertIsNotNone(program.app)
        self.assertIn("User", program.app.tables)
        self.assertIn("Product", program.app.tables)
        self.assertEqual(program.app.pages[0].route_path, "/admin-dashboard")

    def test_semantic_analysis_accepts_dashboard(self):
        source = (ROOT / "examples" / "dashboard.nova").read_text(encoding="utf-8")
        program = NovaParser(source).parse()
        analysis = SemanticAnalyzer().analyze(program, source)

        self.assertTrue(analysis.ok, [error.message for error in analysis.errors])

    def test_generator_writes_frontend_files(self):
        source = (ROOT / "examples" / "products.nova").read_text(encoding="utf-8")
        program = NovaParser(source).parse()

        with tempfile.TemporaryDirectory() as tmp:
            generated = UIGenerator().generate(program.app, Path(tmp))
            generated_names = {path.name for path in generated}

        self.assertIn("index.html", generated_names)
        self.assertIn("styles.css", generated_names)
        self.assertIn("app.js", generated_names)
        self.assertIn("schema.json", generated_names)

    def test_runtime_still_runs_hello_style_code(self):
        output = io.StringIO()
        with redirect_stdout(output):
            run_code('let name = "Aldane"\nprint("Hello " + name)\n')

        self.assertEqual(output.getvalue().strip(), "Hello Aldane")

    def test_runtime_supports_index_expressions(self):
        output = io.StringIO()
        with redirect_stdout(output):
            run_code(
                "\n".join(
                    [
                        'let skills = ["NovaDev", "Python", "Vue"]',
                        'let profile = { name: "Aldane", role: "Developer" }',
                        "print(skills[0])",
                        'print(profile["role"])',
                        'print("NovaDev"[4])',
                    ]
                )
            )

        self.assertEqual(output.getvalue().strip().splitlines(), ["NovaDev", "Developer", "D"])

    def test_runtime_supports_index_assignment_and_interpolation(self):
        output = io.StringIO()
        with redirect_stdout(output):
            run_code(
                "\n".join(
                    [
                        'let skills = ["NovaDev", "Python", "Vue",]',
                        "skills[1] = \"Tailwind\"",
                        'let profile = { name: "Aldane", role: "Developer" }',
                        'profile["role"] = "Builder"',
                        'print("Skill {skills[1]} for {profile.role}")',
                    ]
                )
            )

        self.assertEqual(output.getvalue().strip(), "Skill Tailwind for Builder")

    def test_interpreter_tracks_last_expression_value(self):
        runtime = Interpreter().run("3 + 4")

        self.assertEqual(runtime.last_value, 7)

    def test_triple_quoted_strings_support_multiline_text(self):
        output = io.StringIO()
        source = (
            'let css = """body {\n    color: red;\n}""" \n'
            "let html = '''<main>\n    <h1>NovaDev</h1>\n</main>'''\n"
            "print(css)\n"
            "print(html)\n"
        )

        with redirect_stdout(output):
            run_code(source)

        self.assertIn("body {\n    color: red;\n}", output.getvalue())
        self.assertIn("<main>\n    <h1>NovaDev</h1>\n</main>", output.getvalue())

    def test_single_quoted_strings_tokenize_like_strings(self):
        values = [token.value for token in tokenize("let name = 'Aldane'\n") if token.type == "STRING"]

        self.assertEqual(values, ["Aldane"])

    def test_manager_uses_instance_notebook(self):
        manager_source = (ROOT / "novadev_manager.py").read_text(encoding="utf-8")

        self.assertNotIn("ttk.Frame(notebook", manager_source)
        self.assertIn("ttk.Frame(self.notebook", manager_source)

    def test_backend_generator_writes_sqlalchemy_sqlite_backend(self):
        program = NovaParser(
            """
            app Store {
                project {
                    backend Flask
                    database SQLite
                }

                table Product {
                    id auto
                    name text
                    price number
                }
            }
            """
        ).parse()

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "backend"
            BackendGenerator().generate(program, output, Path(tmp) / "frontend")
            requirements = (output / "requirements.txt").read_text(encoding="utf-8")
            config = (output / "config.py").read_text(encoding="utf-8")
            models = (output / "models.py").read_text(encoding="utf-8")

        self.assertIn("SQLAlchemy>=2.0,<3.0", requirements)
        self.assertIn("DATABASE_PATH = BACKEND_DIR / \"database.db\"", config)
        self.assertIn("import sqlite3", models)
        self.assertIn("from sqlalchemy import", models)
        self.assertIn("create_engine", models)
        self.assertIn("metadata.create_all(engine)", models)


if __name__ == "__main__":
    unittest.main()
