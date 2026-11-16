// FUN_00c8b240 — walks the entry array of the list object held at this+0x08
// and forwards the parameter to each entry's handler-object virtual
// (vtable slot 21), then calls the member routine FUN_00aa0ad0 on this.
//
// Count source: vtable slot 1 of the sub-object embedded at list+0x10, with
// the owner chain (this, list) null-checked; the entry walk re-checks the
// chain on every iteration and skips null slots / null handler objects.
//
// Target: __thiscall (this in ecx), callee pops 4 bytes (1 stack parameter),
// size 109, /MT /O2 /GS /EHsc /Gy.

// Sub-object embedded at list+0x10; its vtable slot 1 returns the entry
// count as an unsigned value.
struct SubObj00 {
    virtual void v0();
    virtual unsigned int GetCount();   // vtable +0x04
};

// Handler object; vtable slot 21 (+0x54) is invoked with the parameter.
struct Handler00;

// Entry object referenced by a slot; field +0x08 points at the handler
// object that receives the per-entry virtual call.
struct Entry00;

// One 16-byte slot of the entry array at list+0x18; only the first dword
// (a pointer to the entry object) is read here.
struct Slot00 {
    Entry00* p0;     // +0x00
    int unk04;
    int unk08;
    int unk0C;
};

struct Entry00 {
    int unk00;
    int unk04;
    Handler00* unk08;   // +0x08
};

struct Handler00 {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void v7();
    virtual void v8();
    virtual void v9();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v20();
    virtual void Handle(void* param);   // vtable +0x54
};

// The list object held at this+0x08: embedded polymorphic sub-object at
// +0x10, spare dword at +0x14, entry array base at +0x18.
struct List00 {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    SubObj00 sub;    // +0x10
    int unk14;
    Slot00* arr;     // +0x18
};

// Owning class of the target member.
struct Owner00 {
    int unk00;
    int unk04;
    List00* unk08;   // +0x08

    void __thiscall FUN_00aa0ad0(void* param);   // defined elsewhere
    void FUN_00c8b240(void* param);
};

void Owner00::FUN_00c8b240(void* param)
{
    unsigned int count;
    if (this != 0) {
        List00* list = this->unk08;
        if (list != 0)
            count = list->sub.GetCount();
        else
            count = 0;
    }
    else
        count = 0;

    for (unsigned int i = 0; i < count; i++) {
        if (this != 0) {
            List00* list = this->unk08;
            if (list != 0) {
                Entry00* entry = list->arr[i].p0;
                if (entry != 0) {
                    Handler00* h = entry->unk08;
                    if (h != 0)
                        h->Handle(param);
                }
            }
        }
    }

    this->FUN_00aa0ad0(param);
}
