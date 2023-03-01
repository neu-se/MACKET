from racket_mutation_analysis.racket_ast.scheme_reader import Number
from racket_mutation_analysis.racket_mutation.schema import Location

from .mutator import MutatorVisitor


class NumLiteralsMutator(MutatorVisitor):
    _replacements = [
        '0', '-1', '1'
    ]

    def visit_Number(self, node: Number):
        new_location: Location = {'start': node.start_loc, 'end': node.end_loc}
        for new_num in self._replacements:
            if (new_num != int(float(node.value))):
                self.list_mutants.append({
                    'id': self._get_next_mutant_id(),
                    'location': new_location,
                    'mutator_name': self.get_mutator_name(),
                    'replacement': new_num
                })
        self.list_mutants.append({
            'id': self._get_next_mutant_id(),
            'location': new_location,
            'mutator_name': self.get_mutator_name(),
            'replacement': str(float(node.value) - 1)
        })
        self.list_mutants.append({
            'id': self._get_next_mutant_id(),
            'location': new_location,
            'mutator_name': self.get_mutator_name(),
            'replacement': str(float(node.value) + 1)
        })
