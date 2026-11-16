void __cdecl __debugbreak();
int __stdcall FUN_00e230f0(int);
extern char DAT_0103d078[];
extern char DAT_010eaf08[];
extern char DAT_010eaeb4[];
struct MessageBuffer
{
    char* begin;
    char* end;
    unsigned int capacity;
    void FUN_00cb1600(char*, unsigned int);
    MessageBuffer* FUN_00cc01c0(const char*);
    MessageBuffer* FUN_00cc0280(int);
    void FUN_00cc00e0();
};
struct ErrorReporter
{
    virtual void unused0();
    virtual void unused1();
    virtual void unused2();
    virtual int Report(int, unsigned int, const char*, const char*, int);
};
extern ErrorReporter* DAT_01268360;

bool __stdcall FUN_00e14b30(bool report)
{
    int error = FUN_00e230f0(1);
    if (report && error)
    {
        MessageBuffer message;
        unsigned int storage[128];
        char* text = reinterpret_cast<char*>(storage);
        message.FUN_00cb1600(text, 512);
        message.FUN_00cc01c0(DAT_010eaf08)->FUN_00cc0280(error)->FUN_00cc01c0(DAT_0103d078);
        if (DAT_01268360->Report(3, 0x4c5c2afa, text, DAT_010eaeb4, 0xb29))
            __debugbreak();
        message.FUN_00cc00e0();
    }
    return error == 0;
}

