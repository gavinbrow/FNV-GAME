extern void __cdecl FUN_004858f0(unsigned int, unsigned int);
extern void __cdecl FUN_00485910(unsigned int, unsigned int);
extern void __cdecl FUN_00485990(unsigned int, const void*, unsigned int);
extern unsigned char __cdecl FUN_00401500();

struct LevelNode_00488400 {
    LEVELED_OBJECT** FUN_006815c0();
    LevelNode_00488400* FUN_00726070();
};

struct ExtraSaver_00488400 : ContainerItemExtra {
    void FUN_0040e6c0();
};

struct FUN_00488400_shell : TESLeveledList {
    LevelNode_00488400* FUN_00717e50();
    void FUN_00488400();
};

void FUN_00488400_shell::FUN_00488400()
{
    FUN_004858f0(0x444c564c, cChanceNone);
    FUN_004858f0(0x464c564c, cLLFlags);
    if (pChanceGlobal) {
        unsigned int chanceFormID = pChanceGlobal->GetFormID();
        FUN_00485910(0x474c564c, chanceFormID);
    }
    LevelNode_00488400* pNode = FUN_00717e50();
    LEVELED_OBJECT* entry;
    while (pNode && (entry = *pNode->FUN_006815c0()) != 0) {
        TmpEndian levelData;
        levelData.f1 = entry->pForm->GetFormID();
        levelData.f0 = entry->sLevel;
        levelData.f2 = entry->sCount;
        if (FUN_00401500())
            levelData.FUN_00488510();
        FUN_00485990(0x4f4c564c, &levelData, 12);
        if (FUN_00401500())
            levelData.FUN_00488510();
        if (entry->pItemExtra)
            static_cast<ExtraSaver_00488400*>(entry->pItemExtra)->FUN_0040e6c0();
        pNode = pNode->FUN_00726070();
    }
}