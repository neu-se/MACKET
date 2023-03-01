from typing import Final

from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, SList

from ..schema import Location, Position
from .mutator import MutatorVisitor


class EmptyListMutator(MutatorVisitor):
    _list_identifiers = [
        'list', 'cons'
    ]

    def visit_SList(self, node: SList):
        if (len(node.items) < 2):
            super().visit_SList(node)
            return

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

        if (isinstance(first_node, Identifier)
                and (first_node.name in self._list_identifiers)):
            self.list_mutants.append({
                'id': self._get_next_mutant_id(),
                'location': new_location,
                'mutator_name': self.get_mutator_name(),
                'replacement': '\'()'
            })

        super().visit_SList(node)
