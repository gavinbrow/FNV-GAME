struct StageReturn
{
    int f00;
    int f04;
    int f08;
    int f0c;
    int f10;
    int f14;
    int f18;
    int f1c;
    int f20;
    int f24;
    int f28;
    int f2c;
    int f30;
    int f34;
    int f38;
    int f3c;
    int f40;
    int f44;
    int f48;
    int f4c;
    int f50;
    int f54;
    int f58;
    int f5c;
    int m_iRefCount;
    void ReturnToPool();
    void DecRefCount()
    {
        --m_iRefCount;
        if (m_iRefCount == 0)
            ReturnToPool();
    }
};

void __cdecl FUN_00e7edf0(StageReturn*& pStage);

struct StagePtr
{
    StageReturn* p;
    StagePtr() : p(0) {}
    ~StagePtr()
    {
        if (p)
            p->DecRefCount();
    }
};

struct MapCls
{
    void FUN_00e7f430(int a, int b, int c);
};

MapCls* __cdecl FUN_00e7f5d0();

struct PassCls
{
    virtual void Placeholder() {}
    int f04;
    int f08;
    int f0c;
    int f10;
    int f14;
    unsigned int f18;
    int f1c;
    int f20;
    int f24;
    int f28;
    int f2c;
    MapCls* m_pkMap;
    int f34;
    int f38;
    int f3c;
    int f40;
    NiPointer<NiD3DPixelShader> m_spPixel;
    int f48;
    int f4c;
    int f50;
    int f54;
    int f58;
    NiPointer<NiD3DPixelShader> m_spVertex;
    int f60;
    unsigned int m_uiRefCount;

    void IncRefCount() { ++m_uiRefCount; }
    void DecRefCount()
    {
        --m_uiRefCount;
        if (!m_uiRefCount)
            FUN_00e80190();
    }
    void FUN_00e80190();
    void FUN_00e802b0(int a, StageReturn* pStage);
    MapCls* GetMap()
    {
        if (!m_pkMap)
            m_pkMap = FUN_00e7f5d0();
        return m_pkMap;
    }
};

void __cdecl FUN_00be0cf0(StageReturn* pStage, int a, int b, int c, int d);

struct PtrPass
{
    PassCls* m_pObject;
    PtrPass() : m_pObject(0) {}
    PtrPass(const PtrPass& other) : m_pObject(other.m_pObject)
    {
        if (m_pObject)
            m_pObject->IncRefCount();
    }
    ~PtrPass()
    {
        if (m_pObject)
            m_pObject->DecRefCount();
    }
    PassCls* operator->() const { return m_pObject; }
    PtrPass& operator=(const PtrPass& other)
    {
        if (m_pObject != other.m_pObject) {
            if (m_pObject)
                m_pObject->DecRefCount();
            m_pObject = other.m_pObject;
            if (m_pObject)
                m_pObject->IncRefCount();
        }
        return *this;
    }
};

extern const float DAT_01200458;

struct DecalCls : public BSShader
{
    PtrPass m_spPasses[2];
    NiPointer<NiD3DPixelShader> m_spVertexShaders[2];
    NiPointer<NiD3DPixelShader> m_spPixelShaders[2];
    PassReference m_pkPass0;
    PassReference m_pkPass1;
    PassReference m_pkPass2;

    void FUN_00bcb7f0();
};

void DecalCls::FUN_00bcb7f0()
{
    PtrPass spPass;
    StagePtr stagePtr;
    StageReturn*& pStage = stagePtr.p;
    spPass = m_spPasses[0];
    unsigned int gateVal = spPass->f18;
    if (gateVal < 2) {
        FUN_00e7edf0(pStage);
        FUN_00be0cf0(pStage, 0, 1, 2, 1);
        spPass->FUN_00e802b0(spPass->f14, pStage);
        FUN_00e7edf0(pStage);
        FUN_00be0cf0(pStage, 1, 3, 2, 1);
        spPass->FUN_00e802b0(spPass->f14, pStage);
    }
    spPass->m_spVertex = m_spVertexShaders[0].m_pObject;
    spPass->m_spPixel = m_spPixelShaders[0].m_pObject;
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0xa8, 15, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x1b, 1, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x13, 9, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x14, 6, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0xf, 1, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x19, 5, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x18, 0, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0xe, 0, 1);
    {
        float fVal = DAT_01200458;
        int bits = *(int*)&fVal;
        if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0xc3, bits, 1);
    }

    spPass = m_spPasses[1];
    if (spPass->f18 < 2) {
        FUN_00e7edf0(pStage);
        FUN_00be0cf0(pStage, 0, 1, 2, 1);
        spPass->FUN_00e802b0(spPass->f14, pStage);
        FUN_00e7edf0(pStage);
        FUN_00be0cf0(pStage, 1, 3, 2, 1);
        spPass->FUN_00e802b0(spPass->f14, pStage);
    }
    spPass->m_spVertex = m_spVertexShaders[1].m_pObject;
    spPass->m_spPixel = m_spPixelShaders[1].m_pObject;
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0xa8, 15, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x1b, 1, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x13, 9, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x14, 6, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0xf, 1, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x19, 5, 1);
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0x18, 0, 1);
    {
        float fVal = DAT_01200458;
        int bits = *(int*)&fVal;
        if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0xc3, bits, 1);
    }
    if (!spPass->m_pkMap) spPass->m_pkMap = FUN_00e7f5d0();
    spPass->m_pkMap->FUN_00e7f430(0xe, 0, 1);
}
