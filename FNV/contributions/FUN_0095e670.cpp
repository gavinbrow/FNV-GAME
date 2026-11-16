struct Item { int FUN_0084e3a0(); };
struct Ref { int FUN_004459e0(int); };
struct Controller {
    void FUN_008c1d20(Item*, int);
    Ref* FUN_00576260(Item*, int);
    void FUN_0094c950(Item*);
    void FUN_0095e670(Item*, int);
};
void Controller::FUN_0095e670(Item* item, int mode) {
    FUN_008c1d20(item, mode);
    Ref* ref = FUN_00576260(item, item->FUN_0084e3a0());
    if (ref) {
        Ref* selectedRef = ref;
        Ref* activeRef = selectedRef;
        activeRef ? activeRef->FUN_004459e0(1) : 0;
        FUN_0094c950(item);
    } else {
        FUN_0094c950(0);
    }
}