
extern "C" void __cdecl FUN_00401030(void* data);
struct FnvMap {
    void* FUN_004b9ba0();
    void FUN_006b7f20(void*& cursor, unsigned int& id, void*& data);
    void FUN_00405430(unsigned int id);
};
struct FnvQueue {
    void FUN_00855010(TESObjectREFR* ref, unsigned int flag);
};
struct FnvRefMethod {
    int FUN_0043fcd0();
};
struct FnvState {
    FnvQueue* unk00;
    FnvQueue* unk04;
    int unk08, unk0c, unk10, unk14, unk18, unk1c, unk20, unk24;
    int unk28, unk2c, unk30, unk34, unk38, unk3c, unk40, unk44;
    int unk48, unk4c, unk50, unk54, unk58, unk5c, unk60;
    FnvMap* unk64;
};
void FUN_0085f5d0_class::FUN_0085f5d0() {
    void* cursor = reinterpret_cast<FnvState*>(this)->unk64->FUN_004b9ba0();
    while (cursor) {
        unsigned int key;
        void* data;
        reinterpret_cast<FnvState*>(this)->unk64->FUN_006b7f20(cursor, key, data);
        TESObjectREFR* refObject = dynamic_cast<TESObjectREFR*>(FUN_004839c0(key));
        if (refObject) {
            if (!reinterpret_cast<FnvRefMethod*>(refObject)->FUN_0043fcd0()) {
                if (reinterpret_cast<FnvState*>(this)->unk04)
                    reinterpret_cast<FnvState*>(this)->unk04->FUN_00855010(refObject, 0);
                else
                    reinterpret_cast<FnvState*>(this)->unk00->FUN_00855010(refObject, 0);
                reinterpret_cast<FnvState*>(this)->unk64->FUN_00405430(key);
                continue;
            }
            reinterpret_cast<FUN_0085f6c0_Class*>(this)->FUN_0085f6c0((int)refObject, (int)data);
        }
        FUN_00401030(data);
        reinterpret_cast<FnvState*>(this)->unk64->FUN_00405430(key);
    }
}
