extern int DAT_010cc984;

struct ContactData;
struct ContactCache
{
    unsigned int unk00;
    unsigned short mode04;
    unsigned short unk06;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1C;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2C;
    void FUN_00d92f20(ContactData* data, const unsigned char* first, const unsigned char* second);
};

struct ContactData
{
    unsigned int unk00;
    unsigned short mode04;
    unsigned short unk06;
    ContactCache* cache08;
    ContactCache* cache0C;
    unsigned int unk10;
    const unsigned char* first14;
    const unsigned char* second18;
    unsigned int unk1C;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2C;
    unsigned int unk30;
    unsigned int flags34;

    void FUN_00cf3f40(int enabled);
    void FUN_00cf3070(unsigned short index);
};

struct ContactManager
{
    int* vtable;
    unsigned short unk04;
    unsigned short state06;
    unsigned int unk08;
    const unsigned char* first0C;
    unsigned short unk10;
    unsigned short unk12;
    ContactCache cache;
    ContactData data;

    ContactManager* FUN_00cfd670(const unsigned char* first,
                                 const unsigned char* second,
                                 const unsigned char* third);
};

ContactManager* ContactManager::FUN_00cfd670(const unsigned char* first,
                                              const unsigned char* second,
                                              const unsigned char* third)
{
    state06 = 1;
    unk08 = 0;
    vtable = &DAT_010cc984;
    cache.FUN_00d92f20(&data, second, third);
    data.FUN_00cf3f40(1);

    data.first14 = second;
    data.cache0C = &cache;
    data.second18 = third;
    data.flags34 = 0xffffffff;
    first0C = first;
    unk12 = 0;
    unk10 = 0;
    cache.mode04 = 0;
    data.mode04 = 0;

    const unsigned char* table = *reinterpret_cast<const unsigned char* const*>(first + 0x80);
    int firstType = static_cast<signed char>(second[0x2a]);
    int secondType = static_cast<signed char>(third[0x2a]);
    int tableIndex = static_cast<signed char>(table[0x1bb0 + firstType * 10 + secondType]);
    unsigned short result = *reinterpret_cast<const unsigned short*>(table + 0x1c5c + tableIndex * 64);
    data.FUN_00cf3070(result);
    return this;
}