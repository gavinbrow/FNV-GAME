#include <windows.h>
static inline BA97B0Heap& BA97B0GetHeap() { return reinterpret_cast<BA97B0Heap&>(g_memoryManager); }
class RefObj_b4622 { public: virtual void v0(); virtual void v1(); volatile long m_uiRefCount; };
class FUN_00bb3d80_cls {
public:
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void v7();
    virtual void v8();
    virtual void v9();
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
    virtual void v48();
    virtual void v49();
    virtual void v50();
    virtual void v51();
    virtual void v52();
    virtual void v53();
    virtual void v54();
    virtual void v55(void* p);
    void __thiscall FUN_00b702b0(void* a, unsigned int b);
    int unk04;
    int unk08;
    int unk0C;
    int unk10;
    int unk14;
    int unk18;
    int unk1C;
    int unk20;
    int unk24;
    int unk28;
    int unk2C;
    int unk30;
    int unk34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    int unk50;
    int unk54;
    int unk58;
    int unk5C;
    int unk60;
    int unk64;
    int unk68;
    int unk6C;
    int unk70;
    int unk74;
    int unk78;
    void* m_07c;
    int unk80;
    int unk84;
    RefObj_b4622* m_088;
    unsigned short m_08c;
    void __thiscall FUN_00bb3d80(FUN_00bb3d80_cls* arg1, unsigned int arg2);
};

void FUN_00bb3d80_cls::FUN_00bb3d80(FUN_00bb3d80_cls* arg1, unsigned int arg2)
{
    this->FUN_00b702b0(arg1, arg2);
    arg1->v55(m_07c);
    RefObj_b4622* old = arg1->m_088;
    if (old != m_088) {
        if (old != 0 && InterlockedDecrement(&old->m_uiRefCount) == 0) {
            old->v1();
        }
        RefObj_b4622* n = m_088;
        arg1->m_088 = n;
        if (n != 0) {
            InterlockedIncrement(&n->m_uiRefCount);
        }
    }
    arg1->m_08c = m_08c;
}

