// @fnv 0x00cb26e0
void FUN_00cb2550();
__declspec(naked) void FUN_00cb26e0()
{
    __asm {
        push esi
        mov esi, [esp+8]
        push ecx
        call FUN_00cb2550
        add esp, 4
        pop esi
        ret 4
    }
}
