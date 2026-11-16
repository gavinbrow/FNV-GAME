struct FUN_00c42b60_class;
struct SpawnHeap_cls { void __thiscall FUN_00aa4060(void* pObject); };
extern "C" char DAT_011f6238;
typedef void (__stdcall *S_00c422d0_IAT_Fn)(void*);
extern "C" S_00c422d0_IAT_Fn DAT_0fdf050;
struct S_00c422d0_Entry { unsigned int unk00; FUN_00c42b60_class* m_pObject; };
struct S_00c422d0_Foo {
    unsigned int m_count;
    unsigned int m_unk04;
    S_00c422d0_Entry* m_pEntries;
    void __thiscall FUN_00c422d0();
};
void __thiscall S_00c422d0_Foo::FUN_00c422d0()
{
    unsigned int V_t;
    unsigned int V_h;
    FUN_00c42b60_class* pItem;
    FUN_00c42b60_class* pBase;
    FUN_00c42b60_class* V_k;
    S_00c422d0_Entry* pObject;
    unsigned int V_n;
    for (V_t = 0; V_t < (V_h = m_count); V_t++) {
        pItem = m_pEntries[V_t].m_pObject;
        pBase = pItem;
        pBase != 0 ? (V_k = pBase, V_k->FUN_00c42b60(), ((0,1)&1) ? reinterpret_cast<SpawnHeap_cls*>(&DAT_011f6238)->FUN_00aa4060(V_k) : (void)0, V_k) : 0;
    }
    pObject = (S_00c422d0_Entry*)m_pEntries;
    reinterpret_cast<SpawnHeap_cls*>(&DAT_011f6238)->FUN_00aa4060(pObject);
    V_n = m_unk04;
    DAT_0fdf050((void*)V_n);
}