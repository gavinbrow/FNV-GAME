struct NiPoint2 {
    float x;
    float y;
    NiPoint2() {}
    NiPoint2(float _x, float _y) : x(_x), y(_y) {}
    float Unitize();
};

struct NiPoint4 {
    float x;
    float y;
    float z;
    float w;
};

struct NiMemObject {
    void* operator new(unsigned int size);
    void operator delete(void* p, unsigned int size);
};

struct RenderTargetGroup {
    virtual void vfn_0000(); virtual void vfn_0004(); virtual void vfn_0008(); virtual void vfn_000c();
    virtual void vfn_0010(); virtual void vfn_0014(); virtual void vfn_0018(); virtual void vfn_001c();
    virtual void vfn_0020(); virtual void vfn_0024(); virtual void vfn_0028(); virtual void vfn_002c();
    virtual void vfn_0030(); virtual void vfn_0034(); virtual void vfn_0038(); virtual void vfn_003c();
    virtual void vfn_0040(); virtual void vfn_0044(); virtual void vfn_0048(); virtual void vfn_004c();
    virtual void vfn_0050(); virtual void vfn_0054(); virtual void vfn_0058(); virtual void vfn_005c();
    virtual void vfn_0060(); virtual void vfn_0064(); virtual void vfn_0068(); virtual void vfn_006c();
    virtual void vfn_0070(); virtual void vfn_0074(); virtual void vfn_0078(); virtual void vfn_007c();
    virtual void vfn_0080(); virtual void vfn_0084(); virtual void vfn_0088(); virtual void vfn_008c();
    virtual void vfn_0090(); virtual void vfn_0094(); virtual void vfn_0098(); virtual void vfn_009c();
    virtual void vfn_00a0(); virtual void vfn_00a4(); virtual void vfn_00a8(); virtual void vfn_00ac();
    virtual void vfn_00b0();
    virtual void* GetView();
};

struct BSRenderedTexture {
    RenderTargetGroup* GetGroup();
    void* FUN_004bc320();
};

struct ImageSpaceTexture {
    unsigned char flag0;
    unsigned char flag1;
    unsigned char flag2;
    int value4;
    int value8;
    int valueC;

    ImageSpaceTexture() : flag0(0), flag1(0), flag2(0), value4(0), value8(0), valueC(0) {}
    ~ImageSpaceTexture();

    BSRenderedTexture* FUN_00ba3770();
    void* GetTexture();
    void FUN_00ba3840(unsigned int);
    void FUN_00ba37a0(void*);
    void FUN_00ba3940(void*);
    void FUN_00ba39a0();
};

struct Type_00b6b380 : public NiMemObject {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    Type_00b6b380(void*, int, int, void*);
};

struct HolderForAccum {
    virtual void Dispose();
    virtual void Dispatch(void*, void*, void*, int);
    void FUN_00ba3cb0(unsigned int, void*, unsigned int);
};

struct Emitter {
    void FUN_00b8a790(int index, float x, float y, float z, float w);
    void FUN_00b8a760(int index, float x, float y, float z, float w);
};

struct NiScreenElementsData : public NiMemObject {
    virtual void Destroy();
    virtual void Release();
    long m_uiRefCount;
    int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c;

    NiScreenElementsData(bool, bool, unsigned short, int, int, int, int, int, int);
    bool FUN_00a87ae0(int, int, int);
    bool SetRectangle(int, float, float, float, float);
    void FUN_00a87900();
    bool FUN_00a88130(int, int, float, float, float, float);
};

struct NiScreenElements : public NiMemObject {
    int unk00; int unk04; int unk08; int unk0c;
    int unk10; int unk14; int unk18; int unk1c;
    int unk20; int unk24; int unk28; int unk2c;
    int unk30; int unk34; int unk38; int unk3c;
    int unk40; int unk44; int unk48; int unk4c;
    int unk50; int unk54; int unk58; int unk5c;
    int unk60; int unk64; int unk68; int unk6c;
    int unk70; int unk74; int unk78; int unk7c;
    int unk80; int unk84; int unk88; int unk8c;
    int unk90; int unk94; int unk98; int unk9c;
    int unka0; int unka4; int unka8; int unkac;
    int unkb0; int unkb4;
    NiScreenElementsData* m_spData;
    int unkbc;
    int unkc0;

    NiScreenElements(NiScreenElementsData*);
    void FUN_00a5a040();
    void Update(const void*);
    void SetName(const void*);
};

extern "C" __declspec(dllimport) long __stdcall InterlockedIncrement(volatile long*);
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);

template <class T>
struct NiPointer {
    T* m_pObject;
    NiPointer() : m_pObject(0) {}
    __forceinline NiPointer(T* p) : m_pObject(p) {
        if (m_pObject) {
            InterlockedIncrement(&m_pObject->m_uiRefCount);
        }
    }
    __forceinline ~NiPointer() {
        if (m_pObject) {
            if (InterlockedDecrement(&m_pObject->m_uiRefCount) == 0) {
                m_pObject->Release();
            }
        }
    }
    NiPointer& operator=(T* p);
    operator T*() const { return m_pObject; }
    T* operator->() const { return m_pObject; }
};

