
extern const char DAT_01030088;

struct FUN_00438170 {
    void* value;
    FUN_00438170(const char* value);
    ~FUN_00438170();
};

struct FNV_569BE0_Inner {
    virtual void vfn0();
    virtual void vfn1();
    virtual void vfn2();
    virtual void vfn3();
    virtual void vfn4();
    virtual void vfn5();
    virtual void vfn6();
    virtual void vfn7();
    virtual void vfn8();
    virtual void vfn9();
    virtual void vfn10();
    virtual void vfn11();
    virtual void vfn12();
    virtual void vfn13();
    virtual void vfn14();
    virtual void vfn15();
    virtual void vfn16();
    virtual void vfn17();
    virtual void vfn18();
    virtual void vfn19();
    virtual void vfn20();
    virtual void vfn21();
    virtual void vfn22();
    virtual void vfn23();
    virtual void vfn24();
    virtual void vfn25();
    virtual void vfn26();
    virtual void vfn27();
    virtual void vfn28();
    virtual void vfn29();
    virtual void vfn30();
    virtual void vfn31();
    virtual void vfn32();
    virtual void vfn33();
    virtual void vfn34();
    virtual void vfn35();
    virtual void vfn36();
    virtual void vfn37();
    virtual void vfn38();
    virtual int ProcessTemporary(const struct FUN_00438170& value);
    virtual void vfn40();
    virtual void vfn41();
    virtual void vfn42();
    virtual void vfn43();
    virtual void vfn44();
    virtual void vfn45();
    virtual void vfn46();
    virtual void vfn47();
    virtual void vfn48();
    virtual void vfn49();
    virtual void vfn50();
    virtual void vfn51();
    virtual void vfn52();
    virtual void vfn53();
    virtual void vfn54();
    virtual void vfn55();
    virtual void vfn56();
    virtual void vfn57();
    virtual void ConsumeResult(int result);
};

struct FNV_569BE0_Node {
    virtual void vfn0();
    virtual void vfn1();
    virtual void vfn2();
    virtual FNV_569BE0_Inner* GetInner();
};

struct FNV_569BE0_This : Unknown {
    void __thiscall FUN_00569be0(int ignored);
};

void FNV_569BE0_This::FUN_00569be0(int ignored)
{
    FNV_569BE0_Node* node = reinterpret_cast<FNV_569BE0_Node*>(GetNode());
    if (node) {
        FNV_569BE0_Inner* inner = node->GetInner();
        if (inner) {
            int value = inner->ProcessTemporary(FUN_00438170(&DAT_01030088));
            if (value) {
                inner->ConsumeResult(value);
                value = 0;
            }
        }
    }
}
