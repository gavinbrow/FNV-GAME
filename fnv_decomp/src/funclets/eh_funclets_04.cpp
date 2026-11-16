// funclets/eh_funclets_04.cpp: 9 EH unwind funclet(s) of the original (Gy sections of functions with unwinding), written as naked asm with real instructions
// and symbolic call targets; replaces the _emit contributions loc_00f33805..loc_00f34d95.

extern char DAT_0117fb00;
extern char DAT_0117fb2c;
extern char DAT_0117fb58;
extern char DAT_0117fb8c;
extern char DAT_0117fbc0;
extern char DAT_0117fbec;
extern char DAT_01180090;
void FUN_00401030();
void FUN_00404ee0();
void FUN_0044a540();
void FUN_0066da50();
void FUN_00aa1460();
void FUN_00aca4b0();
void FUN_00b3c910();
void FUN_00c7fb40();
void FUN_00cce290();
void FUN_00ec330b();
void FUN_00ec3d33();
void FUN_00ec408c();

// @fnv 0x00f33805
__declspec(naked) void FUN_00f33805()
{
    __asm {
        push 0x10
        mov eax, dword ptr [ebp - 0x40]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f33814
__declspec(naked) void FUN_00f33814()
{
    __asm {
        push 0x10
        mov eax, dword ptr [ebp - 0x40]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f33823
__declspec(naked) void FUN_00f33823()
{
    __asm {
        push 0x10
        mov eax, dword ptr [ebp - 0x40]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f33dd0
__declspec(naked) void FUN_00f33dd0()
{
    __asm {
        push 0x10
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f33f90
__declspec(naked) void FUN_00f33f90()
{
    __asm {
        lea ecx, [ebp - 0x40]
        jmp FUN_00404ee0
        L0008:
        lea ecx, [ebp - 0x28]
        jmp FUN_00c7fb40
        L0010:
        lea ecx, [ebp - 0x3c]
        jmp FUN_00c7fb40
        L0018:
        push 0x10
        mov eax, dword ptr [ebp + 8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f33fb7
__declspec(naked) void FUN_00f33fb7()
{
    __asm {
        push 0x10
        mov eax, dword ptr [ebp + 8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f34550
__declspec(naked) void FUN_00f34550()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        add ecx, 8
        jmp FUN_0066da50
    }
}

// @fnv 0x00f347c0
__declspec(naked) void FUN_00f347c0()
{
    __asm {
        lea ecx, [ebp - 0x30]
        jmp FUN_00404ee0
        L0008:
        lea ecx, [ebp - 0x2c]
        jmp FUN_00cce290
        L0010:
        push 0x14
        mov eax, dword ptr [ebp + 4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

extern char PTR_0117fb00;
extern char PTR_0117fb2c;
extern char PTR_0117fb58;
extern char PTR_0117fb8c;
extern char PTR_0117fbc0;
extern char PTR_0117fbec;
extern char PTR_01180090;
// @fnv 0x00f34d95
void SUB_00401030();
void SUB_0044a540();
void SUB_00aca4b0();
void SUB_00b3c910();
void SUB_00ec330b();
void SUB_00ec3d33();
void SUB_00ec408c();
void SUB_00f34e74();
__declspec(naked) void FUN_00f34d95()
{
    __asm {
        lea ecx, [ebp - 0x28]
        jmp SUB_0044a540
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x54]
        xor ecx, eax
        call SUB_00ec408c
        mov eax, offset PTR_0117fb00
        jmp SUB_00ec3d33
        lea ecx, [ebp - 0x10]
        jmp SUB_00ec330b
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x14]
        xor ecx, eax
        call SUB_00ec408c
        mov eax, offset PTR_0117fb2c
        jmp SUB_00ec3d33
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_00b3c910
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x14]
        xor ecx, eax
        call SUB_00ec408c
        mov eax, offset PTR_0117fb58
        jmp SUB_00ec3d33
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_00b3c910
        mov ecx, dword ptr [ebp - 0x10]
        add ecx, 0x18
        jmp SUB_0044a540
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x14]
        xor ecx, eax
        call SUB_00ec408c
        mov eax, offset PTR_0117fb8c
        jmp SUB_00ec3d33
        lea ecx, [ebp - 0x10]
        jmp SUB_00ec330b
        push dword ptr [ebp - 0x14]
        call SUB_00401030
        pop ecx
        ret
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x18]
        xor ecx, eax
        call SUB_00ec408c
        mov eax, offset PTR_0117fbc0
        jmp SUB_00ec3d33
        mov eax, dword ptr [ebp - 0x10]
        and eax, 1
        je SUB_00f34e74
        and dword ptr [ebp - 0x10], 0xfffffffe
        mov ecx, dword ptr [ebp - 0x14]
        add ecx, 4
        jmp SUB_00aca4b0
        ret
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x18]
        xor ecx, eax
        call SUB_00ec408c
        mov eax, offset PTR_0117fbec
        jmp SUB_00ec3d33
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x14]
        xor ecx, eax
        call SUB_00ec408c
        mov eax, offset PTR_01180090
        jmp SUB_00ec3d33
    }
}
