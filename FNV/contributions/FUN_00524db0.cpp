// FUN_00524db0 v1 - worker10 one-pass transcription (history draw, fnvrec)
struct P12 {
    float x, y, z;
    void FUN_006815c0();
    void FUN_00439ef0(P12*, P12*);
    double FUN_00457990();
    P12* FUN_00416870(float, float, float);
    void FUN_0063c8a0(P12*);
    void FUN_00439180(float);
};
struct Mat36 { float m[9]; };
struct Sub461130 {
    float m[9];
    void FUN_00439f50(int, P12*);
    P12* FUN_004b4500(P12*, P12*);
};
struct GetterBase { P12* FUN_0045bb80(); };
struct NodeObj : GetterBase { Sub461130* FUN_00461130(); };
struct BSFaceGenAnimationData : GetterBase {};
struct SubA {
    virtual void Unk_00();
    virtual void Unk_01();
    virtual void Unk_02();
    virtual void Unk_03();
    virtual void Unk_04();
    virtual int vfn_14();
    unsigned int FUN_0048cee0();
};
struct Param {
    virtual void Unk_00();
    virtual void Unk_01();
    virtual void Unk_02();
    virtual void Unk_03();
    virtual void Unk_04();
    virtual void Unk_05();
    virtual void Unk_06();
    virtual void Unk_07();
    virtual void Unk_08();
    virtual void Unk_09();
    virtual void Unk_0a();
    virtual void Unk_0b();
    virtual void Unk_0c();
    virtual void Unk_0d();
    virtual void Unk_0e();
    virtual void Unk_0f();
    virtual void Unk_10();
    virtual void Unk_11();
    virtual void Unk_12();
    virtual void Unk_13();
    virtual void Unk_14();
    virtual void Unk_15();
    virtual void Unk_16();
    virtual void Unk_17();
    virtual void Unk_18();
    virtual void Unk_19();
    virtual void Unk_1a();
    virtual void Unk_1b();
    virtual void Unk_1c();
    virtual void Unk_1d();
    virtual void Unk_1e();
    virtual void Unk_1f();
    virtual void Unk_20();
    virtual void Unk_21();
    virtual void Unk_22();
    virtual void Unk_23();
    virtual void Unk_24();
    virtual void Unk_25();
    virtual void Unk_26();
    virtual void Unk_27();
    virtual void Unk_28();
    virtual void Unk_29();
    virtual void Unk_2a();
    virtual void Unk_2b();
    virtual void Unk_2c();
    virtual void Unk_2d();
    virtual void Unk_2e();
    virtual void Unk_2f();
    virtual void Unk_30();
    virtual void Unk_31();
    virtual void Unk_32();
    virtual void Unk_33();
    virtual void Unk_34();
    virtual void Unk_35();
    virtual void Unk_36();
    virtual void Unk_37();
    virtual void Unk_38();
    virtual void Unk_39();
    virtual void Unk_3a();
    virtual void Unk_3b();
    virtual void Unk_3c();
    virtual void Unk_3d();
    virtual void Unk_3e();
    virtual void Unk_3f();
    virtual bool Unk_40();
    virtual void Unk_41();
    virtual void Unk_42();
    virtual void Unk_43();
    virtual void Unk_44();
    virtual void Unk_45();
    virtual void Unk_46();
    virtual void Unk_47();
    virtual void Unk_48();
    virtual void Unk_49();
    virtual void Unk_4a();
    virtual void Unk_4b();
    virtual void Unk_4c();
    virtual void Unk_4d();
    virtual void Unk_4e();
    virtual void Unk_4f();
    virtual void Unk_50();
    virtual void Unk_51();
    virtual void Unk_52();
    virtual void Unk_53();
    virtual void Unk_54();
    virtual void Unk_55();
    virtual void Unk_56();
    virtual void Unk_57();
    virtual void Unk_58();
    virtual void Unk_59();
    virtual void Unk_5a();
    virtual void Unk_5b();
    virtual void Unk_5c();
    virtual void Unk_5d();
    virtual void Unk_5e();
    virtual void Unk_5f();
    virtual void Unk_60();
    virtual void Unk_61();
    virtual void Unk_62();
    virtual void Unk_63();
    virtual void Unk_64();
    virtual void Unk_65();
    virtual void Unk_66();
    virtual void Unk_67();
    virtual void Unk_68();
    virtual void Unk_69();
    virtual void Unk_6a();
    virtual void Unk_6b();
    virtual void Unk_6c();
    virtual void Unk_6d();
    virtual void Unk_6e();
    virtual void Unk_6f();
    virtual void Unk_70();
    virtual void Unk_71();
    virtual void Unk_72();
    virtual void Unk_73();
    virtual void* Unk_74();
    int FUN_009306d0();
    void* FUN_008d6f30();
    void* FUN_00950be0();
    bool FUN_004eaf60();
};
extern Param* DAT_011dea3c;
struct SettingObj { float* FUN_00403e20(); };
extern SettingObj DAT_011cf57c;
extern SettingObj DAT_011cf4b0;
extern SettingObj DAT_011cf498;
extern SettingObj DAT_011ce0e4;
extern SettingObj DAT_011cf1d4;
extern SettingObj DAT_011ce7c0;
struct Obj2250 { bool FUN_00525430(); };
extern Obj2250 DAT_011f2250;
extern float DAT_0101e704;
extern float DAT_010162c0;
extern P12 DAT_011a946c;
extern char DAT_0102cb00;
void* __cdecl FUN_00aa13e0(unsigned int);
struct XObj {
    static void* __cdecl operator new(unsigned int size) { return FUN_00aa13e0(size); }
    void* pEffect; void* pSource; void* pTransform; unsigned int flags; float intensity; float x; float y; float z; unsigned int lifetime;
    XObj(void*, float, int, Param*, P12*, Mat36*, P12*, P12*, float, int, int);
    void FUN_007e6580(int);
};
bool __cdecl FUN_00525420();
NodeObj* __cdecl FUN_004aae30(void*, const char*);
bool __cdecl FUN_004b61d0(P12, BSFaceGenAnimationData*, float);
float __cdecl FUN_00476b70(float, float);
void __cdecl FUN_00458620(P12*, int);
float __cdecl FUN_0040ebd0(float, float);
void __cdecl FUN_00525340(P12*);
struct ThisObj {
    SubA* FUN_004600d0();
    void FUN_00524db0(Param* param);
};

