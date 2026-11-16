// funclets/eh_gaps.cpp: 38 unwind funclets of the original whose compiled form never matched (formerly 0xCC holes in the strict build); naked asm with real instructions, symbolic call/jmp targets (SUB_<va>).

// @fnv 0x00f1c650
void SUB_009f9f50();
__declspec(naked) void FUN_00f1c650()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_009f9f50
    }
}

// @fnv 0x00f1c6d0
void SUB_009fabb0();
__declspec(naked) void FUN_00f1c6d0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_009fabb0
    }
}

// @fnv 0x00f1c700
void SUB_009f9f50();
__declspec(naked) void FUN_00f1c700()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_009f9f50
    }
}

// @fnv 0x00f1cc18
void SUB_00483710();
__declspec(naked) void FUN_00f1cc18()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x80]
        jmp SUB_00483710
    }
}

// @fnv 0x00f1df20
void SUB_00aa7830();
__declspec(naked) void FUN_00f1df20()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x1c]
        jmp SUB_00aa7830
    }
}

// @fnv 0x00f1df50
void SUB_00a1bbd0();
__declspec(naked) void FUN_00f1df50()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x14]
        jmp SUB_00a1bbd0
    }
}

// @fnv 0x00f1ee30
void SUB_00aa8a00();
__declspec(naked) void FUN_00f1ee30()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x18]
        jmp SUB_00aa8a00
    }
}

// @fnv 0x00f1ee60
void SUB_00aa8a20();
__declspec(naked) void FUN_00f1ee60()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x18]
        jmp SUB_00aa8a20
    }
}

// @fnv 0x00f1f289
void SUB_00483710();
__declspec(naked) void FUN_00f1f289()
{
    __asm {
        lea ecx, [ebp - 0x34]
        jmp SUB_00483710
    }
}

// @fnv 0x00f220a1
void SUB_00401030();
__declspec(naked) void FUN_00f220a1()
{
    __asm {
        mov eax, dword ptr [ebp - 0x2c]
        push eax
        call SUB_00401030
        pop ecx
        ret
    }
}

// @fnv 0x00f220d7
void SUB_00aa7830();
__declspec(naked) void FUN_00f220d7()
{
    __asm {
        lea ecx, [ebp - 0x4c]
        jmp SUB_00aa7830
    }
}

// @fnv 0x00f223c0
void SUB_00ae8d90();
__declspec(naked) void FUN_00f223c0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x20]
        jmp SUB_00ae8d90
    }
}

// @fnv 0x00f23928
void SUB_0055a2d0();
__declspec(naked) void FUN_00f23928()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x1c]
        add ecx, 8
        jmp SUB_0055a2d0
    }
}

// @fnv 0x00f2393e
void SUB_00483710();
__declspec(naked) void FUN_00f2393e()
{
    __asm {
        lea ecx, [ebp - 0x10]
        jmp SUB_00483710
    }
}

// @fnv 0x00f23ca8
void SUB_00483710();
__declspec(naked) void FUN_00f23ca8()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x30]
        jmp SUB_00483710
    }
}

// @fnv 0x00f24b80
void SUB_00b39460();
__declspec(naked) void FUN_00f24b80()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x54]
        jmp SUB_00b39460
    }
}

// @fnv 0x00f27b30
void SUB_00404ee0();
__declspec(naked) void FUN_00f27b30()
{
    __asm {
        lea ecx, [ebp - 0x10]
        jmp SUB_00404ee0
    }
}

// @fnv 0x00f29180
void SUB_00404ee0();
__declspec(naked) void FUN_00f29180()
{
    __asm {
        lea ecx, [ebp - 0x1048]
        jmp SUB_00404ee0
    }
}

// @fnv 0x00f29340
void SUB_00401030();
__declspec(naked) void FUN_00f29340()
{
    __asm {
        mov eax, dword ptr [ebp - 0xd0]
        push eax
        call SUB_00401030
        pop ecx
        ret
    }
}

