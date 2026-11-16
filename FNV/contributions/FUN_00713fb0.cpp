struct D3DVP { unsigned int X; unsigned int Y; unsigned int Width; unsigned int Height; float MinZ; float MaxZ; };

struct NiColorA { float r, g, b, a; NiColorA(float fr, float fg, float fb, float fa); };

struct Dev {

    virtual void __stdcall d000(); virtual void __stdcall d004(); virtual void __stdcall d008(); virtual void __stdcall d00c(); virtual void __stdcall d010(); virtual void __stdcall d014();

    virtual void __stdcall d018(); virtual void __stdcall d01c(); virtual void __stdcall d020(); virtual void __stdcall d024(); virtual void __stdcall d028(); virtual void __stdcall d02c();

    virtual void __stdcall d030(); virtual void __stdcall d034(); virtual void __stdcall d038(); virtual void __stdcall d03c(); virtual void __stdcall d040(); virtual void __stdcall d044();

    virtual void __stdcall d048(); virtual void __stdcall d04c(); virtual void __stdcall d050(); virtual void __stdcall d054(); virtual void __stdcall d058(); virtual void __stdcall d05c();

    virtual void __stdcall d060(); virtual void __stdcall d064(); virtual void __stdcall d068(); virtual void __stdcall d06c(); virtual void __stdcall d070(); virtual void __stdcall d074();

    virtual void __stdcall d078(); virtual void __stdcall d07c(); virtual void __stdcall d080(); virtual void __stdcall d084(); virtual void __stdcall d088(); virtual void __stdcall d08c();

    virtual void __stdcall d090(); virtual void __stdcall d094(); virtual void __stdcall d098(); virtual void __stdcall d09c(); virtual void __stdcall d0a0(); virtual void __stdcall d0a4();

    virtual void __stdcall d0a8(); virtual void __stdcall d0ac(); virtual void __stdcall d0b0(); virtual void __stdcall d0b4(); virtual void __stdcall d0b8();

    virtual void __stdcall SetViewport(D3DVP* vp);

    virtual void __stdcall d0c0(); virtual void __stdcall d0c4(); virtual void __stdcall d0c8(); virtual void __stdcall d0cc(); virtual void __stdcall d0d0(); virtual void __stdcall d0d4();

    virtual void __stdcall d0d8(); virtual void __stdcall d0dc(); virtual void __stdcall d0e0();

    virtual void __stdcall SetRenderState(int state, int value);

    virtual void __stdcall d0e8(); virtual void __stdcall d0ec(); virtual void __stdcall d0f0(); virtual void __stdcall d0f4(); virtual void __stdcall d0f8(); virtual void __stdcall d0fc();

    virtual void __stdcall d100(); virtual void __stdcall d104(); virtual void __stdcall d108(); virtual void __stdcall d10c(); virtual void __stdcall d110(); virtual void __stdcall d114();

    virtual void __stdcall d118(); virtual void __stdcall d11c(); virtual void __stdcall d120(); virtual void __stdcall d124(); virtual void __stdcall d128(); virtual void __stdcall d12c();

    virtual void __stdcall d130(); virtual void __stdcall d134(); virtual void __stdcall d138(); virtual void __stdcall d13c(); virtual void __stdcall d140(); virtual void __stdcall d144();

    virtual void __stdcall d148(); virtual void __stdcall d14c(); virtual void __stdcall d150(); virtual void __stdcall d154(); virtual void __stdcall d158();

    virtual void __stdcall SetPixelShader(int shader);

    virtual void __stdcall GetPixelShader(int* shader);

    virtual void __stdcall d164(); virtual void __stdcall d168(); virtual void __stdcall d16c();

    virtual void __stdcall SetVertexShader(int shader);

    virtual void __stdcall d174(); virtual void __stdcall d178(); virtual void __stdcall d17c(); virtual void __stdcall d180(); virtual void __stdcall d184(); virtual void __stdcall d188();

