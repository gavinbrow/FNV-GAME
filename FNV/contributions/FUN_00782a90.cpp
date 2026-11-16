struct TileS {
    void FUN_00a01350(int, const char*, bool);
    void FUN_00700320(int, int);
};
struct MenuTileObj { TileS* FUN_00a03da0(const char*); void FUN_00700320(int, int); };
struct ListNodeObj {
    void** FUN_006815c0();
    ListNodeObj* FUN_00726070();
    unsigned char FUN_008256d0();
    void FUN_00470470();
};
struct LbObj {
    virtual void q0(int);
    virtual void q1();
    virtual void q2();
    virtual void q3();
    virtual void q4();
    virtual void q5();
    virtual void q6();
    virtual void q7();
    virtual void q8(int);
    TileS* FUN_0071a320(int, const char*, int, int);
    void FUN_0071a320(void*, const char*, void*, int);
    void FUN_0071a200(void*);
    void FUN_0071a670();
    void FUN_007314c0(void*, int, int);
    void FUN_00719ef0(void*, int, int, void*, int, int);
    void FUN_00730bb0(void*);
};
struct InvObj {
    virtual void mq0();
    virtual void mq1();
    virtual void mq2();
    virtual void mq3();
    virtual void mq4();
    virtual void mq5(int, void*);
    int unknown_04; int unknown_08; int unknown_0c; int unknown_10; int unknown_14; int unknown_18; int unknown_1c; int unknown_20; int unknown_24;
    TileS* t28; TileS* t2c; TileS* t30; TileS* t34; int f38; TileS* t3c; int f40;
    TileS* t44; TileS* t48; TileS* t4c;
    int unknown_50; int unknown_54; int unknown_58; int unknown_5c; int unknown_60; int unknown_64; int unknown_68; int unknown_6c; int unknown_70;
    TileS* t74; int f78; TileS* t7c;
    int unknown_80; int unknown_84; int unknown_88; int unknown_8c; int unknown_90; int unknown_94; int unknown_98; int unknown_9c; int unknown_a0; int unknown_a4; int unknown_a8; int unknown_ac; int unknown_b0; int unknown_b4;
    LbObj lb;
    int unknown_bc; int unknown_c0; int unknown_c4; int unknown_c8; int unknown_cc; int unknown_d0; int unknown_d4; int unknown_d8; int unknown_dc; int unknown_e0; int unknown_e4; int unknown_e8; int unknown_ec; int unknown_f0; int unknown_f4; int unknown_f8; int unknown_fc; int unknown_100; int unknown_104; int unknown_108; int unknown_10c; int unknown_110; int unknown_114; int unknown_118;
    ListNodeObj listHead;
    MenuTileObj* FUN_00726070();
};
struct InvChangesObj {
    void FUN_004d4b00(void*, void*);
    int FUN_004c6ba0(int, int*);
};
struct FUN_0096a2d0 {
    void* m_item; FUN_0096a2d0* m_next;
    FUN_0096a2d0();
    ~FUN_0096a2d0();
};
struct ActorAV {
    virtual int q0();
    virtual int q1();
    virtual int q2(int);
    virtual float q3(int);
    virtual int q4();
    virtual int q5();
    virtual int q6();
    virtual int q7(int);
};
struct ProcObj {
    virtual int p0();
    virtual int p1();
    virtual int p2();
    virtual int p3();
    virtual int p4();
    virtual int p5();
    virtual int p6();
    virtual int p7();
    virtual int p8();
    virtual int p9();
    virtual int p10();
    virtual int p11();
    virtual int p12();
    virtual int p13();
    virtual int p14();
    virtual int p15();
    virtual int p16();
    virtual int p17();
    virtual int p18();
    virtual int p19();
    virtual int p20();
    virtual int p21();
    virtual int p22();
    virtual int p23();
    virtual int p24();
    virtual int p25();
    virtual int p26();
    virtual int p27();
    virtual int p28();
    virtual int p29();
    virtual int p30();
    virtual int p31();
    virtual int p32();
    virtual int p33();
    virtual int p34();
    virtual int p35();
    virtual int p36();
    virtual int p37();
    virtual int p38();
    virtual int p39();
    virtual int p40();
    virtual int p41();
    virtual int p42();
    virtual int p43();
    virtual int p44();
    virtual int p45();
    virtual int p46();
    virtual int p47();
    virtual int p48();
    virtual int p49();
    virtual int p50();
    virtual int p51();
    virtual int p52();
    virtual int p53();
    virtual int p54();
    virtual int p55();
    virtual int p56();
    virtual int p57();
    virtual int p58();
    virtual int p59();
    virtual int p60();
    virtual int p61();
    virtual int p62();
    virtual int p63();
    virtual int p64();
    virtual int p65();
    virtual int p66();
    virtual int p67();
    virtual int p68();
    virtual int p69();
    virtual int p70();
    virtual int p71();
    virtual int p72();
    virtual int p73();
    virtual int p74();
    virtual int p75();
    virtual int p76();
    virtual int p77();
    virtual int p78();
    virtual int p79();
    virtual int p80();
    virtual int p81();
    virtual int q82();
};
struct PlayerShell {
    int FUN_00891d70();
    float FUN_008a0c20();
    ProcObj* FUN_008d8520();
};
struct RenderedObj { bool FUN_00974d90(); };
struct FloatSettingObj { float* FUN_00403e20(); };
struct IntSettingObj { int* FUN_0043d4d0(); };
struct SoundHolder { const char* FUN_00408da0(); };
class TESFullName { public: virtual void tf0(); };

