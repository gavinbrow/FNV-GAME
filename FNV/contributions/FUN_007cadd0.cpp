// Candidate for FUN_007cadd0 (FNV decompilation, official checker)

// __thiscall, no stack args (caller pops 0). /Od /Oy- /GS /EHsc.

// Based on an unverified GLM (Z.ai) / zai_glm_01 draft, round 4.
// Corrected and officially checked by gpt-6 / gpt6_fnv_20261023_1512_c9.



struct G_011dea10_cls {

    void FUN_004568c0(char* a, int* b, int c, int d);

};



extern G_011dea10_cls* g_011dea10;



void __cdecl FUN_00406d00(char* dst, int size, const char* a, const char* b, const char* c, ...);

void __cdecl FUN_00406d30(char* dst, int n, const char* src);

void __cdecl FUN_004b7240(char* src, char* dst, int n);

bool __cdecl FUN_00709d40();



extern const char str_01074c4c[];

extern const char str_01076cc0[];

extern const char str_01074c6c[];

extern const char str_01076ca4[];

extern const char str_01074c40[];

extern const char str_0101fd1c[];

extern const char str_0101fd24[];

extern const char str_01074c38[];

extern const char str_01074c24[];

extern const char str_01074c08[];

extern const char str_01074c1c[];

extern const char str_01074c14[];

extern const char str_01074c00[];

extern const char str_01074bf8[];

extern const char str_01074be8[];

extern const char str_01074bd8[];

extern const char str_01074bc8[];

extern const char str_01074bb8[];

extern const char str_01076c94[];



struct FUN_007cadd0_self {

    int unk_000;

    int unk_004;

    int unk_008;

    int unk_00c;

    int unk_010;

    int unk_014;

    int unk_018;

    int unk_01c;

    int unk_020;

    int unk_024;

    int unk_028;

    int unk_02c;

    int unk_030;

    int unk_034;

    int unk_038;

    int unk_03c;

    int unk_040;

    int unk_044;

    int unk_048;

    int unk_04c;

    int unk_050;

    int unk_054;

    int unk_058;

    int unk_05c;

    int unk_060;

    int unk_064;

    int unk_068;

    int unk_06c;

    int unk_070;

    int unk_074;

    int unk_078;

    int unk_07c;

    int unk_080;

    int unk_084;

    int unk_088;

    int unk_08c;

    int unk_090;

    int unk_094;

    int unk_098;

    int unk_09c;

    int unk_0a0;

    int unk_0a4;

    int unk_0a8;

    int unk_0ac;

    int unk_0b0;

    int unk_0b4;

    int unk_0b8;

    int unk_0bc;

    int unk_0c0;

    int unk_0c4;

    int unk_0c8;

    int unk_0cc;

    int unk_0d0;

    int unk_0d4;

    int unk_0d8;

    int unk_0dc;

    int unk_0e0;

    int unk_0e4;

    int unk_0e8;

    int unk_0ec;

    int unk_0f0;

    int unk_0f4;

    int unk_0f8;

    int unk_0fc;

    int unk_100;

    int unk_104;

    int unk_108;

    int unk_10c;

    int unk_110;

    int unk_114;

    int unk_118;

    int unk_11c;

    int unk_120;

    int unk_124;

    int unk_128;

    int unk_12c;

    int unk_130;

    int unk_134;

    int unk_138;

    int unk_13c;

    int unk_140;

    int unk_144;

    int unk_148;

    int unk_14c;

    int unk_150;

    int unk_154;

    int unk_158;

    int unk_15c;

    int unk_160;

    int unk_164;

    int unk_168;

    int unk_16c;

    int unk_170;

    int unk_174;

    int unk_178;

    int unk_17c;

    int m180[10];   // 0x180

    int m1a8[5];    // 0x1a8

    int m1bc;       // 0x1bc

    int m1c0;       // 0x1c0

    int m1c4;       // 0x1c4

    int m1c8;       // 0x1c8

