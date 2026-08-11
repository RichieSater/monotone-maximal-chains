# Problem statement and conventions

The documented source through which Richie Sater learned of the question is
correspondence with Victor Monakhov and Irina Sokhor beginning on August 8,
2026. This records the transmission of the question and does not assert
priority for its original formulation. See
[`question-provenance.md`](question-provenance.md).

## Problem

For every finite group \(G\), is there a chain
\[
1=G_0<G_1<\cdots<G_n=G
\]
such that:

1. \(G_i\) is a maximal proper subgroup of \(G_{i+1}\) for every \(0\le i<n\); and
2. the upward indices \(a_i=\lvert G_i:G_{i-1}\rvert\) satisfy
   \(a_1\le a_2\le\cdots\le a_n\)?

Monakhov and Sokhor call such a chain a **`(<)`-chain**. This repository also
uses the descriptive term **monotone maximal chain** (MMC).

## Resolution

The answer is negative.  See `proofs/counterexample.md` for an infinite
family of soluble counterexamples of order \(2^6p^8\), one for each odd
prime \(p\).

## Immediate observations

- Since \(G_1\) is minimal nontrivial, \(|G_1|\) is prime.
- The product of the index sequence is \(|G|\).
- The property is invariant under group isomorphism.
- A counterexample can be sought among groups for which every maximal subgroup either fails recursively or forces too small a final index.

## Recursive formulation

Let \(\mu(H)\) denote the least possible final index in a monotone maximal chain from \(1\) to \(H\), with \(\mu(1)=1\), if such a chain exists. More generally track all attainable final indices. Then \(G\) has an MMC exactly when some maximal subgroup \(M<G\) has an MMC ending with an index at most \(\lvert G:M\rvert\).
