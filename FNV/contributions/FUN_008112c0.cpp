struct EffB {
    int FUN_0084e3a0();
};
struct EffA {
    EffB* FUN_004fd3c0();
    EffB* FUN_004fd380();
};
struct Handle {
    int h00;
    int h04;
    int h08;
    unsigned char FUN_00ad8ce0();
    void FUN_00ad8d10();
    void FUN_00418900(int);
};
struct V116 {
    void FUN_00440490(float);
    int FUN_0043b230();
};
struct C0Obj {
    int c00;
    int c04;
    int c08;
    int c0c;
    int c10;
    int c14;
    int c18;
    C0Obj(int, void*);
    void FUN_0081c470(int, float);
    void FUN_00621b00(float);
};
struct Ret8d {
    void FUN_00548230();
};
struct Obj30 {
    int o00;
    int o04;
    int o08;
    ~Obj30();
};
struct StrObj {
    int s00;
    StrObj(const char*);
    ~StrObj();
};
struct Obj1c {
    int FUN_0047a520(StrObj*);
};
struct Obj24 {
    float FUN_00508100();
};
void FUN_00401460(void*, void*, int);
void* FUN_00653270(void*, int);
extern int DAT_011f36ac;
extern double DAT_0101de30;

struct Cls8112c0 {
    virtual void virt_000();
    virtual void virt_001();
    virtual void virt_002();
    virtual void virt_003();
    virtual void virt_004();
    virtual void virt_005();
    virtual void virt_006();
    virtual void virt_007();
    virtual void virt_008();
    virtual void virt_009();
    virtual void virt_010();
    virtual void virt_011();
    virtual void virt_012();
    virtual void virt_013();
    virtual void virt_014();
    virtual void virt_015();
    virtual void virt_016();
    virtual void virt_017();
    virtual void virt_018();
    virtual void virt_019();
    virtual void virt_020();
    virtual void virt_021();
    virtual void virt_022();
    virtual void virt_023();
    virtual void virt_024();
    virtual void virt_025();
    virtual void virt_026();
    virtual void virt_027();
    virtual void virt_028();
    virtual void virt_029();
    virtual void virt_030();
    virtual void virt_031();
    virtual void virt_032();
    virtual void virt_033();
    virtual void virt_034();
    virtual void virt_035();
    virtual void virt_036();
    virtual void virt_037();
    virtual void virt_038();
    virtual void virt_039();
    virtual void virt_040();
    virtual void virt_041();
    virtual void virt_042();
    virtual void virt_043();
    virtual void virt_044();
    virtual void virt_045();
    virtual void virt_046();
    virtual void virt_047();
    virtual void virt_048();
    virtual void virt_049();
    virtual void virt_050();
    virtual void virt_051();
    virtual void virt_052();
    virtual void virt_053();
    virtual void virt_054();
    virtual void virt_055();
    virtual void virt_056();
    virtual void virt_057();
    virtual void virt_058();
    virtual void virt_059();
    virtual void virt_060();
    virtual void virt_061();
    virtual void virt_062();
    virtual void virt_063();
    virtual void virt_064();
    virtual void virt_065();
    virtual void virt_066();
    virtual void virt_067();
    virtual void virt_068();
    virtual void virt_069();
    virtual void virt_070();
    virtual void virt_071();
    virtual void virt_072();
    virtual void virt_073();
    virtual void virt_074();
    virtual void virt_075();
    virtual void virt_076();
    virtual void virt_077();
    virtual void virt_078();
    virtual void virt_079();
    virtual void virt_080();
    virtual void virt_081();
    virtual void virt_082();
    virtual void virt_083();
    virtual void virt_084();
    virtual void virt_085();
    virtual void virt_086();
    virtual void virt_087();
    virtual void virt_088();
    virtual void virt_089();
    virtual void virt_090();
    virtual void virt_091();
    virtual void virt_092();
    virtual void virt_093();
    virtual void virt_094();
    virtual void virt_095();
    virtual void virt_096();
    virtual void virt_097();
    virtual void virt_098();
    virtual void virt_099();
    virtual void virt_100();
    virtual void virt_101();
    virtual void virt_102();
    virtual void virt_103();
    virtual void virt_104();
    virtual void virt_105();
    virtual void virt_106();
    virtual void virt_107();
    virtual void virt_108();
    virtual void virt_109();
    virtual void virt_110();
    virtual void virt_111();
    virtual void virt_112();
    virtual void virt_113();
    virtual void virt_114();
    virtual void virt_115();
    virtual V116* virt_116();
    int f04;
    int f08;
    int f0c;
    int f10;
    int f14;
    int f18;
    int f1c;
    int f20;
    int f24;
    int f28;
    int f2c;
    int f30;
    int f34;
    int f38;
    int f3c;
    int f40;
    int f44;
    int f48;
    int f4c;
    int f50;
    int f54;
    int f58;
    int f5c;
    int f60;
    int f64;
    int f68;
    int f6c;
    int f70;
    int f74;
    int f78;
    int f7c;
    int f80;
    int f84;
    int f88;
    int f8c;
    int f90;
    int f94;
    int f98;
    int f9c;
    int fa0;
    int fa4;
    int fa8;
    int m_ac;
    float m_b0;
    Handle m_b4;
    C0Obj* m_c0;
    void FUN_0081ea40(int, int);
    void FUN_0080fcf0();
    Ret8d* FUN_008d6f30(Cls8112c0*, int);
    EffA* FUN_004fd400();
    Obj30 FUN_00933150(int, int, int, int);
    void FUN_008112c0(int, int);
};

void Cls8112c0::FUN_008112c0(int a1, int a2)
{
    float f10;
    FUN_0081ea40(a1, a2);
    FUN_0080fcf0();
    FUN_008d6f30(this, 0)->FUN_00548230();
    if (m_ac != 2) {
        if (FUN_004fd400()->FUN_004fd3c0()) {
            int v14;
            v14 = FUN_004fd400()->FUN_004fd3c0()->FUN_0084e3a0();
            if (m_b4.FUN_00ad8ce0()) {
                m_b4.FUN_00ad8d10();
            }
            {
                m_b4.FUN_00418900((int)&FUN_00933150(v14, 1, 0x40000102, 1));
            }
        }
    }
    if (virt_116()) {
        virt_116()->FUN_00440490(m_b0);
    }
    FUN_00401460(&f10, &m_c0, 4);
    m_c0 = 0;
    if (virt_116()) {
        if (FUN_004fd400()->FUN_004fd380()) {
            m_c0 = new C0Obj(FUN_004fd400()->FUN_004fd380()->FUN_0084e3a0(), virt_116());
            if (m_ac == 2 && m_c0 != 0) {
                V116* v20;
                int t18;
                Obj1c* foundEffect;
                int result;
                v20 = virt_116();
                t18 = v20 ? v20->FUN_0043b230() : 0;
                foundEffect = (Obj1c*)FUN_00653270(&DAT_011f36ac, t18);
                if (foundEffect) {
                    result = foundEffect->FUN_0047a520(&StrObj("SpecialIdle_AreaEffect"));
                    if (result) {
                        m_c0->FUN_0081c470(0, ((Obj24*)result)->FUN_00508100() * DAT_0101de30);
                        m_c0->FUN_00621b00(f10);
                    }
                }
            }
        }
    }
}
