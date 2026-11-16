#include <xmmintrin.h>
extern double DAT_01017b70;
extern double DAT_01012640;
struct Vector4 {
 __m128 m_quad;
 float length3() const {
   __m128 squares = _mm_mul_ps(m_quad,m_quad);
   __m128 yy = _mm_shuffle_ps(squares,squares,_MM_SHUFFLE(1,1,1,1));
   __m128 zz = _mm_shuffle_ps(squares,squares,_MM_SHUFFLE(2,2,2,2));
   return _mm_cvtss_f32(_mm_sqrt_ss(_mm_add_ss(zz,_mm_add_ss(yy,squares))));
 }
};
struct Entity {
 const Vector4& linearVelocity() const { return *(const Vector4*)((const char*)this+0x1b0); }
};
struct FUN_00e37820StandIn {
 void* unk00; void* unk04; void* unk08; void* unk0c; void* unk10; void* unk14; Entity* m_entity;
 float FUN_00e37820();
};
float FUN_00e37820StandIn::FUN_00e37820() {
 return (float)(((double)m_entity->linearVelocity().length3()/DAT_01017b70)*DAT_01012640);
}