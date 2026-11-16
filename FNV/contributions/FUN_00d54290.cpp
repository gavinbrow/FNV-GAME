#include <xmmintrin.h>
extern int DAT_010d0cd4;
extern float DAT_0104da48;
struct FUN_00ca9360_sub { void __fastcall FUN_00ca9360(int count, float* value); };
struct FUN_00d54290 {
    void* volatile m_vptr; unsigned short m_unk04; unsigned short m_word06; int m_value08; int m_unk0c;
    volatile unsigned short m_word10; unsigned short m_unk12; int m_unk14; int m_unk18; int m_unk1c;
    __m128 m_zero20; __m128 m_zero30;
    unsigned short m_word40; volatile unsigned char m_byte42; FUN_00ca9360_sub m_data43; volatile float m_float44;
    FUN_00d54290();
};
FUN_00d54290::FUN_00d54290()
{
    float one = 1.0f;
    m_word06 = 1; m_value08 = 0; m_vptr = &DAT_010d0cd4; m_word10 = 3; m_byte42 = 0; m_word40 = 5;
    m_data43.FUN_00ca9360(5, &one);
    m_float44 = DAT_0104da48;
_mm_store_ps((float*)&m_zero20, _mm_setzero_ps()); _mm_store_ps((float*)&m_zero30, _mm_setzero_ps());
}