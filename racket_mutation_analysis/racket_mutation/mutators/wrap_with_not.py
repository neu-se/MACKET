from typing import Final

from racket_mutation_analysis.racket_ast.scheme_reader import Identifier, LiteralVal, SList
from racket_mutation_analysis.racket_ast.string_visitor import ToStrVisitor
from racket_mutation_analysis.racket_ast.utils import is_call_to_one_of

from ..schema import Location, Position
from .mutator import MutatorVisitor


class WrapWithNotMutator(MutatorVisitor):
    _substitutions: Final = {
        'and', 'or'
    }

    def visit_SList(self, node: SList):
        if not is_call_to_one_of(node, self._substitutions):
            super().visit_SList(node)
            return

        first_node = node.items[0]
        last_node = node.items[len(node.items) - 1]
        new_start_position: Position = {
            'line': first_node.start_loc['line'],
            'column': first_node.start_loc['column']}
        new_end_position: Position = {
            'line': last_node.end_loc['line'],
            'column': last_node.end_loc['column']}
        new_location: Location = {'start': new_start_position,
                                  'end': new_end_position}

        node_str = ''
        str_visitor = ToStrVisitor()
        for child in node.children:
            str_visitor.visit_ASTNode(child)
        node_str += str_visitor.result

        self.list_mutants.append({
            'id': self._get_next_mutant_id(),
            'location': new_location,
            'mutator_name': self.get_mutator_name(),
            'replacement': 'not (' + node_str.strip() + ')'
        })

        super().visit_SList(node)
