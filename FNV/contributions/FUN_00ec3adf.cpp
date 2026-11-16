extern "C" __declspec(dllimport) void __stdcall DeleteCriticalSection(void* section);
// @fnv 0x00ec3adf
extern "C" void __cdecl FUN_00ec3adf(void* section)
{
    DeleteCriticalSection(section);
}