struct CopyRef {
    int m_00;
    CopyRef() {}
    CopyRef(const CopyRef& other) { FUN_00cb0bd0(&other); }
    void FUN_00cb0bd0(const CopyRef*);
    void FUN_00cb0c00();
    void FUN_00cb0c30(const CopyRef*);
};
struct CopyEntry {
    float m_00;
    CopyRef m_04;
    CopyEntry(const CopyEntry& other) { m_00 = other.m_00; m_04.FUN_00cb0bd0(&other.m_04); }
    CopyEntry& operator=(const CopyEntry& other) { m_00 = other.m_00; m_04.FUN_00cb0c30(&other.m_04); return *this; }
    ~CopyEntry() { m_04.FUN_00cb0c00(); }
};
inline void* operator new(unsigned int, void* p) { return p; }
struct CopyAllocator { int m_00, m_04, m_08, m_0c; void* m_10; };
CopyAllocator* __cdecl FUN_00c85750();
void __cdecl FUN_00c908c0(void*, void*, int, int);
static __forceinline void destroyEntries(CopyEntry* p, int count) {
    for (int i = 0; i < count; ++i) p[i].~CopyEntry();
}
static __forceinline void assignEntries(CopyEntry* dst, const CopyEntry* src, int count) {
    for (int i = 0; i < count; ++i) dst[i] = src[i];
}
static __forceinline void constructEntries(CopyEntry* dst, const CopyEntry* src, int count) {
    for (int i = 0; i < count; ++i) new(dst + i) CopyEntry(src[i]);
}
struct CopyArray {
    CopyEntry* m_00;
    int m_04;
    int m_08;
    __forceinline CopyArray(const CopyArray& src) : m_00(0), m_04(0), m_08(0x80000000) {
        CopyAllocator* manager = FUN_00c85750();
        int oldSize = m_04;
        int newSize = src.m_04;
        void* allocator = manager->m_10;
        int common = newSize > oldSize ? oldSize : newSize;
        int capacity = m_08 & 0x3fffffff;
        if (capacity < newSize) {
            int grown = capacity * 2;
            if (newSize >= grown) grown = newSize;
            FUN_00c908c0(allocator, this, grown, 8);
        }
        destroyEntries(m_00 + newSize, oldSize - newSize);
        assignEntries(m_00, src.m_00, common);
        constructEntries(m_00 + common, src.m_00 + common, newSize - common);
        m_04 = newSize;
    }
};
struct FUN_00e4e420 {
    CopyRef m_00;
    CopyArray m_04;
    FUN_00e4e420(const FUN_00e4e420&);
};
FUN_00e4e420::FUN_00e4e420(const FUN_00e4e420& src) : m_00(src.m_00), m_04(src.m_04) {}