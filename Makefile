.PHONY: test public-corpus public-corpus-mutation output-capture-test paper-sync counterexample g3-verification smoke mmc-crosscheck outputs paper clean-paper

# Stable manuscript timestamp: 2026-08-31 00:00:00 UTC.
SOURCE_DATE_EPOCH ?= 1788134400
TECTONIC ?= tectonic

test: public-corpus public-corpus-mutation output-capture-test paper-sync smoke mmc-crosscheck counterexample g3-verification

public-corpus:
	python3 scripts/public_corpus.py

public-corpus-mutation:
	python3 -m unittest tests/test_public_corpus.py

output-capture-test:
	python3 -m unittest tests/test_capture_outputs.py

paper-sync:
	SOURCE_DATE_EPOCH="$(SOURCE_DATE_EPOCH)" TECTONIC="$(TECTONIC)" \
		python3 scripts/check_pdf_sync.py

counterexample:
	./src/run-gap.sh tests/counterexample.g

g3-verification:
	./src/run-gap.sh G3-verification.g

smoke:
	./src/run-gap.sh tests/smoke.g

mmc-crosscheck:
	./src/run-gap.sh tests/mmc-crosscheck.g

outputs:
	./src/capture-outputs.sh

paper:
	mkdir -p paper/build
	SOURCE_DATE_EPOCH="$(SOURCE_DATE_EPOCH)" FORCE_SOURCE_DATE=1 TZ=UTC \
		$(TECTONIC) -X compile paper/main.tex --outdir paper/build
	cp paper/build/main.pdf paper/main.pdf

clean-paper:
	python3 -c 'from pathlib import Path; import shutil; shutil.rmtree(Path("paper/build"), ignore_errors=True)'
