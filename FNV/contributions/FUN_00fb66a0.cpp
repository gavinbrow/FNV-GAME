extern "C" unsigned char g_memoryManager;
extern "C" void __fastcall FUN_00aa3880(void*);
extern "C" void FUN_00fdb290();
extern "C" int __cdecl atexit(void (__cdecl*)());
void FUN_00fb66a0()
{
    FUN_00aa3880(&g_memoryManager);
    atexit(FUN_00fdb290);
}
