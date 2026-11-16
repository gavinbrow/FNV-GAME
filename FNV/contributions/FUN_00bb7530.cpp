#include <windows.h>

struct NiRefObject {
    virtual void vf00();
    virtual void DeleteThis();
    volatile long refCount;
    NiRefObject() : refCount(0) {}
    static void* operator new(unsigned int size);
    void IncRefCount() { InterlockedIncrement(&refCount); }
    void DecRefCount() { if (!InterlockedDecrement(&refCount)) DeleteThis(); }
};

template <class T> struct NiPointer {
    T* ptr;
    NiPointer() : ptr(0) {}
    NiPointer(T* p) : ptr(p) { if (ptr) ptr->IncRefCount(); }
    ~NiPointer() { if (ptr) ptr->DecRefCount(); }
    void Release() {
        T* old = ptr;
        if (old) {
            volatile long& refs = old->refCount;
            if (!InterlockedDecrement(&refs)) old->DeleteThis();
            ptr = 0;
        }
    }
    NiPointer& operator=(T* p) {
        T* old = ptr;
        if (old != p) {
            if (old) old->DecRefCount();
            ptr = p;
            p->IncRefCount();
        }
        return *this;
    }
    operator T*() const { return ptr; }
    T* operator->() const { return ptr; }
};

extern char* DAT_0109b220;

struct NiFixedString {
    char* handle;
    NiFixedString(char* h) : handle(h) {}
    ~NiFixedString() { if (handle != DAT_0109b220) InterlockedDecrement((volatile long*)(handle - 8)); }
};
struct NiGlobalStringTable { static char* __cdecl AddString(const char*); };

struct BSRenderedTexture : NiRefObject { };
struct ImageSpaceTexture { BSRenderedTexture* FUN_00ba3770(); };

struct NiScreenElementsData {
    static void* operator new(unsigned int size);
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    NiScreenElementsData(bool a, bool b, unsigned short c, int d, int e, int f, int g, int h, int i);
    bool FUN_00a87ae0(int a, int b, int c);
    bool SetRectangle(int i, float a, float b, float c, float d);
    void FUN_00a87900();
    bool FUN_00a88130(int i, int j, float a, float b, float c, float d);
    void FUN_00a67050(int a);
};

struct NiUpdateData {
    float fTime;
    bool b0, b1, b2, b3, b4;
    NiUpdateData() : fTime(0.0f), b0(false), b1(false), b2(false), b3(false), b4(false) {}
};

struct HudOwner;
struct ScreenSink;

struct NiScreenElements : NiRefObject {
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
    int unk6c;
    int unk70;
    int unk74;
    int unk78;
    int unk7c;
    int unk80;
    int unk84;
    int unk88;
    int unk8c;
    int unk90;
    int unk94;
    int unk98;
    int unk9c;
    int unka0;
    int unka4;
    int unka8;
    int unkac;
    int unkb0;
    int unkb4;
    NiScreenElementsData* unkb8;
    int unkbc;
    HudOwner* unkc0;
    NiScreenElements(NiScreenElementsData* d);
    void FUN_00a5b950(NiFixedString* s);
    void FUN_00a5a040();
    void FUN_00a59c60(NiUpdateData* u);
    void FUN_00a87790(ScreenSink* s);
};

struct ColorA {
    float a, b, c, d;
    ColorA(float a_, float b_, float c_, float d_) : a(a_), b(b_), c(c_), d(d_) {}
};

