struct ScriptAddedEntries {
    unsigned char FUN_008256d0();
    BGSPerkEntry*& FUN_006815c0();
    void FUN_0063f7b0();
};
struct CurrentLeveledEntries {
    void FUN_00905330(BGSPerkEntry* const&);
};
struct FUN_00487980_shell : TESLeveledList {
    void FUN_00487980();
};

void FUN_00487980_shell::FUN_00487980()
{
    while (!reinterpret_cast<ScriptAddedEntries*>(ScriptAddedList)->FUN_008256d0()) {
        BGSPerkEntry* entryToDestroy = reinterpret_cast<ScriptAddedEntries*>(ScriptAddedList)->FUN_006815c0();
        reinterpret_cast<ScriptAddedEntries*>(ScriptAddedList)->FUN_0063f7b0();
        reinterpret_cast<CurrentLeveledEntries*>(leveledList)->FUN_00905330(entryToDestroy);

        BGSPerkEntry* item = entryToDestroy;
        BGSPerkEntry* removed = item;
        removed ? removed->FUN_00481760(1) : 0;
    }
}
