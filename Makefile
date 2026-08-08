.PHONY: test counterexample smoke mmc-crosscheck certificates paper clean-paper

test: smoke mmc-crosscheck counterexample

counterexample:
	./src/run-gap.sh tests/counterexample.g

smoke:
	./src/run-gap.sh tests/smoke.g

mmc-crosscheck:
	./src/run-gap.sh tests/mmc-crosscheck.g

certificates:
	./src/capture-certificates.sh

paper:
	mkdir -p paper/build
	tectonic -X compile paper/main.tex --outdir paper/build
	cp paper/build/main.pdf paper/main.pdf

clean-paper:
	python3 -c 'from pathlib import Path; import shutil; shutil.rmtree(Path("paper/build"), ignore_errors=True)'
