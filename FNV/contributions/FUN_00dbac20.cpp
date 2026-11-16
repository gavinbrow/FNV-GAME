struct Interface {
    virtual void slot0();
    virtual void slot1();
    virtual void slot2();
    virtual void slot3();
    virtual void slot4();
    virtual void slot5();
    virtual unsigned int getValue();
};
struct FUN_00dba650 {
    unsigned int value;
    __declspec(noinline) FUN_00dba650(unsigned int newValue);
};
FUN_00dba650::FUN_00dba650(unsigned int newValue) : value(newValue) {}
struct Holder {
    Interface* interfaceObject;
    FUN_00dba650 __thiscall FUN_00dbac20();
};
FUN_00dba650 Holder::FUN_00dbac20() {
    return FUN_00dba650(interfaceObject->getValue());
}
