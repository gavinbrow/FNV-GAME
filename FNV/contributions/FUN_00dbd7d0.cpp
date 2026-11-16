struct Inner {
    virtual void f0(); virtual void f1(); virtual void f2(); virtual void f3();
    virtual void f4(); virtual void f5(); virtual void f6(); virtual void f7();
    virtual int f8();
};
struct FUN_00dbd7d0_Class {
    int unk00; int unk04; Inner* object; int offset;
    int FUN_00dbd7d0();
};
int FUN_00dbd7d0_Class::FUN_00dbd7d0()
{
    return object->f8() - offset;
}
