struct RefEntry;
struct RefObject { int __thiscall FUN_007af430(); bool __thiscall FUN_00440d80(); };
struct RefWrapper { RefObject* reference; };
struct RefEntry { bool __thiscall FUN_008256d0(); RefWrapper* __thiscall FUN_006815c0(); RefEntry* __thiscall FUN_00726070(); };
struct CellRefScan { void __thiscall FUN_00541ac0(); RefEntry* __thiscall FUN_009604f0(); void __thiscall FUN_00541ae0(); RefObject* FUN_0054cf20(int typeId, bool filtered); };
RefObject* CellRefScan::FUN_0054cf20(int typeId, bool filtered) {
    if (!typeId) return 0;
    FUN_00541ac0();
    RefEntry* current = FUN_009604f0();
    int itemType;
    RefObject* reference;
    while (current && !current->FUN_008256d0()) {
        reference = current->FUN_006815c0()->reference;
        itemType = reference->FUN_007af430();
        current = current->FUN_00726070();
        if (itemType && (!filtered || !reference->FUN_00440d80()) && itemType == typeId) {
            FUN_00541ae0();
            return reference;
        }
    }
    FUN_00541ae0();
    return 0;
}