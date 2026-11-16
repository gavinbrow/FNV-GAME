struct FUN_00ca9aa0;
struct State {
    unsigned int value;
    State() : value(0) {}
};
struct BaseOwner {
    virtual void Act();
    unsigned short unk04;
    unsigned short unk06;
    State unk08;
    BaseOwner() : unk06(1), unk08() {}
};
struct InternalPart {
    unsigned short mode;
    unsigned short unk12;
    unsigned int unk14;
    unsigned int unk18;
    InternalPart() : mode(1) {}
    ~InternalPart();
};
void __fastcall FUN_00d21ce0(InternalPart* part, unsigned int command, FUN_00ca9aa0* parent);
struct FUN_00ca9aa0 : BaseOwner {
    virtual void Act();
    unsigned int unk0c;
    InternalPart part;
    float value;
    FUN_00ca9aa0();
};
FUN_00ca9aa0::FUN_00ca9aa0() : BaseOwner(), part() {
    unk0c = 0;
    FUN_00d21ce0(&part, 1, this);
    value = 0.01f;
}