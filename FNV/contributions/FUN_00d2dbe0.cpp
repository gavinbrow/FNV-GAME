struct FUN_00d2dbe0;
struct Callback { virtual void Reserved0(); virtual void Reserved1(); virtual void Run(FUN_00d2dbe0*, int); };
struct Result { int unk00[4]; Callback* callback; };
struct FUN_00d2dbe0
{
    int unk00[3];
    Result* result;
    Result* FUN_00c85750();
    virtual void Virtual0();
    FUN_00d2dbe0(unsigned int flags);
};
FUN_00d2dbe0::FUN_00d2dbe0(unsigned int flags)
{
    if (flags & 1) {
        Result* value = FUN_00c85750();
        value->callback->Run(this, 8);
    }
}

