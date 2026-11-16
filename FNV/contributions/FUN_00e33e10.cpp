#include <xmmintrin.h>
struct __declspec(align(16)) AlignedVector4 {float x,y,z,w;};
struct ResultArg { AlignedVector4* ptr; AlignedVector4* get() const {return ptr;} };
extern const AlignedVector4 DAT_01268700;
struct FUN_00e33e10_Class:hkaSplineCompressedAnimation{
 void FUN_00e33e10(float time,int track,int enabled,int block,unsigned int*cursor,ResultArg result);
};
void __cdecl FUN_00e33a30(unsigned int*,int,float,float,int,int,const AlignedVector4*,AlignedVector4*);
void FUN_00e33e10_Class::FUN_00e33e10(float time,int track,int enabled,int block,unsigned int*cursor,ResultArg result){
 __m128 constant=_mm_load_ps(&DAT_01268700.x);
 if ((unsigned char)enabled==0){
  _mm_store_ps(&result.get()->x,constant);
  *cursor=(*cursor+3)&~3u;
  return;
 }
 AlignedVector4 defaults;
 _mm_store_ps(&defaults.x,constant);
 FUN_00e33a30(cursor,track,m_frameDuration,time,enabled,block,&defaults,result.get());
 *cursor=(*cursor+3)&~3u;
}