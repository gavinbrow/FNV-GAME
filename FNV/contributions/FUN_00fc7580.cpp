#include <math.h>

extern double DAT_010231b0;
extern float DAT_0126f9c4;

// @fnv 0x00fc7580
void FUN_00fc7580()
{
    // Preserve the explicit single-precision rounding step.
    volatile float rounded = static_cast<float>(sqrt(DAT_010231b0));
    DAT_0126f9c4 = rounded;
}