// @fnv 0x00f29e39
void SUB_0045cec0();
void SUB_00b66f20();
void SUB_00ba3a00();
__declspec(naked) void FUN_00f29e39()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        add ecx, 0x1f4
        jmp SUB_00b66f20
        mov ecx, dword ptr [ebp - 0x10]
        add ecx, 0x1f8
        jmp SUB_0045cec0
        mov ecx, dword ptr [ebp - 0x10]
        add ecx, 0x200
        jmp SUB_0045cec0
        mov ecx, dword ptr [ebp - 0x10]
        add ecx, 0x204
        jmp SUB_00ba3a00
    }
}

// @fnv 0x00f2af60
void SUB_00404ee0();
__declspec(naked) void FUN_00f2af60()
{
    __asm {
        lea ecx, [ebp - 0xb50]
        jmp SUB_00404ee0
    }
}

// @fnv 0x00f2d6f8
void SUB_00ba3a00();
__declspec(naked) void FUN_00f2d6f8()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x20]
        add ecx, 0x68
        jmp SUB_00ba3a00
    }
}

// @fnv 0x00f2daf0
void SUB_00483710();
__declspec(naked) void FUN_00f2daf0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x24]
        jmp SUB_00483710
    }
}

// @fnv 0x00f2de50
void SUB_00401030();
__declspec(naked) void FUN_00f2de50()
{
    __asm {
        mov eax, dword ptr [ebp - 0x28]
        push eax
        call SUB_00401030
        pop ecx
        ret
    }
}

// @fnv 0x00f2dfe8
void SUB_00c40910();
__declspec(naked) void FUN_00f2dfe8()
{
    __asm {
        lea ecx, [ebp - 0x38]
        jmp SUB_00c40910
    }
}

// @fnv 0x00f30890
void SUB_00b66f20();
__declspec(naked) void FUN_00f30890()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_00b66f20
    }
}

// @fnv 0x00f30df0
void SUB_0059cf00();
__declspec(naked) void FUN_00f30df0()
{
    __asm {
        lea ecx, [ebp - 0x90]
        jmp SUB_0059cf00
    }
}

// @fnv 0x00f311a4
void SUB_00b66f20();
__declspec(naked) void FUN_00f311a4()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x44]
        add ecx, 0x594
        jmp SUB_00b66f20
        mov ecx, dword ptr [ebp - 0x44]
        add ecx, 0x598
        jmp SUB_00b66f20
    }
}

// @fnv 0x00f311d8
void SUB_00c6cca0();
__declspec(naked) void FUN_00f311d8()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x44]
        add ecx, 0x60c
        jmp SUB_00c6cca0
        mov ecx, dword ptr [ebp - 0x44]
        add ecx, 0x630
        jmp SUB_00c6cca0
        mov ecx, dword ptr [ebp - 0x44]
        add ecx, 0x638
        jmp SUB_00c6cca0
    }
}

// @fnv 0x00f316b0
void SUB_00629b40();
__declspec(naked) void FUN_00f316b0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_00629b40
    }
}

// @fnv 0x00f316e0
void SUB_00c7b0f0();
__declspec(naked) void FUN_00f316e0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_00c7b0f0
    }
}

// @fnv 0x00f31a7e
void SUB_0045cec0();
__declspec(naked) void FUN_00f31a7e()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x24]
        add ecx, 0x250
        jmp SUB_0045cec0
    }
}

// @fnv 0x00f33170
void SUB_00ca9900();
__declspec(naked) void FUN_00f33170()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_00ca9900
    }
}

// @fnv 0x00f33480
void SUB_00c8cd00();
__declspec(naked) void FUN_00f33480()
{
    __asm {
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call SUB_00c8cd00
        pop ecx
        ret
    }
}

// @fnv 0x00f33580
void SUB_00404ee0();
__declspec(naked) void FUN_00f33580()
{
    __asm {
        lea ecx, [ebp - 0x5c]
        jmp SUB_00404ee0
    }
}

// @fnv 0x00f34080
void SUB_009ba5f0();
__declspec(naked) void FUN_00f34080()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_009ba5f0
    }
}

// @fnv 0x00f340b0
void SUB_00cc9410();
__declspec(naked) void FUN_00f340b0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        jmp SUB_00cc9410
    }
}

// @fnv 0x00f344e0
void SUB_00404ee0();
__declspec(naked) void FUN_00f344e0()
{
    __asm {
        lea ecx, [ebp - 0x80]
        jmp SUB_00404ee0
    }
}
