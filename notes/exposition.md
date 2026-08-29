# Exposition aids

## Three-paragraph explanation

The problem asks whether every finite group has an unrefinable subgroup chain
whose successive indices are nondecreasing. Because the assertion is
existential, displaying many badly ordered chains does not refute it: a
counterexample must control every possible maximal step. The paper replaces
that global subgroup-lattice search with a local directed system of
maximal-index spectra.

The construction adapts the $t=2$ case of Kohler's class-two $p$-group with a
$D_8\times D_8$ action. Two nonisomorphic irreducible layers of dimension $2$
and an irreducible commutator layer of dimension $4$ produce the nested
spectra $\{2,p^2\}$, $\{2,p^2,p^4\}$, and $\{2,p^4\}$. The identity
$Z=\Phi(L)$ ensures that every maximal subgroup at the top contains $Z$, so no
additional maximal subgroups escape the quotient calculation.

Reading a prospective increasing chain downward, monotonicity forces two
consecutive steps of index $p^2$. At the resulting subgroup $N$, the only
admissible next index is $2$, which forces all remaining lower indices to
equal $2$ and contradicts $p\mid\lvert N\rvert$. This nested spectrum trap is the
transferable idea: a small labeled diagram can control every maximal chain
without classifying the full subgroup lattice. Ordinary mathematics proves
the result for every odd prime; the GAP computations provide finite
corroboration and regression protection.
