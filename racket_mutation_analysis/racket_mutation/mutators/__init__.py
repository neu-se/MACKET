from typing import Final, Mapping, Type

from .arithmetic_deletion import ArithmeticDeletionMutator
from .arithmetic_mut import ArithmeticMutator
from .bool_func_to_bool import BoolFuncToBoolMutator
from .cond_mut import CondMutator
from .empty_list import EmptyListMutator
from .empty_string import EmptyStringMutator
from .flip_bools import FlipBooleansMutator
from .flip_num_sign import FlipNumSignMutator
from .homework_mutator import Homework4and5Mutator
from .if_mut import IfMutator
from .logical_mut import LogicalMutator
from .mutator import MutatorVisitor
from .num_comparison_mutator import NumberComparisonMutator
from .num_literals_mut import NumLiteralsMutator
from .wrap_with_not import WrapWithNotMutator

MUTATOR_CLASSES: Final[Mapping[str, Type[MutatorVisitor]]] = {
    ArithmeticMutator.__name__: ArithmeticMutator,
    LogicalMutator.__name__: LogicalMutator,
    IfMutator.__name__: IfMutator,
    CondMutator.__name__: CondMutator,
    WrapWithNotMutator.__name__: WrapWithNotMutator,
    BoolFuncToBoolMutator.__name__: BoolFuncToBoolMutator,
    FlipNumSignMutator.__name__: FlipNumSignMutator,
    ArithmeticDeletionMutator.__name__: ArithmeticDeletionMutator,
    NumberComparisonMutator.__name__: NumberComparisonMutator,
    FlipBooleansMutator.__name__: FlipBooleansMutator,
    EmptyListMutator.__name__: EmptyListMutator,
    EmptyStringMutator.__name__: EmptyStringMutator,
    NumLiteralsMutator.__name__: NumLiteralsMutator,
    Homework4and5Mutator.__name__: Homework4and5Mutator
}
