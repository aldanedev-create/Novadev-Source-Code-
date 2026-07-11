from __future__ import annotations

"""Beginner-friendly semantic checks for NovaDev 1.0."""

from dataclasses import dataclass, field
from typing import List

from .ast_nodes import Program
from .runtime import Runtime


@dataclass
class SemanticReport:
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


class SemanticAnalyzer:
    def analyze(self, program: Program) -> SemanticReport:
        report = SemanticReport()
        app = program.app
        runtime = Runtime()
        runtime.load_declarations(program)
        if app and not runtime.pages and (app.frontend or app.stack):
            report.warnings.append("app has a frontend target but no page declarations")
        if app and app.backend and not runtime.routes and not runtime.tables:
            report.warnings.append("app has a backend target but no tables or routes")
        return report
