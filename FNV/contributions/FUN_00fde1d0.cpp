extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
extern char* DAT_01268290;
extern char* DAT_0109b220;
extern "C" void __cdecl FUN_00fde1d0(void)
{
    char* p = DAT_01268290;
    if (p != DAT_0109b220)
    {
        InterlockedDecrement(reinterpret_cast<long volatile*>(p - 8));
    }
}
