# A Negative Answer to a Question on Monotone Maximal Chains in Finite Groups

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21878836.svg)](https://doi.org/10.5281/zenodo.21878836)

This repository contains a five-page mathematical note and reproducible GAP
certificates for a negative answer to the Monakhov–Sokhor question on
increasing unrefinable subgroup chains.

For every odd prime `p`, the note constructs a soluble matrix group
`G_p <= GL_5(p)` of order `2^6 p^8` with no unrefinable subgroup chain whose
successive indices are nondecreasing. The smallest member of this family,
`G_3`, has order `419904`; no claim of global minimality is made.

## Read and cite

- [Zenodo record for version 1.1.0](https://doi.org/10.5281/zenodo.21878837)
- [GitHub release v1.1.0](https://github.com/RichieSater/monotone-maximal-chains/releases/tag/v1.1.0)
- [Manuscript PDF](paper/main.pdf)

The Zenodo record includes the note, the standalone `G3-verification.g`
certificate, captured successful runs under GAP 4.11.1 and GAP 4.16.0, a
source archive, and SHA-256 checksums.

## Verify

Run the complete certificate and regression suite with:

```sh
make test
```

To rebuild the manuscript (with Tectonic installed), run:

```sh
make paper
```

## License

The manuscript, documentation, and captured textual results are licensed
under CC BY 4.0. Source code is licensed under the MIT License. See
[`LICENSE`](LICENSE) for the exact file-level split.
