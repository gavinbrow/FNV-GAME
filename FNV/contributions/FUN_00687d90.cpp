struct NiFixedString;
struct NiPoint2 { float x; float y; };
struct NiObj;
struct NiAVObject;
struct DPoint;
struct DBone;
struct DNewPartition;
struct DGeometry;
struct ObjC;
struct ObjD;

unsigned char __cdecl FUN_0043b300(const NiRTTI* rtti, NiAVObject* obj);
void __cdecl FUN_00b57e30(void* a, int b, int c);
extern const NiRTTI DAT_011f444c;

struct GO
{
    NiObj* m_p;
    GO(int a);
    ~GO();
    operator NiObj*() const;
};
struct PtrHolder
{
    void* FUN_0066b0d0(void* p);
};
struct VSub
{
    virtual void f00();
    virtual void f01();
    virtual void f02();
    virtual void f03();
    virtual void f04();
    virtual void f05();
    virtual void f06();
    virtual void f07();
    virtual void f08();
    virtual void f09();
    virtual void f10();
    virtual void f11();
    virtual void f12();
    virtual void f13();
    virtual void f14();
    virtual void f15();
    virtual void f16();
    virtual void f17();
    virtual void f18();
    virtual void f19();
    virtual void f20();
    virtual void f21();
    virtual void f22();
    virtual void f23();
    virtual void f24();
    virtual void f25();
    virtual void f26();
    virtual void f27();
    virtual void f28();
    virtual void f29();
    virtual void f30();
    virtual void f31();
    virtual void f32();
    virtual void f33();
    virtual void f34();
    virtual void f35();
    virtual void v36(int a, GO* s);
};
struct VSubOwner
{
    int f00; int f04; int f08; int f0c; int f10; int f14; int f18; int f1c; int f20; int f24; int f28; int f2c;
    VSub sub;
};
struct NiTriShape
{
    virtual void v00();
    virtual void v01();
    virtual void v02();
    virtual void v03();
    virtual void v04();
    virtual void v05();
    virtual void v06();
    virtual void v07();
    virtual void v08();
    virtual void v09();
    virtual void v10();
    virtual void v11();
    virtual void v12();
    virtual void v13();
    virtual void v14();
    virtual void v15();
    virtual void v16();
    virtual void v17();
    virtual void v18();
    virtual void v19();
    virtual void v20();
    virtual void v21();
    virtual void v22();
    virtual void v23();
    virtual void v24();
    virtual void v25();
    virtual void v26();
    virtual void v27();
    virtual void v28();
    virtual void v29();
    virtual void v30();
    virtual void v31();
    virtual void v32();
    virtual void v33();
    virtual void v34();
    virtual void v35();
    virtual void v36();
    virtual void v37();
    virtual void v38();
    virtual void v39();
    virtual void v40();
    virtual void v41();
    virtual void v42();
    virtual void v43();
    virtual void v44();
    virtual void v45();
    virtual void v46();
    virtual void v47();
    int tf04;
    int tf08;
    int tf0c;
    int tf10;
    int tf14;
    int tf18;
    int tf1c;
    int tf20;
    int tf24;
    int tf28;
    int tf2c;
    int tf30;
    int tf34;
    int tf38;
    int tf3c;
    int tf40;
    int tf44;
    int tf48;
    int tf4c;
    int tf50;
    int tf54;
    int tf58;
    int tf5c;
    int tf60;
    int tf64;
    int tf68;
    int tf6c;
    int tf70;
    int tf74;
    int tf78;
    int tf7c;
    int tf80;
    int tf84;
    int tf88;
    int tf8c;
    int tf90;
    int tf94;
    int tf98;
    int tf9c;
    int tfa0;
    int tfa4;
    int tfa8;
    int tfac;
    int tfb0;
    int tfb4;
    int tfb8;
    int tfbc;
    int tfc0;
    static void* operator new(unsigned int n);
    NiTriShape(unsigned short a, NiPoint3* c, NiPoint3* d, void* z1, NiPoint2* z2, unsigned short z3, unsigned int z4, unsigned short div, unsigned short* e);
    void FUN_00a5b950(const NiFixedString& s);
    void FUN_00439410(void* b);
    void* FUN_005495f0(ObjC* c, int a, int b, int d, int e, int f, int g);
    void FUN_004adde0(ObjD* d);
    void FUN_00440460(int v);
    void FUN_0043fa80(int v);
    void FUN_00440490(float v);
    void FUN_004f00e0(int v);
    void FUN_00688430(NineDw* p);
    void FUN_006427a0(float v);
    void FUN_00a5a040();
};
struct ObjB
{
    int u00;
    int u04;
    int u08;
    int u0c;
    int u10;
    int u14;
    int u18;
    int u1c;
    int u20;
    int u24;
    int u28;
    int u2c;
    int u30;
    int u34;
    int u38;
    int u3c;
    int u40;
    int u44;
    int u48;
    int u4c;
    int u50;
    int u54;
    int u58;
    int u5c;
    int u60;
    int u64;
    int u68;
    int u6c;
    int u70;
    int u74;
    int u78;
    PtrHolder m_7c;
    int w80;
    int w84;
    int w88;
    int w8c;
    int w90;
    int w94;
    int w98;
    int w9c;
    int wa0;
    int wa4;
    int wa8;
    int wac;
    int wb0;
    int wb4;
    int wb8;
    int wbc;
    int wc0;
    int wc4;
    int wc8;
    int wcc;
    int wd0;
    static void* operator new(unsigned int n);
    ObjB();
    void FUN_004ee4b0(float f);
};
struct SkinDataX
{
    int FUN_008041a0();
    int FUN_0048d150(DPoint* p);
};
struct SkinX
{
    SkinDataX* FUN_005585e0();
    int* FUN_00825c00();
    int FUN_0044edb0();
};
struct ObjC
{
    int cf00;
    int cf04;
    int cf08;
    int cf0c;
    int cf10;
    int cf14;
    int cf18;
    int cf1c;
    int cf20;
    int cf24;
    int cf28;
    int cf2c;
    int cf30;
    int cf34;
    int cf38;
    int cf3c;
    int cf40;
    int cf44;
    static void* operator new(unsigned int n);
    ObjC(int partList, DBone* bone, int x);
};
struct ObjD
{
    virtual ~ObjD();
    int df04;
    int df08;
    int df0c;
    int df10;
    int df14;
    int df18;
    int df1c;
    int df20;
    int df24;
    int df28;
    int df2c;
    int df30;
    int df34;
    int df38;
    int df3c;
    static void* operator new(unsigned int n);
    ObjD(ObjC* c, int x, int* arr, Entry4* textObj, int n);
    void FUN_004addc0(void* p);
};
struct ObjE
{
    virtual ~ObjE();
    int ef04; int ef08; int ef0c;
    static void* operator new(unsigned int n);
    ObjE();
    unsigned char FUN_00a84980(void* p);
};
struct GeomX
{
    int FUN_0043c490();
    int FUN_006a9540();
    float FUN_009cdae0();
    int FUN_0045bb80();
    NineDw* FUN_00461130();
    float FUN_008d01e0();
};

