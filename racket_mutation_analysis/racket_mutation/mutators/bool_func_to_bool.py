from typing import Final

from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList
from racket_mutation_analysis.racket_ast.utils import is_call_to_one_of

from ..schema import Location, Mutant, Position
from .mutator import MutatorVisitor


class BoolFuncToBoolMutator(MutatorVisitor):
    _bool_funcs: Final = {
        'and', 'or', 'not', '>', '>=',
        '==', '<', '<=', 'nand', 'nor',
        'andmap', 'ormap'
    }

    def visit_SList(self, node: SList):
        match(node.items):
            case [Identifier(name=name) as first_node, *_] \
                    if name in self._bool_funcs or name.endswith('?'):
                last_node = node.items[len(node.items) - 1]

                new_start_position: Position = {
                    'line': first_node.start_loc['line'],
                    'column': first_node.start_loc['column'] - 1}
                new_end_position: Position = {
                    'line': last_node.end_loc['line'],
                    'column': last_node.end_loc['column'] + 1}
                new_location: Location = {'start': new_start_position,
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

        super().visit_SList(node)