    int m1cc;       // 0x1cc

    int m1d0;       // 0x1d0

    int m1d4;       // 0x1d4

    int m1d8;       // 0x1d8

    int m1dc;       // 0x1dc

    int m1e0;       // 0x1e0

    void FUN_007cadd0();

};



void FUN_007cadd0_self::FUN_007cadd0()

{

    int iStack_228;

    int auStack_110;

    char iStack_224[8];

    char auStack_220[264];

    char auStack_218[264];

    for (auStack_110 = 0; auStack_110 < 0xb; auStack_110++) {

        FUN_00406d00(auStack_220, 0x104, str_01074c4c, str_01076cc0, str_01074c6c, auStack_110);

        FUN_004b7240(auStack_220, auStack_218, 0x104);

        g_011dea10->FUN_004568c0(auStack_218, &m180[auStack_110], 0, 0);

    }

    for (iStack_228 = 1; iStack_228 < 5; iStack_228++) {

        FUN_00406d00(auStack_220, 0x104, str_01074c4c, str_01076ca4, str_01074c40, iStack_228);

        FUN_004b7240(auStack_220, auStack_218, 0x104);

        g_011dea10->FUN_004568c0(auStack_218, &m1a8[iStack_228], 0, 0);

    }

    if (FUN_00709d40())

        FUN_00406d30(iStack_224, 5, str_0101fd1c);

    else

        FUN_00406d30(iStack_224, 5, str_0101fd24);

    FUN_00406d00(auStack_218, 0x104, str_01076c94, str_01076cc0, iStack_224, str_01074c38);

    g_011dea10->FUN_004568c0(auStack_218, &m1c0, 0, 0);

    FUN_00406d00(auStack_220, 0x104, str_01074c08, str_01076cc0, str_01074c24);

    FUN_004b7240(auStack_220, auStack_218, 0x104);

    g_011dea10->FUN_004568c0(auStack_218, &m1bc, 0, 0);

    FUN_00406d00(auStack_218, 0x104, str_01076c94, str_01076cc0, iStack_224, str_01074c1c);

    g_011dea10->FUN_004568c0(auStack_218, &m1c4, 0, 0);

    FUN_00406d00(auStack_220, 0x104, str_01074c08, str_01076cc0, str_01074c14);

    FUN_004b7240(auStack_220, auStack_218, 0x104);

    g_011dea10->FUN_004568c0(auStack_218, &m1c8, 0, 0);

    FUN_00406d00(auStack_218, 0x104, str_01076c94, str_01076cc0, iStack_224, str_01074c00);

    g_011dea10->FUN_004568c0(auStack_218, &m1cc, 0, 0);

    FUN_00406d00(auStack_218, 0x104, str_01076c94, str_01076cc0, iStack_224, str_01074bf8);

    g_011dea10->FUN_004568c0(auStack_218, &m1d0, 0, 0);

    FUN_00406d00(auStack_220, 0x104, str_01074c08, str_01076cc0, str_01074be8);

    FUN_004b7240(auStack_220, auStack_218, 0x104);

    g_011dea10->FUN_004568c0(auStack_218, &m1d4, 0, 0);

    FUN_00406d00(auStack_220, 0x104, str_01074c08, str_01076cc0, str_01074bd8);

    FUN_004b7240(auStack_220, auStack_218, 0x104);

    g_011dea10->FUN_004568c0(auStack_218, &m1d8, 0, 0);

    FUN_00406d00(auStack_220, 0x104, str_01074c08, str_01076cc0, str_01074bc8);

    FUN_004b7240(auStack_220, auStack_218, 0x104);

    g_011dea10->FUN_004568c0(auStack_218, &m1dc, 0, 0);

    FUN_00406d00(auStack_220, 0x104, str_01074c08, str_01076cc0, str_01074bb8);

    FUN_004b7240(auStack_220, auStack_218, 0x104);

    g_011dea10->FUN_004568c0(auStack_218, &m1e0, 0, 0);

}

