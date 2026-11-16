union __declspec(intrin_type) __declspec(align(16)) __m128 {
    float m128_f32[4];
    unsigned __int64 m128_u64[2];
};

extern "C" __m128 _mm_add_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_sub_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_mul_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_min_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_max_ps(__m128 a, __m128 b);
extern "C" __m128 _mm_load_ps1(const float* p);

extern const __m128 DAT_010c71d0;

struct hkVector4D563 {
    __m128 m_quad;
    hkVector4D563() {}
    hkVector4D563(const hkVector4D563& v) { m_quad = v.m_quad; }
    void operator=(const hkVector4D563& v) { m_quad = v.m_quad; }
    void setAll(const float& f) { m_quad = _mm_load_ps1(&f); }
    void setAdd4(const hkVector4D563& a, const hkVector4D563& b) { m_quad = _mm_add_ps(a.m_quad, b.m_quad); }
    void setSub4(const hkVector4D563& a, const hkVector4D563& b) { m_quad = _mm_sub_ps(a.m_quad, b.m_quad); }
    void add4(const hkVector4D563& a) { m_quad = _mm_add_ps(m_quad, a.m_quad); }
    void sub4(const hkVector4D563& a) { m_quad = _mm_sub_ps(m_quad, a.m_quad); }
    void mul4(const __m128& s) { m_quad = _mm_mul_ps(m_quad, s); }
    void setMin4(const hkVector4D563& a, const hkVector4D563& b) { m_quad = _mm_min_ps(a.m_quad, b.m_quad); }
    void setMax4(const hkVector4D563& a, const hkVector4D563& b) { m_quad = _mm_max_ps(a.m_quad, b.m_quad); }
};

struct hkAabbD563 {
    hkVector4D563 m_min;
    hkVector4D563 m_max;
    void includeAabb(const hkAabbD563& other) {
        m_min.setMin4(m_min, other.m_min);
        m_max.setMax4(m_max, other.m_max);
    }
};

struct hkpD563Tree { void FUN_00d4abf0(void* arg); };
struct hkpD563Key { unsigned int unk00, unk04, unk08, unk0c; };

void __cdecl FUN_00d55680(hkpD563Tree* tree, const hkpD563Key* key, hkAabbD563* out);

class hkpD563Shape {
public:
    hkpD563Tree* FUN_00d562f0();
    int FUN_00d56160(void* arg, int level);
    void FUN_00d563a0(void* arg);

    unsigned int unk00, unk04, unk08, unk0c, unk10, unk14, unk18, unk1c;
    unsigned int unk20, unk24, unk28, unk2c, unk30, unk34, unk38, unk3c;
    unsigned int unk40, unk44, unk48, unk4c, unk50, unk54, unk58, unk5c;
    unsigned int unk60, unk64, unk68, unk6c, unk70, unk74, unk78, unk7c;
    hkpD563Key m_key;
    hkVector4D563 m_aabbHalfExtents;
    hkVector4D563 m_aabbCenter;
    unsigned int unkB0, unkB4;
    int m_numLevels;
    unsigned int unkBC, unkC0, unkC4, unkC8, unkCC, unkD0, unkD4, unkD8, unkDC;
    int m_total;
    float m_tolerance;
};

void hkpD563Shape::FUN_00d563a0(void* arg) {
    hkpD563Tree* tree = FUN_00d562f0();
    tree->FUN_00d4abf0(arg);

    hkAabbD563 existing;
    hkAabbD563 updated;
    existing.m_min.setSub4(m_aabbCenter, m_aabbHalfExtents);
    existing.m_max.setAdd4(m_aabbHalfExtents, m_aabbCenter);

    FUN_00d55680(tree, &m_key, &updated);

    hkVector4D563 tolerance;
    tolerance.setAll(m_tolerance);
    hkAabbD563 expanded;
    expanded.m_min.setSub4(updated.m_min, tolerance);
    expanded.m_max.setAdd4(updated.m_max, tolerance);
    existing.includeAabb(expanded);

    hkVector4D563 center;
    center.setAdd4(existing.m_min, existing.m_max);
    center.mul4(DAT_010c71d0);
    m_aabbCenter = center;
    hkVector4D563 halfExtents;
    halfExtents.setSub4(existing.m_max, existing.m_min);
    halfExtents.mul4(DAT_010c71d0);
    m_aabbHalfExtents = halfExtents;

    int lastLevel = m_numLevels - 1;
    m_total += FUN_00d56160(arg, lastLevel);
}
