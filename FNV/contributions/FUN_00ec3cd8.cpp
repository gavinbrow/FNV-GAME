// @fnv 0x00ec3cd8
__declspec(naked) void FUN_00ec3cd8()
{
    __asm {
        pop eax
        pop ecx
        xchg eax, [esp]
        jmp eax
    }
}
