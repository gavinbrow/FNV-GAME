inline void* __cdecl operator new(unsigned int, void* place) { return place; }
struct Vec4 {
    unsigned int x, y, z;
    float w;
    Vec4() : x(0), y(0), z(0), w(1.0f) {}
};
struct Allocator {
    void* __thiscall FUN_00aa3e40(unsigned int bytes);
};
extern "C" Allocator DAT_011f6238;
extern __declspec(thread) int g_threadMemoryMode;
struct ScopedMemoryMode {
    int previous;
    ScopedMemoryMode() : previous(g_threadMemoryMode) { g_threadMemoryMode = 16; }
    ~ScopedMemoryMode() { g_threadMemoryMode = previous; }
};
struct FUN_00cca2a0_class {
    void* m_vtable;
    void* m_object;
    void* m_parent;
    Vec4* m_vec;
    void __thiscall FUN_00cc9df0(Vec4* vec);
    Vec4* __thiscall FUN_00cca2a0(bool* created);
};
Vec4* FUN_00cca2a0_class::FUN_00cca2a0(bool* created) {
    ScopedMemoryMode memoryMode;
    *created = (m_vec == 0);
    if (*created) {
        Vec4* vec = new (DAT_011f6238.FUN_00aa3e40(sizeof(Vec4))) Vec4;
        m_vec = vec;
        if (m_parent)
            FUN_00cc9df0(vec);
    }
    return m_vec;
}