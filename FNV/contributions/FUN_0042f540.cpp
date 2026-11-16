class FUN_0042f4e0
{
public:
    void FUN_0042fe80();
    void* FUN_0042f540(unsigned int flags);
};

// @fnv 0x0042f540
void* FUN_0042f4e0::FUN_0042f540(unsigned int flags)
{
    FUN_0042fe80();
    if ((flags & 1) != 0)
    {
        ::operator delete(this);
    }
    return this;
}