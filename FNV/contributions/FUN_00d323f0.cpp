
#include <xmmintrin.h>
struct Vector4 { float x, y, z, w; };
struct __declspec(align(16)) CopyPacket {
    void* unk00;
    unsigned int unk04, unk08, unk0c;
    unsigned int unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c;
    unsigned int unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48, unk4c;
    Vector4 orientation;
    unsigned int unk60, unk64, unk68, unk6c;
};
struct Argument {
    const void* vtable;
    float scale;
    unsigned int unk08, unk0c;
    Vector4 orientation;
    int identifier;
    unsigned int unk24, unk28, unk2c;
};
extern "C" const float DAT_0104da48;
extern "C" const __m128 DAT_010c44d0;
extern "C" const char UNK_010ce80c;
extern "C" void __cdecl FUN_00d31d30(int, int, const CopyPacket*, const Argument*, const Argument*);

void __cdecl FUN_00d323f0(int a, int b, const CopyPacket* source, int id1, int id2) {
    __m128 orient = _mm_load_ps(&source->orientation.x);
    __m128 inverted = _mm_xor_ps(orient, DAT_010c44d0);
    Argument first;
    first.scale = DAT_0104da48;
    CopyPacket copy = *source;
    _mm_store_ps(&copy.orientation.x, inverted);
    const void* vptr = &UNK_010ce80c;
    first.vtable = vptr;
    first.orientation = source->orientation;
    first.identifier = id1;
    if (id2) {
        Argument second;
        second.vtable = vptr;
        second.scale = DAT_0104da48;
        second.orientation = source->orientation;
        second.identifier = id2;
        FUN_00d31d30(b, a, &copy, &first, &second);
    } else {
        FUN_00d31d30(b, a, &copy, &first, 0);
    }
}