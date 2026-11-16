extern "C" __declspec(dllimport) void __stdcall _fnv_EnterCriticalSection(void* section);
extern "C" __declspec(dllimport) void __stdcall _fnv_LeaveCriticalSection(void* section);
struct FUN_00d605d0_Class
{
    void FUN_00d60960(unsigned int value);
    void FUN_00d605d0(unsigned int value);
    void FUN_00dda730(unsigned int value);
    void FUN_00d609a0(__int64 value);
    void FUN_00d60940(unsigned int value);
    const char* FUN_00d607e0(unsigned int* value);
};
struct Record
{
    int unk00;
    FUN_00d605d0_Class* config;
    void* criticalSection;
    bool FUN_00dd9b40(unsigned int a, unsigned int b, unsigned int c, int d, unsigned int e);
};
bool Record::FUN_00dd9b40(unsigned int a, unsigned int b, unsigned int c, int d, unsigned int e)
{
    _fnv_EnterCriticalSection(criticalSection);
    if (config)
    {
        config->FUN_00d60960(0x29);
        config->FUN_00d605d0(8);
        config->FUN_00dda730(a);
        config->FUN_00dda730(b);
        config->FUN_00d60960(c);
        config->FUN_00d609a0(d);
        config->FUN_00d60940(e);
    }
    bool hasValue;
    if (config)
    {
        const char* value = config->FUN_00d607e0(&a);
        if (value[0] == 0)
            goto noValue;
        hasValue = true;
        goto valueChecked;
    noValue:
        hasValue = false;
    valueChecked:
        ;
    }
    else
        hasValue = false;
    _fnv_LeaveCriticalSection(criticalSection);
    return !hasValue;
}
