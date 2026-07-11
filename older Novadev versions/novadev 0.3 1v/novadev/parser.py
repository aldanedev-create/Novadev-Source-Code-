from __future__ import annotations

"""Recursive-descent parser for NovaDev 0.3.

The parser consumes lexer tokens and creates AST nodes. It understands both the
full-stack NovaDev declarations (`app`, `table`, `page`, `route`, `theme`) and a
small dynamic programming language (`let`, `print`, `if`, `while`, `function`).
"""

from typing import Any, Iterable, List, Optional

from .ast_nodes import (
    AppNode,
    AssignNode,
    AuthNode,
    BinaryOpNode,
    CallNode,
    ComponentNode,
    FieldNode,
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
from .lexer import Lexer, Token


class NovaSyntaxError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        if token:
            super().__init__(f"{message} at line {token.line}, column {token.column}")
        else:
            super().__init__(message)
        self.token = token


NAME_TOKENS = {
    "IDENTIFIER",
    "APP",
    "THEME",
    "USE",
    "TABLE",
    "PAGE",
    "ROUTE",
    "AUTH",
    "REQUIRE",
    "ROLE",
    "RETURN",
    "FORM",
    "CHART",
    "CARD",
    "MODAL",
    "NAVBAR",
    "SIDEBAR",
    "LINK",
    "TO",
    "COLUMNS",
    "ACTIONS",
    "FIELDS",
    "SUBMIT",
    "VALUE",
    "TYPE",
    "TEXT",
    "BUTTON",
    "IF",
    "ELSE",
    "WHILE",
    "FUNCTION",
    "LET",
    "PRINT",
}


DECLARATION_TYPES = (TableNode, PageNode, RouteNode, ThemeNode, AuthNode)


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        body: List[Any] = []
        app: Optional[AppNode] = None

        while not self.at_end():
            self.skip_newlines()
            if self.at_end():
                break
            node = self.statement()
            body.append(node)
            if isinstance(node, AppNode):
                app = node

        if app is None:
            declarations = [node for node in body if isinstance(node, DECLARATION_TYPES) or self.is_use_theme(node)]
            if declarations:
                app = AppNode("NovaDevApp")
                for node in declarations:
                    app.add_member(node)

        return Program(body=body, app=app)

    def statement(self) -> Any:
        self.skip_newlines()
        if self.match("APP"):
            return self.app_declaration()
        if self.match("TABLE"):
            return self.table_declaration()
        if self.match("PAGE"):
            return self.page_declaration()
        if self.match("ROUTE"):
            return self.route_declaration()
        if self.match("THEME"):
            return self.theme_declaration()
        if self.match("AUTH"):
            return self.auth_declaration()
        if self.match("USE"):
            return self.use_declaration()
        if self.match("FUNCTION"):
            return self.function_declaration()
        if self.match("LET"):
            return self.let_statement()
        if self.match("PRINT"):
            return self.print_statement()
        if self.match("IF"):
            return self.if_statement()
        if self.match("WHILE"):
            return self.while_statement()
        if self.match("RETURN"):
            return self.return_statement()
        if self.check("IDENTIFIER") and self.check_next("EQUAL"):
            return self.assignment_statement()

        expression = self.expression()
        self.consume_statement_end()
        return expression

    def app_declaration(self) -> AppNode:
        name = self.consume_word("Expected app name after 'app'")
        app = AppNode(name)
        self.consume("LBRACE", "Expected '{' after app name")

        while not self.check("RBRACE") and not self.at_end():
            self.skip_newlines()
            if self.check("RBRACE"):
                break
            member = self.statement()
            app.add_member(member)

        self.consume("RBRACE", "Expected '}' to close app block")
        self.consume_statement_end()
        return app

    def table_declaration(self) -> TableNode:
        name = self.consume_word("Expected table name after 'table'")
        table = TableNode(name)
        self.consume("LBRACE", "Expected '{' after table name")

        while not self.check("RBRACE") and not self.at_end():
            self.skip_newlines()
            if self.check("RBRACE"):
                break
            field_name = self.consume_word("Expected field name in table")
            field_type = self.consume_word("Expected field type after field name")
            attributes = self.name_list_until_line_or_brace()
            table.fields.append(FieldNode(field_name, field_type, attributes))
            self.consume_statement_end()

        self.consume("RBRACE", "Expected '}' to close table block")
        self.consume_statement_end()
        return table

    def theme_declaration(self) -> ThemeNode:
        name = self.consume_word("Expected theme name after 'theme'")
        theme = ThemeNode(name)
        self.consume("LBRACE", "Expected '{' after theme name")

        while not self.check("RBRACE") and not self.at_end():
            self.skip_newlines()
            if self.check("RBRACE"):
                break
            key = self.consume_word("Expected theme property name")
            value = self.expression()
            theme.values[key] = value.value if isinstance(value, LiteralNode) else value
            self.consume_statement_end()

        self.consume("RBRACE", "Expected '}' to close theme block")
        self.consume_statement_end()
        return theme

    def auth_declaration(self) -> AuthNode:
        table_name = self.consume_word("Expected auth table name")
        self.consume_statement_end()
        return AuthNode(table_name)

    def use_declaration(self) -> ComponentNode:
        kind = self.consume_word("Expected what to use, like: use theme CyberDark")
        if kind != "theme":
            raise NovaSyntaxError("NovaDev 0.3 currently supports 'use theme ThemeName'", self.previous())
        theme_name = self.consume_word("Expected theme name after 'use theme'")
        self.consume_statement_end()
        return ComponentNode("use_theme", name=theme_name)

    def route_declaration(self) -> RouteNode:
        method = self.consume_word("Expected HTTP method after 'route'").upper()
        path_token = self.consume("STRING", 'Expected route path string, like "/api/products"')
        route = RouteNode(method=method, path=path_token.value)
        self.consume("LBRACE", "Expected '{' after route path")

        while not self.check("RBRACE") and not self.at_end():
            self.skip_newlines()
            if self.check("RBRACE"):
                break
            if self.match("REQUIRE"):
                self.apply_require(route)
                self.consume_statement_end()
            elif self.match("RETURN"):
                node = self.return_statement(already_matched=True)
                route.return_expr = node.expression
                route.body.append(node)
            else:
                route.body.append(self.statement())

        self.consume("RBRACE", "Expected '}' to close route block")
        self.consume_statement_end()
        return route

    def page_declaration(self) -> PageNode:
        name = self.consume_word("Expected page name after 'page'")
        page = PageNode(name=name, title=name)
        self.consume("LBRACE", "Expected '{' after page name")

        while not self.check("RBRACE") and not self.at_end():
            self.skip_newlines()
            if self.check("RBRACE"):
                break
            item = self.page_item(page)
            if isinstance(item, ComponentNode):
                page.components.append(item)
            page.body.append(item)

        self.consume("RBRACE", "Expected '}' to close page block")
        self.consume_statement_end()
        return page

    def page_item(self, page: PageNode) -> Any:
        if self.match("REQUIRE"):
            self.apply_require(page)
            self.consume_statement_end()
            return ComponentNode("require", props={"auth": page.requires_auth, "role": page.required_role})
        if self.check_value("title"):
            self.advance()
            title = self.consume_title_value("Expected quoted title after title")
            self.consume_statement_end()
            page.title = title
            return ComponentNode("title", name=title)
        if self.match("SIDEBAR"):
            return self.link_container("sidebar")
        if self.match("NAVBAR"):
            return self.link_container("navbar")
        if self.match("CARD"):
            return self.card_component()
        if self.match("CHART"):
            return self.chart_component()
        if self.match("FORM"):
            return self.form_component()
        if self.match("TABLE"):
            return self.table_component()
        if self.match("MODAL"):
            return self.modal_component()
        if self.match("BUTTON"):
            return self.button_component()
        return self.statement()

    def apply_require(self, target: Any) -> None:
        if self.match("AUTH"):
            target.requires_auth = True
            return
        if self.match("ROLE"):
            target.required_role = self.consume_word("Expected role name after 'require role'")
            target.requires_auth = True
            return
        raise NovaSyntaxError("Expected 'require auth' or 'require role Name'", self.peek())

    def link_container(self, kind: str) -> ComponentNode:
        self.consume("LBRACE", f"Expected '{{' after {kind}")
        links: List[ComponentNode] = []
        while not self.check("RBRACE") and not self.at_end():
            self.skip_newlines()
            if self.check("RBRACE"):
                break
            self.consume("LINK", f"Expected link inside {kind}")
            label = self.consume_title_value("Expected quoted link label")
            self.consume("TO", "Expected 'to' in link declaration")
            target = self.consume_title_value("Expected quoted link target")
            links.append(ComponentNode("link", name=label, props={"target": target}))
            self.consume_statement_end()

        self.consume("RBRACE", f"Expected '}}' to close {kind}")
        self.consume_statement_end()
        return ComponentNode(kind, children=links)

    def card_component(self) -> ComponentNode:
        title = self.consume_title_value("Expected card title")
        props: dict[str, Any] = {}
        if self.match("LBRACE"):
            while not self.check("RBRACE") and not self.at_end():
                self.skip_newlines()
                if self.check("RBRACE"):
                    break
                if self.match("VALUE"):
                    props["value"] = self.expression()
                elif self.match("TEXT"):
                    props["text"] = self.expression()
                else:
                    key = self.consume_word("Expected card property name")
                    props[key] = self.expression()
                self.consume_statement_end()
            self.consume("RBRACE", "Expected '}' to close card block")
        self.consume_statement_end()
        return ComponentNode("card", name=title, props=props)

    def chart_component(self) -> ComponentNode:
        source = self.consume_word("Expected chart source table")
        props = {"type": "line", "x": "", "y": ""}
        if self.match("LBRACE"):
            while not self.check("RBRACE") and not self.at_end():
                self.skip_newlines()
                if self.check("RBRACE"):
                    break
                key = self.consume_word("Expected chart property name")
                if key not in {"type", "x", "y"}:
                    raise NovaSyntaxError("Charts support type, x, and y properties", self.previous())
                props[key] = self.consume_word(f"Expected value after chart {key}")
                self.consume_statement_end()
            self.consume("RBRACE", "Expected '}' to close chart block")
        self.consume_statement_end()
        return ComponentNode("chart", name=source, props=props)

    def form_component(self) -> ComponentNode:
        table_name = self.consume_word("Expected form table name")
        props: dict[str, Any] = {"fields": [], "submit": "Save"}
        if self.match("LBRACE"):
            while not self.check("RBRACE") and not self.at_end():
                self.skip_newlines()
                if self.check("RBRACE"):
                    break
                if self.match("FIELDS"):
                    props["fields"] = self.name_list_until_line_or_brace()
                elif self.match("SUBMIT"):
                    props["submit"] = self.consume_title_value("Expected submit button text")
                else:
                    raise NovaSyntaxError("Forms support fields and submit properties", self.peek())
                self.consume_statement_end()
            self.consume("RBRACE", "Expected '}' to close form block")
        self.consume_statement_end()
        return ComponentNode("form", name=table_name, props=props)

    def table_component(self) -> ComponentNode:
        table_name = self.consume_word("Expected table source name")
        props: dict[str, Any] = {"columns": [], "actions": []}
        if self.match("LBRACE"):
            while not self.check("RBRACE") and not self.at_end():
                self.skip_newlines()
                if self.check("RBRACE"):
                    break
                if self.match("COLUMNS"):
                    props["columns"] = self.name_list_until_line_or_brace()
                elif self.match("ACTIONS"):
                    props["actions"] = self.name_list_until_line_or_brace()
                else:
                    raise NovaSyntaxError("Table components support columns and actions", self.peek())
                self.consume_statement_end()
            self.consume("RBRACE", "Expected '}' to close table block")
        self.consume_statement_end()
        return ComponentNode("table", name=table_name, props=props)

    def modal_component(self) -> ComponentNode:
        title = self.consume_title_value("Expected modal title")
        props: dict[str, Any] = {"text": "", "button": "Close"}
        self.consume("LBRACE", "Expected '{' after modal title")
        while not self.check("RBRACE") and not self.at_end():
            self.skip_newlines()
            if self.check("RBRACE"):
                break
            if self.match("TEXT"):
                value = self.expression()
                props["text"] = value.value if isinstance(value, LiteralNode) else value
            elif self.match("BUTTON"):
                props["button"] = self.consume_title_value("Expected modal button label")
            else:
                raise NovaSyntaxError("Modals support text and button properties", self.peek())
            self.consume_statement_end()
        self.consume("RBRACE", "Expected '}' to close modal block")
        self.consume_statement_end()
        return ComponentNode("modal", name=title, props=props)

    def button_component(self) -> ComponentNode:
        label = self.consume_title_value("Expected button label")
        props: dict[str, Any] = {}
        if self.match("TO"):
            props["to"] = self.consume_title_value("Expected button target after to")
        self.consume_statement_end()
        return ComponentNode("button", name=label, props=props)

    def function_declaration(self) -> FunctionNode:
        name = self.consume_word("Expected function name")
        self.consume("LPAREN", "Expected '(' after function name")
        params: List[str] = []
        if not self.check("RPAREN"):
            while True:
                params.append(self.consume_word("Expected parameter name"))
                if not self.match("COMMA"):
                    break
        self.consume("RPAREN", "Expected ')' after function parameters")
        body = self.block("function")
        self.consume_statement_end()
        return FunctionNode(name, params, body)

    def let_statement(self) -> LetNode:
        name = self.consume_word("Expected variable name after 'let'")
        self.consume("EQUAL", "Expected '=' after variable name")
        expression = self.expression()
        self.consume_statement_end()
        return LetNode(name, expression)

    def assignment_statement(self) -> AssignNode:
        name = self.advance().value
        self.consume("EQUAL", "Expected '=' in assignment")
        expression = self.expression()
        self.consume_statement_end()
        return AssignNode(name, expression)

    def print_statement(self) -> PrintNode:
        if self.match("LPAREN"):
            expression = self.expression()
            self.consume("RPAREN", "Expected ')' after print expression")
        else:
            expression = self.expression()
        self.consume_statement_end()
        return PrintNode(expression)

    def if_statement(self) -> IfNode:
        condition = self.expression()
        then_body = self.block("if")
        self.skip_newlines()
        else_body: List[Any] = []
        if self.match("ELSE"):
            if self.match("IF"):
                else_body = [self.if_statement()]
            else:
                else_body = self.block("else")
        self.consume_statement_end()
        return IfNode(condition, then_body, else_body)

    def while_statement(self) -> WhileNode:
        condition = self.expression()
        body = self.block("while")
        self.consume_statement_end()
        return WhileNode(condition, body)

    def return_statement(self, already_matched: bool = False) -> ReturnNode:
        if not already_matched:
            pass
        if self.check("NEWLINE") or self.check("RBRACE") or self.check("EOF"):
            expression = None
        else:
            expression = self.expression()
        self.consume_statement_end()
        return ReturnNode(expression)

    def block(self, label: str) -> List[Any]:
        self.consume("LBRACE", f"Expected '{{' after {label} condition/header")
        statements: List[Any] = []
        while not self.check("RBRACE") and not self.at_end():
            self.skip_newlines()
            if self.check("RBRACE"):
                break
            statements.append(self.statement())
        self.consume("RBRACE", f"Expected '}}' to close {label} block")
        return statements

    def expression(self) -> Any:
        return self.or_expression()

    def or_expression(self) -> Any:
        expr = self.and_expression()
        while self.match("OR_OR"):
            operator = self.previous().value
            right = self.and_expression()
            expr = BinaryOpNode(expr, operator, right)
        return expr

    def and_expression(self) -> Any:
        expr = self.equality()
        while self.match("AND_AND"):
            operator = self.previous().value
            right = self.equality()
            expr = BinaryOpNode(expr, operator, right)
        return expr

    def equality(self) -> Any:
        expr = self.comparison()
        while self.match("EQUAL_EQUAL", "BANG_EQUAL"):
            operator = self.previous().value
            right = self.comparison()
            expr = BinaryOpNode(expr, operator, right)
        return expr

    def comparison(self) -> Any:
        expr = self.term()
        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous().value
            right = self.term()
            expr = BinaryOpNode(expr, operator, right)
        return expr

    def term(self) -> Any:
        expr = self.factor()
        while self.match("PLUS", "MINUS"):
            operator = self.previous().value
            right = self.factor()
            expr = BinaryOpNode(expr, operator, right)
        return expr

    def factor(self) -> Any:
        expr = self.unary()
        while self.match("STAR", "SLASH"):
            operator = self.previous().value
            right = self.unary()
            expr = BinaryOpNode(expr, operator, right)
        return expr

    def unary(self) -> Any:
        if self.match("MINUS"):
            return UnaryOpNode("-", self.unary())
        return self.call()

    def call(self) -> Any:
        expr = self.primary()
        while True:
            if self.match("DOT"):
                name = self.consume_word("Expected property name after '.'")
                if isinstance(expr, IdentifierNode):
                    expr = IdentifierNode(expr.name + "." + name)
                else:
                    raise NovaSyntaxError("Only identifiers can use dotted calls in NovaDev 0.3", self.previous())
            elif self.match("LPAREN"):
                args: List[Any] = []
                if not self.check("RPAREN"):
                    while True:
                        args.append(self.expression())
                        if not self.match("COMMA"):
                            break
                self.consume("RPAREN", "Expected ')' after arguments")
                expr = CallNode(expr, args)
            else:
                break
        return expr

    def primary(self) -> Any:
        if self.match("NUMBER", "STRING", "BOOLEAN", "NIL"):
            return LiteralNode(self.previous().value)
        if self.check_any(NAME_TOKENS):
            return IdentifierNode(self.advance().value)
        if self.match("LPAREN"):
            expr = self.expression()
            self.consume("RPAREN", "Expected ')' after expression")
            return expr
        raise NovaSyntaxError("Expected expression", self.peek())

    def consume_title_value(self, message: str) -> str:
        if self.match("STRING"):
            return self.previous().value
        return self.consume_word(message)

    def name_list_until_line_or_brace(self) -> List[str]:
        names: List[str] = []
        while not self.check("NEWLINE") and not self.check("RBRACE") and not self.check("EOF"):
            if self.match("COMMA"):
                continue
            names.append(self.consume_word("Expected name in list"))
        return names

    def consume_statement_end(self) -> None:
        while self.match("NEWLINE"):
            pass

    def skip_newlines(self) -> None:
        while self.match("NEWLINE"):
            pass

    def consume_word(self, message: str) -> str:
        if self.check_any(NAME_TOKENS):
            return str(self.advance().value)
        raise NovaSyntaxError(message, self.peek())

    def check_value(self, value: str) -> bool:
        return str(self.peek().value).lower() == value.lower()

    def is_use_theme(self, node: Any) -> bool:
        return isinstance(node, ComponentNode) and node.kind == "use_theme"

    def match(self, *types: str) -> bool:
        if self.check_any(types):
            self.advance()
            return True
        return False

    def consume(self, token_type: str, message: str) -> Token:
        if self.check(token_type):
            return self.advance()
        raise NovaSyntaxError(message, self.peek())

    def check(self, token_type: str) -> bool:
        if self.at_end():
            return token_type == "EOF"
        return self.peek().type == token_type

    def check_any(self, types: Iterable[str]) -> bool:
        if self.at_end():
            return False
        return self.peek().type in types

    def check_next(self, token_type: str) -> bool:
        if self.current + 1 >= len(self.tokens):
            return False
        return self.tokens[self.current + 1].type == token_type

    def advance(self) -> Token:
        if not self.at_end():
            self.current += 1
        return self.previous()

    def at_end(self) -> bool:
        return self.peek().type == "EOF"

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]


class NovaParser(Parser):
    """Compatibility wrapper: old code passed source text directly."""

    def __init__(self, source: str):
        super().__init__(Lexer(source).tokenize())


def parse_source(source: str) -> Program:
    return NovaParser(source).parse()
