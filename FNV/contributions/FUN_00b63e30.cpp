extern char DAT_010adfbc;
void __cdecl FUN_00aa10f0(void* value);
struct Resource {
    void* vtable;
    int unk04;
    void* unk08;
    void __thiscall FUN_00b601a0();
    Resource* __thiscall FUN_00b63e30(unsigned int flags);
};
Resource* Resource::FUN_00b63e30(unsigned int flags) {
    vtable = &DAT_010adfbc;
    FUN_00b601a0();
    FUN_00aa10f0(unk08);
    if (flags & 1) {
        g_memoryManager.Deallocate(this);
    }
    return this;
}