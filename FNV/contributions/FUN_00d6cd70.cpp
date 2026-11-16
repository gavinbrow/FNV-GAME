extern "C" __m128 _mm_xor_ps(__m128,__m128);
extern "C" __m128 _mm_mul_ps(__m128,__m128);
extern "C" __m128 _mm_shuffle_ps(__m128,__m128,unsigned int);
extern "C" __m128 _mm_add_ps(__m128,__m128);
extern "C" __m128 _mm_add_ss(__m128,__m128);
extern "C" void _mm_store_ss(float*,__m128);
extern const __m128 DAT_010c44d0;
extern const double DAT_010c9300;
struct Body409 {
 unsigned unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c;
 unsigned unk20,unk24,unk28,unk2c;
 __m128 inertia;
 unsigned unk40,unk44,unk48,unk4c;
 __m128 basisX,basisY,basisZ;
};
struct Pair409 {
 unsigned unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c;
 unsigned unk20,unk24,unk28,unk2c;
 Body409* first; Body409* second;
};
struct Jacobian409 { __m128 first,second; };
// Adapted from another contributor's previously checked near-match.
void FUN_00d6cd70(const __m128& in, const Pair409& xf, Jacobian409& out, float& outRecip)
{
    const Body409* Q = xf.second;
    __m128 nv = _mm_xor_ps(in, DAT_010c44d0);
    __m128 v = in;
    const Body409* P = xf.first;
    __m128 p50 = P->basisX;
    __m128 p60 = P->basisY;
    __m128 p70 = P->basisZ;
    __m128 t1 = _mm_mul_ps(_mm_shuffle_ps(v, v, 0x55), p60);
    t1 = _mm_add_ps(t1, _mm_mul_ps(_mm_shuffle_ps(v, v, 0), p50));
    t1 = _mm_add_ps(t1, _mm_mul_ps(_mm_shuffle_ps(v, v, 0xaa), p70));
    out.first=t1;
    __m128 q50 = Q->basisX;
    __m128 q60 = Q->basisY;
    __m128 q70 = Q->basisZ;
    __m128 t2 = _mm_mul_ps(_mm_shuffle_ps(nv, nv, 0x55), q60);
    t2 = _mm_add_ps(t2, _mm_mul_ps(_mm_shuffle_ps(nv, nv, 0), q50));
    t2 = _mm_add_ps(t2, _mm_mul_ps(_mm_shuffle_ps(nv, nv, 0xaa), q70));
    out.second=t2;
    __m128 o0 = out.first;
    __m128 o1 = t2;
    __m128 d = _mm_mul_ps(_mm_mul_ps(o0, o0), P->inertia);
    d = _mm_add_ps(d, _mm_mul_ps(_mm_mul_ps(o1, o1), Q->inertia));
    __m128 s = _mm_add_ss(_mm_shuffle_ps(d, d, 0x55), d);
    s = _mm_add_ss(_mm_shuffle_ps(d, d, 0xaa), s);
    float f;
    _mm_store_ss(&f, s);
    f = (float)(f + DAT_010c9300);
    float r = 1.0f / f;
    out.first.m128_f32[3] = r;
    outRecip = r;
}