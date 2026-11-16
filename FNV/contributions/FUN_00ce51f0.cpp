#include <xmmintrin.h>

struct __declspec(align(16)) Vector { float x,y,z,w; };
struct FUN_008cd6a0_Class { Vector row0,row1,row2; void FUN_00cb2d90(void*); };
struct FUN_00cdf250_class { Vector row0,row1,row2; void FUN_00cd55b0(int*,int); };
struct TransformMatrix { Vector row0,row1,row2,row3; void FUN_00cb2050(int); };
struct Transform { Vector position; float rotationX,rotationY,rotationZ,rotationW; float scaleX,scaleY,scaleZ; void FUN_00ce51f0(int); };
void Transform::FUN_00ce51f0(int out) {
 FUN_008cd6a0_Class rotation;
 rotation.FUN_00cb2d90(&rotationX);
 FUN_00cdf250_class scale;
 *(__m128*)&scale.row0 = _mm_setzero_ps(); scale.row0.x=scaleX;
 *(__m128*)&scale.row1 = _mm_setzero_ps(); scale.row1.y=scaleY;
 *(__m128*)&scale.row2 = _mm_setzero_ps(); scale.row2.z=scaleZ;
 FUN_00cdf250_class combined;
 combined.FUN_00cd55b0((int*)&rotation,(int)&scale);
 TransformMatrix result;
 *(__m128*)&result.row0=*(__m128*)&combined.row0; *(__m128*)&result.row1=*(__m128*)&combined.row1; *(__m128*)&result.row2=*(__m128*)&combined.row2; *(__m128*)&result.row3=*(__m128*)&position;
 result.FUN_00cb2050(out);
}




