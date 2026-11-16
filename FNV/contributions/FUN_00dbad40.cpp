struct Delegate {
    virtual void slot00(void*, void*) = 0;
    virtual void slot01(void*, void*) = 0;
    virtual void slot02(void*, void*) = 0;
    virtual void slot03(void*, void*) = 0;
    virtual void slot04(void*, void*) = 0;
    virtual void slot05(void*, void*) = 0;
    virtual void slot06(void*, void*) = 0;
    virtual void slot07(void*, void*) = 0;
    virtual void slot08(void*, void*) = 0;
    virtual void slot09(void*, void*) = 0;
    virtual void slot10(void*, void*) = 0;
    virtual void slot11(void*, void*) = 0;
    virtual void slot12(void*, void*) = 0;
    virtual void slot13(void*, void*) = 0;
    virtual void slot14(void*, void*) = 0;
    virtual void Target(void*, void*) = 0;
};
struct Wrapper {
    Delegate* delegate;
    void* value;
    void FUN_00dbad40(void*);
};
void Wrapper::FUN_00dbad40(void* arg)
{
    delegate->Target(value, arg);
}
