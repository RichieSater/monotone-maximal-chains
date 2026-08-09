Read("src/mmc.g");

Check := function(condition, message)
    if not condition then
        Print("FAIL ", message, "\n");
        QUIT_GAP(1);
    fi;
end;;

Check(MMCLast(TrivialGroup()) = 1, "trivial-group base case");
Check(MMCLast(CyclicGroup(2)) = 2, "cyclic group of order 2");
Check(MMCWitness(SmallGroup(24, 12)).indices = [2, 2, 2, 3],
      "expected S4 witness");
Check(MMCHasChain(AlternatingGroup(5)), "A5 should have a chain");

Print("smoke tests passed\n");
QUIT_GAP(0);