void DDecal::FUN_00687d90(DGeometry* geom, unsigned short a, unsigned short b, DPoint* c, DPoint* d, unsigned short* e, DBone* bone, DNewPartition* newPart, unsigned short* h)
{
    NiTriShape* objA = new NiTriShape(a, (NiPoint3*)c, (NiPoint3*)d, 0, 0, 0, 0, b / 3, e);
    objA->FUN_00a5b950(*FUN_00688460());
    ObjB* entries;
    entries = new ObjB();
    objA->FUN_00439410(entries);
    entries->FUN_004ee4b0(1.0f);
    GO strLocal(0);
    ((VSubOwner*)unk58)->sub.v36(0, &strLocal);
    NiObj* partCount;
    partCount = strLocal;
    if (FUN_0043b300(&DAT_011f444c, (NiAVObject*)partCount))
        entries->m_7c.FUN_0066b0d0(partCount);
    SkinX* count;
    count = (SkinX*)geom->FUN_0043fad0();
    int objD;
    objD = count->FUN_005585e0()->FUN_008041a0();
    ObjC* textObj;
    textObj = new ObjC(objD, bone, count->FUN_005585e0()->FUN_0048d150(c));
    int* s;
    s = count->FUN_00825c00();
    long objC;
    int* partList = new int[objD];
    for (objC = 0; objC < objD; objC++)
        partList[objC] = s[objC];
    int skin;
    skin = 0;
    unsigned int vertexMap[15];
    if (newPart)
    {
        skin = (int)((DPartitionData*)newPart)->FUN_0044ddc0();
    }
    else
    {
        long idx;
        idx = 2;
        for (unsigned int bitIdx = 0; bitIdx < 15; bitIdx++)
        {
            if (bodyParts & idx)
            {
                vertexMap[skin] = bitIdx;
                skin++;
            }
            idx = idx << 1;
        }
    }
    Entry4* kIter;
    kIter = new Entry4[skin];
    {
    long j;
    for (j = 0; j < skin; j++)
    {
        kIter[j].b0 = 1;
        kIter[j].b1 = 1;
        if (h)
            kIter[j].w = h[j];
        else
            kIter[j].w = (unsigned short)vertexMap[j];
    }
    }
    ObjD* arr1 = new ObjD(textObj, count->FUN_0044edb0(), partList, kIter, skin);
    if (newPart)
    {
        arr1->FUN_004addc0(newPart);
        objA->FUN_004adde0(arr1);
    }
    else
    {
        ObjE* val;
        val = new ObjE();
        if (val->FUN_00a84980(objA->FUN_005495f0(textObj, 0x12, 4, 1, 0, 0, 0)))
        {
            arr1->FUN_004addc0(val);
            objA->FUN_004adde0(arr1);
        }
        else
        {
            delete val;
            delete arr1;
        }
    }
    objA->FUN_00440460(((GeomX*)geometry.FUN_00559450())->FUN_0043c490());
    objA->FUN_0043fa80(((GeomX*)geometry.FUN_00559450())->FUN_006a9540());
    objA->FUN_00440490(((GeomX*)geometry.FUN_00559450())->FUN_009cdae0());
    objA->FUN_004f00e0(((GeomX*)geometry.FUN_00559450())->FUN_0045bb80());
    objA->FUN_00688430(((GeomX*)geometry.FUN_00559450())->FUN_00461130());
    objA->FUN_006427a0(((GeomX*)geometry.FUN_00559450())->FUN_008d01e0());
    objA->v47();
    objA->FUN_00a5a040();
    FUN_00b57e30(objA, 0, 0);
    ((PtrHolder*)&unk1c)->FUN_0066b0d0(objA);
    unk20 = (int)geometry.FUN_00559450();}
