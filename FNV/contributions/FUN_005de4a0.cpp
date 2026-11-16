
struct IdleForm {
    unsigned int FUN_00441110();
};
struct IdleAnimation {
    virtual void Unk00();
    virtual void Unk01();
    virtual void Unk02();
    virtual void Unk03();
    virtual void Unk04();
    virtual void Unk05();
    virtual void Unk06();
    virtual void Unk07();
    virtual void Unk08();
    virtual void Unk09();
    virtual void Unk10();
    virtual void Unk11();
    virtual void Unk12();
    virtual void Unk13();
    virtual void Unk14();
    virtual void Unk15();
    virtual void Unk16();
    virtual void Unk17();
    virtual void Unk18();
    virtual void Unk19();
    virtual void Unk20();
    virtual void Unk21();
    virtual void Unk22();
    virtual void Unk23();
    virtual void Unk24();
    virtual void Unk25();
    virtual void Unk26();
    virtual void Unk27();
    virtual void Unk28();
    virtual void Unk29();
    virtual void Unk30();
    virtual void Unk31();
    virtual void Unk32();
    virtual void Unk33();
    virtual void Unk34();
    virtual void Unk35();
    virtual void Unk36();
    virtual IdleForm* GetBase();
};
struct IdleNode {
    void* FUN_006815c0();
    IdleNode* FUN_00726070();
};
struct IdleManager {
    IdleNode* FUN_0043b5d0();
};
struct IdleHandle {
    void* object;
    IdleHandle(void*);
    ~IdleHandle();
    IdleAnimation* FUN_00559450();
};
extern IdleManager* DAT_011dea10;
extern const char DAT_0103d174[];
extern const char DAT_0103d158[];
extern void __cdecl FUN_00703c00(const char*);

bool __cdecl FUN_005de4a0(
    const SCRIPT_PARAMETER* params, const char* scriptData,
    TESObjectREFR* actor, TESObjectREFR* container, Script* script,
    ScriptLocals* locals, double& result, unsigned int& opcodeOffset)
{
    unsigned int formID = 0;
    float scale = 1.0f;
    result = 0.0;
    if (!ExtractArgs(params, scriptData, &opcodeOffset, actor, container,
                     script, locals, &formID, &scale))
        return false;

    IdleNode* node = DAT_011dea10->FUN_0043b5d0();
    while (node != 0) {
        IdleHandle handle(node->FUN_006815c0());
        if (handle.FUN_00559450()) {
            IdleAnimation* pAnimation = handle.FUN_00559450();
            IdleForm* pIdleForm = pAnimation->GetBase();
            if (pIdleForm && pIdleForm->FUN_00441110() == formID) {
                result = 1.0;
                break;
            }
        }
        node = node->FUN_00726070();
    }
    if (result != 0.0)
        FUN_00703c00(DAT_0103d174);
    else
        FUN_00703c00(DAT_0103d158);
    return true;
}
