# The counterexample family

The statement and full proof are in [`paper/main.tex`](../paper/main.tex).
For every odd prime $p$, the soluble group
$G_p\leq\operatorname{GL}_5(p)$ has order $2^6p^8$ and admits no increasing
unrefinable subgroup chain.

## Argument

1. **Proposition 2, Section 2.** The three spectra
   $\{2,p^2\}$, $\{2,p^2,p^4\}$, and $\{2,p^4\}$, with the specified
   conjugacy conditions, force two downward index-$p^2$ steps to $N$.
   The next index must be $2$, forcing all lower indices to be $2$,
   contrary to $p\mid\lvert N\rvert$.
2. **Construction, Section 3.** The block-unitriangular group $L$ has
   $\lvert L\rvert=p^8$ and $L'=\Phi(L)=Z$. The complement
   $H=D_8\times D_8$ acts on $L/Z$ with two nonisomorphic irreducible
   summands of dimension $2$, and on $Z$ irreducibly in dimension $4$.
   The matrix-algebra argument proves this last assertion directly over
   $\mathbb F_p$.
3. **Maximal subgroups, Section 3.** Schur--Zassenhaus describes the maximal
   subgroups of an elementary abelian $p$-group extended by a $p'$-group.
   The manuscript gives the short argument immediately before Lemma 3.
4. **Lemma 3, Section 3.** Every maximal subgroup of $G_p$ contains $Z$.
   The semidirect-product calculation applies to $G_p/Z$, the two middle
   groups, and $N=Z\rtimes H$, giving the spectra and all required
   conjugacy statements.
5. **Theorem 1.** Proposition 2 applies since $\lvert N\rvert=2^6p^4$.

The group construction comes from the $t=2$ case of Section 4, especially
Theorem 4.1, of Kohler's 1964 paper. Its application to increasing chains
uses both the maximal indices and the subgroups realizing them.

## Computations

The proof for all odd primes is independent of computation. The supporting
GAP calculations check concrete groups and the chain-search implementation:

- `tests/counterexample.g` checks orders, spectra, maximal inclusions,
  conjugacy classes, and absence of increasing chains at $p=3,5,7$;
- `G3-verification.g` defines the eight literal matrices for $G_3$ from
  Section 4, computes the relevant maximal-subgroup classes, and runs a
  separate exhaustive top-down search without importing any other file;
- `tests/mmc-crosscheck.g` compares the chain recurrence with a separate
  exhaustive index-sequence enumeration for all 144 groups of order at
  most 32 and validates the subgroup chains returned.

These implementations share GAP's group algorithms. No proof assistant or
proof-producing computation is used. The Python tests check repository
safeguards and output handling, not the group-theoretic theorem.

Run the full suite with `make test`. Captured outputs are stored in `data/`.
