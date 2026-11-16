extern int DAT_010cc4f4;

struct FUN_00d85490_Allocator {
    virtual void FUN_00d85490_Alloc0();
    virtual void* FUN_00d85490_Alloc1(unsigned int size);
};

struct FUN_00d85490_Manager {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00d85490_Allocator* unk10;
};

struct FUN_00d4fe80_Stub {
    int unk00;
    unsigned short unk04;
    unsigned int unk08;
    unsigned int unk0c;
    unsigned char unk10;
    void* FUN_00d4fe80();
};

extern void* __cdecl FUN_00c85750();
extern void __cdecl FUN_00cb1260(void* destination, const void* source, unsigned int size);

void* __cdecl FUN_00d85490(int* source)
{
    FUN_00d85490_Manager* manager =
        reinterpret_cast<FUN_00d85490_Manager*>(FUN_00c85750());
    FUN_00d4fe80_Stub* result =
        reinterpret_cast<FUN_00d4fe80_Stub*>(
            manager->unk10->FUN_00d85490_Alloc1(0xD0));

    result->unk04 = 0xD0;
    result = reinterpret_cast<FUN_00d4fe80_Stub*>(result->FUN_00d4fe80());

    FUN_00cb1260(
        reinterpret_cast<unsigned char*>(result) + 0x10,
        reinterpret_cast<const unsigned char*>(source) + 0x10,
        0xC0);

    return result;
}