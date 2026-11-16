union __declspec(intrin_type) __declspec(align(16)) __m128 {
    float m128_f32[4];
};

extern "C" {
    __m128 _mm_shuffle_ps(__m128, __m128, int);
    __m128 _mm_mul_ps(__m128, __m128);
    __m128 _mm_add_ps(__m128, __m128);
    __m128 _mm_sub_ps(__m128, __m128);
    __m128 _mm_add_ss(__m128, __m128);
    __m128 _mm_unpackhi_ps(__m128, __m128);
}

struct FUN_00ce0ca0_Quaternion {
    __m128 value;

    void __thiscall FUN_00ce0ca0(
        const FUN_00ce0ca0_Quaternion& rhs);
};

void FUN_00ce0ca0_Quaternion::FUN_00ce0ca0(
    const FUN_00ce0ca0_Quaternion& rhs)
{
    __m128 b = rhs.value;
    __m128 a = value;

    __m128 v = _mm_shuffle_ps(a, a, 0xc9);
    __m128 t = _mm_shuffle_ps(b, b, 0xd2);
    v = _mm_mul_ps(v, t);

    __m128 u = _mm_shuffle_ps(b, b, 0xc9);
    t = _mm_shuffle_ps(a, a, 0xd2);
    t = _mm_mul_ps(t, u);
    v = _mm_sub_ps(v, t);

    t = _mm_shuffle_ps(a, a, 0xff);
    t = _mm_shuffle_ps(t, t, 0);
    t = _mm_mul_ps(t, b);
    t = _mm_add_ps(t, v);

    v = _mm_shuffle_ps(b, b, 0xff);
    v = _mm_shuffle_ps(v, v, 0);
    v = _mm_mul_ps(v, a);

    v = _mm_add_ps(v, t);
    a = _mm_mul_ps(a, b);

    t = _mm_shuffle_ps(a, a, 0x55);
    t = _mm_add_ss(t, a);

    b = _mm_shuffle_ps(a, a, 0xaa);
    b = _mm_add_ss(b, t);

    t = v;
    b = _mm_shuffle_ps(b, b, 0);
    a = _mm_sub_ps(a, b);

    v = _mm_unpackhi_ps(v, a);
    t = _mm_shuffle_ps(t, v, 0xc4);

    value = t;
}
