struct TlsBlock_ca57 { unsigned int m_2b4; };
extern __declspec(thread) TlsBlock_ca57 g_tls;
struct TlsFlagGuard_ca57 {
    unsigned int m_saved;
    TlsFlagGuard_ca57() { m_saved=g_tls.m_2b4; g_tls.m_2b4=16; }
    ~TlsFlagGuard_ca57() { g_tls.m_2b4=m_saved; }
};
class Pool_ca57 {public: void* __thiscall FUN_00aa3e40(unsigned int);};
class Node_ca57 {
public:
    unsigned int unk00,unk04,unk08,unk0C,unk10,unk14,unk18,unk1C,unk20,unk24,unk28,unk2C;
    Node_ca57();
    static void operator delete(void*) throw() {}
    void* operator new(unsigned int size) throw() {
        unsigned char* raw=(unsigned char*)((Pool_ca57*)&DAT_011f6238)->FUN_00aa3e40(size);
unsigned char lo=(unsigned char)raw;
lo &= 0x0f;
unsigned char pad=0x10;
pad -= lo;
raw+=pad;
raw[-1]=pad;
return raw;
    }
};
class Owner_ca57 {
public:
    unsigned int unk00,unk04,m_08;
    unsigned int* m_0c;
    void FUN_00ca5360(unsigned int*);
    unsigned int* FUN_00ca57a0(bool*);
};
unsigned int* Owner_ca57::FUN_00ca57a0(bool* out) {
    TlsFlagGuard_ca57 guard;
    *out=(m_0c==0);
    if(*out){
        out=(bool*)new Node_ca57();
        m_0c=(unsigned int*)out;
        if(m_08!=0) FUN_00ca5360(m_0c);
    }
    return m_0c;
}