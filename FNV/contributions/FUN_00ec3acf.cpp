extern "C" __declspec(dllimport) void __stdcall InitializeCriticalSection(void* section);
// @fnv 0x00ec3acf
extern "C" void FUN_00ec3acf(void* section)
{
    InitializeCriticalSection(section);
}
