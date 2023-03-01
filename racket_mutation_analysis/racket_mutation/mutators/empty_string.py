from racket_mutation_analysis.racket_ast.scheme_reader import String
from racket_mutation_analysis.racket_mutation.schema import Location

from .mutator import MutatorVisitor


class EmptyStringMutator(MutatorVisitor):

    def visit_String(self, node: String):
        new_location: Location = {'start': node.start_loc, 'end': node.end_loc}
        self.list_mutants.append({
            'id': self._get_next_mutant_id(),
            'location': new_location,
            'mutator_name': self.get_mutator_name(),
            'replacement': '\"\"'
        })
