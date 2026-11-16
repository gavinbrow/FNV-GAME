struct VirtualFloat {
    virtual void Slot0();
    virtual void Slot1();
    virtual void Slot2();
    virtual float Slot3(float, int);
};
struct FloatOwner {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14;
    VirtualFloat* unk18;
    float __thiscall FUN_00dfb6d0(float value, int mode);
};
float __thiscall FloatOwner::FUN_00dfb6d0(float value, int mode) {
    return unk18->Slot3(value, mode);
}
