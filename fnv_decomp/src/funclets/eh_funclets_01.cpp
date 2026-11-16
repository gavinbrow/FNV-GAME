// funclets/eh_funclets_01.cpp: 80 EH unwind funclet(s) of the original (Gy sections of functions with unwinding), written as naked asm with real instructions
// and symbolic call targets; replaces the _emit contributions loc_00f1d5ba..loc_00f29852.

extern char DAT_01168a30;
extern char DAT_01168a74;
extern char DAT_01168d0c;
extern char DAT_01168d50;
extern char DAT_0116902c;
extern char DAT_0116edf4;
extern char DAT_0116f380;
extern char DAT_01170ad4;
extern char DAT_01174f84;
extern char DAT_011f8190;
extern char DAT_011f8194;
extern char DAT_011f8bdc;
void FUN_004037d0();
void FUN_00404ee0();
void FUN_0040fbe0();
void FUN_004381b0();
void FUN_00449680();
void FUN_0045cec0();
void FUN_00483710();
void FUN_00a11d00();
void FUN_00a1bbd0();
void FUN_00a1bc20();
void FUN_00a22640();
void FUN_00aa1460();
void FUN_00aa7830();
void FUN_00acb6b0();
void FUN_00afc720();
void FUN_00b0e1a0();
void FUN_00b66f20();
void FUN_00b998f0();
void FUN_00ec3d33();
void FUN_00ec408c();
void FUN_00ec5fce();

// @fnv 0x00f1d5ba
__declspec(naked) void FUN_00f1d5ba()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x88]
        add ecx, 0x2264
        jmp FUN_00a1bc20
        L0011:
        mov ecx, dword ptr [ebp - 0x88]
        add ecx, 0x2270
        jmp FUN_00a11d00
        L0022:
        mov ecx, dword ptr [ebp - 0x84]
        jmp FUN_00aa7830
    }
}

