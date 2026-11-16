struct NiColor3 {
    float m_r;
    float m_g;
    float m_b;
    __forceinline NiColor3() : m_r(0.0f), m_g(0.0f), m_b(0.0f) {}
};

class NiMemObject {
public:
    static void* operator new(unsigned int size) throw();
    static void* operator new(unsigned int, void* p) { return p; }
};

inline void* __cdecl operator new(unsigned int, void* p) { return p; }

extern volatile long DAT_011f4400;

class NiRefObject : public NiMemObject {
public:
    NiRefObject() throw() {
        m_uiRefCount = 0;
        InterlockedIncrement(&DAT_011f4400);
    }
    virtual void V0();
    virtual void DeleteThis();
    unsigned int m_uiRefCount;
};

class NiProperty : public NiRefObject {
public:
    NiProperty() throw();
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
};

class NiAlphaProperty : public NiProperty {
public:
    NiAlphaProperty() throw() {
        m_usAlphaArg = 0xec;
        m_ucAlphaArg2 = 0;
    }
    unsigned short m_usAlphaArg;
    unsigned char m_ucAlphaArg2;
    unsigned char m_ucPad1b;
};

struct SubObjF8 {
    int m_00;
    int m_04;
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
    int m_24;
    void __thiscall FUN_00e68810() throw();
    SubObjF8() {
        FUN_00e68810();
    }
};

struct PairEntry {
    int key;
    int val;
};

extern "C" void* __cdecl fnv_zlib_memset(void*, int, unsigned int);

extern int DAT_0126f918;
extern int DAT_0126f91c;
extern int DAT_0126f920;
extern int DAT_0126f924;
extern int DAT_0126f928;
extern unsigned short DAT_0126f92c[];
extern unsigned short DAT_0126f948[8];
extern unsigned short DAT_0126f958[];

class FUN_00e881a0 : public NiRefObject {
public:
    FUN_00e881a0(void* renderer);
    int m_08;
    int m_0c;
    int m_10;
    int m_14;
    int m_18;
    int m_1c;
    int m_20;
    int m_24;
    int m_28;
    int m_2c;
    int m_30;
    int m_34;
    int m_38;
    int m_3c;
    int m_40;
    int m_44;
    int m_48;
    int m_4c;
    int m_50;
    int m_54;
    int m_58;
    int m_5c;
    int m_60;
    int m_64;
    int m_68;
    int m_6c;
    int m_70;
    NiAlphaProperty* m_74;
    float m_78;
    float m_7c;
    float m_80;
    float m_84;
    float m_88;
    NiColor3 m_8c;
    int m_98;
    int m_9c;
    int m_a0;
    int m_a4;
    int m_a8;
    int m_ac;
    int m_b0;
    int m_b4;
    int m_b8;
    int m_bc;
    int m_c0;
    int m_c4;
    int m_c8;
    int m_cc;
    int m_d0;
    int m_d4;
    int m_d8;
    int m_dc;
    int m_e0;
    int m_e4;
    int m_e8;
    int m_ec;
    int m_f0;
    int m_f4;
    SubObjF8 m_f8;
    PairEntry m_120[256];
    int m_920[64];
    PairEntry m_a20[128];
    PairEntry m_e20[80];
    int m_10a0[20];
    int m_10f0;
    unsigned char m_10f4;
    unsigned char m_10f5;
    unsigned char m_10f6;
    unsigned char m_10f7;
    void* m_10f8;
    int m_10fc;
};

