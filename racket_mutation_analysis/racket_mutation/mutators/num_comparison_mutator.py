import time
from typing import Final, List

from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList
from racket_mutation_analysis.racket_ast.string_visitor import ToStrVisitor
from racket_mutation_analysis.racket_ast.utils import is_call_to_one_of

from ..schema import Location
from .mutator import MutatorVisitor


class NumberComparisonMutator(MutatorVisitor):
    _comparisons: List[str] = [
        '>', '>=', '<', '<=', '='
    ]

    def visit_SList(self, node: SList):
        if not is_call_to_one_of(node, self._comparisons):
            super().visit_SList(node)
            return

        first_node = node.items[0]
        new_location: Location = {'start': first_node.start_loc, 'end': first_node.end_loc}

        string_visitor = ToStrVisitor()
        string_visitor.visit(first_node)
        string_rep_of_first_node = string_visitor.result.strip()

        for new_operator in self._comparisons:
            if (new_operator != string_rep_of_first_node):
                self.list_mutants.append({
                    'id': self._get_next_mutant_id(),
                    'location': new_location,
                    'mutator_name': self.get_mutator_name(),
                    'replacement': new_operator
                })
