import argparse
from pathlib import Path

import yaml

from racket_mutation_analysis.racket_ast.scheme_reader import SchemeReader
from racket_mutation_analysis.racket_mutation.mutant_generator import MutantGenerator
from racket_mutation_analysis.racket_mutation.mutators import MUTATOR_CLASSES
from racket_mutation_analysis.racket_mutation.schema import AppliedMutant, GeneratedMutants


def main():
    args = parse_args()

    yaml_dict: GeneratedMutants = {}

    for input_file in args.input_files:
        with open(input_file) as f:
            ast = SchemeReader().read_file(f)

        with open(input_file) as f:
            file_text = f.read()
            code = file_text.splitlines(keepends=True)

        if not args.mutator:
            desired_mutators = list(MUTATOR_CLASSES.values())
        else:
            desired_mutators = [
                mutator_class for mutator_name, mutator_class in MUTATOR_CLASSES.items()
                if mutator_name in args.mutator
            ]

        mutant_generator = MutantGenerator(ast, code, desired_mutators)
        mutants = mutant_generator.run()

        path = Path(input_file).relative_to(args.project_root)
        yaml_dict[str(path)] = {
            'original': file_text,
            'mutants': [
                AppliedMutant(mutated_code=mutated_code, **mutant)
                for mutant, mutated_code in mutants
            ]
        }

    with open(args.output_file, 'w') as f:
        f.write(yaml.dump(yaml_dict, width=float('inf')))  # type: ignore


def parse_args():
    parser = argparse.ArgumentParser(
        "Command line interface for Racket mutant generation")
    # input file
    parser.add_argument('input_files', nargs='+')
    # output YAML file name
    parser.add_argument('output_file')
    # desired mutator(s)
    parser.add_argument('--mutator', '-m', action='append', choices=list(MUTATOR_CLASSES))
    parser.add_argument('--project_root', '-p', default='.')

    return parser.parse_args()


if __name__ == '__main__':
    main()