struct NiUpdateData {
    float m_fTime;
    bool b1;
    bool b2;
    bool b3;
    bool b4;
    bool b5;
    NiUpdateData(float t = 0.0f) : m_fTime(t), b1(false), b2(false), b3(false), b4(false), b5(false) {}
};

extern "C" char* __cdecl FUN_00a5b690(const char*);
extern void* DAT_0109b220;

struct NiFixedString {
    const char* m_kHandle;
    __forceinline NiFixedString(const char* s) {
        m_kHandle = FUN_00a5b690(s);
    }
    __forceinline ~NiFixedString() {
        if (m_kHandle != (const char*)DAT_0109b220) {
            InterlockedDecrement((volatile long*)(m_kHandle - 8));
        }
    }
    operator const void*() const { return &m_kHandle; }
};

struct Allocator {
    virtual void Delete0();
    virtual void Delete1();
    virtual void Free(void*);
};

struct ImageSpaceManager {
    void FUN_00b97550(int, void*, void*, void*, int, int);
};

struct GameObject {
    int unk00; int unk04; int unk08;
    HolderForAccum** nodes;
    int unk10; int unk14; int unk18;
    Emitter** emitters;
    int unk20; int unk24; int unk28;
    ImageSpaceTexture** assets;
    template<int I> ImageSpaceTexture*& GetAsset() { return assets[I]; }
    int unk30; int unk34; int unk38; int unk3C;
    int unk40; int unk44; int unk48; int unk4C;
    int unk50; int unk54;
    NiPointer<NiScreenElements> widget;
    float time;
    float previous;
    int unk64;
    float accumulated;
    float step;

    void FUN_00ba0900(void* arg1, void* arg2, int arg3, int arg4);
};

extern float DAT_010313d4;
extern float DAT_011f9410;
extern float DAT_011ffff4;
extern float DAT_010542a4;
extern float DAT_01013ea4;
extern unsigned char DAT_011fffec;
extern unsigned char DAT_011fffed;
extern unsigned char DAT_01200000;
extern int DAT_011ffffc;
extern int DAT_011ada08;
extern int DAT_011ada0c;
extern int DAT_011ada18;
extern int DAT_011ada1c;
extern NiPoint2* DAT_011ada04;
extern NiPoint2* DAT_011ada14;
extern Allocator DAT_011ada00;
extern Allocator DAT_011ada10;
extern NiPoint4 DAT_01200004;
extern NiPoint4 DAT_01200014;
extern NiPoint2 DAT_01200024;
extern NiPoint4 DAT_0120002c;
extern NiPoint4 DAT_0120003c;
extern void* DAT_011f9508;
extern ImageSpaceManager* DAT_011f91ac;

static HolderForAccum* GetNode(HolderForAccum* p) {
    void* d = p ? (void*)((char*)p - 0x6c) : 0;
    return d ? (HolderForAccum*)((char*)d + 0x6c) : 0;
}

