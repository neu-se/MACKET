import itertools
from abc import ABCMeta
from typing import Final

from racket_mutation_analysis.racket_ast.visitor import Visitor

from ..schema import Mutant


class MutatorVisitor(Visitor, metaclass=ABCMeta):
    _mutant_counter: Final = itertools.count(1)

    def __init__(self) -> None:
        self.list_mutants: list[Mutant] = []

    @classmethod
    def get_mutator_name(cls) -> str:
        return cls.__name__

    @classmethod
    def _get_next_mutant_id(cls) -> str:
        return str(next(cls._mutant_counter))
