Read("src/mmc.g");

if not IsBound(START_ORDER) then START_ORDER := 1; fi;
if not IsBound(STOP_ORDER) then STOP_ORDER := 500; fi;
if not IsBound(STOP_AT_FIRST) then STOP_AT_FIRST := true; fi;
if not IsBound(SKIP_PRIME_POWERS) then SKIP_PRIME_POWERS := false; fi;
if not IsBound(ONLY_NONSUPERSOLVABLE) then
    ONLY_NONSUPERSOLVABLE := false;
fi;

Print("# Exhaustive SmallGroups MMC search: orders ", START_ORDER,
      " through ", STOP_ORDER, "\n");
Print("# GAP ", GAPInfo.Version, "\n");

tested := 0;
inspected := 0;
bad := [];
for n in [START_ORDER..STOP_ORDER] do
    if not (SKIP_PRIME_POWERS and IsPrimePowerInt(n)) then
        count := NrSmallGroups(n);
        for k in [1..count] do
            inspected := inspected + 1;
            G := SmallGroup(n, k);
            if not ONLY_NONSUPERSOLVABLE or not IsSupersolvableGroup(G) then
                value := MMCLast(G);
                tested := tested + 1;
                if value = 0 then
                    Add(bad, [n, k]);
                    Print("COUNTEREXAMPLE SmallGroup(", n, ",", k, ") ",
                          StructureDescription(G), "\n");
                    Print("DIAGNOSTICS ", MMCMaximalDiagnostics(G), "\n");
                    if STOP_AT_FIRST then
                        Print("INSPECTED ", inspected, " TESTED ", tested,
                              "\n");
                        QUIT_GAP(1);
                    fi;
                fi;
            fi;
        od;
    fi;
    if n mod 25 = 0 then
        Print("PROGRESS order=", n, " inspected=", inspected,
              " tested=", tested,
              " bad=", Length(bad), "\n");
    fi;
od;

Print("DONE inspected=", inspected, " tested=", tested,
      " bad=", Length(bad), " list=", bad, "\n");
QUIT_GAP(0);
