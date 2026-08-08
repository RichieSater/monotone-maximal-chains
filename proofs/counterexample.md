# An infinite family of counterexamples

## Result

The answer to Monakhov and Sokhor's question, communicated to Richie Sater
by Monakhov's email of August 8, 2026, is **no**. For every odd
prime $p$, the group $G_p$ constructed below has no unrefinable subgroup
chain with nondecreasing indices. The smallest member, $G_3$, has order

\[
|G_3|=2^6 3^8=419904.
\]

The construction is modeled on the $t=2$ case of an idea used by Joseph Kohler
to show that bounds on maximal-subgroup indices need not pass to subgroups.
The obstruction to a monotone chain appears to be new.

## A maximal-subgroup lemma

Let $V$ be an elementary abelian $p$-group and let a $p'$-group $H$
act on $V$. Put $K=V\rtimes H$. Then the maximal subgroups of $K$
are of the following two types:

1. $V\rtimes J$, where $J$ is maximal in $H$;
2. a $V$-conjugate of $W\rtimes H$, where $W$ is a maximal proper
   $H$-submodule of $V$.

Indeed, let $T$ be maximal in $K$. If $V\le T$, pass to $K/V\cong H$.
Otherwise $VT=K$. The subgroup $W=V\cap T$ is normalized by $T$, and
it is centralized by $V$, so $W\lhd K$. In $K/W$, both $T/W$ and
$WH/W$ are complements to $V/W$. Schur--Zassenhaus makes them
$V/W$-conjugate. Maximality of $T$ is then equivalent to maximality of
$W$ among proper $H$-submodules.

In particular, if $H$ is a $2$-group, the first type has index $2$,
while an irreducible summand of dimension $d$ over $\mathbb F_p$ gives
an index $p^d$ in the second type.

## Construction

Fix an odd prime $p$, put $F=\mathbb F_p$, and let

\[
s=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
t=\begin{pmatrix}1&0\\0&-1\end{pmatrix}.
\]

Then $D=\langle s,t\rangle\cong D_8$. Its natural two-dimensional
$F$-module $U$ is absolutely irreducible: over an algebraic closure, the
only $t$-eigenlines are the two coordinate lines, and $s$ interchanges
them.

Let $H=D\times D$. Define

\[
L=\left\{
\ell(x,y,z)=
\begin{pmatrix}
I_2&x&z\\
0&1&y\\
0&0&I_2
\end{pmatrix}
:x\in F^{2\times1},\ y\in F^{1\times2},\ z\in F^{2\times2}
\right\}.
\]

Multiplication is

\[
\ell(x,y,z)\ell(x',y',z')
=\ell(x+x',y+y',z+z'+xy').
\]

Thus $|L|=p^8$. Put

\[
Z=\{\ell(0,0,z)\},\quad
X=\{\ell(x,0,0)\},\quad
Y=\{\ell(0,y,0)\}.
\]

The outer products $xy$ span $F^{2\times2}$, so $L'=Z$. The group
$L$ has exponent $p$, whence

\[
\Phi(L)=L^pL'=Z.
\]

Embed $H$ as the block-diagonal matrices
$\operatorname{diag}(A,1,B)$, with $A,B\in D$. Conjugation gives

\[
x\longmapsto Ax,\qquad
y\longmapsto yB^{-1},\qquad
z\longmapsto AzB^{-1}.
\]

Finally set $G_p=L\rtimes H\le \operatorname{GL}_5(p)$. Its order is
$2^6p^8$. Both factors are soluble, so $G_p$ is soluble.

Set $\bar X=XZ/Z$ and $\bar Y=YZ/Z$. As an $H$-module,

\[
L/Z\cong \bar X\oplus\bar Y,
\]

where both summands are irreducible of dimension $2$. Their kernels in
$H=D\times D$ are respectively $1\times D$ and $D\times1$, so they are
nonisomorphic. Since $p\nmid |H|=64$, Maschke's theorem applies and these
are the only maximal $H$-submodules of $L/Z$. Moreover,

\[
Z\cong U\boxtimes U^*,
\]

the external tensor product for the two factors of $D\times D$. Over an
algebraic closure, $U$ and $U^*$ remain irreducible, and their external
tensor product is irreducible for $D\times D$. Hence $Z$ is an irreducible
$H$-module of dimension $4$.

## Maximal-subgroup spectra

The conjugation formulas show explicitly that $Z\lhd G_p$. Every maximal
subgroup $M$ of $G_p$ contains $Z$. Otherwise
$G_p=ZM$, and the modular law gives

\[
L=Z(L\cap M)=\Phi(L)(L\cap M).
\]

Here we use the standard Frattini fact that
$L=\Phi(L)K$ implies $K=L$: if $K<L$, a maximal subgroup containing $K$
also contains $\Phi(L)$, a contradiction. Thus $L\cap M=L$, contrary to
$Z\nleq M$.

Consequently the maximal subgroups of $G_p$ are read off from

\[
G_p/Z=(\bar X\oplus\bar Y)\rtimes H.
\]

The lemma gives the maximal-index spectrum

\[
\mathcal I(G_p)=\{2,p^2\}.
\]

Every maximal subgroup of index $p^2$ is conjugate to one of

\[
M_X=(Z\times X)\rtimes H,
\qquad
M_Y=(Z\times Y)\rtimes H.
\]

The two cases are symmetric. In $M_X$, the normal elementary abelian
subgroup $Z\times X$ is the direct sum of irreducible $H$-modules of
dimensions $4$ and $2$. Therefore

\[
\mathcal I(M_X)=\{2,p^2,p^4\}.
\]

The maximal subgroups of $M_X$ of index $p^2$ are conjugate to

\[
N=Z\rtimes H.
\]

Since $Z$ is irreducible of dimension $4$, a final application of the
lemma gives

\[
\mathcal I(N)=\{2,p^4\}.
\]

## Excluding a nondecreasing chain

Suppose

\[
1=G_0<G_1<\cdots<G_n=G_p
\]

were unrefinable, with $j_i=[G_i:G_{i-1}]$ nondecreasing.

The last index belongs to $\{2,p^2\}$. It cannot be $2$, since then all
the $j_i$ would equal $2$, whereas $p\mid |G_p|$. Hence $j_n=p^2$,
and $G_{n-1}$ is conjugate to $M_X$ or $M_Y$.

Inside that subgroup, the last available index must be at most $p^2$.
Its spectrum is $\{2,p^2,p^4\}$. Again it cannot be $2$, so it equals
$p^2$, and $G_{n-2}$ is conjugate to $N=Z\rtimes H$.

But $N$ has maximal-index spectrum $\{2,p^4\}$. The next index must be
at most $p^2$, so it would have to be $2$. All earlier indices would
then also be $2$, impossible because $p\mid |N|$.

This contradiction proves that $G_p$ has no required chain.

## Computational check

Run:

~~~sh
./src/run-gap.sh tests/counterexample.g
~~~

For $p=3,5,7$, GAP reproduces the predicted spectra. For $p=3$ they are

~~~text
[2,9], [2,9,81], [2,81]
~~~

and an exhaustive branch-and-bound search returns no monotone maximal
chain.
