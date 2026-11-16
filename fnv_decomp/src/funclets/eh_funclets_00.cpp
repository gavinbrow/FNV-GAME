// funclets/eh_funclets_00.cpp: 80 EH unwind funclet(s) of the original (Gy sections of functions with unwinding), written as naked asm with real instructions
// and symbolic call targets; replaces the _emit contributions loc_00efe1c0..loc_00f1d460.

extern char DAT_0114eaac;
extern char DAT_01168828;
extern char DAT_011f3318;
void FUN_00401030();
void FUN_00404ee0();
void FUN_004381b0();
void FUN_0045cec0();
void FUN_00483710();
void FUN_004a3bc0();
void FUN_004ad270();
void FUN_004ff7e0();
void FUN_0056d730();
void FUN_0056ea90();
void FUN_006e2620();
void FUN_006ebf90();
void FUN_00800190();
void FUN_009ba610();
void FUN_00aa1460();
void FUN_00c6de10();
void FUN_00ec3d33();
void FUN_00ec408c();

// @fnv 0x00efe1c0
__declspec(naked) void FUN_00efe1c0()
{
    __asm {
        mov eax, dword ptr [ebp - 0x14]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x1c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x24]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x2c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x34]
    }
}

// @fnv 0x00efe1ef
__declspec(naked) void FUN_00efe1ef()
{
    __asm {
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x3c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x44]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x4c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x54]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x5c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x64]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x6c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x74]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x7c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x84]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x8c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x94]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x9c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xa4]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xac]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xb4]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xbc]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xc4]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xcc]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xd4]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xdc]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xe4]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xec]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xf4]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0xfc]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x104]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov eax, dword ptr [ebp - 0x10c]
        push eax
        call FUN_00401030
        pop ecx
        ret
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x184]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_0114eaac
        jmp FUN_00ec3d33
    }
}

