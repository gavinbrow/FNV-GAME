struct DecalTextureObject
{
    ~DecalTextureObject();
    bool FUN_00c4edf0(unsigned int* value, int flags);
};

struct FUN_0068de30_holder
{
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    DecalTextureObject* unk1c;
    int unk20;
    unsigned int unk24;
    bool FUN_0068de30();
};

bool FUN_0068de30_holder::FUN_0068de30()
{
    if (!unk1c->FUN_00c4edf0(&unk24, 0)) {
        return false;
    } else {
        delete unk1c;
        unk1c = 0;
        return true;
    }
}