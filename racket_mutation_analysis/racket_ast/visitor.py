from .scheme_reader import (
    ASTNode, Boolean, Character, Expression, Identifier, LiteralVal, Number, Pair, Program,
    QuasiQuotedExpr, QuotedExpr, SList, String, UnquotedExpr, UnquoteSplicingExpr
)


class Visitor:
    def visit(self, node: ASTNode):
        self.visit_ASTNode(node)

    def visit_ASTNode(self, node: ASTNode):
        match(node):
            case Program():
                self.visit_Program(node)
            case Expression():
                self.visit_Expression(node)
            case _:
                assert False

    def visit_Program(self, node: Program):
        for child in node.children:
            self.visit_ASTNode(child)

    def visit_Expression(self, node: Expression):
        match(node):
            case SList():
                self.visit_SList(node)
            case Pair():
                self.visit_Pair(node)
            case QuotedExpr():
                self.visit_QuotedExpr(node)
            case QuasiQuotedExpr():
                self.visit_QuasiQuotedExpr(node)
            case UnquotedExpr():
                self.visit_UnquotedExpr(node)
            case UnquoteSplicingExpr():
                self.visit_UnquoteSplicingExpr(node)
            case Identifier():
                self.visit_Identifier(node)
            case LiteralVal():
                self.visit_LiteralVal(node)
            case _:
                assert False

    def visit_SList(self, node: SList):
        for child in node.children:
            self.visit_ASTNode(child)

    def visit_Pair(self, node: Pair):
        for child in node.children:
            self.visit_ASTNode(child)

    def visit_QuotedExpr(self, node: QuotedExpr):
        for child in node.children:
            self.visit_ASTNode(child)

    def visit_QuasiQuotedExpr(self, node: QuasiQuotedExpr):
        for child in node.children:
            self.visit_ASTNode(child)

    def visit_UnquotedExpr(self, node: UnquotedExpr):
        for child in node.children:
            self.visit_ASTNode(child)

    def visit_UnquoteSplicingExpr(self, node: UnquoteSplicingExpr):
        for child in node.children:
            self.visit_ASTNode(child)

    def visit_Identifier(self, node: Identifier):
        pass

    def visit_LiteralVal(self, node: LiteralVal):
        match(node):
            case String():
                self.visit_String(node)
            case Boolean():
                self.visit_Boolean(node)
            case Character():
                self.visit_Character(node)
            case Number():
                self.visit_Number(node)
            case _:
                assert False

    def visit_String(self, node: String):
        pass

    def visit_Boolean(self, node: Boolean):
        pass

    def visit_Character(self, node: Character):
        pass

    def visit_Number(self, node: Number):
        pass
