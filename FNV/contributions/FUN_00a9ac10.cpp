struct NiStream;

struct FUN_00a59e00_shell {
    void FUN_00a59e00(NiStream& stream);
};

struct FUN_0049da80_shell {
    int FUN_0049da80(void* ptr);
};

struct StreamData {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14;
    int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44;
    int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64;
    float unk68;
    int unk6c; int unk70;
    float unk74;
    int unk78; int unk7c;
    float unk80;
    int unk84; int unk88;
    float unk8c;
};

struct NiStream {
    int unk00; int unk04; int unk08;
    StreamData* unk0c;
};

struct PtrPair {
    FUN_00a59e00_shell* unk00;
    FUN_00a59e00_shell* unk04;
};

struct TriFloat {
    float f0;
    float f1;
    float f2;
};

struct FUN_00a9ac10_shell {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14;
    int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44;
    int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74;
    int unk78; int unk7c; int unk80; int unk84; int unk88; int unk8c;
    int unk90; int unk94; int unk98; int unk9c;
    PtrPair* unkA0;
    int unkA4; int unkA8; int unkAc; int unkB0; int unkB4; int unkB8;
    FUN_0049da80_shell unkBC;

    void FUN_00a9ac10(NiStream& stream);
};

void FUN_00a9ac10_shell::FUN_00a9ac10(NiStream& stream)
{
    StreamData* data = stream.unk0c;
    int r = unkBC.FUN_0049da80(&data->unk8c);
    if (r == 0) {
        TriFloat tmp;
        tmp.f0 = data->unk68;
        tmp.f1 = data->unk74;
        tmp.f2 = data->unk80;
        r = unkBC.FUN_0049da80(&tmp);
    }
    PtrPair* p = unkA0;
    FUN_00a59e00_shell* a = p->unk00;
    FUN_00a59e00_shell* b = p->unk04;
    if (r == 2) {
        if (b != 0) {
            b->FUN_00a59e00(stream);
        }
        if (a != 0) {
            a->FUN_00a59e00(stream);
        }
    } else {
        if (a != 0) {
            a->FUN_00a59e00(stream);
        }
        if (b != 0) {
            b->FUN_00a59e00(stream);
        }
    }
}
