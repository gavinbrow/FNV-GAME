struct DispatchObject {
    virtual void slot0();
    virtual void slot1();
    virtual void slot2();
    virtual void slot3();
    virtual void slot4();
    virtual void slot5();
    virtual void slot6();
    virtual void slot7();
    virtual void slot8();
    virtual void slot9();
    virtual void invoke(void* value, int flag);
};
struct Owner : DispatchObject {
    int unk04;
    void* unk08;
    void FUN_00d2bdf0();
};
void Owner::FUN_00d2bdf0() {
    invoke(unk08, 0);
}
