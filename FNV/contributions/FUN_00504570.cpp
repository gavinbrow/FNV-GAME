// Structural layout informed by a prior contributor's unverified October 22, 2026 attempt.
// This destructor reconstruction and exact-match check are independently verified.
struct Primary_504570 {
    virtual void v00();
    virtual void v01();
    virtual void v02();
    unsigned int a04, a08, a0c, a10, a14;
    void FUN_00483630();
    ~Primary_504570() { FUN_00483630(); }
};
struct Secondary_504570 {
    virtual void v00();
    unsigned int b04;
    void FUN_00591300();
    ~Secondary_504570() { FUN_00591300(); }
};
struct Elem32_504570 {
    int a0, a4, a8, ac, a10, a14, a18, a1c;
    void FUN_0048a490();
    ~Elem32_504570() { FUN_0048a490(); }
};
struct Elem12_504570 {
    int a0, a4, a8;
    void FUN_0048e2e0();
    ~Elem12_504570() { FUN_0048e2e0(); }
};
struct FUN_00504570_cls : Primary_504570, Secondary_504570 {
    unsigned int unk20;
    Elem32_504570 models[10];
    Elem12_504570 textures[11];
    void FUN_00504620();
    ~FUN_00504570_cls();
};
FUN_00504570_cls::~FUN_00504570_cls() {
    FUN_00504620();
}