union __declspec(intrin_type) __declspec(align(16)) __m128 { float m128_f32[4]; unsigned __int64 m128_u64[2]; };
extern "C" __m128 _mm_sub_ps(__m128, __m128);
extern "C" __m128 _mm_mul_ps(__m128, __m128);
extern "C" __m128 _mm_sub_ss(__m128, __m128);
extern "C" __m128 _mm_mul_ss(__m128, __m128);
extern "C" __m128 _mm_add_ss(__m128, __m128);
extern "C" __m128 _mm_shuffle_ps(__m128, __m128, unsigned int);
extern "C" int _mm_movemask_ps(__m128);

extern const signed char DAT_010cb440[];

struct S00da8390_Real
{
    __m128 r;
    S00da8390_Real operator*(const S00da8390_Real& o) const { S00da8390_Real t; t.r = _mm_mul_ss(r, o.r); return t; }
    S00da8390_Real operator-(const S00da8390_Real& o) const { S00da8390_Real t; t.r = _mm_sub_ss(r, o.r); return t; }
};

struct S00da8390_Vec
{
    __m128 q;
    void setSub4(const S00da8390_Vec& a, const S00da8390_Vec& b) { q = _mm_sub_ps(a.q, b.q); }
    void setMul4(const S00da8390_Vec& a, const S00da8390_Vec& b) { q = _mm_mul_ps(a.q, b.q); }
    S00da8390_Real horizontalAdd3() const
    {
        S00da8390_Real t;
        __m128 y = _mm_shuffle_ps(q, q, 0x55);
        y = _mm_add_ss(y, q);
        __m128 z = _mm_shuffle_ps(q, q, 0xaa);
        t.r = _mm_add_ss(z, y);
        return t;
    }
};

static __declspec(noinline) int __cdecl FUN_00da8390(const S00da8390_Vec* v, const S00da8390_Vec* p, float* dist)
{
    for (int i = 0; i < 3; ++i) {
        int a = DAT_010cb440[i + 2];
        int b = DAT_010cb440[i];
        if (dist[a] >= 0.0f && dist[b] >= 0.0f) {
            S00da8390_Vec ea; ea.setSub4(v[a], v[i]);
            S00da8390_Vec eb; eb.setSub4(v[b], v[i]);
            S00da8390_Vec d; d.setSub4(*p, v[i]);
            S00da8390_Vec n; n.setSub4(v[3], v[i]);
            S00da8390_Vec m_dea; m_dea.setMul4(d, ea);
            S00da8390_Vec m_deb; m_deb.setMul4(d, eb);
            S00da8390_Vec m_nea; m_nea.setMul4(n, ea);
            S00da8390_Vec m_neb; m_neb.setMul4(n, eb);
            S00da8390_Real nb = m_neb.horizontalAdd3();
            S00da8390_Real da = m_dea.horizontalAdd3();
            S00da8390_Real db = m_deb.horizontalAdd3();
            S00da8390_Real na = m_nea.horizontalAdd3();
            S00da8390_Real s; s.r = _mm_sub_ss(_mm_mul_ss(da.r, nb.r), _mm_mul_ss(db.r, na.r));
            if (_mm_movemask_ps(s.r) & 1)
                dist[b] = -1.0f;
            else
                dist[a] = -1.0f;
        }
    }
    if (dist[0] > 0.0f) return 0;
    if (dist[1] > 0.0f) return 1;
    if (dist[2] > 0.0f) return 2;
    return -1;
}

int S00da8390_Call(const S00da8390_Vec* p, float* dist, const S00da8390_Vec* v)
{
    return FUN_00da8390(v, p, dist);
}
