
extern "C" __declspec(dllimport) long __stdcall InterlockedDecrement(volatile long*);
struct RenderBuffer {
    virtual void Unknown();
    virtual void Destroy();
    volatile long m_uiRefCount;
};
struct RendererData;
struct FUN_00ee8560 {
    virtual ~FUN_00ee8560();
    int unk04;
    int unk08;
    RenderBuffer* m_apkBuffers[4];
    int unk1c;
    RenderBuffer* m_pkDepthBuffer;
    RendererData* m_pkRendererData;
    void __thiscall FUN_00a5d3d0();
};
FUN_00ee8560::~FUN_00ee8560() {
    delete m_pkRendererData;
    RenderBuffer* p = m_pkDepthBuffer;
    if (p && !InterlockedDecrement(&p->m_uiRefCount))
        p->Destroy();
    RenderBuffer** pp = m_apkBuffers + 4;
    for (int i = 3; i >= 0; --i) {
        RenderBuffer* q = *(--pp);
        if (q && !InterlockedDecrement(&q->m_uiRefCount))
            q->Destroy();
    }
    FUN_00a5d3d0();
}
