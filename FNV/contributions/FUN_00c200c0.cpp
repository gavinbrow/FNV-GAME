struct FUN_00c200c0_Arr {
    int unk00;
    int unk04;
    unsigned short m_usMax;
    unsigned short m_usSize;
    unsigned short unk0c;
    unsigned short m_usGrow;
    void __thiscall FUN_0096ad30(unsigned int n);
    void __thiscall FUN_0096ae90(unsigned int n, unsigned int* p);
};

extern "C" void __stdcall FUN_00c31db0(FUN_00c200c0_Arr* p);
extern "C" unsigned int __cdecl FUN_00a7d330(unsigned int v);
extern "C" unsigned int __cdecl FUN_00a7d550(const void* p, float f);
extern "C" unsigned int DAT_01202510;
extern "C" int UNK_01015a9c;

struct Emitter00c200c0 {
    char pad[0x58];
    float m_f58;
    void __thiscall FUN_00c200c0(FUN_00c200c0_Arr* p);
};

void __thiscall Emitter00c200c0::FUN_00c200c0(FUN_00c200c0_Arr* p)
{
    FUN_00c31db0(p);
    unsigned int local = FUN_00a7d330(DAT_01202510);
    unsigned int n = p->m_usSize;
    if (n >= p->m_usMax)
    {
        p->FUN_0096ad30(p->m_usGrow + n);
    }
    p->FUN_0096ae90(n, &local);
    local = FUN_00a7d550(&UNK_01015a9c, m_f58);
    n = p->m_usSize;
    if (n >= p->m_usMax)
    {
        p->FUN_0096ad30(p->m_usGrow + n);
    }
    p->FUN_0096ae90(n, &local);
}
