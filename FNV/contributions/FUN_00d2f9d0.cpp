struct Allocator {
    virtual void* release();
    virtual void* allocate(int size);
};
struct Global { int unk00; int unk04; int unk08; int unk0c; Allocator* allocator; };
struct Built { int field00; short field04; int field08; void __thiscall FUN_00d2f980(int); };
extern "C" Global* __cdecl FUN_00c85750();
void __cdecl FUN_00d2f9d0(int arg1, int arg2, int arg3, int arg4)
{
    Global* global = FUN_00c85750();
    Built* object = (Built*)global->allocator->allocate(0x40);
    object->field04 = 0x40;
    object->FUN_00d2f980(arg4);
}