struct ItemObj { unsigned char FUN_004bd820(); };
extern int DAT_011d9ea4;
extern int DAT_011d9eb4;
extern int DAT_011d9eb8;
extern int DAT_011d1020;
extern int DAT_011d3a08;
extern int DAT_011d2a18;
extern int DAT_011d4f60;
extern int DAT_011d35d0;
extern int DAT_011d2eb0;
extern int DAT_011d4378;
extern int DAT_011d25b0;
extern int DAT_011d1e60;
extern int DAT_011d300c;
extern int DAT_011d3b20;
extern int DAT_011c3cb4;
void* __cdecl FUN_00705990();

int __cdecl FUN_00406d90(float);
int __cdecl FUN_00406d00(char*, int, const char*, ...);
int __cdecl FUN_00406d30(char*, unsigned int, const char*);
int __cdecl FUN_00406d50(char*, unsigned int, const char*);
int __cdecl FUN_00408b20(const char*, const char*);
void __cdecl FUN_0077ffd0();
int __cdecl FUN_005e58f0(int, void*, void*, int, float*);
unsigned int __fastcall FUN_0044ddc0(void*);
int __cdecl FUN_004839c0(int);
unsigned int __cdecl FUN_0044a670(const char*);

void __cdecl FUN_007824e0();
void __cdecl FUN_00782620();
static const char kStr_IM_Headline_Title[] = "IM_Headline_Title";
void FUN_00782a90()
{
    ListNodeObj* fh;
    int el;
    InvChangesObj* ea;
    int df;
    int cn;
    int ck;
    int ca;
    float bn;
    float bl;
    char ba[64];
    int ak;
    if (DAT_011d9ea4 && ((RenderedObj*)FUN_00705990())->FUN_00974d90()) {
        ea = (InvChangesObj*)FUN_004bf220(g_thePlayer);
        ca = FUN_00406d90(((ActorAV*)&g_thePlayer->actorValueOwner)->q3(0x12));
        ak = (int)(*((FloatSettingObj*)&DAT_011d1020)->FUN_00403e20());
        if (ca > ak) ca = ak;
        FUN_00406d00(ba, 0x40, "%d", ca);
        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t30->FUN_00a01350(DAT_011d9eb4, ba, true);
        bl = (float)FUN_00406d90(((ActorAV*)&g_thePlayer->actorValueOwner)->q3(0x4c));
        cn = ((PlayerShell*)g_thePlayer)->FUN_008d8520()->q82();
        ck = 0;
        if (cn) ck = (int)FUN_0044ddc0((void*)cn);
        else ck = FUN_004839c0(0x1f4);
        bn = 0.0f;
        FUN_005e58f0(0x38, g_thePlayer, g_thePlayer, ck, &bn);
        FUN_00406d00(ba, 0x40, "%1.1f", (double)(bl + bn));
        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t7c->FUN_00a01350(DAT_011d9eb4, ba, true);
        if (((PlayerShell*)g_thePlayer)->FUN_00891d70() > *((IntSettingObj*)&DAT_011d3a08)->FUN_0043d4d0())
            FUN_00406d00(ba, 0x40, "%d+", *((IntSettingObj*)&DAT_011d3a08)->FUN_0043d4d0());
        else
            FUN_00406d00(ba, 0x40, "%d", ((PlayerShell*)g_thePlayer)->FUN_00891d70());
        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t28->FUN_00a01350(DAT_011d9eb4, ba, true);
        FUN_00406d00(ba, 0x40, "%d/%d", ((ActorAV*)&g_thePlayer->actorValueOwner)->q2(0x2e), (int)(((PlayerShell*)g_thePlayer)->FUN_008a0c20()));
        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t34->FUN_00a01350(DAT_011d9eb4, ba, true);
        FUN_00406d00(ba, 0x40, "%d/%d", ((ActorAV*)&g_thePlayer->actorValueOwner)->q2(0x10), ((ActorAV*)&g_thePlayer->actorValueOwner)->q7(0x10));
        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t2c->FUN_00a01350(DAT_011d9eb4, ba, true);
        if (FUN_00408b20(((InventoryMenuSetting*)&DAT_011c3cb4)->FUN_00403df0(), "ENGLISH")) {
            el = (int)FUN_00a01860("_Title");
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t44->FUN_00a01350(0xfc4, ((InventoryMenuSetting*)&DAT_011d2a18)->FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t48->FUN_00a01350(0xfc4, ((InventoryMenuSetting*)&DAT_011d4f60)->FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t4c->FUN_00a01350(0xfc4, ((InventoryMenuSetting*)&DAT_011d35d0)->FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t74->FUN_00a01350(0xfc4, ((InventoryMenuSetting*)&DAT_011d2eb0)->FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->FUN_00726070()->FUN_00a03da0(kStr_IM_Headline_Title)->FUN_00a01350(0xfc4, ((InventoryMenuSetting*)&DAT_011d4378)->FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t30->FUN_00a01350(el, DAT_011d20c4.FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t7c->FUN_00a01350(el, DAT_011d396c.FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t28->FUN_00a01350(el, ((InventoryMenuSetting*)&DAT_011d25b0)->FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t34->FUN_00a01350(el, ((InventoryMenuSetting*)&DAT_011d1e60)->FUN_00403df0(), true);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t2c->FUN_00a01350(el, ((InventoryMenuSetting*)&DAT_011d300c)->FUN_00403df0(), true);
        }
        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->t3c->FUN_00700320(0xfa3, 0);
        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->FUN_00726070()->FUN_00700320(DAT_011d9eb8, 0);
        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->mq5(0x1d, 0);
        if (((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->listHead.FUN_008256d0() == 0 && ea) {
            FUN_0077ffd0();
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.q0(0);
            for (fh = (ListNodeObj*)&((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->listHead; fh && *fh->FUN_006815c0(); fh = fh->FUN_00726070()) {
                {
                    char bo[128];
                    void* bb;
                    int as;
                    ListNodeObj* am;
                    FUN_0096a2d0 ah;
                    ea->FUN_004d4b00(*fh->FUN_006815c0(), &ah);
                    ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_0071a200(*fh->FUN_006815c0());
                    for (am = (ListNodeObj*)&ah; am && *am->FUN_006815c0(); am = am->FUN_00726070()) {
                        bb = dynamic_cast<TESFullName*>((TESBoundObject*)(void*)((ItemChange*)*am->FUN_006815c0())->FUN_0044ddc0());
                        as = (int)FUN_0044a670(((SoundHolder*)bb)->FUN_00408da0());
                        FUN_00406d30(bo, 0x80, ((SoundHolder*)bb)->FUN_00408da0());
                        if (((ItemObj*)*am->FUN_006815c0())->FUN_004bd820())
                            FUN_00406d50(bo, 0x80, "+");
                        ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_0071a320(*am->FUN_006815c0(), bo, (void*)&FUN_007824e0, 0);
                    }
                }
            }
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_007314c0((void*)&FUN_00782850, 0, 0x7fffffff);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_0071a670();
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_007314c0((void*)&FUN_00780c00, -1, 0x7fffffff);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->listHead.FUN_00470470();
        } else {
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_00719ef0(g_thePlayer, 0, 0, (void*)&FUN_00782850, 0, 0);
            if (ea) {
                if (ea->FUN_004c6ba0(0x2e, &df)) {
                    TileS* tt;
                    tt = ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_0071a320(0, ((InventoryMenuSetting*)&DAT_011d3b20)->FUN_00403df0(), 0, 0);
                    tt->FUN_00700320(0xfaa, 0x1e);
                }
            }
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_00730bb0((void*)&FUN_00782620);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.FUN_007314c0((void*)&FUN_00780c00, -1, 0x7fffffff);
            ((InvObj*)(void*)(unsigned int)DAT_011d9ea4)->lb.q8((int)&FUN_007824e0);
        }
        ((FUN_00781b10_shell*)DAT_011d9ea4)->FUN_00781b10();
        FUN_007800c0();
    }
}
