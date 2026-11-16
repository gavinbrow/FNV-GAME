// @fnv 0x009fea2a
namespace fnv_004da670 {
    __declspec(dllimport) void* __stdcall IMP_fdf0b0(const char*);
    __declspec(dllimport) void* __stdcall IMP_fdf0ac(void*, const char*);
}
extern int DAT_011a621c, DAT_011a6220, DAT_011a6224;
extern char DAT_01273000, DAT_0127300a, DAT_0150e828;
extern void* DAT_011a6228[];
__declspec(naked) int __cdecl FUN_009fea2a()
{
    __asm {
        cmp DAT_011a621c, 0
        je L1
        xor eax, eax
        ret
    L1:
        pushad
        push offset DAT_01273000
        call dword ptr [fnv_004da670::IMP_fdf0b0]
        test eax, eax
        mov esi, eax
        mov DAT_011a6220, -2
        je Ldone
        push offset DAT_0127300a
        push esi
        call dword ptr [fnv_004da670::IMP_fdf0ac]
        test eax, eax
        je Lfail
        mov ebp, eax
        push offset DAT_0150e828
        call ebp
        pop ebx
        test eax, eax
        je Lfail
        call eax
        test eax, eax
        js Lfail
        mov DAT_011a6220, 0
        mov DAT_011a6224, -3
        mov esi, offset DAT_011a6228
    Lloop:
        mov eax, [esi+4]
        test eax, eax
        je Ldone
        push eax
        call ebp
        pop ebx
        test eax, eax
        je Lskip
        mov [esi], eax
    Lskip:
        add esi, 8
        jmp Lloop
    Lfail:
        mov DAT_011a6220, -1
    Ldone:
        popad
        mov eax, DAT_011a6220
        test eax, eax
        jne Lret
        mov DAT_011a621c, 1
    Lret:
        ret
    }
}
