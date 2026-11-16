struct FUN_00433d10_shell {
    void FUN_00433d40();
    void operator delete(void*);
    FUN_00433d10_shell* FUN_00433d10(unsigned int flags);
};

FUN_00433d10_shell* FUN_00433d10_shell::FUN_00433d10(unsigned int flags)
{
    FUN_00433d40();
    if (flags & 1)
        operator delete(this);
    return this;
}