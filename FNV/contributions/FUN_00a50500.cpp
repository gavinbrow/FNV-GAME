#include "h_112b2a6c444e.h"
extern unsigned int _DAT_011f3fe4;
extern unsigned char _DAT_010996bc;
extern unsigned char _DAT_010996ac;
extern unsigned char _DAT_01099698;
unsigned int __cdecl FUN_00a7d330(unsigned int);
unsigned int __cdecl FUN_00a7d510(const unsigned char*, unsigned int);

struct BinaryStreamPosition {
    unsigned int unk00;
    unsigned int unk04;
    unsigned short unk08;
    unsigned short unk0A;
    unsigned short unk0C;
    unsigned short unk0E;
    void FUN_0096ad30(unsigned int);
    void FUN_0096ae90(unsigned int, unsigned int*);
};
struct BSplineBaseCalls : NiBSplineInterpolator {
    void FUN_00a58200(NiStream&);
};
struct QuatLoadCalls : NiQuatTransform {
    void FUN_00a38cb0(NiStream&);
};
struct BSplineTransformLoad : NiBSplineTransformInterpolator {
    void FUN_00a50500(NiStream& stream);
};
void BSplineTransformLoad::FUN_00a50500(NiStream& stream) {
    reinterpret_cast<BSplineBaseCalls*>(this)->FUN_00a58200(stream);
    BinaryStreamPosition& pos = reinterpret_cast<BinaryStreamPosition&>(stream);
    unsigned int value = FUN_00a7d330(_DAT_011f3fe4);
    unsigned int index = pos.unk0A;
    if (index >= pos.unk08)
        pos.FUN_0096ad30(index + pos.unk0E);
    pos.FUN_0096ae90(index, &value);

    reinterpret_cast<QuatLoadCalls&>(m_kTransform).FUN_00a38cb0(stream);
    value = FUN_00a7d510(&_DAT_010996bc, m_uiTranslationHandle);
    index = pos.unk0A;
    if (index >= pos.unk08)
        pos.FUN_0096ad30(index + pos.unk0E);
    pos.FUN_0096ae90(index, &value);

    value = FUN_00a7d510(&_DAT_010996ac, m_uiRotationHandle);
    index = pos.unk0A;
    if (index >= pos.unk08)
        pos.FUN_0096ad30(index + pos.unk0E);
    pos.FUN_0096ae90(index, &value);

    value = FUN_00a7d510(&_DAT_01099698, m_uiScaleHandle);
    index = pos.unk0A;
    if (index >= pos.unk08)
        pos.FUN_0096ad30(index + pos.unk0E);
    pos.FUN_0096ae90(index, &value);
}