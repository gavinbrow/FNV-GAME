#include <xmmintrin.h>
extern const __m128 identityRotation;
struct Owner { int unk00,unk04,unk08; volatile unsigned char active,unk0d; volatile unsigned short mask; __m128 position, rotation, velocity, angularVelocity; __m128 axisX,axisY,axisZ,translation; volatile float mass,drag,tolerance,friction,restitution,damping,maxSpeed,maxAngularSpeed,limit; volatile unsigned char enabled,awake,mode,group,flag0,flag1,flag2,flag3; Owner* FUN_00cf5ea0(); };
Owner* Owner::FUN_00cf5ea0() {
 _mm_store_ps(reinterpret_cast<float*>(&position),_mm_setzero_ps()); _mm_store_ps(reinterpret_cast<float*>(&rotation),identityRotation); _mm_store_ps(reinterpret_cast<float*>(&velocity),_mm_setzero_ps()); _mm_store_ps(reinterpret_cast<float*>(&angularVelocity),_mm_setzero_ps()); _mm_store_ps(reinterpret_cast<float*>(&axisX),_mm_setzero_ps()); _mm_store_ps(reinterpret_cast<float*>(&axisY),_mm_setzero_ps()); _mm_store_ps(reinterpret_cast<float*>(&axisZ),_mm_setzero_ps());
 axisX.m128_f32[0]=1.0f; axisY.m128_f32[1]=1.0f; axisZ.m128_f32[2]=1.0f;
 enabled=1; mass=1.0f; _mm_store_ps(reinterpret_cast<float*>(&translation),_mm_setzero_ps()); drag=0.0f; tolerance=0.05f; friction=1.0f; restitution=0.5f; damping=0.4f; maxSpeed=200.0f; maxAngularSpeed=200.0f; limit=-1.0f; awake=1; active=1; mask=0xffff; mode=2; group=0xff; unk00=0; unk04=0; unk08=0; flag0=0; flag1=0; flag2=0; flag3=0; return this;
}






