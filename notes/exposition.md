# The mathematical idea

A maximal chain records how a finite group can be built by successive
maximal inclusions. Finite nilpotent groups admit chains with nondecreasing
indices by adjoining Sylow factors in increasing prime order. The question
is whether some choice of chain always achieves this, even without
nilpotence. A counterexample must rule out every choice of maximal subgroup,
not merely display a chain with a decrease.

The construction uses the $t=2$ case of Kohler's example. A class-two
$p$-group $L$ has two nonisomorphic irreducible modules of dimension $2$ in
$L/\Phi(L)$ and an irreducible commutator module $Z=\Phi(L)$ of dimension
$4$, under $H=D_8\times D_8$. Every maximal subgroup of $L\rtimes H$
contains $Z$, so the four-dimensional module contributes no maximal index
there. Inside either index-$p^2$ maximal subgroup, however, $Z$ becomes a
complemented summand, making index $p^4$ available. Thus a large maximal
index first appears below a smaller one.

The spectra are $\{2,p^2\}$ at $G_p$, $\{2,p^2,p^4\}$ at either middle
subgroup, and $\{2,p^4\}$ at $N=Z\rtimes H$. The conjugacy statements
identify all possible index-$p^2$ steps. Reading an increasing chain
downward forces two such steps to $N$, where the next index must be $2$.
All remaining indices would then be $2$, contrary to $p\mid\lvert N\rvert$.
This is the reusable observation: local spectra and the subgroups realizing
their indices can control all maximal chains without a full subgroup-lattice
calculation. The proof works for every odd prime; the standalone GAP
calculation separately checks the explicit group of order $419904$ at
$p=3$, without asserting that this is the least possible counterexample.
