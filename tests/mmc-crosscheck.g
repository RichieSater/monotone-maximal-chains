Read("src/mmc.g");;
SizeScreen([200, 24]);;

Check := function(condition, message)
    if not condition then
        Error(message);
    fi;
end;;

# Exhaustively enumerate admissible index sequences without using MMCLast or
# either witness routine. Conjugacy-class representatives suffice because
# conjugate maximal subgroups have the same set of index sequences. The cache
# below is private to this separate implementation and keyed by IdGroup.
BRUTE_SEQUENCE_CACHE := [];;
BruteIndexSequences := function(g)
    local answer, m, j, sequence, id, order, number;
    if Size(g) = 1 then
        return [[]];
    fi;
    id := IdGroup(g);
    order := id[1];
    number := id[2];
    if IsBound(BRUTE_SEQUENCE_CACHE[order]) and
       IsBound(BRUTE_SEQUENCE_CACHE[order][number]) then
        return BRUTE_SEQUENCE_CACHE[order][number];
    fi;
    answer := [];
    for m in MaximalSubgroupClassReps(g) do
        j := Index(g, m);
        for sequence in BruteIndexSequences(m) do
            if Length(sequence) = 0 or Last(sequence) <= j then
                Add(answer, Concatenation(sequence, [j]));
            fi;
        od;
    od;
    answer := Set(answer);
    if not IsBound(BRUTE_SEQUENCE_CACHE[order]) then
        BRUTE_SEQUENCE_CACHE[order] := [];
    fi;
    BRUTE_SEQUENCE_CACHE[order][number] := answer;
    return answer;
end;;

ValidateWitness := function(g, witness)
    local i, lower, upper;
    if witness = fail or Length(witness.groups) <> Length(witness.indices) + 1 then
        return false;
    fi;
    if Size(witness.groups[1]) <> 1 or
       witness.groups[Length(witness.groups)] <> g then
        return false;
    fi;
    for i in [1..Length(witness.indices)] do
        lower := witness.groups[i];
        upper := witness.groups[i + 1];
        if not IsSubgroup(upper, lower) or lower = upper or
           Index(upper, lower) <> witness.indices[i] or
           Length(IntermediateSubgroups(upper, lower).subgroups) <> 0 then
            return false;
        fi;
        if i > 1 and witness.indices[i - 1] > witness.indices[i] then
            return false;
        fi;
    od;
    return true;
end;;

tested := 0;;
for order in [1..32] do
    for number in [1..NrSmallGroups(order)] do
        g := SmallGroup(order, number);;
        sequences := BruteIndexSequences(g);;
        expected := 0;;
        if Size(g) = 1 then
            expected := 1;
        elif Length(sequences) > 0 then
            expected := Minimum(List(sequences, Last));
        fi;
        actual := MMCLast(g);;
        Check(actual = expected,
              Concatenation("MMCLast disagrees with exhaustive enumeration for SmallGroup(",
                            String(order), ",", String(number), ")"));
        witness := MMCWitness(g);;
        Check((witness = fail) = (Length(sequences) = 0),
              Concatenation("witness existence mismatch for SmallGroup(",
                            String(order), ",", String(number), ")"));
        if witness <> fail then
            Check(ValidateWitness(g, witness),
                  Concatenation("invalid witness for SmallGroup(",
                                String(order), ",", String(number), ")"));
        fi;
        tested := tested + 1;
    od;
od;

Check(tested = 144, "unexpected number of SmallGroups of order at most 32");
Print("PASS mmc_crosscheck groups=", tested,
      " range=SmallGroups(order<=32) exhaustive_sequences=true witness_validation=true\n");
QUIT_GAP(0);
