#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
native_gap="${GAP_416_BIN:-$HOME/dev/.tools/gap-4.16.0/gap}"
native_output="$repo_dir/data/counterexample-gap-4.16.0.txt"
docker_output="$repo_dir/data/counterexample-gap-4.11.1.txt"
crosscheck_output="$repo_dir/data/mmc-crosscheck-gap-4.16.0.txt"

if [[ ! -x "$native_gap" ]]; then
  printf 'GAP 4.16.0 binary not found at %s; set GAP_416_BIN\n' "$native_gap" >&2
  exit 1
fi

cd "$repo_dir"
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Refusing to capture certificates from a dirty working tree" >&2
  exit 1
fi
revision="$(git rev-parse HEAD)"

MMC_REPOSITORY_REVISION="$revision" GAP_BIN="$native_gap" \
  ./src/run-gap.sh tests/counterexample.g >"$native_output"
grep -q '^# gap_version=4\.16\.0$' "$native_output"

MMC_REPOSITORY_REVISION="$revision" GAP_BIN="$native_gap" \
  ./src/run-gap.sh tests/mmc-crosscheck.g >"$crosscheck_output"
grep -q '^# gap_version=4\.16\.0$' "$crosscheck_output"
grep -q '^PASS mmc_crosscheck groups=144 ' "$crosscheck_output"

MMC_REPOSITORY_REVISION="$revision" GAP_BIN=/nonexistent \
  ./src/run-gap.sh tests/counterexample.g >"$docker_output"
grep -q '^# gap_version=4\.11\.1$' "$docker_output"

printf 'Wrote %s\nWrote %s\nWrote %s\n' \
  "$native_output" "$docker_output" "$crosscheck_output"
