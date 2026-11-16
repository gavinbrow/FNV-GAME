// Stand-in types are named after the game function whose constructor they wrap.
struct FUN_00416870 {   // 3-float vector
    float unk00; float unk04; float unk08;
    FUN_00416870(float, float, float);
};
struct FUN_00414430 {   // 4-float rectangle (viewport)
    float unk00; float unk04; float unk08; float unk0c;
    FUN_00414430(float, float, float, float);
};
struct FUN_00a71b70 {   // frustum: four edges, near, far, orthographic flag
    float unk00; float unk04; float unk08; float unk0c; float unk10; float unk14; bool unk18;
    FUN_00a71b70(int);
};
struct FUN_0043d410 {   // small 12-byte value object
    float unk00; int unk04; int unk08;
    FUN_0043d410(float, int, int);
};
struct Setting {
    float* FUN_00403e20();
};
struct Renderer {
    virtual void vf00(); virtual void vf01(); virtual void vf02(); virtual void vf03(); virtual void vf04(); virtual void vf05(); virtual void vf06(); virtual void vf07(); virtual void vf08(); virtual void vf09(); virtual void vf10(); virtual void vf11(); virtual void vf12(); virtual void vf13(); virtual void vf14(); virtual void vf15(); virtual void vf16(); virtual void vf17(); virtual void vf18(); virtual void vf19(); virtual void vf20(); virtual void vf21(); virtual void vf22(); virtual void vf23(); virtual void vf24(); virtual void vf25(); virtual void vf26(); virtual void vf27(); virtual void vf28(); virtual void vf29(); virtual void vf30(); virtual void vf31(); virtual void vf32(); virtual void vf33(); virtual void vf34(); virtual void vf35(); virtual void vf36(); virtual void vf37(); virtual void vf38(); virtual void vf39(); virtual void vf40(); virtual void vf41(); virtual void vf42(); virtual void vf43(); virtual void vf44(); virtual void vf45(); virtual void vf46(); virtual void vf47(); virtual void vf48(); virtual void vf49(); virtual void vf50(); virtual void vf51(); virtual void vf52(); virtual void vf53(); virtual void vf54(); virtual void vf55(); virtual void vf56(); virtual void vf57(); virtual void vf58(); virtual void vf59(); virtual void vf60(); virtual void vf61(); virtual void vf62(); virtual void vf63();
    virtual float vf64();   // vtable slot 0x100: returns the far-plane distance
};
struct FUN_00aa13e0 {   // allocator base: supplies the class operator new
    static void* operator new(unsigned int);
    static void operator delete(void*);
};
struct FUN_00a712f0 : FUN_00aa13e0 {   // camera object, size 0x114
    int unk00; int unk04; int unk08; int unk0c; int unk10; int unk14; int unk18; int unk1c; int unk20; int unk24; int unk28; int unk2c; int unk30; int unk34; int unk38; int unk3c; int unk40; int unk44; int unk48; int unk4c; int unk50; int unk54; int unk58; int unk5c; int unk60; int unk64; int unk68; int unk6c; int unk70; int unk74; int unk78; int unk7c; int unk80; int unk84; int unk88; int unk8c; int unk90; int unk94; int unk98; int unk9c; int unka0; int unka4; int unka8; int unkac; int unkb0; int unkb4; int unkb8; int unkbc; int unkc0; int unkc4; int unkc8; int unkcc; int unkd0; int unkd4; int unkd8; int unkdc; int unke0; int unke4; int unke8; int unkec; int unkf0; int unkf4; int unkf8; int unkfc; int unk100; int unk104; int unk108; int unk10c; int unk110;
    FUN_00a712f0();
    void FUN_00712e60(FUN_00414430*);
    void FUN_00507700(float);
    void FUN_00a6faf0(FUN_00a71b70*);
    void FUN_00a701b0(const FUN_00416870&, const FUN_00416870&);
    void FUN_00733fd0(float);
    void FUN_00a59c60(FUN_0043d410*);
};
struct FUN_0078e900_shell {
    FUN_00a712f0* FUN_0078e900();
};

Renderer* FUN_0045c670();
int FUN_004dc200();
int FUN_004dc1f0();
float __cdecl FUN_0057dd70(float);
extern Setting DAT_01203144;
extern Setting DAT_01203150;
extern bool DAT_011f9426;
extern int DAT_011f9434;
extern float DAT_01016264;
extern double DAT_01023128;
extern double DAT_01070c80;

// Builds a camera: viewport, frustum from a field-of-view setting and the
// screen aspect ratio, far/near ratio, and a default orientation.
// Local names are chosen only to reproduce the original stack layout:
//   b = camera, f = viewport rect, c = frustum, g = aspect ratio,
//   d = frustum scale, e = view angle, a = trailing value object.
FUN_00a712f0* FUN_0078e900_shell::FUN_0078e900()
{
    float g;
    FUN_00a712f0* b = new FUN_00a712f0;
    FUN_00414430 f(0.0f, 1.0f, 1.0f, 0.0f);
    float d;
    b->FUN_00712e60(&f);
    FUN_00a71b70 c(0);
    float e;
    c.unk14 = FUN_0045c670()->vf64();
    c.unk10 = *DAT_01203144.FUN_00403e20();
    b->FUN_00507700(c.unk14 / c.unk10);
    g = (double)(DAT_011f9426 ? DAT_011f9434 : FUN_004dc200()) / FUN_004dc1f0();
    d = DAT_01016264;
    e = *DAT_01203150.FUN_00403e20() * DAT_01023128 * DAT_01070c80;
    c.unk00 = -FUN_0057dd70(e) * d;
    c.unk04 = FUN_0057dd70(e) * d;
    c.unk0c = -FUN_0057dd70(e) * g * d;
    c.unk08 = FUN_0057dd70(e) * g * d;
    c.unk18 = false;
    b->FUN_00a6faf0(&c);
    b->FUN_00a701b0(FUN_00416870(0.0f, 0.0f, 1.0f), FUN_00416870(0.0f, 0.0f, 1.0f));
    b->FUN_00733fd0(1.0f);
    FUN_0043d410 a(0.0f, 0, 0);
    b->FUN_00a59c60(&a);
    return b;
}
