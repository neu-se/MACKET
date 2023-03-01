# NOTE: This module has been modified, and the docstrings have not yet been
# updated. We've added type annotations in places where we've modified
# the behavior of functions.

"""This module implements a parser for Scheme expressions.

Pairs and lists are defined in scheme_core.py, as well as a
representation for an unspecified value. Other data types in Scheme
are represented by their corresponding type in Python:
    number:       int or float
    symbol:       string
    string:       quoted string
    boolean:      bool

Project UID 2d6261568f83a98aa474c0a2b04179ce000b9a48
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Sequence, TextIO, Type, TypeAlias

from .buffer import Buffer
from .scheme_tokens import PUNCTUATORS, Location, Token, Tokenizer


@dataclass
class ASTNode:
    start_loc: Location
    end_loc: Location

    @property
    def children(self) -> Sequence[ASTNode]:
        return []


@dataclass
class Program(ASTNode):
    expressions: Sequence[Expression]
    # Dict of {line #: comment token}
    comments: dict[int, Token]

    @property
    def children(self) -> Sequence[ASTNode]:
        return self.expressions


@dataclass
class Expression(ASTNode):
    pass


@dataclass
class SList(Expression):
    items: Sequence[Expression]

    opening_bracket: str = '('
    closing_bracket: str = ')'

    @property
    def is_nil(self) -> bool:
        return len(self.items) == 0

    @property
    def children(self) -> Sequence[ASTNode]:
        return self.items


@dataclass
class Pair(Expression):
    first: Expression
    second: Expression

    @property
    def children(self) -> Sequence[ASTNode]:
        return (self.first, self.second)


@dataclass
class QuotedExpr(Expression):
    expr: Expression

    @property
    def children(self) -> Sequence[ASTNode]:
        return (self.expr,)


@dataclass
class QuasiQuotedExpr(Expression):
    expr: Expression

    @property
    def children(self) -> Sequence[ASTNode]:
        return (self.expr,)


@dataclass
class UnquotedExpr(Expression):
    expr: Expression

    @property
    def children(self) -> Sequence[ASTNode]:
        return (self.expr,)


@dataclass
class UnquoteSplicingExpr(Expression):
    expr: Expression

    @property
    def children(self) -> Sequence[ASTNode]:
        return (self.expr,)


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class LiteralVal(Expression):
    value: str


@dataclass
class String(LiteralVal):
    pass


@dataclass
class Boolean(LiteralVal):
    pass


@dataclass
class Character(LiteralVal):
    pass


@dataclass
class Number(LiteralVal):
    pass


def token_to_node(token: Token) -> Expression:
    match(token['token_type']):
        case 'identifier':
            return Identifier(start_loc=token['start'], end_loc=token['end'], name=token['token'])
        case 'string':
            return String(start_loc=token['start'], end_loc=token['end'], value=token['token'])
        case 'boolean':
            return Boolean(start_loc=token['start'], end_loc=token['end'], value=token['token'])
        case 'character':
            return Character(start_loc=token['start'], end_loc=token['end'], value=token['token'])
        case 'number':
            return Number(start_loc=token['start'], end_loc=token['end'], value=token['token'])
        case 'reader_directive':
            return Identifier(start_loc=token['start'], end_loc=token['end'], name=token['token'])
        case _:
            assert False, f'Unexpected token type {token["token_type"]}'


# Scheme list parser

QuoteExprClass: TypeAlias = (
    Type[QuotedExpr] | Type[QuasiQuotedExpr] | Type[UnquotedExpr] | Type[UnquoteSplicingExpr]
)

# Quotation markers
QUOTES: dict[str, QuoteExprClass] = {
    "'": QuotedExpr,
    '`': QuasiQuotedExpr,
    ',': UnquotedExpr,
    ',@': UnquoteSplicingExpr
}


ClosingBracket: TypeAlias = Literal[')', ']']
MATCHING_BRACKETS: Final[dict[str, ClosingBracket]] = {
    '(': ')',
    '[': ']',
    '#(': ')',
}


class SchemeReader:
    def __init__(self):
        # Dict of {line #: comment token}
        self.comments: dict[int, Token] = {}

    def read_file(self, file_: TextIO) -> Program:
        expressions = []
        tokens = list(Tokenizer().tokenize_lines(file_))
        src = Buffer(iter(tokens))
        while src.current() is not None:
            while src.more_on_line:
                expression = self.scheme_read(src)
                expressions.append(expression)

        return Program(
            start_loc=expressions[0].start_loc,
            end_loc=expressions[0].end_loc,
            expressions=expressions,
            comments=self.comments,
        )

    def scheme_read(self, src: Buffer) -> Expression:
        """Read the next expression from SRC, a Buffer of tokens."""
        token = src.pop()
        if token is None:
            raise EOFError

        if token['token_type'] == 'comment':
            self.comments[token['start']['line']] = token
            return self.scheme_read(src)

        val = token['token']
        start_loc = token['start']
        if val not in PUNCTUATORS:
            return token_to_node(token)
        if val in QUOTES:
            # SKELETON pass  # fill in your solution here
            # BEGIN SOLUTION
            quoted_expr = self.scheme_read(src)
            return QUOTES[val](start_loc=start_loc, end_loc=quoted_expr.end_loc, expr=quoted_expr)
            # END SOLUTION
        if val in MATCHING_BRACKETS:
            opening_bracket = val
            expected_closing_bracket = MATCHING_BRACKETS[opening_bracket]
            current_token = src.current()
            if current_token is None:
                raise SyntaxError('unexpected end of file')

            # Empty list
            if current_token['token'] == expected_closing_bracket:
                closing_paren = src.pop()
                assert closing_paren is not None
                return SList(
                    start_loc=start_loc, end_loc=closing_paren['end'], items=tuple(),
                    opening_bracket=opening_bracket, closing_bracket=closing_paren['token'],
                )

            head = self.read_head(src)

            current_token = src.current()
            if current_token is None:
                raise SyntaxError('unexpected end of file')
            if current_token['token'] == '.':
                src.pop()
                tail = self.scheme_read(src)
                if src.current() is None:
                    raise SyntaxError('unexpected end of file')

                closing_token = src.pop()
                assert closing_token is not None
                if closing_token['token'] != expected_closing_bracket:
                    if closing_token in MATCHING_BRACKETS:
                        raise SyntaxError(
                            f'Bracket mismatch: expected {expected_closing_bracket} '
                            f'but got {closing_token["token"]}'
                        )
                    raise SyntaxError('Expected one element after .')

                return Pair(
                    start_loc=start_loc, end_loc=closing_token['end'],
                    first=head, second=tail
                )

            tail, closing_paren = self.read_tail(src, expected_closing_bracket)
            return SList(
                start_loc=start_loc, end_loc=closing_paren['end'], items=[head, *tail],
                opening_bracket=opening_bracket, closing_bracket=closing_paren['token'],
            )

        raise SyntaxError('unexpected token: {0}'.format(val))

    def read_head(self, src: Buffer) -> Expression:
        """
        Read an expression to be used as the head of a list or pair.
        Return None and leave the closing paren in the buffer if the next token closes the list.
        """
        try:
            current_token = src.current()
            if current_token is None:
                raise SyntaxError('unexpected end of file')
            current_val = current_token['token']

            if current_val == '.':
                raise SyntaxError('. must have at least one element before it')

            expr = self.scheme_read(src)
            if src.current() is None:
                raise SyntaxError('unexpected end of file')

            return expr
        except EOFError as exc:
            raise SyntaxError('unexpected end of file') from exc

    def read_tail(
        self,
        src: Buffer, expected_closing_bracket: ClosingBracket
    ) -> tuple[list[Expression], Token]:
        """Return the remainder of a list in SRC.

        Return a tuple of (expressions, closing paren/bracket token).
        """
        try:
            current_token = src.current()
            if current_token is None:
                raise SyntaxError('unexpected end of file')
            current_val = current_token['token']
            # Empty list
            if current_val == expected_closing_bracket:
                src.pop()
                return [], current_token

            first = self.scheme_read(src)
            rest, closing_paren = self.read_tail(src, expected_closing_bracket)
            return [first, *rest], closing_paren
        except EOFError as exc:
            raise SyntaxError('unexpected end of file') from exc
