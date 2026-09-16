# Claim ledger

| Claim | Mathematical check | Computational check |
|---|---|---|
| The nested spectra force an all-$2$ tail contradiction | Reading downward, the spectra and two conjugacy-incidence statements force two index-$p^2$ steps to $N$.  The next admissible index is $2$, so every remaining lower index would also be $2$, contradicting $p\mid\lvert N\rvert$ | The $p=3$ exhaustive search separately returns no chain |
| $D=\langle s,t\rangle\cong D_8$ and its natural module is absolutely irreducible | $s^2=t^2=1$, $st$ has order $4$; over an algebraic closure the $t$-eigenlines are swapped by $s$ | The generated complement has order $8^2=64$ |
| $\lvert L\rvert=p^8$ | Unique coordinates $x\in F^2$, $y\in(F^2)^*$, $z\in M_2(F)$ | For $p=3$, GAP returns $3^8$ |
| $L'=\Phi(L)=Z\cong C_p^4$ | Outer products span $M_2(F)$; $L$ has exponent $p$; use $\Phi(L)=L^pL'$ | `DerivedSubgroup(L)=Z` and `FrattiniSubgroup(L)=Z` |
| $L/Z=X\oplus Y$, identifying each subgroup with its image, has two nonisomorphic irreducible 2-dimensional summands | Each direct factor of $D\times D$ acts nontrivially on exactly one summand | Reflected in the two index-$9$ maximal-subgroup classes of $G_3$ |
| The $H$-module $Z\cong M_2(\mathbb F_p)$ is irreducible of dimension $4$ | $D$ spans $M_2(\mathbb F_p)$, so an invariant subspace is stable under all left and right matrix multiplications; any nonzero element yields every matrix unit | The complement $H$ is maximal in $N=Z\rtimes H$ with index $81$ |
| Every maximal subgroup of $G_p$ contains $Z$ | If $G_p=ZM$, then $L=Z(L\cap M)=\Phi(L)(L\cap M)$, forcing $L\le M$ | All maximal-index computations agree with the quotient calculation |
| $\mathcal I(G_3)=\{2,9\}$ | Semidirect-product calculation applied to $(X\oplus Y)\rtimes H$, identifying $X,Y$ with their images in $L/Z$ | GAP 4.16.0 and GAP 4.11.1 |
| $\mathcal I(M_X)=\{2,9,81\}$ | Semidirect-product calculation for $(Z\oplus X)\rtimes H$ | Both GAP versions |
| $\mathcal I(N)=\{2,81\}$ | Semidirect-product calculation for irreducible $Z\rtimes H$ | Both GAP versions |
| No increasing unrefinable chain exists for every odd $p$ | The ordinary proof realizes and applies the nested-spectrum criterion uniformly | Exhaustive `MMCConstructWitness(G_3)` returns `fail`; the runs at $p=5,7$ are additional finite corroboration |

The special case $p=3$ also has a self-contained verification script in
`G3-verification.g`. It contains the eight literal $5\times5$ matrices,
imports no other file, enumerates the complete maximal-class index lists, and
runs a separate top-down exhaustive search. Captured executions under GAP
4.11.1 and GAP 4.16.0 are in
`data/G3-verification-gap-4.11.1.txt` and
`data/G3-verification-gap-4.16.0.txt`.

Captured outputs are in `data/counterexample-gap-4.16.0.txt` and
`data/counterexample-gap-4.11.1.txt`. The separate exhaustive recurrence and
witness-validation output is in `data/mmc-crosscheck-gap-4.16.0.txt`.