struct ScreenSink {
    virtual void vf00();
    virtual void vf01();
    virtual void vf02();
    virtual void vf03();
    virtual void vf04();
    virtual void vf05();
    virtual void vf06();
    virtual void vf07();
    virtual void vf08();
    virtual void vf09();
    virtual void vf0a();
    virtual void vf0b();
    virtual void vf0c();
    virtual void vf0d();
    virtual void vf0e();
    virtual void vf0f();
    virtual void vf10();
    virtual void vf11();
    virtual void vf12();
    virtual void vf13();
    virtual void vf14();
    virtual void vf15();
    virtual void vf16();
    virtual void vf17();
    virtual void vf18();
    virtual void vf19();
    virtual void vf1a();
    virtual void vf1b();
    virtual void vf1c();
    virtual void vf1d();
    virtual void vf1e();
    virtual void vf1f();
    virtual void vf20();
    virtual void vf21();
    virtual void vf22();
    virtual void vf23();
    virtual void vf24();
    virtual void vf25();
    virtual void vf26();
    virtual void vf27();
    virtual void vf28();
    virtual void vf29();
    virtual void vf2a();
    virtual void vf2b();
    virtual void vf2c();
    virtual void vf2d();
    virtual void vf2e();
    virtual void vf2f();
    virtual void vf30();
    virtual void vf31();
    virtual void vf32();
    virtual void vf33();
    virtual void vf34();
    virtual void vf35();
    virtual void vf36();
    virtual void vf37();
    virtual void vf38();
    virtual void vf39();
    virtual void vf3a();
    virtual void vf3b();
    virtual void vf3c();
    virtual void vf3d();
    virtual void vf3e();
    virtual void vf3f();
    virtual void vf40();
    virtual void vf41();
    virtual void vf42();
    virtual void vf43();
    virtual void vf44();
    virtual void vf45();
    virtual void vf46();
    virtual void vf47();
    virtual void vf48();
    virtual void vf49();
    virtual void vf4a();
    virtual void vf4b();
    virtual void vf4c();
    virtual void vf4d();
    virtual void vf4e();
    virtual void vf4f();
    virtual void vf50();
    virtual void vf51();
    virtual void vf52();
    virtual void vf53();
    virtual void vf54();
    virtual void vf55();
    virtual void vf56();
    virtual void vf57();
    virtual void vf58();
    virtual void vf59();
    virtual void vf5a();
    virtual void vf5b();
    virtual void vf5c();
    virtual void vf5d();
    virtual void vf5e();
    virtual void vf5f();
    virtual void vf60();
    virtual void vf61();
    virtual void vf62();
    virtual void vf63();
    virtual void vf64(ColorA* c);
    char unk04[0x1fc];
    int unk200;
    int unk204;
    bool unk208;
};

struct GlobalA {
    char unk00[0x200];
    NiPointer<NiScreenElements> unk200;
};

struct Rect4 { float x, y, w, h; };
struct HudParam { int unk00; };
struct RecEntry { float f00, f04, f08, f0c, f10, f14; };

struct SurfaceInfo { int unk00; int unk04; unsigned width; unsigned height; };
struct SurfaceHolder {
    virtual void vf00();
    virtual void vf01();
    virtual void vf02();
    virtual void vf03();
    virtual void vf04();
    virtual void vf05();
    virtual void vf06();
    virtual void vf07();
    virtual void vf08();
    virtual void vf09();
    virtual void vf0a();
    virtual void vf0b();
    virtual void vf0c();
    virtual void vf0d();
    virtual void vf0e();
    virtual void vf0f();
    virtual void vf10();
    virtual void vf11();
    virtual void vf12();
    virtual void vf13();
    virtual void vf14();
    virtual void vf15();
    virtual void vf16();
    virtual void vf17();
    virtual void vf18();
    virtual void vf19();
    virtual void vf1a();
    virtual void vf1b();
    virtual void vf1c();
    virtual void vf1d();
    virtual void vf1e();
    virtual void vf1f();
    virtual void vf20();
    virtual void vf21();
    virtual void vf22();
    virtual void vf23();
    virtual void vf24();
    virtual void vf25();
    virtual void vf26();
    virtual void vf27();
    virtual void vf28();
    virtual void vf29();
    virtual void vf2a();
    virtual void vf2b();
    virtual SurfaceInfo* vf2c(int i);
};
struct SurfaceOwner {
    virtual void vf00();
    virtual void vf01();
    virtual void vf02();
    virtual void vf03();
    virtual void vf04();
    virtual void vf05();
    virtual void vf06();
    virtual void vf07();
    virtual void vf08();
    virtual void vf09();
    virtual void vf0a();
    virtual void vf0b();
    virtual void vf0c();
    virtual void vf0d();
    virtual void vf0e();
    virtual void vf0f();
    virtual void vf10();
    virtual void vf11();
    virtual void vf12();
    virtual void vf13();
    virtual void vf14();
    virtual void vf15();
    virtual void vf16();
    virtual void vf17();
    virtual void vf18();
    virtual void vf19();
    virtual void vf1a();
    virtual void vf1b();
    virtual void vf1c();
    virtual void vf1d();
    virtual void vf1e();
    virtual void vf1f();
    virtual void vf20();
    virtual void vf21();
    virtual void vf22();
    virtual void vf23();
    virtual void vf24();
    virtual void vf25();
    virtual void vf26();
    virtual void vf27();
    virtual void vf28();
    virtual void vf29();
    virtual void vf2a();
    virtual void vf2b();
    virtual void vf2c();
    virtual void vf2d();
    virtual void vf2e();
    virtual void vf2f();
    virtual void vf30();
    virtual void vf31();
    virtual SurfaceHolder* vf32();
    unsigned GetWidth() {
        SurfaceHolder* h = vf32();
        if (!h) return 0;
        SurfaceInfo* s = h->vf2c(0);
        if (!s) return 0;
        return s->width;
    }
    unsigned GetHeight() {
        SurfaceHolder* h = vf32();
        if (!h) return 0;
        SurfaceInfo* s = h->vf2c(0);
        if (!s) return 0;
        return s->height;
    }
};

