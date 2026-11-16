template <typename T>
struct hkArrayD64A {
    T* m_data;
    int m_size;
    int m_capacityAndFlags;
    hkArrayD64A() : m_data(0), m_size(0), m_capacityAndFlags(0x80000000) {}
};
class hkListenerD64A {
public:
    virtual ~hkListenerD64A() throw();
};
class hkEntityD64A {
public:
    void FUN_00c93920(hkListenerD64A* pkListener) throw();
};
class hkWorldD64A {
public:
    int unk00, unk04, unk08, unk0C, unk10, unk14, unk18, unk1C, unk20, unk24, unk28, unk2C;
    int unk30, unk34, unk38, unk3C, unk40, unk44, unk48, unk4C, unk50, unk54, unk58, unk5C;
    int unk60, unk64, unk68;
    hkEntityD64A** m_entities;
    int m_numEntities;
};
class hkBaseAD64A {
public:
    virtual ~hkBaseAD64A() throw();
    int unk04;
};
class hkBaseBD64A {
public:
    virtual ~hkBaseBD64A() throw();
    int unk0C, unk10, unk14, unk18, unk1C;
};
class hkBaseCD64A {
public:
    virtual ~hkBaseCD64A() throw();
};
class FUN_00ddccb0 : public hkBaseAD64A, public hkBaseBD64A, public hkBaseCD64A {
public:
    FUN_00ddccb0(void* pkInfo) throw();
    virtual ~FUN_00ddccb0() throw();
    hkWorldD64A* m_world;
};
struct FlagD64A { bool value; FlagD64A() : value(true) {} };
class FUN_00d64a50 : public FUN_00ddccb0, public hkListenerD64A {
public:
    FlagD64A m_flagA;
    FlagD64A m_flagB;
    hkArrayD64A<void*> m_arrayA;
    hkArrayD64A<void*> m_arrayB;
    FUN_00d64a50(void* pkInfo) throw();
    virtual ~FUN_00d64a50() throw();
};
FUN_00d64a50::FUN_00d64a50(void* pkInfo) throw() : FUN_00ddccb0(pkInfo)
{
    if (m_world) {
        for (int i = 0; i < m_world->m_numEntities; i++)
            m_world->m_entities[i]->FUN_00c93920(this);
    }
}