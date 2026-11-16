struct Arr8 {
    float f;
    char c;
    ~Arr8() {}
    __forceinline static void* operator new[](unsigned int n) {
        return ((P03MM*)&g_memoryManager)->Allocate(n);
    }
    __forceinline static void operator delete[](void* p, unsigned int) {
        g_memoryManager.Deallocate(p);
    }
};

void* __cdecl FUN_00a2cc90(unsigned int count) {
    return new Arr8[count];
}
