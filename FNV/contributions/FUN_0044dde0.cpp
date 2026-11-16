struct Dispatch {
    virtual void Slot00();
    virtual void Slot01();
    virtual void Slot02();
    virtual void Slot03();
    virtual void Slot04();
    virtual void Slot05();
    virtual void Slot06();
    virtual void Slot07();
    virtual void Slot08();
    virtual void Slot09();
    virtual void Slot0A(unsigned int value);
    void FUN_0044dde0(unsigned int* argument);
};
void __cdecl FUN_00401030(void* object);
void Dispatch::FUN_0044dde0(unsigned int* argument) {
    Slot0A(*argument);
    void* target = argument;
    FUN_00401030(target);
}