void GameObject::FUN_00ba0900(void* arg1, void* arg2, int arg3, int arg4)
{
    if (DAT_011fffed) {
        step = DAT_010313d4;
        float nextTime = time + DAT_011f9410;
        time = nextTime;
        accumulated += nextTime;
    } else {
        step = DAT_010313d4;
        float nextTime = time + DAT_011f9410;
        time = nextTime;
        accumulated += nextTime;
    }

    ImageSpaceTexture tex54;
    ImageSpaceTexture tex64;
    ImageSpaceTexture tex34;

    tex64.FUN_00ba3840(8);

    tex34.FUN_00ba37a0(new Type_00b6b380(
        tex64.FUN_00ba3770()->FUN_004bc320(),
        0,
        1,
        GetAsset<1>()->FUN_00ba3770()->GetGroup()->GetView()
    ));

    ImageSpaceTexture tex44;

    if (DAT_011fffec) {
        HolderForAccum* node = GetNode(nodes[0]);
        Emitter* emit = emitters[0];

        node->FUN_00ba3cb0(0, &tex34, 0);
        node->FUN_00ba3cb0(1, assets[1], 1);
        node->Dispatch(arg1, arg2, emit, 1);

        tex44.FUN_00ba3940(assets[1]);
        tex54.FUN_00ba3940(&tex34);
        tex34.FUN_00ba3940(&tex44);
        DAT_011fffec = 0;
    }

    if (DAT_011fffed) {
        HolderForAccum* node = GetNode(nodes[1]);
        Emitter* emit = emitters[1];

        emit->FUN_00b8a790(0, time, 0.0f, 0.0f, 0.0f);
        emit->FUN_00b8a790(1, DAT_011ffff4, 0.0f, 0.0f, 0.0f);
        emit->FUN_00b8a790(2, DAT_01200024.x, DAT_01200024.y, 0.0f, 0.0f);
        emit->FUN_00b8a790(4, DAT_01200004.x, DAT_01200004.y, DAT_01200004.z, DAT_01200004.w);
        emit->FUN_00b8a790(5, DAT_01200014.x, DAT_01200014.y, DAT_01200014.z, DAT_01200014.w);

        node->FUN_00ba3cb0(0, &tex34, 0);
        node->FUN_00ba3cb0(1, assets[1], 0);
        node->Dispatch(arg1, arg2, emit, 1);

        if (DAT_011fffed) {
            DAT_011ffffc = 0;
            HolderForAccum* handler = GetNode(nodes[2]);
            Emitter* secondary = emitters[2];
            handler->FUN_00ba3cb0(0, &tex34, 0);

            if ((unsigned int)DAT_011ada08 > 0) {
                if (!widget.m_pObject) {
                    NiPointer<NiScreenElementsData> spData(new NiScreenElementsData(false, false, 1, 1, 1, 4, 1, 2, 1));
                    widget = new NiScreenElements(spData);

                    NiScreenElementsData* localData0 = widget->m_spData; localData0->FUN_00a87ae0(4, 0, 0);
                    NiScreenElementsData* localData1 = widget->m_spData; localData1->SetRectangle(0, 0.0f, DAT_01013ea4, 1.0f, DAT_010542a4);
                    widget->m_spData->FUN_00a87900();
                    NiScreenElementsData* localData2 = widget->m_spData; localData2->FUN_00a88130(0, 0, 0.0f, 0.0f, 1.0f, 1.0f);
                    widget->FUN_00a5a040();

                    NiUpdateData kData(0.0f);
                    widget->Update(&kData);

                    widget->SetName(NiFixedString("Partial Screen Trishape"));
                }

                for (int i = 0; i < DAT_011ada08; ++i) {
                    NiPoint2* endpoint = &DAT_011ada14[i];
                    DAT_0120002c.x = DAT_011ada04[i].x - DAT_011ada14[i].x;
                    DAT_0120003c.x = DAT_011ada04[i].y - endpoint->y;
                    DAT_0120002c.z = DAT_011ada14[i].x;
                    NiPoint2 tangent;
                    tangent.x = -DAT_0120003c.x;
                    tangent.y = DAT_0120002c.x;
                    tangent.Unitize();
                    DAT_0120002c.y = tangent.x;
                    DAT_0120003c.y = tangent.y;
                    DAT_0120003c.z = endpoint->y;
                    secondary->FUN_00b8a760(0, DAT_0120002c.x, DAT_0120002c.y, DAT_0120002c.z, DAT_0120002c.w);
                    secondary->FUN_00b8a760(1, DAT_0120003c.x, DAT_0120003c.y, DAT_0120003c.z, DAT_0120003c.w);
                    handler->Dispatch(widget, arg2, secondary, 1);
                    ++DAT_011ffffc;
                }

                if (DAT_011ada04) {
                    Allocator* a = &DAT_011ada00; a->Free(DAT_011ada04);
                    DAT_011ada04 = 0;
                    DAT_011ada0c = 0;
                    DAT_011ada08 = 0;
                }
                if (DAT_011ada14) {
                    Allocator* a = &DAT_011ada10; a->Free(DAT_011ada14);
                    DAT_011ada14 = 0;
                    DAT_011ada1c = 0;
                    DAT_011ada18 = 0;
                }
            }
        }
    }

    DAT_01200000 = 0;
    tex44.FUN_00ba3940(assets[1]);
    tex54.FUN_00ba3940(&tex34);
    tex34.FUN_00ba3940(&tex44);

    int frames = 0;
    while (time - previous > step) {
        previous = previous + step;
        if (DAT_011fffed) {
            ++frames;
            HolderForAccum* node = GetNode(nodes[4]);
            Emitter* emit = emitters[4];
            emit->FUN_00b8a790(0, time, 0.0f, 0.0f, 0.0f);
            emit->FUN_00b8a790(1, DAT_011ffff4, 0.0f, 0.0f, 0.0f);
            emit->FUN_00b8a790(2, DAT_01200024.x, DAT_01200024.y, 0.0f, 0.0f);
            emit->FUN_00b8a790(4, DAT_01200004.x, DAT_01200004.y, DAT_01200004.z, DAT_01200004.w);
            emit->FUN_00b8a790(5, DAT_01200014.x, DAT_01200014.y, DAT_01200014.z, DAT_01200014.w);
            node->FUN_00ba3cb0(0, &tex34, 0);
            node->FUN_00ba3cb0(1, &tex54, 1);
            node->Dispatch(arg1, arg2, emit, 1);
            DAT_01200000 = 1;
            tex44.FUN_00ba3940(&tex54);
            tex54.FUN_00ba3940(&tex34);
            tex34.FUN_00ba3940(&tex44);
        }
    }

    if (frames % 2 == 0) {
        void* renderer = DAT_011f9508;
        ImageSpaceManager* mgr = DAT_011f91ac;
        mgr->FUN_00b97550(0x22, renderer, tex54.FUN_00ba3770(), tex34.FUN_00ba3770(), 0, 1);
    }

    if (tex64.GetTexture()) {
        tex64.FUN_00ba39a0();
    }
}