    virtual void __stdcall d18c(); virtual void __stdcall d190(); virtual void __stdcall d194(); virtual void __stdcall d198(); virtual void __stdcall d19c(); virtual void __stdcall d1a0();

    virtual void __stdcall d1a4(); virtual void __stdcall d1a8();

    virtual void __stdcall SetFVF(int fvf);

};

struct Shadow {

    virtual void s000(); virtual void s004(); virtual void s008(); virtual void s00c(); virtual void s010(); virtual void s014();

    virtual void s018(); virtual void s01c(); virtual void s020(); virtual void s024(); virtual void s028(); virtual void s02c();

    virtual void s030(); virtual void s034(); virtual void s038(); virtual void s03c(); virtual void s040(); virtual void s044();

    virtual void s048(); virtual void s04c(); virtual void s050(); virtual void s054(); virtual void s058(); virtual void s05c();

    virtual void s060(); virtual void s064(); virtual void s068(); virtual void s06c(); virtual void s070(); virtual void s074();

    virtual void s078();

    virtual void s07c(int a, int b);

    virtual int s080();

    virtual void s084();

    virtual void s088(int a);

    virtual void s08c(int a, int b);

    virtual int s090();

    virtual void s094();

    virtual void s098(int a);

    virtual void s09c(); virtual void s0a0(); virtual void s0a4(); virtual void s0a8(); virtual void s0ac();

    virtual int s0b0();

    virtual void s0b4();

    virtual void s0b8(int a);

};

struct RT {

    virtual void r000(); virtual void r004(); virtual void r008(); virtual void r00c(); virtual void r010(); virtual void r014();

    virtual void r018(); virtual void r01c(); virtual void r020(); virtual void r024(); virtual void r028(); virtual void r02c();

    virtual void r030(); virtual void r034(); virtual void r038(); virtual void r03c(); virtual void r040(); virtual void r044();

    virtual void r048(); virtual void r04c(); virtual void r050(); virtual void r054(); virtual void r058(); virtual void r05c();

    virtual void r060(); virtual void r064(); virtual void r068(); virtual void r06c(); virtual void r070(); virtual void r074();

    virtual void r078(); virtual void r07c(); virtual void r080(); virtual void r084(); virtual void r088();

    virtual unsigned int GetWidth(int i);

    virtual unsigned int GetHeight(int i);

};

struct ScreenObj { unsigned int FUN_0044ddc0(); unsigned int FUN_0084e3a0(); };

struct Renderer {

    virtual void v000(); virtual void v004(); virtual void v008(); virtual void v00c(); virtual void v010(); virtual void v014();

    virtual void v018(); virtual void v01c(); virtual void v020(); virtual void v024(); virtual void v028(); virtual void v02c();

    virtual void v030(); virtual void v034(); virtual void v038(); virtual void v03c(); virtual void v040(); virtual void v044();

    virtual void v048(); virtual void v04c(); virtual void v050(); virtual void v054(); virtual void v058(); virtual void v05c();

    virtual void v060(); virtual void v064(); virtual void v068(); virtual void v06c(); virtual void v070(); virtual void v074();

    virtual void v078(); virtual void v07c(); virtual void v080(); virtual void v084(); virtual void v088(); virtual void v08c();

    virtual void v090(); virtual void v094(); virtual void v098(); virtual void v09c(); virtual void v0a0(); virtual void v0a4();

    virtual void v0a8();

    virtual void SetBackgroundColor(const NiColorA* c);

    virtual void v0b0();

    virtual void GetBackgroundColor(NiColorA* c);

    virtual void v0b8(); virtual void v0bc(); virtual void v0c0(); virtual void v0c4();

    virtual RT* GetDefaultRT();

    virtual RT* GetCurrentRT();

    virtual void v0d0();

    virtual ScreenObj* GetScreen();

    static Renderer* __cdecl GetSingleton();

    Dev* FUN_004dc020();

    Shadow* FUN_004ecaf0();

