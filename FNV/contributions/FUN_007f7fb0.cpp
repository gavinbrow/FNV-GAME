struct FUN_007f7fb0_Value {
    unsigned int field00;
    unsigned int field04;
    unsigned int field08;
    unsigned int field0C;
};

struct FUN_007f7fb0_Class {
    unsigned char unk00[0xC0];
    FUN_007f7fb0_Value unkC0;

    void __thiscall FUN_007f7fb0(const FUN_007f7fb0_Value* value);
};

void __thiscall FUN_007f7fb0_Class::FUN_007f7fb0(const FUN_007f7fb0_Value* value)
{
    unkC0 = *value;
}