// @fnv 0x00f1d6a4
__declspec(naked) void FUN_00f1d6a4()
{
    __asm {
        lea ecx, [ebp - 0x38]
        jmp FUN_004037d0
        L0008:
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x124]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_01168a30
        jmp FUN_00ec3d33
        L0026:
        push 0xb4
        mov eax, dword ptr [ebp - 0x80]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1d6dc
__declspec(naked) void FUN_00f1d6dc()
{
    __asm {
        lea ecx, [ebp - 0x84]
        jmp FUN_004381b0
        L000b:
        lea ecx, [ebp - 0x44]
        jmp FUN_004037d0
        L0013:
        push 0x1c
        mov eax, dword ptr [ebp - 0xfc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1d701
__declspec(naked) void FUN_00f1d701()
{
    __asm {
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x190]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_01168a74
        jmp FUN_00ec3d33
        L001e:
        push 0xb4
        mov eax, dword ptr [ebp - 0x9c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1d734
__declspec(naked) void FUN_00f1d734()
{
    __asm {
        lea ecx, [ebp - 0xa0]
        jmp FUN_004381b0
        L000b:
        push 0xb4
        mov eax, dword ptr [ebp - 0xa8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1d754
__declspec(naked) void FUN_00f1d754()
{
    __asm {
        lea ecx, [ebp - 0xac]
        jmp FUN_004381b0
        L000b:
        push 0x20
        mov eax, dword ptr [ebp - 0xb4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1d771
__declspec(naked) void FUN_00f1d771()
{
    __asm {
        lea ecx, [ebp - 0x54]
        jmp FUN_004037d0
        L0008:
        push 0x1c
        mov eax, dword ptr [ebp - 0x12c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1da18
__declspec(naked) void FUN_00f1da18()
{
    __asm {
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0xac]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_01168d0c
        jmp FUN_00ec3d33
        L001e:
        push 0xd4
        mov eax, dword ptr [ebp - 0x264]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1da4b
__declspec(naked) void FUN_00f1da4b()
{
    __asm {
        lea ecx, [ebp - 0x268]
        jmp FUN_004381b0
        L000b:
        push 0xb0
        mov eax, dword ptr [ebp - 0x270]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1da6b
__declspec(naked) void FUN_00f1da6b()
{
    __asm {
        lea ecx, [ebp - 0x274]
        jmp FUN_004381b0
        L000b:
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x2d0]
        xor ecx, eax
        call FUN_00ec408c
        mov ecx, dword ptr [edx - 4]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_01168d50
        jmp FUN_00ec3d33
        L0033:
        lea ecx, [ebp - 0x10]
        jmp FUN_00404ee0
        L003b:
        push 0x74
        mov eax, dword ptr [ebp - 0x174]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1dab8
__declspec(naked) void FUN_00f1dab8()
{
    __asm {
        push 0x30
        mov eax, dword ptr [ebp - 0x17c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1ddad
__declspec(naked) void FUN_00f1ddad()
{
    __asm {
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x180]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_0116902c
        jmp FUN_00ec3d33
        L001e:
        lea ecx, [ebp + 8]
        jmp FUN_004037d0
        L0026:
        lea ecx, [ebp - 0x38]
        jmp FUN_0045cec0
        L002e:
        push 0xd4
        mov eax, dword ptr [ebp - 0xc4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1ddf0
__declspec(naked) void FUN_00f1ddf0()
{
    __asm {
        push 0xb0
        mov eax, dword ptr [ebp - 0xcc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1e589
__declspec(naked) void FUN_00f1e589()
{
    __asm {
        push 0xd4
        mov eax, dword ptr [ebp - 0x98]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1e59e
__declspec(naked) void FUN_00f1e59e()
{
    __asm {
        push 0xc4
        mov eax, dword ptr [ebp - 0xa0]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1e5b3
__declspec(naked) void FUN_00f1e5b3()
{
    __asm {
        lea ecx, [ebp - 0xa4]
        jmp FUN_004381b0
        L000b:
        push 0xb0
        mov eax, dword ptr [ebp - 0xac]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1e5d3
__declspec(naked) void FUN_00f1e5d3()
{
    __asm {
        push 0xac
        mov eax, dword ptr [ebp - 0xb4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1e5e8
__declspec(naked) void FUN_00f1e5e8()
{
    __asm {
        lea ecx, [ebp - 0xb8]
        jmp FUN_004381b0
        L000b:
        push 0x14
        mov eax, dword ptr [ebp - 0xc0]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1e730
__declspec(naked) void FUN_00f1e730()
{
    __asm {
        lea ecx, [ebp - 0x14]
        jmp FUN_004037d0
        L0008:
        push 0xac
        mov eax, dword ptr [ebp - 0xbc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1e74d
__declspec(naked) void FUN_00f1e74d()
{
    __asm {
        lea ecx, [ebp - 0xac]
        jmp FUN_00a22640
        L000b:
        push 0xac
        mov eax, dword ptr [ebp - 0xdc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1e76d
__declspec(naked) void FUN_00f1e76d()
{
    __asm {
        push 0x14
        mov eax, dword ptr [ebp - 0xfc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f1f540
__declspec(naked) void FUN_00f1f540()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x88]
        jmp FUN_00449680
    }
}

// @fnv 0x00f20cd0
__declspec(naked) void FUN_00f20cd0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0xbc]
        jmp FUN_00acb6b0
    }
}

// @fnv 0x00f215c0
__declspec(naked) void FUN_00f215c0()
{
    __asm {
        mov eax, dword ptr [ebp - 0x18]
        push eax
        mov ecx, dword ptr [ebp - 0x20]
        push ecx
        call FUN_0040fbe0
        add esp, 8
        ret
    }
}

// @fnv 0x00f21dcc
__declspec(naked) void FUN_00f21dcc()
{
    __asm {
        push offset FUN_00a1bbd0
        push 2
        push 0xc
        mov eax, dword ptr [ebp - 0x58]
        add eax, 0xc
        push eax
        call FUN_00ec5fce
        ret
    }
}

// @fnv 0x00f23180
__declspec(naked) void FUN_00f23180()
{
    __asm {
        lea ecx, [ebp - 0x360]
        jmp FUN_00afc720
        L000b:
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x3ac]
        xor ecx, eax
        call FUN_00ec408c
        mov ecx, dword ptr [edx - 8]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_0116edf4
        jmp FUN_00ec3d33
        L0033:
        push 0x1d0
        mov eax, dword ptr [ebp - 0x240]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f236d0
__declspec(naked) void FUN_00f236d0()
{
    __asm {
        mov ecx, offset DAT_011f8190
        jmp FUN_00afc720
        L000a:
        push offset FUN_00afc720
        push 8
        push 4
        push offset DAT_011f8194
        call FUN_00ec5fce
        ret
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 8]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_0116f380
        jmp FUN_00ec3d33
    }
}

// @fnv 0x00f24530
__declspec(naked) void FUN_00f24530()
{
    __asm {
        mov ecx, offset DAT_011f8bdc
        jmp FUN_00b0e1a0
        L000a:
        mov ecx, offset DAT_011f8bdc
        jmp FUN_00483710
        L0014:
        mov edx, dword ptr [esp + 8]
        lea eax, [edx + 0xc]
        mov ecx, dword ptr [edx - 0x24]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_01170ad4
        jmp FUN_00ec3d33
    }
}

// @fnv 0x00f26cf0
__declspec(naked) void FUN_00f26cf0()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26d30
__declspec(naked) void FUN_00f26d30()
{
    __asm {
        push 0xe4
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26d60
__declspec(naked) void FUN_00f26d60()
{
    __asm {
        push 0xe4
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26d90
__declspec(naked) void FUN_00f26d90()
{
    __asm {
        push 0x64
        mov eax, dword ptr [ebp + 4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26dc0
__declspec(naked) void FUN_00f26dc0()
{
    __asm {
        push 0x14
        mov eax, dword ptr [ebp - 0x16c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26e70
__declspec(naked) void FUN_00f26e70()
{
    __asm {
        push 0x74
        mov eax, dword ptr [ebp - 0x1e8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26e82
__declspec(naked) void FUN_00f26e82()
{
    __asm {
        lea ecx, [ebp - 0x1b4]
        jmp FUN_00b66f20
        L000b:
        push 0x74
        mov eax, dword ptr [ebp - 0x1e8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26e9f
__declspec(naked) void FUN_00f26e9f()
{
    __asm {
        lea ecx, [ebp - 0x1a4]
        jmp FUN_00b66f20
        L000b:
        lea ecx, [ebp - 0x1e0]
        jmp FUN_004381b0
        L0016:
        push 0x74
        mov eax, dword ptr [ebp - 0x1e0]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26ec7
__declspec(naked) void FUN_00f26ec7()
{
    __asm {
        lea ecx, [ebp - 0x1d8]
        jmp FUN_00b66f20
        L000b:
        lea ecx, [ebp - 0x1e0]
        jmp FUN_004381b0
        L0016:
        push 0x74
        mov eax, dword ptr [ebp - 0x1e0]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26eef
__declspec(naked) void FUN_00f26eef()
{
    __asm {
        lea ecx, [ebp - 0x1a0]
        jmp FUN_00b66f20
        L000b:
        lea ecx, [ebp - 0x1d4]
        jmp FUN_004381b0
        L0016:
        push 0x74
        mov eax, dword ptr [ebp - 0x1d4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26f17
__declspec(naked) void FUN_00f26f17()
{
    __asm {
        lea ecx, [ebp - 0x1d4]
        jmp FUN_004381b0
        L000b:
        push 0x74
        mov eax, dword ptr [ebp - 0x1d4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}


// @fnv 0x00f26f9e
__declspec(naked) void FUN_00f26f9e()
{
    __asm {
        push 0x74
        mov eax, dword ptr [ebp - 0x1c8]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26fb0
__declspec(naked) void FUN_00f26fb0()
{
    __asm {
        lea ecx, [ebp - 0x1b0]
        jmp FUN_00b66f20
        L000b:
        lea ecx, [ebp - 0x1cc]
        jmp FUN_004381b0
        L0016:
        push 0x74
        mov eax, dword ptr [ebp - 0x1cc]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f2705f
__declspec(naked) void FUN_00f2705f()
{
    __asm {
        push 0x280
        mov eax, dword ptr [ebp - 0x20]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f271f0
__declspec(naked) void FUN_00f271f0()
{
    __asm {
        push 0x8c
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f272d4
__declspec(naked) void FUN_00f272d4()
{
    __asm {
        push 0x5c
        mov eax, dword ptr [ebp - 0x6ec]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f272f4
__declspec(naked) void FUN_00f272f4()
{
    __asm {
        push 0x54
        mov eax, dword ptr [ebp - 0x73c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f27306
__declspec(naked) void FUN_00f27306()
{
    __asm {
        lea ecx, [ebp - 0x730]
        jmp FUN_0045cec0
        L000b:
        push 0x1c
        mov eax, dword ptr [ebp - 0x73c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f27323
__declspec(naked) void FUN_00f27323()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0x73c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f27580
__declspec(naked) void FUN_00f27580()
{
    __asm {
        lea ecx, [ebp - 0x24]
        jmp FUN_00404ee0
        L0008:
        push 0x140
        mov eax, dword ptr [ebp - 0x1c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f27640
__declspec(naked) void FUN_00f27640()
{
    __asm {
        push 0xfc
        mov eax, dword ptr [ebp + 4]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f27dd0
__declspec(naked) void FUN_00f27dd0()
{
    __asm {
        mov ecx, dword ptr [ebp - 0x10]
        add ecx, 0x20
        jmp FUN_00b998f0
    }
}

// @fnv 0x00f27eac
__declspec(naked) void FUN_00f27eac()
{
    __asm {
        push 0x5c
        mov eax, dword ptr [ebp - 0x784]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f27ecc
__declspec(naked) void FUN_00f27ecc()
{
    __asm {
        push 0x54
        mov eax, dword ptr [ebp - 0x784]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f27ede
__declspec(naked) void FUN_00f27ede()
{
    __asm {
        lea ecx, [ebp - 0x774]
        jmp FUN_0045cec0
        L000b:
        push 0x1c
        mov eax, dword ptr [ebp - 0x784]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f27efb
__declspec(naked) void FUN_00f27efb()
{
    __asm {
        push 0x1c
        mov eax, dword ptr [ebp - 0x784]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f284c0
__declspec(naked) void FUN_00f284c0()
{
    __asm {
        push 0x2c
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f28725
__declspec(naked) void FUN_00f28725()
{
    __asm {
        mov edx, dword ptr [esp + 8]
        lea eax, [edx - 0x14]
        mov ecx, dword ptr [edx - 0x18]
        xor ecx, eax
        call FUN_00ec408c
        mov eax, offset DAT_01174f84
        jmp FUN_00ec3d33
        L001b:
        push 0x40
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f28b80
__declspec(naked) void FUN_00f28b80()
{
    __asm {
        push 0x80
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f28bb0
__declspec(naked) void FUN_00f28bb0()
{
    __asm {
        push 0x80
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f28e30
__declspec(naked) void FUN_00f28e30()
{
    __asm {
        push 0x44
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f28e3f
__declspec(naked) void FUN_00f28e3f()
{
    __asm {
        push 0x44
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f28e4e
__declspec(naked) void FUN_00f28e4e()
{
    __asm {
        push 0x44
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f28e5d
__declspec(naked) void FUN_00f28e5d()
{
    __asm {
        push 0x44
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f29010
__declspec(naked) void FUN_00f29010()
{
    __asm {
        push 0x84
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f29290
__declspec(naked) void FUN_00f29290()
{
    __asm {
        lea ecx, [ebp - 0x14]
        jmp FUN_00404ee0
        L0008:
        push 0x250
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f2934e
__declspec(naked) void FUN_00f2934e()
{
    __asm {
        push 0xc4
        mov eax, dword ptr [ebp - 0xd0]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f29400
__declspec(naked) void FUN_00f29400()
{
    __asm {
        push 0xf0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f294e0
__declspec(naked) void FUN_00f294e0()
{
    __asm {
        push 0x70
        mov eax, dword ptr [ebp - 0x1c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f294ef
__declspec(naked) void FUN_00f294ef()
{
    __asm {
        push 0xc4
        mov eax, dword ptr [ebp - 0x1c]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f29530
__declspec(naked) void FUN_00f29530()
{
    __asm {
        lea ecx, [ebp - 0x2c]
        jmp FUN_00404ee0
        L0008:
        push 0x70
        mov eax, dword ptr [ebp - 0x20]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}


// @fnv 0x00f297c2
__declspec(naked) void FUN_00f297c2()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f297d4
__declspec(naked) void FUN_00f297d4()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f297e6
__declspec(naked) void FUN_00f297e6()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f297f8
__declspec(naked) void FUN_00f297f8()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f2980a
__declspec(naked) void FUN_00f2980a()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f2981c
__declspec(naked) void FUN_00f2981c()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f2982e
__declspec(naked) void FUN_00f2982e()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f29840
__declspec(naked) void FUN_00f29840()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f29852
__declspec(naked) void FUN_00f29852()
{
    __asm {
        push 0xd0
        mov eax, dword ptr [ebp - 0x10]
        push eax
        call FUN_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f26f3f
void SUB_004381b0();
void SUB_00aa1460();
__declspec(naked) void FUN_00f26f3f()
{
    __asm {
        lea ecx, [ebp - 0x1c4]
        jmp SUB_004381b0
        push 0x74
        mov eax, dword ptr [ebp - 0x1c4]
        push eax
        call SUB_00aa1460
        add esp, 8
        ret
    }
}

// @fnv 0x00f2954f
void SUB_004381b0();
void SUB_00aa1460();
__declspec(naked) void FUN_00f2954f()
{
    __asm {
        push 0xc4
        mov eax, dword ptr [ebp - 0x20]
        push eax
        call SUB_00aa1460
        add esp, 8
        ret
        lea ecx, [ebp + 8]
        jmp SUB_004381b0
    }
}
