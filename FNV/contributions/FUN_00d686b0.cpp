struct Allocator {
    virtual void* release();
    virtual void* allocate(int size);
};
struct Global { int unk00; int unk04; int unk08; int unk0c; Allocator* allocator; };
struct Built { int field00; short field04; int field08; int __thiscall FUN_00d682d0(int); };
extern "C" Global* __cdecl FUN_00c85750();
int __cdecl FUN_00d686b0(int arg)
{
    Global* global = FUN_00c85750();
    Built* object = (Built*)global->allocator->allocate(0x2c);
    object->field04 = 0x2c;
    int result = object->FUN_00d682d0(arg);
    if (result) return result + 8;
    return 0;
}
