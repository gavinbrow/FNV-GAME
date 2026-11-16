// @fnv 0x00fb51e0
#include <math.h>
extern const double DAT_01099680;
extern const double DAT_01011598;
extern const double DAT_010996d0;
extern float DAT_011f3fec;
void FUN_00fb51e0()
{
    float root = static_cast<float>(sqrt(DAT_01099680));
    DAT_011f3fec = static_cast<float>((DAT_01011598 / (root * DAT_01099680)) * DAT_010996d0);
}
