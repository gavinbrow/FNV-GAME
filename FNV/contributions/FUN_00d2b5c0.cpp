struct FUN_00cb18f0_t {
    int FUN_00cb1fb0(int value);
    void FUN_00cb1870(int managerValue, int value, int flag);
};
struct FUN_00c85750_return { int unk00; int unk04; int unk08; int unk0c; int unk10; };
FUN_00c85750_return* __cdecl FUN_00c85750();
struct FUN_00d2b5c0_class {
    int unk00;
    int unk04;
    FUN_00cb18f0_t sub;
    void FUN_00d2b5c0(int value, char flag);
};
void FUN_00d2b5c0_class::FUN_00d2b5c0(int value, char flag) {
    if (flag != 0) {
        sub.FUN_00cb1fb0(value);
        return;
    }
    FUN_00c85750_return* manager = FUN_00c85750();
    sub.FUN_00cb1870(manager->unk10, value, 1);
}
