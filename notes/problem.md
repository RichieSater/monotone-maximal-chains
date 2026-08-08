# Problem statement and conventions

## Problem

For every finite group \(G\), is there a chain
\[
1=G_0<G_1<\cdots<G_n=G
\]
such that:

1. \(G_i\) is a maximal proper subgroup of \(G_{i+1}\) for every \(0\le i<n\); and
2. the upward indices \(a_i=[G_i:G_{i-1}]\) satisfy
   \(a_1\le a_2\le\cdots\le a_n\)?

We call such a chain a **monotone maximal chain** (MMC).

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

Let \(\mu(H)\) denote the least possible final index in a monotone maximal chain from \(1\) to \(H\), with \(\mu(1)=1\), if such a chain exists. More generally track all attainable final indices. Then \(G\) has an MMC exactly when some maximal subgroup \(M<G\) has an MMC ending with an index at most \([G:M]\).
