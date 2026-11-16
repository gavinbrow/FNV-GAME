struct Target {
    virtual void slot0();
    virtual void slot1();
    virtual void slot2();
    virtual void slot3();
    virtual void slot4();
    virtual void slot5();
    virtual void invoke();
};
struct Wrapper {
    Target* target;
    void FUN_00dba6f0();
};
void Wrapper::FUN_00dba6f0() {
    target->invoke();
}