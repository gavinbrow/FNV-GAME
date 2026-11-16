extern "C" __declspec(dllimport) void* __stdcall CreateSemaphoreA(void*, long, long, const char*);
extern long DAT_011f4790;
extern long DAT_011f4794;
extern void* DAT_011f4798;
extern "C" void FUN_00fdaf60();
extern "C" int __cdecl atexit(void (__cdecl *)(void));

// @fnv 0x00fb58b0
extern "C" void FUN_00fb58b0()
{
    DAT_011f4790 = 0;
    DAT_011f4794 = 1;
    DAT_011f4798 = CreateSemaphoreA(0, 0, 1, 0);
    atexit(FUN_00fdaf60);
}
