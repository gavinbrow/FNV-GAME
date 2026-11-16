#include <xmmintrin.h>
__forceinline void subtract(__m128& a,const __m128& b){a=_mm_sub_ps(a,b);}
__forceinline void subtractGroup(__m128* d,const __m128* s){subtract(d[0],s[0]); subtract(d[1],s[1]); subtract(d[2],s[2]);}
void __cdecl FUN_00e29380(__m128* destination,const __m128* source){
subtractGroup(destination+0,source+0);
subtractGroup(destination+3,source+3);
subtract(destination[6],source[6]);
subtract(destination[7],source[7]);
subtract(destination[8],source[8]);
subtract(destination[9],source[9]);
subtract(destination[10],source[10]);
subtract(destination[11],source[11]);
}