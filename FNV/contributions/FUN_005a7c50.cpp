struct FUN_00483370 {
    virtual void DestructorEntry();
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    FUN_00483370();
    ~FUN_00483370();
};
struct FUN_00402d00 {
    virtual void DestructorEntry();
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    FUN_00402d00();
    ~FUN_00402d00();
};
struct FUN_00680890 {
    unsigned int first;
    unsigned int second;
    FUN_00680890();
    ~FUN_00680890();
};
struct FUN_0096a2d0 {
    unsigned int first;
    unsigned int second;
    FUN_0096a2d0();
    ~FUN_0096a2d0();
};
struct FUN_005a7c50 : FUN_00483370, FUN_00402d00 {
    FUN_00680890 member34;
    FUN_0096a2d0 member3c;
    FUN_0096a2d0 member44;
    FUN_0096a2d0 member4c;
    FUN_005a7c50();
    void FUN_004f15a0(unsigned int);
};
FUN_005a7c50::FUN_005a7c50()
{
    FUN_004f15a0(0x6a);
}