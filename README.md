# Finite Soluble Groups Need Not Admit Increasing Unrefinable Subgroup Chains

This repository contains a mathematical note, exact GAP verification scripts,
and captured outputs for a negative answer to a question on increasing
unrefinable subgroup chains communicated to the author during correspondence
with V. S. Monakhov and I. L. Sokhor.

For every odd prime \(p\), the note constructs a soluble matrix group
\(G_p\leq \operatorname{GL}_5(p)\) of order \(2^6p^8\) with no unrefinable
subgroup chain whose successive indices are nondecreasing. Its central
mechanism is the nested maximal-index pattern

\[
\{2,p^2\}\longrightarrow\{2,p^2,p^4\}
\longrightarrow\{2,p^4\},
\]

Reading downward, monotonicity forces two index-\(p^2\) steps to the terminal
group \(N\). Its only admissible next index is \(2\), so every remaining lower
index would also be \(2\), contradicting \(p\mid\lvert N\rvert\). The smallest
member of the family, \(G_3\), has order \(419904\); no claim of global
minimality is made.

The ordinary group-theoretic argument proves the family for every odd prime.
GAP reproduces selected instances at \(p=3,5,7\) and exhaustively searches
the displayed group \(G_3\); these computations corroborate the construction
but do not establish its universal quantifier.

## Read and cite

- [Current manuscript PDF](paper/main.pdf)
- [Version 2.0.0 preprint and verification archive](https://doi.org/10.5281/zenodo.22213657)
- [GitHub release v2.0.0](https://github.com/RichieSater/monotone-maximal-chains/releases/tag/v2.0.0)

The version DOI identifies the current seven-page manuscript and its
verification materials. The archive includes the manuscript, the standalone
`G3-verification.g` script, captured successful runs under GAP 4.11.1 and GAP
4.16.0, a source archive, and SHA-256 checksums. The concept DOI
[10.5281/zenodo.21878836](https://doi.org/10.5281/zenodo.21878836) resolves to
the latest archived version.

## Verify

Run the complete verification and regression suite with:

```sh
make test
```

The test target also runs the fail-closed public-corpus policy check, its
mutation tests, a transactional output-capture regression, and a clean
source-to-PDF byte comparison. It requires Python 3, Tectonic 0.17.0, and the
Poppler tools `pdftotext` and `pdfinfo`. GAP is found in the following order:

1. the executable named by `GAP_BIN`;
2. the default native path `$HOME/dev/.tools/gap-4.16.0/gap`;
3. the digest-pinned GAP 4.11.1 Docker image used by `src/run-gap.sh`.

Thus a machine without the default native installation must set `GAP_BIN` to
an executable GAP binary or have Docker available.

To rebuild the manuscript, run:

```sh
make paper
```

The build uses the stable source timestamp recorded in the `Makefile`. To
check the source against the committed PDF without modifying either file, run:

```sh
make paper-sync
```

To regenerate every captured GAP output, including both standalone
`G3-verification.g` logs, from a clean working tree with native GAP 4.16.0 and
Docker available, run:

```sh
make outputs
```

The output-capture target expects the native binary at
`$HOME/dev/.tools/gap-4.16.0/gap`; set `GAP_416_BIN` to override that path.
It captures and validates all five runs in temporary storage before replacing
any tracked file in `data/`. It records the exact repository revision in each
staged output and retains backups until the entire five-file replacement has
succeeded. An ordinary publish-phase failure triggers restoration of the
original set. If restoration itself fails, the target exits with status 74 and
retains a complete backup directory whose path is reported on standard error.

## License

The manuscript, documentation, and captured textual results are licensed
under CC BY 4.0. Source code is licensed under the MIT License. See
[`LICENSE`](LICENSE) for the exact file-level split.
