Read("src/mmc.g");

Assert(0, MMCLast(TrivialGroup()) = 1);
Assert(0, MMCLast(CyclicGroup(2)) = 2);
Assert(0, MMCWitness(SmallGroup(24, 12)).indices = [2, 2, 2, 3]); # S4
Assert(0, MMCHasChain(AlternatingGroup(5)));

Print("smoke tests passed\n");
QUIT_GAP(0);
