#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
image="${GAP_IMAGE:-gapsystem/gap-docker@sha256:d66dca500c3d8b8ca88824d3c3c7315183335af029f6b74ce592ed0d148edaee}"
native_gap="${GAP_BIN:-$HOME/dev/.tools/gap-4.16.0/gap}"
revision="${MMC_REPOSITORY_REVISION:-$(git -C "$repo_dir" rev-parse HEAD 2>/dev/null || printf unknown)}"
if [[ -z "${MMC_REPOSITORY_REVISION:-}" ]] &&
   [[ -n "$(git -C "$repo_dir" status --porcelain 2>/dev/null || true)" ]]; then
    revision="${revision}+dirty"
fi

printf '# repository_revision=%s\n' "$revision"
printf '# host=%s-%s\n' "$(uname -s)" "$(uname -m)"
printf '# invocation=./src/run-gap.sh'
printf ' %q' "$@"
printf '\n'

if [[ -x "$native_gap" ]]; then
  printf '# runner=native gap_binary=%s\n' "$native_gap"
  cd "$repo_dir"
  exec "$native_gap" -A -q "$@"
fi

printf '# runner=docker image=%s platform=linux/amd64\n' "$image"
exec docker run --rm --platform linux/amd64 \
  -v "$repo_dir:/work" -w /work -i "$image" gap -A -q "$@"
