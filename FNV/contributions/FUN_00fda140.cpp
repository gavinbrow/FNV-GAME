extern "C" __declspec(dllimport) void __stdcall DeleteCriticalSection(void*);
extern "C" int DAT_011f3330;
extern "C" void FUN_00fda140() {
    DeleteCriticalSection(&DAT_011f3330);
}