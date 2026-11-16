void* __cdecl operator new(unsigned int size, void* location);
void __cdecl operator delete(void* object, void* location);
struct FUN_007da240 {
    int first;
    int second;
    int third;
    FUN_007da240();
};
struct CopyCollection {
    void FUN_007da1a0(FUN_007da240* records, unsigned count);
};
void CopyCollection::FUN_007da1a0(FUN_007da240* records, unsigned count)
{
    for (unsigned i = 0; i < count; ++i) {
        new (&records[i]) FUN_007da240();
    }
}