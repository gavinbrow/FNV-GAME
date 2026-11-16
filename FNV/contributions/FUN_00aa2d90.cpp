struct NiAlloc {
    void __thiscall FUN_00aa4060(void* ptr);
};
extern NiAlloc DAT_011f6238;
void __cdecl FUN_00aa10f0(void* ptr);

struct FUN_00aa2d90 : NiBinaryStream {
    void* unk04;
    void* unk08;
    void* unk0c;
    void* buffer;
    unsigned int unk14;
    unsigned int unk18;
    unsigned int unk1c;
    unsigned char flag20;
    unsigned char flag21;

    void __thiscall FUN_00aa1d30();
    virtual ~FUN_00aa2d90();
    static void operator delete(void* ptr) { DAT_011f6238.FUN_00aa4060(ptr); }
};

FUN_00aa2d90::~FUN_00aa2d90()
{
    if (!flag20 && !flag21) {
        FUN_00aa10f0(buffer);
    }
    FUN_00aa1d30();
}
