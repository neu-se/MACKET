from racket_mutation_analysis.racket_ast.scheme_reader import Number

from ..schema import Location
from .mutator import MutatorVisitor


class FlipNumSignMutator(MutatorVisitor):

    def visit_Number(self, node: Number):
        new_location: Location = {'start': node.start_loc, 'end': node.end_loc}
        self.list_mutants.append({
            'id': self._get_next_mutant_id(),
            'location': new_location,
            'mutator_name': self.get_mutator_name(),
            'replacement': '(- ' + node.value + ')'
        })
