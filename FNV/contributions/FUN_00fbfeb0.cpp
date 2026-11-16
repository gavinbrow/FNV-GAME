// @fnv 0x00fbfeb0
#include <math.h>
extern "C" const double DAT_01099680;
extern "C" const double DAT_010996d0;
extern "C" const double DAT_01011598;
extern "C" float DAT_01269b1c;
extern "C" void __cdecl FUN_00fbfeb0()
{
    float root = static_cast<float>(sqrt(DAT_01099680));
    double product = root * DAT_01099680;
    DAT_01269b1c = static_cast<float>((DAT_01011598 / product) * DAT_010996d0);
}