// @fnv 0x00f0ff50
__declspec(naked) void FUN_00f0ff50()
{
    __asm {
        push 0x280
        mov eax, dword ptr [ebp - 0x1c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f0ff90
__declspec(naked) void FUN_00f0ff90()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0x2c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f0ffc0
__declspec(naked) void FUN_00f0ffc0()
{
    __asm {
        lea ecx, [ebp - 0x3c]
        jmp FUN_004381b0
        L0008:
        push 0xfc
        mov eax, dword ptr [ebp - 0x44]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10073
__declspec(naked) void FUN_00f10073()
{
    __asm {
        push 0x114
        mov eax, dword ptr [ebp - 0x150]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10088
__declspec(naked) void FUN_00f10088()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0x158]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1009a
__declspec(naked) void FUN_00f1009a()
{
    __asm {
        push 0xfc
        mov eax, dword ptr [ebp - 0x160]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f100d0
__declspec(naked) void FUN_00f100d0()
{
    __asm {
        lea ecx, [ebp - 0x7c]
        jmp FUN_004381b0
        L0008:
        push 0xac
        mov eax, dword ptr [ebp - 0x84]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f100ed
__declspec(naked) void FUN_00f100ed()
{
    __asm {
        push 0x114
        mov eax, dword ptr [ebp - 0x8c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10270
__declspec(naked) void FUN_00f10270()
{
    __asm {
        lea ecx, [ebp - 0x100]
        jmp FUN_004381b0
        L000b:
        lea ecx, [ebp - 0x104]
        jmp FUN_004381b0
        L0016:
        push 0x114
        mov eax, dword ptr [ebp - 0x130]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1029b
__declspec(naked) void FUN_00f1029b()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0x138]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10321
__declspec(naked) void FUN_00f10321()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x1c]
        add ecx, 0x114
        jmp FUN_0045cec0
        L000e:
        mov ecx, dword ptr [ebp - 0x1c]
        add ecx, 0x2c4
        jmp FUN_0045cec0
        L001c:
        mov ecx, dword ptr [ebp - 0x1c]
        add ecx, 0x2cc
        jmp FUN_0045cec0
        L002a:
        push 0x280
        mov eax, dword ptr [ebp - 0x18]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10590
__declspec(naked) void FUN_00f10590()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x28]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f105a2
__declspec(naked) void FUN_00f105a2()
{
    __asm {
        push 0x10
        mov eax, dword ptr [ebp - 0x30]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10680
__declspec(naked) void FUN_00f10680()
{
    __asm {
        push 0x3c
        mov eax, dword ptr [ebp - 0x30]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1068f
__declspec(naked) void FUN_00f1068f()
{
    __asm {
        push 0x6c
        mov eax, dword ptr [ebp - 0x38]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10720
__declspec(naked) void FUN_00f10720()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0xb8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10735
__declspec(naked) void FUN_00f10735()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x108]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10910
__declspec(naked) void FUN_00f10910()
{
    __asm {
        push 0x3c
        mov eax, dword ptr [ebp - 0x80]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10b10
__declspec(naked) void FUN_00f10b10()
{
    __asm {
        push 0xfc
        mov eax, dword ptr [ebp - 0x50]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10ed0
__declspec(naked) void FUN_00f10ed0()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x48]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10ee2
__declspec(naked) void FUN_00f10ee2()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x50]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10ef4
__declspec(naked) void FUN_00f10ef4()
{
    __asm {
        push 0x10
        mov eax, dword ptr [ebp - 0x58]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10f50
__declspec(naked) void FUN_00f10f50()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x3c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f10fa0
__declspec(naked) void FUN_00f10fa0()
{
    __asm {
        lea ecx, [ebp - 0xf0]
        jmp FUN_00c6de10
        L000b:
        push 0x14
        mov eax, dword ptr [ebp - 0xf4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f11790
__declspec(naked) void FUN_00f11790()
{
    __asm {
        lea ecx, [ebp - 0x38]
        jmp FUN_00483710
        L0008:
        push 0xac
        mov eax, dword ptr [ebp - 0x3e4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f11a70
__declspec(naked) void FUN_00f11a70()
{
    __asm {
        push 0x14
        mov eax, dword ptr [ebp - 0x2c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f11b8b
__declspec(naked) void FUN_00f11b8b()
{
    __asm {
        push 0x6c
        mov eax, dword ptr [ebp - 0x70]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f13810
__declspec(naked) void FUN_00f13810()
{
    __asm {
        push 0x74
        mov eax, dword ptr [ebp - 0xb8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f14390
__declspec(naked) void FUN_00f14390()
{
    __asm {
        lea ecx, [ebp - 0x20]
        jmp FUN_00404ee0
        L0008:
        push 0x280
        mov eax, dword ptr [ebp - 0xa0]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f14520
__declspec(naked) void FUN_00f14520()
{
    __asm {
        push 0x74
        mov eax, dword ptr [ebp - 0x33c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f14570
__declspec(naked) void FUN_00f14570()
{
    __asm {
        lea ecx, [ebp - 0x98]
        jmp FUN_00404ee0
        L000b:
        lea ecx, [ebp - 0x12c]
        jmp FUN_004381b0
        L0016:
        lea ecx, [ebp - 0xb4]
        jmp FUN_0045cec0
        L0021:
        push 0x74
        mov eax, dword ptr [ebp - 0x13c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f15280
__declspec(naked) void FUN_00f15280()
{
    __asm {
        push 0x50
        mov eax, dword ptr [ebp - 0x8c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f15292
__declspec(naked) void FUN_00f15292()
{
    __asm {
        push 0x50
        mov eax, dword ptr [ebp - 0x94]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f15340
__declspec(naked) void FUN_00f15340()
{
    __asm {
        lea ecx, [ebp - 0x10]
        jmp FUN_004381b0
        L0008:
        push 0xac
        mov eax, dword ptr [ebp - 0x1dc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1535d
__declspec(naked) void FUN_00f1535d()
{
    __asm {
        lea ecx, [ebp - 0x1e0]
        jmp FUN_004381b0
        L000b:
        lea ecx, [ebp - 0xdc]
        jmp FUN_004ad270
        L0016:
        push 0xac
        mov eax, dword ptr [ebp - 0x280]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f157c0
__declspec(naked) void FUN_00f157c0()
{
    __asm {
        push 0x6c
        mov eax, dword ptr [ebp - 0x1c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f15ae0
__declspec(naked) void FUN_00f15ae0()
{
    __asm {
        lea ecx, [ebp - 0xf0]
        jmp FUN_00c6de10
        L000b:
        push 0x14
        mov eax, dword ptr [ebp - 0xf4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f15c50
__declspec(naked) void FUN_00f15c50()
{
    __asm {
        push 0x3c
        mov eax, dword ptr [ebp - 0x18]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f16260
__declspec(naked) void FUN_00f16260()
{
    __asm {
        lea ecx, [ebp - 0x90]
        jmp FUN_004ff7e0
        L000b:
        lea ecx, [ebp - 0x5c]
        jmp FUN_004ff7e0
        L0013:
        lea ecx, [ebp - 0x98]
        jmp FUN_00800190
        L001e:
        lea ecx, [ebp - 0xa0]
        jmp FUN_00800190
        L0029:
        push 0xb0
        mov eax, dword ptr [ebp - 0xac]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1629e
__declspec(naked) void FUN_00f1629e()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0xb4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f162b0
__declspec(naked) void FUN_00f162b0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0xb8]
        jmp FUN_006ebf90
        L000b:
        mov ecx, dword ptr [ebp - 0xbc]
        jmp FUN_0045cec0
        L0016:
        push 0xb0
        mov eax, dword ptr [ebp - 0xc4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f162db
__declspec(naked) void FUN_00f162db()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0xcc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f163ff
__declspec(naked) void FUN_00f163ff()
{
    __asm {
        lea ecx, [ebp - 0xa0]
        jmp FUN_0056ea90
        L000b:
        push 0x18
        mov eax, dword ptr [ebp - 0xa4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f16a40
__declspec(naked) void FUN_00f16a40()
{
    __asm {
        push 0x18
        mov eax, dword ptr [ebp - 0x1c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1800f
__declspec(naked) void FUN_00f1800f()
{
    __asm {
        lea ecx, [ebp - 0x120]
        jmp FUN_0056d730
        L000b:
        push 0x1c
        mov eax, dword ptr [ebp - 0x128]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f18510
__declspec(naked) void FUN_00f18510()
{
    __asm {
        push 0x10
        mov eax, dword ptr [ebp - 0x274]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f18590
__declspec(naked) void FUN_00f18590()
{
    __asm {
        lea ecx, [ebp - 0x4c0]
        jmp FUN_004a3bc0
        L000b:
        push 0x14
        mov eax, dword ptr [ebp - 0x508]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f18640
__declspec(naked) void FUN_00f18640()
{
    __asm {
        push 0x50
        mov eax, dword ptr [ebp - 0xd4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f18652
__declspec(naked) void FUN_00f18652()
{
    __asm {
        push 0x50
        mov eax, dword ptr [ebp - 0xdc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f18664
__declspec(naked) void FUN_00f18664()
{
    __asm {
        push 0x50
        mov eax, dword ptr [ebp - 0x108]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f197a0
__declspec(naked) void FUN_00f197a0()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x118]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f197b5
__declspec(naked) void FUN_00f197b5()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x120]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f197ca
__declspec(naked) void FUN_00f197ca()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x128]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f197df
__declspec(naked) void FUN_00f197df()
{
    __asm {
        push 0x50
        mov eax, dword ptr [ebp - 0x160]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f197f1
__declspec(naked) void FUN_00f197f1()
{
    __asm {
        lea ecx, [ebp - 0x100]
        jmp FUN_0045cec0
        L000b:
        push 0x1c
        mov eax, dword ptr [ebp - 0x174]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f198c0
__declspec(naked) void FUN_00f198c0()
{
    __asm {
        lea ecx, [ebp - 0x7c]
        jmp FUN_004ff7e0
        L0008:
        push 0x54
        mov eax, dword ptr [ebp - 0xe8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f19b40
__declspec(naked) void FUN_00f19b40()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0x98]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f19b55
__declspec(naked) void FUN_00f19b55()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0xa0]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1aa40
__declspec(naked) void FUN_00f1aa40()
{
    __asm {
        lea ecx, [ebp - 0xa4]
        jmp FUN_004ad270
        L000b:
        push 0xac
        mov eax, dword ptr [ebp - 0xa8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1aa60
__declspec(naked) void FUN_00f1aa60()
{
    __asm {
        push 0x14
        mov eax, dword ptr [ebp - 0xc4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1aa72
__declspec(naked) void FUN_00f1aa72()
{
    __asm {
        push 0x14
        mov eax, dword ptr [ebp - 0xd4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1aa9a
__declspec(naked) void FUN_00f1aa9a()
{
    __asm {
        imul edi, dword ptr [eax + 0x8c483ff], 0xb868c3
        add byte ptr [eax], al
        mov eax, dword ptr [ebp - 0x1d8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1aab6
__declspec(naked) void FUN_00f1aab6()
{
    __asm {
        push 0x40
        mov eax, dword ptr [ebp - 0x200]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1ab20
__declspec(naked) void FUN_00f1ab20()
{
    __asm {
        lea ecx, [ebp - 0x80]
        jmp FUN_0056ea90
        L0008:
        push 0x14
        mov eax, dword ptr [ebp - 0x84]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1ab3a
__declspec(naked) void FUN_00f1ab3a()
{
    __asm {
        push 0x18
        mov eax, dword ptr [ebp - 0x98]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}


// @fnv 0x00f1ae27
__declspec(naked) void FUN_00f1ae27()
{
    __asm {
        lea ecx, [ebp - 0x80]
        jmp FUN_004ad270
        L0008:
        lea ecx, [ebp - 0x620]
        jmp FUN_004a3bc0
        L0013:
        lea ecx, [ebp - 0x650]
        jmp FUN_009ba610
        L001e:
        push 0x10
        mov eax, dword ptr [ebp - 0x764]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1b1a0
__declspec(naked) void FUN_00f1b1a0()
{
    __asm {
        lea ecx, [ebp - 0x190]
        jmp FUN_00c6de10
        L000b:
        push 0x14
        mov eax, dword ptr [ebp - 0x194]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1b1bd
__declspec(naked) void FUN_00f1b1bd()
{
    __asm {
        push 0x14
        mov eax, dword ptr [ebp - 0x1a0]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1b4a0
__declspec(naked) void FUN_00f1b4a0()
{
    __asm {
        push 0xfc
        mov eax, dword ptr [ebp - 0x1c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1b4b2
__declspec(naked) void FUN_00f1b4b2()
{
    __asm {
        push 0xfc
        mov eax, dword ptr [ebp - 0x24]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1b580
__declspec(naked) void FUN_00f1b580()
{
    __asm {
        lea ecx, [ebp - 0xec]
        jmp FUN_006e2620
        L000b:
        lea ecx, [ebp - 0x38]
        jmp FUN_004ff7e0
        L0013:
        push 0x18
        mov eax, dword ptr [ebp - 0x100]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1b830
__declspec(naked) void FUN_00f1b830()
{
    __asm {
        lea ecx, [ebp - 0x244]
        jmp FUN_004ff7e0
        L000b:
        push 0x18
        mov eax, dword ptr [ebp - 0x24c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1ba32
__declspec(naked) void FUN_00f1ba32()
{
    __asm {
        push 0x10c
        mov eax, dword ptr [ebp - 0x98]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1bd00
__declspec(naked) void FUN_00f1bd00()
{
    __asm {
        push 0xb0
        mov eax, dword ptr [ebp - 0x88]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1be22
__declspec(naked) void FUN_00f1be22()
{
    __asm {
        push 0x18
        mov eax, dword ptr [ebp - 0x1ac]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1c2d0
__declspec(naked) void FUN_00f1c2d0()
{
    __asm {
        push 0x18
        mov eax, dword ptr [ebp - 0x2c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1d460
__declspec(naked) void FUN_00f1d460()
{
    __asm {
        mov ecx, offset DAT_011f3318
        jmp FUN_00483710
        L000a:
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x18]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_01168828
        jmp FUN_00ec3d33
    }
}

// @fnv 0x00f1ae0e
void SUB_004381b0();
void SUB_00f1ae26();
__declspec(naked) void FUN_00f1ae0e()
{
    __asm {
        mov eax, dword ptr [ebp - 0x1c]
        and eax, 1
        je SUB_00f1ae26
        and dword ptr [ebp - 0x1c], 0xfffffffe
        lea ecx, [ebp - 0x50]
        jmp SUB_004381b0
        ret
    }
}
