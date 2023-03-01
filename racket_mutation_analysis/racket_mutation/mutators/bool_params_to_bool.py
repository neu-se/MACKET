from typing import Final

from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList

from ..schema import Location, Mutant, Position
from .mutator import MutatorVisitor


class BoolParamsToBool(MutatorVisitor):
    _bool_param_funcs: Final = {
        'and', 'or', 'not'
    }

    def visit_SList(self, node: SList):
        first_node = node.items[0]

        if (not isinstance(first_node, Identifier)
                or first_node.name not in self._bool_param_funcs):
            super().visit_SList(node)
            return

        for param in node.items[1:]:
            new_start_position: Position = {
                'line': param.start_loc['line'],
                'column': param.start_loc['column']}
            new_end_position: Position = {
                'line': param.end_loc['line'],
                'column': param.end_loc['column']}
            new_location: Location = {
                'start': new_start_position,
                'end': new_end_position}

            new_mutant_true: Mutant = {
                'id': self._get_next_mutant_id(),
                'location': new_location,
                'mutator_name': self.get_mutator_name(),
                'replacement': '#t'}
            new_mutant_false: Mutant = {
                'id': self._get_next_mutant_id(),
                'location': new_location,
                'mutator_name': self.get_mutator_name(),
                'replacement': '#f'}
            self.list_mutants.append(new_mutant_true)
            self.list_mutants.append(new_mutant_false)

        for node_in_list in node.items:
            self.visit_ASTNode(node_in_list)
