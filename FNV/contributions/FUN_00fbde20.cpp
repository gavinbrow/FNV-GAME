#include <xmmintrin.h>

extern float DAT_01011d78;
extern float DAT_01012068;
extern __m128 DAT_012683b0;

// @fnv 0x00fbde20
void FUN_00fbde20()
{
    DAT_012683b0 = _mm_setr_ps(DAT_01011d78, DAT_01011d78,
                            DAT_01011d78, DAT_01012068);
}
