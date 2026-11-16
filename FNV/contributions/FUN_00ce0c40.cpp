#include <math.h>
float FUN_00ce0c40(float angle)
{
    float original = angle;
    angle = fabsf(angle);
    if (angle >= 1.0f) {
        if (original > 0.0f) angle = 1.5707963705062866f;
        else angle = -1.5707963705062866f;
    } else {
        return asinf(original);
    }
    return angle;
}
