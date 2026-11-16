struct FUN_00d67970_helper
{
    void __thiscall c93920(void* value);
    void __thiscall c93a20(void* value);
};

struct FUN_00d67970_class
{
    void* unk00;
    void* unk04;
    void* unk08;
    void* unk0c;

    void __thiscall FUN_00d67970(FUN_00d67970_helper* helper);
};

void __thiscall FUN_00d67970_class::FUN_00d67970(FUN_00d67970_helper* helper)
{
    void* base = reinterpret_cast<char*>(this) - 0x20;
    void* value;

    if (base)
        value = &unk0c;
    else
        value = 0;

    helper->c93920(value);

    if (base)
        value = &unk08;
    else
        value = 0;

    helper->c93a20(value);
}