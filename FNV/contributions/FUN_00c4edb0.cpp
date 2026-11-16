// Candidate v2 for FUN_00c4edb0 (zai_04).
// Same guard logic; callee hypothesis: virtual __stdcall member taking one int,
// called as m_p->vfn(1). MSVC passes this as the first __stdcall stack argument
// (push 1 then push m_p), vtable slot 6 (+0x18), no ecx requirement at call.

extern unsigned char DAT_012030a4;

struct FUN_00c4edb0_Virt {
    virtual void vfn_0000();
    virtual void vfn_0004();
    virtual void vfn_0008();
    virtual void vfn_000c();
    virtual void vfn_0010();
    virtual void vfn_0014();
    virtual void __stdcall vfn_0018(int one);
};

struct FUN_00c4edb0_Class {
    FUN_00c4edb0_Virt* m_p;
    void FUN_00c4edb0();
};

void FUN_00c4edb0_Class::FUN_00c4edb0() {
    if (DAT_012030a4) {
        DAT_012030a4 = 0;
        m_p->vfn_0018(1);
    }
}
