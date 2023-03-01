from typing import Final

from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList
from racket_mutation_analysis.racket_ast.string_visitor import ToStrVisitor
from racket_mutation_analysis.racket_ast.utils import is_call_to_one_of

from ..schema import Location, Position
from .mutator import MutatorVisitor


class ArithmeticDeletionMutator(MutatorVisitor):
    _operators: Final = {
        '+', '-', '*', '/'
    }

    def visit_SList(self, node: SList):
        if not is_call_to_one_of(node, self._operators):
            super().visit_SList(node)
            return

        first_node = node.items[0]
        last_node = node.items[len(node.items) - 1]
        new_start: Position = {'line': first_node.start_loc['line'],
                               'column': first_node.start_loc['column'] - 1}
        new_end: Position = {'line': last_node.end_loc['line'],
                             'column': last_node.end_loc['column'] + 1}
        new_location: Location = {'start': new_start, 'end': new_end}

        for expr_node in node.items[1:]:
            str_visitor = ToStrVisitor()
            str_visitor.visit(expr_node)
            self.list_mutants.append({
                'id': self._get_next_mutant_id(),
                'location': new_location,
                'mutator_name': self.get_mutator_name(),
                'replacement': str_visitor.result.strip()
            })

        super().visit_SList(node)
