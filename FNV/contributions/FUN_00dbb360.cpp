struct FUN_00c90510_Obj : hkReferencedObject { void FUN_00c90510(); };
struct FUN_00d87790_Result { unsigned char value; };
struct FUN_00d87790_Obj { void __thiscall FUN_00d87790(FUN_00d87790_Result); };
struct FUN_00dbb360_Global { virtual void vf00(); virtual void vf04(); virtual void vf08(); virtual void vf0C(); virtual FUN_00c90510_Obj* vf10(); virtual FUN_00c90510_Obj* vf14(); };
extern FUN_00dbb360_Global* DAT_01268b08;
extern int DAT_010d6518[];
struct FUN_00dbb360_Class {
    int m_00; unsigned short m_04,m_06; hkReferencedObject* m_08; hkReferencedObject* m_0C;
    FUN_00d87790_Obj m_10; int m_14,m_18,m_1C,m_20,m_24;
    FUN_00dbb360_Class* __thiscall FUN_00dbb360();
};
FUN_00dbb360_Class* __thiscall FUN_00dbb360_Class::FUN_00dbb360() {
    FUN_00d87790_Result result;
    m_06=1;
    result.value=0;
    m_00=(int)DAT_010d6518;
    *reinterpret_cast<hkReferencedObject* volatile*>(&m_08)=0;
    *reinterpret_cast<hkReferencedObject* volatile*>(&m_0C)=0;
    m_10.FUN_00d87790(result);
    m_24=0; m_20=0;
    FUN_00c90510_Obj* p=DAT_01268b08->vf14();
    if(p) p->FUN_00c90510();
    if(m_0C) m_0C->removeReference();
    m_0C=p;
    p=DAT_01268b08->vf10();
    if(p) p->FUN_00c90510();
    if(m_08) m_08->removeReference();
    m_08=p;
    return this;
}