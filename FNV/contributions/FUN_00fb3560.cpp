#include "original_setting_eh_initializers.h"
extern const char DAT_0109505c;
inline unsigned int PackRgba(unsigned int aiRed, unsigned int aiGreen, unsigned int aiBlue, unsigned int aiAlpha)
{
    unsigned int uirgba;
    uirgba = aiRed << 24;
    uirgba |= (aiGreen & 0xFF) << 16;
    uirgba |= (aiBlue & 0xFF) << 8;
    uirgba |= (aiAlpha & 0xFF);
    return uirgba;
}
namespace fnv_00a0fe20
{
    // @fnv 0x00fb3560
    Setting_01017720_011f96a0 DAT_011f33bc(&::DAT_0109505c, static_cast<int>(PackRgba(255, 251, 233, 255)));
}
