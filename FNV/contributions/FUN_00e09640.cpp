struct Allocator
{
    virtual void* unk00(void* p);
    virtual void* unk04(void* p);
    virtual void __thiscall blockFree(void* p, unsigned short size);
};
struct Router
{
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;
    Allocator* allocator;
};
extern "C" Router* __cdecl FUN_00c85750();
struct FUN_00e09640_class
{
    virtual void unknownVirtual();
    unsigned short unk04;
    void __thiscall FUN_00e09450();
    FUN_00e09640_class* __thiscall FUN_00e09640(int flags);
};
FUN_00e09640_class* __thiscall FUN_00e09640_class::FUN_00e09640(int flags)
{
    FUN_00e09450();
    if (flags & 1) {
        Router* router = FUN_00c85750();
        router->allocator->blockFree(this, unk04);
    }
    return this;
}
