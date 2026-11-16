struct FUN_00df71c0_Value {
    int unk00;
    float value;
};
struct FUN_00df71c0_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00df71c0_Value* unk10;
    float FUN_00df71c0();
};
float FUN_00df71c0_Class::FUN_00df71c0() {
    return unk10->value;
}
