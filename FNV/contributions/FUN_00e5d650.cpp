union __declspec(intrin_type) __declspec(align(16)) __m128 {
    float m128_f32[4];
    unsigned __int64 m128_u64[2];
};
extern "C" {
__m128 _mm_set_ps1(float a);
__m128 _mm_setzero_ps(void);
__m128 _mm_add_ps(__m128 a, __m128 b);
__m128 _mm_sub_ps(__m128 a, __m128 b);
__m128 _mm_unpackhi_ps(__m128 a, __m128 b);
__m128 _mm_shuffle_ps(__m128 a, __m128 b, unsigned int imm);
}
struct hkVector4 {
    __m128 m_quad;
    __forceinline void setZero4() { m_quad = _mm_setzero_ps(); }
    __forceinline void setAll(float x) { m_quad = _mm_set_ps1(x); }
    __forceinline void setSub4(const hkVector4& a, const hkVector4& b) { m_quad = _mm_sub_ps(a.m_quad, b.m_quad); }
    __forceinline void add4(const hkVector4& a) { m_quad = _mm_add_ps(m_quad, a.m_quad); }
    __forceinline void setXYZ(const hkVector4& v) { m_quad = _mm_shuffle_ps(v.m_quad, _mm_unpackhi_ps(v.m_quad, m_quad), 0xc4); }
    __forceinline float& operator()(int i) { return m_quad.m128_f32[i]; }
    __forceinline const float& operator()(int i) const { return m_quad.m128_f32[i]; }
};
struct RaySegment {
    hkVector4 m_from;
    hkVector4 m_to;
    volatile unsigned int m_code;
};
struct PrimitiveInfo {
    unsigned int m_00;
    unsigned int m_04;
    unsigned int m_08;
    unsigned int m_0c;
    unsigned int m_10;
    unsigned int m_stride;
};
struct RayVirtualMachine {
    unsigned int m_input;
    unsigned int m_04;
    unsigned int m_08;
    unsigned int m_0c;
    float m_invLength;
    unsigned int m_14;
    unsigned int m_18;
    unsigned int m_1c;
    unsigned int m_output;
    unsigned int m_24;
    unsigned int m_28;
    unsigned int m_2c;
    hkVector4 m_ray;
    void FUN_00e5f070(PrimitiveInfo* info, unsigned int code, hkVector4* offset);
};
struct RayQuery {
    hkVector4 m_offset;
    hkVector4 m_scale;
    RayVirtualMachine m_vm;
};
extern const double DAT_01091c00;
void FUN_00e5d650(const RaySegment* seg, const hkVector4* to, unsigned int input, unsigned int output)
{
    RayQuery q;
    q.m_vm.m_invLength = 1.0f / seg->m_to(3);
    const unsigned int inputCopy = *reinterpret_cast<volatile const unsigned int*>(&input);
    const unsigned int code = seg->m_code;

    q.m_offset.setZero4();
    q.m_vm.m_input = inputCopy;
    PrimitiveInfo info;
    info.m_08 = 0;
    info.m_0c = 0;
    info.m_10 = 0;
    info.m_00 = 0;
    info.m_stride = 16;
    info.m_04 = 0;
    q.m_scale.setAll((float)(q.m_vm.m_invLength * DAT_01091c00));
    hkVector4 dir;
    dir.setSub4(*to, seg->m_to);
    dir.add4(dir);
    q.m_vm.m_ray.setXYZ(dir);
    q.m_vm.m_ray(3) = (*to)(3) + (*to)(3);
    q.m_vm.m_output = output;
    q.m_vm.FUN_00e5f070(&info, code, &q.m_offset);
}