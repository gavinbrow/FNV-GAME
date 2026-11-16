struct FUN_00df9840_Class {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    void* member10;
    int unk14;
    volatile long* member18;
    void FUN_00df9840();
};
void FUN_00df9840_Class::FUN_00df9840() {
    if (member18) {
        InterlockedExchangeAdd(member18, 1);
    }
    if (member10) {
        FUN_00d043c0(member10, 1);
    }
}
