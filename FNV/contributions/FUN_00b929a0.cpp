struct FUN_00b929a0_str16 { const char* a; const char* b; int c; int d; };
struct FUN_00b929a0_obj {
    int m_00; int m_04; int m_08; int m_0c; int m_10; int m_14; int m_18; int m_1c;
    int m_20; int m_24; int m_28; int m_2c; int m_30; int m_34; int m_38;
};
int __cdecl FUN_00b4f380(int x);
void __cdecl FUN_00ec61c0(void* p, int z, unsigned int n);
class FUN_00b929a0_cls {
public:
    virtual void v00(); virtual void v01(); virtual void v02(); virtual void v03();
    virtual void v04(); virtual void v05(); virtual void v06(); virtual void v07();
    virtual void v08(); virtual void v09(); virtual void v0a(); virtual void v0b();
    virtual void v0c(); virtual void v0d(); virtual void v0e(); virtual void v0f();
    virtual void v10(); virtual void v11(); virtual void v12(); virtual void v13();
    virtual void v14(); virtual void v15(); virtual void v16(); virtual void v17();
    virtual void v18(); virtual void v19(); virtual void v1a(); virtual void v1b();
    virtual void v1c(); virtual void v1d(); virtual void v1e(); virtual void v1f();
    virtual void v20(); virtual void v21(); virtual void v22(); virtual void v23();
    virtual void v24(); virtual void v25(); virtual void v26(); virtual void v27();
    virtual void v28(); virtual void v29(); virtual void v2a(); virtual void v2b();
    virtual void v2c(); virtual void v2d(); virtual void v2e(); virtual void v2f();
    virtual void v30(); virtual void v31(); virtual void v32(); virtual void v33();
    virtual void v34(); virtual void v35(); virtual void v36(); virtual void v37();
    virtual void v38(); virtual void v39(); virtual void v3a(); virtual void v3b();
    virtual void v3c(); virtual void v3d(); virtual void v3e(); virtual void v3f();
    virtual void v40(); virtual void v41(); virtual void v42(); virtual void v43();
    virtual void v44(); virtual void v45(); virtual void v46(); virtual void v47();
    virtual void v48(); virtual void v49(); virtual void v4a(); virtual void v4b();
    virtual void v4c(); virtual void v4d(); virtual void v4e();
    virtual void v4f(void* a, void* b, const char* c, const char* d, int e);
    virtual void v50(); virtual void v51(); virtual void v52();
    virtual void v53();
    void FUN_00b929a0();
};
void FUN_00b929a0_cls::FUN_00b929a0() {
    struct Frame {
        FUN_00b929a0_str16 s2; FUN_00b929a0_obj o2;
        FUN_00b929a0_str16 s1; FUN_00b929a0_obj o1;
    } f;
    f.s1.a = "water\\2_ab\\v\\displace.v.hlsl";
    f.s1.b = "RIPPLE_MAKER_WADING";
    f.s1.c = 0;
    f.s1.d = 0;
    FUN_00ec61c0(&f.o1, 0, sizeof(f.o1));
    f.s2.a = "water\\2_ab\\p\\displace.p.hlsl";
    f.s2.b = "RIPPLE_MAKER_WADING";
    f.s2.c = 0;
    f.s2.d = 0;
    FUN_00ec61c0(&f.o2, 0, sizeof(f.o2));
    int r = FUN_00b4f380(1);
    this->v4f(&f.s1, &f.s2, "WATERDISPLACEMENTWADINGRIPPLE", "vs_1_1", r);
    this->v53();
}




