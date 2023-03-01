from racket_mutation_analysis.racket_ast.scheme_reader import (
    ASTNode, Identifier, LiteralVal, Pair, Program, QuasiQuotedExpr, QuotedExpr, SList,
    UnquotedExpr, UnquoteSplicingExpr
)
from racket_mutation_analysis.racket_ast.scheme_tokens import Location
from racket_mutation_analysis.racket_ast.visitor import Visitor


class ToStrVisitor(Visitor):
    def __init__(self):
        self.current_line = 0
        self.current_col = 0

        self.result = ''

        self.program: Program | None = None

    def _pad_until(self, loc: Location):
        while self.current_line < loc['line']:
            if self.program is not None and self.current_line in self.program.comments:
                comment = self.program.comments[self.current_line]
                self._pad_until(comment['start'])
                self.result += comment['token']

            self.result += '\n'
            self.current_line += 1
            self.current_col = 0

        while self.current_col < loc['column']:
            self.result += ' '
            self.current_col += 1

    def visit_ASTNode(self, node: ASTNode):
        if self.program is None and isinstance(node, Program):
            self.program = node

        self._pad_until(node.start_loc)
        super().visit_ASTNode(node)

    def visit_SList(self, node: SList):
        self.result += node.opening_bracket
        self.current_col += len(node.opening_bracket)

        super().visit_SList(node)

        # The end column stored in the node includes the closing ), but we
        # still need to print it ourselves.
        self._pad_until({'line': node.end_loc['line'], 'column': node.end_loc['column'] - 1})
        self.result += node.closing_bracket
        self.current_col += 1

    def visit_Pair(self, node: Pair):
        self.result += '('
        self.current_col += 1

        self.visit_ASTNode(node.first)
        self.result += '.'
        self.current_col += 1
        self.visit_ASTNode(node.second)

        # The end column stored in the node includes the closing ), but we
        # still need to print it ourselves.
        self._pad_until({'line': node.end_loc['line'], 'column': node.end_loc['column'] - 1})
        self.result += ')'
        self.current_col += 1

    def visit_QuotedExpr(self, node: QuotedExpr):
        self.result += "'"
        self.current_col += 1
        super().visit_QuotedExpr(node)

    def visit_QuasiQuotedExpr(self, node: QuasiQuotedExpr):
        self.result += '`'
        self.current_col += 1
        super().visit_QuasiQuotedExpr(node)

    def visit_UnquotedExpr(self, node: UnquotedExpr):
        self.result += ','
        self.current_col += 1
        super().visit_UnquotedExpr(node)

    def visit_UnquoteSplicingExpr(self, node: UnquoteSplicingExpr):
        self.result += ',@'
        self.current_col += 2
        super().visit_UnquoteSplicingExpr(node)

    def visit_Identifier(self, node: Identifier):
        self.result += node.name
        self.current_col += len(node.name)

    def visit_LiteralVal(self, node: LiteralVal):
        self.result += node.value
        self.current_col += len(node.value)
