struct AnimData { unsigned char FUN_00549580(); };
struct Resource {
    Resource* FUN_00586170();
    void FUN_006fcfa0();
    void FUN_00929260();
};
struct RefEx : VClass1d0 {
    void FUN_0056f700();
    AnimData* FUN_007af430();
};
struct CellStub {
    void FUN_0054af40(bool flag);
    void FUN_00541ac0();
    NodeStub* FUN_009604f0();
    Resource* FUN_0054ddd0();
    Resource* FUN_0054ddd0(RefEx* reference, bool flag);
    Resource* FUN_0054ddd0(bool flag);
    void FUN_00541ae0();
    void FUN_0054bc10();
};
void CellStub::FUN_0054bc10() {
    FUN_0054af40(false);
    FUN_00541ac0();
    NodeStub* cursor = FUN_009604f0();
    while (cursor != 0) {
        RefEx* reference = reinterpret_cast<RefEx*>(*cursor->_ref_006815c0());
        if (reference != 0) {
            reference->FUN_0056f700();
            if (reference->FUN_007af430()->FUN_00549580()) {
                if (reference->vfn_1d0()) {
                    if (FUN_0054ddd0() != 0) {
                        FUN_0054ddd0(reference, true)->FUN_00586170()->FUN_006fcfa0();
                        FUN_0054ddd0(true)->FUN_00586170()->FUN_00929260();
                    }
                }
            }
        }
        cursor = cursor->_ref_00726070();
    }
    FUN_00541ae0();
}