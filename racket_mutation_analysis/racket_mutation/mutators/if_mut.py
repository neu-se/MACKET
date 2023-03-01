from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList
from racket_mutation_analysis.racket_ast.utils import is_call_to

from ..schema import Location, Mutant
from .mutator import MutatorVisitor


class IfMutator(MutatorVisitor):

    def visit_SList(self, node: SList):
        # length is four (if, boolean statement, first case, second case)
        if not is_call_to(node, 'if') or len(node.items) != 4:
            super().visit_SList(node)
            return

        boolean_node = node.items[1]
        new_location: Location = {'start': boolean_node.start_loc, 'end': boolean_node.end_loc}

        new_mutant_false: Mutant = {
            'id': self._get_next_mutant_id(),
            'location': new_location,
            'mutator_name': self.get_mutator_name(),
            'replacement': '#f'}
        new_mutant_true: Mutant = {
            'id': self._get_next_mutant_id(),
            'location': new_location,
            'mutator_name': self.get_mutator_name(),
            'replacement': '#t'}
        self.list_mutants.append(new_mutant_true)
        self.list_mutants.append(new_mutant_false)

        for node_in_list in node.items:
            self.visit_ASTNode(node_in_list)
