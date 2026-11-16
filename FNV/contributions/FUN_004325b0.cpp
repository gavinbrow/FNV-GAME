struct FUN_0040ec80 {
    virtual void unk_vfn();
    int unk04;
    int unk08;
    FUN_0040ec80(int value);
};

void FUN_0040ec80::unk_vfn() {}
FUN_0040ec80::FUN_0040ec80(int value) {}

struct FUN_004325b0 : FUN_0040ec80 {
    unsigned char unk0c;
    FUN_004325b0(unsigned char param);
};

FUN_004325b0::FUN_004325b0(unsigned char param) : FUN_0040ec80(0x31)
{
    unk0c = param;
}
