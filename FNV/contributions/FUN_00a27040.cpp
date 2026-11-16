struct TempArrayElement
{
    void* a;
    void* b;
    void* c;
    void* d;
    ~TempArrayElement() {}
    static void* operator new[](unsigned int size)
    {
        return ((P03MM*)&g_memoryManager)->Allocate(size);
    }
    static void operator delete[](void* p, unsigned int)
    {
        g_memoryManager.Deallocate(p);
    }
};

TempArrayElement* __cdecl FUN_00a27040(unsigned int count)
{
    return new TempArrayElement[count];
}
