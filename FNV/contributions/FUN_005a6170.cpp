extern char* DAT_011dea3c;
extern double DAT_010290b0;
unsigned int __fastcall FUN_005a6260(char*);
extern "C" void* __fastcall FUN_006815c0(void*);
extern "C" unsigned int __fastcall FUN_0084e3a0(void*);
extern "C" void* __fastcall FUN_00504e60(void*);
extern "C" void* __fastcall FUN_00726070(void*);
struct Record { unsigned int formId; int threshold; };
struct EntryHolder { Record* record; };
struct SpellData { int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c,unk20,unk24,multiplier; };
bool __cdecl FUN_005a6170(int unused, void* subject, int unused2, double* result)
{
    void* target = subject;
    if (target != 0) {
        void* current = (void*)FUN_005a6260(DAT_011dea3c);
        while (current != 0 && ((EntryHolder*)FUN_006815c0(current))->record != 0) {
            if (((EntryHolder*)FUN_006815c0(current))->record->formId == FUN_0084e3a0(target)) {
                int limit;
                {
                    int multiplier = ((SpellData*)FUN_00504e60(target))->multiplier;
                    limit = ((EntryHolder*)FUN_006815c0(current))->record->threshold;
                    *result = 0.0;
                    for (int i = 0; i < 4; i++) {
                        if ((double)multiplier * ((double)(i + 1) * DAT_010290b0) <= (double)limit) {
                            *result = (double)(i + 1);
                        }
                    }
                }
            }
            current = FUN_00726070(current);
        }
    } else {
        return false;
    }
    return true;
}