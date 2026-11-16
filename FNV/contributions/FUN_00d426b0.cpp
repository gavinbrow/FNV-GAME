struct InterfaceA {
    virtual void First(int);
    virtual void V1(); virtual void V2(); virtual void V3(); virtual void V4();
    virtual void V5(); virtual void V6(); virtual void V7(); virtual void V8();
    virtual void V9(); virtual void V10(); virtual void V11();
    virtual void Dispatch(int, int);
};
struct InterfaceB {
    virtual void First(int);
    virtual void V1(); virtual void V2(); virtual void V3(); virtual void V4();
    virtual void V5(); virtual void V6(); virtual void V7(); virtual void V8();
    virtual void V9(); virtual void V10(); virtual void V11();
    virtual void Dispatch(int, int);
};
struct Owner {
    virtual void First(int);
    virtual void V1(); virtual void V2(); virtual void V3(); virtual void V4();
    virtual void V5(); virtual void V6(); virtual void V7(); virtual void V8();
    virtual void V9(); virtual void V10(); virtual void V11();
    int unk04;
    int unk08;
    int argA;
    int argB;
    InterfaceA* first;
    InterfaceB* second;
    int selectorA;
    int selectorB;
    void FUN_00d426b0(int);
};
void Owner::FUN_00d426b0(int) {
    if (selectorA == 0x1D)
        first->Dispatch(argA, argB);
    if (selectorB == 0x1D)
        second->Dispatch(argB, argA);
    First(1);
}

