
struct FNV_ParsedScript {
    void* script;
    int status;
};
struct FNV_QuestObject {
    int formID;
    int value;
};
struct FNV_ObjectRef {
    FNV_QuestObject* object;
};
struct FNV_ListNode {
    FNV_ObjectRef* FUN_006815c0();
    FNV_ListNode* FUN_00726070();
};
struct FNV_ListOwner {
    FNV_ListNode* FUN_005a6260();
};
struct FNV_ScriptResult {
    int FUN_0084e3a0();
    void* FUN_00504e60();
};
extern "C" FNV_ListOwner* DAT_011dea3c;
extern "C" double DAT_010290b0;
extern "C" void __cdecl FUN_005accb0(unsigned int, unsigned int, unsigned int,
                                      unsigned int, unsigned int, unsigned int,
                                      unsigned int, FNV_ParsedScript*);

bool __cdecl FUN_005dec30(unsigned int p1, unsigned int p2,
                          unsigned int p3, unsigned int p4,
                          unsigned int p5, unsigned int p6,
                          double* result, unsigned int p8)
{
    FNV_ParsedScript parsed;
    parsed.status = 0;
    FUN_005accb0(p1,p2,p8,p3,p4,p5,p6,&parsed);
    if (parsed.script != 0) {
        FNV_ListNode* node = DAT_011dea3c->FUN_005a6260();
        while (node != 0 && node->FUN_006815c0()->object != 0) {
            if (node->FUN_006815c0()->object->formID == static_cast<FNV_ScriptResult*>(parsed.script)->FUN_0084e3a0()) {
                int amount;
                int factor = *reinterpret_cast<int*>(reinterpret_cast<char*>(static_cast<FNV_ScriptResult*>(parsed.script)->FUN_00504e60()) + 0x28);
                amount = node->FUN_006815c0()->object->value;
                *result = 0.0;
                for (int i = 0; i < 4; ++i) {
                    if ((double)factor * ((double)(i + 1) * DAT_010290b0) <= (double)amount) {
                        *result = (double)(i + 1);
                    }
                }
            }
            node = node->FUN_00726070();
        }
    } else {
        return false;
    }
    return true;
}
