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


if __name__ == "__main__":
    unittest.main()
