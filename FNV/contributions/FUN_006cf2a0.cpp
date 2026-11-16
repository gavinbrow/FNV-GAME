struct FUN_005e0510 {
    void* m_vftable;
    unsigned int m_count;
    unsigned int m_capacity;
    unsigned int m_flags;
    FUN_005e0510();
    ~FUN_005e0510();
};

extern int DAT_0106c968;

struct HeapProvider {
    void* FUN_00aa42e0();
};

HeapProvider* __cdecl FUN_00401020();

struct FUN_006cf2a0 : FUN_005e0510 {
    void* m_heap;
    FUN_006cf2a0(int first, int second, void* heap);
    void FUN_006b3eb0(int first, int second);
};

FUN_006cf2a0::FUN_006cf2a0(int first, int second, void* heap)
{
    m_vftable = &DAT_0106c968;
    m_heap = heap ? heap : FUN_00401020()->FUN_00aa42e0();
    FUN_006b3eb0(first, second);
}
