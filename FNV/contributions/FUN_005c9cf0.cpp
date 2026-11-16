// FUN_005c9cf0: builds a 6-vertex axis-cross line object around a reference. claude_opus_01 (Claude Opus 5.5).
struct LinePoint {
    float x, y, z;
    LinePoint();
    LinePoint(float fX, float fY, float fZ);
};
struct LineColor {
    float r, g, b, a;
    LineColor();
    LineColor(float fR, float fG, float fB, float fA);
};
struct LineBound {
    float FUN_0084d030();
};
struct Line3D {
    LineBound* FUN_0043d450();
};
void* FUN_00aa13e0(unsigned int size);
struct FUN_00a746e0 {
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c;
    int unk80; int unk84; int unk88; int unk8c; int unk90; int unk94; int unk98; int unk9c;
    int unka0; int unka4; int unka8; int unkac; int unkb0; int unkb4; int unkb8; int unkbc;
    int unkc0;
    FUN_00a746e0(unsigned short usVertices, LinePoint* pkVertex, LineColor* pkColor, void* pkTexture,
                 unsigned short usNumTextureSets, int eNBTMethod, bool* pkFlags);
    static void* operator new(unsigned int size);
    static void operator delete(void* p);
    void FUN_00440460(const LinePoint* pkPos);
};
struct LineDrawer {
    void FUN_00458e20(FUN_00a746e0* pkLines, float fLifetime);
};
extern float DAT_01017b78;
extern float DAT_01017868;
struct LineRef {
    virtual void* V000(); virtual void* V001(); virtual void* V002(); virtual void* V003();
    virtual void* V004(); virtual void* V005(); virtual void* V006(); virtual void* V007();
    virtual void* V008(); virtual void* V009(); virtual void* V010(); virtual void* V011();
    virtual void* V012(); virtual void* V013(); virtual void* V014(); virtual void* V015();
    virtual void* V016(); virtual void* V017(); virtual void* V018(); virtual void* V019();
    virtual void* V020(); virtual void* V021(); virtual void* V022(); virtual void* V023();
    virtual void* V024(); virtual void* V025(); virtual void* V026(); virtual void* V027();
    virtual void* V028(); virtual void* V029(); virtual void* V030(); virtual void* V031();
    virtual void* V032(); virtual void* V033(); virtual void* V034(); virtual void* V035();
    virtual void* V036(); virtual void* V037(); virtual void* V038(); virtual void* V039();
    virtual void* V040(); virtual void* V041(); virtual void* V042(); virtual void* V043();
    virtual void* V044(); virtual void* V045(); virtual void* V046(); virtual void* V047();
    virtual void* V048(); virtual void* V049(); virtual void* V050(); virtual void* V051();
    virtual void* V052(); virtual void* V053(); virtual void* V054(); virtual void* V055();
    virtual void* V056(); virtual void* V057(); virtual void* V058(); virtual void* V059();
    virtual void* V060(); virtual void* V061(); virtual void* V062(); virtual void* V063();
    virtual void* V064(); virtual void* V065(); virtual void* V066(); virtual void* V067();
    virtual void* V068(); virtual void* V069(); virtual void* V070(); virtual void* V071();
    virtual void* V072(); virtual void* V073(); virtual void* V074(); virtual void* V075();
    virtual void* V076(); virtual void* V077(); virtual void* V078(); virtual void* V079();
    virtual void* V080(); virtual void* V081(); virtual void* V082(); virtual void* V083();
    virtual void* V084(); virtual void* V085(); virtual void* V086(); virtual void* V087();
    virtual void* V088(); virtual void* V089(); virtual void* V090(); virtual void* V091();
    virtual void* V092(); virtual void* V093(); virtual void* V094(); virtual void* V095();
    virtual void* V096(); virtual void* V097(); virtual void* V098(); virtual void* V099();
    virtual void* V100(); virtual void* V101(); virtual void* V102(); virtual void* V103();
    virtual void* V104(); virtual void* V105(); virtual void* V106(); virtual void* V107();
    virtual void* V108(); virtual void* V109(); virtual void* V110(); virtual void* V111();
    virtual void* V112(); virtual void* V113(); virtual void* V114(); virtual void* V115();
    virtual Line3D* Get3D();
    virtual void* V117(); virtual void* V118(); virtual void* V119(); virtual void* V120();
    virtual void* V121(); virtual void* V122(); virtual void* V123(); virtual void* V124();
    virtual LinePoint* GetPos();
};

bool FUN_005c9cf0(void* a1, void* a2, LineRef* pRef)
{
    if (pRef) {
        float fSize = DAT_01017b78;
        if (pRef->Get3D()) {
            float fRadius = pRef->Get3D()->FUN_0043d450()->FUN_0084d030() * 0.5;
            if (fRadius < fSize)
                fSize = fRadius;
        }
        LinePoint* pColors = new LinePoint[6];
        LineColor* pFlags = new LineColor[6];
        bool* pPoints = new bool[6];
        pPoints[0] = true;
        pPoints[1] = false;
        pPoints[2] = true;
        pPoints[3] = false;
        pPoints[4] = true;
        pPoints[5] = false;
        pFlags[0] = LineColor(1.0f, 1.0f, 0.0f, 1.0f);
        pFlags[1] = LineColor(1.0f, 1.0f, 0.0f, 1.0f);
        pFlags[2] = LineColor(1.0f, 1.0f, 0.0f, 1.0f);
        pFlags[3] = LineColor(1.0f, 1.0f, 0.0f, 1.0f);
        pFlags[4] = LineColor(1.0f, 1.0f, 0.0f, 1.0f);
        pFlags[5] = LineColor(1.0f, 1.0f, 0.0f, 1.0f);
        pColors[0] = LinePoint(-fSize, 0.0f, 0.0f);
        pColors[1] = LinePoint(fSize, 0.0f, 0.0f);
        pColors[2] = LinePoint(0.0f, -fSize, 0.0f);
        pColors[3] = LinePoint(0.0f, fSize, 0.0f);
        pColors[4] = LinePoint(0.0f, 0.0f, -fSize);
        pColors[5] = LinePoint(0.0f, 0.0f, fSize);
        FUN_00a746e0* pLines = new FUN_00a746e0(6, pColors, pFlags, 0, 1, 0, pPoints);
        pLines->FUN_00440460(pRef->GetPos());
        ((LineDrawer*)DAT_011dea10)->FUN_00458e20(pLines, DAT_01017868);
    }
    return true;
}
