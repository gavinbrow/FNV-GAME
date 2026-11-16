extern "C" __declspec(dllimport) void __stdcall LeaveCriticalSection(void*);
// @fnv 0x00ec3aff
void __cdecl FUN_00ec3aff(void* criticalSection)
{
    LeaveCriticalSection(criticalSection);
}
