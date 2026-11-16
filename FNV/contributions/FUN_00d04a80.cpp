struct Bucket {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    void FUN_00d056d0(int);
};
struct Registry {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14;
    int unk18; int unk1C; int unk20; int unk24; int unk28;
    Bucket buckets[1];
};
__declspec(align(16)) struct RequestContext {
    int unk00; int unk04; int unk08; int unk0C; int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28; int unk2C; int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int unk48; int unk4C; int unk50; int unk54; int unk58; int unk5C;
    int unk60; int unk64; int unk68; int unk6C; int unk70; int unk74; int unk78; int unk7C;
    int unk80; int unk84; int unk88; int unk8C; int unk90; int unk94; int unk98; int unk9C;
    int unkA0; int unkA4; int unkA8; int unkAC; int unkB0; int unkB4; int unkB8; int unkBC;
    int unkC0; int unkC4; int unkC8; int unkCC; int unkD0; int unkD4; int unkD8; int unkDC;
    int unkE0; int unkE4; int unkE8; int unkEC; int unkF0; int unkF4; int unkF8; int unkFC;
    int unk100; int unk104; int unk108; int unk10C; int unk110; int unk114; int unk118; int unk11C;
    int unk120; int unk124; int unk128; int unk12C; int unk130; int unk134; int unk138; int unk13C;
    int unk140; int unk144; int unk148; int unk14C; int unk150; int unk154; int unk158; int unk15C;
    int unk160; int unk164;
};
struct Owner {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28; int unk2C;
    int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int count;
    Registry* FUN_00d04400(RequestContext*);
    void FUN_00d04420(Registry*);
    void FUN_00d04a80(int, int);
};
void Owner::FUN_00d04a80(int first, int second)
{
    RequestContext context;
    Registry* data = FUN_00d04400(&context);
    ((Bucket*)((char*)data + 0x2c))[unk30 + first].FUN_00d056d0(second);
    for (int i = 0; i < count; ++i)
        ((Bucket*)((char*)data + 0x2c))[*((unsigned char*)this + 0x3d + i * 8)].FUN_00d056d0(second);
    FUN_00d04420(data);
}