    void* FUN_005585e0();

    void FUN_007148c0(NiColorA* c, int b);

};

struct Obj10 { unsigned int FUN_0044ddc0(); };

struct Obj6629 { void FUN_00712e60(float* p); };

struct Obj7fa { Obj10* FUN_008d80e0(); Obj6629* FUN_006629f0(); };

struct ScopeE8 { int unk0; ScopeE8(int a, int b, const char* f, int l); ~ScopeE8(); };

struct ObjE4 {

    int u000, u004, u008, u00c, u010, u014, u018, u01c, u020, u024, u028, u02c;

    int u030, u034, u038, u03c, u040, u044, u048, u04c, u050, u054, u058, u05c;

    int u060, u064, u068, u06c, u070, u074, u078, u07c, u080, u084, u088, u08c;

    int u090, u094, u098, u09c, u0a0, u0a4, u0a8, u0ac, u0b0, u0b4, u0b8, u0bc;

    int u0c0, u0c4;

    ObjE4(unsigned int v);

    ~ObjE4();

};

struct ObjF0 { int unk0; ObjF0(void* p); ~ObjF0(); };

struct FlagHolder { unsigned char* FUN_00408d60(); };

extern FlagHolder DAT_011db2cc;

extern unsigned char DAT_011f9426;

extern float DAT_011ad840;

extern float DAT_011ad844;

extern float DAT_011ad848;

extern float DAT_011ad84c;

extern NiColorA DAT_011a9bd0;

extern float DAT_01026994;

extern float DAT_010340a4;

extern const char DAT_0106ef50[];

bool __cdecl FUN_004e9510();

void __cdecl FUN_00b6b890(int a, int b);

bool __cdecl FUN_004de080();

int __cdecl FUN_00683a60();

bool __cdecl FUN_00714a00();

void __cdecl FUN_00a81a80();

void __cdecl FUN_00714960(int a);

bool __cdecl FUN_007178a0();

bool __cdecl FUN_00717990();

void __cdecl FUN_00714900();

void __cdecl FUN_00b6b730();

void __cdecl FUN_00714a40(int a);

void __cdecl FUN_00714a60(int a);

void __cdecl FUN_00714a80(int a);

void __cdecl FUN_00714aa0(int a);

void __cdecl FUN_00714ac0(int a);

void __cdecl FUN_00714ae0(int a);

void __cdecl FUN_00714b00(int a);

void __cdecl FUN_004eced0(int a);

void __cdecl FUN_004ecb40(int a);

void __cdecl FUN_00714b20(int a);

void __cdecl FUN_00714b50(int a);

void __cdecl FUN_00714b80(int a);

void __cdecl FUN_00714bb0(int a);

void __cdecl FUN_00714bd0(int a);

void __cdecl FUN_004eb510(int a);

void __cdecl FUN_00714bf0(int a);

void __cdecl FUN_00714c20(int a);

void __cdecl FUN_00714c40(int a);

struct MenuMgr {

    int u000, u004, u008, u00c, u010, u014, u018, u01c, u020, u024, u028, u02c;

    int u030, u034, u038, u03c, u040, u044, u048, u04c, u050, u054, u058, u05c;

    int u060, u064, u068, u06c, u070, u074, u078, u07c, u080, u084, u088, u08c;

    int u090, u094, u098, u09c, u0a0, u0a4, u0a8, u0ac, u0b0, u0b4, u0b8, u0bc;

    int u0c0, u0c4, u0c8, u0cc, u0d0, u0d4, u0d8, u0dc, u0e0, u0e4, u0e8, u0ec;

    int u0f0, u0f4, u0f8, u0fc, u100, u104, u108, u10c, u110, u114, u118, u11c;

    int u120, u124, u128, u12c, u130, u134, u138, u13c, u140, u144, u148, u14c;

    int u150, u154, u158, u15c, u160, u164;

    unsigned char unk168;

