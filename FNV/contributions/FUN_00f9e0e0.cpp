extern "C" __declspec(dllimport) void* __stdcall CreateEventA(
    void* securityAttributes,
    int manualReset,
    int initialState,
    const char* name);

extern void* DAT_011dd3b0;

// @fnv 0x00f9e0e0
void FUN_00f9e0e0()
{
    DAT_011dd3b0 = CreateEventA(0, 0, 0, 0);
}
