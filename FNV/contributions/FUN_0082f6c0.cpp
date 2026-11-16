// FUN_0082f6c0 @ 0x0082f6c0 (size 150)
// Base-object destructor of a thread-like class: clears the "running" flag bit,
// signals the object at +0x34, waits for the worker thread to leave, closes its
// handle, then runs the base class destructor.

extern "C" __declspec(dllimport) int __stdcall CloseHandle(void* hObject);

void __cdecl FUN_0040fca0(int milliseconds);

struct FUN_00aa63c0 {
    virtual ~FUN_00aa63c0();
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
};

struct FUN_0082f6c0 : FUN_00aa63c0 {
    void* unk30;
    int unk34;
    int unk38;
    unsigned int unk3C;

    void FUN_0082f760(void* arg);
    virtual ~FUN_0082f6c0();
};

FUN_0082f6c0::~FUN_0082f6c0()
{
    unk3C &= 0xFFFFFFFE;
    FUN_0082f760(&unk34);
    while (unk3C & 2)
        FUN_0040fca0(10);
    CloseHandle(unk30);
}
