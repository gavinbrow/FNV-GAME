extern "C" __m128 _mm_mul_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_shuffle_ps(__m128 a, __m128 b, int imm8);
extern "C" __m128 _mm_load_ps(const float* p);
extern "C" void _mm_store_ps(float* p, __m128 a);
void FUN_00e29510(__m128* out, const __m128* m, const __m128* v)
{
    __m128 v1 = v[0];
    __m128 a = _mm_mul_ps(_mm_shuffle_ps(v1, v1, 0x55), m[1]);
    a = _mm_add_ps(a, _mm_mul_ps(_mm_shuffle_ps(v1, v1, 0x00), m[0]));
    a = _mm_add_ps(a, _mm_mul_ps(_mm_shuffle_ps(v1, v1, 0xaa), m[2]));
    __m128 v2 = v[1];
    __m128 b = _mm_mul_ps(_mm_shuffle_ps(v2, v2, 0x55), m[4]);
    b = _mm_add_ps(b, _mm_mul_ps(_mm_shuffle_ps(v2, v2, 0x00), m[3]));
    b = _mm_add_ps(b, _mm_mul_ps(_mm_shuffle_ps(v2, v2, 0xaa), m[5]));
    _mm_store_ps((float*)out, b);
    __m128 w1 = v[0];
    __m128 d = _mm_mul_ps(_mm_shuffle_ps(w1, w1, 0x55), m[7]);
    d = _mm_add_ps(d, _mm_mul_ps(_mm_shuffle_ps(w1, w1, 0x00), m[6]));
    d = _mm_add_ps(d, _mm_mul_ps(_mm_shuffle_ps(w1, w1, 0xaa), m[8]));
    __m128 w2 = v[1];
    __m128 e = _mm_mul_ps(_mm_shuffle_ps(w2, w2, 0x55), m[10]);
    e = _mm_add_ps(e, _mm_mul_ps(_mm_shuffle_ps(w2, w2, 0x00), m[9]));
    e = _mm_add_ps(e, _mm_mul_ps(_mm_shuffle_ps(w2, w2, 0xaa), m[11]));
    _mm_store_ps((float*)out, _mm_add_ps(_mm_load_ps((float*)out), a));
    hkVector4* dest = reinterpret_cast<hkVector4*>(out);
    dest[1].m_quad = e;
    hkVector4 extra;
    extra.m_quad = d;
    dest[1].add4(extra);
}