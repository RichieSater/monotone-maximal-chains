# Proof and dependency map

The canonical statement and proof are in [`paper/main.tex`](../paper/main.tex).
This file is a navigation aid rather than a second full proof.

## Theorem and mechanism

For every odd prime $p$, the manuscript constructs a soluble group
$G_p\leq\operatorname{GL}_5(p)$ of order $2^6p^8$ with no increasing
unrefinable subgroup chain. Its conceptual core is the nested spectrum trap

\[
\{2,p^2\}\longrightarrow\{2,p^2,p^4\}
\longrightarrow\{2,p^4\},
\]

Reading downward, the trap forces two index-$p^2$ steps to $N$.  Its next
admissible index is $2$, so every remaining lower index would also be $2$,
contradicting $p\mid\lvert N\rvert$.

## Mathematical dependency graph

1. **Abstract obstruction — Proposition 2.** Three maximal-index spectra,
   two conjugacy-incidence statements, and $p\mid\lvert N\rvert$ exclude an
   increasing chain. This step is independent of the matrix construction.
2. **Coprime semidirect products — Lemma 3.** For $V\rtimes H$ with $V$ an
   elementary abelian $p$-group and $H$ a $p'$-group, the maximal subgroups
   arise either from maximal subgroups of $H$ or from maximal proper
   $H$-submodules of $V$.
3. **Matrix construction — Section 3.** The group $G_p=L\rtimes(D_8\times
   D_8)$ has $\lvert L\rvert=p^8$ and
   $L'=\Phi(L)=Z$. The quotient $L/Z$ has two nonisomorphic irreducible
   layers of dimension $2$, while $Z$ is an irreducible layer of dimension
   $4$.
4. **Frattini reduction and spectra — Lemma 4.** Every maximal subgroup of
   $G_p$ contains $Z$, so Lemma 3 applies successively to $G_p/Z$, the two
   middle groups, and $N=Z\rtimes(D_8\times D_8)$. It supplies exactly the
   spectra and incidences required by Proposition 2.
5. **Conclusion — Theorem 1.** Lemma 4 instantiates Proposition 2 for every
   odd prime $p$.

The reusable result is Proposition 2. The matrix family is adapted from the
$t=2$ construction in Section 4, especially Theorem 4.1, of Kohler's 1964
paper.

## Verification boundary

The universal quantifier is proved by the ordinary mathematical argument
above. GAP provides finite corroboration and regression protection:

- `tests/counterexample.g` checks the orders, spectra, incidences, and failed
  chain searches at $p=3,5,7$;
- `G3-verification.g` separately defines the eight literal matrices for
  $G_3$, enumerates the relevant maximal-subgroup classes, and exhaustively
  searches the admissible branches;
- `tests/mmc-crosscheck.g` compares the chain recurrence with a separate
  exhaustive index-sequence enumeration for all $144$ groups of order at
  most $32$.

Run the full suite with:

```sh
make test
```

Captured successful outputs are stored in `data/`. No proof assistant or
proof-producing computation is used.
