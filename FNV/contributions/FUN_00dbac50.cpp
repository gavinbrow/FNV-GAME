struct Fnv299VTarget {
    virtual void unk00(); virtual void unk04(); virtual void unk08(); virtual void unk0C();
    virtual void unk10(); virtual void unk14(); virtual void unk18(); virtual void unk1C(); virtual void unk20(int arg);
};
struct FUN_00dbac50_cls { Fnv299VTarget* m_00; int m_04; void __thiscall FUN_00dbac50(int a1); };
typedef void (__thiscall *Fnv299Dispatch)(Fnv299VTarget*, int);
void FUN_00dbac50_cls::FUN_00dbac50(int a1) {
    Fnv299VTarget* t = m_00;
    void* volatile* table = *(void* volatile**)t;
    *(volatile int*)&a1 = m_04;
    Fnv299Dispatch fn = (Fnv299Dispatch)table[8];
    fn(t, a1);
}