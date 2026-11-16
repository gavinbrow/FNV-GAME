struct Delegate {
    virtual void slot00(void*) = 0;
    virtual void slot01(void*) = 0;
    virtual void slot02(void*) = 0;
    virtual void slot03(void*) = 0;
    virtual void slot04(void*) = 0;
    virtual void slot05(void*) = 0;
    virtual void slot06(void*) = 0;
    virtual void slot07(void*) = 0;
    virtual void slot08(void*) = 0;
    virtual void slot09(void*) = 0;
    virtual void slot10(void*) = 0;
    virtual void slot11(void*) = 0;
    virtual void slot12(void*) = 0;
    virtual void slot13(void*) = 0;
    virtual void slot14(void*) = 0;
    virtual void Target(void*) = 0;
};
struct Wrapper {
    Delegate* delegate;
    void* value;
    void FUN_00dbaa00();
};
void Wrapper::FUN_00dbaa00()
{
    delegate->Target(value);
}

