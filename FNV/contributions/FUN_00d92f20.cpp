
extern unsigned char DAT_010cc934;

struct PacketResult {
    unsigned short unk00;
    unsigned short unk02;
    unsigned short unk04;
    unsigned short unk06;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned short state10;
    volatile unsigned short version12;
    void* volatile ptr14;
    void* volatile ptr18;
    void* ptr1c;
    void* ptr20;
    void* ptr24;
    void* ptr28;
    void* ptr2c;
};

struct FUN_00d92f20 {
    void* vtable;
    unsigned short unk04;
    unsigned short active06;
    unsigned int field08;
    void* field0c;
    unsigned int field10;
    unsigned int field14;
    unsigned int field18;
    unsigned int field1c;
    unsigned int field20;
    void* volatile context24;
    S_00d92690* buffer28;
    unsigned int size2c;

    FUN_00d92f20(void* atom, const unsigned char* first, const unsigned char* second);
};

FUN_00d92f20::FUN_00d92f20(void* atom, const unsigned char* first, const unsigned char* second)
{
    vtable = &DAT_010cc934;
    active06 = 1;
    field08 = 0;
    field0c = &field18;
    field10 = 0;
    field14 = 0x80000008;
    context24 = atom;

    unsigned int lenA = first[0xd1];
    unsigned int lenB = second[0xd1];
    unsigned int bytesPerEntry = (lenA + lenB) * 4 + 0x34;
    buffer28 = FUN_00d92510(1, lenA, lenB, (unsigned short)(0x3400 / (int)bytesPerEntry));

    PacketResult* result = reinterpret_cast<PacketResult*>(buffer28);
    result->state10 = 0;
    result->version12 = 3;
    result->ptr14 = 0;
    result->ptr18 = 0;
    result->ptr1c = 0;
    result->ptr20 = 0;
    result->ptr24 = 0;
    result->ptr28 = 0;
    result->ptr2c = 0;

    size2c = buffer28->unk2;
}
