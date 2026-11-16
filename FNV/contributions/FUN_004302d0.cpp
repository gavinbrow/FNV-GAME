struct FUN_00430390 {
    ~FUN_00430390();
};
struct FUN_004385a0 {
    unsigned int FUN_0044ddc0();
    FUN_00430390*& FUN_006a7ad0(unsigned int index);
    ~FUN_004385a0();
};
struct FUN_0040ecb0 {
    virtual ~FUN_0040ecb0();
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
};
struct FUN_004302d0 : FUN_0040ecb0 {
    FUN_004385a0 members;
    virtual ~FUN_004302d0();
};
FUN_004302d0::~FUN_004302d0() {
    for (unsigned int index = 0; index < members.FUN_0044ddc0(); ++index) {
        delete members.FUN_006a7ad0(index);
    }
}