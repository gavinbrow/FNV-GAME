class PlayerCharacter;
extern PlayerCharacter* pPlayer;

struct Reference_005d8e20 {
    virtual void V0();
    virtual void V1();
    virtual void V2();
    virtual void V3();
    virtual void V4();
    virtual void V5();
    virtual void V6();
    virtual void V7();
    virtual void V8();
    virtual void V9();
    virtual void V10();
    virtual void V11();
    virtual void V12();
    virtual void V13();
    virtual void V14();
    virtual void V15();
    virtual void V16();
    virtual void V17();
    virtual void V18();
    virtual void V19();
    virtual void V20();
    virtual void V21();
    virtual void V22();
    virtual void V23();
    virtual void V24();
    virtual void V25();
    virtual void V26();
    virtual void V27();
    virtual void V28();
    virtual void V29();
    virtual void V30();
    virtual void V31();
    virtual void V32();
    virtual void V33();
    virtual void V34();
    virtual void V35();
    virtual void V36();
    virtual void V37();
    virtual void V38();
    virtual void V39();
    virtual void V40();
    virtual void V41();
    virtual void V42();
    virtual void V43();
    virtual void V44();
    virtual void V45();
    virtual void V46();
    virtual void V47();
    virtual void V48();
    virtual void V49(bool removeFromWorld);
    bool FUN_00440d80();
    int FUN_00484e60(int);
};

struct ReferenceRemovalManager {
    void FUN_005ae3d0(Reference_005d8e20**);
};
extern ReferenceRemovalManager DAT_011cacb8;

bool __cdecl FUN_005d8e20(void* unused1, void* unused2, Reference_005d8e20* reference) {
    if (reference && !reference->FUN_00440d80() &&
        static_cast<void*>(reference) != static_cast<void*>(pPlayer)) {
        reference->V49(true);
        if (!reference->FUN_00484e60(0)) {
            DAT_011cacb8.FUN_005ae3d0(&reference);
        }
    }
    return true;
}
