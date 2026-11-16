struct SubObject
{
    virtual void* unk00();
    virtual void* unk04();
    virtual void* unk08();
    virtual void* unk0c();
    virtual void __thiscall invoke(int* value, int mode);
};
struct FUN_00cc01a0_class
{
    int unk00;
    int unk04;
    SubObject* unk08;
    FUN_00cc01a0_class* __thiscall FUN_00cc01a0(int value);
};
FUN_00cc01a0_class* __thiscall FUN_00cc01a0_class::FUN_00cc01a0(int value)
{
    unk08->invoke(&value, 1);
    return this;
}
