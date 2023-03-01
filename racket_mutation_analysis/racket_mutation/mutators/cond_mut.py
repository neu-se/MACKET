from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList
from racket_mutation_analysis.racket_ast.utils import is_call_to

from ..schema import Location, Mutant
from .mutator import MutatorVisitor


class CondMutator(MutatorVisitor):

    def visit_SList(self, node: SList):
        if not is_call_to(node, 'cond'):
            super().visit_SList(node)
            return

        # iterate through cond branches
        for statement in node.items:
            # checking if valid cond branches (two parts)
            if len(statement.children) != 2:
                continue
            predicate = statement.children[0]
            # skip else case
            if isinstance(predicate, Identifier) and predicate.name == 'else':
                continue
            new_location: Location = {'start': predicate.start_loc, 'end': predicate.end_loc}

            new_mutant_true: Mutant = {
                'id': self._get_next_mutant_id(), 'location': new_location,
                'mutator_name': self.get_mutator_name(), 'replacement': '#t'}
            new_mutant_false: Mutant = {
                'id': self._get_next_mutant_id(), 'location': new_location,
                'mutator_name': self.get_mutator_name(), 'replacement': '#f'}
            self.list_mutants.append(new_mutant_true)
            self.list_mutants.append(new_mutant_false)

        for node_in_list in node.items:
            self.visit_ASTNode(node_in_list)
