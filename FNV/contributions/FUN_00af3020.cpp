struct FUN_00af33f0
{
    void* vtbl;
    int x;
    FUN_00af33f0();
    ~FUN_00af33f0();
};

void* __cdecl FUN_00af3020()
{
    static FUN_00af33f0 instance;
    return &instance;
}