extern "C" char DAT_010f1fa4;
extern "C" void __cdecl FUN_00ecd291(void*);
struct FUN_00ec79a1_Class
{
    void* vftable;
    void* allocation;
    unsigned int initialized;
    void FUN_00ec79a1();
};
// @fnv 0x00ec79a1
void FUN_00ec79a1_Class::FUN_00ec79a1()
{
    vftable = &DAT_010f1fa4;
    if (initialized != 0)
    {
        FUN_00ecd291(allocation);
    }
}