struct CallbackTarget {
    virtual void unk00();
    virtual void unk04();
    virtual void unk08();
    virtual void Send(void* value);
};
struct FUN_00dbd730_class {
    int unk00; int unk04; CallbackTarget* target;
    void* FUN_00dbd730(void* value);
};
void* FUN_00dbd730_class::FUN_00dbd730(void* value) {
    target->Send(value);
    return value;
}
