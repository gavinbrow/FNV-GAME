struct FUN_00626490_Class {
    int FUN_00cb1930(int first, int second);
};
struct FUN_00d2b3b0_Class {
    int unk00;
    int unk04;
    FUN_00626490_Class helper;
    unsigned char* FUN_00d2b3b0(unsigned char* result, int value);
};
unsigned char* FUN_00d2b3b0_Class::FUN_00d2b3b0(unsigned char* result, int value) {
    *result = (helper.FUN_00cb1930(value, 0) == 0);
    return result;
}
