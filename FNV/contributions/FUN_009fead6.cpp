// @fnv 0x009fead6
extern char DAT_011a6240;
extern char DAT_011a6248;
__declspec(naked) void FUN_009fead6()
{
    __asm {
        jmp dword ptr [DAT_011a6240]
        jmp dword ptr [DAT_011a6248]
    }
}
