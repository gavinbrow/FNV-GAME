struct VirtualBase {
    virtual void v0();
    virtual void v1();
    virtual void v2();
    virtual void v3();
    virtual void v4();
    virtual void v5();
    virtual void v6();
    virtual void Dispatch();
};
struct FUN_00ddf020_Class {
    void __thiscall FUN_00ddf020();
};
void __thiscall FUN_00ddf020_Class::FUN_00ddf020()
{
    ((VirtualBase*)this)->Dispatch();
}
