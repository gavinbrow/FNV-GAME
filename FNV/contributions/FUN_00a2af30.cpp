// FNV candidate v2: FUN_00a2af30 (0x00a2af30, 61 bytes)
// return new BezierKeyS[count]; with sizeof(element)=76 (0x4c), non-trivial dtor -> 4-byte cookie,
// class-specific operator new[] inlining to ((P03MM*)&g_memoryManager)->Allocate(n).
// Packet TU already provides MemoryManager/Vec3S/P03MM/g_memoryManager/TCBKeyS(64B);
// element type must be 76 bytes, so it is a distinct type, not the packet's TCBKeyS.
struct BezierKeyS {
    float time;
    Vec3S pos;
    Vec3S in;
    Vec3S out;
    float extra[9];
    ~BezierKeyS() {}
    static void* operator new[](unsigned int n) { return ((P03MM*)&g_memoryManager)->Allocate(n); }
    static void operator delete[](void* p, unsigned int) { g_memoryManager.Deallocate(p); }
};

BezierKeyS* __cdecl FUN_00a2af30(unsigned int count) {
    return new BezierKeyS[count];
}
