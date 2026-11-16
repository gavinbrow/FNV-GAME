#include <xmmintrin.h>
struct SourceData { float x; float y; float z; unsigned int unk0C; __m128 unk10; unsigned int unk20; unsigned char unk24; };
struct Destination {
    unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0C;
    unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1C;
    unsigned int unk20; unsigned int unk24; unsigned int unk28; unsigned int unk2C;
    unsigned int unk30; unsigned int unk34; unsigned int unk38; unsigned int unk3C;
    float unk40; float unk44; float unk48; __m128 unk50;
    unsigned int unk60; unsigned char unk64;
    void FUN_00dd4c70(unsigned int srcAddress);
};
void Destination::FUN_00dd4c70(unsigned int srcAddress) {
    const SourceData* src = (const SourceData*)srcAddress;
    unk40 = src->x;
    unk44 = src->y;
    unk48 = src->z;
    unk50 = src->unk10;
    unk60 = src->unk20;
    unk64 = src->unk24;
}