void ThisObj::FUN_00524db0(Param* param)
{
    if (param != 0) {
    if (param->Unk_40()) {
    if (this->FUN_004600d0()->FUN_0048cee0() > 0) {
    if (!FUN_00525420()) {
    P12 bufC3;
    P12 tempBCz;
    XObj* qB7;
    XObj* qA7;
    float _fa8;
    P12 vecA0;
    P12 temp6;
    float f8c2;
    P12 ob88;
    float f7c5;
    float f9;
    P12 obj14;
    int dword4;
    P12 point1;
    Mat36 matTmp;
    P12 obj34;
    bool flag7;
    P12 aVec24;
    NodeObj* node3;
    Param* paramHome8;
    void* pR;
    paramHome8 = param;
    pR = (paramHome8 == DAT_011dea3c) ? DAT_011dea3c->FUN_00950be0() : paramHome8->Unk_74();
    node3 = FUN_004aae30(pR, (const char*)&DAT_0102cb00);
    if (node3 != 0) {
    flag7 = true;
    if (!FUN_004b61d0(*node3->FUN_0045bb80(), FUN_00524c90(), DAT_0101e704))
        flag7 = false;
    node3->FUN_0045bb80()->FUN_00439ef0(&aVec24, FUN_00524c90()->FUN_0045bb80());
    if (aVec24.FUN_00457990() > *DAT_011cf57c.FUN_00403e20())
        flag7 = false;
    if (flag7) {
    dword4 = this->FUN_004600d0()->vfn_14();
    point1 = *node3->FUN_0045bb80();
    matTmp = *(Mat36*)node3->FUN_00461130();
    obj34.FUN_006815c0();
    node3->FUN_00461130()->FUN_00439f50(2, &obj34);
    f7c5 = -*DAT_011cf4b0.FUN_00403e20();
    f9 = *DAT_011cf4b0.FUN_00403e20();
    obj34.FUN_0063c8a0(tempBCz.FUN_00416870(FUN_00476b70(f7c5, f9), FUN_00476b70(f7c5, f9), FUN_00476b70(f7c5, f9)));
    obj34.FUN_00439180(*DAT_011cf498.FUN_00403e20());
    if (paramHome8->FUN_009306d0()) {
        ob88.FUN_006815c0();
        FUN_00458620(&ob88, paramHome8->FUN_009306d0() + 0x4f0);
        obj34.FUN_0063c8a0(&ob88);
    }
    obj14.FUN_006815c0();
    vecA0 = DAT_011a946c;
    _fa8 = -*DAT_011ce0e4.FUN_00403e20();
    f8c2 = *DAT_011ce0e4.FUN_00403e20();
    vecA0.FUN_00439180(1.0f + FUN_00476b70(_fa8, f8c2));
    FUN_00525340(&vecA0);
    temp6.FUN_00416870(*DAT_011cf1d4.FUN_00403e20() * vecA0.x, 0.0f, *DAT_011cf1d4.FUN_00403e20() * vecA0.z);
    obj14 = *node3->FUN_00461130()->FUN_004b4500(&bufC3, &temp6);
    if (paramHome8 == DAT_011dea3c && !DAT_011dea3c->FUN_004eaf60() && !DAT_011f2250.FUN_00525430()) {
        qA7 = new XObj(param->FUN_008d6f30(), FUN_0040ebd0(*DAT_011ce7c0.FUN_00403e20(), DAT_010162c0), dword4, param, &point1, &matTmp, &obj34, &obj14, 1.0f, 0, 1);
        qA7->FUN_007e6580(1);
    } else {
        qB7 = new XObj(param->FUN_008d6f30(), *DAT_011ce7c0.FUN_00403e20(), dword4, param, &point1, &matTmp, &obj34, &obj14, 1.0f, 0, 1);
    }
    }
    }
    }
    }
    }
    }
}
