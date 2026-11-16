void* __cdecl FUN_006e6da0(unsigned int bytes, void* heap);
struct S006d1520_Container { unsigned int FUN_006cef10(); void* FUN_006e8f40(unsigned int value); };
struct S006d1520_LocationOps { void FUN_006dd6f0(int zero); };
struct FUN_006f4d00 {
    unsigned int m00,m04,m08,m0c,m10,m14,m18,m1c,m20,m24,m28,m2c;
    FUN_006f4d00(const PathingLocation& location);
    static __forceinline void* operator new(unsigned int bytes, void* heap) { return FUN_006e6da0(bytes, heap); }
    static void operator delete(void* pointer, void* heap);
};
struct FUN_006d1520_shell {
    unsigned int unk00; unsigned int unk04; S006d1520_Container m_container;
    unsigned int FUN_006d1520(const NiPoint3& pos, TESObjectCELL* cell, TESWorldSpace* world);
};
unsigned int FUN_006d1520_shell::FUN_006d1520(const NiPoint3& pos, TESObjectCELL* cell, TESWorldSpace* world) {
    void* heap;
    unsigned int index;
    {
        PathingLocation location(pos, cell, world);
        reinterpret_cast<S006d1520_LocationOps*>(&location)->FUN_006dd6f0(0);
        index = m_container.FUN_006cef10();
        heap = m_container.FUN_006e8f40(index);
        new(heap) FUN_006f4d00(location);
        return index;
    }
}