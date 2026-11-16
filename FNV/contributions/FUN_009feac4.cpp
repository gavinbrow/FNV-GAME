// @fnv 0x009feac4
extern char DAT_011a6228;
extern char DAT_011a6230;
__declspec(naked) void FUN_009feac4()
{
    __asm {
        jmp dword ptr [DAT_011a6228]
        jmp dword ptr [DAT_011a6230]
    }
}
