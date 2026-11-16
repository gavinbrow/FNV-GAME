void* __cdecl FUN_00aa13e0(unsigned int bytes);
inline void* __cdecl operator new(unsigned int, void* p) { return p; }
struct BillboardClone : FUN_00a5ecb0 {
    unsigned int unkA0;
    unsigned int unkA4;
    unsigned int unkA8;
    unsigned short m_mode;
    float m_value;
    BillboardClone() : FUN_00a5ecb0(0), m_mode(9), m_value(0.0f) {}
    virtual void Dummy() {}
};
struct BillboardCloneSource : StandIn {
    void FUN_00a5dc80(BillboardClone* dest, void* context);
    BillboardClone* FUN_00a7e710(void* context);
};
BillboardClone* BillboardCloneSource::FUN_00a7e710(void* context) {
    void* storage = FUN_00aa13e0(sizeof(BillboardClone));
    BillboardClone* clone = storage ? new (storage) BillboardClone() : 0;
    FUN_00a5dc80(clone, context);
    clone->m_mode = m_field;
    return clone;
}