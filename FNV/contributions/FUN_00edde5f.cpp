struct CriticalSectionSlot
{
    void* section;
    unsigned int reserved;
};
extern "C" CriticalSectionSlot DAT_011c28a8[];
extern "C" __declspec(dllimport) void __stdcall LeaveCriticalSection(void* section);
// @fnv 0x00edde5f
extern "C" void FUN_00edde5f(int index)
{
    LeaveCriticalSection(DAT_011c28a8[index].section);
}
