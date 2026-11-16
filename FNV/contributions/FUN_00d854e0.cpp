// FUN_00d854e0 @ 0x00d854e0, size 68, __cdecl (caller pops), /MT /O2 /GS /EHsc /Gy
//
// Reconstructed behavior:
//   A* a          = FUN_00c85750();              // cdecl, no args
//   C* obj        = a->unk10->Create(0x140);     // virtual slot +4, __thiscall
//   obj->unk04    = 0x140;                       // u16 field at +4
//   D* result     = obj->FUN_00cdf2f0();         // __thiscall, no stack args
//   FUN_00cb1260(&result->unk10, &src->unk10, 0x130);  // cdecl, 3 args
//   return result;

struct C_Stub;
struct D_Stub;

// polymorphic stand-in reached through A_Stub::unk10; Create sits in vtable slot +4
struct B_Stub {
    virtual void* virt0();
    virtual C_Stub* Create(int size);
};

struct A_Stub {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    B_Stub* unk10;
};

struct C_Stub {
    int unk00;
    unsigned short unk04;
    D_Stub* FUN_00cdf2f0();   // game function at 0x00cdf2f0 (__thiscall member)
};

struct D_Stub {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
};

// caller-supplied source structure; only the sub-object at +0x10 is touched
struct Src_Stub {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
};

A_Stub* __cdecl FUN_00c85750();
void __cdecl FUN_00cb1260(void* dst, const void* src, unsigned int size);

D_Stub* __cdecl FUN_00d854e0(Src_Stub* src)
{
    A_Stub* a = FUN_00c85750();
    C_Stub* obj = a->unk10->Create(0x140);
    obj->unk04 = 0x140;
    D_Stub* result = obj->FUN_00cdf2f0();
    FUN_00cb1260(&result->unk10, &src->unk10, 0x130);
    return result;
}
