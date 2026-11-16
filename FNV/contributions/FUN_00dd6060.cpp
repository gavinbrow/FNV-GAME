#include <xmmintrin.h>
struct FNV_dd6060_Shape {
    virtual void v00(); virtual void v04(); virtual void v08(); virtual void v0C();
    virtual void v10(); virtual void v14(); virtual void v18();
    virtual void v1C(const hkRotation* rotation, float distance, __m128* output);
};
struct FNV_dd6060_Class : hkpConvexTranslateShape {
    void __thiscall FUN_00dd6060(const hkRotation* rotation, float distance, __m128* output);
};
void FNV_dd6060_Class::FUN_00dd6060(const hkRotation* rotation, float distance, __m128* output)
{
    FNV_dd6060_Shape* shape = reinterpret_cast<FNV_dd6060_Shape*>(m_childShape.m_childShape);
    shape->v1C(rotation, distance, output);
    __m128 translation = _mm_load_ps(&m_translation.x);
    __m128 moved = _mm_mul_ps(_mm_shuffle_ps(translation, translation, 0x55), _mm_load_ps(&rotation->m_col1.x));
    moved = _mm_add_ps(moved, _mm_mul_ps(_mm_shuffle_ps(translation, translation, 0x00), _mm_load_ps(&rotation->m_col0.x)));
    moved = _mm_add_ps(moved, _mm_mul_ps(_mm_shuffle_ps(translation, translation, 0xaa), _mm_load_ps(&rotation->m_col2.x)));
    output[0] = _mm_add_ps(output[0], moved);
    output[1] = _mm_add_ps(output[1], moved);
}
