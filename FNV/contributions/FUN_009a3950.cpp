void* __cdecl operator new(unsigned int count, void* place);
void __cdecl operator delete(void* ptr, void* place);
struct FUN_009a3d90 {
    int timestamp;
    int flags;
    FUN_009a3d90();
};
struct FUN_009a3950_Class {
    void FUN_009a3950(FUN_009a3d90* objects, unsigned int count);
};
void FUN_009a3950_Class::FUN_009a3950(FUN_009a3d90* objects, unsigned int count)
{
    for (unsigned int index = 0; index < count; ++index) {
        new (&objects[index]) FUN_009a3d90();
    }
}