extern "C" void* __cdecl FUN_0056d280(unsigned int size);

struct FUN_00626000
{
    unsigned int source;
    unsigned int flags;
    unsigned int counter;
    unsigned int state;
    FUN_00626000(int index);
    static __forceinline void* operator new(unsigned int size) { return FUN_0056d280(size); }
};

struct FUN_00624e90_Class
{
    FUN_00626000* FUN_00624e90(int index);
};

FUN_00626000* FUN_00624e90_Class::FUN_00624e90(int index)
{
    return new FUN_00626000(index);
}
