struct TargetObject {
    bool FUN_00449110();
    void FUN_006faa30(void* destination);
    void FUN_006f6250(void* destination);
};
struct SmartRef {
    void* value;
    TargetObject* FUN_00559450();
    void FUN_006f74f0(int value);
};
struct Owner {
    int unk00;
    void* firstDestination;
    void* secondDestination;
    int unk0c;
    void* thirdDestination;
    int unk14;
    SmartRef firstReference;
    SmartRef secondReference;
    bool completed;
    void FUN_006f6150(bool update);
};
void Owner::FUN_006f6150(bool update) {
    if (firstReference.FUN_00559450() != 0) {
        if (firstReference.FUN_00559450()->FUN_00449110()) {
            if (update) {
                firstReference.FUN_00559450()->FUN_006faa30(&firstDestination);
                firstReference.FUN_00559450()->FUN_006f6250(&secondDestination);
            }
            firstReference.FUN_006f74f0(0);
            if (secondReference.FUN_00559450() == 0) completed = true;
        }
    }
    if (secondReference.FUN_00559450() != 0) {
        if (secondReference.FUN_00559450()->FUN_00449110()) {
            if (update) secondReference.FUN_00559450()->FUN_006f6250(&thirdDestination);
            secondReference.FUN_006f74f0(0);
            if (firstReference.FUN_00559450() == 0) completed = true;
        }
    }
}