    int u16c, u170, u174, u178, u17c, u180, u184, u188, u18c, u190, u194, u198;

    int u19c, u1a0, u1a4, u1a8, u1ac, u1b0, u1b4, u1b8, u1bc, u1c0, u1c4, u1c8;

    int u1cc, u1d0, u1d4, u1d8, u1dc, u1e0, u1e4, u1e8, u1ec, u1f0, u1f4, u1f8;

    int u1fc, u200, u204, u208, u20c, u210, u214, u218, u21c, u220, u224, u228;

    int u22c, u230, u234, u238, u23c, u240, u244, u248, u24c, u250, u254, u258;

    int u25c, u260, u264, u268, u26c, u270, u274, u278, u27c, u280, u284, u288;

    int u28c, u290, u294, u298, u29c, u2a0, u2a4, u2a8, u2ac, u2b0, u2b4, u2b8;

    int u2bc, u2c0, u2c4, u2c8, u2cc, u2d0, u2d4, u2d8, u2dc, u2e0, u2e4, u2e8;

    int u2ec, u2f0, u2f4, u2f8, u2fc, u300, u304, u308, u30c, u310, u314, u318;

    int u31c, u320, u324, u328, u32c, u330, u334, u338, u33c, u340, u344, u348;

    int u34c, u350, u354, u358, u35c, u360, u364, u368, u36c, u370, u374, u378;

    int u37c, u380, u384, u388, u38c, u390, u394, u398, u39c, u3a0, u3a4, u3a8;

    int u3ac, u3b0, u3b4, u3b8, u3bc, u3c0, u3c4, u3c8, u3cc, u3d0, u3d4, u3d8;

    int u3dc, u3e0, u3e4, u3e8, u3ec, u3f0, u3f4, u3f8, u3fc, u400, u404, u408;

    int u40c, u410, u414, u418, u41c, u420, u424, u428, u42c, u430, u434, u438;

    int u43c, u440, u444, u448, u44c, u450, u454, u458, u45c, u460, u464, u468;

    int u46c, u470, u474, u478, u47c, u480, u484, u488, u48c, u490, u494, u498;

    int u49c, u4a0, u4a4, u4a8, u4ac, u4b0, u4b4, u4b8;

    int unk4bc;

    Obj7fa* FUN_007fa950();

    void FUN_007134d0(ObjE4* p, bool b);

    void FUN_00713fb0(int a, int b);

};



void MenuMgr::FUN_00713fb0(int a, int b)

