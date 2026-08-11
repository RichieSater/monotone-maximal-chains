# Core routines for monotone maximal chains (MMCs) in finite groups.
#
# An MMC is an unrefinable chain 1 = G_0 < ... < G_n = G whose
# upward indices are nondecreasing.  The key dynamic-programming invariant is
#
#   MMCLast(G) = the least possible last index |G:G_{n-1}| of an MMC in G,
#
# with value 0 if no MMC exists and MMCLast(1) = 1.  Then
#
#   MMCLast(G) = min { |G:M| : M maximal in G,
#                              MMCLast(M) <= |G:M| }.
#
# Conjugate maximal subgroups have the same value, so class representatives
# suffice.  The cache is indexed by IdGroup and is therefore intended for
# groups in the GAP Small Groups library range.

if not IsBound(MMC_CACHE) then
    MMC_CACHE := [];
fi;
if not IsBound(MMC_GREEDY_CACHE) then
    MMC_GREEDY_CACHE := [];
fi;

MMCResetCache := function()
    MMC_CACHE := [];
    MMC_GREEDY_CACHE := [];
end;

MMCGetCached := function(G)
    local id, n, k;
    if Size(G) = 1 then
        return 1;
    fi;
    id := IdGroup(G);
    n := id[1];
    k := id[2];
    if IsBound(MMC_CACHE[n]) and IsBound(MMC_CACHE[n][k]) then
        return MMC_CACHE[n][k];
    fi;
    return fail;
end;

MMCSetCached := function(G, value)
    local id, n, k;
    if Size(G) = 1 then
        return;
    fi;
    id := IdGroup(G);
    n := id[1];
    k := id[2];
    if not IsBound(MMC_CACHE[n]) then
        MMC_CACHE[n] := [];
    fi;
    MMC_CACHE[n][k] := value;
end;

MMCLast := function(G)
    local cached, best, M, t, j;
    if Size(G) = 1 then
        return 1;
    fi;
    cached := MMCGetCached(G);
    if cached <> fail then
        return cached;
    fi;
    best := 0;
    for M in MaximalSubgroupClassReps(G) do
        t := MMCLast(M);
        j := Index(G, M);
        if t > 0 and t <= j and (best = 0 or j < best) then
            best := j;
        fi;
    od;
    MMCSetCached(G, best);
    return best;
end;

MMCHasChain := G -> MMCLast(G) > 0;

# Stronger greedy variant: at every downward step choose a maximal subgroup
# of maximum index (equivalently, minimum order).  This is useful for testing
# the natural greedy conjecture; it is not assumed equivalent to MMC.
MMCGreedyLast := function(G)
    local id, n, k, maxes, d, M, sub;
    if Size(G) = 1 then
        return 1;
    fi;
    id := IdGroup(G);
    n := id[1];
    k := id[2];
    if IsBound(MMC_GREEDY_CACHE[n]) and
       IsBound(MMC_GREEDY_CACHE[n][k]) then
        return MMC_GREEDY_CACHE[n][k];
    fi;
    maxes := MaximalSubgroupClassReps(G);
    d := Maximum(List(maxes, M -> Index(G, M)));
    sub := 0;
    for M in maxes do
        if Index(G, M) = d and MMCGreedyLast(M) <= d and
           MMCGreedyLast(M) > 0 then
            sub := d;
            break;
        fi;
    od;
    if not IsBound(MMC_GREEDY_CACHE[n]) then
        MMC_GREEDY_CACHE[n] := [];
    fi;
    MMC_GREEDY_CACHE[n][k] := sub;
    return sub;
end;

MMCGreedyWitness := function(G)
    local maxes, d, M, sub;
    if Size(G) = 1 then
        return rec(groups := [G], indices := [], last := 1);
    fi;
    maxes := MaximalSubgroupClassReps(G);
    d := Maximum(List(maxes, M -> Index(G, M)));
    for M in maxes do
        if Index(G, M) = d then
            sub := MMCGreedyWitness(M);
            if sub <> fail and sub.last <= d then
                return rec(
                    groups := Concatenation(sub.groups, [G]),
                    indices := Concatenation(sub.indices, [d]),
                    last := d
                );
            fi;
        fi;
    od;
    return fail;
end;

# Return one explicit MMC as a record containing actual nested subgroups and
# its index sequence.  Return fail if none exists.  This deliberately does
# not use the IdGroup cache because the subgroup embeddings matter.
MMCWitness := function(G)
    local best, M, sub, j, candidate;
    if Size(G) = 1 then
        return rec(groups := [G], indices := [], last := 1);
    fi;
    best := fail;
    for M in MaximalSubgroupClassReps(G) do
        sub := MMCWitness(M);
        if sub <> fail then
            j := Index(G, M);
            if sub.last <= j and (best = fail or j < best.last) then
                candidate := rec(
                    groups := Concatenation(sub.groups, [G]),
                    indices := Concatenation(sub.indices, [j]),
                    last := j
                );
                best := candidate;
            fi;
        fi;
    od;
    return best;
end;

# A branch-and-bound witness search.  Read from the top down, a monotone
# chain has nonincreasing edge labels.  Thus `bound` is the largest permitted
# value of |G:M| at the current node.  Unlike MMCWitness, this routine rejects
# inadmissible top edges before recursing, which is essential for constructed
# groups outside the Small Groups library.
MMCThresholdWitness := function(G, bound)
    local primes, candidates, M, j, row, sub;
    if Size(G) = 1 then
        return rec(groups := [G], indices := [], last := 1);
    fi;
    primes := PrimeDivisors(Size(G));
    if Maximum(primes) > bound then
        return fail;
    fi;
    candidates := [];
    for M in MaximalSubgroupClassReps(G) do
        j := Index(G, M);
        if j <= bound then
            Add(candidates, rec(group := M, index := j));
        fi;
    od;
    # Try the least restrictive (largest) admissible edge first.
    Sort(candidates, function(a, b) return a.index > b.index; end);
    for row in candidates do
        sub := MMCThresholdWitness(row.group, row.index);
        if sub <> fail then
            return rec(
                groups := Concatenation(sub.groups, [G]),
                indices := Concatenation(sub.indices, [row.index]),
                last := row.index
            );
        fi;
    od;
    return fail;
end;

MMCConstructWitness := G -> MMCThresholdWitness(G, Size(G));

# Diagnostic table for all conjugacy classes of maximal subgroups.
MMCMaximalDiagnostics := function(G)
    local rows, M;
    rows := [];
    for M in MaximalSubgroupClassReps(G) do
        Add(rows, rec(
            subgroup_id := IdGroup(M),
            subgroup_order := Size(M),
            top_index := Index(G, M),
            subgroup_last := MMCLast(M),
            admissible := MMCLast(M) > 0 and MMCLast(M) <= Index(G, M)
        ));
    od;
    return rows;
end;
