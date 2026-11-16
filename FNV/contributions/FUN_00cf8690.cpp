// @fnv 0x00cf8690
struct R { unsigned a,b,c,d; };
__declspec(naked) void __cdecl FUN_00cf8690(R* dst, const R* src)
{
    __asm {
        push esi
        mov esi, [esp+0Ch]
        push edi
        mov edi, [esp+0Ch]
        lea ecx, [esi+0Ch]
        mov edx, 2
        lea eax, [edi+8]
        sub esi, edi
    L1:
        mov edi, [ecx-0Ch]
        mov [eax-8], edi
        mov edi, [ecx-8]
        mov [eax-4], edi
        mov edi, [esi+eax]
        mov [eax], edi
        mov edi, [ecx]
        mov [eax+4], edi
        dec edx
        add ecx, 10h
        add eax, 10h
        test edx, edx
        jg L1
        pop edi
        pop esi
        ret
    }
}
