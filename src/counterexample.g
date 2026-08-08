# Explicit counterexample family for the monotone-maximal-chain problem.
#
# For an odd prime p, this builds a 5-dimensional matrix group over GF(p)
# modeled on the t=2 case of Kohler's construction.  The smallest family
# member, at p=3, has order 2^6 * 3^8 = 419904.

MMCBuildCounterexample := function(p)
    local field, one, identity5, matrix_generator, block_diagonal,
          swap, sign, identity2, xgens, ygens, zgens, hgens,
          lmat, hmat, zmat, mxmat, mymat, nmat, gmat, iso;

    if not IsPrimeInt(p) or p = 2 then
        Error("MMCBuildCounterexample requires an odd prime");
    fi;

    field := GF(p);
    one := One(field);
    identity5 := IdentityMat(5, field);

    matrix_generator := function(i, j)
        local a;
        a := MutableCopyMat(identity5);
        a[i][j] := a[i][j] + one;
        ConvertToMatrixRep(a, field);
        MakeImmutable(a);
        return a;
    end;

    block_diagonal := function(a, b)
        local result, i, j;
        result := MutableCopyMat(identity5);
        for i in [1..2] do
            for j in [1..2] do
                result[i][j] := a[i][j] * one;
            od;
        od;
        for i in [1..2] do
            for j in [1..2] do
                result[i+3][j+3] := b[i][j] * one;
            od;
        od;
        ConvertToMatrixRep(result, field);
        MakeImmutable(result);
        return result;
    end;

    # These two involutions generate D_8 in its absolutely irreducible
    # 2-dimensional representation over every field of odd characteristic.
    swap := ImmutableMatrix(field, [[0, 1], [1, 0]]);
    sign := ImmutableMatrix(field, [[1, 0], [0, -1]]);
    identity2 := IdentityMat(2, field);

    # Block sizes are 2,1,2.  X and Y are the two off-diagonal generating
    # spaces; their commutators generate the 2-by-2 central block Z.
    xgens := [matrix_generator(1, 3), matrix_generator(2, 3)];
    ygens := [matrix_generator(3, 4), matrix_generator(3, 5)];
    zgens := [matrix_generator(1, 4), matrix_generator(1, 5),
              matrix_generator(2, 4), matrix_generator(2, 5)];
    hgens := [block_diagonal(swap, identity2),
              block_diagonal(sign, identity2),
              block_diagonal(identity2, swap),
              block_diagonal(identity2, sign)];

    lmat := Group(Concatenation(xgens, ygens));
    hmat := Group(hgens);
    zmat := Group(zgens);
    mxmat := Group(Concatenation(zgens, xgens, hgens));
    mymat := Group(Concatenation(zgens, ygens, hgens));
    nmat := Group(Concatenation(zgens, hgens));
    gmat := Group(Concatenation(xgens, ygens, hgens));

    iso := IsomorphismPcGroup(gmat);
    return rec(
        prime := p,
        field := field,
        matrix_group := gmat,
        group := Image(iso),
        l_subgroup := Image(iso, lmat),
        h_subgroup := Image(iso, hmat),
        z_subgroup := Image(iso, zmat),
        mx_subgroup := Image(iso, mxmat),
        my_subgroup := Image(iso, mymat),
        n_subgroup := Image(iso, nmat),
        isomorphism_to_pc_group := iso
    );
end;
