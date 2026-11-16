struct BGSSaveGameBuffer
{
    virtual void bufferMethod();
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    BGSSaveGameBuffer();
    ~BGSSaveGameBuffer();
};
struct BGSSaveLoadFormHeader
{
    unsigned char unk00;
    unsigned char unk01;
    unsigned char unk02;
    unsigned char unk03;
    unsigned char unk04;
    unsigned char unk05;
    unsigned char unk06;
    unsigned char unk07;
    unsigned char unk08;
    unsigned char unk09;
    unsigned char unk0a;
    unsigned char unk0b;
    BGSSaveLoadFormHeader();
};
struct FUN_008659c0 : BGSSaveGameBuffer
{
    BGSSaveLoadFormHeader header;
    int unk20;
    FUN_008659c0();
};
FUN_008659c0::FUN_008659c0() : BGSSaveGameBuffer(), header()
{
    unk20=0;
}
