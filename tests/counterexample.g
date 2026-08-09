Read("src/mmc.g");;
Read("src/counterexample.g");;
SizeScreen([200, 24]);;

Print("# gap_version=", GAPInfo.Version, "\n");
Print("# test_primes=3,5,7\n");

Check := function(condition, message)
    if not condition then
        Print("FAIL ", message, "\n");
        QUIT_GAP(1);
    fi;
end;;

CheckCounterexample := function(p)
    local c, g, mx, my, n, h, z, top_maximals, mx_maximals,
          my_maximals, bottom_maximals, top_spectrum, mx_spectrum,
          my_spectrum, bottom_spectrum, top_p, mx_p, my_p, bottom_p,
          witness, label;

    label := Concatenation(" (p=", String(p), ")");
    c := MMCBuildCounterexample(p);
    g := c.group;
    mx := c.mx_subgroup;
    my := c.my_subgroup;
    n := c.n_subgroup;
    h := c.h_subgroup;
    z := c.z_subgroup;

    Check(Size(g) = 2^6 * p^8, Concatenation("wrong order for G", label));
    Check(Size(c.l_subgroup) = p^8, Concatenation("wrong order for L", label));
    Check(Size(h) = 2^6, Concatenation("wrong order for H", label));
    Check(Size(z) = p^4, Concatenation("wrong order for Z", label));
    Check(DerivedSubgroup(c.l_subgroup) = z,
          Concatenation("L' is not Z", label));
    Check(FrattiniSubgroup(c.l_subgroup) = z,
          Concatenation("Phi(L) is not Z", label));
    Check(IsNormal(g, z), Concatenation("Z is not normal in G", label));
    Check(IsElementaryAbelian(z),
          Concatenation("Z is not elementary abelian", label));
    Check(IsElementaryAbelian(SylowSubgroup(mx, p)),
          Concatenation("the normal p-subgroup of Mx is not elementary abelian", label));
    Check(IsElementaryAbelian(SylowSubgroup(my, p)),
          Concatenation("the normal p-subgroup of My is not elementary abelian", label));

    Check(Index(g, mx) = p^2 and Index(g, my) = p^2,
          Concatenation("the named top subgroups have wrong index", label));
    Check(Index(mx, n) = p^2 and Index(my, n) = p^2,
          Concatenation("N has wrong index in a named top subgroup", label));
    Check(Index(n, h) = p^4,
          Concatenation("H has wrong index in N", label));

    # Empty intermediate-subgroup lists directly certify maximality of the
    # five named inclusions.
    Check(Length(IntermediateSubgroups(g, mx).subgroups) = 0,
          Concatenation("Mx is not maximal in G", label));
    Check(Length(IntermediateSubgroups(g, my).subgroups) = 0,
          Concatenation("My is not maximal in G", label));
    Check(Length(IntermediateSubgroups(mx, n).subgroups) = 0,
          Concatenation("N is not maximal in Mx", label));
    Check(Length(IntermediateSubgroups(my, n).subgroups) = 0,
          Concatenation("N is not maximal in My", label));
    Check(Length(IntermediateSubgroups(n, h).subgroups) = 0,
          Concatenation("H is not maximal in N", label));

    top_maximals := MaximalSubgroupClassReps(g);
    mx_maximals := MaximalSubgroupClassReps(mx);
    my_maximals := MaximalSubgroupClassReps(my);
    bottom_maximals := MaximalSubgroupClassReps(n);
    top_spectrum := Set(List(top_maximals, m -> Index(g, m)));
    mx_spectrum := Set(List(mx_maximals, m -> Index(mx, m)));
    my_spectrum := Set(List(my_maximals, m -> Index(my, m)));
    bottom_spectrum := Set(List(bottom_maximals, m -> Index(n, m)));

    Check(top_spectrum = [2, p^2],
          Concatenation("wrong maximal-index spectrum for G", label));
    Check(mx_spectrum = [2, p^2, p^4],
          Concatenation("wrong maximal-index spectrum for Mx", label));
    Check(my_spectrum = [2, p^2, p^4],
          Concatenation("wrong maximal-index spectrum for My", label));
    Check(bottom_spectrum = [2, p^4],
          Concatenation("wrong maximal-index spectrum for N", label));

    # Check both the number of classes and coverage by the named subgroups.
    top_p := Filtered(top_maximals, m -> Index(g, m) = p^2);
    mx_p := Filtered(mx_maximals, m -> Index(mx, m) = p^2);
    my_p := Filtered(my_maximals, m -> Index(my, m) = p^2);
    bottom_p := Filtered(bottom_maximals, m -> Index(n, m) = p^4);
    Check(Length(top_p) = 2,
          Concatenation("G should have two classes of index-p^2 maximals", label));
    Check(not IsConjugate(g, mx, my),
          Concatenation("Mx and My should not be conjugate", label));
    Check(ForAny(top_p, m -> IsConjugate(g, m, mx)) and
          ForAny(top_p, m -> IsConjugate(g, m, my)) and
          ForAll(top_p, m -> IsConjugate(g, m, mx) or
                             IsConjugate(g, m, my)),
          Concatenation("Mx and My do not cover the top index-p^2 classes", label));
    Check(Length(mx_p) = 1 and
          ForAll(mx_p, m -> IsConjugate(mx, m, n)),
          Concatenation("N does not cover the Mx index-p^2 class", label));
    Check(Length(my_p) = 1 and
          ForAll(my_p, m -> IsConjugate(my, m, n)),
          Concatenation("N does not cover the My index-p^2 class", label));
    Check(Length(bottom_p) = 1 and
          ForAll(bottom_p, m -> IsConjugate(n, m, h)),
          Concatenation("H does not cover the N index-p^4 class", label));

    witness := MMCConstructWitness(g);
    Check(witness = fail,
          Concatenation("the proposed counterexample has a monotone chain", label));

    Print("PASS p=", p, " order=", Size(g),
          " spectra=G:", top_spectrum,
          " Mx:", mx_spectrum, " My:", my_spectrum, " N:", bottom_spectrum,
          " monotone_chain=false conjugacy_coverage=true\n");
end;;

for p in [3, 5, 7] do
    CheckCounterexample(p);
od;
QUIT_GAP(0);
