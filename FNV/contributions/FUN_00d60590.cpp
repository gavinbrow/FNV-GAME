extern int DAT_010d14f8;
extern int DAT_0102e388;

struct D60590Callback {
    void FUN_00c905b0();
};

struct D60590Object {
    int* vtable;
    int unk04;
    D60590Callback* callback;

    void FUN_00d60590();
};

void D60590Object::FUN_00d60590() {
    vtable = &DAT_010d14f8;
    callback->FUN_00c905b0();
    vtable = &DAT_0102e388;
}
