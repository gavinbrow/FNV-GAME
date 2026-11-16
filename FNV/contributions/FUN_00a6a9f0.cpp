class NiTexture {
public:
    virtual ~NiTexture();
    virtual void DeleteThis();
    unsigned int m_uiRefCount;
    void IncRefCount() { InterlockedIncrement((volatile long*)&m_uiRefCount); }
    void DecRefCount() { if (!InterlockedDecrement((volatile long*)&m_uiRefCount)) DeleteThis(); }
};

struct DeallocHelper00aa4060 {
    void FUN_00aa4060(void* p);
};

NiTexturingProperty::Map::~Map() {
    reinterpret_cast<DeallocHelper00aa4060*>(&g_memoryManager)->FUN_00aa4060(m_pkTextureTransform);
    if (m_spTexture.m_pObject)
        m_spTexture.m_pObject->DecRefCount();
}

struct MapScalarDtorCandidate : NiTexturingProperty::Map {
    void* FUN_00a6a9f0(unsigned int flags);
};

void* MapScalarDtorCandidate::FUN_00a6a9f0(unsigned int flags) {
    this->NiTexturingProperty::Map::~Map();
    if (flags & 1)
        reinterpret_cast<DeallocHelper00aa4060*>(&g_memoryManager)->FUN_00aa4060(this);
    return this;
}