{

    Renderer* pkRenderer = Renderer::GetSingleton();

    bool bRestorec = false;

    if (FUN_004e9510()) {

        if (DAT_011f9426) {

            unsigned int uiWidth = Renderer::GetSingleton()->GetScreen()->FUN_0044ddc0();

            unsigned int uiHeighth = Renderer::GetSingleton()->GetScreen()->FUN_0084e3a0();

            D3DVP kViewportb;

            kViewportb.MinZ = 0.0f;

            kViewportb.MaxZ = 1.0f;

            kViewportb.X = (unsigned int)(uiWidth * DAT_011ad840);

            kViewportb.Width = (unsigned int)((DAT_011ad844 - DAT_011ad840) * uiWidth);

            kViewportb.Y = (unsigned int)(uiHeighth * DAT_011ad84c);

            kViewportb.Height = (unsigned int)((DAT_011ad848 - DAT_011ad84c) * uiHeighth);

            Renderer::GetSingleton()->FUN_004dc020()->SetViewport(&kViewportb);

        }

        FUN_00b6b890(7, 0);

        bRestorec = true;

        if (FUN_004de080()) {

            NiColorA kOldColorf(0.0f, 0.0f, 0.0f, 0.0f);

            Renderer::GetSingleton()->GetBackgroundColor(&kOldColorf);

            Renderer::GetSingleton()->SetBackgroundColor(&DAT_011a9bd0);

            NiColorA kColord(0.0f, 0.0f, 0.0f, 0.0f);

            kColord.r = 0.0f;

            kColord.g = DAT_01026994;

            kColord.b = 1.0f;

            kColord.a = 0.0f;

            Renderer::GetSingleton()->FUN_007148c0(&kColord, 1);

            kColord.r = DAT_010340a4;

            kColord.g = 1.0f;

            kColord.b = 1.0f;

            kColord.a = 0.0f;

            Renderer::GetSingleton()->FUN_007148c0(&kColord, 1);

            Renderer::GetSingleton()->SetBackgroundColor(&kOldColorf);

        }

        if (DAT_011f9426) {

            FUN_007fa950()->FUN_006629f0()->FUN_00712e60(&DAT_011ad840);

        }

    }

    ScopeE8 kScopee(0xd, 1, DAT_0106ef50, 0x1069);

    Obj7fa* pMenuh8 = FUN_007fa950();

    int iEarlyh4 = 0;

    if (!pMenuh8) {

        iEarlyh4 = 1;

        return;

    }

    Obj10* pTilea_ = pMenuh8->FUN_008d80e0();

    ObjE4 kE4g(pTilea_->FUN_0044ddc0());

    ObjF0 kF0f6(pkRenderer->FUN_005585e0());

    if (FUN_00683a60()) {

        if (FUN_00714a00())

            FUN_00a81a80();

        FUN_00714960(-1);

    }

    bool bFlagl;

    if (*DAT_011db2cc.FUN_00408d60())

        bFlagl = unk4bc == 2 || ((FUN_007178a0() || unk168) && FUN_00717990());

    else

        bFlagl = false;

    FUN_007134d0(&kE4g, bFlagl);

    if (bRestorec) {

        D3DVP kVPl;

        kVPl.X = 0;

        kVPl.Y = 0;

        kVPl.MinZ = 0.0f;

        kVPl.MaxZ = 1.0f;

        RT* pRTh = Renderer::GetSingleton()->GetCurrentRT();

        if (!pRTh)

            pRTh = Renderer::GetSingleton()->GetDefaultRT();

        kVPl.Width = pRTh->GetWidth(0);

        kVPl.Height = pRTh->GetHeight(0);

        Renderer::GetSingleton()->FUN_004dc020()->SetViewport(&kVPl);

        int iShadero = 0;

        Renderer::GetSingleton()->FUN_004dc020()->GetPixelShader(&iShadero);

        Renderer::GetSingleton()->FUN_004dc020()->SetRenderState(0x1b, 0);

        Renderer::GetSingleton()->FUN_004ecaf0()->s08c(0, 0);

        Renderer::GetSingleton()->FUN_004ecaf0()->s07c(0, 0);

        Renderer::GetSingleton()->FUN_004dc020()->SetFVF(0);

        Renderer::GetSingleton()->FUN_004dc020()->SetVertexShader(0);

        Renderer::GetSingleton()->FUN_004dc020()->SetPixelShader(iShadero);

        FUN_00714a40(0);

        FUN_00714a60(0);

        FUN_00714a80(0);

        FUN_00714aa0(0);

        FUN_00714ac0(0);

        FUN_00714ae0(0);

        FUN_00714b00(0);

        FUN_004eced0(0);

        FUN_004ecb40(0);

        FUN_00714b20(0);

        FUN_00714b50(0);

        FUN_00714b80(0);

        FUN_00714bb0(0);

        FUN_00714bd0(0);

        FUN_004eb510(0);

        FUN_00714bf0(0);

        FUN_00714c20(0);

        FUN_00714c40(0);

        FUN_00b6b730();

        Shadow* pShadowf5 = Renderer::GetSingleton()->FUN_004ecaf0();

        pShadowf5->s0b8(pShadowf5->s0b0());

        pShadowf5->s098(pShadowf5->s090());

        pShadowf5->s088(pShadowf5->s080());

    }

    if (FUN_00683a60())

        FUN_00714900();

}
