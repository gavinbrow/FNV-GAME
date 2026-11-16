#include <math.h>
extern "C" double DAT_01099680;
extern "C" double DAT_01011598;
extern "C" double DAT_010996d0;
extern "C" float DAT_011f49fc;
// @fnv 0x00fb5a70
void FUN_00fb5a70()
{
    float root = static_cast<float>(sqrt(DAT_01099680));
    DAT_011f49fc = static_cast<float>(DAT_01011598 / (root * DAT_01099680) * DAT_010996d0);
}