struct NiStream;
struct FirstInterface {
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C();
    virtual void* FUN_00ca4f40_get();
};
struct SecondInterface {
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C();
    virtual void v10(); virtual void v14(); virtual void v18(); virtual void v1C();
    virtual void v20(); virtual void v24(); virtual void v28(); virtual void v2C();
    virtual void v30(); virtual void v34(); virtual void v38(); virtual void v3C();
    virtual void v40(); virtual void v44(); virtual void v48(); virtual void v4C();
    virtual void v50(); virtual void FUN_00ca4f40_stream(NiStream* stream);
};
struct ReturnedObject { int unk00; int unk04; SecondInterface* unk08; };
struct HC1Base {
    int unk00; int unk04; FirstInterface* unk08; int unk0C; int unk10; int unk14; int unk18;
    bool __thiscall FUN_00aa0ad0(NiStream* stream);
    void __thiscall FUN_00ca4f40(NiStream* stream);
};
void HC1Base::FUN_00ca4f40(NiStream* stream) {
    if (this) {
        FirstInterface* first = unk08;
        if (first) {
            void* result = first->FUN_00ca4f40_get();
            if (result) {
                ReturnedObject* object = (ReturnedObject*)((char*)result - 0x10);
                if (object) {
                    SecondInterface* second = object->unk08;
                    if (second)
                        second->FUN_00ca4f40_stream(stream);
                }
            }
        }
    }
    FUN_00aa0ad0(stream);
}
