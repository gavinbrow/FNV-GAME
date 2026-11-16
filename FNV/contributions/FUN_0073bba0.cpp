// Adapted from a contributor's 2026-10-24 reconstruction of the Caravan menu destructor.
// Unknown member offsets are recorded explicitly, preserving the source binary layout.
struct ArrA { int a0; int a1; int a2; int a3; unsigned int FUN_0044ddc0(); unsigned int* FUN_006f2270(); void FUN_00753140(); ~ArrA(); };
struct ObjB { int a0; int a1; int a2; int a3; void FUN_008454f0(bool); ~ObjB(); };
struct ObjC { int a0; int a1; int a2; int a3; unsigned int FUN_0044ddc0(); void FUN_008454f0(bool); ~ObjC(); };
struct ListObj { ~ListObj(); void** FUN_006815c0(); void FUN_0063f7b0(); };
struct NodeFromGO { int FUN_00453470(); void FUN_00572160(); };
struct GlobalPtr { void operator=(void* x4); };
struct ModelLoader { void FUN_0045a5e0(const char* m26); };
struct DataHandler { void FUN_0046faf0(); };
extern GlobalPtr DAT_011d91a8;
extern ModelLoader* DAT_011c3b3c;
extern DataHandler* DAT_011c3f2c;
int __cdecl sprintf_s(char* v5, unsigned int n, const char* fmt, ...);
int __cdecl strcpy_s(char* v5, unsigned int n, const char* m26);
struct ShadowSceneNode {
    virtual void s00();
    virtual void s01();
    virtual void s02();
    virtual void s03();
    virtual void s04();
    virtual void s05();
    virtual void s06();
    virtual void s07();
    virtual void s08();
    virtual void s09();
    virtual void s10();
    virtual void s11();
    virtual void s12();
    virtual void s13();
    virtual void s14();
    virtual void s15();
    virtual void s16();
    virtual void s17();
    virtual void s18();
    virtual void s19();
    virtual void s20();
    virtual void s21();
    virtual void s22();
    virtual void s23();
    virtual void s24();
    virtual void s25();
    virtual void s26();
    virtual void s27();
    virtual void s28();
    virtual void s29();
    virtual void s30();
    virtual void s31();
    virtual void s32();
    virtual void s33();
    virtual void s34();
    virtual void s35();
    virtual void s36();
    virtual void s37();
    virtual void s38();
    virtual void s39();
    virtual void s40();
    virtual void s41();
    virtual void s42();
    virtual void s43();
    virtual void s44();
    virtual void s45();
    virtual void s46();
    virtual void s47();
    virtual void s48();
    virtual void s49();
    virtual void s50();
    virtual void s51();
    virtual void s52();
    virtual void s53();
    virtual void s54();
    virtual void s55();
    virtual void s56();
    virtual void s57();
    virtual void slot58(void* arg);
    void FUN_00b5d180();
};
struct Menu_007a8b10 { virtual ~Menu_007a8b10(); };
struct Cell1 { int vals[7]; };
struct Cell2 { int f0; int f1; int f2; int vals[4]; };
union GridU { Cell1 c1[6]; Cell2 c2[6]; };
struct FUN_0073bba0 : Menu_007a8b10 {
    int unk004;
    int unk008;
    int unk00c;
    int unk010;
    int unk014;
    int unk018;
    int unk01c;
    int unk020;
    int unk024;
    int m_028;
    int unk02c;
    int unk030;
    int unk034;
    int unk038;
    int unk03c;
    int unk040;
    int unk044;
    int unk048;
    int unk04c;
    int unk050;
    int unk054;
    int unk058;
    int unk05c;
    int unk060;
    int unk064;
    int unk068;
    int unk06c;
    int unk070;
    int unk074;
    int unk078;
    int unk07c;
    int unk080;
    int unk084;
    int unk088;
    int unk08c;
    int unk090;
    int unk094;
    int unk098;
    int unk09c;
    int unk0a0;
    int unk0a4;
    int unk0a8;
    int unk0ac;
    int unk0b0;
    int unk0b4;
    int unk0b8;
    int unk0bc;
    int unk0c0;
    int unk0c4;
    int unk0c8;
    int unk0cc;
    int unk0d0;
    int unk0d4;
    int unk0d8;
    int unk0dc;
    int unk0e0;
    int unk0e4;
    int unk0e8;
    int unk0ec;
    int unk0f0;
    int unk0f4;
    int unk0f8;
    int unk0fc;
    int m_100;
    int m_104;
    int unk108;
    int unk10c;
    int unk110;
    int m_114;
    int m_118;
    int m_11c[3];
    int m_128[3];
    ArrA m_134;
    ListObj* m_144;
    int f_148;
    ArrA m_14c;
    ListObj* m_15c;
    int f_160;
    ObjB m_164;
    ObjB m_174;
    int m_184;
    int m_188;
    int m_18c;
    int m_190;
    int m_194;
    GridU m_198;
    int m_240;
    int m_244[4];
    int m_254;
    int m_258[6];
    int m_270;
    int m_274[6];
    int m_28c[2];
    int unk294;
    int unk298;
    int unk29c;
    int unk2a0;
    int unk2a4;
    int unk2a8;
    int unk2ac;
    int unk2b0;
    int unk2b4;
    int unk2b8;
    int unk2bc;
    int unk2c0;
    int unk2c4;
    int unk2c8;
    int unk2cc;
    int unk2d0;
    int unk2d4;
    int unk2d8;
    int unk2dc;
    int unk2e0;
    int unk2e4;
    int unk2e8;
    int unk2ec;
    int unk2f0;
    int unk2f4;
    int unk2f8;
    int unk2fc;
    int unk300;
    int m_304[6][7];
    int m_3ac[6][7][4][2];
    int m_8ec[96];
    ObjC m_a6c;
    ObjB m_a7c[6];
    int unkadc;
    int unkae0;
    int unkae4;
    int unkae8;
    int unkaec;
    int unkaf0;
    int unkaf4;
    int unkaf8;
    int unkafc;
    int unkb00;
    ObjC m_b04;
    ObjC m_b14;
    ObjC m_b24;
    ObjC m_b34;
    ObjC m_b44[6][7];
    int unkde4;
    int unkde8;
    int unkdec;
    int unkdf0;
    int unkdf4;
    int unkdf8;
    int unkdfc;
    int unke00;
    int unke04;
    int unke08;
    int unke0c;
    int unke10;
    int unke14;
    int unke18;
    int unke1c;
    int unke20;
    int unke24;
    int unke28;
    int unke2c;
    int unke30;
    int unke34;
    int unke38;
    int unke3c;
    int unke40;
    int unke44;
    int unke48;
    int unke4c;
    int unke50;
    int m_e54[6];
    int m_e6c;
    int m_e70;
    virtual ~FUN_0073bba0();
};
FUN_0073bba0::~FUN_0073bba0()
{
    int z8;
    int q47;
    int q32;
    int q13;
    int x49;
    int x39;
    int x30;
    int x28;
    int x27;
    int x4;
    int m54;
    int m52;
    int m26;
    int m19;
    int m4;
    int n39;
    char n29[260];
    int n8;
    int v59;
    void* v45;
    void* v39;
    unsigned int v28;
    unsigned int v26;
    int v21;
    int v11;
    char v5[260];
    DAT_011d91a8 = 0;
    DAT_011c3b3c->FUN_0045a5e0("Meshes\\Terminals\\NV_Caravan\\NV_Caravan-Table.NIF");
    ((ShadowSceneNode*)FUN_00450b80(1))->slot58((NodeFromGO*)DAT_011d91e4.FUN_00559450());
    ((ShadowSceneNode*)FUN_00450b80(1))->FUN_00b5d180();
    if ((NodeFromGO*)DAT_011d91e4.FUN_00559450())
    {
        if (((NodeFromGO*)DAT_011d91e4.FUN_00559450())->FUN_00453470())
        {
            ((NodeFromGO*)DAT_011d91e4.FUN_00559450())->FUN_00572160();
        }
    }
    m_184 = 0;
    m_240 = 0;
    for (v11 = 0; v11 < 4; v11++)
        m_244[v11] = 0;
    ((GlobalPtr&)DAT_011d91e4) = 0;
    DAT_011d917c = 0;
    m_100 = 0;
    m_104 = 0;
    sprintf_s(v5, 260, "%sCurrency-Bill_Grid.NIF", "Meshes\\Terminals\\NV_Caravan\\");
    DAT_011c3b3c->FUN_0045a5e0(v5);
    sprintf_s(v5, 260, "%sCurrency-Coin_Grid.NIF", "Meshes\\Terminals\\NV_Caravan\\");
    DAT_011c3b3c->FUN_0045a5e0(v5);
    m_114 = 0;
    m_118 = 0;
    for (v21 = 0; v21 < 3; v21++)
    {
        sprintf_s(v5, 260, "%sCurrency-Bill_%i.NIF", "Meshes\\Terminals\\NV_Caravan\\", v21 + 1);
        DAT_011c3b3c->FUN_0045a5e0(v5);
        sprintf_s(v5, 260, "%sCurrency-Coin_%i.NIF", "Meshes\\Terminals\\NV_Caravan\\", v21 + 1);
        DAT_011c3b3c->FUN_0045a5e0(v5);
        m_128[v21] = 0;
        m_11c[v21] = 0;
    }
    while (m_134.FUN_0044ddc0() > 0)
    {
        v26 = *m_134.FUN_006f2270();
        m_134.FUN_00753140();
        v26 = 0;
    }
    while (m_14c.FUN_0044ddc0() > 0)
    {
        v28 = *m_14c.FUN_006f2270();
        m_14c.FUN_00753140();
        v28 = 0;
    }
    while (m_15c != 0 && *m_15c->FUN_006815c0() != 0)
    {
        v39 = *m_15c->FUN_006815c0();
        m_15c->FUN_0063f7b0();
        v39 = 0;
    }
    delete m_15c;
    m_15c = 0;
    while (m_144 != 0 && *m_144->FUN_006815c0() != 0)
    {
        v45 = *m_144->FUN_006815c0();
        m_144->FUN_0063f7b0();
        v45 = 0;
    }
    delete m_144;
    m_144 = 0;
    m_174.FUN_008454f0(true);
    m_164.FUN_008454f0(true);
    if (DAT_011c3f2c != 0)
        DAT_011c3f2c->FUN_0046faf0();
    switch (m_028)
    {
    case 0:
        break;
    case 1:
        {
            DAT_011c3b3c->FUN_0045a5e0("Meshes\\Terminals\\NV_Caravan\\NV_Caravan-Deck.NIF");
            DAT_011c3b3c->FUN_0045a5e0("Meshes\\Terminals\\NV_Caravan\\NV_Caravan-Available.NIF");
            m_188 = 0;
            m_18c = 0;
            m_270 = 0;
            m_254 = 0;
            for (v59 = 0; v59 < 6; v59++)
            {
                m_258[v59] = 0;
                m_274[v59] = 0;
            }
            if (m_a6c.FUN_0044ddc0() > 0)
                m_a6c.FUN_008454f0(true);
            for (n8 = 0; n8 < 96; n8++)
                m_8ec[n8] = 0;
        }
        break;
    case 2:
        goto sharedStateCleanup;
    case 3:
sharedStateCleanup:
        {
            for (n39 = 0; n39 < 2; n39++)
                m_28c[n39] = 0;
            for (m4 = 0; m4 < 2; m4++)
            {
                for (m19 = 0; m19 < 6; m19++)
                {
                }
            }
            for (m26 = 0; m26 < 2; m26++)
            {
                for (m52 = 0; m52 < 8; m52++)
                {
                }
            }
            for (m54 = 0; m54 < 6; m54++)
            {
                for (x4 = 0; x4 < 7; x4++)
                    m_304[m54][x4] = 0;
            }
            for (x27 = 0; x27 < 6; x27++)
            {
                for (x28 = 0; x28 < 7; x28++)
                {
                    x30 = 0;
                    for (; x28 < 4; x28++)
                    {
                        for (x39 = 0; x39 < 2; x39++)
                            m_3ac[x27][x28][x30][x39] = 0;
                    }
                }
            }
            if (m_b04.FUN_0044ddc0() > 0)
                m_b04.FUN_008454f0(true);
            if (m_b14.FUN_0044ddc0() > 0)
                m_b14.FUN_008454f0(true);
            if (m_b24.FUN_0044ddc0() > 0)
                m_b24.FUN_008454f0(true);
            if (m_b34.FUN_0044ddc0() > 0)
                m_b34.FUN_008454f0(true);
            for (x49 = 0; x49 < 6; x49++)
            {
                for (q13 = 0; q13 < 7; q13++)
                {
                    if (m_b44[x49][q13].FUN_0044ddc0())
                        m_b44[x49][q13].FUN_008454f0(true);
                }
            }
            strcpy_s(n29, 260, "PlayerGrid_1.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            strcpy_s(n29, 260, "PlayerGrid_2.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            strcpy_s(n29, 260, "PlayerGrid_3.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            strcpy_s(n29, 260, "OppGrid_1.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            strcpy_s(n29, 260, "OppGrid_2.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            strcpy_s(n29, 260, "OppGrid_3.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            strcpy_s(n29, 260, "Select_Add.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            strcpy_s(n29, 260, "Select_Remove.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            m_e6c = 0;
            m_e70 = 0;
            sprintf_s(n29, 260, "%s%s", "Meshes\\Terminals\\NV_Caravan\\", "Player_Deck-Start.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            sprintf_s(n29, 260, "%s%s", "Meshes\\Terminals\\NV_Caravan\\", "Opponent_Deck-Start.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            sprintf_s(n29, 260, "%s%s", "Meshes\\Terminals\\NV_Caravan\\", "Player_Deck.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            sprintf_s(n29, 260, "%s%s", "Meshes\\Terminals\\NV_Caravan\\", "Opponent_Deck.NIF");
            DAT_011c3b3c->FUN_0045a5e0(n29);
            m_190 = 0;
            m_194 = 0;
            for (q32 = 0; q32 < 6; q32++)
                m_e54[q32] = 0;
            for (q47 = 0; q47 < 3; q47++)
            {
                for (z8 = 0; z8 < 7; z8++)
                {
                    sprintf_s(n29, 260, "%sPlayer_%i_0%i.NIF", "Meshes\\Terminals\\NV_Caravan\\", q47 + 1, z8 + 1);
                    DAT_011c3b3c->FUN_0045a5e0(n29);
                    m_198.c1[q47].vals[z8] = 0;
                    sprintf_s(n29, 260, "%sOpponent_%i_0%i.NIF", "Meshes\\Terminals\\NV_Caravan\\", q47 + 1, z8 + 1);
                    DAT_011c3b3c->FUN_0045a5e0(n29);
                    m_198.c2[q47 + 3].vals[z8] = 0;
                }
            }
        }
        break;
    }
}
