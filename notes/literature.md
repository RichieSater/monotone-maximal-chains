# Literature notes

## Direct background

- Victor S. Monakhov and Irina L. Sokhor, **On Indices of Maximal Chains in
  Finite Groups**, *Results in Mathematics* **80** (2025), article 155,
  DOI: [10.1007/s00025-025-02468-5](https://doi.org/10.1007/s00025-025-02468-5).
  This paper introduces the `<`-chain and `>`-chain terminology used in
  the question. It proves a supersolvability criterion from two monotone
  chains of the same length in opposite directions and classifies finite
  groups in which every maximal chain in every proper subgroup is a
  `<`-chain or a `>`-chain.

  The universal-existence question addressed in this repository is not
  attributed to that article. It was communicated to Richie Sater during
  correspondence with Monakhov and Sokhor beginning on August 8, 2026. This
  records how Sater learned of the question, not priority for its original
  formulation; the article supplies the surrounding terminology and
  background.

- Victor S. Monakhov and Irina L. Sokhor, **To the Iwasawa and Huppert
  Theorems on Supersolvability of Finite Groups**, *Siberian Electronic
  Mathematical Reports* **22** (2025), 143--153,
  DOI: [10.33048/semi.2025.22.011](https://doi.org/10.33048/semi.2025.22.011).
  This open-access paper treats monotone chains whose indices are all prime.
  It includes the useful test groups `SmallGroup(36,9)`,
  `SmallGroup(216,153)`, and `SmallGroup(200,43)`.

## Source of the construction

- Joseph Kohler, **Finite Groups with All Maximal Subgroups of Prime or Prime
  Square Index**, *Canadian Journal of Mathematics* **16** (1964), 435--442,
  DOI: [10.4153/CJM-1964-046-6](https://doi.org/10.4153/CJM-1964-046-6).
  In Section 4, especially Theorem 4.1, Kohler constructs, for every odd
  prime $p$ and positive integer $t$, a soluble group with property (M)---every
  maximal subgroup has prime or prime-square index---containing a subgroup
  with a maximal subgroup of index $p^{2^t}$.  The counterexample
  in this repository is modeled on the $t=2$ case: its four degree-one
  coordinates and four independent cross-commutator coordinates yield a
  group of order $p^8$. The observation here is that its nested
  maximal-index spectra exclude every nondecreasing maximal chain.

- Joseph Kohler, **Finite Groups with All Maximal Subgroups of Prime or Prime
  Square Index**, PhD thesis, California Institute of Technology (1962),
  DOI: [10.7907/JRE0-KW77](https://doi.org/10.7907/JRE0-KW77).
  The thesis contains a longer presentation of the same construction.

## Related structural material consulted

- Greg Kuperberg and Michael E. Zieve, **Analogues of the Jordan--Hölder
  Theorem for Transitive $G$-Sets**, arXiv:0712.4142 (2007),
  DOI: [10.48550/arXiv.0712.4142](https://doi.org/10.48550/arXiv.0712.4142).
  They study a Jordan property for subgroup-lattice intervals: under specified
  hypotheses, every maximal chain between a point stabilizer and a transitive
  permutation group has the same length and the same relative indices up to
  permutation.  This invariance problem across all chains is adjacent to, but
  logically different from, the existential ordering question considered here.

- V. S. Monakhov, **Indices of Maximal Subgroups of Finite Soluble Groups**,
  *Algebra and Logic* **43** (2004), 230--237,
  DOI: [10.1023/B:ALLO.0000035114.00094.62](https://doi.org/10.1023/B:ALLO.0000035114.00094.62).

- Robert M. Guralnick and Gareth Tracey, **On the generalized Fitting height
  and insoluble length of finite groups**, *Bulletin of the London
  Mathematical Society* **52** (2020), 924--931,
  DOI: [10.1112/blms.12372](https://doi.org/10.1112/blms.12372).  This contains a
  generalization of Wielandt's zipper lemma for subgroups lying in a unique
  maximal overgroup.  It was relevant to an abandoned positive-proof route.

## Access note

The terminology statement above was checked against the article text. The
SEMR paper, Kohler paper/thesis, and published Guralnick--Tracey record were
consulted through the linked primary sources.

## Search boundary (August 27--29, 2026)

A reproducible title-and-abstract search was run in OpenAlex using the
following ten queries:

1. `increasing unrefinable subgroup chain finite groups`;
2. `<-chain maximal chain finite group indices`;
3. `nondecreasing indices maximal chain finite group`;
4. `successive indices maximal subgroups saturated chain group lattice`;
5. `maximal subgroup index sequence finite group chain`;
6. `saturated chains subgroup lattice indices finite groups`;
7. `prescribed indices maximal chains finite groups`;
8. `chain of maximal subgroups index sequence soluble group`;
9. `maximal-index spectra finite groups`;
10. `Kohler construction monotone maximal chains finite groups`.

Crossref searches using the exact Monakhov--Sokhor and Kohler titles, together
with broader queries for indices of maximal chains, recovered the two primary
sources above and adjacent work on maximal-subgroup indices. The published
abstract for Monakhov--Sokhor and the full Kohler paper were inspected.  The
corrected second query above was rerun after the terminology was checked
against the published abstract.
No searched result stated the universal-existence counterexample or the same
three-level spectrum obstruction. This negative search result is not proof of
priority, and the manuscript therefore makes no priority claim for the
abstract criterion.

An exact-title search on August 29 located the Kuperberg--Zieve preprint above;
its abstract and definition of the Jordan property were checked against the
full arXiv source before the comparison was added to the manuscript.
