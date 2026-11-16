struct Helper
{
    virtual void h0(); virtual void h1(); virtual void h2(); virtual void h3();
    virtual void h4(); virtual void h5(); virtual void h6();
    virtual void dispatch(unsigned int *values, int count, int threshold);
};
struct Owner
{
    virtual void v0();
    virtual void v1();
    virtual void check(unsigned int value, int threshold);
    Helper *helper;
    void FUN_00d2c090(unsigned int *values, int count, int threshold);
};
void Owner::FUN_00d2c090(unsigned int *values, int count, int threshold)
{
    if (threshold <= 0x2000)
    {
        for (int i = 0; i < count; ++i)
            check(values[i], threshold);
    }
    else
        helper->dispatch(values, count, threshold);
}
