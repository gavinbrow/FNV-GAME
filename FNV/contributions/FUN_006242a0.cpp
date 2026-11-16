struct ActivationBaseA {
    int value;
};
struct ActivationBaseB {
    int value;
};
struct ActivationListener {
    void FUN_00c938a0(void* owner);
    void FUN_00c93820(ActivationBaseB* owner);
};
struct FUN_006242a0_cls : ActivationBaseA, ActivationBaseB {
    void FUN_006242a0(ActivationListener* listener);
};
void FUN_006242a0_cls::FUN_006242a0(ActivationListener* listener) {
    if (listener) {
        listener->FUN_00c938a0(this);
        listener->FUN_00c93820(static_cast<ActivationBaseB*>(this));
    }
}
