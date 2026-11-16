struct hkMemoryAllocator {
    virtual void* unk00() = 0;
    virtual void* allocate(unsigned int size) = 0;
};

struct hkMemoryManager {
    virtual void* unk00() = 0;
    virtual void* unk04() = 0;
    virtual void* unk08() = 0;
    virtual void* unk0c() = 0;
    virtual void* unk10() = 0;
    virtual void* unk14() = 0;
    virtual void* unk18() = 0;
    virtual void* unk1c() = 0;
    virtual void* unk20() = 0;
    virtual void* allocate(unsigned int size) = 0;
};

struct FUN_00dd8700_cls : public hkMemoryAllocator {
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    hkMemoryManager* unk98;

    void* FUN_00dd8700(unsigned int size);
};

void* FUN_00dd8700_cls::FUN_00dd8700(unsigned int size)
{
    unsigned int allocationSize = (size + 0x1fu) & 0xfffffff0u;
    void* block = allocate(allocationSize);

    if (block != 0) {
        *static_cast<int*>(block) = 1;
        return static_cast<unsigned char*>(block) + 0x10;
    }

    block = unk98->allocate(allocationSize);

    if (block != 0) {
        *static_cast<int*>(block) = 0;
        return static_cast<unsigned char*>(block) + 0x10;
    }

    return 0;
}