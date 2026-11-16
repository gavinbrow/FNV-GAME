struct BGSLoadFormBuffer {
    void FUN_00864980(void* destination, unsigned int size);
};
struct FUN_00996ef0_shell {
    void FUN_00996ef0(BGSLoadFormBuffer* stream);
};
struct FUN_009a5f20_shell {
    float x;
    float y;
    void FUN_009a5f20(BGSLoadFormBuffer* stream);
};
struct FUN_009d6c80_shell {
    FUN_009d6c80_shell* FUN_00586150();
};
struct FUN_0097fb60_shell {
    unsigned int FUN_0097fb60();
};
unsigned int __fastcall FUN_0097b050(void* object);
struct Float3 { float x; float y; float z; };
struct HideTargetLayout {
    void* unk00;
    FUN_009d6c80_shell* owner;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    FUN_009a5f20_shell unk18;
    Float3 unk20;
    Float3 unk2C;
    unsigned int state;
    unsigned char unk3C;
    unsigned char unk3D;
    void FUN_009d6900(BGSLoadFormBuffer* stream);
};
void HideTargetLayout::FUN_009d6900(BGSLoadFormBuffer* stream)
{
    ((FUN_00996ef0_shell*)this)->FUN_00996ef0(stream);
    stream->FUN_00864980(&unk10, 4);
    stream->FUN_00864980(&unk14, 4);
    unk18.FUN_009a5f20(stream);
    stream->FUN_00864980(&unk20, 12);
    stream->FUN_00864980(&unk2C, 12);
    stream->FUN_00864980(&unk3C, 1);
    stream->FUN_00864980(&unk3D, 1);
    unsigned char tag = 0;
    stream->FUN_00864980(&tag, 1);
    if (tag == 2) {
        state = ((FUN_0097fb60_shell*)owner->FUN_00586150())->FUN_0097fb60();
    } else if (tag == 1) {
        state = FUN_0097b050(owner->FUN_00586150());
    }
}
