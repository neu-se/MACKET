from __future__ import annotations

from typing import TYPE_CHECKING, Literal, TypeAlias, TypedDict

if TYPE_CHECKING:
    from typing_extensions import Required


# Dict of file paths to Mutations
GeneratedMutants: TypeAlias = dict[str, 'Mutations']


class Mutations(TypedDict):
    # The original, unmutated file contents
    original: str
    mutants: list[AppliedMutant]


class Mutant(TypedDict):
    id: str
    location: Location
    mutator_name: str
    replacement: str


class AppliedMutant(Mutant):
    mutated_code: str


class Location(TypedDict):
    start: Position
    end: Position


class Position(TypedDict):
    line: int
    column: int


# From https://github.com/stryker-mutator/mutation-testing-elements/blob
#       /master/packages/report-schema/src/mutation-testing-report-schema.json
# Note that we're making some keys required here even if they aren't
# required by the spec. This will simplify type checking for our use case.


class MutationTestResult(TypedDict, total=False):
    schemaVersion: Required[str]
    thresholds: Required[Thresholds]
    files: Required[dict[str, FileResultDictionary]]
    projectRoot: str


class Thresholds(TypedDict):
    high: int
    low: int


class FileResultDictionary(TypedDict):
    language: str
    source: str
    mutants: list[MutantResult]


class MutantResult(TypedDict):
    id: str
    mutatorName: str
    location: Location
    status: MutantStatus
    mutatorName: str
    replacement: str
    killedBy: list[str]


MutantStatus: TypeAlias = Literal[
    "Killed", "Survived", "NoCoverage", "CompileError",
    "RuntimeError", "Timeout", "Ignored"
]
