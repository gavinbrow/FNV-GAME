void FUN_00d043c0(void*, int);

struct ReferenceData {
    unsigned short unk00;
    unsigned short unk02;
    unsigned short unk04;
    unsigned short unk06;
    unsigned short unk08;
    unsigned short unk0A;
    unsigned short unk0C;
    unsigned short unk0E;
    unsigned short unk10;
    unsigned short unk12;
    unsigned short unk14;
    unsigned short unk16;
    unsigned short unk18;
    unsigned short unk1A;
    unsigned short unk1C;
    unsigned short unk1E;
    unsigned short unk20;
    unsigned short counts[5];
};

struct ItemManager {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28; int unk2C;
    int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int unk48; int unk4C;
    int unk50; int unk54; int unk58; int unk5C;
    int unk60; int unk64; int unk68; int unk6C;
    int unk70; int unk74;
    void* values[5];
    int count;
    void FUN_00d048e0(ReferenceData* refs);
    void FUN_00d04990(int index, ReferenceData* refs);
};

void ItemManager::FUN_00d04990(int index, ReferenceData* refs)
{
    if (index < count)
    {
        unsigned short refCount = refs->counts[index];
        if (refCount > 0)
        {
            refs->counts[index] = refCount - 1;
            FUN_00d043c0(values[index], 1);
            return;
        }
    }
    FUN_00d048e0(refs);
}



