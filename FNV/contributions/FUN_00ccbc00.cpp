
extern int DAT_010ca744;
extern "C" int DAT_01268678;
extern "C" int (__cdecl *DAT_00fdf1c4)(void*);

class NiRefObject {
public:
    virtual ~NiRefObject();
    virtual void DeleteThis();
    unsigned int m_uiRefCount;
};

struct FUN_00ccbc00_elem {
    unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0C;
    unsigned int unk10; unsigned int m_14; unsigned int unk18; unsigned int unk1C;
    unsigned int unk20; unsigned int unk24; unsigned int unk28; unsigned int unk2C;
    unsigned int unk30; unsigned int unk34; unsigned int unk38; unsigned int unk3C;
    unsigned int unk40; unsigned int unk44; unsigned int unk48; unsigned int unk4C;
    unsigned int unk50; unsigned int unk54; unsigned int unk58; unsigned int unk5C;
};

struct FUN_00ccbc00_inner {
    unsigned int unk00; unsigned int unk04; unsigned int unk08; unsigned int unk0C;
    unsigned int unk10; unsigned int unk14; unsigned int unk18; unsigned int unk1C;
    unsigned int unk20; unsigned int unk24; unsigned int unk28; unsigned int unk2C;
    unsigned int unk30; unsigned int unk34; unsigned int unk38; unsigned int unk3C;
    unsigned int unk40; unsigned int unk44; unsigned int unk48; unsigned int unk4C;
    unsigned int unk50; unsigned int unk54; unsigned int unk58; unsigned int unk5C;
    unsigned int unk60; unsigned int unk64; unsigned int unk68; unsigned int unk6C;
    unsigned int unk70; unsigned int unk74; unsigned int unk78; unsigned int unk7C;
    unsigned int unk80; unsigned int unk84; unsigned int unk88; unsigned int unk8C;
    unsigned int unk90; unsigned int unk94; unsigned int unk98; unsigned int unk9C;
    unsigned int unkA0; unsigned int unkA4; unsigned int unkA8; unsigned int unkAC;
    unsigned int unkB0; FUN_00ccbc00_elem* m_b4; unsigned int m_b8;
};


struct CcbcOwnerBase {
    void FUN_00c876a0();
    void FUN_00cd2de0();
    ~CcbcOwnerBase() { FUN_00cd2de0(); }
};

struct RefSmartPtr {
    NiRefObject* ptr;
    ~RefSmartPtr() {
        NiRefObject* p = ptr;
        if (p) {
            if (InterlockedDecrement((volatile long*)&p->m_uiRefCount) == 0) p->DeleteThis();
        }
    }
};

class FUN_00ccbc00 : public CcbcOwnerBase {
public:
    void* volatile m_pVtable;
    unsigned int unk04;
    FUN_00ccbc00_inner* volatile m_08;
    unsigned int unk0c;
    unsigned int unk10;
    RefSmartPtr m_14;
    ~FUN_00ccbc00();
};

FUN_00ccbc00::~FUN_00ccbc00() {
    m_pVtable = (void*)&DAT_010ca744;
    FUN_00ccbc00_inner* x = m_08;
    if ((int)x->m_b8 > 0) {
        int n = (int)x->m_b8;
        unsigned int off = 0;
        do {
            *(unsigned int*)((char*)x->m_b4 + off + 0x14) = 0;
            off += 0x60;
        } while (--n != 0);
    }
    FUN_00c876a0();
    int one = 1;
    DAT_01268678 -= one;
    NiRefObject* p = m_14.ptr;
    if (p) {
        if (InterlockedDecrement((volatile long*)&p->m_uiRefCount) == 0) p->DeleteThis();
        m_14.ptr = 0;
    }

}
