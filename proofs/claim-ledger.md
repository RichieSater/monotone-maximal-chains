# Claim ledger

| Claim | Mathematical check | Computational check |
|---|---|---|
| $D=\langle s,t\rangle\cong D_8$ and its natural module is absolutely irreducible | $s^2=t^2=1$, $st$ has order $4$; over an algebraic closure the $t$-eigenlines are swapped by $s$ | The generated complement has order $8^2=64$ |
| $|L|=p^8$ | Unique coordinates $x\in F^2$, $y\in(F^2)^*$, $z\in M_2(F)$ | For $p=3$, GAP returns $3^8$ |
| $L'=\Phi(L)=Z\cong C_p^4$ | Outer products span $M_2(F)$; $L$ has exponent $p$; use $\Phi(L)=L^pL'$ | `DerivedSubgroup(L)=Z` and `FrattiniSubgroup(L)=Z` |
| $L/Z=\bar X\oplus\bar Y$, with two nonisomorphic irreducible 2-dimensional modules | Each direct factor of $D\times D$ acts naturally on exactly one summand | Reflected in the two index-$9$ maximal-subgroup classes of $G_3$ |
| $Z\cong U\boxtimes U^*$ is irreducible of dimension $4$ | External tensor products of absolutely irreducible modules for direct-product factors are absolutely irreducible | The complement $H$ is maximal in $N=Z\rtimes H$ with index $81$ |
| Every maximal subgroup of $G_p$ contains $Z$ | If $G_p=ZM$, then $L=Z(L\cap M)=\Phi(L)(L\cap M)$, forcing $L\le M$ | All maximal-index computations agree with the quotient calculation |
| $\mathcal I(G_3)=\{2,9\}$ | Semidirect-product lemma applied to $(\bar X\oplus\bar Y)\rtimes H$ | GAP 4.16.0 and GAP 4.11.1 |
| $\mathcal I(M_X)=\{2,9,81\}$ | Apply the lemma to $(Z\oplus X)\rtimes H$ | Both GAP versions |
| $\mathcal I(N)=\{2,81\}$ | Apply the lemma to irreducible $Z\rtimes H$ | Both GAP versions |
| No increasing unrefinable chain exists | The spectra force final indices $p^2,p^2,2$; the last choice would make a group divisible by $p$ have order a power of $2$ | Exhaustive `MMCConstructWitness(G_3)` returns `fail` |

Captured outputs are in `data/counterexample-gap-4.16.txt` and
`data/counterexample-gap-4.11.1.txt`.
