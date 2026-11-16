struct FUN_00d2be30
{
    void SetFile(const char* fileName, const char* mode);
};
extern const unsigned char DAT_0106e798[];
struct Candidate : FUN_00d2be30
{
    volatile int* vtable;
    unsigned short unk04;
    volatile unsigned short flags;
    volatile void* file;
    volatile unsigned char opened;
    void* FUN_00d2bf70(const char* fileName);
};
void* Candidate::FUN_00d2bf70(const char* fileName)
{
    flags = 1;
    vtable = &DAT_010ce6f4;
    file = 0;
    opened = 1;
    if (fileName != 0)
        SetFile(fileName, (const char*)DAT_0106e798);
    return this;
}
