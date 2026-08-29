#!/usr/bin/env python3
"""Rebuild the manuscript in isolation and compare it with the public PDF."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile


EXPECTED_TECTONIC_VERSION = "Tectonic 0.17.0"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_checked(command: list[str], *, cwd: Path, env: dict[str, str]) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode:
        print(result.stdout, file=sys.stderr, end="")
        raise RuntimeError(f"command failed with exit status {result.returncode}")
    return result.stdout


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    source = root / "paper" / "main.tex"
    expected = root / "paper" / "main.pdf"
    if not source.is_file() or not expected.is_file():
        print("paper/main.tex and paper/main.pdf must both exist", file=sys.stderr)
        return 1

    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "paper/main.pdf"],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if tracked.returncode:
        print("paper/main.pdf must be tracked", file=sys.stderr)
        return 1

    tectonic = os.environ.get("TECTONIC", "tectonic")
    try:
        version = subprocess.run(
            [tectonic, "--version"],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"cannot run Tectonic: {exc}", file=sys.stderr)
        return 1
    if version != EXPECTED_TECTONIC_VERSION:
        print(
            f"expected {EXPECTED_TECTONIC_VERSION}, found {version}",
            file=sys.stderr,
        )
        return 1

    epoch = os.environ.get("SOURCE_DATE_EPOCH", "")
    if not epoch.isdigit():
        print("SOURCE_DATE_EPOCH must be a nonnegative integer", file=sys.stderr)
        return 1
    env = os.environ.copy()
    env.update(
        {
            "SOURCE_DATE_EPOCH": epoch,
            "FORCE_SOURCE_DATE": "1",
            "TZ": "UTC",
        }
    )

    try:
        with tempfile.TemporaryDirectory(prefix="monotone-paper-sync-") as tmp:
            outdir = Path(tmp)
            run_checked(
                [tectonic, "-X", "compile", str(source), "--outdir", str(outdir)],
                cwd=root,
                env=env,
            )
            rebuilt = outdir / "main.pdf"
            if not rebuilt.is_file():
                print("Tectonic did not produce main.pdf", file=sys.stderr)
                return 1
            expected_hash = sha256(expected)
            rebuilt_hash = sha256(rebuilt)
            if expected.read_bytes() != rebuilt.read_bytes():
                print("source-to-PDF synchronization failed", file=sys.stderr)
                print(f"  paper/main.pdf: {expected_hash}", file=sys.stderr)
                print(f"  rebuilt PDF:   {rebuilt_hash}", file=sys.stderr)
                print("run `make paper` and inspect the result", file=sys.stderr)
                return 1
    except (OSError, RuntimeError) as exc:
        print(f"PDF synchronization check failed: {exc}", file=sys.stderr)
        return 1

    print(f"source-to-PDF synchronization passed ({expected_hash})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
