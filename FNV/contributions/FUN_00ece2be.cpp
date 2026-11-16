// @fnv 0x00ece2be
__declspec(naked) void FUN_00ece2be()
{
    __asm {
        mov ecx, [ebp-0Ch]
        mov fs:[0], ecx
        pop ecx
        pop edi
        pop edi
        pop esi
        pop ebx
        mov esp, ebp
        pop ebp
        push ecx
        ret
    }
}
