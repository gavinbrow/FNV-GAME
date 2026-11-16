struct FUN_0044edd0_Disposable {
    unsigned int value;
    ~FUN_0044edd0_Disposable();
};
struct FUN_0044edd0_owner {
    virtual void OnMessage0();
    virtual void OnMessage1();
    virtual void OnMessage2();
    virtual void OnMessage3();
    virtual void OnMessage4();
    virtual void OnMessage5();
    virtual void OnMessage6();
    virtual void OnMessage7();
    virtual void OnMessage8();
    virtual void OnMessage9();
    virtual void OnMessage10(unsigned int value);
    void FUN_0044edd0(FUN_0044edd0_Disposable* object);
};
void FUN_0044edd0_owner::FUN_0044edd0(FUN_0044edd0_Disposable* object)
{
    OnMessage10(object->value);
    delete object;
}
