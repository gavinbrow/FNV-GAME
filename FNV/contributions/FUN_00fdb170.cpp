// @fnv 0x00fdb170
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" const char* DAT_0109b220;
struct NiRTTI { const char* data; };
extern NiRTTI g_011f5eac;
void FUN_00fdb170()
{
    NiRTTI* item = &g_011f5eac;
    for (int remaining = 3; remaining >= 0; --remaining)
    {
        const char* str = (--item)->data;
        if (str != DAT_0109b220)
        {
            InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(str)) - 2);
        }
    }
}