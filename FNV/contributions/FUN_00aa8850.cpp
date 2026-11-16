extern "C" __declspec(dllimport) int __stdcall CloseHandle(void* handle);

extern MemoryManager DAT_011f6238;
void* __stdcall FUN_00ec5fce(void* base, unsigned int size, unsigned int count, void (__cdecl* destructor)(void*));
void __cdecl FUN_0055a2d0(void* element);

struct VectorOwnedItem {
    void* vtable;
    void* handle;
    void* other;
    void* __thiscall FUN_00aa8850(unsigned int flags);
};

void* VectorOwnedItem::FUN_00aa8850(unsigned int flags)
{
    if (flags & 2) {
        FUN_00ec5fce(this, 12, ((unsigned int*)this)[-1], FUN_0055a2d0);
        if (flags & 1)
            DAT_011f6238.Deallocate((char*)this - 4);
        return (char*)this - 4;
    }
    CloseHandle(handle);
    if (flags & 1)
        DAT_011f6238.Deallocate(this);
    return this;
}
