struct CombatEntry {
    ~CombatEntry();
};

struct CombatEntryOwner {
    bool __thiscall FUN_00853130(int key, CombatEntry** result);
    void __thiscall FUN_00405430(int key);
    void __thiscall FUN_009a41e0(int key);
};

void CombatEntryOwner::FUN_009a41e0(int key) {
    CombatEntry* entry = 0;
    if (FUN_00853130(key, &entry)) {
        FUN_00405430(key);
        delete entry;
    }
}