struct FUN_00623510_class
{
    void* FUN_00623510(unsigned int flags);
};
void* FUN_00623510_class::FUN_00623510(unsigned int flags)
{
    ((FUN_006234d0*)this)->FUN_006234f0();
    if (flags & 1)
        Deallocate(this);
    return this;
}
