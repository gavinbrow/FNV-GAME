union __declspec(intrin_type) __declspec(align(16)) __m128 { float m128_f32[4]; unsigned __int64 m128_u64[2]; };
extern const __m128 DAT_01267e30;
extern float DAT_01016248;
extern float DAT_0101e2bc;
extern __declspec(thread) int DAT_012722b4;

struct S00cb87e0_Node {
    int unk00;
    int unk04;
    int unk08;
    int unk0C;
    __m128 v10;
    __m128 v20;
    volatile float f30;
    float f34;
    int unk38;
    int unk3C;
    int unk40;
    int unk44;
    int unk48;
    int unk4C;
    __forceinline S00cb87e0_Node() {
        f30 = DAT_01016248;
        unk00 = 0;
        unk04 = 0;
        v10 = DAT_01267e30;
        v20 = DAT_01267e30;
        f34 = DAT_0101e2bc;
    }
    void* operator new(unsigned int size) throw() {
        unsigned char* raw = (unsigned char*)((MemoryManager_t*)&DAT_011f6238)->FUN_00aa3e40(size);
        unsigned char lo = (unsigned char)raw;
        lo &= 0x0f;
        unsigned char pad = 0x10;
        pad -= lo;
        raw += pad;
        raw[-1] = pad;
        return raw;
    }
    void operator delete(void*) throw() {}
};

struct S00cb87e0_Guard {
    int m_saved;
    S00cb87e0_Guard() { m_saved = DAT_012722b4; DAT_012722b4 = 0x10; }
    ~S00cb87e0_Guard() { DAT_012722b4 = m_saved; }
};

struct S00cb87e0_Obj {
    int unk00;
    int unk04;
    int m_08;
    S00cb87e0_Node* m_0c;
    void FUN_00cb84a0(S00cb87e0_Node* p);
    void* FUN_00cb87e0(bool* out);
};

void* S00cb87e0_Obj::FUN_00cb87e0(bool* out)
{
    S00cb87e0_Guard guard;
    bool empty = (m_0c == 0);
    *out = empty;
    if (empty)
    {
        unsigned char* raw = (unsigned char*)((MemoryManager_t*)&DAT_011f6238)->FUN_00aa3e40(sizeof(S00cb87e0_Node));
        double defaultScale = DAT_01016248;
        unsigned char low = (unsigned char)raw;
        low &= 0x0f;
        unsigned char padding = 0x10;
        padding -= low;
        raw += padding;
        raw[-1] = padding;
        S00cb87e0_Node* p = (S00cb87e0_Node*)raw;
        p->unk00 = 0;
        p->unk04 = 0;
        p->v10 = DAT_01267e30;
        p->v20 = DAT_01267e30;
        p->f30 = defaultScale;
        p->f34 = DAT_0101e2bc;
        m_0c = p;
        if (m_08)
            FUN_00cb84a0(p);
    }
    return m_0c;
}
