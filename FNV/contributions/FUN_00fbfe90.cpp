// @fnv 0x00fbfe90
#include <math.h>
extern "C" const double DAT_01099680;
extern "C" const double DAT_010996d0;
extern "C" float DAT_01269b24;
extern "C" void __cdecl FUN_00fbfe90()
{
    float divisor = static_cast<float>(sqrt(DAT_01099680));
    DAT_01269b24 = static_cast<float>(DAT_010996d0 / divisor);
}