struct FUN_00c819f0_stream {
    void* vtable;
    unsigned int m_04;
    unsigned int unk08;
    unsigned int (__cdecl* m_0c)(FUN_00c819f0_stream* self, void* buffer, unsigned int size, unsigned int* sizes, unsigned int count);
};

class FUN_00c819f0_cls {
public:
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0C;
    unsigned int unk10;
    unsigned int unk14;
    unsigned int m_18;
    unsigned int m_1c;
    void Callee65820(int a1);
    void FUN_00c819f0(int a1);
};

void FUN_00c819f0_cls::FUN_00c819f0(int a1) {
    char* obj = (char*)a1;
    FUN_00c819f0_stream* __restrict o;
    unsigned int (__cdecl* fn)(FUN_00c819f0_stream*, void*, unsigned int, unsigned int*, unsigned int);
    unsigned int* cnt = (unsigned int*)&a1;
    Callee65820(a1);
    o = *(FUN_00c819f0_stream**)(obj + 0x250);
    
    o->m_04 += o->m_0c((a1 = 4, o), &m_18, 4, cnt, 1);
    o = *(FUN_00c819f0_stream**)(obj + 0x250);
    
    o->m_04 += o->m_0c((a1 = 4, o), &m_1c, 4, cnt, 1);
}