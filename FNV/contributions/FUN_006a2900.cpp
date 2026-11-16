extern int DAT_0106b460;

struct FUN_006a2900_shell {
    int* vtable;
    void FUN_008454f0(int initialize);
    void FUN_006a2900();
};

void FUN_006a2900_shell::FUN_006a2900() {
    vtable = &DAT_0106b460;
    FUN_008454f0(1);
}