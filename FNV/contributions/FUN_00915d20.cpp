#include "h_5e47b0f5d932.h"

struct FUN_00915d20_shell : public MiddleHighProcess {
    void FUN_00915d20(unsigned char value);
};

void FUN_00915d20_shell::FUN_00915d20(unsigned char value)
{
    *reinterpret_cast<unsigned char*>(&bWantWeaponDrawn) = value;
}