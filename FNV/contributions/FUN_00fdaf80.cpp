// @fnv 0x00fdaf80
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
extern "C" const char* DAT_0109b220;
struct NiFixedStringEntry { const char* data; };
extern "C" NiFixedStringEntry DAT_011f49d8;
void FUN_00fdaf80()
{
    NiFixedStringEntry* item = &DAT_011f49d8;
    for (int remaining = 9; remaining >= 0; --remaining)
    {
        const char* str = (--item)->data;
        if (str != DAT_0109b220)
        {
            InterlockedDecrement(reinterpret_cast<volatile long*>(const_cast<char*>(str)) - 2);
        }
    }
}