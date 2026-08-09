# Standalone verification of the explicit group G_3.
#
# Requirements: an unmodified GAP installation (tested with GAP 4.11.1 and
# GAP 4.16.0).  No package and no other file from this repository is used.
# Run from a terminal with:
#
#     gap -A -q --quitonbreak G3-verification.g
#
# All matrix entries below lie in GF(3); the entry 2 represents -1.

F := GF(3);;
SizeScreen([500,24]);;
Mat := function(rows)
    local matrix;
    matrix := List(rows,row -> List(row,entry -> entry * One(F)));
    ConvertToMatrixRep(matrix,F);
    MakeImmutable(matrix);
    return matrix;
end;;

# Four unitriangular generators I_5+E_13, I_5+E_23,
# I_5+E_34, and I_5+E_35.
x1 := Mat([
    [1,0,1,0,0],
    [0,1,0,0,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;
x2 := Mat([
    [1,0,0,0,0],
    [0,1,1,0,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;
y1 := Mat([
    [1,0,0,0,0],
    [0,1,0,0,0],
    [0,0,1,1,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;
y2 := Mat([
    [1,0,0,0,0],
    [0,1,0,0,0],
    [0,0,1,0,1],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;

# Four generators I_5+E_14, I_5+E_15, I_5+E_24, I_5+E_25
# for the central subgroup Z.
z14 := Mat([
    [1,0,0,1,0],
    [0,1,0,0,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;
z15 := Mat([
    [1,0,0,0,1],
    [0,1,0,0,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;
z24 := Mat([
    [1,0,0,0,0],
    [0,1,0,1,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;
z25 := Mat([
    [1,0,0,0,0],
    [0,1,0,0,1],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;

# A copy of D_8 on coordinates 1,2 and a second copy on coordinates 4,5.
# The diagonal entry 2 is -1 in GF(3).
aSwap := Mat([
    [0,1,0,0,0],
    [1,0,0,0,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;
aSign := Mat([
    [1,0,0,0,0],
    [0,2,0,0,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,1]
]);;
bSwap := Mat([
    [1,0,0,0,0],
    [0,1,0,0,0],
    [0,0,1,0,0],
    [0,0,0,0,1],
    [0,0,0,1,0]
]);;
bSign := Mat([
    [1,0,0,0,0],
    [0,1,0,0,0],
    [0,0,1,0,0],
    [0,0,0,1,0],
    [0,0,0,0,2]
]);;

xGenerators := [x1,x2];;
yGenerators := [y1,y2];;
zGenerators := [z14,z15,z24,z25];;
hGenerators := [aSwap,aSign,bSwap,bSign];;

# The explicit matrix groups used in the obstruction.
G3Matrix := Group(Concatenation(xGenerators,yGenerators,hGenerators));;
LMatrix  := Group(Concatenation(xGenerators,yGenerators));;
XMatrix  := Group(xGenerators);;
YMatrix  := Group(yGenerators);;
ZMatrix  := Group(zGenerators);;
HMatrix  := Group(hGenerators);;
MXMatrix := Group(Concatenation(zGenerators,xGenerators,hGenerators));;
MYMatrix := Group(Concatenation(zGenerators,yGenerators,hGenerators));;
NMatrix  := Group(Concatenation(zGenerators,hGenerators));;

# GAP's maximal-subgroup algorithms are substantially faster on a pc group.
# This is only a change of representation: every named subgroup is mapped by
# the same explicit isomorphism from G3Matrix.
iso := IsomorphismPcGroup(G3Matrix);;
G3 := Image(iso);;
LSub := Image(iso,LMatrix);;
XSub := Image(iso,XMatrix);;
YSub := Image(iso,YMatrix);;
ZSub := Image(iso,ZMatrix);;
HSub := Image(iso,HMatrix);;
MX := Image(iso,MXMatrix);;
MY := Image(iso,MYMatrix);;
NSub := Image(iso,NMatrix);;

Check := function(condition,message)
    if not condition then
        Print("FAIL ",message,"\n");
        QUIT_GAP(1);
    fi;
end;;

MaximalData := function(K)
    local representatives, indices;
    representatives := MaximalSubgroupClassReps(K);
    indices := List(representatives,M -> Index(K,M));
    return rec(
        representatives := representatives,
        indices := indices,
        spectrum := Set(indices)
    );
end;;

# Direct exhaustive search, written here rather than imported from the
# project's general-purpose chain-search code.  Reading a chain downward,
# successive indices must be nonincreasing, so `bound` is the largest index
# allowed at the current step.  One representative of each conjugacy class
# suffices because the existence of such a chain is invariant under
# conjugation.
HasIncreasingMaximalChain := function(K,bound)
    local row, j;
    if Size(K) = 1 then
        return true;
    fi;
    if Maximum(PrimeDivisors(Size(K))) > bound then
        return false;
    fi;
    for row in MaximalSubgroupClassReps(K) do
        j := Index(K,row);
        if j <= bound and HasIncreasingMaximalChain(row,j) then
            return true;
        fi;
    od;
    return false;
end;;

Print("GAP version: ",GAPInfo.Version,"\n");
Print("Construction: eight literal 5x5 generators over GF(3)\n");

# Structural checks on the concrete group.
Check(Size(G3) = 419904,"|G3| must equal 2^6*3^8 = 419904");
Check(Size(LSub) = 6561,"|L| must equal 3^8 = 6561");
Check(Size(XSub) = 9 and Size(YSub) = 9,"|X|=|Y|=3^2");
Check(Size(ZSub) = 81,"|Z| must equal 3^4 = 81");
Check(Size(HSub) = 64,"|H| must equal 2^6 = 64");
Check(Size(MX) = 46656 and Size(MY) = 46656,
      "|MX|=|MY|=2^6*3^6 = 46656");
Check(Size(NSub) = 5184,"|N| must equal 2^6*3^4 = 5184");
Check(IsSolvableGroup(G3),"G3 must be soluble");
Check(DerivedSubgroup(LSub) = ZSub,"L' must equal Z");
Check(FrattiniSubgroup(LSub) = ZSub,"Phi(L) must equal Z");
Check(IsElementaryAbelian(ZSub),"Z must be elementary abelian");
Check(IsNormal(G3,ZSub),"Z must be normal in G3");

# The five inclusions used in the proof, with no subgroup strictly between
# either endpoint.  Thus all five inclusions are maximal.
Check(Index(G3,MX) = 9 and Index(G3,MY) = 9,
      "MX and MY must have index 9 in G3");
Check(Index(MX,NSub) = 9 and Index(MY,NSub) = 9,
      "N must have index 9 in MX and MY");
Check(Index(NSub,HSub) = 81,"H must have index 81 in N");
Check(IsEmpty(IntermediateSubgroups(G3,MX).subgroups),"MX maximal in G3");
Check(IsEmpty(IntermediateSubgroups(G3,MY).subgroups),"MY maximal in G3");
Check(IsEmpty(IntermediateSubgroups(MX,NSub).subgroups),"N maximal in MX");
Check(IsEmpty(IntermediateSubgroups(MY,NSub).subgroups),"N maximal in MY");
Check(IsEmpty(IntermediateSubgroups(NSub,HSub).subgroups),"H maximal in N");

# Enumerate conjugacy classes of maximal subgroups and compute their indices.
gData  := MaximalData(G3);;
mxData := MaximalData(MX);;
myData := MaximalData(MY);;
nData  := MaximalData(NSub);;

Check(gData.spectrum = [2,9],"I(G3) must be {2,9}");
Check(mxData.spectrum = [2,9,81],"I(MX) must be {2,9,81}");
Check(myData.spectrum = [2,9,81],"I(MY) must be {2,9,81}");
Check(nData.spectrum = [2,81],"I(N) must be {2,81}");

# Check that the named subgroups cover every relevant maximal-subgroup class,
# not merely that their indices occur somewhere in each spectrum.
top9 := Filtered(gData.representatives,M -> Index(G3,M) = 9);;
mx9  := Filtered(mxData.representatives,M -> Index(MX,M) = 9);;
my9  := Filtered(myData.representatives,M -> Index(MY,M) = 9);;
n81  := Filtered(nData.representatives,M -> Index(NSub,M) = 81);;

Check(Length(top9) = 2,"G3 must have two classes of index-9 maximals");
Check(not IsConjugate(G3,MX,MY),"MX and MY must not be G3-conjugate");
Check(ForAll(top9,M -> IsConjugate(G3,M,MX) or
                       IsConjugate(G3,M,MY)),
      "MX and MY must cover all index-9 maximal classes of G3");
Check(Length(mx9) = 1 and ForAll(mx9,M -> IsConjugate(MX,M,NSub)),
      "N must cover the index-9 maximal class of MX");
Check(Length(my9) = 1 and ForAll(my9,M -> IsConjugate(MY,M,NSub)),
      "N must cover the index-9 maximal class of MY");
Check(Length(n81) = 1 and ForAll(n81,M -> IsConjugate(NSub,M,HSub)),
      "H must cover the index-81 maximal class of N");

Check(not HasIncreasingMaximalChain(G3,Size(G3)),
      "G3 must have no increasing unrefinable chain");

Print("PASS |G3|=",Size(G3)," = 2^6*3^8\n");
Print("PASS |MX|=|MY|=",Size(MX),"; |N|=",Size(NSub),"; |H|=",Size(HSub),"\n");
Print("PASS maximal-class index list for G3=",SortedList(gData.indices),"\n");
Print("PASS maximal-class index list for MX=",SortedList(mxData.indices),"\n");
Print("PASS maximal-class index list for MY=",SortedList(myData.indices),"\n");
Print("PASS maximal-class index list for N=",SortedList(nData.indices),"\n");
Print("PASS I(G3)=",gData.spectrum,"\n");
Print("PASS I(MX)=",mxData.spectrum,"\n");
Print("PASS I(MY)=",myData.spectrum,"\n");
Print("PASS I(N)=",nData.spectrum,"\n");
Print("PASS all relevant conjugacy classes are covered by MX, MY, N, and H\n");
Print("PASS increasing unrefinable chain exists: false\n");
Print("ALL CHECKS PASSED\n");

QUIT_GAP(0);
