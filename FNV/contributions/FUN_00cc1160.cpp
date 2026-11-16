struct Interface
{
    virtual void unk00(); virtual void unk04(); virtual void unk08(); virtual void unk0c();
    virtual void unk10(); virtual void unk14(); virtual void unk18(); virtual void unk1c();
    virtual void unk20(); virtual void unk24(); virtual void Invoke(void* value);
};
struct Holder
{
    int unk00; int unk04;
    Interface* interfaceObject;
};
struct Entry
{
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14;
    Holder* holder;
};
struct Root
{
    int unk00; int unk04; int unk08; int unk0c;
    signed char displacement;
    unsigned char unk11; unsigned char unk12; unsigned char unk13;
    int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30;
    int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48; int unk4c; int unk50;
    int unk54; int unk58; int unk5c; int unk60; int unk64; int unk68; int unk6c; int unk70;
    int unk74; int unk78; int unk7c; int unk80; int unk84; int unk88; int unk8c; int unk90;
    int unk94; int unk98; int unk9c; int unka0; int unka4; int unka8; int unkac; int unkb0;
    int unkb4; int unkb8; int unkbc; int unkc0; int unkc4; int unkc8;
};
struct Owner
{
    int unk00; int unk04; int unk08; int unk0c;
    Root* root;
};
void __cdecl FUN_00cc10b0(Owner* owner);
void __cdecl FUN_00cc1160(Owner* owner)
{
    Owner* self = owner;
    char* base = (char*)self->root;
    int offset = ((signed char*)base)[0x10];
    Entry* entry = *(Entry**)(base + offset + 0xcc);
    Holder* holder = entry->holder;
    Interface* receiver = holder->interfaceObject;
    receiver->Invoke(self);
    FUN_00cc10b0(self);
}



