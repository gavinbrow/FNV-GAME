class FUN_0041cba0_class {
public:
    void* FUN_00410220(int);
    char FUN_0041cba0();
};

char FUN_0041cba0_class::FUN_0041cba0()
{
    void* p = FUN_00410220(0x19);
    if (p)
        return *(char*)((char*)p + 0x18);
    else
        return 0;
}