struct Owner;

struct Inner
{
    unsigned char unk00[8];
    int threshold;
    int FUN_00cb1c60(unsigned __int64 value);
};

struct Owner
{
    unsigned char unk00[0x30];
    Inner inner;
    volatile unsigned char* FUN_00def3d0(volatile unsigned char* result, int first, int second);
};

volatile unsigned char* Owner::FUN_00def3d0(volatile unsigned char* result, int first, int second)
{
    if (first == 0 || second == 0)
    {
        *result = 1;
        return result;
    }

    unsigned __int64 firstValue = (unsigned __int64)(__int64)first;
    unsigned __int64 secondValue = (unsigned __int64)(__int64)second;
    unsigned __int64 value;
    if (firstValue < secondValue)
        value = firstValue * 0x100000000LL + secondValue;
    else
        value = secondValue * 0x100000000LL + firstValue;

    Inner* state = &inner;
    int actual = state->FUN_00cb1c60(value);
    if (actual > state->threshold)
    {
        *result = 1;
        return result;
    }
    *result = 0;
    return result;
}
