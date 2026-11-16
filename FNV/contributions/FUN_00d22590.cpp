#include <xmmintrin.h>
extern int DAT_010ce25c;
union __declspec(align(16)) AlignedHKVector4 { __m128 simd; struct {float x,y,z,w;}; };
struct FUN_00d22590_Class : hkpCapsuleShape {
    FUN_00d22590_Class* __thiscall FUN_00d22590(
        const AlignedHKVector4& first, const AlignedHKVector4& second, float radius);
};
FUN_00d22590_Class* __thiscall FUN_00d22590_Class::FUN_00d22590(
    const AlignedHKVector4& first,const AlignedHKVector4& second,float radius)
{
    m_radius = radius;
    m_referenceCount = 1;
    m_userData = 0;
    m_type = 5;
    *reinterpret_cast<void**>(this) = &DAT_010ce25c;
    reinterpret_cast<AlignedHKVector4*>(&m_vertexA)->simd = first.simd;
    reinterpret_cast<AlignedHKVector4*>(&m_vertexB)->simd = second.simd;
    *reinterpret_cast<volatile float*>(&m_vertexA.w) = radius;
    *reinterpret_cast<volatile float*>(&m_vertexB.w) = radius;
    return this;
}
