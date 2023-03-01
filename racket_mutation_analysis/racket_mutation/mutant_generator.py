from typing import Sequence, Type

from racket_mutation_analysis.racket_ast.scheme_reader import Program
from racket_mutation_analysis.racket_mutation.mutators.mutator import MutatorVisitor
from racket_mutation_analysis.racket_mutation.schema import Mutant


class MutantGenerator:

    def __init__(self, tree: Program, input_file: list[str],
                 mutator_classes: Sequence[Type[MutatorVisitor]]) -> None:
        self.ast = tree
        self.input_file = input_file
        self.mutations: list[Mutant] = []
        self.mutator_classes = mutator_classes

    # Applies each visitor to the given AST
    def run(self) -> list[tuple[Mutant, str]]:
        mutants: list[tuple[Mutant, str]] = []

        for mutator_class in self.mutator_classes:
            mutator = mutator_class()
            mutator.visit(self.ast)
            self.mutations += mutator.list_mutants

        # For each Mutant in list, create a new mutated string
        for mutant in self.mutations:
            new_string = ''  # reset new mutant string
            start_line_num = mutant['location']['start']['line']
            start_col_num = mutant['location']['start']['column']
            end_line_num = mutant['location']['end']['line']
            end_col_num = mutant['location']['end']['column']

            line = 0
            while line < len(self.input_file):
                if line == start_line_num == end_line_num:
                    new_string += self.input_file[line][0:start_col_num]
                    new_string += mutant['replacement']
                    new_string += self.input_file[line][end_col_num:]
                    line += 1
                elif line == start_line_num:
                    new_string += self.input_file[line][0:start_col_num]
                    new_string += mutant['replacement']
                    line = end_line_num
                elif line == end_line_num:
                    new_string += self.input_file[line][end_col_num:]
                    line += 1
                else:  # there is no mutant in this line
                    new_string += self.input_file[line]
                    line += 1

            mutants.append((mutant, new_string))

        return mutants
