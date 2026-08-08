.PHONY: test counterexample smoke paper clean-paper

test: smoke counterexample

counterexample:
	./src/run-gap.sh tests/counterexample.g

smoke:
	./src/run-gap.sh tests/smoke.g

paper:
	mkdir -p paper/build
	tectonic -X compile paper/main.tex --outdir paper/build
	cp paper/build/main.pdf paper/main.pdf

clean-paper:
	python3 -c 'from pathlib import Path; import shutil; shutil.rmtree(Path("paper/build"), ignore_errors=True)'
