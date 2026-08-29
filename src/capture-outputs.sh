#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
native_gap="${GAP_416_BIN:-$HOME/dev/.tools/gap-4.16.0/gap}"

if [[ ! -x "$native_gap" ]]; then
  printf 'GAP 4.16.0 binary not found at %s; set GAP_416_BIN\n' "$native_gap" >&2
  exit 1
fi

cd "$repo_dir"
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Refusing to capture outputs from a dirty working tree" >&2
  exit 1
fi
revision="$(git rev-parse HEAD)"

stage_dir="$(mktemp -d "${TMPDIR:-/tmp}/mmc-output-capture.XXXXXX")"
publish_dir="$(mktemp -d "$repo_dir/data/.capture-publish.XXXXXX")"
backup_dir="$(mktemp -d "$repo_dir/data/.capture-backup.XXXXXX")"
transaction_active=0

cleanup() {
  local status=$?
  local rollback_status=0

  trap - EXIT HUP INT TERM
  set +e
  if [[ "$transaction_active" -eq 1 ]]; then
    rollback_outputs
    rollback_status=$?
    if [[ "$rollback_status" -ne 0 ]]; then
      rm -rf "$stage_dir" "$publish_dir"
      printf 'Output rollback failed; backups remain at %s\n' "$backup_dir" >&2
      exit 74
    fi
  fi
  rm -rf "$stage_dir" "$publish_dir" "$backup_dir"
  exit "$status"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

native_output="$stage_dir/counterexample-gap-4.16.0.txt"
docker_output="$stage_dir/counterexample-gap-4.11.1.txt"
crosscheck_output="$stage_dir/mmc-crosscheck-gap-4.16.0.txt"
native_g3_output="$stage_dir/G3-verification-gap-4.16.0.txt"
docker_g3_output="$stage_dir/G3-verification-gap-4.11.1.txt"

MMC_REPOSITORY_REVISION="$revision" GAP_BIN="$native_gap" \
  ./src/run-gap.sh tests/counterexample.g >"$native_output"

MMC_REPOSITORY_REVISION="$revision" GAP_BIN="$native_gap" \
  ./src/run-gap.sh G3-verification.g >"$native_g3_output"

MMC_REPOSITORY_REVISION="$revision" GAP_BIN="$native_gap" \
  ./src/run-gap.sh tests/mmc-crosscheck.g >"$crosscheck_output"

MMC_REPOSITORY_REVISION="$revision" GAP_BIN=/nonexistent \
  ./src/run-gap.sh tests/counterexample.g >"$docker_output"

MMC_REPOSITORY_REVISION="$revision" GAP_BIN=/nonexistent \
  ./src/run-gap.sh G3-verification.g >"$docker_g3_output"

validate_revision() {
  local output="$1"
  local count

  count="$(grep -c "^# repository_revision=$revision$" "$output" || true)"
  [[ "$count" -eq 1 ]]
}

validate_counterexample() {
  local output="$1"
  local version="$2"
  local prime

  [[ -s "$output" ]]
  validate_revision "$output"
  grep -q "^# gap_version=$version$" "$output"
  [[ "$(grep -c '^PASS p=' "$output")" -eq 3 ]]
  for prime in 3 5 7; do
    grep -Eq \
      "^PASS p=$prime .*monotone_chain=false conjugacy_coverage=true$" \
      "$output"
  done
}

validate_g3() {
  local output="$1"
  local version="$2"

  [[ -s "$output" ]]
  validate_revision "$output"
  grep -q "^GAP version: $version$" "$output"
  tail -n 1 "$output" | grep -q '^ALL CHECKS PASSED$'
}

validate_crosscheck() {
  local output="$1"

  [[ -s "$output" ]]
  validate_revision "$output"
  grep -q '^# gap_version=4\.16\.0$' "$output"
  tail -n 1 "$output" | grep -q \
    '^PASS mmc_crosscheck groups=144 .*exhaustive_sequences=true witness_validation=true$'
}

# Nothing under data/ is touched until every computation has completed and
# every staged output has passed its format and success checks.
validate_counterexample "$native_output" '4\.16\.0'
validate_g3 "$native_g3_output" '4\.16\.0'
validate_crosscheck "$crosscheck_output"
validate_counterexample "$docker_output" '4\.11\.1'
validate_g3 "$docker_g3_output" '4\.11\.1'

output_names=(
  counterexample-gap-4.16.0.txt
  G3-verification-gap-4.16.0.txt
  mmc-crosscheck-gap-4.16.0.txt
  counterexample-gap-4.11.1.txt
  G3-verification-gap-4.11.1.txt
)

rollback_outputs() {
  local name
  local rollback_failed=0
  local rollback_path

  for name in "${output_names[@]}"; do
    rollback_path="$repo_dir/data/.capture-rollback.$name.$$"
    if ! cp "$backup_dir/$name" "$rollback_path"; then
      rollback_failed=1
    fi
  done
  if [[ "$rollback_failed" -eq 0 ]]; then
    for name in "${output_names[@]}"; do
      rollback_path="$repo_dir/data/.capture-rollback.$name.$$"
      if ! mv -f "$rollback_path" "$repo_dir/data/$name"; then
        rollback_failed=1
      fi
    done
  fi
  for name in "${output_names[@]}"; do
    rm -f "$repo_dir/data/.capture-rollback.$name.$$"
  done
  return "$rollback_failed"
}

for name in "${output_names[@]}"; do
  cp "$stage_dir/$name" "$publish_dir/$name"
  chmod 0644 "$publish_dir/$name"
  cp "$repo_dir/data/$name" "$backup_dir/$name"
done

transaction_active=1
for name in "${output_names[@]}"; do
  mv -f "$publish_dir/$name" "$repo_dir/data/$name"
done
transaction_active=0

printf 'Replaced %s\nReplaced %s\nReplaced %s\nReplaced %s\nReplaced %s\n' \
  "$repo_dir/data/counterexample-gap-4.16.0.txt" \
  "$repo_dir/data/G3-verification-gap-4.16.0.txt" \
  "$repo_dir/data/mmc-crosscheck-gap-4.16.0.txt" \
  "$repo_dir/data/counterexample-gap-4.11.1.txt" \
  "$repo_dir/data/G3-verification-gap-4.11.1.txt"
