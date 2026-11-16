struct BGSDistantTreeBlockLoadTask
{
    void* FUN_006f9470(unsigned int flags);
    void FUN_006f94a0();
};

struct Callee
{
    void FUN_0045cec0();
};

struct FUN_006f9080_owner : BGSDistantTreeBlockLoadTask
{
    char unk1b[0x1c];
    Callee callee;

    void FUN_006f9080();
};

void Callee::FUN_0045cec0()
{
}

void FUN_006f9080_owner::FUN_006f9080()
{
    callee.FUN_0045cec0();
}