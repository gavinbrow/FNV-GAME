struct FUN_00561580_class {
    void FUN_00561580(bool enabled);
};
struct FUN_00c671b0_dispatch {
    virtual void vf00();
    virtual void vf04();
    virtual void vf08();
    virtual void vf0c();
    virtual void vf10();
    virtual void vf14();
    virtual void vf18();
    virtual void vf1c();
    virtual void vf20();
    virtual void vf24();
    virtual void vf28();
    virtual void vf2c();
    virtual void vf30();
    virtual void vf34();
    virtual void vf38();
    virtual void vf3c();
    virtual FUN_00561580_class* vf40();
};
struct FUN_00c671b0_source {
    int unk00;
    int unk04;
    int unk08;
    int unk0c;
    FUN_00c671b0_dispatch* dispatcher;
};
struct FUN_00c671b0_state {
    int unk00;
    int unk04;
    int unk08;
    int enabled;
};
void __cdecl FUN_00c671b0(FUN_00c671b0_source* source, FUN_00c671b0_state* state) {
    if (source) {
        FUN_00c671b0_dispatch* dispatcher = source->dispatcher;
        if (dispatcher) {
            FUN_00561580_class* object = dispatcher->vf40();
            if (object) object->FUN_00561580(state->enabled != 0);
        }
    }
}
