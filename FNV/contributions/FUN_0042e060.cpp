struct FUN_00436b20 {
    unsigned int unk00;
    unsigned int unk04;
    unsigned int unk08;
    unsigned int unk0c;
    FUN_00436b20(unsigned int a, unsigned int b);
};
struct FUN_0042e060_class {
    void* __thiscall FUN_00410220(unsigned char type);
    void __thiscall FUN_00410020(void* extra, bool remove);
    void __thiscall FUN_0040ff60(void* extra);
    void __thiscall FUN_0042e060(unsigned int a, unsigned int b);
};
void FUN_0042e060_class::FUN_0042e060(unsigned int a, unsigned int b)
{
    void* previous = FUN_00410220(0x55);
    if (previous)
        FUN_00410020(previous, true);
    previous = new FUN_00436b20(a, b);
    FUN_0040ff60(previous);
}
