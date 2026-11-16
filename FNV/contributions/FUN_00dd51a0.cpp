extern void* DAT_010d7ba8;

struct FUN_00dd5150_component {
    void FUN_00dd5150(int value);
};

struct FUN_00dd51a0 {
    void** vftable;
    short unk04;
    short enabled06;
    FUN_00dd5150_component component08;

    FUN_00dd51a0(const int* data);
    void FUN_00dd5170(const int* data);
};

FUN_00dd51a0::FUN_00dd51a0(const int* data) {
    enabled06 = 1;
    vftable = &DAT_010d7ba8;
    component08.FUN_00dd5150(0);
    FUN_00dd5170(data);
}
