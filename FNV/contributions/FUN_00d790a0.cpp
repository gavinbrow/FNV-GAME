struct FUN_00d83430_class {
    void FUN_00d83430(int, int, int, float);
};
struct FUN_00d790a0_class {
    int unk00;
    int unk04;
    FUN_00d83430_class* unk08;
    void FUN_00d790a0(int a, int b, int c, float d);
};
void FUN_00d790a0_class::FUN_00d790a0(int a, int b, int c, float d) {
    unk08->FUN_00d83430(a, b, c, d);
}
