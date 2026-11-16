
struct BSSpinLock { void Lock(const char*); void Unlock(); };
struct Item {
    bool FUN_0044e550();
    bool FUN_0044e680();
    bool FUN_00528bb0();
};
struct Iteration {
    int unk00;
    unsigned int index;
    unsigned int value;
    bool FUN_006ebde0();
    bool FUN_0044de20();
    void FUN_0044de40(bool);
    void FUN_0044de80(bool);
};
struct FUN_0044b8d0_Class {
    int unk00,unk04,unk08,unk0c,unk10,unk14,unk18,unk1c;
    BSSpinLock lock;
    Item* FUN_00449f80(unsigned int, unsigned int*, unsigned int);
    Item* FUN_00449f80(unsigned int);
    unsigned int FUN_0044ddc0();
    bool FUN_0044b8d0(Iteration*, unsigned int*, unsigned int, bool);
};
bool FUN_0044b8d0_Class::FUN_0044b8d0(Iteration* it, unsigned int* result, unsigned int extra, bool retry) {
    lock.Lock(0);
    bool success = false;
    if (it->FUN_006ebde0()) {
        success = false;
    } else {
        while (true) {
            if (!it->FUN_0044de20()) {
                success = FUN_00449f80(it->index, &it->value, extra)->FUN_0044e550();
                it->FUN_0044de40(true);
            } else {
                success = FUN_00449f80(it->index, &it->value, extra)->FUN_0044e680();
            }
            if (!success) {
                it->index++;
                if (it->index >= FUN_0044ddc0()) {
                    it->FUN_0044de80(true);
                } else if (retry) {
                    it->FUN_0044de40(false);
                    continue;
                }
            } else {
                *result = it->value;
            }
            break;
        }
    }
    if (success) {
        success = FUN_00449f80(*result)->FUN_00528bb0();
    }
    lock.Unlock();
    return success;
}