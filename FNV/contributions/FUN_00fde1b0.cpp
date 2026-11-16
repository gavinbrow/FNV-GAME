extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(long volatile*);
extern char* DAT_0126826c;
extern char* DAT_0109b220;
extern "C" void __cdecl FUN_00fde1b0(void)
{
    char* p = DAT_0126826c;
    if (p != DAT_0109b220)
    {
        InterlockedDecrement(reinterpret_cast<long volatile*>(p - 8));
    }
}
