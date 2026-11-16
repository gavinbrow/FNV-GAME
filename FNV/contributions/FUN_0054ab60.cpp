
struct FUN_00440640 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    ~FUN_00440640();
};
struct FUN_0045cec0 {
    unsigned int value;
    ~FUN_0045cec0();
};
struct FUN_0054ab60 : FUN_00440640 {
    FUN_0045cec0 member1c;
    FUN_0045cec0 member20;
    ~FUN_0054ab60();
};
FUN_0054ab60::~FUN_0054ab60() {}
