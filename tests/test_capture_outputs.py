#!/usr/bin/env python3
"""Regression tests for transactional captured-output replacement."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import unittest


OUTPUT_NAMES = (
    "counterexample-gap-4.16.0.txt",
    "G3-verification-gap-4.16.0.txt",
    "mmc-crosscheck-gap-4.16.0.txt",
    "counterexample-gap-4.11.1.txt",
    "G3-verification-gap-4.11.1.txt",
)


class CaptureOutputsTest(unittest.TestCase):
    def setUp(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "src").mkdir()
        (self.root / "data").mkdir()
        (self.root / "bin").mkdir()
        (self.root / "tmp").mkdir()

        capture = self.root / "src" / "capture-outputs.sh"
        shutil.copy2(source_root / "src" / "capture-outputs.sh", capture)
        capture.chmod(0o755)

        native_gap = self.root / "bin" / "gap"
        native_gap.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        native_gap.chmod(0o755)

        fake_git = self.root / "bin" / "git"
        fake_git.write_text(
            textwrap.dedent(
                """\
                #!/bin/sh
                if [ "$1" = status ] && [ "$2" = --porcelain ]; then
                  exit 0
                fi
                if [ "$1" = rev-parse ] && [ "$2" = HEAD ]; then
                  printf '%s\\n' deadbeef
                  exit 0
                fi
                exit 2
                """
            ),
            encoding="utf-8",
        )
        fake_git.chmod(0o755)

        system_mv = shutil.which("mv")
        if system_mv is None:
            self.fail("system mv command not found")
        fake_mv = self.root / "bin" / "mv"
        fake_mv.write_text(
            textwrap.dedent(
                f"""\
                #!/bin/sh
                source_path="$2"
                case "$source_path" in
                  */data/.capture-publish.*)
                    count_file="${{FAKE_PUBLISH_MV_COUNT_FILE:?}}"
                    count=$(cat "$count_file")
                    count=$((count + 1))
                    printf '%s\\n' "$count" >"$count_file"
                    if [ "$count" -eq "${{FAIL_PUBLISH_MOVE_AT:-0}}" ]; then
                      exit 71
                    fi
                    ;;
                  */data/.capture-rollback.*)
                    count_file="${{FAKE_ROLLBACK_MV_COUNT_FILE:?}}"
                    count=$(cat "$count_file")
                    count=$((count + 1))
                    printf '%s\\n' "$count" >"$count_file"
                    if [ "$count" -eq "${{FAIL_ROLLBACK_MOVE_AT:-0}}" ]; then
                      exit 72
                    fi
                    ;;
                esac
                exec {system_mv!s} "$@"
                """
            ),
            encoding="utf-8",
        )
        fake_mv.chmod(0o755)

        fake_runner = self.root / "src" / "run-gap.sh"
        fake_runner.write_text(
            textwrap.dedent(
                r"""\
                #!/usr/bin/env bash
                set -euo pipefail
                target="$1"
                if [[ "$GAP_BIN" == /nonexistent ]]; then
                  version=4.11.1
                else
                  version=4.16.0
                fi
                printf '# repository_revision=%s\n' "$MMC_REPOSITORY_REVISION"
                printf '# host=TestOS-testarch\n'
                printf '# invocation=./src/run-gap.sh %s\n' "$target"
                printf '# runner=fake gap_version=%s\n' "$version"
                if [[ "${DUPLICATE_REVISION:-0}" == 1 && \
                      "$target" == G3-verification.g ]]; then
                  printf '# repository_revision=%s\n' "$MMC_REPOSITORY_REVISION"
                fi
                if [[ "${FAIL_DOCKER:-0}" == 1 && "$version" == 4.11.1 && \
                      "$target" == tests/counterexample.g ]]; then
                  echo 'simulated Docker failure' >&2
                  exit 9
                fi
                case "$target" in
                  tests/counterexample.g)
                    printf '# gap_version=%s\n' "$version"
                    for prime in 3 5 7; do
                      printf 'PASS p=%s %s\n' "$prime" \
                        'monotone_chain=false conjugacy_coverage=true'
                    done
                    ;;
                  G3-verification.g)
                    printf 'GAP version: %s\n' "$version"
                    printf 'ALL CHECKS PASSED\n'
                    ;;
                  tests/mmc-crosscheck.g)
                    printf '# gap_version=%s\n' "$version"
                    printf '%s%s\n' \
                      'PASS mmc_crosscheck groups=144 exhaustive_sequences=true' \
                      ' witness_validation=true'
                    ;;
                  *) exit 3 ;;
                esac
                """
            ),
            encoding="utf-8",
        )
        fake_runner.chmod(0o755)

        self.original = {
            name: f"original:{name}\n".encode("utf-8") for name in OUTPUT_NAMES
        }
        for name, content in self.original.items():
            (self.root / "data" / name).write_bytes(content)

        self.environment = os.environ.copy()
        self.environment.update(
            {
                "PATH": f"{self.root / 'bin'}:{self.environment['PATH']}",
                "GAP_416_BIN": str(native_gap),
                "TMPDIR": str(self.root / "tmp"),
                "FAKE_PUBLISH_MV_COUNT_FILE": str(
                    self.root / "publish-mv-count"
                ),
                "FAKE_ROLLBACK_MV_COUNT_FILE": str(
                    self.root / "rollback-mv-count"
                ),
            }
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_capture(
        self,
        *,
        fail_docker: bool = False,
        fail_publish_move_at: int = 0,
        fail_rollback_move_at: int = 0,
        duplicate_revision: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        environment = self.environment.copy()
        environment["FAIL_DOCKER"] = "1" if fail_docker else "0"
        environment["FAIL_PUBLISH_MOVE_AT"] = str(fail_publish_move_at)
        environment["FAIL_ROLLBACK_MOVE_AT"] = str(fail_rollback_move_at)
        environment["DUPLICATE_REVISION"] = "1" if duplicate_revision else "0"
        Path(environment["FAKE_PUBLISH_MV_COUNT_FILE"]).write_text(
            "0\n", encoding="utf-8"
        )
        Path(environment["FAKE_ROLLBACK_MV_COUNT_FILE"]).write_text(
            "0\n", encoding="utf-8"
        )
        return subprocess.run(
            [str(self.root / "src" / "capture-outputs.sh")],
            cwd=self.root,
            env=environment,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def assert_no_staging_residue(self) -> None:
        self.assertEqual([], list((self.root / "data").glob(".capture-*")))
        self.assertEqual([], list((self.root / "tmp").iterdir()))

    def test_late_failure_preserves_every_tracked_output(self) -> None:
        result = self.run_capture(fail_docker=True)
        self.assertNotEqual(0, result.returncode)
        for name, content in self.original.items():
            self.assertEqual(content, (self.root / "data" / name).read_bytes())
        self.assert_no_staging_residue()

    def test_duplicate_revision_metadata_is_rejected(self) -> None:
        result = self.run_capture(duplicate_revision=True)
        self.assertNotEqual(0, result.returncode)
        for name, content in self.original.items():
            self.assertEqual(content, (self.root / "data" / name).read_bytes())
        self.assert_no_staging_residue()

    def test_publish_failure_rolls_back_every_tracked_output(self) -> None:
        for position in range(1, len(OUTPUT_NAMES) + 1):
            with self.subTest(publish_move=position):
                result = self.run_capture(fail_publish_move_at=position)
                self.assertEqual(71, result.returncode, result.stderr)
                for name, content in self.original.items():
                    self.assertEqual(
                        content, (self.root / "data" / name).read_bytes()
                    )
                self.assert_no_staging_residue()

    def test_rollback_failure_retains_complete_backups(self) -> None:
        result = self.run_capture(
            fail_publish_move_at=2, fail_rollback_move_at=1
        )
        self.assertEqual(74, result.returncode, result.stderr)
        self.assertIn("Output rollback failed; backups remain at ", result.stderr)

        backup_directories = list(
            (self.root / "data").glob(".capture-backup.*")
        )
        self.assertEqual(1, len(backup_directories))
        backup = backup_directories[0]
        for name, content in self.original.items():
            self.assertEqual(content, (backup / name).read_bytes())

        self.assertEqual([], list((self.root / "data").glob(".capture-publish.*")))
        self.assertEqual([], list((self.root / "tmp").iterdir()))

    def test_success_replaces_all_validated_outputs(self) -> None:
        result = self.run_capture()
        self.assertEqual(0, result.returncode, result.stderr)
        for name, content in self.original.items():
            captured = (self.root / "data" / name).read_bytes()
            self.assertNotEqual(content, captured)
            self.assertEqual(
                1, captured.count(b"# repository_revision=deadbeef\n")
            )
        self.assert_no_staging_residue()


if __name__ == "__main__":
    unittest.main()
