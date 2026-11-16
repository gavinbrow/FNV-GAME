extern "C" __m128 _mm_sub_ps(__m128 a, __m128 b);
extern int DAT_010eade0;
struct FUN_00e121c0_probe {
    int m_vptr;
    int unk04;
    int unk08;
    int unk0c;
    float m_v10x;
    float m_v10y;
    float m_v10z;
    float m_v10w;
    float m_v20x;
    float m_v20y;
    float m_v20z;
    float m_v20w;
    int m_i30;
    float m_f34;
};
void __cdecl FUN_00d1d0b0(void* owner, const void* a, const void* b, FUN_00e121c0_probe* out, float f);
struct FUN_00e121c0_cls {
    float FUN_00e121c0(const __m128* a, const __m128* b, int* outI);
};
float FUN_00e121c0_cls::FUN_00e121c0(const __m128* a, const __m128* b, int* outI)
{
    __declspec(align(16)) FUN_00e121c0_probe t;
    __m128 va = *a;
    __m128 vd = _mm_sub_ps(*b, va);
    t.m_vptr = (int)&DAT_010eade0;
    t.m_i30 = 0;
    _mm_store_ps(&t.m_v10x, va);
    _mm_store_ps(&t.m_v20x, vd);
    t.m_f34 = 1.0f;
    FUN_00d1d0b0((char*)this + 0x40, a, b, &t, 1.0f);
    int v = t.m_i30;
    float r = t.m_f34;
    if (outI != 0) {
        *outI = v;
    }
    return r;
}