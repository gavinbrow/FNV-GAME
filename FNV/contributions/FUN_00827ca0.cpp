struct FUN_008050d0_shell {
    void FUN_008050d0(BGSLoadFormBuffer*);
};

struct FUN_008579b0_shell {
    void FUN_008579b0(void*, unsigned int);
};

struct FUN_005a9670_shell {
    void FUN_005a9670();
};

struct FUN_00827ca0_shell : ScriptEffect {
    void FUN_00827ca0(BGSLoadFormBuffer* apBuffer);
};

void FUN_00827ca0_shell::FUN_00827ca0(BGSLoadFormBuffer* apBuffer) {
    ((FUN_008050d0_shell*)this)->FUN_008050d0(apBuffer);
    unsigned short count = 0;
    if (g_TESSaveLoadGame->FUN_008df040() >= 0x2a) {
        if (pEffectLocals) {
            count = ((FUN_005a94f0_shell*)pEffectLocals)->FUN_005a94f0();
        }
        ((FUN_008579b0_shell*)g_TESSaveLoadGame)->FUN_008579b0(&count, 2);
    }
    if (g_TESSaveLoadGame->FUN_008df040() < 0x2a) {
        count = 1;
    }
    if (count) {
        ((FUN_005a9670_shell*)pEffectLocals)->FUN_005a9670();
    }
}
