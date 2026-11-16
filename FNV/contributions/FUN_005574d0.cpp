class BGSPerkEntry;

class BGSLoadedReferenceCollection; // already defined by pack header

extern BGSLoadedReferenceCollection* DAT_011c95c8;

struct S_005270b0_Coll {
    void FUN_005270b0(BGSPerkEntry* entry);
};

struct S_00549580_Owner {
    bool FUN_00549580();
};

struct S_00586170_Result {
    void FUN_006fd010();
    void FUN_006fcfa0();
    void FUN_00929260();
};

struct S_00575d70_Owner {
    S_00586170_Result* FUN_00586170(BGSPerkEntry* entry);
    S_00586170_Result* FUN_00586170(BGSPerkEntry* entry, unsigned int flag);
    S_00586170_Result* FUN_00586170(unsigned int flag);
};

class BGSPerkEntry {
public:
    S_00549580_Owner* FUN_007af430();
    S_00575d70_Owner* FUN_00575d70();
    bool FUN_00440da0();
};

struct S_011dea10_Owner {
    int FUN_005f36f0();
    int FUN_004fd3e0();
};
extern S_011dea10_Owner* DAT_011dea10;

class S_005574d0_Owner {
public:
    void FUN_00541ac0();
    void FUN_00541ae0();
    BSSimpleList<BGSPerkEntry*>* FUN_009604f0();
    void FUN_005574d0();
};

void S_005574d0_Owner::FUN_005574d0() {
    FUN_00541ac0();
    BSSimpleList<BGSPerkEntry*>* list = FUN_009604f0();
    while (list != 0) {
        BGSPerkEntry* entry = list->GetItem();
        if (entry != 0) {
            ((S_005270b0_Coll*)DAT_011c95c8)->FUN_005270b0(entry);
            if (DAT_011dea10->FUN_005f36f0() == 0 && DAT_011dea10->FUN_004fd3e0() != 0 && entry->FUN_007af430()->FUN_00549580()) {
                S_00575d70_Owner* refs = entry->FUN_00575d70();
                if (refs != 0) {
                    if (!entry->FUN_00440da0()) {
                        refs->FUN_00586170(entry)->FUN_006fd010();
                    } else {
                        refs->FUN_00586170(entry, 1)->FUN_006fcfa0();
                    }
                    refs->FUN_00586170(1)->FUN_00929260();
                }
            }
        }
        list = list->GetNext();
    }
    FUN_00541ae0();
}
