from typing import Final

from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList
from racket_mutation_analysis.racket_ast.utils import is_call_to_one_of
from racket_mutation_analysis.racket_mutation.schema import Location, Mutant, Position

from .mutator import MutatorVisitor


class Homework4and5Mutator(MutatorVisitor):
    # methods with second parameters of [List-of X] data type
    _second_param_list_funcs: Final = {
        'take-n', 'drop-n', 'take-while',
        'drop-while', 'group-by',
    }
    # methods that return [List-of X] data type
    _return_list_funcs: Final = {
        'take-n', 'drop-n', 'take-while', 'drop-while'
    }
    # functionally switchable methods
    _switchable_func: Final = {
        'take-n': 'drop-n',
        'drop-n': 'take-n',
        'take-while': 'drop-while',
        'drop-while': 'take-while'
    }

    def visit_SList(self, node: SList):

        if is_call_to_one_of(node, self._second_param_list_funcs) and len(node.items) >= 3:
            first_node = node.items[0]
            third_node = node.items[2]
            empty_list_new_mutant: Mutant = {
                'id': self._get_next_mutant_id(),
                'location': {'start': third_node.start_loc,
                             'end': third_node.end_loc},
                'mutator_name': self.get_mutator_name(),
                'replacement': '\'()'}
            self.list_mutants.append(empty_list_new_mutant)

        if is_call_to_one_of(node, self._return_list_funcs):
            first_node = node.items[0]
            last_node = node.items[len(node.items) - 1]
            new_start_position: Position = {
                'line': first_node.start_loc['line'],
                'column': first_node.start_loc['column'] - 1}
            new_end_position: Position = {
                'line': last_node.end_loc['line'],
                'column': last_node.end_loc['column'] + 1}
            new_location: Location = {'start': new_start_position,
                                      'end': new_end_position}

            empty_list_return_new_mutant: Mutant = {
                'id': self._get_next_mutant_id(),
                'location': new_location,
                'mutator_name': self.get_mutator_name(),
                'replacement': '\'()'}
            self.list_mutants.append(empty_list_return_new_mutant)

        if is_call_to_one_of(node, self._switchable_func):
            first_node = node.items[0]
            assert isinstance(first_node, Identifier)
            switchable_func_new_mutant: Mutant = {
                'id': self._get_next_mutant_id(),
                'location': {'start': first_node.start_loc,
                             'end': first_node.end_loc},
                'mutator_name': self.get_mutator_name(),
                'replacement': self._switchable_func[first_node.name]}
            self.list_mutants.append(switchable_func_new_mutant)

        super().visit_SList(node)
