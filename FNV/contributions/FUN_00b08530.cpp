extern double _DAT_0101a6b0;
struct FUN_00b08530_class {
    short FUN_00b08530(float level);
};

short FUN_00b08530_class::FUN_00b08530(float level)
{
    short index = 0;
    if (level == _DAT_0101a6b0)
        level = ((FUN_00b08440_shell*)this)->FUN_00b08440();

    int count = ((FUN_00b086f0_class*)this)->FUN_00b086f0();
    index = (short)((1.0 - level) * count);
    if (index == count)
        --index;
    return index;
}