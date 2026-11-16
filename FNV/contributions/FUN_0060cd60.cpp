
struct FNV_InitNode;
struct FNV_SubObject {
    void FUN_00483710();
    void FUN_005ec280();
};
struct FNV_NodeValue { FNV_SubObject* object; };
struct FNV_InitNode {
    bool FUN_008256d0();
    FNV_NodeValue* FUN_006815c0();
    FNV_InitNode* FUN_00726070();
};
struct FNV_InitPart {
    void FUN_0048cca0();
    void FUN_00487010();
    void FUN_0048e370(unsigned int);
    void FUN_0060ce80();
};
struct FUN_0060cd60_shell : TESQuest {
    void FUN_004855a0();
    void FUN_00485e20(void*, unsigned int);
    FNV_SubObject* FUN_005f5760();
    FNV_InitNode* FUN_005d43c0();
    FNV_InitNode* FUN_005d43e0();
    void FUN_00485680();
    void FUN_0060cd60();
};
struct FNV_EventObject { void FUN_00680910(); };
extern "C" bool __cdecl FUN_00401500();

void FUN_0060cd60_shell::FUN_0060cd60()
{
    FUN_004855a0();
    reinterpret_cast<FNV_InitPart*>(&tESScriptableFormComponent)->FUN_0048cca0();
    reinterpret_cast<FNV_InitPart*>(&tESIconComponent + 1)->FUN_00487010();
    reinterpret_cast<FNV_InitPart*>(&tESIconComponent)->FUN_0048e370(0x4e4f4349);
    if (FUN_00401500()) {
        reinterpret_cast<FNV_InitPart*>(&tESFullNameComponent + 1)->FUN_0060ce80();
    }
    FUN_00485e20(reinterpret_cast<char*>(&tESFullNameComponent) + 12, 8);
    if (FUN_00401500()) {
        reinterpret_cast<FNV_InitPart*>(&tESFullNameComponent + 1)->FUN_0060ce80();
    }
    if (FUN_005f5760() != 0) {
        reinterpret_cast<FNV_EventObject*>(FUN_005f5760())->FUN_00680910();
    }
    FNV_InitNode* node = FUN_005d43c0();
    while (node != 0 && !node->FUN_008256d0()) {
        node->FUN_006815c0()->object->FUN_00483710();
        node = node->FUN_00726070();
    }
    FNV_InitNode* other = FUN_005d43e0();
    while (other != 0 && !other->FUN_008256d0()) {
        other->FUN_006815c0()->object->FUN_005ec280();
        other = other->FUN_00726070();
    }
    FUN_00485680();
}
