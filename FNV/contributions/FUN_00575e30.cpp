class FUN_00575e30_cls;
class BSExtraData {
public:
    virtual ~BSExtraData();
};
class NonActorMagicCaster : public BSExtraData {};
class FUN_00575e30_thing {
public:
    int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c, unk20;
    FUN_00575e30_thing(FUN_00575e30_cls* owner);
};
class FUN_00575e30_mid {
public:
    BSExtraData* FUN_00410220();
    void FUN_0040ff60();
};
class FUN_00575e30_cls {
public:
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0c();
    virtual void v10(); virtual void v14(); virtual void v18(); virtual void v1c();
    virtual void v20(); virtual void v24(); virtual void v28(); virtual void v2c();
    virtual void v30(); virtual void v34(); virtual void v38(); virtual void v3c();
    virtual void v40(); virtual void v44(); virtual void v48(unsigned int);
    FUN_00575e30_mid* FUN_005d43c0(unsigned int a);
    FUN_00575e30_mid* FUN_005d43c0(void* a);
    void* FUN_00575e30();
};
void* FUN_00575e30_cls::FUN_00575e30() {
    void* z = 0;
    z = dynamic_cast<NonActorMagicCaster*>(FUN_005d43c0(0x32u)->FUN_00410220());
    if (z == 0) {
        z = new FUN_00575e30_thing(this);
        FUN_005d43c0(z)->FUN_0040ff60();
        v48(0x80000000);
    }
    return z != 0 ? (char*)z + 0xc : 0;
}