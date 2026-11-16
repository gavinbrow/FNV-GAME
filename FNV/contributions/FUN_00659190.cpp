struct FUN_00659190_class
{
    void* unk00;
    unsigned int unk04;

    bool __thiscall FUN_005ca4f0();
    unsigned char* __thiscall FUN_0060b980();

    FUN_00659190_class* __thiscall FUN_00659190();
};

FUN_00659190_class* __thiscall FUN_00659190_class::FUN_00659190()
{
    if (!FUN_005ca4f0())
        FUN_00ec7c56();

    do
    {
    } while (0);

    if (unk04 >= *reinterpret_cast<unsigned int*>(FUN_0060b980() + 0x10))
        FUN_00ec7c56();

    do
    {
    } while (0);

    unk04 += 4;
    return this;
}