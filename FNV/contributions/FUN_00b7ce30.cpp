struct MM { void __thiscall Deallocate(void*); };
extern MM g_memoryManager;
class NiNode;
template<class T> struct NiPointer {
    T* ptr;
    ~NiPointer();
    static void __cdecl operator delete[](void* memory)
    {
        g_memoryManager.Deallocate(memory);
    }
};
void __cdecl FUN_00b7ce30(NiPointer<NiNode>* buffer)
{
    if (buffer)
        delete[] buffer;
}
