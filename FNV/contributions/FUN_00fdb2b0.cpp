extern "C" __declspec(dllimport) void __stdcall DeleteCriticalSection(void*);
extern "C" int DAT_011f6bd4;
extern "C" void FUN_00fdb2b0() {
    DeleteCriticalSection(&DAT_011f6bd4);
}