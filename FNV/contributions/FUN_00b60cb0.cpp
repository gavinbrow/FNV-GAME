struct RefCounted_b60 {
    int m_iRefCount;
    virtual void Unk00();
    virtual void Destroy();
    void IncRefCount() { InterlockedIncrement((volatile long*)&m_iRefCount); }
    void DecRefCount() { if (InterlockedDecrement((volatile long*)&m_iRefCount) == 0) Destroy(); }
};
struct RefSlot88_b60 {
  RefCounted_b60* ptr;
  RefSlot88_b60() {}
  ~RefSlot88_b60() { if (ptr) ptr->DecRefCount(); }
};
class BaseObj_b60 {
public:
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int unk18;
    BaseObj_b60();
    virtual ~BaseObj_b60();
};
class FUN_00b60cb0 : public BaseObj_b60 {
public:
    unsigned int m_1c;
    unsigned int unk20;
    unsigned int unk24;
    unsigned int unk28;
    unsigned int unk2C;
    unsigned int unk30;
    unsigned int unk34;
    unsigned int unk38;
    unsigned int unk3C;
    unsigned int unk40;
    unsigned int unk44;
    unsigned int unk48;
    unsigned int unk4C;
    unsigned int unk50;
    unsigned int unk54;
    unsigned int unk58;
    unsigned int unk5C;
    unsigned int unk60;
    unsigned int unk64;
    unsigned int unk68;
    unsigned int unk6C;
    unsigned int unk70;
    unsigned int unk74;
    unsigned int unk78;
    unsigned int m_7c;
    NiPointer<RefCounted_b60> m_80;
    NiPointer<RefCounted_b60> m_84;
    RefSlot88_b60 m_88;
    unsigned short m_8c;
    unsigned short m_8e;
    FUN_00b60cb0();
    virtual ~FUN_00b60cb0();
};
FUN_00b60cb0::FUN_00b60cb0() {
    m_88.ptr = 0;
    m_8c = 0;
    m_8e = 0;
    m_80 = (RefCounted_b60*)0;
    m_7c = 0;
    m_1c = 4;
}
