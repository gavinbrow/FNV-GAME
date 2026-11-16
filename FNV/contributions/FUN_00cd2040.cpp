struct FUN_00cd10a0_Class {
    void FUN_00cd10a0(int value);
};
struct FUN_00cd2040_Class {
    void FUN_00cd2040(int value);
};
void FUN_00cd2040_Class::FUN_00cd2040(int value) {
    FUN_00cd10a0_Class* target = *(FUN_00cd10a0_Class**)((char*)this - 0x5c);
    if (target) target->FUN_00cd10a0(value);
}
