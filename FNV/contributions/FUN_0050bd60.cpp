extern int DAT_01183028;
extern int DAT_01183140;
extern int DAT_01187818;
unsigned int __cdecl FUN_00487f50();
unsigned int __cdecl FUN_00ec43fb(unsigned int, int, void*, void*, int);
void* __cdecl FUN_0040ca30(unsigned int);

struct Entry {
    unsigned int form;
    unsigned short count;
    unsigned short level;
};
struct ListNode {
    Entry** FUN_006815c0();
    ListNode* FUN_00726070();
};
struct ListData {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual unsigned char ChanceNone();
    ListNode* FUN_00717e50();
    unsigned char FUN_004877e0();
};
struct FormHandle {
    unsigned int FUN_004065e0();
};
struct FieldLayout {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    FormHandle form0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2c;
    ListData list30;
};
struct LeveledSpellList : FUN_0050bf90_cls {
    void FUN_0050bd60(void*, unsigned short, unsigned int*, unsigned short*, unsigned char);
};
void LeveledSpellList::FUN_0050bd60(
    void* desiredForm, unsigned short level,
    unsigned int* outForm, unsigned short* outCount,
    unsigned char recurse)
{
    *outForm = 0;
    *outCount = 0;
    unsigned int candidateCount;
    int maxLevel;
    ListNode* best;
    ListNode* node;
    unsigned char chanceNone = ((FieldLayout*)this)->list30.ChanceNone();
    if (chanceNone > 0) {
        int chanceRoll = (int)(FUN_00487f50() % 100);
        if (chanceRoll < chanceNone)
            return;
    }

    candidateCount = 1;
    maxLevel = 0;
    best = 0;
    node = ((FieldLayout*)this)->list30.FUN_00717e50();
    while (node != 0 && *node->FUN_006815c0() != 0) {
        Entry* entryLevel = *node->FUN_006815c0();
        FUN_0050bf90_cls* mapped =
            (FUN_0050bf90_cls*)FUN_00ec43fb(entryLevel->form, 0,
                   &DAT_01183028, &DAT_01183140, 0);
        int entry = entryLevel->level;
        if (entry > level ||
            (mapped != 0 &&
             FUN_0040ca30(((FieldLayout*)mapped)->form0c.FUN_004065e0()) != desiredForm))
            break;
        if (entry > maxLevel &&
            (maxLevel == 0 || !((FieldLayout*)this)->list30.FUN_004877e0())) {
            candidateCount = 1;
            best = node;
            maxLevel = entry;
        } else {
            ++candidateCount;
        }
        node = node->FUN_00726070();
    }
    if (best != 0) {
        unsigned int skip = FUN_00487f50() % candidateCount;
        node = best;
        while (skip != 0) {
            node = node->FUN_00726070();
            --skip;
            if (node == 0)
                return;
        }
        unsigned short nestedRecord;
        Entry* chosen = *node->FUN_006815c0();
        unsigned int foundForm = chosen->form;
        nestedRecord = chosen->count;
        FUN_0050bf90_cls* selectedEntry =
            (FUN_0050bf90_cls*)FUN_00ec43fb(chosen->form, 0,
                  &DAT_01183028, &DAT_01187818, 0);
        if (selectedEntry != 0 && recurse != 0) {
            unsigned short recursiveCount;
            unsigned int recursiveForm = 0;
            recursiveCount = 0;
            selectedEntry->FUN_0050bd60(desiredForm, level,
                                &recursiveForm, &recursiveCount, recurse);
            foundForm = recursiveForm;
            nestedRecord *= recursiveCount;
        }
        *outForm = foundForm;
        *outCount = nestedRecord;
    }
}