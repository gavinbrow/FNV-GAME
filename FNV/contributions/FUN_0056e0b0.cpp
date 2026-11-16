struct TransformMember {
    void FUN_0056e270();
    void FUN_0056e120();
};
struct FUN_0056e0b0 : public FUN_0056e180 {
    unsigned int unk18;
    unsigned int unk1c;
    TransformMember transform;
    FUN_0056e0b0();
};
FUN_0056e0b0::FUN_0056e0b0() : FUN_0056e180() {
    transform.FUN_0056e270();
    transform.FUN_0056e120();
}