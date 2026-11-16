#include <xmmintrin.h>
struct __declspec(align(16)) Vec4 { float x; float y; float z; float w; };
struct FUN_008cd6a0_Class {
    void FUN_00cb2d90(void* value);
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    __m128 unk30;
};
struct hkIArchive { void FUN_00dd8fe0(void* destination, int componentSize, int components); };
struct hkDisplaySerializeIStream : hkIArchive { void FUN_00ddac80(FUN_008cd6a0_Class* target); };
void hkDisplaySerializeIStream::FUN_00ddac80(FUN_008cd6a0_Class* target) {
    Vec4 source;
    Vec4 destination;
    FUN_00dd8fe0(&source, 4, 3);
    source.w = 1.0f;
    FUN_00dd8fe0(&destination, 4, 4);
    target->unk30 = *(__m128*)&source;
    target->FUN_00cb2d90(&destination);
}
