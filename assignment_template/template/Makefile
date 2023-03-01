# Run make sol=/path/to/hwX.rkt to use a different implementation file (e.g., from a student).
sol := hwX.rkt

all: test mutation

# Yes, we want hwX hardcoded in the recipe below
test: setup hwX-instructor-tests.rkt
	cp hwX-instructor-tests.rkt _working_dir
	cd _working_dir; \
		bash prepare_student_impl.bash \
			hwX "$$(grep -E "(#lang|#reader)" reader-directive.txt)" \
			> hwX-temp.rkt; \
		mv hwX-temp.rkt hwX.rkt; \
		raco test hwX-instructor-tests.rkt

mutation: setup
	cp hwX-mutants.yml _working_dir
	cd _working_dir; \
		bash extract_student_tests.bash \
			hwX "$$(grep -E "(#lang|#reader)" reader-directive.txt)" \
			> hwX-tests.rkt; \
		run-mutants --run_tests_in_one_batch hwX-mutants.yml; \
		echo "HTML report available in hwX/_working_dir/mutants.html"

setup:
	mkdir -p _working_dir
	cp *.rkt mutation_commands.sh preprocessing/* reader-directive.txt _working_dir
	cp $(sol) _working_dir/hwX.rkt

hwX-instructor-tests.rkt:
	bash preprocessing/extract_instructor_tests.bash hwX \
		"$$(grep -E "(#lang|#reader)" reader-directive.txt)" \
		> hwX-instructor-tests.rkt

clean:
	rm -rf _working_dir

.PHONY: all test mutation setup clean