struct HudBase {
    int FUN_00c03c80();
    virtual void vf00();
    virtual void vf01();
    virtual void vf02();
    virtual void vf03();
    virtual void vf04();
    virtual void vf05();
    virtual void vf06();
    virtual void vf07();
    virtual void vf08();
    virtual void vf09();
    virtual void vf0a();
    virtual void vf0b();
    virtual void vf0c();
    virtual void vf0d();
    virtual void vf0e();
    virtual void vf0f();
    virtual void vf10();
    virtual void vf11();
    virtual void vf12();
    virtual void vf13();
    virtual void vf14(NiScreenElements* s);
    virtual void vf15();
    virtual void vf16();
    virtual void vf17();
    virtual void vf18();
    virtual void vf19();
    virtual void vf1a();
    virtual void vf1b();
    virtual void vf1c();
    virtual void vf1d();
    virtual void vf1e();
    virtual void vf1f();
    virtual void vf20();
    virtual void vf21();
    virtual void vf22();
    virtual void vf23();
    virtual void vf24();
    virtual void vf25();
    virtual void vf26();
    virtual void vf27();
    virtual void vf28();
    virtual void vf29();
    virtual void vf2a();
    virtual void vf2b();
    virtual void vf2c();
    virtual void vf2d();
    virtual void vf2e();
    virtual void vf2f();
    virtual void vf30();
    virtual void vf31();
    virtual void vf32();
    virtual void vf33();
    virtual void vf34();
    virtual void vf35();
    virtual void vf36();
    virtual void vf37();
    virtual void vf38();
    virtual void vf39();
    virtual void vf3a();
    virtual void vf3b();
    virtual void vf3c();
    virtual void vf3d();
    virtual void vf3e();
    virtual void vf3f();
    virtual void vf40();
    virtual void vf41();
    virtual void vf42();
    virtual void vf43();
    virtual void vf44();
    virtual void vf45();
    virtual void vf46();
    virtual void vf47();
    virtual void vf48();
    virtual void vf49();
    virtual void vf4a();
    virtual void vf4b();
    virtual void vf4c();
    virtual void vf4d();
    virtual void vf4e();
    virtual void vf4f();
    virtual void vf50();
    virtual void vf51();
    virtual void vf52(HudParam* p);
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    int unk2c;
    int unk30;
    int unk34;
    int unk38;
    int unk3c;
    int unk40;
    int unk44;
    int unk48;
    int unk4c;
    int unk50;
    int unk54;
    int unk58;
    int unk5c;
    int unk60;
    int unk64;
    int unk68;
};

