// Prior binding evidence: gpt6_astra_pro_fnv_20261114_16de7c73ca_small.
// The neighbouring object g_011c7810 bounds this four-byte array to three elements.
typedef void (__thiscall* ElementRoutine)(void*);

extern unsigned char DAT_011c7804[];
// The iterator invokes these external entry points with a thiscall receiver.
extern "C" void __cdecl FUN_006694e0();
extern "C" void __cdecl FUN_0045cec0();
extern "C" void __stdcall FUN_00ec782f(
    void* elements,
    unsigned int elementSize,
    int elementCount,
    ElementRoutine construct,
    ElementRoutine destroy);
extern "C" void __cdecl FUN_00fc9a10();
extern "C" int __cdecl atexit(void (__cdecl* callback)());

// @fnv 0x00f416c0
void FUN_00f416c0()
{
    FUN_00ec782f(
        DAT_011c7804,
        4,
        3,
        reinterpret_cast<ElementRoutine>(FUN_006694e0),
        reinterpret_cast<ElementRoutine>(FUN_0045cec0));
    atexit(FUN_00fc9a10);
}
