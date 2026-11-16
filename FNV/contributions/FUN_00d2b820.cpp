struct FUN_00da30a0_class {
    int unk00;
    unsigned short unk04;
    void FUN_00da30a0(int value);
};
struct FUN_00c85750_context {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    struct Allocator { virtual void first(); virtual FUN_00da30a0_class* allocate(unsigned int); } *unk10;
};
FUN_00c85750_context* __cdecl FUN_00c85750();
void __cdecl FUN_00d2b820() {
    FUN_00c85750_context* context = FUN_00c85750();
    FUN_00da30a0_class* value = context->unk10->allocate(0x24);
    value->unk04 = 0x24;
    value->FUN_00da30a0(-1);
}
