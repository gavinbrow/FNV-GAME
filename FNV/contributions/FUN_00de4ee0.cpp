#include <xmmintrin.h>
struct MatrixOwner {
    int unk00; int unk04; int unk08; int unk0C;
    int unk10; int unk14; int unk18; int unk1C;
    int unk20; int unk24; int unk28; int unk2C;
    int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int unk48; int unk4C;
    int unk50; int unk54; int unk58; int unk5C;
    __m128 unk60;
    __m128 unk70;
    __m128 unk80;
    __m128 unk90;
    void __thiscall FUN_00de4ee0(const __m128*, const __m128*, const __m128*, const __m128*);
};
void __thiscall MatrixOwner::FUN_00de4ee0(const __m128* a, const __m128* b, const __m128* c, const __m128* d) {
    unk60 = *a;
    unk70 = *c;
    unk80 = *b;
    unk90 = *d;
}
