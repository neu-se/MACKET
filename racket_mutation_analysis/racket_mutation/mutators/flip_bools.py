from racket_mutation_analysis.racket_ast.scheme_reader import Number

from ..schema import Location
from .mutator import MutatorVisitor


class FlipBooleansMutator(MutatorVisitor):

    def visit_Boolean(self, node: Number):
        _boolean_key = {
            '#t': '#f',
            '#f': '#t'
        }

        new_location: Location = {'start': node.start_loc, 'end': node.end_loc}
        self.list_mutants.append({
            'id': self._get_next_mutant_id(),
            'location': new_location,
            'mutator_name': self.get_mutator_name(),
            'replacement': _boolean_key[node.value]
        })
