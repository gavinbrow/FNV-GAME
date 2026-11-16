
#include "h_4521e010f48c.h"

extern __declspec(thread) unsigned char DAT_tls_0268[0x269];
extern "C" void __cdecl FUN_00703c00(const char* format, ...);
extern char str_01035ee4[];

bool __cdecl FUN_005a4540(TESObjectREFR* reference, void* arg1, void* arg2, double& result)
{
    result = 0.0;
    if (reference->IsMobileObject()) {
        MobileObject* mobile = static_cast<MobileObject*>(reference);
        mobile->Unk_B6();
    }
    if (DAT_tls_0268[0x268]) {
        FUN_00703c00(str_01035ee4, result);
    }
    return true;
}