extern float DAT_012007d0;
extern float DAT_012007d4;

static inline void Remap(float& x, float& y, float& w, float& h, float u, float v, float& e0, float& e1)
{
    x = 2.0 * x - 1.0 + DAT_012007d0;
    y = 1.0 - 2.0 * y - DAT_012007d4;
    e0 = w + u;
    e1 = h + v;
    w = 2.0 * w;
    h = 2.0 * -h;
}

struct HudInner {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    int unk10;
    int unk14;
    int unk18;
    int unk1c;
    int unk20;
    int unk24;
    int unk28;
    ImageSpaceTexture** unk2c;
    void FUN_00bb7530(int a1, SurfaceOwner* a2, HudParam* a3, int a4);
};

struct HudOwner : HudBase, HudInner { };

extern unsigned short DAT_011ae5e2;
extern bool DAT_011ae5d4;
extern RecEntry** DAT_011ae5dc;
extern GlobalA* DAT_011f91ac;
extern ScreenSink* DAT_011f4748;
extern HudParam DAT_01202410;

void HudInner::FUN_00bb7530(int a1, SurfaceOwner* a2, HudParam* a3, int a4)
{
    ColorA color(0.0f, 1.0f, 1.0f, 0.0f);
    if (DAT_011ae5e2 != 0) {
        HudParam* p = a3;
        if (p == 0) p = &DAT_01202410;
        if (DAT_011ae5d4) {
            NiPointer<BSRenderedTexture> tex = (*unk2c)->FUN_00ba3770();
            DAT_011f91ac->unk200.Release();
            NiScreenElements* se = new NiScreenElements(new NiScreenElementsData(false, false, 1, 1, 1, 4, 1, 2, 1));
            int i = 0;
            for (i = 0; i < DAT_011ae5e2; i++) {
                unsigned w = a2->GetWidth();
                unsigned h = a2->GetHeight();
                float aspect = (float)w / (float)h;
                aspect = aspect / 1.3333333730697632;
                se->unkb8->FUN_00a87ae0(4, 0, 0);
                RecEntry* r = DAT_011ae5dc[i];
                double A = aspect * 1280.0;
                float qx = r->f10 / A;
                float qy = r->f14 / 960.0;
                float qw = r->f08 / A;
                float qh = r->f0c / 960.0;
                float v4 = r->f00 / A;
                float v5 = r->f04 / 960.0;
                float x2 = 2.0 * qx - 1.0 + DAT_012007d0;
                float y2 = 1.0 - 2.0 * qy - DAT_012007d4;
                float w2 = 2.0 * qw;
                float h2 = 2.0 * -qh;
                float e0 = qw + v4;
                float e1 = qh + v5;
                se->unkb8->SetRectangle(i, x2, y2, w2, h2);
                se->unkb8->FUN_00a87900();
                NiScreenElementsData* d2 = se->unkb8;
                d2->FUN_00a88130(i, 0, v4, v5, e0, e1);
                se->unkb8->FUN_00a67050(0);
                NiFixedString name(NiGlobalStringTable::AddString("Interface: HUD Unpack Geometry"));
                se->FUN_00a5b950(&name);
            }
            se->FUN_00a5a040();
            NiUpdateData ud;
            se->FUN_00a59c60(&ud);
            se->unkc0 = (HudOwner*)((char*)this - 0x6c);
            DAT_011f91ac->unk200 = se;
        }
        NiScreenElements* spr = DAT_011f91ac->unk200;
        HudOwner* o = (HudOwner*)((char*)this - 0x6c);
        o->vf14(spr);
        o->vf52(p);
        o->FUN_00c03c80();
        if (DAT_011f4748->unk200 == 1 || DAT_011f4748->unk200 == 2) {
            if (DAT_011f4748->unk208 == true) DAT_011f4748->vf64(&color);
        }
        spr->FUN_00a87790(DAT_011f4748);
        DAT_011ae5d4 = false;
    }
}
