#include "h_5ea5442dbdbb.h"

class NiInterpControllerFlagCheck : public NiInterpController {
public:
    void FUN_00a2f8f0();
};

void NiInterpControllerFlagCheck::FUN_00a2f8f0()
{
    unsigned char value = *(unsigned char*)((char*)this + 8);
    for (int i = 0; i < 5; ++i)
        value = (unsigned char)(value >> 1);
    if (!(value & 1)) {
        *(float*)((char*)this + 0x14) = 0.0f;
        *(float*)((char*)this + 0x18) = 0.0f;
    }
}
