#include <math.h>
extern "C" double DAT_01099680;
extern "C" double DAT_01011598;
extern "C" double DAT_010996d0;
extern "C" float DAT_011f400c;
// @fnv 0x00fb5290
void FUN_00fb5290()
{
    volatile float root = static_cast<float>(sqrt(DAT_01099680));
    DAT_011f400c = (DAT_01011598 / (root * DAT_01099680)) * DAT_010996d0;
}
