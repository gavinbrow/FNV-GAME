#include <xmmintrin.h>
extern double _gModifierZero;
struct FUN_00e07b90_bounds { float unk00,unk04,unk08,minimumX,maximumX,minimumY,maximumY,minimumZ,maximumZ; };
struct FUN_00e07b90_vector { float x,y,z,w; };
void __stdcall FUN_00e07b90(const FUN_00e07b90_bounds* bounds, FUN_00e07b90_vector* result)
{
    __m128 initial = _mm_setr_ps(bounds->minimumX, bounds->minimumY, bounds->minimumZ, 0.0f);
    _mm_store_ps(&result->x, initial);
    float largest = 0.0f;
    float extent = bounds->maximumX - bounds->minimumX;
    if (!(extent < _gModifierZero)) largest = extent;
    extent = bounds->maximumY - bounds->minimumY;
    if (!(largest > extent)) largest = extent;
    extent = bounds->maximumZ - bounds->minimumZ;
    if (!(largest > extent)) largest = extent;
    result->w = 65536.0 * (254.0 / largest);
}




