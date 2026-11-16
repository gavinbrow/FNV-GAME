#include <xmmintrin.h>
extern int DAT_010d0a64;
struct WheelHeader {
    int* m_vtable; unsigned short m_memSizeAndFlags, m_referenceCount; unsigned int m_userData;
    WheelHeader() : m_referenceCount(1), m_userData(0) { m_vtable = &DAT_010d0a64; }
};
union Vec4 { __m128 simd; volatile float component[4]; };
struct Matrix3 {
    Vec4 axis0,axis1,axis2;
    void SetIdentity() {
        __m128 zero = _mm_setzero_ps();
        axis0.simd=zero; axis1.simd=zero; axis2.simd=zero;
        axis0.component[0]=1.0f;
        axis1.component[1]=1.0f;
        axis2.component[2]=1.0f;
    }
};
struct FUN_00d4f000 {
    unsigned int unk00, unk04, unk08, unk0C;
    Matrix3 m_20; Vec4 m_50; Matrix3 m_60; Vec4 m_90;
    unsigned char unkA0, unkA1, m_a2, unkA3;
    float m_a4,m_a8;
    unsigned char unkAC,unkAD,m_ae,unkAF;
    float m_b0,m_b4;
    unsigned char unkB8,unkB9,m_ba,unkBB,unkBC,unkBD,m_be,unkBF;
    Vec4 m_c0; Matrix3 m_d0,m_100;
    unsigned char unk130,unk131; volatile unsigned char m_132; unsigned char unk133;
    unsigned int unk134,unk138,unk13C;
    FUN_00d4f000();
};
struct FUN_00d4edc0 {
    WheelHeader m_header; unsigned int m_reserved0C;
    FUN_00d4f000 m_atoms;
    Vec4 m_initialAxleInB,m_initialSteeringAxisInB;
    FUN_00d4edc0();
};
FUN_00d4edc0::FUN_00d4edc0() {
    m_atoms.m_a4 = -0.5f;
    m_atoms.m_a2 = 0;
    m_atoms.m_a8 = 0.5f;
    m_atoms.m_ae = 0;
    m_atoms.m_ba = 1;
    m_atoms.m_be = 2;
    m_atoms.m_b4 = m_atoms.m_b0 = 0.0f;
    m_atoms.m_d0.SetIdentity();
    m_atoms.m_100.SetIdentity();
    m_atoms.m_20.SetIdentity();
    __m128 zero = _mm_setzero_ps();
    m_atoms.m_50.simd = zero;
    m_atoms.m_60.SetIdentity();
    m_atoms.m_90.simd = zero;
    m_atoms.m_132=0;
}