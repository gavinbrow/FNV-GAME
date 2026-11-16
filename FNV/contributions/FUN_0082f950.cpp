struct FUN_0082f950_shell
{
    void FUN_0082f6c0();
    void* FUN_0082f950(unsigned int flags);
};

extern void __stdcall FUN_00ec5fce(void*, unsigned int, unsigned int,
    void (FUN_0082f950_shell::*)());
extern void __cdecl FUN_00401030(void*);

void* FUN_0082f950_shell::FUN_0082f950(unsigned int flags)
{
    if ((flags & 2) != 0)
    {
        FUN_00ec5fce(this, 0x4c, ((unsigned int*)this)[-1],
            &FUN_0082f950_shell::FUN_0082f6c0);
        if ((flags & 1) != 0)
            FUN_00401030((char*)this - 4);
        return (char*)this - 4;
    }

    FUN_0082f6c0();
    if ((flags & 1) != 0)
        FUN_00401030(this);
    return this;
}