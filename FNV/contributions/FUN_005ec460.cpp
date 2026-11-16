struct FUN_005ec460_List { bool FUN_008256d0(); StandIn** FUN_006815c0(); void FUN_0063f7b0(); };
struct FUN_005ec460_Owner { FUN_005ec460_List* FUN_007d6bb0(); void FUN_005ec460(); };
void FUN_005ec460_Owner::FUN_005ec460() {
    FUN_005ec460_List* list = FUN_007d6bb0();
    while (list && !list->FUN_008256d0()) {
        StandIn* target = *list->FUN_006815c0();
        StandIn* deletionTarget = target;
        deletionTarget ? deletionTarget->FUN_005ec4d0(1) : 0;
        list->FUN_0063f7b0();
    }
}