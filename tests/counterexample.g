Read("src/mmc.g");;
Read("src/counterexample.g");;
SizeScreen([200, 24]);;

Check := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

c := MMCBuildCounterexample(3);;
g := c.group;;
mx := c.mx_subgroup;;
my := c.my_subgroup;;
n := c.n_subgroup;;
h := c.h_subgroup;;
z := c.z_subgroup;;

Check(Size(g) = 2^6 * 3^8, "wrong order for G");
Check(Size(c.l_subgroup) = 3^8, "wrong order for L");
Check(Size(h) = 2^6, "wrong order for H");
Check(Size(z) = 3^4, "wrong order for Z");
Check(DerivedSubgroup(c.l_subgroup) = z, "L' is not Z");
Check(FrattiniSubgroup(c.l_subgroup) = z, "Phi(L) is not Z");
Check(IsNormal(g, z), "Z is not normal in G");
Check(IsElementaryAbelian(z), "Z is not elementary abelian");
Check(IsElementaryAbelian(SylowSubgroup(mx, 3)),
      "the normal 3-subgroup of Mx is not elementary abelian");
Check(IsElementaryAbelian(SylowSubgroup(my, 3)),
      "the normal 3-subgroup of My is not elementary abelian");

Check(Index(g, mx) = 9 and Index(g, my) = 9,
       "the two named top subgroups should have index 9");
Check(Index(mx, n) = 9 and Index(my, n) = 9,
       "N should have index 9 in both named top subgroups");
Check(Index(n, h) = 81, "H should have index 81 in N");

# Empty intermediate-subgroup lists independently certify maximality of the
# three named inclusions.
Check(Length(IntermediateSubgroups(g, mx).subgroups) = 0,
       "Mx is not maximal in G");
Check(Length(IntermediateSubgroups(g, my).subgroups) = 0,
       "My is not maximal in G");
Check(Length(IntermediateSubgroups(mx, n).subgroups) = 0,
       "N is not maximal in Mx");
Check(Length(IntermediateSubgroups(my, n).subgroups) = 0,
       "N is not maximal in My");
Check(Length(IntermediateSubgroups(n, h).subgroups) = 0,
       "H is not maximal in N");

top_maximals := MaximalSubgroupClassReps(g);;
middle_maximals := MaximalSubgroupClassReps(mx);;
bottom_maximals := MaximalSubgroupClassReps(n);;
top_spectrum := Set(List(top_maximals, m -> Index(g, m)));;
middle_spectrum := Set(List(middle_maximals, m -> Index(mx, m)));;
bottom_spectrum := Set(List(bottom_maximals, m -> Index(n, m)));;

Check(top_spectrum = [2, 9], "wrong maximal-index spectrum for G");
Check(middle_spectrum = [2, 9, 81],
       "wrong maximal-index spectrum for Mx");
Check(bottom_spectrum = [2, 81],
      "wrong maximal-index spectrum for N");
Check(Length(Filtered(top_maximals, m -> Index(g, m) = 9)) = 2,
      "G should have two conjugacy classes of index-9 maximals");
Check(Length(Filtered(middle_maximals, m -> Index(mx, m) = 9)) = 1,
      "Mx should have one conjugacy class of index-9 maximals");
Check(Length(Filtered(bottom_maximals, m -> Index(n, m) = 81)) = 1,
      "N should have one conjugacy class of index-81 maximals");

witness := MMCConstructWitness(g);;
Check(witness = fail, "the proposed counterexample has a monotone chain");

Print("PASS counterexample order=", Size(g),
      " spectra=", top_spectrum, "/", middle_spectrum, "/", bottom_spectrum,
      " monotone_chain=false\n");
QUIT_GAP(0);
