from typing import Final

from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList
from racket_mutation_analysis.racket_ast.utils import is_call_to_one_of

from ..schema import Location
from .mutator import MutatorVisitor


class ArithmeticMutator(MutatorVisitor):
    _operator_substitutions: Final = {
        '+': '-',
        '-': '+',
        '*': '/',
        '/': '*',
    }

    def visit_SList(self, node: SList):
        if is_call_to_one_of(node, self._operator_substitutions):
            first_node = node.items[0]
            assert isinstance(first_node, Identifier)
            new_location: Location = {'start': first_node.start_loc, 'end': first_node.end_loc}
            self.list_mutants.append({
                'id': self._get_next_mutant_id(),
                'location': new_location,
                'mutator_name': self.get_mutator_name(),
                'replacement': self._operator_substitutions[first_node.name]
            })

        super().visit_SList(node)
