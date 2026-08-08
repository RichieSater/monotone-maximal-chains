#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
image="${GAP_IMAGE:-gapsystem/gap-docker:latest}"
native_gap="${GAP_BIN:-$HOME/dev/.tools/gap-4.16.0/gap}"

if [[ -x "$native_gap" ]]; then
  cd "$repo_dir"
  exec "$native_gap" -A -q "$@"
fi

exec docker run --rm --platform linux/amd64 \
  -v "$repo_dir:/work" -w /work -i "$image" gap -A -q "$@"
