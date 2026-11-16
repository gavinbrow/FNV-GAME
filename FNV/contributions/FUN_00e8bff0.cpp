struct Holder_e8bff0 {
    virtual void __stdcall slot00() = 0;
    virtual void __stdcall slot04() = 0;
    virtual void __stdcall slot08() = 0;
    virtual void __stdcall slot0c() = 0;
    virtual void __stdcall slot10() = 0;
    virtual void __stdcall slot14() = 0;
    virtual void __stdcall slot18() = 0;
    virtual void __stdcall slot1c() = 0;
    virtual void __stdcall slot20() = 0;
    virtual void __stdcall slot24() = 0;
    virtual void __stdcall slot28() = 0;
    virtual int __stdcall read(unsigned int type, unsigned int length, unsigned int* out, unsigned int flags) = 0;
};
extern "C" __declspec(dllimport) void __stdcall EnterCriticalSection(void*);
void __cdecl FUN_00aa10f0(void* p);
void* __cdecl FUN_00aa1070(unsigned int n);
void __cdecl FUN_00ec44d0(void* p, unsigned int out, unsigned int n);
struct Owner_e8bff0 {
    void*& Data() { return *reinterpret_cast<void**>(reinterpret_cast<char*>(this) + 0x40); }
    unsigned int& Capacity() { return *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x44); }
    unsigned int& Offset() { return *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x48); }
    unsigned int& Size() { return *reinterpret_cast<unsigned int*>(reinterpret_cast<char*>(this) + 0x4c); }
    void* CriticalSection() { return reinterpret_cast<char*>(this) + 0x80; }
    void* FUN_00e8bff0(Holder_e8bff0* source, unsigned int type, unsigned int length, unsigned int flags);
};
void* Owner_e8bff0::FUN_00e8bff0(Holder_e8bff0* source, unsigned int type, unsigned int length, unsigned int flags) {
    unsigned int out = 0;
    if (source->read(type, length, &out, flags) < 0)
        return 0;
    EnterCriticalSection(CriticalSection());
    Offset() = out;
    Size() = length;
    if (Capacity() < length) {
        FUN_00aa10f0(Data());
        Data() = FUN_00aa1070(length);
        Capacity() = length;
    }
    if ((flags & 0x3000) == 0)
        FUN_00ec44d0(Data(), out, length);
    return Data();
}