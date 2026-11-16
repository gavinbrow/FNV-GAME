int __cdecl FUN_00dd7e70(int a)
{
    unsigned int r = (unsigned int)(a - 1);
    unsigned int t = r >> 12 & 0x10;
    unsigned int kIter = 0;
    kIter += t;
    r >>= t;
    t = r >> 5 & 8;
    kIter += t;
    r >>= t;
    t = r >> 2 & 4;
    kIter += t;
    r >>= t;
    t = r >> 1 & 2;
    kIter += t;
    r >>= t;
    t = r >> 1 & 1;
    kIter += t;
    r >>= t;
    return (int)(r + kIter);
}
