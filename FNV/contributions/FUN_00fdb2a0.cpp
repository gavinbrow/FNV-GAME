extern "C" __declspec(dllimport) void __stdcall DeleteCriticalSection(void*);
extern "C" int DAT_011f6bb8;

// @fnv 0x00fdb2a0
void FUN_00fdb2a0()
{
    DeleteCriticalSection(&DAT_011f6bb8);
}
