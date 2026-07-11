from __future__ import annotations

"""Runtime for NovaDev 0.3.

The runtime is the part of the language that gives AST nodes behavior. It stores
variables, calls functions, executes control flow, and keeps registries of app
declarations that generators can use later.
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from .ast_nodes import (
    AppNode,
    AssignNode,
    AuthNode,
    BinaryOpNode,
    CallNode,
    ComponentNode,
    FunctionNode,
    IdentifierNode,
    IfNode,
    LetNode,
    LiteralNode,
    PageNode,
    PrintNode,
    Program,
    ReturnNode,
    RouteNode,
    TableNode,
    ThemeNode,
    UnaryOpNode,
    WhileNode,
)
from .parser import parse_source


class NovaRuntimeError(Exception):
    """Raised when a valid AST cannot be executed safely."""


class NovaNameError(NovaRuntimeError):
    """Raised when a program reads a missing variable."""


class ReturnSignal(Exception):
    def __init__(self, value: Any):
        self.value = value


@dataclass
class Environment:
    values: Dict[str, Any] = field(default_factory=dict)
    parent: Optional["Environment"] = None

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def assign(self, name: str, value: Any) -> None:
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise NovaNameError(f"Variable '{name}' is not defined")

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise NovaNameError(f"Variable '{name}' is not defined")


class Runtime:
    def __init__(self, output: Callable[[str], None] | None = None):
        self.output = output or print
        self.environment = Environment()
        self.functions: Dict[str, FunctionNode] = {}
        self.apps: Dict[str, AppNode] = {}
        self.tables: Dict[str, TableNode] = {}
        self.table_data: Dict[str, List[Dict[str, Any]]] = {}
        self.pages: List[PageNode] = []
        self.routes: List[RouteNode] = []
        self.themes: Dict[str, ThemeNode] = {}
        self.auth_models: List[AuthNode] = []
        self.active_theme: Optional[str] = None

    def execute_program(self, program: Program) -> None:
        for node in program.body:
            self.execute(node)

    def load_declarations(self, program: Program) -> None:
        """Register app/table/page/route/theme nodes without running code."""
        for node in program.body:
            self.register_declaration(node)

    def execute(self, node: Any) -> Any:
        if isinstance(node, AppNode):
            self.register_app(node)
            for member in node.body:
                self.execute(member)
            return None
        if isinstance(node, TableNode):
            self.register_table(node)
            return None
        if isinstance(node, PageNode):
            self.register_page(node)
            return None
        if isinstance(node, RouteNode):
            self.register_route(node)
            return None
        if isinstance(node, ThemeNode):
            self.register_theme(node)
            return None
        if isinstance(node, AuthNode):
            self.auth_models.append(node)
            return None
        if isinstance(node, ComponentNode):
            if node.kind == "use_theme":
                self.active_theme = node.name
            return None
        if isinstance(node, FunctionNode):
            self.functions[node.name] = node
            self.environment.define(node.name, node)
            return None
        if isinstance(node, LetNode):
            self.environment.define(node.name, self.evaluate(node.expression))
            return None
        if isinstance(node, AssignNode):
            self.environment.assign(node.name, self.evaluate(node.expression))
            return None
        if isinstance(node, PrintNode):
            self.output(self.format_value(self.evaluate(node.expression)))
            return None
        if isinstance(node, IfNode):
            branch = node.then_body if self.truthy(self.evaluate(node.condition)) else node.else_body
            self.execute_block(branch, Environment(parent=self.environment))
            return None
        if isinstance(node, WhileNode):
            guard = 0
            while self.truthy(self.evaluate(node.condition)):
                self.execute_block(node.body, Environment(parent=self.environment))
                guard += 1
                if guard > 10000:
                    raise NovaRuntimeError("while loop stopped after 10000 iterations")
            return None
        if isinstance(node, ReturnNode):
            value = self.evaluate(node.expression) if node.expression is not None else None
            raise ReturnSignal(value)
        return self.evaluate(node)

    def execute_block(self, statements: List[Any], environment: Environment) -> None:
        previous = self.environment
        self.environment = environment
        try:
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def evaluate(self, node: Any) -> Any:
        if node is None:
            return None
        if isinstance(node, LiteralNode):
            return node.value
        if isinstance(node, IdentifierNode):
            return self.environment.get(node.name)
        if isinstance(node, UnaryOpNode):
            value = self.evaluate(node.expression)
            if node.operator == "-":
                return -value
            raise NovaRuntimeError(f"Unknown unary operator {node.operator}")
        if isinstance(node, BinaryOpNode):
            return self.evaluate_binary(node)
        if isinstance(node, CallNode):
            return self.call(node)
        raise NovaRuntimeError(f"Cannot evaluate node {node.__class__.__name__}")

    def evaluate_binary(self, node: BinaryOpNode) -> Any:
        if node.operator == "&&":
            return self.truthy(self.evaluate(node.left)) and self.truthy(self.evaluate(node.right))
        if node.operator == "||":
            return self.truthy(self.evaluate(node.left)) or self.truthy(self.evaluate(node.right))

        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.operator == "+":
            if isinstance(left, str) or isinstance(right, str):
                return f"{left}{right}"
            return left + right
        if node.operator == "-":
            return left - right
        if node.operator == "*":
            return left * right
        if node.operator == "/":
            return left / right
        if node.operator == "==":
            return left == right
        if node.operator == "!=":
            return left != right
        if node.operator == ">":
            return left > right
        if node.operator == ">=":
            return left >= right
        if node.operator == "<":
            return left < right
        if node.operator == "<=":
            return left <= right
        raise NovaRuntimeError(f"Unknown binary operator {node.operator}")

    def call(self, node: CallNode) -> Any:
        callee_name = self.callee_name(node.callee)
        args = [self.evaluate(arg) for arg in node.args]

        if callee_name == "print":
            self.output(" ".join(self.format_value(arg) for arg in args))
            return None
        if callee_name in self.functions:
            return self.call_user_function(self.functions[callee_name], args)

        table_name, _, method = callee_name.partition(".")
        if table_name in self.tables:
            rows = self.table_data.setdefault(table_name, [])
            if method == "count":
                return len(rows)
            if method == "all":
                return rows
            if method == "first":
                return rows[0] if rows else None

        raise NovaRuntimeError(f"Unknown function '{callee_name}'")

    def call_user_function(self, function: FunctionNode, args: List[Any]) -> Any:
        if len(args) != len(function.params):
            raise NovaRuntimeError(
                f"Function '{function.name}' expected {len(function.params)} argument(s), got {len(args)}"
            )
        local = Environment(parent=self.environment)
        for name, value in zip(function.params, args):
            local.define(name, value)
        try:
            self.execute_block(function.body, local)
        except ReturnSignal as signal:
            return signal.value
        return None

    def callee_name(self, node: Any) -> str:
        if isinstance(node, IdentifierNode):
            return node.name
        raise NovaRuntimeError("Can only call named functions in NovaDev 0.3")

    def register_declaration(self, node: Any) -> None:
        if isinstance(node, AppNode):
            self.register_app(node)
            for member in node.body:
                self.register_declaration(member)
        elif isinstance(node, TableNode):
            self.register_table(node)
        elif isinstance(node, PageNode):
            self.register_page(node)
        elif isinstance(node, RouteNode):
            self.register_route(node)
        elif isinstance(node, ThemeNode):
            self.register_theme(node)
        elif isinstance(node, AuthNode):
            self.auth_models.append(node)
        elif isinstance(node, ComponentNode) and node.kind == "use_theme":
            self.active_theme = node.name
        elif isinstance(node, FunctionNode):
            self.functions[node.name] = node

    def register_app(self, app: AppNode) -> None:
        self.apps[app.name] = app
        if app.active_theme:
            self.active_theme = app.active_theme

    def register_table(self, table: TableNode) -> None:
        self.tables[table.name] = table
        self.table_data.setdefault(table.name, [])

    def register_page(self, page: PageNode) -> None:
        if not any(existing.name == page.name for existing in self.pages):
            self.pages.append(page)

    def register_route(self, route: RouteNode) -> None:
        if not any(existing.method == route.method and existing.path == route.path for existing in self.routes):
            self.routes.append(route)

    def register_theme(self, theme: ThemeNode) -> None:
        self.themes[theme.name] = theme

    def truthy(self, value: Any) -> bool:
        return bool(value)

    def format_value(self, value: Any) -> str:
        if value is True:
            return "true"
        if value is False:
            return "false"
        if value is None:
            return "nil"
        return str(value)


def run_code(source: str) -> Runtime:
    program = parse_source(source)
    runtime = Runtime()
    runtime.execute_program(program)
    return runtime
