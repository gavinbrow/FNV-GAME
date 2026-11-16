struct DispatchInterface {
    virtual int slot00() = 0; virtual int slot04() = 0;
    virtual int slot08() = 0; virtual int slot0c() = 0;
    virtual int slot10() = 0; virtual int slot14() = 0;
    virtual int slot18() = 0; virtual int slot1c() = 0;
    virtual int slot20() = 0; virtual int slot24() = 0;
    virtual int slot28() = 0; virtual int slot2c() = 0;
    virtual int slot30() = 0; virtual int slot34() = 0;
    virtual int slot38() = 0; virtual int slot3c() = 0;
    virtual int Dispatch(int address) = 0;
};
struct DispatchHolder {
    void* member00; void* member04; void* member08; void* member0c;
    void* member10; void* member14; void* member18; void* member1c;
    DispatchInterface* volatile member20;
};
struct DispatchAdapter {
    void* member00; void* member04; void* member08;
    DispatchHolder* member0c; int member10;
    int FUN_00dc7160(int offset);
};
int DispatchAdapter::FUN_00dc7160(int offset) {
    DispatchInterface* receiver = member0c->member20;
    return receiver->Dispatch(member10 + offset);
}