FUN_00e881a0::FUN_00e881a0(void* renderer)
    : NiRefObject(), m_74(0), m_8c(), m_f8()
{
    PairEntry* p1 = m_120;
    int i1 = 255;
    do {
        p1->key = 0x7fffffff;
        ++p1;
        --i1;
    } while (i1 >= 0);
    PairEntry* p2 = m_a20;
    int i2 = 127;
    do {
        p2->key = 0x7fffffff;
        ++p2;
        --i2;
    } while (i2 >= 0);
    PairEntry* p3 = m_e20;
    int i3 = 79;
    do {
        p3->key = 0x7fffffff;
        ++p3;
        --i3;
    } while (i3 >= 0);

    void* r = renderer;
    int& firstSlot = m_10f0; firstSlot = 0;
    m_10f8 = 0;
    m_10fc = 0;
    ((FUN_00e87af0_This*)this)->FUN_00e87af0(r);

    m_0c = 0;
    m_10 = 1;
    m_14 = 1;
    m_18 = 2;
    m_1c = 3;
    m_6c = 0;
    m_70 = 0;
    NiAlphaProperty* pNew = new NiAlphaProperty();

    NiAlphaProperty* pOld = m_74;
    if (pOld != pNew) {
        if (pOld) {
            if (InterlockedDecrement((volatile long*)((char*)pOld + 4)) == 0)
                pOld->DeleteThis();
        }
        m_74 = pNew;
        if (pNew)
            InterlockedIncrement((volatile long*)((char*)pNew + 4));
    }

    int four = 4;
    int five = 5;
    int six = 6;

    m_20 = 2;
    m_24 = 1;
    m_28 = 3;
    m_2c = four;
    m_30 = 9;
    m_34 = 10;
    m_38 = five;
    m_3c = six;
    m_40 = 7;
    m_44 = 8;
    m_48 = 11;
    m_4c = 8;

    m_50 = 2;
    m_54 = 3;
    m_58 = four;
    m_5c = five;
    m_60 = six;
    m_64 = 7;
    m_68 = 1;

    m_78 = 0.0f;
    m_7c = 0.0f;
    m_80 = 0.0f;
    m_84 = 0.0f;
    m_88 = 1.0f;

    m_b8 = 8;
    m_a0 = 2;
    m_a4 = 3;
    m_a8 = four;
    m_ac = five;
    m_b0 = six;
    m_b4 = 7;
    m_9c = 1;

    m_bc = 1;
    m_c0 = 2;
    m_c4 = 3;
    m_c8 = four;
    m_cc = five;
    m_d0 = six;
    m_d4 = 2;
    m_dc = 2;
    m_e4 = 3;
    m_ec = 1;
    m_d8 = 3;
    m_e0 = 3;
    m_e8 = 2;
    m_f0 = 1;
    m_f4 = 0;

    m_8c = *(NiColor3*)&DAT_011f4998;
    int b0 = (unsigned char)(m_8c.m_r * 255.0);
    int b1 = (unsigned char)(m_8c.m_g * 255.0);
    int b2 = (unsigned char)(m_8c.m_b * 255.0);
    int packed = (b0 | 0xffffff00);
    packed = (packed << 8) | (unsigned char)b1;
    packed = (packed << 8) | (unsigned char)b2;
    m_98 = packed;
    m_08 = 0;

    m_f8.m_08 = 8;
    m_f8.m_0c = 2;
    m_f8.m_10 = 3;
    m_f8.m_14 = 4;
    m_f8.m_18 = 5;
    m_f8.m_1c = 6;
    m_f8.m_20 = 7;
    m_f8.m_24 = 1;

    m_10f4 = 0;
    m_10f5 = 0;
    fnv_zlib_memset(DAT_0126f958, 0xffff, 0x42);

    DAT_0126f958[1] = 0;
    DAT_0126f958[2] = 1;
    DAT_0126f958[3] = 2;
    DAT_0126f958[4] = 3;
    DAT_0126f958[5] = 4;
    DAT_0126f958[6] = 5;
    DAT_0126f958[7] = 6;
    DAT_0126f958[24] = 7;
    DAT_0126f948[0] = 1;
    DAT_0126f948[1] = 2;
    DAT_0126f948[2] = 3;
    DAT_0126f948[3] = 4;
    DAT_0126f948[4] = 5;
    DAT_0126f948[5] = 6;
    DAT_0126f948[6] = 7;

    ((int*)DAT_0126f92c)[0] = -1;
    ((int*)DAT_0126f92c)[3] = -1;
    ((int*)DAT_0126f92c)[1] = -1;
    ((int*)DAT_0126f92c)[2] = -1;
    DAT_0126f948[7] = 0x18;
    ((int*)DAT_0126f92c)[4] = -1;
    ((int*)DAT_0126f92c)[5] = -1;
    ((int*)DAT_0126f92c)[6] = -1;
    DAT_0126f92c[1] = 0;
    DAT_0126f92c[2] = 1;
    DAT_0126f92c[5] = 2;
    DAT_0126f92c[6] = 3;
    DAT_0126f92c[7] = 4;

    DAT_0126f918 = 1;
    DAT_0126f91c = 2;
    DAT_0126f920 = 5;
    DAT_0126f924 = 6;
    DAT_0126f928 = 7;
}